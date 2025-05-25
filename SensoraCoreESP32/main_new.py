# main.py para ESP32 (MicroPython) - Versión con Brazo Ángulo
# Lee potenciómetros, sensor capacitivo y controla LED por WiFi
import network # type: ignore
import socket
from machine import Pin, ADC # type: ignore
import time

# Configuración WiFi (ajusta en wifi_config.py)
try:
    from wifi_config import SSID, PASSWORD
except ImportError:
    SSID = 'CanelaYMaya'
    PASSWORD = 'CanelayMayaEner0'

led = Pin(2, Pin.OUT)

# Configuración para Ángulo Simple
pot = ADC(Pin(32))  # GPIO 32 como se muestra en el diagrama
pot.atten(ADC.ATTN_11DB)
pot.width(ADC.WIDTH_12BIT)

# Configuración para Brazo Ángulo (3 potenciómetros + sensor capacitivo)
pot1 = ADC(Pin(32))  # Primer potenciómetro (base)
pot2 = ADC(Pin(33))  # Segundo potenciómetro (articulación 1)
pot3 = ADC(Pin(34))  # Tercer potenciómetro (articulación 2)
sensor_cap = Pin(25, Pin.IN, Pin.PULL_UP)  # Sensor capacitivo para agarre

# Configuración para sensores de distancia DIGITALES
# Sensor IR: GPIO digital en GPIO 35 (solo ON/OFF)
sensor_ir = Pin(35, Pin.IN, Pin.PULL_UP)  # Sensor infrarrojo digital

# Sensor Capacitivo de Distancia: GPIO digital en GPIO 36 (solo ON/OFF)
sensor_cap_dist = Pin(36, Pin.IN, Pin.PULL_UP)  # Sensor capacitivo digital

# Sensor Ultrasónico HC-SR04: Pines trigger y echo
trigger_pin = Pin(26, Pin.OUT)  # Pin trigger del HC-SR04
echo_pin = Pin(27, Pin.IN)      # Pin echo del HC-SR04

# Configurar ADCs para los potenciómetros del brazo
for pot_adc in [pot1, pot2, pot3]:
    pot_adc.atten(ADC.ATTN_11DB)
    pot_adc.width(ADC.WIDTH_12BIT)

# Variables globales para el modo continuo
current_mode = None
continuous_client = None

# Conexión WiFi
sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.connect(SSID, PASSWORD)
while not sta.isconnected():
    time.sleep(0.5)

print(f'WiFi conectado. IP: {sta.ifconfig()[0]}')

# Servidor simple para recibir comandos y enviar datos
addr = socket.getaddrinfo('0.0.0.0', 8080)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)

def angulo_simple_loop(client):
    global current_mode, continuous_client
    try:
        while current_mode == 'ANGULO_SIMPLE' and continuous_client == client:
            lectura = pot.read()
            # Mapea de 0-4095 a 0-270 grados (rango típico de potenciómetro)
            angulo = int((lectura * 270) / 4095)
            msg = f"POT:{lectura},ANG:{angulo}\n"
            try:
                client.send(msg.encode())
            except:
                break
            time.sleep(0.1)
    except Exception as e:
        print(f"Error en angulo_simple_loop: {e}")
        pass

def brazo_angulo_loop(client):
    global current_mode, continuous_client
    try:
        while current_mode == 'BRAZO_ANGULO' and continuous_client == client:
            # Leer los 3 potenciómetros
            lectura1 = pot1.read()
            lectura2 = pot2.read() 
            lectura3 = pot3.read()
            
            # Mapear de 0-4095 a -135 a +135 grados (como en Arduino)
            angulo1 = int(((lectura1 * 270) / 4095) - 135)
            angulo2 = int(((lectura2 * 270) / 4095) - 135)
            angulo3 = int(((lectura3 * 270) / 4095) - 135)
            
            # Leer sensor capacitivo (invertido por pull-up)
            sensor_estado = not sensor_cap.value()  # Invertir porque usa pull-up
            
            msg = f"POT1:{lectura1},ANG1:{angulo1},POT2:{lectura2},ANG2:{angulo2},POT3:{lectura3},ANG3:{angulo3},SENSOR:{sensor_estado}\n"
            try:
                client.send(msg.encode())
            except:
                break
            time.sleep(0.1)
    except Exception as e:
        print(f"Error en brazo_angulo_loop: {e}")
        pass

def distancia_ir_loop(client):
    global current_mode, continuous_client
    try:
        while current_mode == 'DISTANCIA_IR' and continuous_client == client:
            # Leer sensor IR digital (solo ON/OFF)
            sensor_detectado = not sensor_ir.value()  # Invertir por pull-up
            
            # Enviar estado digital simple
            msg = f"IR_DIGITAL:{sensor_detectado}\n"
            try:
                client.send(msg.encode())
            except:
                break
            time.sleep(0.1)
    except Exception as e:
        print(f"Error en distancia_ir_loop: {e}")
        pass

def distancia_cap_loop(client):
    global current_mode, continuous_client
    try:
        while current_mode == 'DISTANCIA_CAP' and continuous_client == client:
            # Leer sensor capacitivo digital (solo ON/OFF)
            sensor_detectado = not sensor_cap_dist.value()  # Invertir por pull-up
            
            # Enviar estado digital simple
            msg = f"CAP_DIGITAL:{sensor_detectado}\n"
            try:
                client.send(msg.encode())
            except:
                break
            time.sleep(0.1)
    except Exception as e:
        print(f"Error en distancia_cap_loop: {e}")
        pass

def distancia_ultrasonico_loop(client):
    global current_mode, continuous_client
    try:
        while current_mode == 'DISTANCIA_ULTRA' and continuous_client == client:
            # Medir distancia con HC-SR04
            trigger_pin.off()
            time.sleep_us(2)
            trigger_pin.on()
            time.sleep_us(10)
            trigger_pin.off()
            
            # Medir tiempo de echo
            start_time = time.ticks_us()
            timeout_start = start_time
            
            # Esperar que echo se active
            while echo_pin.value() == 0:
                start_time = time.ticks_us()
                if time.ticks_diff(start_time, timeout_start) > 30000:  # Timeout 30ms
                    break
            
            # Esperar que echo se desactive
            end_time = start_time
            while echo_pin.value() == 1:
                end_time = time.ticks_us()
                if time.ticks_diff(end_time, start_time) > 30000:  # Timeout 30ms
                    break
            
            # Calcular distancia
            duration = time.ticks_diff(end_time, start_time)
            if duration > 0:
                distancia_cm = (duration * 0.034) / 2  # Velocidad del sonido
                distancia_cm = max(2, min(400, distancia_cm))  # Límites del HC-SR04
            else:
                distancia_cm = 400  # Fuera de rango
            
            # Simular ADC y voltaje para compatibilidad con gráficas
            # Mapear distancia a rango ADC simulado (2-400cm -> 0-4095)
            adc_simulado = int((distancia_cm - 2) * 4095 / 398)
            voltaje_simulado = (adc_simulado * 3.3) / 4095
            
            msg = f"ULTRA_ADC:{adc_simulado},ULTRA_V:{voltaje_simulado:.2f},ULTRA_CM:{distancia_cm:.1f}\n"
            try:
                client.send(msg.encode())
            except:
                break
            time.sleep(0.1)
    except Exception as e:
        print(f"Error en distancia_ultrasonico_loop: {e}")
        pass

# Bucle principal del servidor
print("Servidor iniciado, esperando conexiones...")
while True:
    cl, addr = s.accept()
    print('Cliente conectado desde', addr)
    data = cl.recv(1024).decode()
    
    if 'GET_POT' in data:
        value = pot.read()
        cl.send(str(value).encode())
    elif 'LED_ON' in data:
        led.value(1)
        cl.send(b'LED_ON_OK')
    elif 'LED_OFF' in data:
        led.value(0)
        cl.send(b'LED_OFF_OK')
    elif 'MODO:ANGULO_SIMPLE' in data:
        current_mode = 'ANGULO_SIMPLE'
        continuous_client = cl
        cl.send(b'ANGULO_SIMPLE_OK')
        angulo_simple_loop(cl)
        cl.close()
        current_mode = None
        continuous_client = None
        continue
    elif 'MODO:BRAZO_ANGULO' in data:
        current_mode = 'BRAZO_ANGULO'
        continuous_client = cl
        cl.send(b'BRAZO_ANGULO_OK')
        brazo_angulo_loop(cl)
        cl.close()
        current_mode = None
        continuous_client = None
        continue
    elif 'MODO:DISTANCIA_IR' in data:
        current_mode = 'DISTANCIA_IR'
        continuous_client = cl
        cl.send(b'DISTANCIA_IR_OK')
        distancia_ir_loop(cl)
        cl.close()
        current_mode = None
        continuous_client = None
        continue
    elif 'MODO:DISTANCIA_CAP' in data:
        current_mode = 'DISTANCIA_CAP'
        continuous_client = cl
        cl.send(b'DISTANCIA_CAP_OK')
        distancia_cap_loop(cl)
        cl.close()
        current_mode = None
        continuous_client = None
        continue
    elif 'MODO:DISTANCIA_ULTRA' in data:
        current_mode = 'DISTANCIA_ULTRA'
        continuous_client = cl
        cl.send(b'DISTANCIA_ULTRA_OK')
        distancia_ultrasonico_loop(cl)
        cl.close()
        current_mode = None
        continuous_client = None
        continue
    elif 'STOP' in data:
        current_mode = None
        cl.send(b'STOP_OK')
    else:
        cl.send(b'CMD_UNKNOWN')
    
    cl.close()
