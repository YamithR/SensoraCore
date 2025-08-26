# Manual de Usuario - SENSORA THERMOREGULATION

## 1. Introducción

El módulo **SENSORA_THERMOREGULATION** representa una solución avanzada para el monitoreo y control de temperatura utilizando múltiples tecnologías de sensado térmico. Este sistema está diseñado para aplicaciones industriales, científicas y educativas que requieren mediciones precisas de temperatura con capacidades de calibración, análisis temporal y control automático.

### Características Principales
- **Triple sensor**: LM35 (analógico), DS18B20 (digital OneWire) y Termopar Tipo K (SPI)
- **Rango amplio**: -55°C a +150°C (LM35), -55°C a +125°C (DS18B20), -200°C a +1024°C (Tipo K)
- **Calibración avanzada**: Compensación lineal y cuadrática por sensor
- **Visualización**: Gráficas temporales en tiempo real con matplotlib
- **Exportación**: Datos completos en Excel/CSV con metadatos de calibración
- **Comunicación**: TCP/IP con ESP32 para monitoreo continuo

### Aplicaciones
- Sistemas de control térmico industrial
- Monitoreo ambiental y climático
- Procesos de manufactura sensibles a temperatura
- Investigación científica en termofísica
- Sistemas HVAC (calefacción, ventilación, aire acondicionado)
- Aplicaciones educativas en instrumentación térmica

## 2. Especificaciones Técnicas

### Sensor LM35 (Analógico)
- **Tipo**: Circuito integrado analógico de precisión
- **Rango**: -55°C a +150°C
- **Precisión**: ±1°C a temperatura ambiente
- **Linealidad**: 10 mV/°C (factor de escala fijo)
- **Alimentación**: 4V a 30V (típico 5V)
- **Corriente**: 60 µA (bajo consumo)
- **Tiempo respuesta**: < 1 segundo
- **Resolución**: Limitada por ADC (12-bit = 0.08°C)

### Sensor DS18B20 (Digital OneWire)
- **Tipo**: Sensor digital con protocolo OneWire
- **Rango**: -55°C a +125°C
- **Precisión**: ±0.5°C (-10°C a +85°C)
- **Resolución**: Configurable 9-12 bits (0.5°C a 0.0625°C)
- **Alimentación**: 3.0V a 5.5V (modo normal) o parasítico
- **Tiempo conversión**: 93.75ms (9-bit) a 750ms (12-bit)
- **Protocolo**: Dallas OneWire (1 cable de datos)
- **Direccionamiento**: 64-bit único (múltiples sensores en bus)

### Termopar Tipo K con MAX6675
- **Tipo**: Termopar Chromel-Alumel con conversor SPI
- **Rango**: -200°C a +1024°C (limitado por MAX6675: 0°C a +1024°C)
- **Precisión**: ±3°C (0°C a +700°C)
- **Resolución**: 0.25°C (12-bit)
- **Tiempo conversión**: 170ms típico
- **Compensación**: Junta fría automática en MAX6675
- **Protocolo**: SPI (3 cables: SCK, MISO, CS)
- **Alimentación**: 3.0V a 5.5V

### Sistema de Comunicación
- **Protocolo**: TCP/IP sobre WiFi
- **Comando inicial**: "MODO:THERMOREGULATION"
- **Configuración sensor**: "TH_SET:LM35/DS18B20/TYPEK"
- **Control streaming**: "TH_START:<period_ms>", "TH_STOP"
- **Formatos datos**:
  - LM35: "SENSOR:LM35,TEMP_C:25.3,RAW:2048"
  - DS18B20: "SENSOR:DS18B20,TEMP_C:24.7"
  - TYPEK: "SENSOR:TYPEK,TEMP_C:350.25,RAW:1401"

## 3. Compatibilidad de Hardware

### Microcontrolador Requerido
- **ESP32 DevKit V1** o compatible
- **ADC**: 12-bit para sensor LM35
- **GPIO**: OneWire para DS18B20
- **SPI**: Para comunicación MAX6675
- **WiFi**: 802.11 b/g/n para comunicación TCP

### Conexiones por Sensor
**LM35 (Analógico)**:
```
ESP32 Pin    LM35 Pin    Función
3V3      →   VCC         Alimentación
GND      →   GND         Tierra
D36/VP   ←   VOUT        Salida analógica
```

**DS18B20 (OneWire)**:
```
ESP32 Pin    DS18B20 Pin    Función
3V3      →   VDD            Alimentación
GND      →   GND            Tierra
D27      ↔   DQ             Datos OneWire
```
*Nota: Resistor pull-up 4.7kΩ entre DQ y VDD requerido*

**Termopar Tipo K + MAX6675**:
```
ESP32 Pin    MAX6675 Pin    Función
3V3      →   VCC            Alimentación
GND      →   GND            Tierra
D32      →   SCK            Clock SPI
D35      ←   SO (MISO)      Datos SPI
D33      →   CS             Chip Select
          →   T+             Terminal positivo termopar
          →   T-             Terminal negativo termopar
```

### Consideraciones de Instalación
- **LM35**: Montaje con disipador térmico para mediciones precisas
- **DS18B20**: Cable blindado para aplicaciones industriales
- **Termopar K**: Uniones soldadas o conectores de compensación

## 4. Instalación y Configuración

### Requisitos del Sistema
- **Python**: 3.8 o superior
- **PySide6**: Framework Qt6 para interfaz gráfica
- **matplotlib**: Visualización científica de datos
- **numpy**: Procesamiento matemático
- **pandas**: Análisis de datos temporales
- **openpyxl**: Exportación a Excel

### Instalación de Dependencias
```bash
pip install PySide6 matplotlib numpy pandas openpyxl
```

### Configuración ESP32
1. **Programar firmware**: Incluir módulo THERMOREGULATION
2. **Configurar sensores**: Instalar sensores según aplicación
3. **Red WiFi**: Conectar ESP32 a red local
4. **Verificar IP**: Anotar dirección asignada

### Estructura de Archivos
```
thermoregulation/
├── thermoregulation_logic.py    # Lógica principal y algoritmos
├── thermoregulation_ui.py       # Interfaz gráfica generada
├── thermoregulation.ui          # Diseño Qt Designer
└── ~/.sensora_core/thermo_calib.json  # Calibraciones persistentes
```

## 5. Manual de Usuario

### Inicio del Sistema
1. **Abrir aplicación** SENSORA CORE
2. **Seleccionar módulo** "THERMOREGULATION"
3. **Verificar conexiones** de sensores instalados
4. **Introducir IP** del ESP32 en campo correspondiente
5. **Seleccionar sensor** activo (LM35/DS18B20/TYPEK)

### Interfaz de Usuario
- **Panel Superior**: Título y descripción del módulo
- **Panel Izquierdo**: Selector de sensores y lecturas en tiempo real
- **Panel Central**: Gráfica temporal de temperatura
- **Panel Derecho**: Controles de operación y calibración

### Selección de Sensor
1. **LM35**: Presionar botón correspondiente (sensor analógico)
2. **DS18B20**: Activar sensor digital OneWire
3. **TYPEK**: Seleccionar termopar de alta temperatura
4. **Cambio dinámico**: Posible durante monitoreo activo

### Configuración de Muestreo
- **Período mínimo**: 100ms (LM35), 800ms (DS18B20), 200ms (TYPEK)
- **Configuración**: Slider o campo numérico en interfaz
- **Aplicación**: Automática al cambiar valor

### Proceso de Calibración
**Calibración por Puntos de Referencia**:
1. **Punto de hielo**: 0°C con hielo destilado
2. **Temperatura ambiente**: Verificar con termómetro patrón
3. **Punto de ebullición**: 100°C (ajustar por presión atmosférica)
4. **Puntos adicionales**: Para calibración cuadrática

**Tipos de Calibración**:
- **Lineal**: T_real = a × T_medido + b
- **Cuadrática**: T_real = a × T_medido² + b × T_medido + c

### Monitoreo en Tiempo Real
1. **Iniciar streaming**: Presionar "Iniciar Monitoreo"
2. **Observar datos**: Temperatura actual y valor RAW
3. **Analizar tendencias**: Gráfica temporal automática
4. **Cambiar sensor**: Selección dinámica sin detener
5. **Pausar**: Mantener datos históricos

## 6. Algoritmos y Procesamiento

### Procesamiento LM35
```python
def lm35_to_celsius(adc_value, vref=3.3, adc_max=4095):
    # Conversión ADC a voltaje
    voltage = (adc_value / adc_max) * vref
    # Conversión a temperatura (10 mV/°C)
    temperature = voltage * 100.0  # 1000 mV/V / 10 mV/°C
    return temperature
```

### Procesamiento DS18B20
```python
# Protocolo OneWire implementado en firmware ESP32
# Conversión interna del sensor (12-bit por defecto)
# Transmisión directa del valor en °C
def ds18b20_read():
    # Comando de conversión + lectura scratchpad
    # Resolución: 0.0625°C (12-bit)
    return temperature_celsius
```

### Procesamiento Termopar Tipo K
```python
def max6675_to_celsius(raw_value):
    # Bits 15-3: datos temperatura
    # Bit 2: estado termopar (0=conectado, 1=desconectado)
    # Bits 1-0: no usados
    
    if raw_value & 0x4:  # Bit 2 = 1
        return float('nan')  # Termopar desconectado
    
    # Extraer datos temperatura (bits 15-3)
    temp_data = (raw_value >> 3) & 0xFFF
    
    # Conversión a °C (resolución 0.25°C)
    temperature = temp_data * 0.25
    
    return temperature
```

### Algoritmos de Calibración
```python
def linear_calibration(measured_points, reference_points):
    # Regresión lineal: y = ax + b
    from numpy import polyfit
    coeffs = polyfit(measured_points, reference_points, 1)
    return coeffs[0], coeffs[1]  # a, b

def quadratic_calibration(measured_points, reference_points):
    # Regresión cuadrática: y = ax² + bx + c
    from numpy import polyfit
    coeffs = polyfit(measured_points, reference_points, 2)
    return coeffs[0], coeffs[1], coeffs[2]  # a, b, c
```

### Comunicación TCP
```python
# Inicialización
socket.connect((ip, 8080))
socket.sendall(b"MODO:THERMOREGULATION\n")

# Configuración sensor
socket.sendall(b"TH_SET:LM35\n")  # o DS18B20, TYPEK
socket.sendall(b"TH_START:500\n")  # período 500ms

# Datos recibidos
"SENSOR:LM35,TEMP_C:25.3,RAW:2048"
```

## 7. Validación y Calibración

### Protocolo de Validación
1. **Test hardware**: Verificar conexiones y alimentación
2. **Test comunicación**: Respuesta TCP y lectura sensores
3. **Calibración inicial**: Puntos de referencia conocidos
4. **Prueba estabilidad**: Medición continua 30 minutos
5. **Validación cruzada**: Comparar con termómetro patrón

### Procedimientos de Calibración
**LM35 (Calibración de dos puntos)**:
- **Punto 1**: 0°C (hielo destilado en equilibrio)
- **Punto 2**: 100°C (vapor agua destilada a presión conocida)
- **Corrección**: Lineal suficiente para rango operativo

**DS18B20 (Calibración digital)**:
- **Verificación**: Comparar con patrón certificado
- **Ajuste**: Principalmente por deriva temporal
- **Múltiples puntos**: -10°C, 0°C, 25°C, 50°C, 85°C

**Termopar Tipo K (Calibración extendida)**:
- **Punto frío**: 0°C (hielo)
- **Punto medio**: 100°C (vapor agua)
- **Punto alto**: 500°C (horno calibrado)
- **Punto muy alto**: 800°C (validación opcional)

### Métricas de Calidad
- **Exactitud**: ±0.5°C en rango normal (0°C a 100°C)
- **Repetibilidad**: CV < 0.1% en mediciones consecutivas
- **Deriva temporal**: < 0.1°C por mes en uso continuo
- **Tiempo respuesta**: 90% valor final en < 30 segundos

### Incertidumbre de Medición
- **LM35**: ±1°C (especificación) + ±0.08°C (cuantización ADC)
- **DS18B20**: ±0.5°C (especificación) + deriva calibración
- **Tipo K**: ±3°C (especificación) + ±0.25°C (resolución MAX6675)

## 8. Aplicaciones Educativas

### Laboratorio de Instrumentación
- **Principios sensores térmicos**: Diferentes tecnologías comparadas
- **Acondicionamiento señales**: ADC, OneWire, SPI
- **Calibración metrológica**: Trazabilidad a patrones
- **Análisis de incertidumbre**: Propagación errores

### Termodinámica Aplicada
- **Transferencia de calor**: Medición coeficientes
- **Capacidad calorífica**: Experimentos calentamiento
- **Cinética térmica**: Constantes de tiempo
- **Procesos isotérmicos**: Control retroalimentado

### Control Automático
- **Sensado de proceso**: Temperatura como variable controlada
- **Sistemas SISO**: Single Input Single Output
- **Controladores PID**: Sintonización térmica
- **Modelado dinámico**: Funciones transferencia

### Metrología y Calidad
- **Patrones de temperatura**: ITS-90 y escalas prácticas
- **Calibración comparativa**: Métodos de laboratorio
- **Certificación equipos**: Procedimientos normalizados
- **Documentación técnica**: Reportes de calibración

## 9. Mantenimiento y Solución de Problemas

### Mantenimiento Preventivo
- **Limpieza sensores**: Alcohol isopropílico mensual
- **Verificación conexiones**: Resistencia contactos < 0.1Ω
- **Actualización firmware**: ESP32 y aplicación PC
- **Backup calibraciones**: Archivo thermo_calib.json

### Problemas Comunes por Sensor
**LM35 - Lecturas errática**:
- Verificar alimentación estable 3.3V
- Revisar capacitor desacoplamiento 100nF
- Comprobar ruido electromagnético
- Validar rango temperatura (-55°C a +150°C)

**DS18B20 - Sin respuesta OneWire**:
- Verificar resistor pull-up 4.7kΩ
- Comprobar longitud cable (máximo 100m)
- Revisar integridad bus OneWire
- Validar tiempo conversión (750ms)

**Tipo K - Lecturas inestables**:
- Verificar conexiones termopar soldadas
- Comprobar compensación junta fría
- Revisar ruido en cables largos
- Validar rango MAX6675 (0°C a +1024°C)

### Diagnóstico Avanzado
```python
# Test comunicación por sensor
def test_sensor_communication():
    send_command("TH_SET:LM35")
    response = read_response()
    if "LM35" in response:
        print("LM35: OK")
    
    # Repetir para DS18B20 y TYPEK

# Verificación calibración
def verify_calibration():
    raw_temp = read_raw_temperature()
    calibrated_temp = apply_calibration(raw_temp)
    print(f"Raw: {raw_temp}, Calibrated: {calibrated_temp}")
```

### Procedimientos de Emergencia
- **Sobretemperatura**: Límites software programables
- **Fallo sensor**: Cambio automático a sensor backup
- **Pérdida comunicación**: Alarmas locales
- **Deriva excesiva**: Protocolo recalibración inmediata

## 10. Seguridad y Consideraciones

### Seguridad Eléctrica
- **Aislamiento galvánico**: Separar circuitos alta temperatura
- **Protección**: Fusibles y limitadores corriente
- **Cableado certificado**: Resistente a temperatura operativa
- **Conexiones seguras**: Terminales apropiados para aplicación

### Seguridad Térmica
- **Límites programables**: Alarmas por sobretemperatura
- **Materiales resistentes**: Cables y conectores certificados
- **Distancias seguridad**: Separación de componentes sensibles
- **Procedimientos emergencia**: Desconexión automática

### Consideraciones Ambientales
- **Rango operativo**: Validar especificaciones ambientales
- **Humedad**: < 90% RH para componentes electrónicos
- **Vibración**: Montaje antivibratorio para precisión
- **Interferencias**: Blindaje para mediciones precisas

### Protección de Datos
- **Backup automático**: Calibraciones críticas
- **Trazabilidad**: Log de calibraciones con timestamp
- **Validación**: Comparación con patrones certificados
- **Documentación**: Procedimientos según ISO 17025

## 11. Conclusiones

El módulo **SENSORA_THERMOREGULATION** proporciona una plataforma completa y versátil para medición de temperatura utilizando tres tecnologías complementarias. Su diseño modular permite desde aplicaciones educativas básicas hasta sistemas industriales de control térmico.

### Ventajas Clave
- **Versatilidad**: Tres sensores con rangos y aplicaciones específicas
- **Precisión**: Calibración avanzada con compensación matemática
- **Robustez**: Comunicación TCP con reconexión automática
- **Usabilidad**: Interfaz intuitiva con visualización científica
- **Integración**: Exportación completa para análisis posteriores

### Limitaciones Identificadas
- **Rango LM35**: Limitado a +150°C máximo
- **DS18B20**: Tiempo conversión relativamente lento (750ms)
- **Tipo K**: Deriva de junta fría en MAX6675
- **Precisión**: Dependiente de calidad calibración inicial

### Desarrollos Futuros
- Compensación automática de junta fría para termopares
- Algoritmos de filtrado digital para reducir ruido
- Múltiples sensores DS18B20 en mismo bus OneWire
- Integración con sistemas de control industrial (Modbus, OPC-UA)
- Calibración automática con patrones internos
- Interfaz web para monitoreo remoto

### Impacto Educativo y Científico
El sistema establecido proporciona una base sólida para:
- Educación en instrumentación térmica moderna
- Investigación en transferencia de calor aplicada
- Desarrollo de sistemas de control térmico
- Validación de modelos termodinámicos

Esta plataforma facilita la comprensión práctica de conceptos fundamentales en medición de temperatura, proporcionando experiencia directa con tecnologías industriales estándar y preparando usuarios para aplicaciones profesionales en instrumentación térmica.
