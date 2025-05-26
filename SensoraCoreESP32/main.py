# main.py para ESP32 (MicroPython) - SensoraCore Alpha 0.2
# Sistema unificado con interfaces digital/analógica
# Sensores: Potenciómetro, IR Digital, Capacitivo Digital, Ultrasónico Analógico
import network # type: ignore
import socket
from machine import Pin, ADC, reset # type: ignore
import time

# Esperar a que el ESP32 se inicialice completamente
print("Iniciando SensoraCore ESP32...")
time.sleep(2)

# Configuración WiFi (ajusta en wifi_config.py)
try:
    from wifi_config import SSID, PASSWORD
except ImportError:
    # Si no existe wifi_config.py, usa estos valores predeterminados
    SSID = 'NombreDeTuRed'
    PASSWORD = 'ContraseñaDeTuRed'

# Configuración del LED integrado (GPIO 2)
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
# Sensor IR: GPIO digital en GPIO 14 (solo ON/OFF)
sensor_ir = Pin(14, Pin.IN, Pin.PULL_UP)  # Sensor infrarrojo digital

# Sensor Capacitivo de Distancia: GPIO digital en GPIO 35 (solo ON/OFF)
sensor_cap_dist = Pin(35, Pin.IN, Pin.PULL_UP)  # Sensor capacitivo digital

# Sensor Ultrasónico HC-SR04: Pines trigger y echo
trigger_pin = Pin(26, Pin.OUT)   # Pin trigger del HC-SR04
echo_pin = Pin(27, Pin.IN)       # Pin echo del HC-SR04

# Configurar ADCs para los potenciómetros del brazo
for pot_adc in [pot1, pot2, pot3]:
    pot_adc.atten(ADC.ATTN_11DB)
    pot_adc.width(ADC.WIDTH_12BIT)

# Variables globales para el modo continuo
current_mode = None
continuous_client = None

# Función para conectar WiFi con manejo de errores
def connect_wifi():
    print("Iniciando conexión WiFi...")
    sta = network.WLAN(network.STA_IF)
    
    # Desactivar y reactivar WiFi para limpiar estado
    sta.active(False)
    time.sleep(1)
    sta.active(True)
    
    # Intentar conexión con reintentos
    max_attempts = 5
    attempt = 1
    
    while attempt <= max_attempts:
        try:
            print(f"Intento {attempt}/{max_attempts}: Conectando a '{SSID}'...")
            
            # Verificar si ya está conectado
            if sta.isconnected():
                print(f'WiFi ya conectado. IP: {sta.ifconfig()[0]}')
                return sta
            
            # Conectar a la red
            sta.connect(SSID, PASSWORD)
            
            # Esperar conexión con timeout
            timeout = 15  # 15 segundos timeout
            start_time = time.time()
            
            while not sta.isconnected() and (time.time() - start_time) < timeout:
                time.sleep(0.5)
                led.value(not led.value())  # Parpadear LED durante conexión
            
            if sta.isconnected():
                led.value(0)  # Apagar LED
                ip = sta.ifconfig()[0]
                print(f'WiFi conectado exitosamente!')
                print(f'IP: {ip}')
                print(f'Máscara: {sta.ifconfig()[1]}')
                print(f'Gateway: {sta.ifconfig()[2]}')
                print(f'DNS: {sta.ifconfig()[3]}')
                return sta
            else:
                print(f"Timeout en intento {attempt}")
                
        except OSError as e:
            print(f"Error OSError en intento {attempt}: {e}")
        except Exception as e:
            print(f"Error desconocido en intento {attempt}: {e}")
        
        attempt += 1
        if attempt <= max_attempts:
            print("Esperando antes del siguiente intento...")
            time.sleep(2)
    
    print("ERROR: No se pudo conectar al WiFi después de todos los intentos")
    print("Verifique:")
    print("1. Nombre de red (SSID) correcto")
    print("2. Contraseña correcta") 
    print("3. Red WiFi disponible")
    print("4. ESP32 dentro del rango de la red")
    return None

# Conectar WiFi
sta = connect_wifi()
if not sta:
    print("FALLO CRÍTICO: Sin conexión WiFi - Reiniciando...")
    reset()

# Servidor simple para recibir comandos y enviar datos
def create_server():
    try:
        addr = socket.getaddrinfo('0.0.0.0', 8080)[0][-1]
        s = socket.socket()
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Reutilizar dirección
        s.bind(addr)
        s.listen(1)
        print(f"Servidor iniciado en puerto 8080")
        print(f"IP del servidor: {sta.ifconfig()[0]}:8080")
        return s
    except Exception as e:
        print(f"Error creando servidor: {e}")
        return None

s = create_server()
if not s:
    print("FALLO CRÍTICO: No se pudo crear el servidor - Reiniciando...")
    reset()

def angulo_simple_loop(client):
    global current_mode, continuous_client
    try:
        while current_mode == 'ANGULO_SIMPLE' and continuous_client == client:
            lectura = pot.read()
            # Mapear de 0-4095 a -135 a +135 grados
            angulo = int(((lectura * 270) / 4095) - 135)
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
    try:
        cl, addr = s.accept()
        print('Cliente conectado desde', addr)
        
        # Configurar timeout para el socket del cliente
        cl.settimeout(30)  # 30 segundos timeout
        
        data = cl.recv(1024).decode()
        print(f"Comando recibido: {data.strip()}")
        
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
        
    except OSError as e:
        print(f"Error de red: {e}")
        try:
            cl.close()
        except:
            pass
        # Verificar conexión WiFi
        if not sta.isconnected():
            print("Conexión WiFi perdida - Intentando reconectar...")
            sta = connect_wifi()
            if not sta:
                print("No se pudo reconectar - Reiniciando...")
                reset()
    except Exception as e:
        print(f"Error inesperado: {e}")
        try:
            cl.close()
        except:
            pass
