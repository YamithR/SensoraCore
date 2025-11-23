# main_parte4_color_luz.py - SensoraCore Alpha 0.4
# Módulos: Color TCS3200, Color CNY70, Brightness (LDR)
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
print("SensoraCore ESP32 - Parte 4: Color y Luz")
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
        oled.text("SensoraCore P4", 0, 0)
        oled.text("Color & Luz", 0, 13)
        oled.text("-" * 16, 0, 26)
        ip = sta.ifconfig()[0]
        oled.text(f"IP: {ip}", 0, 39)
        oled.text(mode[:16], 0, 52)
        oled.show()
    except Exception:
        pass

def oled_draw_bar(x, y, width, height, percentage):
    """Dibuja una barra de progreso en la OLED"""
    if not oled_enabled or not oled:
        return
    try:
        # Marco de la barra
        oled.rect(x, y, width, height, 1)
        # Relleno de la barra según porcentaje
        fill_width = int((width - 2) * percentage / 100)
        if fill_width > 0:
            oled.fill_rect(x + 1, y + 1, fill_width, height - 2, 1)
    except Exception:
        pass

# Mostrar pantalla de inicio
oled_write("SensoraCore P4", "Color & Luz", "", "Iniciando...", "WiFi connecting")

# ============================================================================
# CONFIGURACIÓN DE HARDWARE - PINES GPIO
# ============================================================================

# LED integrado
led = Pin(2, Pin.OUT)

# --- MÓDULO: BRIGHTNESS (Fotoresistencia LDR) ---
# LDR en GPIO34

# --- MÓDULO: COLOR CNY (Sensor CNY70 reflectivo) ---
# CNY70 en GPIO35

# --- MÓDULO: COLOR TCS (Sensor TCS3200) ---
# S2: GPIO32
# S3: GPIO33
# OUT: GPIO36

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
            oled_write("SensoraCore P4", "WiFi...", f"Intento {attempt}/5", "", "")
            
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
# ANIMACIÓN DE ENTRADA - LUZ Y COLOR
# ============================================================================

def animation_light_color():
    """
    Animación de entrada: Bombilla parpadeando → Zoom a Sol → Luna diagonal → Parpadeo alternado
    Duración: 20 segundos
    Non-blocking: permite interrupción por conexión entrante
    """
    if not oled_enabled or not oled:
        return
    
    print("[Animación] Iniciando secuencia de entrada...")
    start_time = time.ticks_ms()
    duration_ms = 20000  # 20 segundos
    
    try:
        import math
        
        # FASE 1: Bombilla con relleno pulsante y rayos (0-5s)
        phase_duration = 5000
        phase_start = time.ticks_ms()
        while time.ticks_diff(time.ticks_ms(), phase_start) < phase_duration:
            if time.ticks_diff(time.ticks_ms(), start_time) >= duration_ms:
                return
            
            progress = time.ticks_diff(time.ticks_ms(), phase_start) / phase_duration
            
            # Pulso sinusoidal (más suave que on/off)
            pulse = abs(math.sin(progress * math.pi * 8))  # 4 ciclos completos en 5s
            
            oled.fill(0)
            
            bulb_x = 64
            bulb_y = 35
            bulb_r = 10
            
            # Bulbo de vidrio (contorno siempre visible)
            for angle in range(0, 360, 6):
                rad = math.radians(angle)
                x = int(bulb_x + bulb_r * math.cos(rad))
                y = int(bulb_y + bulb_r * math.sin(rad))
                if 0 <= x < 128 and 0 <= y < 64:
                    oled.pixel(x, y, 1)
            
            # Casquillo/base (siempre visible)
            oled.fill_rect(bulb_x - 4, bulb_y + 10, 8, 3, 1)
            oled.fill_rect(bulb_x - 3, bulb_y + 13, 6, 2, 1)
            
            # Relleno interno que pulsa (según intensidad del pulso)
            fill_radius = int(bulb_r * pulse * 0.8)
            if fill_radius > 2:
                # Rellenar círculo interior
                for y in range(-fill_radius, fill_radius + 1):
                    for x in range(-fill_radius, fill_radius + 1):
                        if x*x + y*y <= fill_radius*fill_radius:
                            px = bulb_x + x
                            py = bulb_y + y
                            if 0 <= px < 128 and 0 <= py < 64:
                                oled.pixel(px, py, 1)
            
            # Filamento central siempre visible
            oled.line(bulb_x - 3, bulb_y - 4, bulb_x + 3, bulb_y - 4, 1)
            oled.line(bulb_x, bulb_y - 6, bulb_x, bulb_y - 2, 1)
            
            # Rayos que aparecen según el pulso (más intensidad = más rayos largos)
            if pulse > 0.3:
                num_rays = 8
                ray_length = int(6 + 10 * pulse)
                for i in range(num_rays):
                    angle = i * (360 / num_rays)
                    rad = math.radians(angle)
                    x1 = int(bulb_x + (bulb_r + 2) * math.cos(rad))
                    y1 = int(bulb_y + (bulb_r + 2) * math.sin(rad))
                    x2 = int(bulb_x + (bulb_r + 2 + ray_length) * math.cos(rad))
                    y2 = int(bulb_y + (bulb_r + 2 + ray_length) * math.sin(rad))
                    oled.line(x1, y1, x2, y2, 1)
            
            oled.show()
            time.sleep(0.05)
        
        # FASE 2: Bombilla explota en zoom transformándose en sol (5-10s)
        phase_duration = 5000
        phase_start = time.ticks_ms()
        while time.ticks_diff(time.ticks_ms(), phase_start) < phase_duration:
            if time.ticks_diff(time.ticks_ms(), start_time) >= duration_ms:
                return
            
            oled.fill(0)
            
            progress = time.ticks_diff(time.ticks_ms(), phase_start) / phase_duration
            
            # Centro del sol
            sun_x = 64
            sun_y = 32
            
            # Aceleración en el crecimiento (explosión)
            growth_curve = progress * progress  # Aceleración cuadrática
            sun_r = int(10 + 20 * growth_curve)
            
            # Círculo del sol (triple línea para máxima visibilidad)
            for angle in range(0, 360, 3):
                rad = math.radians(angle)
                # Línea exterior
                x = int(sun_x + sun_r * math.cos(rad))
                y = int(sun_y + sun_r * math.sin(rad))
                if 0 <= x < 128 and 0 <= y < 64:
                    oled.pixel(x, y, 1)
                # Línea media
                x2 = int(sun_x + (sun_r - 1) * math.cos(rad))
                y2 = int(sun_y + (sun_r - 1) * math.sin(rad))
                if 0 <= x2 < 128 and 0 <= y2 < 64:
                    oled.pixel(x2, y2, 1)
                # Línea interior
                if progress > 0.4:
                    x3 = int(sun_x + (sun_r - 2) * math.cos(rad))
                    y3 = int(sun_y + (sun_r - 2) * math.sin(rad))
                    if 0 <= x3 < 128 and 0 <= y3 < 64:
                        oled.pixel(x3, y3, 1)
            
            # Rayos del sol (aumentan en cantidad y rotan)
            num_rays = 8 + int(8 * progress)  # De 8 a 16 rayos
            rotation = progress * 120  # Rotación más rápida
            ray_length = int(8 + 12 * progress)
            
            for i in range(num_rays):
                angle = i * (360 / num_rays) + rotation
                rad = math.radians(angle)
                
                # Rayo principal con grosor
                x1 = int(sun_x + (sun_r + 2) * math.cos(rad))
                y1 = int(sun_y + (sun_r + 2) * math.sin(rad))
                x2 = int(sun_x + (sun_r + 2 + ray_length) * math.cos(rad))
                y2 = int(sun_y + (sun_r + 2 + ray_length) * math.sin(rad))
                
                if 0 <= x1 < 128 and 0 <= y1 < 64 and 0 <= x2 < 128 and 0 <= y2 < 64:
                    oled.line(x1, y1, x2, y2, 1)
                    
                    # Líneas paralelas para grosor (si es rayo principal)
                    if i % 2 == 0 and progress > 0.3:
                        offset = 1
                        perp_angle = angle + 90
                        perp_rad = math.radians(perp_angle)
                        
                        x1_off = int(x1 + offset * math.cos(perp_rad))
                        y1_off = int(y1 + offset * math.sin(perp_rad))
                        x2_off = int(x2 + offset * math.cos(perp_rad))
                        y2_off = int(y2 + offset * math.sin(perp_rad))
                        
                        if 0 <= x1_off < 128 and 0 <= y1_off < 64:
                            oled.line(x1_off, y1_off, x2_off, y2_off, 1)
            
            # Relleno central que crece (núcleo brillante)
            center_size = int(sun_r * 0.4 * progress)
            if center_size > 1:
                for y in range(-center_size, center_size + 1):
                    for x in range(-center_size, center_size + 1):
                        if x*x + y*y <= center_size*center_size:
                            px = sun_x + x
                            py = sun_y + y
                            if 0 <= px < 128 and 0 <= py < 64:
                                oled.pixel(px, py, 1)
            
            oled.show()
            time.sleep(0.05)
        
        # FASE 3: Aparece la luna en diagonal (10-15s)
        phase_duration = 5000
        phase_start = time.ticks_ms()
        while time.ticks_diff(time.ticks_ms(), phase_start) < phase_duration:
            if time.ticks_diff(time.ticks_ms(), start_time) >= duration_ms:
                return
            
            oled.fill(0)
            
            progress = time.ticks_diff(time.ticks_ms(), phase_start) / phase_duration
            
            # Sol en su posición final (esquina superior izquierda)
            sun_x = 25
            sun_y = 20
            sun_r = 12
            
            # Dibujar sol más pequeño
            for angle in range(0, 360, 8):
                rad = math.radians(angle)
                x = int(sun_x + sun_r * math.cos(rad))
                y = int(sun_y + sun_r * math.sin(rad))
                if 0 <= x < 128 and 0 <= y < 64:
                    oled.pixel(x, y, 1)
            
            # Rayos del sol (simplificados, 8 rayos)
            for i in range(8):
                angle = i * 45
                rad = math.radians(angle)
                x1 = int(sun_x + (sun_r + 2) * math.cos(rad))
                y1 = int(sun_y + (sun_r + 2) * math.sin(rad))
                x2 = int(sun_x + (sun_r + 8) * math.cos(rad))
                y2 = int(sun_y + (sun_r + 8) * math.sin(rad))
                if 0 <= x1 < 128 and 0 <= y1 < 64:
                    oled.line(x1, y1, x2, y2, 1)
            
            oled.fill_rect(sun_x - 2, sun_y - 2, 5, 5, 1)
            
            # Luna apareciendo (esquina inferior derecha) - cuarto creciente
            if progress > 0.2:
                t = (progress - 0.2) / 0.8
                moon_x = 103
                moon_y = 44
                moon_r = int(13 * t)
                
                if moon_r > 3:
                    # Luna en cuarto creciente - forma de C (media luna)
                    # Arco exterior (lado derecho)
                    for angle in range(-85, 86, 4):
                        rad = math.radians(angle)
                        x = int(moon_x + moon_r * math.cos(rad))
                        y = int(moon_y + moon_r * math.sin(rad))
                        if 0 <= x < 128 and 0 <= y < 64:
                            oled.pixel(x, y, 1)
                    
                    # Arco interior cóncavo (lado izquierdo/sombra)
                    inner_offset = int(moon_r * 0.6)
                    for angle in range(-80, 81, 4):
                        rad = math.radians(angle)
                        x = int(moon_x - inner_offset + moon_r * 0.5 * math.cos(rad))
                        y = int(moon_y + moon_r * 0.95 * math.sin(rad))
                        if 0 <= x < 128 and 0 <= y < 64:
                            oled.pixel(x, y, 1)
                    
                    # Cráteres en la parte visible
                    if t > 0.5:
                        crater_positions = [(4, -3), (6, 2), (5, -1)]
                        for cx_off, cy_off in crater_positions:
                            cx = moon_x + cx_off
                            cy = moon_y + cy_off
                            crater_r = 1
                            oled.fill_rect(cx - crater_r, cy - crater_r, crater_r * 2 + 1, crater_r * 2 + 1, 1)
            
            oled.show()
            time.sleep(0.05)
        
        # FASE 4: Aparecen estrellas (15-20s)
        phase_duration = 5000
        phase_start = time.ticks_ms()
        
        # Generar posiciones aleatorias para estrellas (evitar área de sol y luna)
        import random
        stars = []
        for _ in range(25):
            x = random.randint(5, 123)
            y = random.randint(5, 59)
            # Evitar área del sol (15-35, 10-30)
            # Evitar área de la luna (93-113, 34-54)
            if not (15 <= x <= 35 and 10 <= y <= 30) and not (93 <= x <= 113 and 34 <= y <= 54):
                stars.append((x, y, random.randint(0, 3)))  # x, y, fase inicial
        
        while time.ticks_diff(time.ticks_ms(), phase_start) < phase_duration:
            if time.ticks_diff(time.ticks_ms(), start_time) >= duration_ms:
                return
            
            oled.fill(0)
            
            progress = time.ticks_diff(time.ticks_ms(), phase_start) / phase_duration
            elapsed_phase = time.ticks_diff(time.ticks_ms(), phase_start)
            
            # Sol en su posición final
            sun_x = 25
            sun_y = 20
            sun_r = 12
            
            for angle in range(0, 360, 8):
                rad = math.radians(angle)
                x = int(sun_x + sun_r * math.cos(rad))
                y = int(sun_y + sun_r * math.sin(rad))
                if 0 <= x < 128 and 0 <= y < 64:
                    oled.pixel(x, y, 1)
            
            for i in range(8):
                angle = i * 45
                rad = math.radians(angle)
                x1 = int(sun_x + (sun_r + 2) * math.cos(rad))
                y1 = int(sun_y + (sun_r + 2) * math.sin(rad))
                x2 = int(sun_x + (sun_r + 8) * math.cos(rad))
                y2 = int(sun_y + (sun_r + 8) * math.sin(rad))
                if 0 <= x1 < 128 and 0 <= y1 < 64:
                    oled.line(x1, y1, x2, y2, 1)
            
            oled.fill_rect(sun_x - 2, sun_y - 2, 5, 5, 1)
            
            # Luna en su posición final
            moon_x = 103
            moon_y = 44
            moon_r = 13
            
            # Luna en cuarto creciente - forma de C
            for angle in range(-85, 86, 4):
                rad = math.radians(angle)
                x = int(moon_x + moon_r * math.cos(rad))
                y = int(moon_y + moon_r * math.sin(rad))
                if 0 <= x < 128 and 0 <= y < 64:
                    oled.pixel(x, y, 1)
            
            inner_offset = int(moon_r * 0.6)
            for angle in range(-80, 81, 4):
                rad = math.radians(angle)
                x = int(moon_x - inner_offset + moon_r * 0.5 * math.cos(rad))
                y = int(moon_y + moon_r * 0.95 * math.sin(rad))
                if 0 <= x < 128 and 0 <= y < 64:
                    oled.pixel(x, y, 1)
            
            # Cráteres
            crater_positions = [(4, -3), (6, 2), (5, -1)]
            for cx_off, cy_off in crater_positions:
                cx = moon_x + cx_off
                cy = moon_y + cy_off
                crater_r = 1
                oled.fill_rect(cx - crater_r, cy - crater_r, crater_r * 2 + 1, crater_r * 2 + 1, 1)
            
            # Estrellas apareciendo gradualmente con parpadeo
            num_visible = int(len(stars) * progress)
            for i in range(num_visible):
                x, y, phase_offset = stars[i]
                # Parpadeo suave basado en tiempo
                blink = (elapsed_phase / 300 + phase_offset) % 4
                if blink < 3:  # Visible 75% del tiempo
                    oled.pixel(x, y, 1)
            
            oled.show()
            time.sleep(0.05)
        
        print("[Animación] Secuencia completada")
        
    except Exception as e:
        print(f"[Animación] Error: {e}")

# ============================================================================
# MÓDULO: BRIGHTNESS (Fotoresistencia LDR)
# ============================================================================

def brightness_loop(client):
    """Loop del módulo de brillo con fotoresistencia LDR"""
    global current_mode, continuous_client
    
    print("[Brightness] Módulo activo")
    oled_status("Brightness")
    
    # Configurar ADC para LDR en GPIO34 (ADC1 para compatibilidad WiFi)
    ldr_adc = None
    try:
        ldr_adc = ADC(Pin(34))
        ldr_adc.atten(ADC.ATTN_11DB)  # Rango completo 0-3.3V
        ldr_adc.width(ADC.WIDTH_12BIT)  # Resolución de 12 bits (0-4095)
        print("[Brightness] LDR configurado en GPIO34")
    except Exception as e:
        print(f"[Brightness] LDR no disponible: {e}")
    
    # Calibración mejorada para LDR
    # Valores recibidos desde la app de escritorio o valores por defecto
    LDR_MIN = 0      # ADC mínimo (oscuridad) - actualizable
    LDR_MAX = 4095   # ADC máximo (luz máxima) - actualizable
    calibrated = False  # Estado de calibración
    
    period_ms = 200
    last_read = 0
    
    try:
        client.settimeout(0.01)
        
        while current_mode == 'BRIGHTNESS' and continuous_client == client:
            # Procesar comandos
            try:
                cmd = client.recv(64)
                if cmd:
                    txt = cmd.decode().strip().upper()
                    if 'STOP' in txt:
                        break
                    # Comando de calibración: CAL:MIN=150,MAX=2800
                    elif 'CAL:' in txt:
                        try:
                            # Extraer valores de calibración
                            cal_part = txt.split('CAL:')[1]
                            for param in cal_part.split(','):
                                if 'MIN=' in param:
                                    LDR_MIN = int(param.split('=')[1])
                                elif 'MAX=' in param:
                                    LDR_MAX = int(param.split('=')[1])
                            calibrated = True
                            print(f"[Brightness] Calibración recibida: MIN={LDR_MIN}, MAX={LDR_MAX}")
                        except Exception as e:
                            print(f"[Brightness] Error en calibración: {e}")
            except Exception:
                pass
            
            # Leer sensor
            now = time.ticks_ms()
            if time.ticks_diff(now, last_read) >= period_ms:
                last_read = now
                
                if ldr_adc:
                    # Leer con filtrado para reducir ruido
                    raw = read_adc_filtered(ldr_adc, samples=10)
                    
                    # Calcular voltaje real
                    voltage = (raw / 4095.0) * 3.3
                    
                    # Mapear a porcentaje de luz (0-100%) con calibración
                    brightness_percent = map_value(raw, LDR_MIN, LDR_MAX, 0, 100)
                    brightness_percent = max(0, min(100, brightness_percent))  # Limitar 0-100
                else:
                    raw = 0
                    voltage = 0.0
                    brightness_percent = 0
                
                # Actualizar OLED con barra de progreso
                if oled_enabled and oled:
                    try:
                        oled.fill(0)
                        # Mostrar estado de calibración en título
                        if calibrated:
                            oled.text("LDR [CAL]", 0, 0)
                        else:
                            oled.text("Brightness/LDR", 0, 0)
                        oled.text(f"ADC: {raw}", 0, 12)
                        oled.text(f"V: {voltage:.2f}V", 0, 24)
                        oled.text(f"Luz: {brightness_percent}%", 0, 36)
                        # Barra de progreso en la parte inferior
                        oled_draw_bar(0, 52, 120, 10, brightness_percent)
                        oled.show()
                    except Exception:
                        pass
                
                # Enviar datos con estado de calibración
                msg = f"LDR_RAW:{raw},VOLTAGE:{voltage:.3f},BRIGHTNESS:{brightness_percent},CALIBRATED:{1 if calibrated else 0}\n"
                try:
                    client.sendall(msg.encode())
                except Exception:
                    break
            
            time.sleep(0.05)
            
    except Exception as e:
        print(f"[Brightness] Error: {e}")
    finally:
        print("[Brightness] Módulo detenido")
        oled_status("Detenido")

# ============================================================================
# MÓDULO: COLOR CNY (Sensor CNY70 reflectivo)
# ============================================================================

def color_cny_loop(client):
    """Loop del módulo de color con sensor CNY70"""
    global current_mode, continuous_client
    
    print("[Color CNY] Módulo activo")
    oled_status("Color CNY")
    
    # Configurar ADC para CNY70 en GPIO35 (ADC1)
    cny_adc = None
    try:
        cny_adc = ADC(Pin(35))
        cny_adc.atten(ADC.ATTN_11DB)  # Rango completo 0-3.3V
        cny_adc.width(ADC.WIDTH_12BIT)  # 12 bits de resolución
        print("[Color CNY] CNY70 configurado en GPIO35")
    except Exception as e:
        print(f"[Color CNY] CNY70 no disponible: {e}")
    
    # Calibración para CNY70
    # Superficie negra/oscura: valores bajos (~100-800)
    # Superficie blanca/clara: valores altos (~2000-4000)
    CNY_MIN = 100    # Superficie más oscura detectada
    CNY_MAX = 3500   # Superficie más clara detectada
    
    period_ms = 150  # Lectura más rápida para sensores ópticos
    last_read = 0
    
    try:
        client.settimeout(0.01)
        
        while current_mode == 'COLOR_CNY' and continuous_client == client:
            # Procesar comandos
            try:
                cmd = client.recv(64)
                if cmd:
                    txt = cmd.decode().strip().upper()
                    if 'STOP' in txt:
                        break
            except Exception:
                pass
            
            # Leer sensor
            now = time.ticks_ms()
            if time.ticks_diff(now, last_read) >= period_ms:
                last_read = now
                
                if cny_adc:
                    # Leer con filtrado mejorado
                    raw = read_adc_filtered(cny_adc, samples=8)
                    
                    # Calcular voltaje
                    voltage = (raw / 4095.0) * 3.3
                    
                    # Reflectividad calibrada: valores altos = superficie clara
                    reflectivity = map_value(raw, CNY_MIN, CNY_MAX, 0, 100)
                    reflectivity = max(0, min(100, reflectivity))
                    
                    # Determinar tipo de superficie
                    if reflectivity < 30:
                        surface_type = "Oscura"
                    elif reflectivity < 70:
                        surface_type = "Media"
                    else:
                        surface_type = "Clara"
                else:
                    raw = 0
                    voltage = 0.0
                    reflectivity = 0
                    surface_type = "N/A"
                
                # Actualizar OLED
                oled_write("CNY70 Optico", f"ADC: {raw}", f"V: {voltage:.2f}V", f"Reflec: {reflectivity}%", surface_type)
                
                # Enviar datos
                msg = f"CNY_RAW:{raw},VOLTAGE:{voltage:.3f},REFLECTIVITY:{reflectivity},SURFACE:{surface_type}\n"
                try:
                    client.sendall(msg.encode())
                except Exception:
                    break
            
            time.sleep(0.05)
            
    except Exception as e:
        print(f"[Color CNY] Error: {e}")
    finally:
        print("[Color CNY] Módulo detenido")
        oled_status("Detenido")

# ============================================================================
# MÓDULO: COLOR TCS (Sensor TCS3200)
# ============================================================================

def color_tcs_loop(client):
    """Loop del módulo de color con sensor TCS3200"""
    global current_mode, continuous_client
    
    print("[Color TCS] Módulo activo")
    oled_status("Color TCS")
    
    # Configurar pines TCS3200
    s2 = None
    s3 = None
    out_pin = None
    s0 = None
    s1 = None
    
    try:
        # Pines de control de filtro
        s2 = Pin(32, Pin.OUT)
        s3 = Pin(33, Pin.OUT)
        # Pin de salida de frecuencia
        out_pin = Pin(36, Pin.IN)
        # Pines de escala de frecuencia (opcional, configurar a 100%)
        # S0=HIGH, S1=HIGH = 100% frequency scaling
        print("[Color TCS] TCS3200 configurado (S2:32, S3:33, OUT:36)")
    except Exception as e:
        print(f"[Color TCS] TCS3200 no disponible: {e}")
    
    # CALIBRACIÓN TCS3200
    # Estos valores deben calibrarse con superficie blanca y negra
    # Valores típicos obtenidos de calibración:
    R_MIN = 20   # Frecuencia mínima rojo (superficie negra)
    R_MAX = 150  # Frecuencia máxima rojo (superficie blanca)
    G_MIN = 25
    G_MAX = 180
    B_MIN = 15
    B_MAX = 140
    
    def select_filter(color):
        """Selecciona filtro de color: RED, GREEN, BLUE, CLEAR"""
        if s2 is None or s3 is None:
            return
        
        if color == 'RED':
            s2.value(0)
            s3.value(0)
        elif color == 'GREEN':
            s2.value(1)
            s3.value(1)
        elif color == 'BLUE':
            s2.value(0)
            s3.value(1)
        else:  # CLEAR
            s2.value(1)
            s3.value(0)
    
    def measure_pulse_width(color):
        """Mide el ancho de pulso del sensor para un color específico usando time_pulse_us"""
        select_filter(color)
        time.sleep_ms(20)  # Dar tiempo para estabilización del filtro
        
        try:
            # Medir duración de pulso LOW en microsegundos (timeout 50ms)
            pulse_width = time_pulse_us(out_pin, 0, 50000)
            if pulse_width > 0:
                return pulse_width
            else:
                return 0
        except Exception:
            return 0
    
    def time_pulse_us(pin, level, timeout_us):
        """Implementación simplificada de pulseIn para MicroPython"""
        start = time.ticks_us()
        # Esperar a que el pin esté en el nivel opuesto
        while pin.value() == level:
            if time.ticks_diff(time.ticks_us(), start) > timeout_us:
                return 0
        
        # Esperar a que el pin cambie al nivel deseado
        while pin.value() != level:
            if time.ticks_diff(time.ticks_us(), start) > timeout_us:
                return 0
        
        # Medir duración del pulso
        pulse_start = time.ticks_us()
        while pin.value() == level:
            if time.ticks_diff(time.ticks_us(), pulse_start) > timeout_us:
                return 0
        
        return time.ticks_diff(time.ticks_us(), pulse_start)
    
    period_ms = 400  # Periodo más largo para mediciones precisas
    last_read = 0
    
    try:
        client.settimeout(0.01)
        
        while current_mode == 'COLOR_TCS' and continuous_client == client:
            # Procesar comandos
            try:
                cmd = client.recv(64)
                if cmd:
                    txt = cmd.decode().strip().upper()
                    if 'STOP' in txt:
                        break
            except Exception:
                pass
            
            # Leer colores
            now = time.ticks_ms()
            if time.ticks_diff(now, last_read) >= period_ms:
                last_read = now
                
                if s2 and s3 and out_pin:
                    # Medir anchos de pulso para cada color
                    pulse_red = measure_pulse_width('RED')
                    pulse_green = measure_pulse_width('GREEN')
                    pulse_blue = measure_pulse_width('BLUE')
                    
                    # Convertir a frecuencias aproximadas (Hz)
                    # Frecuencia = 1 / (2 * pulse_width) cuando duty cycle = 50%
                    freq_red = (1000000.0 / (2 * pulse_red)) if pulse_red > 0 else 0
                    freq_green = (1000000.0 / (2 * pulse_green)) if pulse_green > 0 else 0
                    freq_blue = (1000000.0 / (2 * pulse_blue)) if pulse_blue > 0 else 0
                    
                    # Mapear frecuencias a valores RGB 0-255 con calibración
                    # Menor frecuencia (pulso más largo) = más color
                    red = map_value(int(freq_red), R_MIN, R_MAX, 255, 0)
                    green = map_value(int(freq_green), G_MIN, G_MAX, 255, 0)
                    blue = map_value(int(freq_blue), B_MIN, B_MAX, 255, 0)
                    
                    # Limitar valores a rango 0-255
                    red = max(0, min(255, red))
                    green = max(0, min(255, green))
                    blue = max(0, min(255, blue))
                else:
                    freq_red = freq_green = freq_blue = 0
                    red = green = blue = 0
                
                # Actualizar OLED
                oled_write("TCS3200 Color", f"R:{red:3d} G:{green:3d}", f"B:{blue:3d}", f"Hz:{freq_red:.0f}", f"{freq_green:.0f},{freq_blue:.0f}")
                
                # Enviar datos
                msg = f"TCS_RED:{red},TCS_GREEN:{green},TCS_BLUE:{blue},FREQ_R:{freq_red:.1f},FREQ_G:{freq_green:.1f},FREQ_B:{freq_blue:.1f}\n"
                try:
                    client.sendall(msg.encode())
                except Exception:
                    break
            
            time.sleep(0.05)
            
    except Exception as e:
        print(f"[Color TCS] Error: {e}")
    finally:
        print("[Color TCS] Módulo detenido")
        oled_status("Detenido")

# ============================================================================
# BUCLE PRINCIPAL DEL SERVIDOR
# ============================================================================

print("\n" + "=" * 50)
print("SERVIDOR LISTO - Esperando conexiones...")
print("=" * 50 + "\n")

# Ejecutar animación de entrada
animation_light_color()

# Mostrar estado de espera después de la animación
oled_status("Esperando...")

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
                time.sleep(0.1)  # Dar tiempo para que llegue la respuesta
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
        elif 'MODO:BRIGHTNESS' in data:
            current_mode = 'BRIGHTNESS'
            continuous_client = client
            client.sendall(b"BRIGHTNESS_OK\n")
            brightness_loop(client)
            
        elif 'MODO:COLOR_CNY' in data:
            current_mode = 'COLOR_CNY'
            continuous_client = client
            client.sendall(b"COLOR_CNY_OK\n")
            color_cny_loop(client)
            
        elif 'MODO:COLOR_TCS' in data:
            current_mode = 'COLOR_TCS'
            continuous_client = client
            client.sendall(b"COLOR_TCS_OK\n")
            color_tcs_loop(client)
            
        elif 'STOP' in data:
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
