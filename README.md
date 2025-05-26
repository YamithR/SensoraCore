# SensoraCore Alpha 0.2.2

**Sistema de Monitoreo de Sensores WiFi ESP32 + PySide6** 🚀

✅ **VERSIÓN ALPHA 0.2.2** - Estado: **FUNCIONAL** con Correcciones de Gráficas

**Fecha de Lanzamiento:** Mayo 25, 2025

SensoraCore es un sistema de monitoreo de sensores que conecta un ESP32 ejecutando MicroPython con una aplicación de escritorio desarrollada en Python usando PySide6. El sistema permite leer datos de sensores en tiempo real a través de WiFi, visualizarlos gráficamente y exportar los datos a Excel.

## ✨ Características Principales

### 🎨 **Interfaz Moderna y Responsive**
- **Layout de dos paneles**: Panel izquierdo para conexión y sensores, panel derecho para detalles
- **Diseño responsive**: Ajustable con splitter, proporción 1/3 - 2/3
- **Animaciones suaves**: Transiciones fade-in al conectar ESP32
- **Colores optimizados**: Mejor visibilidad en gráficas y diagramas
- **Diagrama de conexiones ESP32**: Información visual incluida en la interfaz

### 🔐 **Experiencia de Usuario Inteligente**
- **Sensores ocultos hasta conexión**: Previene errores de uso prematuro
- **Indicadores visuales de estado**: Verde=conectado, Rojo=desconectado
- **Controles dinámicos**: Botones cambian según el contexto
- **Validación inteligente**: Sistema previene estados inconsistentes
- **Lista de sensores como menú**: Selección intuitiva con efectos visuales

### 📊 **Visualización Avanzada**
- **Gráficas profesionales**: Colores destacados y grid sutil
- **Monitoreo en tiempo real**: Actualización continua de datos
- **Controles de reproducción**: Iniciar/Pausar/Continuar/Detener
- **Exportación Excel mejorada**: Formato profesional con gráficas integradas
- **Estadísticas automáticas**: Min, max, promedio calculados en tiempo real

### 📡 **Comunicación WiFi Robusta**
- **Conexión inalámbrica estable**: Entre ESP32 y aplicación de escritorio
- **Protocolo de comandos**: Sistema de comunicación estructurado
- **Manejo de errores**: Reconexión automática y timeouts inteligentes
- **Feedback en tiempo real**: Estado de conexión siempre visible
- **Thread para recepción continua**: Sistema no bloqueante

## 📋 Sensores Soportados

### ✅ Implementados y Funcionales
- **Ángulo Simple (Potenciómetro)**: Lee un potenciómetro como sensor de ángulo (0-270°) - **Analógico con gráficas**
- **Brazo Ángulo**: Sensor multi-ángulo para brazo robótico (3 potenciómetros + sensor capacitivo) - **Analógico múltiple**
- **DistanciaIR**: Sensor de distancia infrarrojo Sharp GP2Y0A21YK - **Digital ON/OFF**
- **DistanciaCap**: Sensor de distancia capacitivo - **Digital ON/OFF** 
- **DistanciaUltrasonido**: Sensor ultrasónico HC-SR04 (2-400 cm) - **Analógico con gráficas**

### 🔄 Próximamente
- **OpticTestLR_Velocidad**: Sensor óptico de velocidad

### 🆕 Novedades Alpha 0.2
- **✅ Interfaz digital/analógica unificada**: Sensores IR y capacitivos ahora muestran estados digitales ON/OFF
- **✅ Indicadores visuales mejorados**: Colores dinámicos para estados de detección
- **✅ Sensor ultrasónico implementado**: HC-SR04 con medición precisa de distancia
- **✅ Optimización de rendimiento**: Sistema de updates mejorado para mejor fluidez
- **✅ Arquitectura híbrida**: Diferenciación clara entre sensores digitales y analógicos

### 🔧 Correcciones Alpha 0.2.2
- **✅ Inicialización de gráficas corregida**: Solucionado problema donde las gráficas no se mostraban correctamente al seleccionar sensores
- **✅ Canvas draw inicial agregado**: Añadido `canvas.draw()` inicial en todas las interfaces de sensores analógicos
- **✅ Renderizado mejorado**: Las gráficas ahora se renderizan correctamente desde el primer uso
- **✅ Estabilidad aumentada**: Eliminados errores de visualización en sensores de ángulo simple, brazo ángulo y ultrasónico

## 📊 Estado del Proyecto - ALPHA 0.2.2

### ✅ COMPLETADO

#### 🏗️ Estructura del Proyecto
- [x] Estructura de carpetas organizada
- [x] Separación clara entre aplicación y código ESP32
- [x] Documentación completa y unificada
- [x] Guía de inicio rápido integrada

#### 💻 Aplicación de Escritorio (SensoraCoreApp)
- [x] Interfaz gráfica con PySide6
- [x] Diseño responsive con QSplitter
- [x] Layout moderno de dos paneles (1/3 - 2/3)
- [x] Panel izquierdo con conexión y lista de sensores
- [x] Panel derecho para detalles específicos del sensor
- [x] Campo de entrada para IP del ESP32
- [x] Botón de conexión con estado visual mejorado
- [x] Indicador de estado de conexión con colores
- [x] Lista de sensores oculta hasta conectar ESP32
- [x] Animación fade-in al mostrar sensores
- [x] Interfaz específica por sensor seleccionado
- [x] Gráfica con colores destacados y mejor visibilidad
- [x] Controles de inicio/pausa/detener monitoreo
- [x] Exportación a Excel con formato profesional
- [x] Botón para limpiar gráfica
- [x] Manejo de errores y mensajes informativos
- [x] Configuración centralizada (config.py)
- [x] Script para generar ejecutable (build_exe.py)
- [x] **Inicialización de gráficas corregida (Alpha 0.2.2)**: Solucionado problema de renderizado inicial

#### 🔌 ESP32 (SensoraCoreESP32)
- [x] Código MicroPython funcional
- [x] Conexión WiFi automática
- [x] Servidor socket en puerto 8080
- [x] Lectura de potenciómetro en GPIO 32
- [x] Control del LED integrado
- [x] Modo continuo para transmisión de datos
- [x] Mapeo correcto de ángulos (-135° <> 135°)
- [x] Manejo de comandos por protocolo
- [x] Sensores digitales (IR y capacitivo)
- [x] Sensor ultrasónico implementado

#### 📡 Comunicación
- [x] Protocolo de comandos definido y ampliado
- [x] Cliente de red (network_client.py)
- [x] Thread para recepción continua (AnguloSimpleThread)
- [x] Manejo de timeouts y errores de conexión
- [x] Formato de datos estructurado
- [x] Protocolos diferenciados por tipo de sensor

### 🎯 ESTADO ACTUAL: LISTO PARA USO

#### ✅ Lo que ya funciona:
1. **Conexión WiFi ESP32 ↔ PC** ✅
2. **Lectura de todos los sensores implementados** ✅
3. **Visualización en tiempo real** ✅
4. **Exportación a Excel** ✅
5. **Interfaz gráfica completa y moderna** ✅
6. **Sistema híbrido digital/analógico** ✅

#### 🚀 Listo para:
- Demostración del sistema completo
- Uso en entorno educativo
- Migración de sensores desde Arduino
- Desarrollo de nuevas funcionalidades
- Aplicaciones en tiempo real

## 🏗️ Estructura del Proyecto

```
SensoraCore/
├── README.md                    # Documentación completa y unificada
├── PROJECT_STATUS.md           # Estado detallado del proyecto
├── QUICKSTART.md               # Guía de inicio rápido
├── RELEASE_NOTES_Alpha_0.2.md  # Notas de la versión actual
├── SensoraCoreApp/             # Aplicación de escritorio (Python/PySide6)
│   ├── main.py                 # Punto de entrada de la aplicación
│   ├── requirements.txt        # Dependencias Python
│   ├── network_client.py       # Cliente de red para comunicación con ESP32
│   ├── config.py               # Configuración centralizada
│   ├── build_exe.py            # Script para generar ejecutable
│   ├── compilar.bat            # Script de compilación Windows
│   └── ui/
│       ├── __init__.py
│       └── main_window.py      # Interfaz gráfica principal
└── SensoraCoreESP32/           # Código para ESP32 (MicroPython)
    ├── main.py                 # Servidor principal del ESP32
    ├── main_brazo.py           # Configuración específica para brazo robótico
    ├── main_new.py             # Versión en desarrollo
    └── wifi_config.py          # Configuración WiFi
```

## 🚀 Guía de Inicio Rápido

### ⚡ Requisitos Previos
- **Hardware**: ESP32 DevKit V1
- **Software**: Python 3.8+, MicroPython para ESP32
- **Red**: WiFi 2.4GHz (WPA/WPA2)

### 🔧 Instalación y Configuración

#### 1. Aplicación de Escritorio (Python)

```bash
# Clonar o descargar el proyecto
cd SensoraCoreApp

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar la aplicación
python main.py
```

#### 2. ESP32 (MicroPython)

1. **Instalar MicroPython** en tu ESP32 DevKit V1:
   - Descargar firmware MicroPython para ESP32
   - Flashear usando esptool o Thonny IDE

2. **Configurar WiFi** en `wifi_config.py`:
```python
SSID = 'Tu_Red_WiFi'
PASSWORD = 'Tu_Contraseña'
```

3. **Subir archivos** al ESP32:
   - `main.py` (servidor principal)
   - `wifi_config.py` (configuración WiFi)

### ⚡ Uso Rápido

1. **Preparar ESP32**: Conectar sensores según diagramas
2. **Encender ESP32**: Anotar IP mostrada en monitor serial  
3. **Ejecutar App**: `python main.py`
4. **Conectar**: Ingresar IP y presionar "Conectar"
5. **Monitorear**: Seleccionar sensor y ver datos en tiempo real
6. **Exportar**: Guardar datos en Excel cuando necesites

## 🔌 Conexiones Hardware

### ESP32 DevKit V1 - Diagrama Completo

```
ESP32 DevKit V1 - Conexiones de Sensores:

┌────────────────────────────────────────────────────┐
│              ESP32 DevKit V1                       │
│                                                    │
│  ┌─ Sensores Analógicos ─┐  ┌─ Sensores Digitales ─┐
│  │ 3V3 ○ ←── Pot (+)     │  │ 3V3 ○ ←── IR VCC     │
│  │ GND ○ ←── Pot (-)     │  │ GND ○ ←── IR GND     │
│  │ D32 ○ ←── Pot (S)     │  │ D35 ○ ←── IR OUT     │
│  │                       │  │                      │
│  │ 5V  ○ ←── Ultra VCC   │  │ 3V3 ○ ←── Cap VCC    │
│  │ GND ○ ←── Ultra GND   │  │ GND ○ ←── Cap GND    │
│  │ D26 ○ ←── Ultra Trig  │  │ D35 ○ ←── Cap OUT    │
│  │ D27 ○ ←── Ultra Echo  │  │                      │
│  └───────────────────────┘  └──────────────────────┘
│                                                    │
│  LED integrado: GPIO 2                             │
│  Puerto Serie: 115200 baudios                      │
│  WiFi: 2.4GHz                                      │
└────────────────────────────────────────────────────┘

Especificaciones de Sensores:

Potenciómetro 10kΩ (Ángulo):
• Pin (+): Alimentación 3.3V
• Pin (-): Tierra (GND)
• Pin (S): Señal analógica → GPIO 32
• Rango: 0-270° (mapeo automático)

Sensor IR Sharp GP2Y0A21YK:
• Pin VCC → 3.3V ESP32
• Pin GND → GND ESP32
• Pin OUT → GPIO 14 ESP32
• Rango: 10-80 cm (modo digital ON/OFF)

Sensor Capacitivo de Distancia:
• Pin VCC → 3.3V ESP32
• Pin GND → GND ESP32
• Pin OUT → GPIO 35 ESP32
• Rango: 0-40 cm (modo digital ON/OFF)

Sensor Ultrasónico HC-SR04:
• Pin VCC → 5V ESP32 (importante: requiere 5V)
• Pin GND → GND ESP32
• Pin Trig → GPIO 26 ESP32
• Pin Echo → GPIO 27 ESP32
• Rango: 2-400 cm (medición analógica precisa)
```

### 🔧 Configuración de Brazo Robótico

Para el sensor "Brazo Ángulo" se requieren múltiples potenciómetros:

```
Brazo Robótico - Configuración Múltiple:

GPIO 32 → Potenciómetro 1 (Articulación Base)
GPIO 33 → Potenciómetro 2 (Articulación Medio)  
GPIO 34 → Potenciómetro 3 (Articulación Final)
GPIO 25 → Sensor Capacitivo (Detector de Objeto)

Todos los potenciómetros: 3.3V, GND, señal analógica
```

## 🖥️ Uso de la Aplicación

### 🚀 Flujo Básico de Uso

1. **Conectar ESP32**:
   - Enciende el ESP32 y espera que se conecte al WiFi
   - Anota la IP que aparece en el monitor serial (ej: 192.168.1.100)

2. **Conectar desde la App**:
   - Ingresa la IP del ESP32 en la aplicación
   - Presiona "Conectar y encender LED integrado"
   - Si la conexión es exitosa, el LED del ESP32 se encenderá
   - El indicador de estado cambiará a verde

3. **Seleccionar Sensor**:
   - Elige el sensor deseado de la lista lateral (aparece después de conectar)
   - **Ángulo Simple**: Gira el potenciómetro para ver datos en tiempo real
   - **Brazo Ángulo**: Monitor de 3 potenciómetros + sensor capacitivo
   - **Distancia IR**: Medición digital ON/OFF con sensor infrarrojo
   - **Distancia Capacitivo**: Medición digital ON/OFF capacitiva
   - **Distancia Ultrasónico**: Medición analógica precisa (2-400 cm)

4. **Monitorear Datos**:
   - **Sensores Analógicos**: Ver gráficas en tiempo real con valores numéricos
   - **Sensores Digitales**: Ver indicadores de estado ON/OFF con colores
   - Usar controles de Iniciar/Pausar/Continuar/Detener según necesites

5. **Exportar Datos**:
   - Presiona "Exportar datos a Excel" para guardar los datos
   - El archivo incluye datos tabulados y gráficas automáticas
   - Estadísticas (min, max, promedio) incluidas

6. **Limpiar Gráfica**:
   - Usa "Limpiar gráfica" para borrar todos los datos y reiniciar

### 🎯 Características de la Interfaz

#### Panel Izquierdo (1/3 del ancho)
- **Campo IP**: Entrada para dirección ESP32
- **Botón Conectar**: Con indicador visual de estado
- **Lista de Sensores**: Aparece solo después de conexión exitosa
- **Diagrama de Conexiones**: Información visual del hardware

#### Panel Derecho (2/3 del ancho)  
- **Área de Gráficas**: Para sensores analógicos
- **Indicadores Digitales**: Para sensores ON/OFF
- **Controles de Monitoreo**: Iniciar, Pausar, Detener
- **Estadísticas en Tiempo Real**: Min, Max, Promedio
- **Botones de Acción**: Exportar, Limpiar

## 📡 Protocolo de Comunicación

### Comandos ESP32 → Aplicación

| Comando | Descripción | Respuesta | Tipo |
|---------|-------------|-----------|------|
| `LED_ON` | Encender LED integrado | `LED_ON_OK` | Control |
| `LED_OFF` | Apagar LED integrado | `LED_OFF_OK` | Control |
| `GET_POT` | Leer potenciómetro una vez | `valor_adc` | Lectura única |
| `MODO:ANGULO_SIMPLE` | Activar modo continuo | `POT:lectura,ANG:angulo` | Analógico |
| `MODO:BRAZO_ANGULO` | Activar modo brazo robótico | `POT1:val,ANG1:ang,POT2:val,ANG2:ang,POT3:val,ANG3:ang,SENSOR:state` | Analógico múltiple |
| `MODO:DISTANCIA_IR` | Activar sensor IR digital | `IR_DIGITAL:True/False` | Digital |
| `MODO:DISTANCIA_CAP` | Activar sensor capacitivo digital | `CAP_DIGITAL:True/False` | Digital |
| `MODO:DISTANCIA_ULTRA` | Activar sensor ultrasónico | `ULTRA_ADC:val,ULTRA_V:volt,ULTRA_CM:dist` | Analógico |
| `STOP` | Detener modo continuo | `STOP_OK` | Control |

### Formato de Datos en Tiempo Real

#### Sensores Analógicos (Con Gráficas)
```
# Ángulo Simple
POT:2048,ANG:135
POT:1024,ANG:67

# Brazo Robótico (Múltiple)
POT1:2048,ANG1:135,POT2:1024,ANG2:67,POT3:3072,ANG3:203,SENSOR:True

# Sensor Ultrasónico  
ULTRA_ADC:1500,ULTRA_V:1.21,ULTRA_CM:125.3
ULTRA_ADC:2000,ULTRA_V:1.61,ULTRA_CM:165.8
```

#### Sensores Digitales (Estados ON/OFF)
```
# Sensor IR (True = objeto detectado)
IR_DIGITAL:True
IR_DIGITAL:False

# Sensor Capacitivo (True = proximidad detectada)
CAP_DIGITAL:True  
CAP_DIGITAL:False
```

### Protocolo de Red
- **Puerto**: 8080 (TCP)
- **Formato**: Texto plano UTF-8
- **Terminador**: `\n` (nueva línea)
- **Timeout**: 5 segundos por comando
- **Reconexión**: Automática en caso de fallo

## 📊 Funcionalidades de Exportación

### Archivo Excel Generado

El archivo Excel exportado contiene múltiples hojas según el sensor:

#### **Hoja "Datos Ángulo Simple"**:
- **Columna A**: Número de muestra (1, 2, 3...)
- **Columna B**: Lectura ADC raw (0-4095)
- **Columna C**: Ángulo calculado (0-270°)
- **Columna D**: Timestamp (fecha y hora)
- **Estadísticas automáticas**: Min, Max, Promedio
- **Gráfica de líneas**: Incluida automáticamente

#### **Hoja "Datos Brazo Robótico"**:
- **Columnas A-D**: Muestra, Timestamp, Pot1, Ángulo1
- **Columnas E-F**: Pot2, Ángulo2
- **Columnas G-H**: Pot3, Ángulo3  
- **Columna I**: Estado sensor capacitivo
- **Múltiples gráficas**: Una por articulación

#### **Hoja "Datos Ultrasónico"**:
- **Columna A**: Número de muestra
- **Columna B**: Valor ADC
- **Columna C**: Voltaje (V)
- **Columna D**: Distancia (cm)
- **Columna E**: Timestamp
- **Gráfica de distancia vs tiempo**

#### **Sensores Digitales**:
- **Archivo CSV**: Para estados TRUE/FALSE con timestamps
- **Log de eventos**: Cambios de estado registrados

### Formato Profesional
- **Encabezados con formato**: Negrita y colores
- **Celdas autoajustadas**: Ancho óptimo automático
- **Gráficas integradas**: Con títulos y ejes etiquetados
- **Estadísticas resaltadas**: En celdas especiales

## 🛠️ Desarrollo y Extensión

### Agregar Nuevos Sensores

#### 1. En ESP32 (`main.py`):
```python
# Agregar nuevo comando en el bucle principal
elif command == "MODO:MI_NUEVO_SENSOR":
    modo_continuo = True
    while modo_continuo:
        # Leer sensor
        valor = leer_mi_sensor()
        # Enviar respuesta
        cl.send(f"MI_SENSOR:{valor}\n")
        time.sleep(0.1)
```

#### 2. En Aplicación (`main_window.py`):
```python
# Crear nuevo QGroupBox para el sensor
self.mi_sensor_widget = self.crear_widget_mi_sensor()

# Implementar thread de comunicación  
class MiSensorThread(QThread):
    data_received = pyqtSignal(str)
    # ... implementación específica

# Agregar visualización específica
def actualizar_mi_sensor(self, data):
    # Procesar datos y actualizar interfaz
    pass
```

### Estructura de Threads

- **AnguloSimpleThread**: Maneja comunicación continua con ESP32
- **MainWindow**: Interfaz principal y coordinación de threads
- **ESP32Client**: Cliente de red para comandos individuales
- **Threads específicos**: Uno por cada tipo de sensor

### Configuración (config.py)

```python
# Configuraciones centralizadas
ESP32_PORT = 8080
DEFAULT_IP = "192.168.1.100"
EXCEL_PATH = "./exports/"
GRAPH_UPDATE_INTERVAL = 100  # ms
CONNECTION_TIMEOUT = 5  # segundos
```

## 🎓 Aplicaciones Educativas

### 📚 Para Estudiantes

#### Conceptos que se Pueden Enseñar:
- **Señales Analógicas vs Digitales**: Diferenciación visual clara
- **Calibración de Sensores**: Mapeo de valores ADC a unidades físicas  
- **Comunicación WiFi**: Protocolos TCP/IP en aplicaciones reales
- **Visualización de Datos**: Gráficas en tiempo real y estadísticas
- **Automatización**: Control remoto de dispositivos

#### Experimentos Prácticos:
1. **Medición de Ángulos**: Calibrar potenciómetro como goniómetro
2. **Detección de Proximidad**: Comparar sensores IR vs Capacitivo
3. **Medición de Distancia**: Precisión del sensor ultrasónico
4. **Sistemas de Control**: Brazo robótico con múltiples articulaciones
5. **Adquisición de Datos**: Exportación y análisis en Excel

### 👨‍🏫 Para Educadores

#### Ventajas del Sistema:
- **Todo en uno**: Hardware + software + documentación
- **Escalable**: Fácil agregar nuevos sensores y experimentos
- **Visual**: Interfaz intuitiva con feedback inmediato
- **Documentado**: Guías completas y ejemplos listos
- **Flexible**: Adaptable a diferentes niveles educativos

#### Módulos Didácticos Incluidos:
1. **Introducción a Sensores**: Conceptos básicos con potenciómetro
2. **Sensores de Distancia**: Comparación de tecnologías diferentes  
3. **Robótica Básica**: Control de brazo con múltiples articulaciones
4. **Comunicación Inalámbrica**: Principios de redes y protocolos
5. **Análisis de Datos**: Estadísticas y visualización científica

## 🔄 Futuras Mejoras (Roadmap)

### 🎯 Versión Alpha 0.3 (Planificada)
- [ ] **Sensores Ambientales**: Temperatura, humedad, presión
- [ ] **Sistema de Calibración**: Automático con puntos de referencia
- [ ] **Modo Multi-Sensor**: Monitoreo simultáneo de varios sensores
- [ ] **Interfaz Web**: Acceso remoto desde navegador
- [ ] **Base de Datos**: Almacenamiento persistente de experimentos

### 🎨 Mejoras de Interfaz
- [ ] **Tema Oscuro/Claro**: Selección de usuario
- [ ] **Pestañas Múltiples**: Para varios sensores simultáneos
- [ ] **Dashboards Personalizables**: Layouts definidos por usuario
- [ ] **Alertas Inteligentes**: Notificaciones por valores fuera de rango
- [ ] **Perfiles de Usuario**: Configuraciones guardables

### 📊 Análisis Avanzado
- [ ] **Filtros Digitales**: Media móvil, Kalman, pasa-bajos
- [ ] **FFT y Análisis Espectral**: Para señales periódicas
- [ ] **Machine Learning**: Detección de patrones automática
- [ ] **Comparación de Sesiones**: Análisis histórico
- [ ] **Reportes Automáticos**: Generación de informes PDF

### 🔧 Funcionalidades Técnicas
- [ ] **Discovery Automático**: Encontrar ESP32 en red automáticamente
- [ ] **OTA Updates**: Actualización remota del firmware ESP32
- [ ] **Logs Detallados**: Sistema de debugging avanzado
- [ ] **API REST**: Integración con sistemas externos
- [ ] **Plugins**: Sistema de extensiones de terceros

## 🐛 Solución de Problemas

### ❌ Error de Conexión ESP32

**Síntomas**: No se puede conectar, timeout de conexión
```
Verificaciones:
✅ ESP32 encendido y ejecutando código
✅ WiFi conectado (verificar IP en monitor serial)  
✅ IP correcta en la aplicación
✅ Puerto 8080 no bloqueado por firewall
✅ ESP32 y PC en la misma red WiFi
```

**Soluciones**:
1. Reiniciar ESP32 y verificar conexión WiFi
2. Verificar firewall de Windows (permitir puerto 8080)
3. Probar con IP estática en lugar de DHCP
4. Usar comando `ping` para verificar conectividad

### ❌ Error al Exportar Excel

**Síntomas**: Fallo al guardar archivo, permisos denegados
```
Verificaciones:
✅ openpyxl instalado: pip install openpyxl
✅ Permisos de escritura en carpeta destino
✅ Archivo Excel no abierto en otra aplicación
✅ Espacio suficiente en disco
```

**Soluciones**:
1. Ejecutar como administrador si es necesario
2. Cambiar carpeta de destino a Documentos
3. Cerrar archivos Excel abiertos
4. Reinstalar openpyxl: `pip uninstall openpyxl && pip install openpyxl`

### ❌ Gráfica no se Actualiza

**Síntomas**: Datos recibidos pero gráfica estática
```
Verificaciones:
✅ matplotlib instalado correctamente
✅ Sensor seleccionado adecuadamente
✅ Modo continuo activado (botón "Iniciar")
✅ Thread de comunicación funcionando
```

**Soluciones**:
1. Reiniciar aplicación completamente
2. Verificar instalación: `pip install matplotlib`
3. Limpiar gráfica y reiniciar monitoreo
4. Verificar conexión WiFi estable

### ❌ Sensores Digitales No Responden

**Síntomas**: Siempre muestra el mismo estado
```
Verificaciones:
✅ Conexiones de alimentación (3.3V, GND)
✅ Cable de señal en GPIO correcto
✅ Sensor dentro del rango operativo
✅ Alimentación suficiente del ESP32
```

**Soluciones**:
1. Verificar voltajes con multímetro
2. Probar sensor con código de prueba simple
3. Ajustar sensibilidad (si es ajustable)
4. Verificar datasheet del sensor específico

### ❌ Sensor Ultrasónico Readings Erróneas

**Síntomas**: Mediciones inconsistentes o fuera de rango
```
Verificaciones:
✅ Alimentación 5V (no 3.3V)
✅ Cables Trig y Echo en GPIOs correctos
✅ Superficie reflectante enfrente del sensor
✅ Distancia dentro del rango (2-400 cm)
```

**Soluciones**:
1. **Importante**: Verificar alimentación de 5V
2. Probar con objeto grande y plano
3. Verificar conexiones con continuidad
4. Ajustar timeout en código si es necesario

### ❌ Gráficas No Se Muestran al Iniciar (Solucionado en 0.2.2)

**Síntomas**: Las gráficas aparecen en blanco o no se renderizan al seleccionar sensores analógicos
```
Estado: ✅ SOLUCIONADO en Alpha 0.2.2
Causa: Falta de inicialización del canvas matplotlib
Solución: Agregado canvas.draw() inicial en todas las interfaces
```

**Si experimentas este problema en versiones anteriores**:
1. Actualizar a SensoraCore Alpha 0.2.2 o superior
2. Verificar que se ejecute `canvas.draw()` después de configurar la gráfica
3. Reiniciar la aplicación después de seleccionar un sensor

## 🚀 Generación de Ejecutable

### Crear Aplicación Standalone

Para distribuir la aplicación sin requerir Python instalado:

```bash
# Navegar a la carpeta de la aplicación
cd SensoraCoreApp

# Instalar PyInstaller (si no está instalado)
pip install pyinstaller

# Usar el script incluido (recomendado)
python build_exe.py

# O ejecutar manualmente
pyinstaller --onefile --windowed --icon=icon.ico main.py

# En Windows, también puedes usar
compilar.bat
```

El ejecutable se genera en la carpeta `dist/` y puede distribuirse independientemente.

## 📝 Contribuir al Proyecto

### 🔧 Proceso de Contribución

1. **Fork del repositorio**: Crear copia personal
2. **Crear rama específica**: `git checkout -b feature/nueva-funcionalidad`
3. **Implementar cambios**: Seguir estándares del código existente
4. **Documentar cambios**: Actualizar README y comentarios
5. **Ejecutar pruebas**: Verificar que todo funciona
6. **Crear Pull Request**: Describir cambios detalladamente

### 📋 Áreas de Contribución

#### 🔬 Nuevos Sensores
- Sensores de temperatura/humedad (DHT22, SHT30)
- Acelerómetros y giroscopios (MPU6050)
- Sensores de luz (LDR, TSL2561)
- Sensores de gas (MQ series)
- Cámaras ESP32-CAM

#### 💻 Mejoras de Software
- Optimización de rendimiento
- Nuevas funciones de análisis
- Mejoras de UI/UX
- Traducción a otros idiomas
- Testing automatizado

#### 📚 Documentación
- Tutoriales paso a paso
- Videos demostrativos  
- Ejemplos de aplicaciones
- Guías de troubleshooting
- Traducción de documentación

### 🎯 Estándares de Código

#### Python (Aplicación)
```python
# Usar docstrings para funciones importantes
def procesar_datos_sensor(data: str) -> dict:
    """
    Procesa datos recibidos del sensor.
    
    Args:
        data: String con formato "SENSOR:valor"
    
    Returns:
        dict: Datos procesados
    """
    pass

# Usar type hints cuando sea posible
# Seguir PEP 8 para estilo de código
# Manejo de errores con try/except específicos
```

#### MicroPython (ESP32)
```python
# Comentarios claros para configuraciones
# Funciones modulares y reutilizables
# Manejo de recursos (memoria, conexiones)
# Timeouts apropiados para operaciones de red
```

## 🔐 Compatibilidad y Requisitos

### 💻 Software Requerido

#### Aplicación de Escritorio
```
Python: 3.8+ (recomendado 3.10+)
Librerías:
├── PySide6 >= 6.0.0    # Interfaz gráfica
├── matplotlib >= 3.5.0 # Gráficas
├── openpyxl >= 3.0.0   # Exportación Excel  
├── numpy >= 1.20.0     # Procesamiento numérico
└── pyqtgraph >= 0.12.0 # Gráficas de alto rendimiento (opcional)
```

#### ESP32
```
MicroPython: v1.19+ para ESP32
Memoria: Mínimo 4MB Flash
WiFi: 2.4GHz, WPA/WPA2
Pines: Según sensor específico
```

### 🔌 Hardware Soportado

#### Microcontroladores
- ✅ ESP32 DevKit V1 (recomendado)
- ✅ ESP32 WROOM-32
- ✅ ESP32-S2/S3 (con modificaciones menores)
- ⚠️ ESP8266 (funcionalidad limitada)

#### Sensores Verificados
| Sensor | Modelo | Tipo | Status |
|--------|--------|------|--------|
| Potenciómetro | 10kΩ lineal | Analógico | ✅ Funcional |
| IR Distancia | Sharp GP2Y0A21YK | Digital | ✅ Funcional |
| Capacitivo | Genérico | Digital | ✅ Funcional |
| Ultrasónico | HC-SR04 | Analógico | ✅ Funcional |
| Temperatura | DHT22 | Digital | 🔄 En desarrollo |
| Acelerómetro | MPU6050 | I2C | 🔄 Planeado |

### 🌐 Redes Soportadas
- **WiFi 2.4GHz**: WPA, WPA2, WPA3 (según ESP32)
- **Protocolos**: TCP/IP, HTTP (para futuras versiones)
- **Topología**: Punto a punto (ESP32 ↔ PC)
- **Rango**: Según red WiFi (típicamente 10-50 metros)

## 📄 Licencia y Créditos

### 📜 Licencia
```
MIT License

Copyright (c) 2025 Proyecto SensoraCore

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

### 👥 Créditos y Reconocimientos

#### 🎓 Proyecto Educativo
**Desarrollado como parte del proyecto**: "Módulos Didácticos para el Fortalecimiento de Competencias en Calibración de Sensores"

#### 🛠️ Tecnologías Utilizadas
- **[Python](https://python.org)**: Lenguaje principal de la aplicación
- **[PySide6](https://doc.qt.io/qtforpython/)**: Framework de interfaz gráfica
- **[MicroPython](https://micropython.org)**: Firmware para ESP32
- **[matplotlib](https://matplotlib.org)**: Biblioteca de gráficas científicas
- **[OpenPyXL](https://openpyxl.readthedocs.io)**: Generación de archivos Excel

#### 🤝 Contribuidores
- **Equipo de Desarrollo**: Yamith Romero
- **Supervisión Académica**: Saul Pérez & Carlos Diaz
- **Testing y Validación**: Yamith Romero
- **Documentación**: Yamith Romero & Elian Ruidiaz

#### 🎯 Objetivos del Proyecto
1. **Educación STEM**: Facilitar el aprendizaje de conceptos de sensores y automatización
2. **Accesibilidad**: Tecnología abierta y de bajo costo
3. **Escalabilidad**: Base para proyectos más complejos
4. **Documentación**: Material educativo completo y accesible

---

## 📞 Contacto y Soporte

### 🌐 Enlaces del Proyecto
- **Repositorio**: https://github.com/YamithR/SensoraCore
- **Issues**: [Mail : yamithromero@hotmail.com](https://github.com/YamithR/SensoraCore/issues)
- **Discusiones**: [URL del foro de la comunidad]

### 🐞 Reportar Problemas
Para reportar bugs o solicitar funcionalidades:
1. Verificar que no existe un issue similar
2. Usar plantillas de issue proporcionadas
3. Incluir información del sistema y pasos para reproducir
4. Adjuntar logs si es posible

---

**Versión**: Alpha 0.2.2
**Estado**: Funcional con correcciones de gráficas aplicadas  
**Última actualización**: Mayo 25, 2025
