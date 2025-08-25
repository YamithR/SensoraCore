# main.py para ESP32 (MicroPython) - SensoraCore Alpha 0.2
# Sistema unificado con interfaces digital/analógica
# Sensores: Potenciómetro, IR Digital, Capacitivo Digital, Ultrasónico Analógico
import network # type: ignore
import socket
from machine import Pin, ADC, reset, PWM, SoftSPI # type: ignore
import time

# Esperar a que el ESP32 se inicialice completamente
print("Iniciando SensoraCore ESP32...")
time.sleep(2)

# Configuración WiFi (ajusta en wifi_config.py)
SSID = 'CanelaYMaya'
PASSWORD = 'CanelayMayaEner0'


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
                print(f"Enviado: POT:{lectura},ANG:{angulo}")  # Debug
            except:
                break
            time.sleep(0.5)  # Muestreo cada 0.5 segundos
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
                distancia_cm = max(2, min(200, distancia_cm))  # Límites del HC-SR04
            else:
                distancia_cm = 200  # Fuera de rango
            
            # Enviar solo la distancia real (sin datos simulados falsos)
            msg = f"ULTRA_CM:{distancia_cm:.1f}\n"
            try:
                client.send(msg.encode())
            except:
                break
            time.sleep(0.1)
    except Exception as e:
        print(f"Error en distancia_ultrasonico_loop: {e}")
        pass

# ------ OPTICAL SPEED (encoders + control de velocidad) ------
# Nota: GPIO36 es solo entrada; evitamos usarlo como salida aunque aparezca en el diagrama.
# Encoders (entrada):
enc_l = Pin(39, Pin.IN)  # Izquierdo
enc_r = Pin(34, Pin.IN)  # Derecho

"""
Configuración L298N (aclaración):
- IN1..IN4 son pines de ENTRADA del driver; del lado del ESP32 todos son SALIDAS.
- Usamos 4 GPIOs PWM-capaces para controlar ambos motores en ambos sentidos.
- Mapeo (ESP32 → L298N):
    IN1 ← GPIO25 (motor izquierdo, forward)
    IN2 ← GPIO26 (motor izquierdo, reverse)
    IN3 ← GPIO32 (motor derecho, forward)
    IN4 ← GPIO33 (motor derecho, reverse)
"""
# PWM en los 4 canales del L298N
in1_pwm = PWM(Pin(25))   # IN1 (L fwd)
in2_pwm = PWM(Pin(26))   # IN2 (L rev)
in3_pwm = PWM(Pin(32))   # IN3 (R fwd)
in4_pwm = PWM(Pin(33))   # IN4 (R rev)

for p in (in1_pwm, in2_pwm, in3_pwm, in4_pwm):
        try:
                p.freq(1000)
        except Exception:
                pass

def _pwm_set(pwm_obj, percent):
    try:
        # MicroPython duty_u16 en 0..65535
        pwm_obj.duty_u16(int(max(0, min(100, percent)) * 65535 / 100))
    except Exception:
        # Fallback a duty 0..1023
        pwm_obj.duty(int(max(0, min(100, percent)) * 1023 / 100))

_speed_percent = 0  # -100..100
_ppr = 20  # Pulsos por revolución (ajustable si se desea)
_cnt_l = 0
_cnt_r = 0

def _irq_l(pin):
    global _cnt_l
    _cnt_l += 1

def _irq_r(pin):
    global _cnt_r
    _cnt_r += 1

enc_l.irq(trigger=Pin.IRQ_RISING, handler=_irq_l)
enc_r.irq(trigger=Pin.IRQ_RISING, handler=_irq_r)

def _apply_speed(percent):
    global _speed_percent
    # Clamp -100..100
    val = int(percent)
    if val > 100:
        val = 100
    if val < -100:
        val = -100
    _speed_percent = val

    spd = abs(val)
    # Motor izquierdo (IN1/IN2)
    if val >= 0:
        _pwm_set(in1_pwm, spd)
        _pwm_set(in2_pwm, 0)
    else:
        _pwm_set(in1_pwm, 0)
        _pwm_set(in2_pwm, spd)

    # Motor derecho (IN3/IN4)
    if val >= 0:
        _pwm_set(in3_pwm, spd)
        _pwm_set(in4_pwm, 0)
    else:
        _pwm_set(in3_pwm, 0)
        _pwm_set(in4_pwm, spd)

def optical_speed_loop(client):
    global current_mode, continuous_client, _cnt_l, _cnt_r
    _apply_speed(_speed_percent)
    last_l = _cnt_l
    last_r = _cnt_r
    last_t = time.ticks_ms()
    try:
        while current_mode == 'OPTICAL_SPEED' and continuous_client == client:
            # Procesar comandos no bloqueantes si llegan
            client.settimeout(0.01)
            try:
                cmd = client.recv(64)
                if cmd:
                    txt = cmd.decode().strip()
                    if txt.startswith('SET_SPEED:'):
                        try:
                            val = int(txt.split(':',1)[1])
                            _apply_speed(val)
                        except Exception:
                            pass
                    elif txt.startswith('SET_PPR:'):
                        try:
                            val = int(txt.split(':',1)[1])
                            if val > 0:
                                global _ppr
                                _ppr = val
                        except Exception:
                            pass
                    elif 'STOP' in txt:
                        break
            except Exception:
                pass

            # Ventana de cálculo ~200ms
            now = time.ticks_ms()
            if time.ticks_diff(now, last_t) >= 200:
                dl = _cnt_l - last_l
                dr = _cnt_r - last_r
                dt = time.ticks_diff(now, last_t) / 1000.0
                last_l = _cnt_l
                last_r = _cnt_r
                last_t = now
                try:
                    rpm_l = (dl / dt) * (60.0 / _ppr) if dt > 0 and _ppr > 0 else 0.0
                    rpm_r = (dr / dt) * (60.0 / _ppr) if dt > 0 and _ppr > 0 else 0.0
                except Exception:
                    rpm_l = 0.0
                    rpm_r = 0.0
                msg = f"RPM_L:{rpm_l:.1f},RPM_R:{rpm_r:.1f},SPEED:{_speed_percent}\n"
                try:
                    client.send(msg.encode())
                except Exception:
                    break
            time.sleep(0.01)
    except Exception as e:
        print(f"Error en optical_speed_loop: {e}")
    finally:
        _apply_speed(0)

# ------ IR STEERING (5 sensores IR + PID + control de 2 motores) ------
# Pines de los 5 sensores IR (ajustar según hardware si es necesario)
# Elegidos para evitar conflicto con PWM (25/26/32/33) y ultrasónico (26/27)
ir_pins = [Pin(4, Pin.IN, Pin.PULL_UP),   # más a la izquierda
           Pin(16, Pin.IN, Pin.PULL_UP),
           Pin(17, Pin.IN, Pin.PULL_UP),
           Pin(18, Pin.IN, Pin.PULL_UP),
           Pin(19, Pin.IN, Pin.PULL_UP)]  # más a la derecha

# Parámetros PID y velocidad base
_kp, _ki, _kd = 1.0, 0.0, 0.5
_base_speed = 40  # -100..100, signo define sentido
_err_int = 0.0
_last_err = 0.0

def _read_ir_bits():
    # Lectura con pull-ups: línea negra usualmente baja el pin (0)
    # Normalizamos a 1 = detecta línea, 0 = blanco
    bits = ''
    for p in ir_pins:
        v = 1 if (not p.value()) else 0
        bits += '1' if v else '0'
    return bits  # 5 caracteres de izquierda a derecha

def _error_from_bits(bits: str) -> float:
    # Mapear posiciones a errores: L2=-2, L1=-1, C=0, R1=+1, R2=+2 (promedio ponderado)
    weights = [-2, -1, 0, 1, 2]
    num = 0.0
    den = 0.0
    for i, ch in enumerate(bits[:5]):
        if ch == '1':
            num += weights[i]
            den += 1.0
    if den == 0:
        return 0.0  # línea perdida → error 0 (se puede mejorar con última dirección)
    return num / den

def _motor_mix_from_err(base: int, err: float, dt: float):
    global _err_int, _last_err
    # PID
    _err_int += err * dt
    der = (err - _last_err) / dt if dt > 0 else 0.0
    _last_err = err
    corr = _kp * err + _ki * _err_int + _kd * der
    # Mezcla diferencial: motor izquierdo disminuye con corr positiva y viceversa
    left = max(-100, min(100, int(base - corr * 30)))
    right = max(-100, min(100, int(base + corr * 30)))
    return left, right

def _apply_dual(left: int, right: int):
    # Usa los mismos 4 PWMs (in1..in4, in3..in4) para cada lado por separado
    # Izquierdo
    if left >= 0:
        _pwm_set(in1_pwm, abs(left))
        _pwm_set(in2_pwm, 0)
    else:
        _pwm_set(in1_pwm, 0)
        _pwm_set(in2_pwm, abs(left))
    # Derecho
    if right >= 0:
        _pwm_set(in3_pwm, abs(right))
        _pwm_set(in4_pwm, 0)
    else:
        _pwm_set(in3_pwm, 0)
        _pwm_set(in4_pwm, abs(right))

def ir_steering_loop(client):
    global current_mode, continuous_client, _base_speed, _cnt_l, _cnt_r
    last_t = time.ticks_ms()
    last_l = _cnt_l
    last_r = _cnt_r
    rpm_l = 0.0
    rpm_r = 0.0
    try:
        while current_mode == 'IR_STEERING' and continuous_client == client:
            # Recibir comandos no bloqueantes
            client.settimeout(0.005)
            try:
                cmd = client.recv(64)
                if cmd:
                    txt = cmd.decode().strip()
                    if txt.startswith('SET_BASE:'):
                        try:
                            _base_speed = int(txt.split(':',1)[1])
                            if _base_speed > 100:
                                _base_speed = 100
                            if _base_speed < -100:
                                _base_speed = -100
                        except Exception:
                            pass
                    elif txt.startswith('SET_PID:'):
                        try:
                            vals = txt.split(':',1)[1]
                            parts = vals.split(',')
                            d = {}
                            for p in parts:
                                if '=' in p:
                                    k,v = p.split('=',1)
                                    d[k.strip().lower()] = float(v)
                            global _kp, _ki, _kd
                            _kp = float(d.get('kp', _kp))
                            _ki = float(d.get('ki', _ki))
                            _kd = float(d.get('kd', _kd))
                        except Exception:
                            pass
                    elif 'STOP' in txt:
                        break
            except Exception:
                pass

            now = time.ticks_ms()
            dt = time.ticks_diff(now, last_t) / 1000.0
            if dt <= 0:
                dt = 0.01
            last_t = now

            bits = _read_ir_bits()
            err = _error_from_bits(bits)
            l, r = _motor_mix_from_err(_base_speed, err, dt)
            _apply_dual(l, r)
            # Estado
            # Calcular RPMs del mismo contador de encoders (ventana ~200ms)
            now2 = time.ticks_ms()
            if time.ticks_diff(now2, last_t) >= 200:
                dl = _cnt_l - last_l
                dr = _cnt_r - last_r
                dt2 = time.ticks_diff(now2, last_t) / 1000.0
                last_l = _cnt_l
                last_r = _cnt_r
                if dt2 > 0 and _ppr > 0:
                    rpm_l = (dl / dt2) * (60.0 / _ppr)
                    rpm_r = (dr / dt2) * (60.0 / _ppr)
                last_t = now2
            msg = f"SENS:{bits},ERR:{err:.2f},OUT_L:{l},OUT_R:{r},SPEED:{_base_speed},RPM_L:{rpm_l:.1f},RPM_R:{rpm_r:.1f}\n"
            try:
                client.send(msg.encode())
            except Exception:
                break
            time.sleep(0.02)
    except Exception as e:
        print(f"Error en ir_steering_loop: {e}")
    finally:
        _apply_dual(0, 0)

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
        elif 'MODO:OPTICAL_SPEED' in data:
            current_mode = 'OPTICAL_SPEED'
            continuous_client = cl
            cl.send(b'OPTICAL_SPEED_OK')
            optical_speed_loop(cl)
            cl.close()
            current_mode = None
            continuous_client = None
            continue
        elif 'MODO:IR_STEERING' in data:
            current_mode = 'IR_STEERING'
            continuous_client = cl
            cl.send(b'IR_STEERING_OK')
            ir_steering_loop(cl)
            cl.close()
            current_mode = None
            continuous_client = None
            continue
        elif 'MODO:THERMOREGULATION' in data:
            # --- THERMOREGULATION MODE ---
            current_mode = 'THERMOREGULATION'
            continuous_client = cl
            cl.send(b'THERMOREGULATION_OK')

            # Config sensores
            # LM35 en ADC GPIO36 (VP)
            try:
                lm35_adc = ADC(Pin(36))
                lm35_adc.atten(ADC.ATTN_11DB)
                lm35_adc.width(ADC.WIDTH_12BIT)
            except Exception:
                lm35_adc = None

            # DS18B20 en GPIO27 (OneWire) - evitar conflicto con CS=33 del MAX6675
            onewire = None
            ds_sensor = None
            try:
                import onewire, ds18x20  # type: ignore
                ow_pin = Pin(27)
                onewire = onewire.OneWire(ow_pin)
                ds_sensor = ds18x20.DS18X20(onewire)
                roms = ds_sensor.scan()
                if not roms:
                    ds_sensor = None
                else:
                    ds_rom = roms[0]
            except Exception:
                ds_sensor = None
                ds_rom = None

            # MAX6675 via SoftSPI: SCK=32, MISO=35, CS=33, MOSI dummy=25
            spi = None
            cs = None
            try:
                spi = SoftSPI(baudrate=5000000, polarity=0, phase=0, sck=Pin(32), mosi=Pin(25), miso=Pin(35))
                cs = Pin(33, Pin.OUT)
                cs.value(1)
            except Exception:
                spi = None
                cs = None

            sel = 'LM35'
            period_ms = 500
            last_read = 0

            def read_lm35_c():
                if lm35_adc is None:
                    return 0.0, None
                # ADC 12-bit 0..4095, ATTN_11DB => ~3.3V full scale
                raw = lm35_adc.read()
                v = (raw / 4095.0) * 3.3
                temp_c = (v * 100.0)  # 10mV/°C
                return temp_c, raw

            def read_ds18b20_c():
                if ds_sensor is None:
                    return 0.0
                try:
                    ds_sensor.convert_temp()
                    time.sleep_ms(800)  # resolución típica
                    return ds_sensor.read_temp(ds_rom)
                except Exception:
                    return 0.0

            def read_max6675_c():
                if spi is None or cs is None:
                    return 0.0, None
                try:
                    cs.value(0)
                    data = spi.read(2)
                    cs.value(1)
                    if not data or len(data) < 2:
                        return 0.0, None
                    val = (data[0] << 8) | data[1]
                    # bit D2 (0x04) = 1 => no thermocouple connected
                    if val & 0x04:
                        return 0.0, val
                    # bits 15..3 => temp * 0.25°C
                    temp = (val >> 3) * 0.25
                    return float(temp), val
                except Exception:
                    return 0.0, None

            # Loop principal Thermo
            try:
                cl.settimeout(0.01)
                while current_mode == 'THERMOREGULATION' and continuous_client == cl:
                    # comandos no bloqueantes
                    try:
                        cmd = cl.recv(64)
                        if cmd:
                            txt = cmd.decode().strip()
                            if txt.startswith('TH_SET:'):
                                sel = txt.split(':',1)[1].strip().upper()
                                if sel not in ('LM35','DS18B20','TYPEK'):
                                    sel = 'LM35'
                            elif txt.startswith('TH_START:'):
                                try:
                                    p = int(txt.split(':',1)[1])
                                    if sel == 'DS18B20':
                                        period_ms = max(800, p)
                                    else:
                                        period_ms = max(200, p)
                                except Exception:
                                    pass
                            elif 'TH_STOP' in txt or 'STOP' in txt:
                                break
                    except Exception:
                        pass

                    now = time.ticks_ms()
                    if time.ticks_diff(now, last_read) >= period_ms:
                        last_read = now
                        if sel == 'LM35':
                            temp, raw = read_lm35_c()
                            msg = f"SENSOR:LM35,TEMP_C:{temp:.2f},RAW:{raw}\n"
                        elif sel == 'DS18B20':
                            temp = read_ds18b20_c()
                            msg = f"SENSOR:DS18B20,TEMP_C:{temp:.2f}\n"
                        else:  # TYPEK
                            temp, raw = read_max6675_c()
                            msg = f"SENSOR:TYPEK,TEMP_C:{temp:.2f},RAW:{raw}\n"
                        try:
                            cl.send(msg.encode())
                        except Exception:
                            break
                    time.sleep_ms(5)
            except Exception as e:
                print(f"Error en THERMOREGULATION: {e}")
            finally:
                # fin de modo
                cl.close()
                current_mode = None
                continuous_client = None
                continue
        elif 'MODO:BRIGHTNESS' in data:
            # --- BRIGHTNESS MODE ---
            current_mode = 'BRIGHTNESS'
            continuous_client = cl
            cl.send(b'BRIGHTNESS_OK')

            # ADC en GPIO34 para LDR
            try:
                adc_ldr = ADC(Pin(34))
                adc_ldr.atten(ADC.ATTN_11DB)
                adc_ldr.width(ADC.WIDTH_12BIT)
            except Exception:
                adc_ldr = None

            period_ms = 200
            last_read = 0
            try:
                cl.settimeout(0.01)
                while current_mode == 'BRIGHTNESS' and continuous_client == cl:
                    # comandos
                    try:
                        cmd = cl.recv(64)
                        if cmd:
                            txt = cmd.decode().strip()
                            if txt.startswith('BR_START:'):
                                try:
                                    p = int(float(txt.split(':',1)[1]))
                                    period_ms = max(50, p)
                                    cl.send(b'OK')
                                except Exception:
                                    cl.send(b'ERR')
                            elif 'BR_STOP' in txt or 'STOP' in txt:
                                cl.send(b'OK')
                                break
                    except Exception:
                        pass

                    now = time.ticks_ms()
                    if time.ticks_diff(now, last_read) >= period_ms:
                        last_read = now
                        try:
                            val = adc_ldr.read() if adc_ldr else 0
                        except Exception:
                            val = 0
                        volt = (val / 4095.0) * 3.3
                        msg = f"SENSOR:LDR,ADC:{val},VOLT:{volt:.3f}\n"
                        try:
                            cl.send(msg.encode())
                        except Exception:
                            break
                    time.sleep_ms(5)
            except Exception as e:
                print(f"Error en BRIGHTNESS: {e}")
            finally:
                cl.close()
                current_mode = None
                continuous_client = None
                continue
        elif 'MODO:COLOR_CNY' in data:
            # --- COLOR CNY MODE ---
            current_mode = 'COLOR_CNY'
            continuous_client = cl
            cl.send(b'COLOR_CNY_OK')

            # ADC en GPIO35 para CNY70 (ADC1)
            try:
                adc_cny = ADC(Pin(35))
                adc_cny.atten(ADC.ATTN_11DB)
                adc_cny.width(ADC.WIDTH_12BIT)
            except Exception:
                adc_cny = None

            period_ms = 200
            last_read = 0
            try:
                cl.settimeout(0.01)
                while current_mode == 'COLOR_CNY' and continuous_client == cl:
                    # comandos
                    try:
                        cmd = cl.recv(64)
                        if cmd:
                            txt = cmd.decode().strip()
                            if txt.startswith('CNY_START:'):
                                try:
                                    p = int(float(txt.split(':',1)[1]))
                                    period_ms = max(50, p)
                                    cl.send(b'OK')
                                except Exception:
                                    cl.send(b'ERR')
                            elif 'CNY_STOP' in txt or 'STOP' in txt:
                                cl.send(b'OK')
                                break
                    except Exception:
                        pass

                    now = time.ticks_ms()
                    if time.ticks_diff(now, last_read) >= period_ms:
                        last_read = now
                        try:
                            val = adc_cny.read() if adc_cny else 0
                        except Exception:
                            val = 0
                        volt = (val / 4095.0) * 3.3
                        msg = f"SENSOR:CNY70,ADC:{val},VOLT:{volt:.3f}\n"
                        try:
                            cl.send(msg.encode())
                        except Exception:
                            break
                    time.sleep_ms(5)
            except Exception as e:
                print(f"Error en COLOR_CNY: {e}")
            finally:
                cl.close()
                current_mode = None
                continuous_client = None
                continue
        elif 'MODO:GAS_REGULATION' in data:
            # --- GAS REGULATION MODE ---
            current_mode = 'GAS_REGULATION'
            continuous_client = cl
            cl.send(b'GAS_REGULATION_OK')

            # Preparar ADCs: MQ2 en GPIO36 (VP), MQ3 en GPIO39
            mq2_adc = None
            mq3_adc = None
            enc39_irq_disabled = False
            try:
                try:
                    mq2_adc = ADC(Pin(36))
                    mq2_adc.atten(ADC.ATTN_11DB)
                    mq2_adc.width(ADC.WIDTH_12BIT)
                except Exception:
                    mq2_adc = None
                # Desactivar IRQ del encoder en 39 durante este modo para evitar conflictos
                try:
                    enc_l.irq(handler=None)
                    enc39_irq_disabled = True
                except Exception:
                    pass
                try:
                    mq3_adc = ADC(Pin(39))
                    mq3_adc.atten(ADC.ATTN_11DB)
                    mq3_adc.width(ADC.WIDTH_12BIT)
                except Exception:
                    mq3_adc = None
            except Exception:
                pass

            sel = 'MQ2'
            period_ms = 500
            last_read = 0

            def read_adc_v(adc_obj):
                if adc_obj is None:
                    return 0, 0.0
                try:
                    val = adc_obj.read()
                    volt = (val / 4095.0) * 3.3
                    return val, volt
                except Exception:
                    return 0, 0.0

            try:
                cl.settimeout(0.01)
                while current_mode == 'GAS_REGULATION' and continuous_client == cl:
                    # comandos no bloqueantes
                    try:
                        cmd = cl.recv(64)
                        if cmd:
                            txt = cmd.decode().strip()
                            if txt.startswith('GR_SET:'):
                                sensor_cmd = txt.split(':',1)[1].strip().upper()
                                if sensor_cmd in ('MQ2','MQ3'):
                                    sel = sensor_cmd
                            elif txt.startswith('GR_START:'):
                                try:
                                    p = int(txt.split(':',1)[1])
                                    period_ms = max(100, p)
                                except Exception:
                                    pass
                            elif 'GR_STOP' in txt or 'STOP' in txt:
                                break
                    except Exception:
                        pass

                    now = time.ticks_ms()
                    if time.ticks_diff(now, last_read) >= period_ms:
                        last_read = now
                        if sel == 'MQ2':
                            adc, volt = read_adc_v(mq2_adc)
                            msg = f"SENSOR:MQ2,ADC:{adc},VOLT:{volt:.3f}\n"
                        else:
                            adc, volt = read_adc_v(mq3_adc)
                            msg = f"SENSOR:MQ3,ADC:{adc},VOLT:{volt:.3f}\n"
                        try:
                            cl.send(msg.encode())
                        except Exception:
                            break
                    time.sleep_ms(5)
            except Exception as e:
                print(f"Error en GAS_REGULATION: {e}")
            finally:
                # Restaurar IRQ del encoder en 39 si se desactivó
                try:
                    if enc39_irq_disabled:
                        enc_l.irq(trigger=Pin.IRQ_RISING, handler=_irq_l)
                except Exception:
                    pass
                cl.close()
                current_mode = None
                continuous_client = None
                continue
        elif 'MODO:COLOR_TCS' in data:
            # --- COLOR TCS (TCS3200) MODE ---
            current_mode = 'COLOR_TCS'
            continuous_client = cl
            cl.send(b'COLOR_TCS_OK')

            # Pines del TCS3200 según diagrama de la UI:
            # S0 -> GPIO36, S1 -> GPIO39, S2 -> GPIO34, S3 -> GPIO35, OUT -> GPIO32
            # Nota: en ESP32, 36/39 son solo entrada analógica; como digitales pueden limitarse.
            # Para robustez usamos S2=34, S3=35 como salidas; y OUT=32 como entrada para contar pulsos.
            # Si su módulo cablea S0/S1, puede omitirse o fijarse a división por hardware (ej. 20%).
            try:
                s2 = Pin(34, Pin.OUT)
                s3 = Pin(35, Pin.OUT)
            except Exception:
                s2 = None
                s3 = None
            try:
                out_pin = Pin(32, Pin.IN)
            except Exception:
                out_pin = None

            # Contador simple por interrupciones (mutable para cierre)
            _pulse_cnt = [0]
            def _irq_out(pin):
                try:
                    _pulse_cnt[0] += 1
                except Exception:
                    pass
            try:
                if out_pin:
                    out_pin.irq(trigger=Pin.IRQ_RISING, handler=_irq_out)
            except Exception:
                pass

            # Helper para seleccionar filtro
            def _sel_filter(name):
                # Filtro codificación típica: (S2,S3)
                # Red=(1,0) Green=(1,1) Blue=(0,1) Clear=(0,0)
                try:
                    if s2 is None or s3 is None:
                        return
                    if name == 'RED':
                        s2.value(1); s3.value(0)
                    elif name == 'GREEN':
                        s2.value(1); s3.value(1)
                    elif name == 'BLUE':
                        s2.value(0); s3.value(1)
                    else:  # CLEAR
                        s2.value(0); s3.value(0)
                except Exception:
                    pass

            period_ms = 300
            last_read = 0
            # Medición de frecuencia por filtro durante dt_ms
            def measure(filter_name, dt_ms=80):
                try:
                    _sel_filter(filter_name)
                    _pulse_cnt[0] = 0
                    t0 = time.ticks_ms()
                    while time.ticks_diff(time.ticks_ms(), t0) < dt_ms:
                        time.sleep_ms(1)
                    return (_pulse_cnt[0] * 1000.0) / dt_ms
                except Exception:
                    return 0.0
            try:
                cl.settimeout(0.01)
                while current_mode == 'COLOR_TCS' and continuous_client == cl:
                    # comandos
                    try:
                        cmd = cl.recv(64)
                        if cmd:
                            txt = cmd.decode().strip()
                            if txt.startswith('TCS_START:'):
                                try:
                                    p = int(float(txt.split(':',1)[1]))
                                    period_ms = max(100, p)
                                    cl.send(b'OK')
                                except Exception:
                                    cl.send(b'ERR')
                            elif 'TCS_STOP' in txt or 'STOP' in txt:
                                cl.send(b'OK')
                                break
                    except Exception:
                        pass

                    now = time.ticks_ms()
                    if time.ticks_diff(now, last_read) >= period_ms:
                        last_read = now
                        # Medir R,G,B secuencialmente dentro del mismo periodo (subventanas cortas)
                        r = measure('RED', 80)
                        g = measure('GREEN', 80)
                        b = measure('BLUE', 80)
                        msg = f"SENSOR:TCS3200,R:{r:.0f},G:{g:.0f},B:{b:.0f}\n"
                        try:
                            cl.send(msg.encode())
                        except Exception:
                            break
                    time.sleep_ms(5)
            except Exception as e:
                print(f"Error en COLOR_TCS: {e}")
            finally:
                try:
                    if out_pin:
                        out_pin.irq(handler=None)
                except Exception:
                    pass
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
