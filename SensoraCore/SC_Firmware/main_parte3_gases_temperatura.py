# main_parte3_gases_temperatura.py - SensoraCore Alpha 0.4
# Módulos: Gas Regulation (MQ2/MQ3), Thermoregulation (LM35/DS18B20/MAX6675)
# Pantalla OLED 128x64 I2C integrada
# Autor: SensoraCore Team
# Fecha: 2025-11-21

import network  # type: ignore
import socket
import time
from machine import Pin, ADC, reset, SoftSPI, I2C  # type: ignore
import ssd1306  # type: ignore
from red import SSID, PASSWORD  # type: ignore

# ============================================================================
# CONFIGURACIÓN INICIAL
# ============================================================================

print("=" * 50)
print("SensoraCore ESP32 - Parte 3: Gases y Temperatura")
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
        oled.text("SensoraCore P3", 0, 0)
        oled.text("Gas & Temp", 0, 13)
        oled.text("-" * 16, 0, 26)
        oled.text(f"Modo:", 0, 39)
        oled.text(mode[:16], 0, 52)
        oled.show()
    except Exception:
        pass

# Mostrar pantalla de inicio
oled_write("SensoraCore P3", "Gas & Temp", "", "Iniciando...", "WiFi connecting")

# ============================================================================
# CONFIGURACIÓN DE HARDWARE - PINES GPIO
# ============================================================================

# LED integrado
led = Pin(2, Pin.OUT)

# --- MÓDULO: GAS REGULATION ---
# MQ2 en GPIO36 (ADC1_CH0 - input only, compatible WiFi)
# MQ3 en GPIO39 (ADC1_CH3 - input only, compatible WiFi)

# --- MÓDULO: THERMOREGULATION ---
# LM35 en GPIO34 (ADC1_CH6 - input only, compatible WiFi)
# DS18B20 en GPIO27 (OneWire digital, compatible WiFi)
# MAX6675 (Termopar Type-K) - Solo 5 pines: VCC, GND, SCK, SO, CS
#   SCK (Clock): GPIO32
#   SO (MISO): GPIO19 (solo salida del MAX6675, compatible WiFi)
#   CS (Chip Select): GPIO33
#   NOTA: MAX6675 NO usa MOSI (solo lectura)

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
            oled_write("SensoraCore P3", "WiFi...", f"Intento {attempt}/5", "", "")
            
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
# ANIMACIÓN DE ENTRADA - GASES Y TEMPERATURA
# ============================================================================

def animation_gas_temperature():
    """
    Animación de entrada: Nubes cielo → Nubes gas/spray → Spray → Termómetro → Hielo y Llama
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
        
        # FASE 1: Auto en movimiento botando humo (0-5s)
        phase_duration = 5000
        phase_start = time.ticks_ms()
        while time.ticks_diff(time.ticks_ms(), phase_start) < phase_duration:
            if time.ticks_diff(time.ticks_ms(), start_time) >= duration_ms:
                return
            
            oled.fill(0)
            
            progress = time.ticks_diff(time.ticks_ms(), phase_start) / phase_duration
            
            # Posición del auto (se mueve de izquierda a derecha)
            car_x = int(10 + 80 * progress)
            car_y = 38
            
            # Auto estilo lateral más detallado
            # Carrocería inferior (chasis)
            oled.hline(car_x + 4, car_y + 8, 18, 1)
            oled.hline(car_x + 3, car_y + 9, 20, 1)
            
            # Cuerpo principal del auto (forma trapezoidal)
            oled.line(car_x + 2, car_y + 8, car_x + 2, car_y + 2, 1)  # Parte trasera vertical
            oled.line(car_x + 2, car_y + 2, car_x + 6, car_y, 1)  # Inclinación trasera
            oled.hline(car_x + 6, car_y, 10, 1)  # Techo
            oled.line(car_x + 16, car_y, car_x + 23, car_y + 4, 1)  # Parabrisas/capó inclinado
            oled.line(car_x + 23, car_y + 4, car_x + 23, car_y + 8, 1)  # Frente vertical
            
            # Ventanas (espacios vacíos representados con líneas)
            oled.line(car_x + 7, car_y + 2, car_x + 12, car_y + 2, 1)  # Ventana superior
            oled.line(car_x + 7, car_y + 2, car_x + 7, car_y + 6, 1)  # División ventana
            
            # Ruedas con más detalle (círculos)
            # Rueda trasera
            for angle in range(0, 360, 30):
                rad = math.radians(angle)
                x = int(car_x + 7 + 3.5 * math.cos(rad))
                y = int(car_y + 10 + 3.5 * math.sin(rad))
                if 0 <= x < 128 and 0 <= y < 64:
                    oled.pixel(x, y, 1)
            oled.fill_rect(car_x + 6, car_y + 9, 3, 3, 1)  # Centro rueda
            
            # Rueda delantera
            for angle in range(0, 360, 30):
                rad = math.radians(angle)
                x = int(car_x + 18 + 3.5 * math.cos(rad))
                y = int(car_y + 10 + 3.5 * math.sin(rad))
                if 0 <= x < 128 and 0 <= y < 64:
                    oled.pixel(x, y, 1)
            oled.fill_rect(car_x + 17, car_y + 9, 3, 3, 1)  # Centro rueda
            
            # Tubo de escape (parte trasera inferior)
            oled.fill_rect(car_x, car_y + 7, 3, 2, 1)
            
            # Humo saliendo del escape (nubes de gases)
            num_smoke_puffs = int(6 + 4 * progress)
            for i in range(num_smoke_puffs):
                # Cada nube de humo se dispersa hacia atrás y arriba
                smoke_x = car_x - 8 - i * 5
                smoke_y = car_y - int(2 * i) + int(3 * math.sin(progress * 4 * math.pi + i * 0.5))
                
                if smoke_x > 0:
                    # Nube de humo pequeña (círculos superpuestos)
                    smoke_size = int(3 + i * 0.5)  # Crece al alejarse
                    
                    # Círculo principal
                    for angle in range(0, 360, 20):
                        rad = math.radians(angle)
                        x = int(smoke_x + smoke_size * math.cos(rad))
                        y = int(smoke_y + smoke_size * math.sin(rad))
                        if 0 <= x < 128 and 0 <= y < 64:
                            oled.pixel(x, y, 1)
                    
                    # Círculos adicionales para dar forma de nube
                    if smoke_size > 3:
                        for angle in range(0, 360, 30):
                            rad = math.radians(angle)
                            x = int(smoke_x + (smoke_size - 1) * math.cos(rad))
                            y = int(smoke_y + (smoke_size - 1) * math.sin(rad))
                            if 0 <= x < 128 and 0 <= y < 64:
                                oled.pixel(x, y, 1)
            
            # Línea de suelo
            oled.hline(0, car_y + 13, 128, 1)
            
            oled.show()
            time.sleep(0.05)
        
        # FASE 2: Nubes se transforman en gas/aerosol con spray (5-10s)
        phase_duration = 5000
        phase_start = time.ticks_ms()
        while time.ticks_diff(time.ticks_ms(), phase_start) < phase_duration:
            if time.ticks_diff(time.ticks_ms(), start_time) >= duration_ms:
                return
            
            oled.fill(0)
            
            progress = time.ticks_diff(time.ticks_ms(), phase_start) / phase_duration
            
            # Spray/aerosol apareciendo desde abajo
            spray_x = 64
            spray_y = int(60 - 20 * progress)
            
            # Cuerpo del spray (lata/botella)
            if progress > 0.2:
                oled.rect(spray_x - 6, spray_y, 12, 15, 1)
                oled.fill_rect(spray_x - 5, spray_y + 1, 10, 13, 1)
                # Tapa/boquilla
                oled.fill_rect(spray_x - 3, spray_y - 3, 6, 3, 1)
                oled.fill_rect(spray_x - 1, spray_y - 5, 2, 2, 1)
            
            # Partículas de gas saliendo del spray
            if progress > 0.4:
                num_particles = int(20 * (progress - 0.4) / 0.6)
                for i in range(num_particles):
                    # Partículas dispersas hacia arriba
                    offset_x = int(10 * math.sin(i * 0.8))
                    offset_y = -5 - i * 2
                    particle_x = spray_x + offset_x
                    particle_y = spray_y + offset_y
                    
                    if 0 <= particle_x < 128 and 0 <= particle_y < 64:
                        # Partículas como puntos pequeños
                        oled.pixel(particle_x, particle_y, 1)
                        if i % 2 == 0:
                            oled.pixel(particle_x + 1, particle_y, 1)
            
            # Nubes de gas en la parte superior (más dispersas)
            if progress > 0.6:
                for cloud_idx in range(2):
                    base_x = 30 + cloud_idx * 60
                    base_y = 10
                    
                    # Nubes más difusas (solo contornos)
                    for angle in range(0, 360, 15):
                        rad = math.radians(angle)
                        x = int(base_x + 12 * math.cos(rad))
                        y = int(base_y + 6 * math.sin(rad))
                        if 0 <= x < 128 and 0 <= y < 64:
                            oled.pixel(x, y, 1)
            
            oled.show()
            time.sleep(0.05)
        
        # FASE 3: Spray se transforma en termómetro (10-15s)
        phase_duration = 5000
        phase_start = time.ticks_ms()
        while time.ticks_diff(time.ticks_ms(), phase_start) < phase_duration:
            if time.ticks_diff(time.ticks_ms(), start_time) >= duration_ms:
                return
            
            oled.fill(0)
            
            progress = time.ticks_diff(time.ticks_ms(), phase_start) / phase_duration
            
            # Centro de la pantalla
            cx = 64
            
            if progress < 0.5:
                # Primera mitad: spray se alarga verticalmente
                t = progress * 2
                height = int(15 + 25 * t)
                width = int(12 - 6 * t)
                y_pos = 32 - height // 2
                
                # Cuerpo alargándose
                oled.rect(cx - width//2, y_pos, width, height, 1)
                oled.fill_rect(cx - width//2 + 1, y_pos + 1, width - 2, height - 2, 1)
                
                # Tapa desapareciendo
                if t < 0.5:
                    oled.fill_rect(cx - 3, y_pos - 3, 6, 3, 1)
                
            else:
                # Segunda mitad: emerge el termómetro completo
                t = (progress - 0.5) * 2
                
                # Bulbo del termómetro (parte inferior redonda)
                bulb_y = 50
                bulb_r = 5
                for angle in range(0, 360, 5):
                    rad = math.radians(angle)
                    x = int(cx + bulb_r * math.cos(rad))
                    y = int(bulb_y + bulb_r * math.sin(rad))
                    if 0 <= x < 128 and 0 <= y < 64:
                        oled.pixel(x, y, 1)
                
                # Tubo del termómetro
                tube_height = int(30 * t)
                oled.vline(cx - 3, bulb_y - tube_height, tube_height, 1)
                oled.vline(cx + 3, bulb_y - tube_height, tube_height, 1)
                
                # Tope superior
                if t > 0.5:
                    oled.hline(cx - 3, bulb_y - tube_height, 7, 1)
                
                # Líquido interior (rojo/mercurio) subiendo
                liquid_height = int(tube_height * t)
                if liquid_height > 0:
                    oled.fill_rect(cx - 1, bulb_y - liquid_height, 3, liquid_height, 1)
                
                # Marcas de temperatura en el tubo
                if t > 0.7:
                    for i in range(5):
                        mark_y = bulb_y - 5 - i * 5
                        oled.hline(cx + 4, mark_y, 3, 1)
            
            oled.show()
            time.sleep(0.05)
        
        # FASE 4: Del termómetro emergen hielo y llama (15-20s)
        phase_duration = 5000
        phase_start = time.ticks_ms()
        while time.ticks_diff(time.ticks_ms(), phase_start) < phase_duration:
            if time.ticks_diff(time.ticks_ms(), start_time) >= duration_ms:
                return
            
            oled.fill(0)
            
            progress = time.ticks_diff(time.ticks_ms(), phase_start) / phase_duration
            
            # Termómetro central (siempre visible)
            cx = 64
            bulb_y = 50
            bulb_r = 5
            
            # Bulbo
            for angle in range(0, 360, 5):
                rad = math.radians(angle)
                x = int(cx + bulb_r * math.cos(rad))
                y = int(bulb_y + bulb_r * math.sin(rad))
                if 0 <= x < 128 and 0 <= y < 64:
                    oled.pixel(x, y, 1)
            
            # Tubo
            tube_height = 30
            oled.vline(cx - 3, bulb_y - tube_height, tube_height, 1)
            oled.vline(cx + 3, bulb_y - tube_height, tube_height, 1)
            oled.hline(cx - 3, bulb_y - tube_height, 7, 1)
            
            # Líquido
            oled.fill_rect(cx - 1, bulb_y - 15, 3, 15, 1)
            
            # Marcas
            for i in range(5):
                mark_y = bulb_y - 5 - i * 5
                oled.hline(cx + 4, mark_y, 3, 1)
            
            # HIELO emergiendo a la izquierda (cristal hexagonal con detalles)
            if progress > 0.2:
                t = (progress - 0.2) / 0.8
                ice_x = int(25 + 5 * (1 - t))  # Se acerca desde fuera
                ice_y = 32
                ice_size = int(13 * t)
                
                if ice_size > 3:
                    # Cristal de hielo hexagonal (copo de nieve estilizado)
                    # Hexágono exterior
                    hex_r = ice_size
                    for i in range(6):
                        angle1 = i * 60
                        angle2 = (i + 1) * 60
                        rad1 = math.radians(angle1)
                        rad2 = math.radians(angle2)
                        x1 = int(ice_x + hex_r * math.cos(rad1))
                        y1 = int(ice_y + hex_r * math.sin(rad1))
                        x2 = int(ice_x + hex_r * math.cos(rad2))
                        y2 = int(ice_y + hex_r * math.sin(rad2))
                        oled.line(x1, y1, x2, y2, 1)
                    
                    # Brazos internos del copo (6 radios)
                    if t > 0.4:
                        inner_r = int(hex_r * 0.7)
                        for i in range(6):
                            angle = i * 60
                            rad = math.radians(angle)
                            x_end = int(ice_x + inner_r * math.cos(rad))
                            y_end = int(ice_y + inner_r * math.sin(rad))
                            oled.line(ice_x, ice_y, x_end, y_end, 1)
                            
                            # Pequeñas ramificaciones en los brazos
                            if t > 0.6:
                                mid_r = int(hex_r * 0.5)
                                x_mid = int(ice_x + mid_r * math.cos(rad))
                                y_mid = int(ice_y + mid_r * math.sin(rad))
                                
                                # Ramitas perpendiculares
                                perp_angle1 = angle + 30
                                perp_angle2 = angle - 30
                                branch_len = 3
                                
                                x_b1 = int(x_mid + branch_len * math.cos(math.radians(perp_angle1)))
                                y_b1 = int(y_mid + branch_len * math.sin(math.radians(perp_angle1)))
                                oled.line(x_mid, y_mid, x_b1, y_b1, 1)
                                
                                x_b2 = int(x_mid + branch_len * math.cos(math.radians(perp_angle2)))
                                y_b2 = int(y_mid + branch_len * math.sin(math.radians(perp_angle2)))
                                oled.line(x_mid, y_mid, x_b2, y_b2, 1)
                    
                    # Centro sólido
                    oled.fill_rect(ice_x - 1, ice_y - 1, 3, 3, 1)
            
            # LLAMA emergiendo a la derecha (fuego con capas)
            if progress > 0.2:
                t = (progress - 0.2) / 0.8
                flame_x = int(103 - 5 * (1 - t))  # Se acerca desde fuera
                flame_y = 40
                flame_height = int(20 * t)
                
                if flame_height > 5:
                    # Capa externa de la llama (amarillo/naranja simulado)
                    base_width = int(flame_height * 0.7)
                    
                    # Contorno exterior ondulado
                    for i in range(flame_height):
                        y = flame_y - i
                        progress_height = i / flame_height
                        
                        # Ancho que se reduce con ondulación
                        width_factor = (1 - progress_height) * (1 - progress_height)
                        oscillation = int(2 * math.sin(progress_height * math.pi * 3))
                        width = int(base_width * width_factor) + oscillation
                        
                        if width > 0 and 0 <= y < 64:
                            # Contornos laterales
                            if flame_x - width >= 0:
                                oled.pixel(flame_x - width, y, 1)
                            if flame_x + width < 128:
                                oled.pixel(flame_x + width, y, 1)
                    
                    # Base de la llama (más ancha y sólida)
                    oled.hline(flame_x - base_width//2, flame_y, base_width, 1)
                    if t > 0.3:
                        oled.hline(flame_x - base_width//2 + 1, flame_y - 1, base_width - 2, 1)
                    
                    # Punta afilada con ondulación
                    tip_oscillation = int(2 * math.sin(t * math.pi * 4))
                    tip_y = flame_y - flame_height
                    oled.pixel(flame_x + tip_oscillation, tip_y, 1)
                    oled.pixel(flame_x + tip_oscillation, tip_y + 1, 1)
                    
                    # Capa interna (núcleo caliente - más brillante)
                    if t > 0.5:
                        inner_height = int(flame_height * 0.65)
                        inner_base = int(base_width * 0.5)
                        
                        for i in range(inner_height):
                            y = flame_y - 3 - i
                            progress_inner = i / inner_height
                            inner_width = int(inner_base * (1 - progress_inner) * (1 - progress_inner * 0.7))
                            
                            if inner_width > 0 and 0 <= y < 64:
                                if flame_x - inner_width >= 0:
                                    oled.pixel(flame_x - inner_width, y, 1)
                                if flame_x + inner_width < 128:
                                    oled.pixel(flame_x + inner_width, y, 1)
                        
                        # Núcleo central muy pequeño (más blanco/caliente)
                        if t > 0.7:
                            core_height = int(flame_height * 0.3)
                            for i in range(core_height):
                                y = flame_y - 5 - i
                                if 0 <= y < 64:
                                    oled.pixel(flame_x, y, 1)
            
            oled.show()
            time.sleep(0.05)
        
        print("[Animación] Secuencia completada")
        
    except Exception as e:
        print(f"[Animación] Error: {e}")

# ============================================================================
# MÓDULO: THERMOREGULATION (LM35, DS18B20, Termopar Type-K)
# ============================================================================

def thermoregulation_loop(client):
    """Loop del módulo de termorregulación con múltiples sensores"""
    global current_mode, continuous_client
    
    print("[Thermoregulation] Módulo activo")
    oled_status("Thermoregulation")
    
    # Configurar sensores
    # LM35 en GPIO34 (ADC)
    lm35_adc = None
    try:
        lm35_adc = ADC(Pin(34))
        lm35_adc.atten(ADC.ATTN_11DB)
        lm35_adc.width(ADC.WIDTH_12BIT)
        print("[Thermo] LM35 configurado en GPIO34")
    except Exception as e:
        print(f"[Thermo] LM35 no disponible: {e}")
    
    # DS18B20 en GPIO27 (OneWire)
    ds_sensor = None
    ds_rom = None
    try:
        import onewire  # type: ignore
        import ds18x20  # type: ignore
        ow = onewire.OneWire(Pin(27))
        ds_sensor = ds18x20.DS18X20(ow)
        roms = ds_sensor.scan()
        if roms:
            ds_rom = roms[0]
            print(f"[Thermo] DS18B20 encontrado: {ds_rom.hex()}")
        else:
            print("[Thermo] DS18B20 no encontrado")
    except Exception as e:
        print(f"[Thermo] DS18B20 no disponible: {e}")
    
    # MAX6675 (Termopar Type-K) - Solo 3 pines SPI
    spi = None
    cs = None
    try:
        # MAX6675 solo usa SCK, SO (MISO), CS - NO requiere MOSI
        # SoftSPI requiere mosi aunque no se use físicamente
        spi = SoftSPI(baudrate=1000000, polarity=0, phase=0,
                     sck=Pin(32), mosi=Pin(25), miso=Pin(19))
        cs = Pin(33, Pin.OUT)
        cs.value(1)
        print("[Thermo] MAX6675 configurado: SCK=32, SO=19, CS=33")
    except Exception as e:
        print(f"[Thermo] MAX6675 no disponible: {e}")
    
    # Funciones de lectura
    def read_lm35():
        """Lee LM35 con compensación de no-linealidad del ADC ESP32
        NOTA: LM35 alimentado a 5V, pero ADC ESP32 lee máximo 3.3V
        """
        if lm35_adc is None:
            return -999
        try:
            # Promediar múltiples lecturas para estabilidad
            raw = read_adc_filtered(lm35_adc, samples=20)
            
            # Compensación de no-linealidad del ADC ESP32
            # El ADC ESP32 es no-lineal en los extremos (0-150mV y 3150-3300mV)
            # Rango útil: 150mV - 3150mV (aprox 150-4000 ADC)
            
            # IMPORTANTE: ADC ESP32 lee máximo 3.3V aunque LM35 esté a 5V
            # LM35 con Vcc=5V puede dar hasta 1.5V (150°C)
            # Esto está dentro del rango del ADC (0-3.3V)
            voltage = (raw / 4095.0) * 3.3
            
            # LM35: 10mV/°C (0.01V/°C) sin importar Vcc
            # La salida es proporcional a temperatura, no a Vcc
            # Fórmula: Temp(°C) = Voltage(V) × 100
            temp_c = voltage * 100.0
            
            # Validar rango físico del LM35
            # Con Vcc=5V y ADC=3.3V máximo:
            # Rango medible: 0°C a 150°C (0V a 1.5V) - limitado por LM35
            # ADC puede leer hasta 330°C teórico (3.3V), pero LM35 máx es 150°C
            if temp_c < -10 or temp_c > 150:
                return -999
            
            return round(temp_c, 2)
        except Exception as e:
            print(f"[LM35] Error lectura: {e}")
            return -999
    
    def read_ds18b20():
        """Lee DS18B20 digital con protocolo OneWire"""
        if ds_sensor is None or ds_rom is None:
            return -999
        try:
            # Iniciar conversión de temperatura
            ds_sensor.convert_temp()
            
            # Esperar tiempo de conversión según resolución:
            # 9-bit: 93.75ms, 10-bit: 187.5ms, 11-bit: 375ms, 12-bit: 750ms
            # Por defecto usa 12-bit (máxima precisión: 0.0625°C)
            time.sleep_ms(750)
            
            # Leer temperatura
            temp_c = ds_sensor.read_temp(ds_rom)
            
            # Validar rango DS18B20 (-55°C a +125°C)
            if temp_c < -55 or temp_c > 125:
                print(f"[DS18B20] Temp fuera de rango: {temp_c}°C")
                return -999
            
            # Verificar lectura válida (DS18B20 devuelve 85°C si hay error)
            if temp_c == 85.0:
                print("[DS18B20] Lectura de error (85°C) - sensor no listo")
                return -999
            
            return round(temp_c, 2)
        except OSError as e:
            print(f"[DS18B20] Error OneWire: {e}")
            return -999
        except Exception as e:
            print(f"[DS18B20] Error lectura: {e}")
            return -999
    
    def read_max6675():
        """Lee MAX6675 (termopar Type-K) vía SPI"""
        if spi is None or cs is None:
            return -999
        try:
            # Activar chip (CS LOW)
            cs.value(0)
            # Esperar tiempo de setup (100ns típico)
            time.sleep_us(1)
            
            # Leer 2 bytes (16 bits) del MAX6675
            data = spi.read(2)
            
            # Desactivar chip (CS HIGH)
            cs.value(1)
            
            if len(data) != 2:
                print("[MAX6675] Error: datos incompletos")
                return -999
            
            # Combinar bytes (MSB primero)
            raw = (data[0] << 8) | data[1]
            
            # Estructura de datos MAX6675 (16 bits):
            # Bit 15-3: Temperatura (12 bits, signo + 11 bits datos)
            # Bit 2 (D2): Thermocouple Input Open (1 = desconectado)
            # Bit 1: Siempre 0
            # Bit 0: Device ID (siempre 0 para MAX6675)
            
            # Verificar bit D2 (termopar desconectado)
            if raw & 0x0004:  # Bit 2
                print("[MAX6675] ERROR: Termopar desconectado o en circuito abierto")
                return -999
            
            # Verificar bit 0 (debe ser 0 para MAX6675 válido)
            if raw & 0x0001:
                print("[MAX6675] ERROR: Bit de ID inválido")
                return -999
            
            # Extraer temperatura: bits [14:3] = 12 bits
            # Desplazar 3 bits a la derecha y aplicar máscara
            temp_bits = (raw >> 3) & 0x0FFF
            
            # Conversión: cada bit = 0.25°C (resolución 12-bit)
            temp_c = temp_bits * 0.25
            
            # Validar rango MAX6675 con termopar Type-K
            # Rango: 0°C a +1024°C (limitado por MAX6675)
            # Termopar Type-K soporta -200°C a +1350°C
            if temp_c < 0 or temp_c > 1024:
                print(f"[MAX6675] Temp fuera de rango: {temp_c}°C")
                return -999
            
            # Nota: MAX6675 incluye compensación de unión fría automática
            return round(temp_c, 2)
            
        except Exception as e:
            print(f"[MAX6675] Error lectura SPI: {e}")
            return -999
    
    # Estado inicial
    selected_sensor = 'LM35'
    period_ms = 500
    last_read = 0
    
    # Parámetros de calibración por sensor (offset y escala)
    # Temp_calibrada = (Temp_medida + offset) * escala
    calib_params = {
        'LM35': {'offset': 0.0, 'scale': 1.0},
        'DS18B20': {'offset': 0.0, 'scale': 1.0},
        'MAX6675': {'offset': 0.0, 'scale': 1.0}
    }
    
    try:
        client.settimeout(0.1)
        
        while current_mode == 'THERMOREGULATION' and continuous_client == client:
            # Procesar comandos
            try:
                cmd = client.recv(128)
                if cmd:
                    txt = cmd.decode().strip().upper()
                    
                    if 'SENSOR:LM35' in txt:
                        selected_sensor = 'LM35'
                        print(f"[Thermo] Cambiado a {selected_sensor}")
                        client.sendall(b"OK:SENSOR_LM35\n")
                    elif 'SENSOR:DS18B20' in txt:
                        selected_sensor = 'DS18B20'
                        print(f"[Thermo] Cambiado a {selected_sensor}")
                        client.sendall(b"OK:SENSOR_DS18B20\n")
                    elif 'SENSOR:MAX6675' in txt:
                        selected_sensor = 'MAX6675'
                        print(f"[Thermo] Cambiado a {selected_sensor}")
                        client.sendall(b"OK:SENSOR_MAX6675\n")
                    elif 'CALIB_OFFSET:' in txt:
                        # Comando: CALIB_OFFSET:LM35:-2.5
                        parts = txt.split(':')
                        if len(parts) >= 3:
                            sensor = parts[1].strip()
                            try:
                                offset_val = float(parts[2])
                                if sensor in calib_params:
                                    calib_params[sensor]['offset'] = offset_val
                                    print(f"[Thermo] {sensor} offset: {offset_val}°C")
                                    client.sendall(f"OK:OFFSET_{sensor}={offset_val}\n".encode())
                                else:
                                    client.sendall(b"ERROR:INVALID_SENSOR\n")
                            except ValueError:
                                client.sendall(b"ERROR:INVALID_OFFSET_VALUE\n")
                    elif 'CALIB_SCALE:' in txt:
                        # Comando: CALIB_SCALE:LM35:1.02
                        parts = txt.split(':')
                        if len(parts) >= 3:
                            sensor = parts[1].strip()
                            try:
                                scale_val = float(parts[2])
                                if sensor in calib_params and scale_val > 0:
                                    calib_params[sensor]['scale'] = scale_val
                                    print(f"[Thermo] {sensor} escala: {scale_val}")
                                    client.sendall(f"OK:SCALE_{sensor}={scale_val}\n".encode())
                                else:
                                    client.sendall(b"ERROR:INVALID_SCALE\n")
                            except ValueError:
                                client.sendall(b"ERROR:INVALID_SCALE_VALUE\n")
                    elif 'GET_CALIB:' in txt:
                        # Comando: GET_CALIB:LM35
                        parts = txt.split(':')
                        if len(parts) >= 2:
                            sensor = parts[1].strip()
                            if sensor in calib_params:
                                offset = calib_params[sensor]['offset']
                                scale = calib_params[sensor]['scale']
                                msg = f"CALIB_{sensor}:OFFSET={offset},SCALE={scale}\n"
                                client.sendall(msg.encode())
                    elif 'STOP' in txt:
                        break
            except Exception:
                pass
            
            # Leer sensor según selección
            now = time.ticks_ms()
            if time.ticks_diff(now, last_read) >= period_ms:
                last_read = now
                
                if selected_sensor == 'LM35':
                    temp_raw = read_lm35()
                    sensor_label = "LM35"
                elif selected_sensor == 'DS18B20':
                    temp_raw = read_ds18b20()
                    sensor_label = "DS18B20"
                else:  # MAX6675
                    temp_raw = read_max6675()
                    sensor_label = "MAX6675"
                
                # Aplicar calibración si la temperatura es válida
                if temp_raw != -999:
                    offset = calib_params[selected_sensor]['offset']
                    scale = calib_params[selected_sensor]['scale']
                    temp_calibrated = (temp_raw + offset) * scale
                else:
                    temp_calibrated = temp_raw
                
                # Actualizar OLED
                if temp_raw != -999:
                    oled_write("Thermoregulation", sensor_label, f"Raw: {temp_raw:.1f}C", f"Cal: {temp_calibrated:.1f}C", "")
                else:
                    oled_write("Thermoregulation", sensor_label, "ERROR lectura", "", "")
                
                # Enviar datos (incluir temperatura raw y calibrada)
                msg = f"SENSOR:{selected_sensor},TEMP_C:{temp_calibrated:.2f},TEMP_RAW:{temp_raw:.2f}\n"
                try:
                    client.sendall(msg.encode())
                except Exception:
                    break
            
            time.sleep(0.05)
            
    except Exception as e:
        print(f"[Thermoregulation] Error: {e}")
    finally:
        print("[Thermoregulation] Módulo detenido")
        oled_status("Detenido")

# ============================================================================
# MÓDULO: GAS REGULATION (Sensores MQ2/MQ3)
# ============================================================================

def warmup_with_progress(sensor_name, duration_sec=20):
    """
    Muestra cuenta regresiva con barra de progreso en OLED durante calentamiento
    
    Parámetros:
    - sensor_name: Nombre del sensor (ej: 'MQ2', 'MQ3')
    - duration_sec: Duración en segundos
    """
    print(f"[{sensor_name}] Calentando por {duration_sec}s...")
    
    start_time = time.ticks_ms()
    
    while True:
        elapsed_ms = time.ticks_diff(time.ticks_ms(), start_time)
        elapsed_sec = elapsed_ms / 1000.0
        
        if elapsed_sec >= duration_sec:
            break
        
        # Calcular tiempo restante
        remaining = duration_sec - elapsed_sec
        progress = (elapsed_sec / duration_sec) * 100.0
        
        # Crear barra de progreso ASCII (16 caracteres para OLED de 128px)
        bar_length = 16
        filled = int((progress / 100.0) * bar_length)
        bar = "#" * filled + "-" * (bar_length - filled)
        
        # Actualizar OLED con cuenta regresiva y barra
        oled_write(
            "Calentamiento",
            f"{sensor_name}",
            f"Restante: {int(remaining)}s",
            f"[{bar}]",
            f"{int(progress)}%"
        )
        
        time.sleep(0.5)  # Actualizar cada 500ms
    
    print(f"[{sensor_name}] Calentamiento completado")
    oled_write("Calentamiento", f"{sensor_name}", "Completado", "Listo!", "")
    time.sleep(1)

def read_mq_sensor(adc, sensor_name, samples=20, R0=None, RL=10000.0):
    """
    Lectura filtrada de sensor MQ con algoritmo PPM real basado en Rs/R0
    
    Parámetros:
    - adc: ADC configurado
    - sensor_name: 'MQ2' o 'MQ3'
    - samples: muestras para promedio (default 20)
    - R0: Resistencia del sensor en aire limpio (calibración). Si None, usa valores por defecto
    - RL: Resistencia de carga en el módulo (típicamente 10kΩ)
    
    Retorna: (raw, voltage, Rs, ppm) o None si hay error
    
    Algoritmo basado en:
    - Rs = RL * (Vcc - Vout) / Vout
    - ratio = Rs / R0
    - PPM = 10^((log10(ratio) - b) / m)  [curva característica del datasheet]
    """
    if not adc:
        return None
    
    try:
        raw = read_adc_filtered(adc, samples=samples)
        
        # Voltaje de salida del sensor (0-3.3V)
        voltage = (raw / 4095.0) * 3.3
        
        # Protección contra división por cero
        if voltage < 0.01:
            voltage = 0.01
        
        # Calcular Rs (resistencia del sensor)
        # Vcc = 5V (alimentación del sensor)
        # Formula: Rs = RL * (Vcc - Vout) / Vout
        Vcc = 5.0
        Rs = RL * (Vcc - voltage) / voltage
        
        # Valores R0 por defecto si no hay calibración
        # R0 = resistencia del sensor en aire limpio (200-300 ppm típico)
        if R0 is None:
            if sensor_name == 'MQ2':
                R0 = 10000.0  # Valor típico del datasheet
            elif sensor_name == 'MQ3':
                R0 = 60000.0  # Valor típico del datasheet
            else:
                R0 = 10000.0
        
        # Calcular ratio Rs/R0
        ratio = Rs / R0
        
        # Calcular PPM usando curvas características logarítmicas del datasheet
        # Ecuación: log10(PPM) = m * log10(Rs/R0) + b
        # O bien: PPM = 10^((log10(ratio) - b) / m)
        
        if sensor_name == 'MQ2':
            # MQ2 - Curva para H2 (hidrógeno) como referencia general
            # Pendiente aproximada: m = -0.45, intercepto b = 2.3
            # Rango: 200-10000 PPM
            m = -0.45
            b = 2.3
            if ratio <= 0:
                ppm = 200.0  # Mínimo detectable
            else:
                import math
                log_ratio = math.log10(ratio)
                log_ppm = m * log_ratio + b
                ppm = 10 ** log_ppm
                # Limitar rango
                if ppm < 200:
                    ppm = 200.0
                elif ppm > 10000:
                    ppm = 10000.0
        
        elif sensor_name == 'MQ3':
            # MQ3 - Curva para alcohol etílico
            # Pendiente aproximada: m = -0.36, intercepto b = 2.0
            # Rango: 25-500 PPM (0.05-10 mg/L)
            m = -0.36
            b = 2.0
            if ratio <= 0:
                ppm = 25.0  # Mínimo detectable
            else:
                import math
                log_ratio = math.log10(ratio)
                log_ppm = m * log_ratio + b
                ppm = 10 ** log_ppm
                # Limitar rango
                if ppm < 25:
                    ppm = 25.0
                elif ppm > 500:
                    ppm = 500.0
        else:
            ppm = 0.0
        
        return (raw, voltage, Rs, ppm)
    
    except Exception as e:
        print(f"[{sensor_name}] Error de lectura: {e}")
        return None

def gas_regulation_loop(client):
    """
    Módulo de regulación de gases (MQ2, MQ3)
    
    Comandos:
    - SENSOR:MQx          -> Seleccionar sensor
    - CALIB_R0:MQx:valor  -> Establecer R0 de calibración
    - GET_R0:MQx          -> Obtener R0 actual
    - STOP                -> Detener módulo
    
    IMPORTANTE: Sensores MQ requieren precalentamiento:
    - Primera vez o almacenamiento prolongado: 24-48 horas
    - Uso reciente: 5-10 minutos (implementado 20s mínimo)
    
    Referencias:
    - https://esp32io.com/tutorials/esp32-gas-sensor
    """
    global current_mode, continuous_client
    
    print("[Gas Regulation] Módulo activo")
    oled_status("Gas Regulation")
    
    # Configurar ADCs
    mq2_adc = None
    mq3_adc = None
    
    try:
        # MQ2 en GPIO36 (ADC1_CH0) - Compatible con WiFi
        mq2_adc = ADC(Pin(36))
        mq2_adc.atten(ADC.ATTN_11DB)  # Rango 0-3.3V (máx aprox 3.6V)
        mq2_adc.width(ADC.WIDTH_12BIT)  # 12 bits = 0-4095
        print("[Gas] MQ2 configurado en GPIO36")
    except Exception as e:
        print(f"[Gas] MQ2 no disponible: {e}")
    
    try:
        # MQ3 en GPIO39 (ADC1_CH3) - Compatible con WiFi
        mq3_adc = ADC(Pin(39))
        mq3_adc.atten(ADC.ATTN_11DB)
        mq3_adc.width(ADC.WIDTH_12BIT)
        print("[Gas] MQ3 configurado en GPIO39")
    except Exception as e:
        print(f"[Gas] MQ3 no disponible: {e}")
    
    # Periodo de calentamiento con visualización mejorada
    # Calentar cada sensor disponible por separado
    if mq2_adc:
        warmup_with_progress("MQ2", duration_sec=20)
    if mq3_adc:
        warmup_with_progress("MQ3", duration_sec=20)
    
    print("[Gas] Todos los sensores listos para monitoreo")
    oled_status("Gas: Listo")
    
    selected_sensor = 'MQ2'
    period_ms = 500  # Lectura cada 500ms
    last_read = 0
    
    # Valores R0 de calibración (pueden ser actualizados por comandos)
    R0_mq2 = None  # None = usar valor por defecto
    R0_mq3 = None
    RL = 10000.0  # Resistencia de carga (10kΩ típico)
    
    try:
        client.settimeout(0.1)
        
        while current_mode == 'GAS_REGULATION' and continuous_client == client:
            # Procesar comandos
            try:
                cmd = client.recv(128)
                if cmd:
                    txt = cmd.decode().strip().upper()
                    
                    if 'SENSOR:MQ2' in txt:
                        selected_sensor = 'MQ2'
                        print(f"[Gas] Cambiado a {selected_sensor}")
                        client.sendall(b"OK:SENSOR_MQ2\n")
                    elif 'SENSOR:MQ3' in txt:
                        selected_sensor = 'MQ3'
                        print(f"[Gas] Cambiado a {selected_sensor}")
                        client.sendall(b"OK:SENSOR_MQ3\n")
                    elif 'CALIB_R0:' in txt:
                        # Comando: CALIB_R0:MQ2:10000.0
                        parts = txt.split(':')
                        if len(parts) >= 3:
                            sensor = parts[1].strip()
                            try:
                                r0_val = float(parts[2])
                                if sensor == 'MQ2':
                                    R0_mq2 = r0_val
                                    print(f"[Gas] R0 MQ2 calibrado: {r0_val} Ω")
                                    client.sendall(f"OK:R0_MQ2={r0_val}\n".encode())
                                elif sensor == 'MQ3':
                                    R0_mq3 = r0_val
                                    print(f"[Gas] R0 MQ3 calibrado: {r0_val} Ω")
                                    client.sendall(f"OK:R0_MQ3={r0_val}\n".encode())
                            except ValueError:
                                client.sendall(b"ERROR:INVALID_R0_VALUE\n")
                    elif 'GET_R0:' in txt:
                        # Comando: GET_R0:MQ2
                        parts = txt.split(':')
                        if len(parts) >= 2:
                            sensor = parts[1].strip()
                            if sensor == 'MQ2':
                                val = R0_mq2 if R0_mq2 else 10000.0
                                client.sendall(f"R0_MQ2:{val}\n".encode())
                            elif sensor == 'MQ3':
                                val = R0_mq3 if R0_mq3 else 60000.0
                                client.sendall(f"R0_MQ3:{val}\n".encode())
                    elif 'STOP' in txt:
                        break
            except Exception:
                pass
            
            # Leer sensor según selección
            now = time.ticks_ms()
            if time.ticks_diff(now, last_read) >= period_ms:
                last_read = now
                
                result = None
                sensor_label = ""
                r0_used = None
                
                if selected_sensor == 'MQ2' and mq2_adc:
                    r0_used = R0_mq2
                    result = read_mq_sensor(mq2_adc, 'MQ2', samples=20, R0=r0_used, RL=RL)
                    sensor_label = "MQ2 (Humo/LPG)"
                elif selected_sensor == 'MQ3' and mq3_adc:
                    r0_used = R0_mq3
                    result = read_mq_sensor(mq3_adc, 'MQ3', samples=20, R0=r0_used, RL=RL)
                    sensor_label = "MQ3 (Alcohol)"
                
                if result is None:
                    # Sensor no disponible o error de lectura
                    oled_write("Gas Regulation", "ERROR", f"{selected_sensor}", "no disponible", "")
                    msg = f"SENSOR:{selected_sensor},ERROR:NOT_AVAILABLE\n"
                    try:
                        client.sendall(msg.encode())
                    except Exception:
                        break
                    time.sleep(0.05)
                    continue
                
                raw, voltage, Rs, ppm = result
                
                # Actualizar OLED
                oled_write("Gas Regulation", sensor_label, f"ADC: {raw}", f"V: {voltage:.2f}V", f"PPM: {ppm:.1f}")
                
                # Enviar datos (incluir Rs para calibración en app)
                msg = f"SENSOR:{selected_sensor},RAW:{raw},VOLTAGE:{voltage:.3f},RS:{Rs:.2f},PPM:{ppm:.2f}\n"
                try:
                    client.sendall(msg.encode())
                except Exception:
                    break
            
            time.sleep(0.05)
            
    except Exception as e:
        print(f"[Gas Regulation] Error: {e}")
    finally:
        print("[Gas Regulation] Módulo detenido")
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
        
        elif 'MODO:THERMOREGULATION' in data:
            current_mode = 'THERMOREGULATION'
            continuous_client = client
            client.sendall(b"THERMOREGULATION_OK\n")
            thermoregulation_loop(client)
        
        elif 'MODO:GAS_REGULATION' in data:
            current_mode = 'GAS_REGULATION'
            continuous_client = client
            client.sendall(b"GAS_REGULATION_OK\n")
            gas_regulation_loop(client)
        
        elif 'STOP' in data:
            client.sendall(b"STOPPED\n")
        
        else:
            client.send(b"UNKNOWN_CMD\n")
        
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
    animation_gas_temperature()
    animation_running = False  # La función ya maneja sus 20s internamente

# Si la animación terminó sin interrupción, mostrar estado de espera
if animation_running or time.ticks_diff(time.ticks_ms(), animation_start) >= 20000:
    oled_status("Esperando...")

# Restaurar timeout normal del servidor
server.settimeout(30)

while True:
    client = None
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
        elif 'MODO:THERMOREGULATION' in data:
            current_mode = 'THERMOREGULATION'
            continuous_client = client
            client.sendall(b"THERMOREGULATION_OK\n")
            thermoregulation_loop(client)
            
        elif 'MODO:GAS_REGULATION' in data:
            current_mode = 'GAS_REGULATION'
            continuous_client = client
            client.sendall(b"GAS_REGULATION_OK\n")
            gas_regulation_loop(client)
            
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
        if client:
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
        if client:
            try:
                client.close()
            except Exception:
                pass
