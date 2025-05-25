# main.py para ESP32 (MicroPython) - Versión con Brazo Ángulo
# Lee potenciómetros, sensor capacitivo y controla LED por WiFi
import network
import socket
from machine import Pin, ADC
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

# Configurar ADCs para los potenciómetros del brazo
for pot_adc in [pot1, pot2, pot3]:
    pot_adc.atten(ADC.ATTN_11DB)
    pot_adc.width(ADC.WIDTH_12BIT)

# Conexión WiFi
sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.connect(SSID, PASSWORD)
while not sta.isconnected():
    time.sleep(0.5)

# Servidor simple para recibir comandos y enviar datos
addr = socket.getaddrinfo('0.0.0.0', 8080)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)

print('ESP32 listo en', sta.ifconfig())

# Estados de modo
current_mode = None
continuous_client = None

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

# Bucle principal del servidor
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
    elif 'STOP' in data:
        current_mode = None
        cl.send(b'STOP_OK')
    else:
        cl.send(b'CMD_UNKNOWN')
    
    cl.close()
