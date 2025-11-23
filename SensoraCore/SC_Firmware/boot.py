# boot.py - SensoraCore ESP32
# Ejecutado en cada arranque del sistema
# Animación de bienvenida y configuración inicial

import time
from machine import Pin, SoftI2C  # type: ignore

# ============================================================================
# CONFIGURACIÓN OLED
# ============================================================================

# Configuración I2C para pantalla OLED SSD1306
try:
    i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
    from ssd1306 import SSD1306_I2C  # type: ignore
    oled = SSD1306_I2C(128, 64, i2c)
    oled_enabled = True
    print("[Boot] OLED detectado y configurado")
except Exception as e:
    oled = None
    oled_enabled = False
    print(f"[Boot] OLED no disponible: {e}")

# ============================================================================
# ANIMACIÓN DE BIENVENIDA
# ============================================================================

def boot_animation():
    """
    Animación de bienvenida al arranque de SensoraCore
    Muestra el logo, nombre del proyecto y autor
    Duración: ~8 segundos
    """
    if not oled_enabled or not oled:
        print("\n" + "="*50)
        print("   SENSORACORE - Sistema de Sensores ESP32")
        print("   Autor: Yamith.R")
        print("="*50 + "\n")
        time.sleep(2)
        return
    
    try:
        import math
        
        # FASE 1: Logo animado - Sensor con ondas (0-3s)
        print("[Boot] Iniciando animación de bienvenida...")
        start = time.ticks_ms()
        duration = 3000
        
        while time.ticks_diff(time.ticks_ms(), start) < duration:
            oled.fill(0)
            progress = time.ticks_diff(time.ticks_ms(), start) / duration
            
            # Centro del sensor (círculo)
            cx, cy = 64, 28
            sensor_r = 8
            
            # Círculo del sensor
            for angle in range(0, 360, 8):
                rad = math.radians(angle)
                x = int(cx + sensor_r * math.cos(rad))
                y = int(cy + sensor_r * math.sin(rad))
                if 0 <= x < 128 and 0 <= y < 64:
                    oled.pixel(x, y, 1)
            
            # Núcleo del sensor
            oled.fill_rect(cx - 3, cy - 3, 7, 7, 1)
            
            # Ondas expandiéndose (3 ondas concéntricas)
            for wave in range(3):
                wave_progress = (progress + wave * 0.33) % 1.0
                wave_r = int(sensor_r + 25 * wave_progress)
                alpha = 1.0 - wave_progress  # Desvanecimiento
                
                if wave_r < 40 and alpha > 0.2:
                    # Dibujar onda circular
                    for angle in range(0, 360, 12):
                        rad = math.radians(angle)
                        x = int(cx + wave_r * math.cos(rad))
                        y = int(cy + wave_r * math.sin(rad))
                        if 0 <= x < 128 and 0 <= y < 64:
                            oled.pixel(x, y, 1)
            
            # Puntos de datos flotantes (representando información)
            num_dots = 8
            for i in range(num_dots):
                angle = (progress * 360 + i * 45) % 360
                rad = math.radians(angle)
                dist = sensor_r + 15
                x = int(cx + dist * math.cos(rad))
                y = int(cy + dist * math.sin(rad))
                if 0 <= x < 128 and 0 <= y < 64:
                    oled.fill_rect(x - 1, y - 1, 3, 3, 1)
            
            oled.show()
            time.sleep(0.05)
        
        # FASE 2: Nombre del proyecto apareciendo (3-5.5s)
        start = time.ticks_ms()
        duration = 4000
        
        while time.ticks_diff(time.ticks_ms(), start) < duration:
            oled.fill(0)
            progress = time.ticks_diff(time.ticks_ms(), start) / duration
            
            # Texto "SENSORACORE" con efecto de aparecer letra por letra
            text = "SENSORACORE"
            visible_chars = int(len(text) * progress)
            display_text = text[:visible_chars]
            
            # Centrar texto (fuente 8x8, aprox 88 pixels de ancho)
            x_pos = (128 - len(display_text) * 8) // 2
            oled.text(display_text, x_pos, 20, 1)
            
            # Líneas decorativas que crecen
            if progress > 0.3:
                line_progress = (progress - 0.3) / 0.7
                line_width = int(50 * line_progress)
                # Línea superior
                oled.hline(64 - line_width // 2, 15, line_width, 1)
                # Línea inferior
                oled.hline(64 - line_width // 2, 35, line_width, 1)
            
            # Versión/subtítulo apareciendo
            if progress > 0.2:
                subtitle_progress = (progress - 0.6) / 0.4
                if subtitle_progress > 0.1:
                    oled.text("Sensores ESP32", 10, 45, 1)
            
            oled.show()
            time.sleep(0.05)
        
        # FASE 3: Autor apareciendo (5.5-7.5s)
        start = time.ticks_ms()
        duration = 3000
        
        # Mantener nombre del proyecto visible
        oled.fill(0)
        oled.text("SENSORACORE", 12, 10, 1)
        oled.hline(14, 20, 100, 1)
        
        while time.ticks_diff(time.ticks_ms(), start) < duration:
            progress = time.ticks_diff(time.ticks_ms(), start) / duration
            
            # "Por" aparece primero
            if progress > 0.2:
                oled.text("Por", 48, 30, 1)
            
            # Nombre del autor con efecto de desvanecimiento
            if progress > 0.4:
                author_progress = (progress - 0.4) / 0.6
                # Efecto de parpadeo inicial
                if author_progress < 0.3 or int(author_progress * 10) % 2 == 0 or author_progress > 0.7:
                    oled.text("Yamith.R", 36, 42, 1)
            
            oled.show()
            time.sleep(0.05)
        
        # FASE 4: Módulos indicadores (7.5-8s)
        oled.fill(0)
        oled.text("SENSORACORE", 12, 5, 1)
        oled.text("Yamith.R", 36, 18, 1)
        oled.hline(10, 28, 108, 1)
        
        # Iconos de módulos (representación gráfica de sensores)
        modules_icons = [
            (15, 35), (35, 35), (55, 35), (75, 35), (95, 35),  # Fila 1
            (15, 50), (35, 50), (55, 50), (75, 50), (95, 50), (115, 50)  # Fila 2 (11 módulos)
        ]
        
        start = time.ticks_ms()
        while time.ticks_diff(time.ticks_ms(), start) < 500:
            progress = time.ticks_diff(time.ticks_ms(), start) / 500
            num_visible = int(len(modules_icons) * progress)
            
            for i in range(num_visible):
                x, y = modules_icons[i]
                # Pequeño cuadrado para cada módulo
                oled.fill_rect(x, y, 3, 3, 1)
            
            oled.show()
            time.sleep(0.05)
        
        time.sleep(0.5)
        
        # Transición final
        for fade in range(4):
            oled.fill(0 if fade % 2 else 1)
            oled.show()
            time.sleep(0.1)
        
        oled.fill(0)
        oled.show()
        
        print("[Boot] Animación completada")
        
    except Exception as e:
        print(f"[Boot] Error en animación: {e}")
        # Fallback simple
        oled.fill(0)
        oled.text("SENSORACORE", 12, 20, 1)
        oled.text("Yamith.R", 36, 35, 1)
        oled.show()
        time.sleep(2)
        oled.fill(0)
        oled.show()

# Ejecutar animación de bienvenida
boot_animation()

print("[Boot] Sistema inicializado")
# Mensaje para cargar módulo
if oled_enabled and oled:
    oled.fill(0)
    oled.text("Ahora carga el", 8, 24, 1)
    oled.text("modulo a usar", 8, 34, 1)
    oled.show()
else:
    print("Ahora carga el modulo a usar")

