# main_parte1_distancia_angulo.py - SensoraCore Alpha 0.4
# Módulos: Simple Angle, Angle Arm, Infrared, Capacitive, Ultrasonic
# Pantalla OLED 128x64 I2C integrada
# Autor: SensoraCore Team
# Fecha: 2025-11-21

import network  # type: ignore
import socket
import time
from machine import Pin, ADC, reset, I2C  # type: ignore
import ssd1306  # type: ignore
from red import SSID, PASSWORD  # type: ignore

# ============================================================================
# CONFIGURACIÓN INICIAL
# ============================================================================

print("=" * 50)
print("SensoraCore ESP32 - Parte 1: Distancia y Ángulo")
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
        oled.text("SensoraCore P1", 0, 0)
        oled.text("Dist & Angulo", 0, 13)
        oled.text("-" * 16, 0, 26)
        oled.text(f"Modo:", 0, 39)
        oled.text(mode[:16], 0, 52)
        oled.show()
    except Exception:
        pass

# Mostrar pantalla de inicio
oled_write("SensoraCore P1", "Dist & Angulo", "", "Iniciando...", "WiFi connecting")

# ============================================================================
# CONFIGURACIÓN DE HARDWARE - PINES GPIO
# ============================================================================

# LED integrado
led = Pin(2, Pin.OUT)

# --- MÓDULO: ÁNGULO SIMPLE ---
pot_simple = ADC(Pin(34))  # Potenciómetro simple
pot_simple.atten(ADC.ATTN_11DB)
pot_simple.width(ADC.WIDTH_12BIT)

# --- MÓDULO: BRAZO ÁNGULO (3 potenciómetros + sensor capacitivo) ---
pot1 = ADC(Pin(35))  # Base
pot2 = ADC(Pin(32))  # Articulación 1
pot3 = ADC(Pin(33))  # Articulación 2
sensor_cap_arm = Pin(25, Pin.IN, Pin.PULL_DOWN)  # Sensor capacitivo agarre

for pot_adc in [pot1, pot2, pot3]:
    pot_adc.atten(ADC.ATTN_11DB)
    pot_adc.width(ADC.WIDTH_12BIT)

# --- MÓDULO: SENSORES DE DISTANCIA DIGITALES ---
sensor_ir = Pin(26, Pin.IN, Pin.PULL_DOWN)  # Sensor infrarrojo digital
sensor_cap_dist = Pin(27, Pin.IN, Pin.PULL_DOWN)  # Sensor capacitivo de distancia

# --- MÓDULO: SENSOR ULTRASÓNICO HC-SR04 ---
trigger_pin = Pin(13, Pin.OUT)  # Trigger
echo_pin = Pin(12, Pin.IN)      # Echo

# ============================================================================
# VARIABLES GLOBALES
# ============================================================================

current_mode = None
continuous_client = None

# ============================================================================
# FUNCIONES DE UTILIDAD
# ============================================================================

def read_adc_filtered(adc_obj, samples=5):
    """Lee el ADC con promedio de múltiples muestras para reducir ruido"""
    total = 0
    for _ in range(samples):
        total += adc_obj.read()
        time.sleep_ms(1)
    return total // samples

def map_value(value, in_min, in_max, out_min, out_max):
    """Mapea un valor de un rango a otro"""
    return int((value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

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
            oled_write("SensoraCore P1", "WiFi...", f"Intento {attempt}/5", "", "")
            
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
# ANIMACIÓN DE ENTRADA - DISTANCIA Y ÁNGULO
# ============================================================================

def animation_distance_angle():
    """
    Animación de entrada: Regla → Escuadra → Transportador 180° → Transportador 360°
    Duración: 20 segundos
    Non-blocking: permite interrupción por conexión entrante
    """
    if not oled_enabled or not oled:
        return
    
    print("[Animación] Iniciando secuencia de entrada...")
    start_time = time.ticks_ms()
    duration_ms = 20000  # 20 segundos
    
    try:
        # FASE 1: Regla recta horizontal (0-5s)
        phase_duration = 5000
        phase_start = time.ticks_ms()
        while time.ticks_diff(time.ticks_ms(), phase_start) < phase_duration:
            if time.ticks_diff(time.ticks_ms(), start_time) >= duration_ms:
                return
            
            oled.fill(0)
            
            # Regla horizontal creciente
            progress = time.ticks_diff(time.ticks_ms(), phase_start) / phase_duration
            line_length = int(100 * progress)
            oled.hline(14, 32, line_length, 1)
            
            # Marcas de medición en la regla
            for i in range(0, line_length, 10):
                oled.vline(14 + i, 30, 5, 1)
            
            oled.show()
            time.sleep(0.05)
        
        # FASE 2: Transformación a escuadra (5-10s)
        phase_duration = 5000
        phase_start = time.ticks_ms()
        while time.ticks_diff(time.ticks_ms(), phase_start) < phase_duration:
            if time.ticks_diff(time.ticks_ms(), start_time) >= duration_ms:
                return
            
            oled.fill(0)
            
            # Línea horizontal
            oled.hline(30, 50, 60, 1)
            # Línea vertical creciente
            progress = time.ticks_diff(time.ticks_ms(), phase_start) / phase_duration
            v_length = int(40 * progress)
            oled.vline(30, 50 - v_length, v_length, 1)
            
            # Marcas en ambos lados
            for i in range(0, 60, 10):
                oled.vline(30 + i, 48, 4, 1)
            for i in range(0, v_length, 10):
                oled.hline(28, 50 - i, 4, 1)
            
            oled.show()
            time.sleep(0.05)
        
        # FASE 3: Transformación a transportador 180° (10-15s)
        phase_duration = 5000
        phase_start = time.ticks_ms()
        while time.ticks_diff(time.ticks_ms(), phase_start) < phase_duration:
            if time.ticks_diff(time.ticks_ms(), start_time) >= duration_ms:
                return
            
            oled.fill(0)
            
            # Semicírculo superior
            progress = time.ticks_diff(time.ticks_ms(), phase_start) / phase_duration
            cx, cy, r = 64, 45, 28
            
            # Dibujar arco de semicírculo
            import math
            for angle in range(0, int(180 * progress)):
                rad = math.radians(angle + 180)  # Empezar desde la izquierda
                x = int(cx + r * math.cos(rad))
                y = int(cy + r * math.sin(rad))
                if 0 <= x < 128 and 0 <= y < 64:
                    oled.pixel(x, y, 1)
            
            # Línea base
            oled.hline(cx - r, cy, r * 2, 1)
            
            # Marcas de grados
            for angle in range(0, int(180 * progress), 30):
                rad = math.radians(angle + 180)
                x1 = int(cx + r * math.cos(rad))
                y1 = int(cy + r * math.sin(rad))
                x2 = int(cx + (r - 5) * math.cos(rad))
                y2 = int(cy + (r - 5) * math.sin(rad))
                oled.line(x1, y1, x2, y2, 1)
            
            oled.show()
            time.sleep(0.05)
        
        # FASE 4: Completar a transportador 360° (15-20s)
        phase_duration = 5000
        phase_start = time.ticks_ms()
        while time.ticks_diff(time.ticks_ms(), phase_start) < phase_duration:
            if time.ticks_diff(time.ticks_ms(), start_time) >= duration_ms:
                return
            
            oled.fill(0)
            
            # Círculo completo
            progress = time.ticks_diff(time.ticks_ms(), phase_start) / phase_duration
            cx, cy, r = 64, 32, 28
            
            # Dibujar círculo completo (primeros 180° + nuevos 180°)
            import math
            # Parte superior (siempre visible)
            for angle in range(0, 180):
                rad = math.radians(angle + 180)
                x = int(cx + r * math.cos(rad))
                y = int(cy + r * math.sin(rad))
                if 0 <= x < 128 and 0 <= y < 64:
                    oled.pixel(x, y, 1)
            
            # Parte inferior (creciendo)
            for angle in range(0, int(180 * progress)):
                rad = math.radians(angle)
                x = int(cx + r * math.cos(rad))
                y = int(cy + r * math.sin(rad))
                if 0 <= x < 128 and 0 <= y < 64:
                    oled.pixel(x, y, 1)
            
            # Marcas de grados cada 45°
            for angle in range(0, 360, 45):
                rad = math.radians(angle)
                x1 = int(cx + r * math.cos(rad))
                y1 = int(cy + r * math.sin(rad))
                x2 = int(cx + (r - 4) * math.cos(rad))
                y2 = int(cy + (r - 4) * math.sin(rad))
                oled.line(x1, y1, x2, y2, 1)
            
            # Centro
            oled.fill_rect(cx - 1, cy - 1, 3, 3, 1)
            
            oled.show()
            time.sleep(0.05)
        
        print("[Animación] Secuencia completada")
        
    except Exception as e:
        print(f"[Animación] Error: {e}")

# ============================================================================
# MÓDULO: ÁNGULO SIMPLE
# ============================================================================

def angulo_simple_loop(client):
    """Loop del módulo de ángulo simple con potenciómetro"""
    global current_mode, continuous_client
    
    print("[Ángulo Simple] Módulo activo")
    oled_status("Simple Angle")
    
    try:
        while current_mode == 'ANGULO_SIMPLE' and continuous_client == client:
            # Leer ADC con filtrado
            lectura = read_adc_filtered(pot_simple, samples=3)
            
            # Mapear de 0-4095 a -135 a +135 grados
            angulo = map_value(lectura, 0, 4095, -135, 135)
            
            # Actualizar OLED
            oled_write("Simple Angle", "-" * 16, f"ADC: {lectura}", f"Ang: {angulo:+4d}deg", "")
            
            # Enviar datos
            msg = f"POT:{lectura},ANG:{angulo}\n"
            try:
                client.sendall(msg.encode())
            except Exception:
                break
            
            time.sleep(0.1)  # 10 Hz
            
    except Exception as e:
        print(f"[Ángulo Simple] Error: {e}")
    finally:
        print("[Ángulo Simple] Módulo detenido")
        oled_status("Detenido")

# ============================================================================
# MÓDULO: BRAZO ÁNGULO
# ============================================================================

def brazo_angulo_loop(client):
    """Loop del módulo de brazo con 3 potenciómetros + sensor capacitivo"""
    global current_mode, continuous_client
    
    print("[Brazo Ángulo] Módulo activo")
    oled_status("Angle Arm")
    
    try:
        while current_mode == 'BRAZO_ANGULO' and continuous_client == client:
            # Leer los 3 potenciómetros con filtrado
            lectura1 = read_adc_filtered(pot1, samples=3)
            lectura2 = read_adc_filtered(pot2, samples=3)
            lectura3 = read_adc_filtered(pot3, samples=3)
            
            # Mapear a grados
            angulo1 = map_value(lectura1, 0, 4095, -135, 135)
            angulo2 = map_value(lectura2, 0, 4095, -135, 135)
            angulo3 = map_value(lectura3, 0, 4095, -135, 135)
            
            # Leer sensor capacitivo
            sensor_estado = sensor_cap_arm.value()
            
            # Actualizar OLED
            oled_write("Angle Arm", f"1:{angulo1:+4d} 2:{angulo2:+4d}", f"3:{angulo3:+4d}deg", f"Cap: {'ON' if sensor_estado else 'OFF'}", "")
            
            # Enviar datos
            msg = f"POT1:{lectura1},ANG1:{angulo1},POT2:{lectura2},ANG2:{angulo2},POT3:{lectura3},ANG3:{angulo3},SENSOR:{sensor_estado}\n"
            try:
                client.sendall(msg.encode())
            except Exception:
                break
            
            time.sleep(0.05)  # 20 Hz
            
    except Exception as e:
        print(f"[Brazo Ángulo] Error: {e}")
    finally:
        print("[Brazo Ángulo] Módulo detenido")
        oled_status("Detenido")

# ============================================================================
# MÓDULO: DISTANCIA IR (Digital)
# ============================================================================

def distancia_ir_loop(client):
    """Loop del módulo de distancia infrarroja digital"""
    global current_mode, continuous_client
    
    print("[Distancia IR] Módulo activo")
    oled_status("IR Distance")
    
    try:
        while current_mode == 'DISTANCIA_IR' and continuous_client == client:
            # Leer sensor digital
            sensor_detectado = sensor_ir.value()
            
            # Actualizar OLED
            status_text = "DETECTADO!" if sensor_detectado else "Libre"
            oled_write("IR Distance", "-" * 16, "", status_text, "")
            
            # Enviar datos
            msg = f"IR_DIGITAL:{sensor_detectado}\n"
            try:
                client.sendall(msg.encode())
            except Exception:
                break
            
            time.sleep(0.1)  # 10 Hz
            
    except Exception as e:
        print(f"[Distancia IR] Error: {e}")
    finally:
        print("[Distancia IR] Módulo detenido")
        oled_status("Detenido")

# ============================================================================
# MÓDULO: DISTANCIA CAPACITIVA (Digital)
# ============================================================================

def distancia_cap_loop(client):
    """Loop del módulo de distancia capacitiva digital"""
    global current_mode, continuous_client
    
    print("[Distancia Capacitiva] Módulo activo")
    oled_status("Cap Distance")
    
    try:
        while current_mode == 'DISTANCIA_CAP' and continuous_client == client:
            # Leer sensor digital
            sensor_detectado = sensor_cap_dist.value()
            
            # Actualizar OLED
            status_text = "DETECTADO!" if sensor_detectado else "Libre"
            oled_write("Cap Distance", "-" * 16, "", status_text, "")
            
            # Enviar datos
            msg = f"CAP_DIGITAL:{sensor_detectado}\n"
            try:
                client.sendall(msg.encode())
            except Exception:
                break
            
            time.sleep(0.1)  # 10 Hz
            
    except Exception as e:
        print(f"[Distancia Capacitiva] Error: {e}")
    finally:
        print("[Distancia Capacitiva] Módulo detenido")
        oled_status("Detenido")

# ============================================================================
# MÓDULO: DISTANCIA ULTRASÓNICA HC-SR04
# ============================================================================

def distancia_ultrasonico_loop(client):
    """Loop del módulo de distancia ultrasónica HC-SR04"""
    global current_mode, continuous_client
    
    print("[Ultrasónico] Módulo activo")
    oled_status("Ultrasonic")
    
    try:
        while current_mode == 'DISTANCIA_ULTRA' and continuous_client == client:
            # Generar pulso trigger
            trigger_pin.off()
            time.sleep_us(2)
            trigger_pin.on()
            time.sleep_us(10)
            trigger_pin.off()
            
            # Medir tiempo de echo con timeout
            timeout_us = 30000  # 30ms timeout
            
            # Esperar inicio de echo
            start_time = time.ticks_us()
            timeout_start = start_time
            while echo_pin.value() == 0:
                start_time = time.ticks_us()
                if time.ticks_diff(start_time, timeout_start) > timeout_us:
                    break
            
            # Medir duración del echo
            end_time = start_time
            while echo_pin.value() == 1:
                end_time = time.ticks_us()
                if time.ticks_diff(end_time, start_time) > timeout_us:
                    break
            
            # Calcular distancia
            duration = time.ticks_diff(end_time, start_time)
            
            if 0 < duration < timeout_us:
                # Velocidad del sonido: 343 m/s = 0.0343 cm/us
                # Distancia = (tiempo * velocidad) / 2
                distancia_cm = (duration * 0.0343) / 2
            else:
                distancia_cm = -1  # Error o fuera de rango
            
            # Actualizar OLED
            if distancia_cm >= 0:
                oled_write("Ultrasonic", "-" * 16, f"Dist: {distancia_cm:.1f}cm", "", "")
            else:
                oled_write("Ultrasonic", "-" * 16, "Fuera rango", "", "")
            
            # Enviar datos
            msg = f"ULTRA_CM:{distancia_cm:.1f}\n"
            try:
                client.sendall(msg.encode())
            except Exception:
                break
            
            time.sleep(0.06)  # ~16 Hz
            
    except Exception as e:
        print(f"[Ultrasónico] Error: {e}")
    finally:
        print("[Ultrasónico] Módulo detenido")
        oled_status("Detenido")

# ============================================================================
# BUCLE PRINCIPAL DEL SERVIDOR
# ============================================================================

print("\n" + "=" * 50)
print("SERVIDOR LISTO - Esperando conexiones...")
print("=" * 50 + "\n")

# Ejecutar animación de entrada (non-blocking con timeout de 20s)
# El servidor sigue escuchando en segundo plano
server.settimeout(0.1)  # Non-blocking para permitir animación
animation_start = time.ticks_ms()
animation_running = True

while animation_running and time.ticks_diff(time.ticks_ms(), animation_start) < 20000:
    # Intentar aceptar conexión sin bloquear
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
        
        # Procesar comando (código duplicado necesario para manejar primera conexión)
        if 'GET_POT' in data:
            lectura = pot_simple.read()
            try:
                client.sendall(f"POT:{lectura}\n".encode())
                time.sleep(0.1)
            except Exception as e:
                print(f"[GET_POT] Error enviando: {e}")
        
        elif 'LED_ON' in data:
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
        
        elif 'MODO:ANGULO_SIMPLE' in data:
            current_mode = 'ANGULO_SIMPLE'
            continuous_client = client
            client.sendall(b"ANGULO_SIMPLE_OK\n")
            angulo_simple_loop(client)
        
        elif 'MODO:BRAZO_ANGULO' in data:
            current_mode = 'BRAZO_ANGULO'
            continuous_client = client
            client.sendall(b"BRAZO_ANGULO_OK\n")
            brazo_angulo_loop(client)
        
        elif 'MODO:DISTANCIA_IR' in data:
            current_mode = 'DISTANCIA_IR'
            continuous_client = client
            client.sendall(b"DISTANCIA_IR_OK\n")
            distancia_ir_loop(client)
        
        elif 'MODO:DISTANCIA_CAP' in data:
            current_mode = 'DISTANCIA_CAP'
            continuous_client = client
            client.sendall(b"DISTANCIA_CAP_OK\n")
            distancia_cap_loop(client)
        
        elif 'MODO:DISTANCIA_ULTRA' in data:
            current_mode = 'DISTANCIA_ULTRA'
            continuous_client = client
            client.sendall(b"DISTANCIA_ULTRA_OK\n")
            distancia_ultrasonico_loop(client)
        
        elif 'STOP' in data:
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
    animation_distance_angle()
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
        if 'GET_POT' in data:
            lectura = pot_simple.read()
            try:
                client.sendall(f"POT:{lectura}\n".encode())
                time.sleep(0.1)
            except Exception as e:
                print(f"[GET_POT] Error enviando: {e}")
            
        elif 'LED_ON' in data:
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
        elif 'MODO:ANGULO_SIMPLE' in data:
            current_mode = 'ANGULO_SIMPLE'
            continuous_client = client
            client.sendall(b"ANGULO_SIMPLE_OK\n")
            angulo_simple_loop(client)
            
        elif 'MODO:BRAZO_ANGULO' in data:
            current_mode = 'BRAZO_ANGULO'
            continuous_client = client
            client.sendall(b"BRAZO_ANGULO_OK\n")
            brazo_angulo_loop(client)
            
        elif 'MODO:DISTANCIA_IR' in data:
            current_mode = 'DISTANCIA_IR'
            continuous_client = client
            client.sendall(b"DISTANCIA_IR_OK\n")
            distancia_ir_loop(client)
            
        elif 'MODO:DISTANCIA_CAP' in data:
            current_mode = 'DISTANCIA_CAP'
            continuous_client = client
            client.sendall(b"DISTANCIA_CAP_OK\n")
            distancia_cap_loop(client)
            
        elif 'MODO:DISTANCIA_ULTRA' in data:
            current_mode = 'DISTANCIA_ULTRA'
            continuous_client = client
            client.sendall(b"DISTANCIA_ULTRA_OK\n")
            distancia_ultrasonico_loop(client)
            
        elif 'STOP' in data:
            client.sendall(b"STOPPED\n")
            
        else:
            client.send(b"UNKNOWN_CMD\n")
        
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
