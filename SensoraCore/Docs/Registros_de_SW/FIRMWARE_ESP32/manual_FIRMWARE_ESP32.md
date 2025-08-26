# Manual de Usuario - Firmware ESP32 SensoraCore

## 1. Introducción

### 1.1 Descripción General
El firmware ESP32 de SensoraCore es un sistema embebido desarrollado en MicroPython que proporciona la funcionalidad de adquisición y control de datos para una plataforma completa de instrumentación científica. Este firmware opera en un microcontrolador ESP32 y gestiona 11 módulos especializados de sensores diferentes, ofreciendo comunicación TCP/IP robusta con la aplicación desktop principal.

### 1.2 Características Principales
- **Conectividad WiFi**: Conexión automática con reconexión tras fallos
- **Servidor TCP**: Puerto 8080 para comunicación bidireccional
- **11 Modos de Sensores**: Soporte completo para todos los módulos SensoraCore
- **Tiempo Real**: Adquisición y control en tiempo real con baja latencia
- **Robustez Industrial**: Operación continua 24/7 con recuperación automática
- **Protocolo Simple**: Comandos de texto ASCII para máxima compatibilidad

### 1.3 Arquitectura del Sistema
```
┌─────────────────────────────────────┐
│      Aplicación Desktop PC          │
│         (Python/Qt6)               │
└─────────────────┬───────────────────┘
                  │ TCP/IP
                  │ Puerto 8080
┌─────────────────▼───────────────────┐
│        Firmware ESP32               │
│       (MicroPython)                │
├─────────────────────────────────────┤
│  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐   │
│  │Mod1 │ │Mod2 │ │...  │ │Mod11│   │
│  └─────┘ └─────┘ └─────┘ └─────┘   │
└─────────────────────────────────────┘
                  │
┌─────────────────▼───────────────────┐
│        Hardware Sensores            │
│  Analógicos │ Digitales │ Actuadores│
└─────────────────────────────────────┘
```

## 2. Instalación y Configuración

### 2.1 Requisitos Hardware

#### 2.1.1 Microcontrolador
- **ESP32-WROOM-32** o compatible
- **Flash Memory**: Mínimo 4 MB (recomendado 16 MB)
- **RAM**: 520 KB (estándar ESP32)
- **Frecuencia**: 240 MHz dual-core

#### 2.1.2 Alimentación
- **Voltaje**: 3.3V ±5% (regulado)
- **Corriente**: 500 mA mínimo (1A recomendado)
- **Fuente**: USB, regulador LDO, o fuente switching

#### 2.1.3 Conectividad
- **WiFi**: 802.11 b/g/n 2.4 GHz
- **Antena**: PCB integrada o externa U.FL
- **Rango**: Hasta 150m en línea de vista

### 2.2 Instalación del Firmware

#### 2.2.1 Preparación del Entorno
```bash
# Instalar esptool para flashing
pip install esptool

# Instalar ampy para gestión de archivos
pip install adafruit-ampy

# Descargar MicroPython para ESP32
wget https://micropython.org/download/esp32/esp32-20220618-v1.19.1.bin
```

#### 2.2.2 Flash del Firmware Base
```bash
# Borrar flash completamente
esptool.py --chip esp32 --port COM3 erase_flash

# Instalar MicroPython
esptool.py --chip esp32 --port COM3 --baud 460800 write_flash -z 0x1000 esp32-20220618-v1.19.1.bin

# Verificar instalación
esptool.py --chip esp32 --port COM3 flash_id
```

#### 2.2.3 Carga del Código de Aplicación
```bash
# Conectar al ESP32 y cargar main.py
ampy --port COM3 put main.py

# Verificar archivo cargado
ampy --port COM3 ls

# Reiniciar para ejecutar
ampy --port COM3 reset
```

### 2.3 Configuración de Red WiFi

#### 2.3.1 Configuración Directa en Código
Editar las variables en `main.py`:
```python
# Configuración WiFi
SSID = 'NombreDeRed'
PASSWORD = 'ContraseñaDeRed'
```

#### 2.3.2 Configuración Dinámica (Opcional)
Crear archivo `wifi_config.py`:
```python
# wifi_config.py
NETWORKS = [
    {'ssid': 'Red_Principal', 'password': 'contraseña1'},
    {'ssid': 'Red_Backup', 'password': 'contraseña2'},
]
```

### 2.4 Verificación de Instalación

#### 2.4.1 Monitor Serie
```bash
# Conectar a monitor serie
screen /dev/ttyUSB0 115200
# O en Windows:
putty -serial COM3 -serspeed 115200
```

#### 2.4.2 Mensajes de Inicio Esperados
```
Iniciando SensoraCore ESP32...
Iniciando conexión WiFi...
Intento 1/5: Conectando a 'NombreDeRed'...
WiFi conectado exitosamente!
IP: 192.168.1.100
Servidor iniciado en puerto 8080
```

## 3. Configuración de Hardware

### 3.1 Mapeo de Pines por Módulo

#### 3.1.1 SENSORA_SIMPLE_ANGLE
```
GPIO32 (ADC1_CH4) → Potenciómetro (señal analógica)
VCC → 3.3V
GND → GND
```

#### 3.1.2 SENSORA_ANGLE_ARM
```
GPIO32 (ADC1_CH4) → Potenciómetro 1 (Base)
GPIO33 (ADC1_CH5) → Potenciómetro 2 (Articulación 1)
GPIO34 (ADC1_CH6) → Potenciómetro 3 (Articulación 2)
GPIO25 → Sensor Capacitivo (digital)
```

#### 3.1.3 SENSORA_INFRARED
```
GPIO14 → Sensor IR Digital (entrada)
VCC → 3.3V
GND → GND
```

#### 3.1.4 SENSORA_CAPACITIVE
```
GPIO35 → Sensor Capacitivo Digital (entrada)
VCC → 3.3V
GND → GND
```

#### 3.1.5 SENSORA_ULTRASONIC (HC-SR04)
```
GPIO26 → Trigger
GPIO27 → Echo
VCC → 5V (con divisor de voltaje para Echo)
GND → GND
```

#### 3.1.6 SENSORA_OPTICAL_SPEED
```
# Encoders
GPIO39 → Encoder Izquierdo
GPIO34 → Encoder Derecho

# Control L298N
GPIO25 → IN1 (Motor Izq Forward)
GPIO26 → IN2 (Motor Izq Reverse)
GPIO32 → IN3 (Motor Der Forward)
GPIO33 → IN4 (Motor Der Reverse)
```

#### 3.1.7 SENSORA_IR_STEERING
```
# Array de 5 sensores IR
GPIO4  → IR Sensor 1 (Izquierda)
GPIO16 → IR Sensor 2
GPIO17 → IR Sensor 3 (Centro)
GPIO18 → IR Sensor 4
GPIO19 → IR Sensor 5 (Derecha)

# Motores (mismo que OPTICAL_SPEED)
GPIO25/26 → Motor Izquierdo
GPIO32/33 → Motor Derecho
```

#### 3.1.8 SENSORA_THERMOREGULATION
```
# LM35
GPIO36 (VP) → LM35 Salida

# DS18B20 (OneWire)
GPIO27 → DS18B20 Data (con pull-up 4.7kΩ)

# MAX6675 (SPI)
GPIO32 → SCK
GPIO35 → MISO
GPIO33 → CS
GPIO25 → MOSI (no usado, dummy)
```

#### 3.1.9 SENSORA_GAS_REGULATION
```
GPIO36 (VP) → MQ2 Salida Analógica
GPIO39 → MQ3 Salida Analógica
VCC → 5V (con divisor para señales analógicas)
```

#### 3.1.10 SENSORA_BRIGHTNESS
```
GPIO34 → LDR con divisor resistivo
VCC → 3.3V
GND → GND
```

#### 3.1.11 SENSORA_COLOR_CNY
```
GPIO35 → CNY70 Salida Analógica
VCC → 5V (LED IR)
GND → GND
```

#### 3.1.12 SENSORA_COLOR_TCS
```
GPIO34 → S2 (Filtro)
GPIO35 → S3 (Filtro)
GPIO32 → OUT (Frecuencia)
VCC → 3.3V
GND → GND
```

### 3.2 Consideraciones de Alimentación

#### 3.2.1 Voltajes de Operación
- **ESP32**: 3.3V (regulado)
- **Sensores Analógicos**: 3.3V máximo en entradas ADC
- **Sensores Digitales**: 3.3V o 5V con divisores
- **Actuadores**: 5V-12V según especificaciones

#### 3.2.2 Consumo de Corriente
```
Componente          Corriente    Voltaje
ESP32 WiFi          150-240 mA   3.3V
Sensores Pasivos    1-5 mA       3.3V/5V
Motores DC          100-500 mA   5V-12V
LED Indicadores     10-20 mA     3.3V
Total Estimado      300-800 mA   Múltiple
```

### 3.3 Protecciones Recomendadas

#### 3.3.1 Protección de Entradas
- **Divisores Resistivos**: Para señales de 5V a entradas de 3.3V
- **Diodos Zener**: Protección contra sobrevoltaje
- **Resistencias Pull-up/Pull-down**: Para señales digitales

#### 3.3.2 Protección de Salidas
- **Resistencias Limitadoras**: En salidas PWM
- **Optoacopladores**: Para aislamiento galvánico
- **Drivers de Potencia**: Para cargas inductivas

## 4. Protocolos de Comunicación

### 4.1 Protocolo TCP/IP Base

#### 4.1.1 Características del Protocolo
- **Protocolo**: TCP
- **Puerto**: 8080
- **Formato**: ASCII texto plano
- **Terminación**: `\n` (nueva línea)
- **Timeout**: 30 segundos por defecto

#### 4.1.2 Estructura de Mensajes
```
COMANDO[:PARAMETROS]\n
```

Ejemplos:
```
LED_ON\n
MODO:ANGULO_SIMPLE\n
TH_SET:LM35\n
SET_SPEED:50\n
```

### 4.2 Comandos Básicos

#### 4.2.1 Comandos de Test
```bash
# Encender LED de estado
LED_ON
Respuesta: LED_ON_OK

# Apagar LED de estado  
LED_OFF
Respuesta: LED_OFF_OK

# Leer potenciómetro (test ADC)
GET_POT
Respuesta: <valor_0_4095>

# Detener modo actual
STOP
Respuesta: STOP_OK
```

#### 4.2.2 Comandos de Modo
```bash
# Activar modo específico
MODO:<NOMBRE_MODO>
Respuesta: <NOMBRE_MODO>_OK

# Ejemplo: Activar modo ángulo simple
MODO:ANGULO_SIMPLE
Respuesta: ANGULO_SIMPLE_OK
```

### 4.3 Modos de Operación Específicos

#### 4.3.1 ANGULO_SIMPLE
```bash
# Activar modo
MODO:ANGULO_SIMPLE

# Stream de datos automático
POT:<valor_adc>,ANG:<angulo_grados>
Ejemplo: POT:2048,ANG:0
```

#### 4.3.2 BRAZO_ANGULO
```bash
# Activar modo
MODO:BRAZO_ANGULO

# Stream de datos
POT1:<val1>,ANG1:<ang1>,POT2:<val2>,ANG2:<ang2>,POT3:<val3>,ANG3:<ang3>,SENSOR:<bool>
Ejemplo: POT1:1500,ANG1:-45,POT2:2000,ANG2:-20,POT3:2500,ANG3:15,SENSOR:True
```

#### 4.3.3 DISTANCIA_ULTRA
```bash
# Activar modo
MODO:DISTANCIA_ULTRA

# Stream de datos
ULTRA_CM:<distancia_cm>
Ejemplo: ULTRA_CM:25.3
```

#### 4.3.4 OPTICAL_SPEED
```bash
# Activar modo
MODO:OPTICAL_SPEED

# Configurar velocidad (-100 a +100)
SET_SPEED:<velocidad>
Ejemplo: SET_SPEED:75

# Configurar PPR
SET_PPR:<pulsos_por_revolucion>
Ejemplo: SET_PPR:20

# Stream de datos
RPM_L:<rpm_izq>,RPM_R:<rpm_der>,SPEED:<velocidad_actual>
Ejemplo: RPM_L:120.5,RPM_R:118.2,SPEED:75
```

#### 4.3.5 IR_STEERING
```bash
# Activar modo
MODO:IR_STEERING

# Configurar velocidad base
SET_BASE:<velocidad_base>
Ejemplo: SET_BASE:40

# Configurar PID
SET_PID:kp=<P>,ki=<I>,kd=<D>
Ejemplo: SET_PID:kp=1.0,ki=0.0,kd=0.5

# Stream de datos
SENS:<5_bits>,ERR:<error>,OUT_L:<motor_izq>,OUT_R:<motor_der>,SPEED:<base>,RPM_L:<rpm_l>,RPM_R:<rpm_r>
Ejemplo: SENS:00100,ERR:0.00,OUT_L:40,OUT_R:40,SPEED:40,RPM_L:85.2,RPM_R:87.1
```

#### 4.3.6 THERMOREGULATION
```bash
# Activar modo
MODO:THERMOREGULATION

# Seleccionar sensor
TH_SET:<sensor>
Opciones: LM35, DS18B20, TYPEK
Ejemplo: TH_SET:LM35

# Configurar período (ms)
TH_START:<periodo_ms>
Ejemplo: TH_START:500

# Stream de datos
SENSOR:<tipo>,TEMP_C:<temperatura>,RAW:<valor_raw>
Ejemplo: SENSOR:LM35,TEMP_C:23.45,RAW:717

# Para DS18B20 (sin RAW)
SENSOR:DS18B20,TEMP_C:23.6250

# Detener
TH_STOP
```

#### 4.3.7 GAS_REGULATION
```bash
# Activar modo
MODO:GAS_REGULATION

# Seleccionar sensor
GR_SET:<sensor>
Opciones: MQ2, MQ3
Ejemplo: GR_SET:MQ2

# Iniciar con período
GR_START:<periodo_ms>
Ejemplo: GR_START:1000

# Stream de datos
SENSOR:<tipo>,ADC:<valor>,VOLT:<voltaje>
Ejemplo: SENSOR:MQ2,ADC:1234,VOLT:1.250

# Detener
GR_STOP
```

#### 4.3.8 BRIGHTNESS
```bash
# Activar modo
MODO:BRIGHTNESS

# Iniciar con período
BR_START:<periodo_ms>
Ejemplo: BR_START:200

# Stream de datos
SENSOR:LDR,ADC:<valor>,VOLT:<voltaje>
Ejemplo: SENSOR:LDR,ADC:2048,VOLT:1.650

# Detener
BR_STOP
```

#### 4.3.9 COLOR_TCS
```bash
# Activar modo
MODO:COLOR_TCS

# Iniciar medición
TCS_START:<periodo_ms>
Ejemplo: TCS_START:300

# Stream de datos
SENSOR:TCS3200,R:<freq_rojo>,G:<freq_verde>,B:<freq_azul>
Ejemplo: SENSOR:TCS3200,R:1250,G:980,B:750

# Detener
TCS_STOP
```

## 5. Operación y Monitoreo

### 5.1 Estados del Sistema

#### 5.1.1 Estados del LED Integrado
- **Apagado**: Sistema inicializado correctamente
- **Parpadeo Rápido**: Conectando a WiFi
- **Encendido Fijo**: Test de conexión activo (LED_ON)
- **Parpadeo Lento**: Error de red o reconexión

#### 5.1.2 Estados de Conexión WiFi
```python
# Estados reportados en consola serie
"Iniciando conexión WiFi..."        # Proceso iniciado
"WiFi conectado exitosamente!"      # Conexión establecida
"Conexión WiFi perdida"             # Desconexión detectada
"No se pudo conectar al WiFi"       # Fallo tras reintentos
```

#### 5.1.3 Estados del Servidor TCP
```python
"Servidor iniciado en puerto 8080"     # Servidor activo
"Cliente conectado desde <IP>"          # Nueva conexión
"Error de red: <detalle>"              # Problema de comunicación
```

### 5.2 Monitoreo en Tiempo Real

#### 5.2.1 Console Serie (UART)
- **Puerto**: Generalmente COM3 (Windows) o /dev/ttyUSB0 (Linux)
- **Baudrate**: 115200 bps
- **Configuración**: 8N1 (8 bits, sin paridad, 1 stop bit)

#### 5.2.2 Mensajes de Debug Típicos
```
Iniciando SensoraCore ESP32...
WiFi conectado exitosamente!
IP: 192.168.1.100
Servidor iniciado en puerto 8080
Cliente conectado desde ('192.168.1.50', 54321)
Comando recibido: MODO:ANGULO_SIMPLE
Enviado: POT:2048,ANG:0
```

#### 5.2.3 WebREPL (Opcional)
```python
# Habilitar WebREPL para acceso remoto
import webrepl_setup
# Seguir instrucciones para configurar contraseña
# Acceder via navegador: http://<IP_ESP32>:8266
```

### 5.3 Diagnóstico de Problemas

#### 5.3.1 Problemas de Conectividad WiFi

**Síntoma**: "No se pudo conectar al WiFi"
```python
# Verificaciones:
1. SSID correcto en código
2. Contraseña correcta
3. Red disponible y en rango
4. Frecuencia 2.4 GHz (ESP32 no soporta 5 GHz)
5. Seguridad compatible (WPA/WPA2)
```

**Solución**:
```python
# En REPL, probar manualmente:
import network
sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.scan()  # Ver redes disponibles
sta.connect('SSID', 'PASSWORD')
sta.isconnected()  # Verificar estado
```

#### 5.3.2 Problemas de Comunicación TCP

**Síntoma**: Cliente no puede conectar al puerto 8080
```bash
# Desde PC, verificar conectividad:
ping <IP_ESP32>
telnet <IP_ESP32> 8080
```

**Diagnóstico**:
```python
# Verificar IP del ESP32
sta.ifconfig()  # En REPL

# Verificar firewall del PC
# Windows: permitir conexiones entrantes en puerto 8080
# Linux: iptables -A INPUT -p tcp --dport 8080 -j ACCEPT
```

#### 5.3.3 Problemas de Sensores

**Síntoma**: Lecturas erróneas o sin datos
```python
# Test manual de ADC:
from machine import Pin, ADC
adc = ADC(Pin(32))
adc.atten(ADC.ATTN_11DB)
adc.read()  # Debe retornar 0-4095

# Test de GPIO digital:
pin = Pin(14, Pin.IN, Pin.PULL_UP)
pin.value()  # Debe retornar 0 o 1
```

#### 5.3.4 Problemas de Memoria

**Síntoma**: "MemoryError" o reinicios aleatorios
```python
# Verificar memoria disponible:
import gc
gc.collect()
gc.mem_free()  # Debe ser >20KB para operación estable

# En caso de memoria insuficiente:
# - Reducir frecuencia de muestreo
# - Simplificar buffers de datos
# - Forzar garbage collection más frecuente
```

## 6. Configuración Avanzada

### 6.1 Optimización de Red

#### 6.1.1 Configuración WiFi Estática
```python
# En main.py, después de sta.connect():
sta.ifconfig(('192.168.1.100', '255.255.255.0', '192.168.1.1', '8.8.8.8'))
```

#### 6.1.2 Ajuste de Potencia WiFi
```python
# Reducir potencia para ahorrar energía
import network
sta = network.WLAN(network.STA_IF)
sta.config(txpower=8.5)  # Rango: 2.5 - 20 dBm
```

#### 6.1.3 Configuración de Timeout TCP
```python
# En create_server(), ajustar timeout:
s.settimeout(60)  # 60 segundos
```

### 6.2 Optimización de Rendimiento

#### 6.2.1 Frecuencia de CPU
```python
# Ajustar frecuencia para ahorro energético
import machine
machine.freq(160000000)  # 160 MHz (por defecto: 240 MHz)
```

#### 6.2.2 Gestión de Memoria
```python
# Forzar garbage collection periódico
import gc
# En loops principales, agregar:
if gc.mem_free() < 20000:
    gc.collect()
```

#### 6.2.3 Optimización de ADC
```python
# Para mayor precisión en ADC:
adc.width(ADC.WIDTH_12BIT)  # Máxima resolución
adc.atten(ADC.ATTN_11DB)    # Rango completo 0-3.3V
```

### 6.3 Configuración de Seguridad

#### 6.3.1 Filtrado de IP
```python
# En main.py, agregar verificación de IP cliente:
allowed_ips = ['192.168.1.50', '192.168.1.51']
if addr[0] not in allowed_ips:
    cl.close()
    continue
```

#### 6.3.2 Autenticación Simple
```python
# Requerir comando de autenticación antes de operar:
def authenticate(command):
    if command != "AUTH:secret_key":
        return False
    return True
```

### 6.4 Logging Avanzado

#### 6.4.1 Log a Archivo
```python
# Guardar logs en archivo (si hay suficiente flash):
def log(message):
    with open('sensor.log', 'a') as f:
        f.write(f"{time.ticks_ms()}: {message}\n")
```

#### 6.4.2 Log por Red
```python
# Enviar logs a servidor syslog externo:
import socket
def send_log(message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(message.encode(), ('192.168.1.10', 514))
    sock.close()
```

## 7. Mantenimiento y Actualización

### 7.1 Actualización de Firmware

#### 7.1.1 Actualización Manual
```bash
# Cargar nuevo main.py
ampy --port COM3 put main_new.py main.py

# Reiniciar ESP32
ampy --port COM3 reset
```

#### 7.1.2 Backup de Configuración
```bash
# Descargar configuración actual
ampy --port COM3 get main.py main_backup.py
ampy --port COM3 get wifi_config.py wifi_backup.py
```

#### 7.1.3 Actualización OTA (Over-The-Air)
```python
# Código básico para OTA (agregar a main.py):
def check_update():
    import urequests
    response = urequests.get('http://server/firmware_version')
    if response.text.strip() > current_version:
        download_update()

def download_update():
    # Descargar y aplicar nueva versión
    pass
```

### 7.2 Monitoreo de Salud del Sistema

#### 7.2.1 Métricas de Sistema
```python
# Agregar al loop principal:
def system_health():
    import gc, machine
    print(f"Memoria libre: {gc.mem_free()} bytes")
    print(f"Frecuencia CPU: {machine.freq()} Hz")
    print(f"Temperatura interna: {esp32.raw_temperature()} °F")
```

#### 7.2.2 Watchdog Timer
```python
# Implementar watchdog para reinicio automático:
from machine import WDT
wdt = WDT(timeout=30000)  # 30 segundos

# En loop principal:
wdt.feed()  # Reset watchdog
```

### 7.3 Calibración de Sensores

#### 7.3.1 Calibración ADC
```python
# Procedimiento de calibración de ADC:
def calibrate_adc():
    # Conectar referencias conocidas y medir
    ref_0v = adc.read()    # Con entrada a GND
    ref_3v3 = adc.read()   # Con entrada a 3.3V
    # Calcular offset y ganancia
    offset = ref_0v
    gain = (4095 - ref_0v) / 3.3
    return offset, gain
```

#### 7.3.2 Calibración de Sensores Térmicos
```python
# Calibración multi-punto para LM35:
def calibrate_lm35():
    # Medir a temperaturas conocidas
    temp_points = [0, 25, 50]  # °C
    adc_readings = []
    for temp in temp_points:
        input(f"Coloque sensor a {temp}°C y presione Enter")
        reading = adc.read()
        adc_readings.append(reading)
    # Calcular coeficientes de calibración
    return calculate_calibration(temp_points, adc_readings)
```

## 8. Resolución de Problemas Específicos

### 8.1 Errores Comunes y Soluciones

#### 8.1.1 "OSError: [Errno 113] EHOSTUNREACH"
**Causa**: Problema de routing de red
**Solución**:
```bash
# Verificar gateway:
ip route show  # Linux
route print    # Windows

# Verificar máscara de subred
```

#### 8.1.2 "MemoryError"
**Causa**: Memoria RAM insuficiente
**Solución**:
```python
# Simplificar código:
# - Reducir variables globales
# - Usar generadores en lugar de listas
# - Llamar gc.collect() más frecuentemente
# - Reducir buffers de datos
```

#### 8.1.3 "ValueError: invalid pin"
**Causa**: GPIO no válido para la función
**Solución**:
```python
# Verificar pinout ESP32:
# - ADC1: GPIO32-39
# - ADC2: GPIO0,2,4,12-15,25-27 (conflicto con WiFi)
# - Solo input: GPIO34,35,36,39
# - Evitar: GPIO6-11 (flash), GPIO1,3 (UART)
```

#### 8.1.4 Sensores Retornan Valores Constantes
**Causa**: Configuración incorrecta de pines
**Solución**:
```python
# Verificar configuración:
# - Pull-up/pull-down apropiados
# - Atenuación ADC correcta
# - Divisores de voltaje si es necesario
# - Conexiones físicas
```

### 8.2 Herramientas de Diagnóstico

#### 8.2.1 Test de Conectividad Completo
```python
def connectivity_test():
    print("=== Test de Conectividad ===")
    
    # Test WiFi
    if sta.isconnected():
        print(f"✓ WiFi: {sta.ifconfig()[0]}")
    else:
        print("✗ WiFi: Desconectado")
    
    # Test TCP
    try:
        s = socket.socket()
        s.bind(('0.0.0.0', 8080))
        s.listen(1)
        print("✓ TCP: Puerto 8080 disponible")
        s.close()
    except:
        print("✗ TCP: Puerto 8080 ocupado")
    
    # Test Hardware
    test_hardware()

def test_hardware():
    print("=== Test de Hardware ===")
    
    # Test ADC
    adc = ADC(Pin(32))
    reading = adc.read()
    print(f"ADC GPIO32: {reading} ({reading/4095*3.3:.2f}V)")
    
    # Test GPIO Digital
    pin = Pin(14, Pin.IN, Pin.PULL_UP)
    print(f"GPIO14: {pin.value()}")
```

#### 8.2.2 Monitor de Rendimiento
```python
def performance_monitor():
    import time, gc
    start_time = time.ticks_ms()
    
    while True:
        current_time = time.ticks_ms()
        uptime = time.ticks_diff(current_time, start_time)
        
        print(f"Uptime: {uptime//1000}s")
        print(f"Memoria libre: {gc.mem_free()} bytes")
        print(f"WiFi RSSI: {sta.status('rssi')} dBm")
        
        time.sleep(10)
```

## 9. Optimización para Producción

### 9.1 Configuración de Producción

#### 9.1.1 Deshabilitar Debug
```python
# Reducir prints para mejor rendimiento
DEBUG_LEVEL = 0  # 0=silencioso, 1=errores, 2=info, 3=debug

def debug_print(level, message):
    if level <= DEBUG_LEVEL:
        print(message)
```

#### 9.1.2 Configuración de Red Robusta
```python
# Configuración para entorno industrial
MAX_RETRIES = 10
RECONNECT_DELAY = 5  # segundos
KEEPALIVE_INTERVAL = 30  # segundos

def robust_wifi_connect():
    for attempt in range(MAX_RETRIES):
        try:
            sta.connect(SSID, PASSWORD)
            # Esperar con timeout
            timeout = time.time() + 20
            while not sta.isconnected() and time.time() < timeout:
                time.sleep(0.5)
            
            if sta.isconnected():
                return True
        except Exception as e:
            debug_print(1, f"Error WiFi: {e}")
        
        time.sleep(RECONNECT_DELAY)
    return False
```

### 9.2 Gestión de Energía

#### 9.2.1 Modos de Bajo Consumo
```python
# Para aplicaciones con batería
import machine

def enter_light_sleep(duration_ms):
    # Configurar wake-up timer
    timer = machine.Timer(0)
    timer.init(period=duration_ms, mode=machine.Timer.ONE_SHOT, 
               callback=lambda t: None)
    
    # Entrar en light sleep
    machine.lightsleep()

def optimize_power():
    # Reducir frecuencia CPU
    machine.freq(80000000)  # 80 MHz
    
    # Ajustar potencia WiFi
    sta.config(txpower=5)  # Mínima potencia
```

### 9.3 Redundancia y Recuperación

#### 9.3.1 Múltiples Redes WiFi
```python
WIFI_NETWORKS = [
    {'ssid': 'Red_Principal', 'password': 'pass1'},
    {'ssid': 'Red_Backup', 'password': 'pass2'},
    {'ssid': 'Red_Emergencia', 'password': 'pass3'}
]

def connect_best_network():
    networks = sta.scan()
    available_ssids = [net[0].decode() for net in networks]
    
    for network in WIFI_NETWORKS:
        if network['ssid'] in available_ssids:
            try:
                sta.connect(network['ssid'], network['password'])
                return True
            except:
                continue
    return False
```

#### 9.3.2 Recuperación Automática
```python
def recovery_system():
    error_count = 0
    max_errors = 5
    
    while True:
        try:
            # Operación normal
            main_loop()
            error_count = 0  # Reset contador en operación exitosa
            
        except Exception as e:
            error_count += 1
            debug_print(1, f"Error {error_count}: {e}")
            
            if error_count >= max_errors:
                debug_print(1, "Demasiados errores, reiniciando...")
                machine.reset()
            
            time.sleep(1)  # Pausa antes de reintento
```

## 10. Referencias y Recursos

### 10.1 Documentación Técnica

#### 10.1.1 ESP32
- [ESP32 Datasheet](https://www.espressif.com/sites/default/files/documentation/esp32_datasheet_en.pdf)
- [ESP32 Technical Reference](https://www.espressif.com/sites/default/files/documentation/esp32_technical_reference_manual_en.pdf)
- [MicroPython ESP32 Quick Reference](https://docs.micropython.org/en/latest/esp32/quickref.html)

#### 10.1.2 Bibliotecas MicroPython
- [machine module](https://docs.micropython.org/en/latest/library/machine.html)
- [network module](https://docs.micropython.org/en/latest/library/network.html)
- [socket module](https://docs.micropython.org/en/latest/library/socket.html)

### 10.2 Herramientas de Desarrollo

#### 10.2.1 IDEs Recomendados
- **Thonny**: IDE simple para MicroPython
- **uPyCraft**: IDE especializado para ESP32
- **VSCode**: Con extensión MicroPython
- **PyCharm**: Con plugin MicroPython

#### 10.2.2 Herramientas de Flash
- **esptool.py**: Herramienta oficial de Espressif
- **ESP32 Flash Download Tool**: GUI oficial
- **ampy**: Gestión de archivos MicroPython

### 10.3 Recursos de Comunidad

#### 10.3.1 Foros y Soporte
- [MicroPython Forum](https://forum.micropython.org/)
- [ESP32 Forum](https://www.esp32.com/)
- [Reddit r/esp32](https://www.reddit.com/r/esp32/)

#### 10.3.2 Repositorios de Código
- [MicroPython GitHub](https://github.com/micropython/micropython)
- [ESP32 Examples](https://github.com/espressif/esp-idf/tree/master/examples)
- [Awesome MicroPython](https://github.com/mcauser/awesome-micropython)

### 10.4 Especificaciones de Sensores

#### 10.4.1 Sensores Analógicos
- **LM35**: Sensor de temperatura ±0.5°C precisión
- **MQ2**: Sensor de gas/humo 300-10000 ppm
- **LDR**: Fotoresistor 1-100k ohm rango

#### 10.4.2 Sensores Digitales
- **HC-SR04**: Ultrasónico 2-400cm rango
- **DS18B20**: Temperatura digital ±0.5°C
- **TCS3200**: Sensor de color RGB frecuencia de salida

### 10.5 Estándares y Certificaciones

#### 10.5.1 Cumplimiento Regulatorio
- **FCC Part 15**: Certificación para Estados Unidos
- **CE**: Conformidad Europea
- **IC**: Industry Canada
- **RoHS**: Restricción de sustancias peligrosas

#### 10.5.2 Estándares Industriales
- **IEC 61010**: Seguridad en equipos de medición
- **IEEE 802.11**: Estándares WiFi
- **TCP/IP**: Protocolos de red estándar
