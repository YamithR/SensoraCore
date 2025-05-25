# main.py para ESP32 (MicroPython)
# Lee un potenciómetro y permite encender/apagar el LED integrado por WiFi
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
pot = ADC(Pin(32))  # GPIO 32 como se muestra en el diagrama
pot.atten(ADC.ATTN_11DB)
pot.width(ADC.WIDTH_12BIT)

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

while True:
    cl, addr = s.accept()
    print('Cliente conectado desde', addr)
    data = cl.recv(1024).decode()
    if 'GET_POT' in data:
        value = pot.read()
        cl.send(str(value))
    elif 'LED_ON' in data:
        led.value(1)
        cl.send('LED_ON_OK')
    elif 'LED_OFF' in data:
        led.value(0)
        cl.send('LED_OFF_OK')
    elif 'MODO:ANGULO_SIMPLE' in data:
        current_mode = 'ANGULO_SIMPLE'
        continuous_client = cl
        cl.send(b'ANGULO_SIMPLE_OK')
        angulo_simple_loop(cl)
        cl.close()
        current_mode = None
        continuous_client = None
        continue
    elif 'STOP' in data:
        current_mode = None
        cl.send(b'STOP_OK')
    else:
        cl.send('CMD_UNKNOWN')
    cl.close()
