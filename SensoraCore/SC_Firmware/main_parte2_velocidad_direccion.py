# main_parte2_velocidad_direccion.py - SensoraCore Alpha 0.4
# Módulos: Optical Speed, IR Steering
# Pantalla OLED 128x64 I2C integrada
# Autor: SensoraCore Team
# Fecha: 2025-11-21

import network  # type: ignore
import socket
import time
from machine import Pin, ADC, reset, PWM, I2C  # type: ignore
import ssd1306  # type: ignore
from red import SSID, PASSWORD  # type: ignore

# ============================================================================
# CONFIGURACIÓN INICIAL
# ============================================================================

print("=" * 50)
print("SensoraCore ESP32 - Parte 2: Velocidad y Dirección")
print("=" * 50)
time.sleep(2)

# ============================================================================
# CONFIGURACIÓN PANTALLA OLED 128x64 I2C
# ============================================================================

try:
    # I2C en GPIO21 (SDA) y GPIO22 (SCL) - pines estándar ESP32
    i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)
    oled = ssd1306.SSD1306_I2C(128, 64, i2c)
    oled_enabled = True
    print("[OLED] ✓ Pantalla inicializada")
except Exception as e:
    oled_enabled = False
    oled = None
    print(f"[OLED] ✗ No disponible: {e}")

def oled_clear():
    """Limpia la pantalla OLED"""
    if oled_enabled and oled:
        try:
            oled.fill(0)
            oled.show()
        except Exception:
            pass

def oled_write(line1="", line2="", line3="", line4="", line5=""):
    """Escribe hasta 5 líneas en la pantalla OLED"""
    if not oled_enabled or not oled:
        return
    try:
        oled.fill(0)
        if line1: oled.text(line1[:16], 0, 0)
        if line2: oled.text(line2[:16], 0, 13)
        if line3: oled.text(line3[:16], 0, 26)
        if line4: oled.text(line4[:16], 0, 39)
        if line5: oled.text(line5[:16], 0, 52)
        oled.show()
    except Exception:
        pass

def oled_status(mode="Esperando..."):
    """Muestra estado del sistema en OLED"""
    if not oled_enabled or not oled:
        return
    try:
        oled.fill(0)
        oled.text("SensoraCore P2", 0, 0)
        oled.text("Veloc & Direcc", 0, 13)
        oled.text("-" * 16, 0, 26)
        if mode == "Esperando...":
            ip = sta.ifconfig()[0]
            oled.text(f"IP: {ip}", 0, 39)
            oled.text("Esperando...", 0, 52)
        else:
            oled.text(f"Modo:", 0, 39)
            oled.text(mode[:16], 0, 52)
        oled.show()
    except Exception:
        pass

# Mostrar pantalla de inicio
oled_write("SensoraCore P2", "Veloc & Direcc", "", "Iniciando...", "WiFi connecting")

# ============================================================================
# CONFIGURACIÓN DE HARDWARE - PINES GPIO
# ============================================================================

# LED integrado
led = Pin(2, Pin.OUT)

# --- MÓDULO: OPTICAL SPEED (Encoders + Control de motores) ---
# Encoders con módulo LM393 FC-03 (comparador + salida digital D0)
# Especificaciones: 15 ranuras, genera 2 pulsos por ranura (rising+falling)
# Resolución: 30 PPR (pulsos por revolución), diámetro disco 25mm
enc_left = Pin(34, Pin.IN, Pin.PULL_UP)   # D0 Encoder izquierdo (GPIO 12)
enc_right = Pin(35, Pin.IN, Pin.PULL_UP)  # D0 Encoder derecho (GPIO 35)

# Control de motores L298N
# Motor Izquierdo (ENA)
in1_pwm = PWM(Pin(32))  # IN1 - Adelante izquierdo
in2_pwm = PWM(Pin(33))  # IN2 - Atrás izquierdo
# Motor Derecho (ENB)
in3_pwm = PWM(Pin(25))  # IN3 - Adelante derecho
in4_pwm = PWM(Pin(26))  # IN4 - Atrás derecho

# Configurar frecuencia PWM para los motores
for pwm_pin in [in1_pwm, in2_pwm, in3_pwm, in4_pwm]:
    try:
        pwm_pin.freq(1000)  # 1 kHz
    except Exception:
        pass

# --- MÓDULO: IR STEERING (5 sensores IR + PID) ---
ir_sensors = [
    Pin(19, Pin.IN, Pin.PULL_UP),   # Sensor 1 (más a la izquierda)
    Pin(18, Pin.IN, Pin.PULL_UP),  # Sensor 2
    Pin(5, Pin.IN, Pin.PULL_UP),  # Sensor 3 (centro)
    Pin(17, Pin.IN, Pin.PULL_UP),  # Sensor 4
    Pin(16, Pin.IN, Pin.PULL_UP)   # Sensor 5 (más a la derecha)
]

# ============================================================================
# VARIABLES GLOBALES
# ============================================================================

# Estado del servidor
current_mode = None
continuous_client = None

# Variables del módulo Optical Speed
_speed_percent = 0  # Velocidad -100 a +100
_ppr = 30           # Pulsos por revolución (15 ranuras × 2 flancos = 30 PPR)
_cnt_left = 0       # Contador encoder izquierdo
_cnt_right = 0      # Contador encoder derecho
_last_left_time = 0 # Último tiempo IRQ izquierdo (debounce)
_last_right_time = 0 # Último tiempo IRQ derecho (debounce)
_debounce_us = 200   # Debounce de 0.2ms para mejor detección

# Variables del módulo IR Steering (PID)
_kp, _ki, _kd = 1.0, 0.0, 0.5  # Parámetros PID
_base_speed = 40                # Velocidad base -100 a +100
_err_integral = 0.0             # Error integral
_last_error = 0.0               # Último error

# ============================================================================
# FUNCIONES DE UTILIDAD
# ============================================================================

def pwm_set(pwm_obj, percent):
    """Configura el duty cycle de un pin PWM (0-100%)"""
    try:
        # MicroPython duty_u16: 0-65535
        duty = int(max(0, min(100, percent)) * 65535 / 100)
        pwm_obj.duty_u16(duty)
    except Exception:
        # Fallback duty: 0-1023
        duty = int(max(0, min(100, percent)) * 1023 / 100)
        pwm_obj.duty(duty)

# ============================================================================
# CONEXIÓN WIFI
# ============================================================================

def connect_wifi():
    """Conecta al WiFi con reintentos y manejo de errores"""
    print("\n[WiFi] Iniciando conexión...")
    sta = network.WLAN(network.STA_IF)
    
    sta.active(False)
    time.sleep(1)
    sta.active(True)
    
    max_attempts = 5
    
    for attempt in range(1, max_attempts + 1):
        try:
            print(f"[WiFi] Intento {attempt}/{max_attempts}: Conectando a '{SSID}'...")
            oled_write("SensoraCore P2", "WiFi...", f"Intento {attempt}/5", "", "")
            
            if sta.isconnected():
                sta.disconnect()
                time.sleep(1)
            
            sta.connect(SSID, PASSWORD)
            
            timeout = 15
            start_time = time.time()
            
            while not sta.isconnected() and (time.time() - start_time) < timeout:
                time.sleep(0.5)
                led.value(not led.value())
            
            if sta.isconnected():
                led.value(1)
                ip = sta.ifconfig()[0]
                print(f"[WiFi] ✓ Conectado: {ip}")
                oled_write("WiFi OK!", ip, "", "Servidor", "iniciando...")
                time.sleep(2)
                return sta
            else:
                print(f"[WiFi] ✗ Timeout en intento {attempt}")
                
        except OSError as e:
            print(f"[WiFi] ✗ Error OSError: {e}")
        except Exception as e:
            print(f"[WiFi] ✗ Error: {e}")
        
        if attempt < max_attempts:
            time.sleep(2)
    
    print("[WiFi] ✗✗✗ ERROR CRÍTICO: No se pudo conectar")
    oled_write("ERROR WiFi", "No conectado", "", "Reiniciando...", "")
    time.sleep(3)
    return None

sta = connect_wifi()
if not sta:
    print("[Sistema] Reiniciando...")
    reset()

# ============================================================================
# SERVIDOR TCP
# ============================================================================

def create_server():
    """Crea el servidor TCP en el puerto 8080"""
    try:
        addr = socket.getaddrinfo('0.0.0.0', 8080)[0][-1]
        s = socket.socket()
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(addr)
        s.listen(1)
        print(f"\n[Servidor] ✓ Iniciado en puerto 8080")
        print(f"[Servidor] IP: {sta.ifconfig()[0]}:8080")
        return s
    except Exception as e:
        print(f"[Servidor] ✗ Error: {e}")
        return None

server = create_server()
if not server:
    print("[Sistema] Reiniciando...")
    oled_write("ERROR", "Servidor", "no inicio", "", "Reiniciando")
    time.sleep(3)
    reset()

# ============================================================================
# ANIMACIÓN DE ENTRADA - VELOCIDAD Y DIRECCIÓN
# ============================================================================

def animation_speed_direction():
    """
    Animación de entrada: Automóvil acelerando → Transición líquida → Volante girando
    Duración: 20 segundos
    Non-blocking: permite interrupción por conexión entrante
    """
    if not oled_enabled or not oled:
        return
    
    print("[Animación] Iniciando secuencia de entrada...")
    start_time = time.ticks_ms()
    duration_ms = 20000  # 20 segundos
    
    try:
        # FASE 1: Velocímetro analógico acelerando (0-7s)
        phase_duration = 7000
        phase_start = time.ticks_ms()
        while time.ticks_diff(time.ticks_ms(), phase_start) < phase_duration:
            if time.ticks_diff(time.ticks_ms(), start_time) >= duration_ms:
                return
            
            oled.fill(0)
            
            progress = time.ticks_diff(time.ticks_ms(), phase_start) / phase_duration
            
            # Centro y radio del velocímetro
            cx, cy, r = 64, 45, 30
            
            import math
            
            # Arco del velocímetro (de 135° a 45° = 270° total)
            start_angle = 135
            end_angle = 45
            for angle in range(start_angle, 360):
                rad = math.radians(angle)
                x = int(cx + r * math.cos(rad))
                y = int(cy + r * math.sin(rad))
                if 0 <= x < 128 and 0 <= y < 64:
                    oled.pixel(x, y, 1)
            for angle in range(0, end_angle + 1):
                rad = math.radians(angle)
                x = int(cx + r * math.cos(rad))
                y = int(cy + r * math.sin(rad))
                if 0 <= x < 128 and 0 <= y < 64:
                    oled.pixel(x, y, 1)
            
            # Marcas de velocidad (cada 30°, total 9 marcas)
            for i in range(10):
                angle = 135 + i * 27  # 270° / 10 marcas
                if angle >= 360:
                    angle -= 360
                rad = math.radians(angle)
                x1 = int(cx + r * math.cos(rad))
                y1 = int(cy + r * math.sin(rad))
                x2 = int(cx + (r - 5) * math.cos(rad))
                y2 = int(cy + (r - 5) * math.sin(rad))
                oled.line(x1, y1, x2, y2, 1)
            
            # Aguja que acelera (de 135° a 45°)
            needle_angle = 135 + progress * 270
            if needle_angle >= 360:
                needle_angle -= 360
            rad = math.radians(needle_angle)
            
            # Aguja gruesa
            needle_length = r - 8
            x_end = int(cx + needle_length * math.cos(rad))
            y_end = int(cy + needle_length * math.sin(rad))
            
            # Dibujar aguja con grosor (3 líneas paralelas)
            oled.line(cx, cy, x_end, y_end, 1)
            offset_x = int(math.sin(rad) * 1)
            offset_y = int(-math.cos(rad) * 1)
            oled.line(cx + offset_x, cy + offset_y, x_end + offset_x, y_end + offset_y, 1)
            oled.line(cx - offset_x, cy - offset_y, x_end - offset_x, y_end - offset_y, 1)
            
            # Centro de la aguja (pivote)
            oled.fill_rect(cx - 2, cy - 2, 5, 5, 1)
            
            # Líneas de velocidad radiales (efecto de movimiento)
            if progress > 0.3:
                num_lines = int(5 * progress)
                for i in range(num_lines):
                    line_angle = needle_angle + 10 + i * 8
                    if line_angle >= 360:
                        line_angle -= 360
                    rad_line = math.radians(line_angle)
                    x_start = int(cx + (r - 12) * math.cos(rad_line))
                    y_start = int(cy + (r - 12) * math.sin(rad_line))
                    x_end_line = int(cx + (r - 5) * math.cos(rad_line))
                    y_end_line = int(cy + (r - 5) * math.sin(rad_line))
                    if 0 <= x_start < 128 and 0 <= y_start < 64:
                        oled.line(x_start, y_start, x_end_line, y_end_line, 1)
            
            oled.show()
            time.sleep(0.05)
        
        # FASE 2: Transición del velocímetro al volante (7-13s)
        phase_duration = 6000
        phase_start = time.ticks_ms()
        while time.ticks_diff(time.ticks_ms(), phase_start) < phase_duration:
            if time.ticks_diff(time.ticks_ms(), start_time) >= duration_ms:
                return
            
            oled.fill(0)
            
            progress = time.ticks_diff(time.ticks_ms(), phase_start) / phase_duration
            
            # Centro de la pantalla
            cx, cy = 64, 32
            
            import math
            
            if progress < 0.5:
                # Primera mitad: el velocímetro se cierra en círculo completo
                t = progress * 2  # 0 a 1
                
                # Arco que va cerrándose (de semicírculo a círculo)
                r = 28
                # Ángulo inicial del arco (va de 135° → 0°)
                start_angle = int(135 * (1 - t))
                
                # Dibujar arco superior (siempre presente)
                for angle in range(start_angle, 360):
                    rad = math.radians(angle)
                    x = int(cx + r * math.cos(rad))
                    y = int(cy + r * math.sin(rad))
                    if 0 <= x < 128 and 0 <= y < 64:
                        oled.pixel(x, y, 1)
                
                # Arco inferior que se va completando
                for angle in range(0, int(45 + (135 - start_angle))):
                    rad = math.radians(angle)
                    x = int(cx + r * math.cos(rad))
                    y = int(cy + r * math.sin(rad))
                    if 0 <= x < 128 and 0 <= y < 64:
                        oled.pixel(x, y, 1)
                
                # Aguja que va girando hacia el centro (posición 0°)
                needle_angle = 45 - (45 * t)
                rad_needle = math.radians(needle_angle)
                needle_length = r - 8
                x_end = int(cx + needle_length * math.cos(rad_needle))
                y_end = int(cy + needle_length * math.sin(rad_needle))
                oled.line(cx, cy, x_end, y_end, 1)
                
                # Centro
                oled.fill_rect(cx - 2, cy - 2, 5, 5, 1)
                
            else:
                # Segunda mitad: emerge el volante desde el círculo
                t = (progress - 0.5) * 2  # 0 a 1
                
                # Círculo exterior del volante (con doble línea para grosor)
                r_outer = 26
                for angle in range(0, 360, 2):
                    rad = math.radians(angle)
                    x = int(cx + r_outer * math.cos(rad))
                    y = int(cy + r_outer * math.sin(rad))
                    if 0 <= x < 128 and 0 <= y < 64:
                        oled.pixel(x, y, 1)
                    # Segunda línea para grosor
                    x2 = int(cx + (r_outer - 1) * math.cos(rad))
                    y2 = int(cy + (r_outer - 1) * math.sin(rad))
                    if 0 <= x < 128 and 0 <= y < 64:
                        oled.pixel(x2, y2, 1)
                
                # Círculo interior del volante
                r_inner = int(10 * t)
                for angle in range(0, 360, 3):
                    rad = math.radians(angle)
                    x = int(cx + r_inner * math.cos(rad))
                    y = int(cy + r_inner * math.sin(rad))
                    if 0 <= x < 128 and 0 <= y < 64:
                        oled.pixel(x, y, 1)
                
                # Radios del volante (3 barras gruesas)
                if t > 0.3:
                    for spoke_angle in [90, 210, 330]:  # Posiciones estéticas
                        rad = math.radians(spoke_angle)
                        x1 = int(cx + r_inner * math.cos(rad))
                        y1 = int(cy + r_inner * math.sin(rad))
                        x2 = int(cx + (r_outer - 2) * math.cos(rad))
                        y2 = int(cy + (r_outer - 2) * math.sin(rad))
                        
                        # Línea central del radio
                        oled.line(x1, y1, x2, y2, 1)
                        
                        # Líneas paralelas para grosor (si t > 0.6)
                        if t > 0.6:
                            offset_x = int(math.sin(rad) * 1)
                            offset_y = int(-math.cos(rad) * 1)
                            oled.line(x1 + offset_x, y1 + offset_y, x2 + offset_x, y2 + offset_y, 1)
                            oled.line(x1 - offset_x, y1 - offset_y, x2 - offset_x, y2 - offset_y, 1)
                
                # Centro del volante
                oled.fill_rect(cx - 3, cy - 3, 7, 7, 1)
                oled.rect(cx - 2, cy - 2, 5, 5, 0)  # Hueco interior
            
            oled.show()
            time.sleep(0.05)
        
        # FASE 3: Volante girando (izquierda y derecha) (13-20s)
        phase_duration = 7000
        phase_start = time.ticks_ms()
        while time.ticks_diff(time.ticks_ms(), phase_start) < phase_duration:
            if time.ticks_diff(time.ticks_ms(), start_time) >= duration_ms:
                return
            
            oled.fill(0)
            
            progress = time.ticks_diff(time.ticks_ms(), phase_start) / phase_duration
            
            # Oscilación del volante: izquierda → derecha → centro
            import math
            rotation_angle = math.sin(progress * math.pi * 3) * 45  # Oscila 3 veces, ±45°
            
            cx, cy = 64, 32
            r_outer = 26
            r_inner = 10
            
            # Círculo exterior del volante (doble línea para grosor)
            for angle in range(0, 360, 2):
                rad = math.radians(angle)
                x = int(cx + r_outer * math.cos(rad))
                y = int(cy + r_outer * math.sin(rad))
                if 0 <= x < 128 and 0 <= y < 64:
                    oled.pixel(x, y, 1)
                # Segunda línea para grosor
                x2 = int(cx + (r_outer - 1) * math.cos(rad))
                y2 = int(cy + (r_outer - 1) * math.sin(rad))
                if 0 <= x < 128 and 0 <= y < 64:
                    oled.pixel(x2, y2, 1)
            
            # Círculo interior
            for angle in range(0, 360, 3):
                rad = math.radians(angle)
                x = int(cx + r_inner * math.cos(rad))
                y = int(cy + r_inner * math.sin(rad))
                if 0 <= x < 128 and 0 <= y < 64:
                    oled.pixel(x, y, 1)
            
            # Radios del volante rotados según rotation_angle (3 barras gruesas)
            for spoke_angle in [90, 210, 330]:
                rad = math.radians(spoke_angle + rotation_angle)
                x1 = int(cx + r_inner * math.cos(rad))
                y1 = int(cy + r_inner * math.sin(rad))
                x2 = int(cx + (r_outer - 2) * math.cos(rad))
                y2 = int(cy + (r_outer - 2) * math.sin(rad))
                
                # Línea central del radio
                oled.line(x1, y1, x2, y2, 1)
                
                # Líneas paralelas para grosor
                offset_x = int(math.sin(rad) * 1)
                offset_y = int(-math.cos(rad) * 1)
                oled.line(x1 + offset_x, y1 + offset_y, x2 + offset_x, y2 + offset_y, 1)
                oled.line(x1 - offset_x, y1 - offset_y, x2 - offset_x, y2 - offset_y, 1)
            
            # Centro del volante (botón de claxon)
            oled.fill_rect(cx - 3, cy - 3, 7, 7, 1)
            oled.rect(cx - 2, cy - 2, 5, 5, 0)  # Hueco interior
            
            # Indicador de dirección (flechas más elaboradas)
            if rotation_angle > 12:  # Girando a la derecha
                # Flecha derecha →
                oled.fill_rect(95, 30, 15, 3, 1)
                oled.fill_rect(107, 26, 3, 11, 1)
                oled.pixel(106, 27, 1)
                oled.pixel(106, 35, 1)
            elif rotation_angle < -12:  # Girando a la izquierda
                # Flecha izquierda ←
                oled.fill_rect(18, 30, 15, 3, 1)
                oled.fill_rect(18, 26, 3, 11, 1)
                oled.pixel(21, 27, 1)
                oled.pixel(21, 35, 1)
            
            oled.show()
            time.sleep(0.05)
        
        print("[Animación] Secuencia completada")
        
    except Exception as e:
        print(f"[Animación] Error: {e}")

# ============================================================================
# MÓDULO: OPTICAL SPEED (Encoders + Control PWM)
# ============================================================================

def encoder_left_irq(pin):
    """Handler IRQ para encoder izquierdo (LM393)"""
    global _cnt_left, _last_left_time
    now = time.ticks_us()
    if time.ticks_diff(now, _last_left_time) > _debounce_us:
        _cnt_left += 1
        _last_left_time = now

def encoder_right_irq(pin):
    """Handler IRQ para encoder derecho (LM393)"""
    global _cnt_right, _last_right_time
    now = time.ticks_us()
    if time.ticks_diff(now, _last_right_time) > _debounce_us:
        _cnt_right += 1
        _last_right_time = now

# Configurar interrupciones de encoders - ambos flancos para máxima resolución
try:
    enc_left.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=encoder_left_irq)
    enc_right.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=encoder_right_irq)
    print("[Encoders] ✓ Interrupciones configuradas en GPIO 12 (izq) y 35 (der)")
    print("[Encoders] ✓ Detectando rising + falling edges")
except Exception as e:
    print(f"[Encoders] ✗ Error configurando IRQ: {e}")

def apply_motor_speed(percent):
    """Aplica velocidad a ambos motores (-100 a +100)"""
    global _speed_percent
    
    percent = max(-100, min(100, int(percent)))
    _speed_percent = percent
    
    speed = abs(percent)
    
    # Motor izquierdo (IN1/IN2)
    if percent >= 0:
        pwm_set(in1_pwm, speed)
        pwm_set(in2_pwm, 0)
    else:
        pwm_set(in1_pwm, 0)
        pwm_set(in2_pwm, speed)
    
    # Motor derecho (IN3/IN4)
    if percent >= 0:
        pwm_set(in3_pwm, speed)
        pwm_set(in4_pwm, 0)
    else:
        pwm_set(in3_pwm, 0)
        pwm_set(in4_pwm, speed)

def stop_motors():
    """Detiene ambos motores"""
    apply_motor_speed(0)

def optical_speed_loop(client):
    """Loop del módulo de velocidad óptica con encoders LM393"""
    global current_mode, continuous_client, _cnt_left, _cnt_right, _ppr, _speed_percent
    
    print("[Optical Speed] Módulo activo")
    print(f"[Optical Speed] Encoder: 15 ranuras × 2 flancos = 30 PPR, Sensor LM393")
    print(f"[Optical Speed] Pines: GPIO12 (izq), GPIO35 (der)")
    print(f"[Optical Speed] Resolución: {_ppr} pulsos por revolución")
    oled_status("Optical Speed")
    
    # Reset contadores para nueva sesión
    _cnt_left = 0
    _cnt_right = 0
    
    # Aplicar velocidad inicial
    apply_motor_speed(_speed_percent)
    
    # Test inicial de detección de pulsos
    print(f"[Optical Speed] Test GPIO: enc_left={enc_left.value()} enc_right={enc_right.value()}")
    print("[Optical Speed] Esperando pulsos... (mueve los encoders manualmente si no hay movimiento)")
    
    last_cnt_left = 0
    last_cnt_right = 0
    last_time = time.ticks_ms()
    last_rpm_time = last_time
    last_oled_update = last_time
    last_send_time = last_time
    last_pulse_time_left = last_time
    last_pulse_time_right = last_time
    last_debug_time = last_time
    
    rpm_left = 0.0
    rpm_right = 0.0
    # Filtros de suavizado exponencial (EMA) - alpha = 0.4 para respuesta más rápida
    # Con 40 PPR tenemos mejor resolución, podemos usar filtro más ligero
    rpm_left_filtered = 0.0
    rpm_right_filtered = 0.0
    alpha = 0.4  # Factor de suavizado (0.0 = muy suave, 1.0 = sin filtro)
    
    try:
        while current_mode == 'OPTICAL_SPEED' and continuous_client == client:
            now = time.ticks_ms()
            
            # Procesar comandos no bloqueantes
            client.settimeout(0.01)
            try:
                cmd = client.recv(64)
                if cmd:
                    txt = cmd.decode().strip().upper()
                    
                    if txt.startswith('SET_SPEED:'):
                        try:
                            val = int(txt.split(':', 1)[1])
                            apply_motor_speed(val)
                            print(f"[Optical Speed] Velocidad cambiada a {val}%")
                        except Exception:
                            pass
                            
                    elif txt.startswith('SET_PPR:'):
                        try:
                            val = int(txt.split(':', 1)[1])
                            if val > 0:
                                _ppr = val
                                print(f"[Optical Speed] PPR cambiado a {val}")
                        except Exception:
                            pass
                            
                    elif 'STOP' in txt:
                        break
                        
            except Exception:
                pass
            
            # Detectar pulsos nuevos para actualizar timestamp
            if _cnt_left > last_cnt_left:
                last_pulse_time_left = now
            if _cnt_right > last_cnt_right:
                last_pulse_time_right = now
            
            # Calcular RPM cada 200ms
            if time.ticks_diff(now, last_rpm_time) >= 200:
                delta_left = _cnt_left - last_cnt_left
                delta_right = _cnt_right - last_cnt_right
                delta_time = time.ticks_diff(now, last_rpm_time) / 1000.0
                
                # Calcular RPM instantáneo
                if delta_time > 0 and _ppr > 0:
                    rpm_left_instant = (delta_left / delta_time) * (60.0 / _ppr)
                    rpm_right_instant = (delta_right / delta_time) * (60.0 / _ppr)
                else:
                    rpm_left_instant = 0.0
                    rpm_right_instant = 0.0
                
                # Detección de velocidad cero: si no hay pulsos en 300ms, RPM = 0
                # Con 40 PPR, incluso a 10 RPM hay pulsos cada ~150ms
                if time.ticks_diff(now, last_pulse_time_left) > 300:
                    rpm_left_instant = 0.0
                if time.ticks_diff(now, last_pulse_time_right) > 300:
                    rpm_right_instant = 0.0
                
                # Aplicar filtro de suavizado exponencial (EMA)
                # Si hay movimiento, suavizar; si es cero, resetear rápido
                if rpm_left_instant > 0 or delta_left > 0:
                    rpm_left_filtered = alpha * rpm_left_instant + (1 - alpha) * rpm_left_filtered
                else:
                    rpm_left_filtered = 0.0
                
                if rpm_right_instant > 0 or delta_right > 0:
                    rpm_right_filtered = alpha * rpm_right_instant + (1 - alpha) * rpm_right_filtered
                else:
                    rpm_right_filtered = 0.0
                
                # Usar valores filtrados
                rpm_left = rpm_left_filtered
                rpm_right = rpm_right_filtered
                
                last_cnt_left = _cnt_left
                last_cnt_right = _cnt_right
                last_rpm_time = now
                
                # Debug info cada segundo
                if time.ticks_diff(now, last_time) >= 1000:
                    print(f"[Optical Speed] RPM L:{rpm_left:.1f} R:{rpm_right:.1f} | Pulsos L:{_cnt_left} R:{_cnt_right} | Delta L:{delta_left} R:{delta_right} | Speed: {_speed_percent}%")
                    last_time = now
            
            # Debug de detección de pulsos cada 2 segundos
            if time.ticks_diff(now, last_debug_time) >= 2000:
                gpio_state_l = enc_left.value()
                gpio_state_r = enc_right.value()
                print(f"[Encoders DEBUG] Total pulsos: L={_cnt_left} R={_cnt_right} | GPIO: L={gpio_state_l} R={gpio_state_r}")
                last_debug_time = now
            
            # Enviar datos cada 100ms (10 Hz) - independiente del cálculo de RPM
            if time.ticks_diff(now, last_send_time) >= 100:
                msg = f"RPM_L:{rpm_left:.1f},RPM_R:{rpm_right:.1f},SPEED:{_speed_percent},PULSES_L:{_cnt_left},PULSES_R:{_cnt_right}\n"
                try:
                    client.sendall(msg.encode())
                    last_send_time = now
                except Exception:
                    break
            
            # Actualizar OLED cada 300ms
            if time.ticks_diff(now, last_oled_update) >= 300:
                oled_write("Optical Speed", f"L:{rpm_left:5.1f} rpm", f"R:{rpm_right:5.1f} rpm", f"Speed: {_speed_percent:+4d}%", "")
                last_oled_update = now
            
            time.sleep(0.01)  # 100 Hz loop principal
            
    except Exception as e:
        print(f"[Optical Speed] Error: {e}")
    finally:
        stop_motors()
        print(f"[Optical Speed] Módulo detenido | Total pulsos L:{_cnt_left} R:{_cnt_right}")
        oled_status("Detenido")

# ============================================================================
# MÓDULO: IR STEERING (Seguidor de línea con PID)
# ============================================================================

def read_ir_sensors():
    """Lee los 5 sensores IR y devuelve string binario"""
    bits = ''
    for sensor in ir_sensors:
        # Pull-up: línea negra baja el pin (0), normalizar a 1=detecta línea
        detected = 1 if (not sensor.value()) else 0
        bits += str(detected)
    return bits

def calculate_line_error(bits):
    """Calcula el error de posición respecto a la línea"""
    weights = [-2, -1, 0, 1, 2]
    weighted_sum = 0.0
    count = 0.0
    
    for i, bit in enumerate(bits[:5]):
        if bit == '1':
            weighted_sum += weights[i]
            count += 1.0
    
    if count == 0:
        return 0.0  # Línea perdida
    
    return weighted_sum / count

def pid_motor_control(base_speed, error, delta_time):
    """Calcula las velocidades de los motores usando PID"""
    global _err_integral, _last_error
    
    # PID
    _err_integral += error * delta_time
    derivative = (error - _last_error) / delta_time if delta_time > 0 else 0.0
    _last_error = error
    
    correction = _kp * error + _ki * _err_integral + _kd * derivative
    
    # Mezcla diferencial (invertida para corregir sentido de giro)
    # Error positivo (línea a la derecha) -> aumentar izquierdo, reducir derecho
    left_speed = base_speed + correction * 30
    right_speed = base_speed - correction * 30
    
    # Clamp
    left_speed = max(-100, min(100, int(left_speed)))
    right_speed = max(-100, min(100, int(right_speed)))
    
    return left_speed, right_speed

def apply_dual_motor(left_speed, right_speed):
    """Aplica velocidades independientes a cada motor"""
    # Motor izquierdo
    if left_speed >= 0:
        pwm_set(in1_pwm, abs(left_speed))
        pwm_set(in2_pwm, 0)
    else:
        pwm_set(in1_pwm, 0)
        pwm_set(in2_pwm, abs(left_speed))
    
    # Motor derecho
    if right_speed >= 0:
        pwm_set(in3_pwm, abs(right_speed))
        pwm_set(in4_pwm, 0)
    else:
        pwm_set(in3_pwm, 0)
        pwm_set(in4_pwm, abs(right_speed))

def ir_steering_loop(client):
    """Loop del módulo de seguidor de línea con PID"""
    global current_mode, continuous_client, _base_speed, _cnt_left, _cnt_right, _ppr
    global _err_integral, _last_error
    
    print("[IR Steering] Módulo activo")
    oled_status("IR Steering")
    
    # Reset PID
    _err_integral = 0.0
    _last_error = 0.0
    
    last_time = time.ticks_ms()
    last_cnt_left = _cnt_left
    last_cnt_right = _cnt_right
    last_oled_update = last_time
    rpm_left = 0.0
    rpm_right = 0.0
    
    try:
        while current_mode == 'IR_STEERING' and continuous_client == client:
            # Procesar comandos no bloqueantes
            client.settimeout(0.005)
            try:
                cmd = client.recv(64)
                if cmd:
                    txt = cmd.decode().strip().upper()
                    
                    if txt.startswith('SET_BASE_SPEED:'):
                        try:
                            val = int(txt.split(':', 1)[1])
                            _base_speed = max(-100, min(100, val))
                        except Exception:
                            pass
                            
                    elif txt.startswith('SET_KP:'):
                        try:
                            _kp = float(txt.split(':', 1)[1])
                        except Exception:
                            pass
                            
                    elif txt.startswith('SET_KI:'):
                        try:
                            _ki = float(txt.split(':', 1)[1])
                        except Exception:
                            pass
                            
                    elif txt.startswith('SET_KD:'):
                        try:
                            _kd = float(txt.split(':', 1)[1])
                        except Exception:
                            pass
                            
                    elif 'STOP' in txt:
                        break
                        
            except Exception:
                pass
            
            # Calcular delta time
            now = time.ticks_ms()
            delta_time = time.ticks_diff(now, last_time) / 1000.0
            if delta_time <= 0:
                delta_time = 0.01
            last_time = now
            
            # Leer sensores IR
            bits = read_ir_sensors()
            error = calculate_line_error(bits)
            
            # Calcular velocidades con PID
            left_speed, right_speed = pid_motor_control(_base_speed, error, delta_time)
            apply_dual_motor(left_speed, right_speed)
            
            # Calcular RPM cada 200ms
            if time.ticks_diff(now, last_oled_update) >= 200:
                delta_left = _cnt_left - last_cnt_left
                delta_right = _cnt_right - last_cnt_right
                dt = time.ticks_diff(now, last_oled_update) / 1000.0
                
                last_cnt_left = _cnt_left
                last_cnt_right = _cnt_right
                
                if dt > 0 and _ppr > 0:
                    rpm_left = (delta_left / dt) * (60.0 / _ppr)
                    rpm_right = (delta_right / dt) * (60.0 / _ppr)
                
                # Actualizar OLED
                oled_write("IR Steering", f"Sens:{bits}", f"Err:{error:+.2f}", f"L:{left_speed:+3d} R:{right_speed:+3d}", "")
                last_oled_update = now
            
            # Enviar datos
            msg = f"SENSORS:{bits},ERROR:{error:.2f},LEFT:{left_speed},RIGHT:{right_speed},RPM_L:{rpm_left:.1f},RPM_R:{rpm_right:.1f}\n"
            try:
                client.sendall(msg.encode())
            except Exception:
                break
            
            time.sleep(0.02)  # 50 Hz
            
    except Exception as e:
        print(f"[IR Steering] Error: {e}")
    finally:
        apply_dual_motor(0, 0)
        print("[IR Steering] Módulo detenido")
        oled_status("Detenido")

# ============================================================================
# BUCLE PRINCIPAL DEL SERVIDOR
# ============================================================================

print("\n" + "=" * 50)
print("SERVIDOR LISTO - Esperando conexiones...")
print("=" * 50 + "\n")

# Ejecutar animación de entrada (non-blocking con timeout de 20s)
server.settimeout(0.1)  # Non-blocking para permitir animación
animation_start = time.ticks_ms()
animation_running = True

while animation_running and time.ticks_diff(time.ticks_ms(), animation_start) < 20000:
    try:
        client, addr = server.accept()
        # Conexión recibida, interrumpir animación
        print("\n[Animación] Interrumpida por conexión entrante")
        animation_running = False
        server.settimeout(30)  # Restaurar timeout normal
        
        # Procesar la conexión inmediatamente
        oled_write("Cliente", "conectado", str(addr[0]), "", "")
        time.sleep(1)
        
        client.settimeout(30)
        data = client.recv(1024).decode().strip()
        print(f'[Servidor] Comando: {data}')
        
        # Procesar comando
        if 'LED_ON' in data:
            led.on()
            try:
                client.sendall(b"LED_ON_OK\n")
                time.sleep(0.1)
            except Exception as e:
                print(f"[LED_ON] Error enviando: {e}")
        
        elif 'LED_OFF' in data:
            led.off()
            try:
                client.sendall(b"LED_OFF_OK\n")
                time.sleep(0.1)
            except Exception as e:
                print(f"[LED_OFF] Error enviando: {e}")
        
        elif 'MODO:OPTICAL_SPEED' in data:
            current_mode = 'OPTICAL_SPEED'
            continuous_client = client
            client.sendall(b"OPTICAL_SPEED_OK\n")
            optical_speed_loop(client)
        
        elif 'MODO:IR_STEERING' in data:
            current_mode = 'IR_STEERING'
            continuous_client = client
            client.sendall(b"IR_STEERING_OK\n")
            ir_steering_loop(client)
        
        elif 'STOP' in data:
            stop_motors()
            client.sendall(b"STOPPED\n")
        
        else:
            client.sendall(b"UNKNOWN_CMD\n")
        
        try:
            client.close()
        except Exception:
            pass
        
        current_mode = None
        continuous_client = None
        oled_status("Esperando...")
        
        break  # Salir del bucle de animación
        
    except OSError:
        # No hay conexión aún, continuar con animación
        pass
    
    # Ejecutar un frame de la animación
    animation_speed_direction()
    animation_running = False  # La función ya maneja sus 20s internamente

# Si la animación terminó sin interrupción, mostrar estado de espera
if animation_running or time.ticks_diff(time.ticks_ms(), animation_start) >= 20000:
    oled_status("Esperando...")

# Restaurar timeout normal del servidor
server.settimeout(30)

while True:
    try:
        client, addr = server.accept()
        print(f'\n[Servidor] ✓ Cliente conectado: {addr}')
        oled_write("Cliente", "conectado", str(addr[0]), "", "")
        time.sleep(1)
        
        client.settimeout(30)
        
        # Recibir comando
        data = client.recv(1024).decode().strip()
        print(f'[Servidor] Comando: {data}')
        
        # Procesar comandos simples (responder y cerrar)
        if 'LED_ON' in data:
            led.on()
            try:
                client.sendall(b"LED_ON_OK\n")
                time.sleep(0.1)
            except Exception as e:
                print(f"[LED_ON] Error enviando: {e}")
            
        elif 'LED_OFF' in data:
            led.off()
            try:
                client.sendall(b"LED_OFF_OK\n")
                time.sleep(0.1)
            except Exception as e:
                print(f"[LED_OFF] Error enviando: {e}")
        
        # Modos continuos (mantener conexión)
        elif 'MODO:OPTICAL_SPEED' in data:
            current_mode = 'OPTICAL_SPEED'
            continuous_client = client
            client.sendall(b"OPTICAL_SPEED_OK\n")
            optical_speed_loop(client)
            
        elif 'MODO:IR_STEERING' in data:
            current_mode = 'IR_STEERING'
            continuous_client = client
            client.sendall(b"IR_STEERING_OK\n")
            ir_steering_loop(client)
            
        elif 'STOP' in data:
            stop_motors()
            client.sendall(b"STOPPED\n")
            
        else:
            client.sendall(b"UNKNOWN_CMD\n")
        
        # Limpiar estado
        try:
            client.close()
        except Exception:
            pass
        
        current_mode = None
        continuous_client = None
        oled_status("Esperando...")
        
    except OSError as e:
        print(f"[Servidor] ✗ Error de red: {e}")
        try:
            client.close()
        except Exception:
            pass
        
        # Verificar conexión WiFi
        if not sta.isconnected():
            print("[WiFi] Reconectando...")
            oled_write("WiFi", "Reconectando", "", "", "")
            sta = connect_wifi()
            if not sta:
                reset()
                
    except Exception as e:
        print(f"[Servidor] ✗ Error inesperado: {e}")
        try:
            client.close()
        except Exception:
            pass
