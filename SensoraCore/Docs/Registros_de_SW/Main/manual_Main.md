# Manual de Usuario - Código Principal SensoraCore

## Índice
1. [Introducción](#introducción)
2. [Instalación y Configuración](#instalación-y-configuración)
3. [Interfaz de Usuario](#interfaz-de-usuario)
4. [Conexión con ESP32](#conexión-con-esp32)
5. [Selección y Uso de Sensores](#selección-y-uso-de-sensores)
6. [Sistema de Logging](#sistema-de-logging)
7. [Solución de Problemas](#solución-de-problemas)
8. [Especificaciones Técnicas](#especificaciones-técnicas)
9. [Mantenimiento](#mantenimiento)
10. [Soporte Técnico](#soporte-técnico)
11. [Apéndices](#apéndices)

---

## 1. Introducción

### Descripción General
SensoraCore es una plataforma de instrumentación científica avanzada que proporciona control centralizado para un sistema distribuido de sensores basado en microcontrolador ESP32. La aplicación principal actúa como centro de comando unificado, permitiendo el monitoreo, control y análisis de datos de 11 tipos diferentes de sensores especializados.

**Arquitectura del Código Principal**:
El archivo `main.py` (2387 líneas) implementa la lógica central del sistema con componentes clave:
- **Función `app_path()`**: Sistema inteligente de resolución de rutas compatible con PyInstaller
- **Clase `LoadingSplashScreen`**: Pantalla de inicio profesional con barra de progreso
- **Clase `ui(QMainWindow)`**: Controlador principal de la aplicación con gestión de 12 widgets de sensores
- **Clase `ESP32Client`**: Cliente TCP para comunicación robusta con microcontrolador
- **Clase `EmittingStream`**: Redirección de logs a interfaz gráfica

**Gestión Dinámica de Sensores**:
La aplicación maneja dinámicamente 12 módulos de sensores mediante:
- Carga de interfaces .ui específicas para cada sensor
- Instanciación controlada de lógicas especializadas (SimpleAngleLogic, AngleArmLogic, etc.)
- Sistema de limpieza automática con función `_cleanup_active_sensors()`
- Recreación de widgets con `_recreate_sensor_widgets()` para robustez

### Características Principales
- **Interfaz Gráfica Intuitiva**: Desarrollada en Qt6 para máxima usabilidad y rendimiento
- **Conectividad Robusta**: Comunicación TCP/IP estable con ESP32 para aplicaciones industriales
- **Modularidad Avanzada**: Sistema de plugins para fácil extensión y personalización
- **Compatibilidad Multiplataforma**: Soporte nativo para Windows, Linux y macOS
- **Logging Profesional**: Sistema de trazabilidad completa para aplicaciones científicas

### Aplicaciones
- **Educación Superior**: Laboratorios de ingeniería, física y ciencias aplicadas
- **Investigación Científica**: Adquisición de datos experimentales y validación de modelos
- **Industria**: Monitoreo de procesos, control de calidad y automatización
- **Desarrollo**: Prototipado rápido de sistemas de instrumentación

---

## 2. Instalación y Configuración

### Requisitos del Sistema

#### Requisitos Mínimos
- **Sistema Operativo**: Windows 10, Ubuntu 20.04 LTS, macOS 11+
- **Procesador**: Dual-core 2.0 GHz (Intel i3, AMD A8, ARM Cortex-A72)
- **Memoria RAM**: 4 GB (8 GB recomendado)
- **Almacenamiento**: 2 GB de espacio libre
- **Red**: WiFi 802.11n o Ethernet 100Mbps

#### Requisitos Recomendados
- **Procesador**: Quad-core 3.0 GHz+ con soporte de virtualización
- **Memoria RAM**: 16 GB+ para análisis de datasets extensos
- **Almacenamiento**: SSD 500 GB NVMe para rendimiento óptimo
- **GPU**: Dedicada con OpenGL 4.0+ para aceleración de visualización
- **Red**: Gigabit Ethernet con switch dedicado

### Instalación desde Ejecutable

#### Windows
1. **Descargar** el ejecutable `SensoraCore_Beta1.0.exe` desde el directorio de versiones
2. **Ejecutar** como administrador para instalación completa del sistema
3. **Configurar** firewall para permitir comunicaciones en puerto 8080
4. **Verificar** la instalación ejecutando la aplicación

#### Linux
```bash
# Instalar dependencias del sistema
sudo apt update
sudo apt install python3 python3-pip qt6-base-dev

# Hacer ejecutable el binario
chmod +x SensoraCore_Beta1.0
./SensoraCore_Beta1.0
```

#### macOS
```bash
# Permitir ejecución de aplicaciones de terceros
sudo spctl --master-disable
./SensoraCore_Beta1.0
sudo spctl --master-enable
```

### Instalación desde Código Fuente

#### Preparación del Entorno
```bash
# Clonar el repositorio
git clone <url-repositorio> SensoraCore
cd SensoraCore

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

#### Ejecución de Desarrollo
```bash
cd SC_DesktopApp
python main.py
```

**Detalles del Archivo Principal**:
El archivo `main.py` contiene la implementación completa del sistema:
- **2387 líneas de código** con arquitectura modular robusta
- **Sistema de resolución de rutas** compatible con PyInstaller onefile/onedir
- **12 imports de módulos** de sensores especializados desde carpeta Modules
- **Gestión automática de recursos** con cleanup sistemático
- **Protocolo TCP personalizado** para comunicación ESP32

**Estructura de Importaciones**:
```python
from Modules.simpleAngle.simpleAngle_logic import SimpleAngleLogic
from Modules.angleArm.angleArm_logic import AngleArmLogic
from Modules.infrared.infrared_logic import InfraredLogic
# ... (9 módulos adicionales)
```

### Configuración de Red

#### Configuración del ESP32
1. **Conectar** ESP32 a la red WiFi de instrumentación
2. **Anotar** la dirección IP asignada al dispositivo
3. **Verificar** conectividad mediante ping al ESP32
4. **Configurar** reglas de firewall si es necesario

#### Configuración de Firewall
```bash
# Windows (Ejecutar como administrador)
netsh advfirewall firewall add rule name="SensoraCore" dir=in action=allow protocol=TCP localport=8080

# Linux (iptables)
sudo iptables -A INPUT -p tcp --dport 8080 -j ACCEPT

# macOS (pf)
echo "pass in proto tcp from any to any port 8080" | sudo pfctl -f -
```

---

## 3. Interfaz de Usuario

### Ventana Principal

#### Splash Screen
Al iniciar la aplicación, se muestra una pantalla de carga profesional con:
- **Barra de progreso** animada para indicar el estado de inicialización
- **Logo de SensoraCore** con branding corporativo
- **Información de versión** y copyright
- **Tiempo de carga** aproximado de 3-5 segundos

**Implementación Técnica del Splash Screen**:
```python
class LoadingSplashScreen(QWidget):
    # Widget sin marco con QVBoxLayout
    # Timer de 30ms con incremento +1% hasta 100%
    # Estilo CSS personalizado: fondo blanco, borde gris
    # Tamaño fijo: 420x110 pixels
```

#### Layout Principal
La interfaz principal está organizada en áreas funcionales claramente definidas:

**Panel Superior:**
- **Campo de IP**: Entrada para dirección IP del ESP32 con validación en tiempo real
- **Botón Conectar**: Establece conexión con feedback visual inmediato
- **Indicador de Estado**: LED virtual que muestra estado de conectividad

**Panel de Sensores:**
- **12 Botones de Sensor**: Organizados en grid 3x4 para acceso rápido
- **Habilitación Dinámica**: Solo sensores disponibles están activos
- **Identificación Visual**: Iconos distintivos para cada tipo de sensor

**Área de Trabajo Central:**
- **Widget de Bienvenida**: Información de inicio y guías rápidas
- **Área de Sensor Activa**: Carga dinámicamente la interfaz del sensor seleccionado
- **Área de Estado**: Muestra información de sensor actual y estado de conexión

**Panel Inferior:**
- **Botón de Log**: Acceso al sistema de logging y debugging
- **Botón Reset**: Reinicia la aplicación al estado inicial
- **Información de Sistema**: Versión, estado de memoria y rendimiento

### Elementos de Interfaz

#### Campo de Dirección IP
- **Formato**: Validación automática de IPv4 (ej: 192.168.1.100)
- **Placeholder**: Texto de ayuda "Ingrese IP del ESP32"
- **Validación**: Comprobación en tiempo real con feedback visual
- **Historial**: Dropdown con IPs utilizadas recientemente

#### Botones de Sensor
Cada botón de sensor incluye:
- **Icono Distintivo**: Representación visual del tipo de sensor
- **Texto Descriptivo**: Nombre claro del módulo de sensor
- **Estado Visual**: Habilitado/deshabilitado según conectividad
- **Tooltip**: Información adicional al pasar el mouse

**Lista de Sensores Disponibles:**
1. **SENSORA_ANGLE_ARM** - Medición de ángulos con brazo mecánico
2. **SENSORA_BRIGHTNESS** - Sensor de luminosidad ambiente
3. **SENSORA_CAPACITIVE** - Detección capacitiva de proximidad
4. **SENSORA_COLOR_CNY** - Sensor de color CNY70
5. **SENSORA_COLOR_TCS** - Sensor de color TCS3200
6. **SENSORA_GAS_REGULATION** - Control y monitoreo de gases
7. **SENSORA_INFRARED** - Detección infrarroja
8. **SENSORA_IR_STEERING** - Control direccional IR
9. **SENSORA_OPTICAL_SPEED** - Medición de velocidad óptica
10. **SENSORA_SIMPLE_ANGLE** - Medición angular simple
11. **SENSORA_THERMOREGULATION** - Control térmico avanzado
12. **SENSORA_ULTRASONIC** - Medición ultrasónica de distancia

#### Indicadores de Estado
- **LED de Conexión**: Verde = conectado, Rojo = desconectado, Amarillo = conectando
- **Barra de Estado**: Información textual del estado actual
- **Contador de Datos**: Muestra cantidad de mediciones recibidas
- **Indicador de Latencia**: Tiempo de respuesta de comunicación

---

## 4. Conexión con ESP32

### Procedimiento de Conexión

#### Paso 1: Preparación
1. **Verificar** que el ESP32 esté encendido y conectado a la red
2. **Obtener** la dirección IP del ESP32 (consultar router o monitor serie)
3. **Confirmar** que el ESP32 ejecuta el firmware SensoraCore correcto
4. **Verificar** conectividad de red mediante ping

#### Paso 2: Configuración en la Aplicación
1. **Introducir** la dirección IP del ESP32 en el campo correspondiente
2. **Verificar** que el formato IP sea válido (aparecerá borde verde)
3. **Hacer clic** en el botón "Conectar"
4. **Observar** el indicador de estado durante el proceso de conexión

#### Paso 3: Verificación de Conexión
1. **Esperar** la confirmación visual (LED verde de conexión)
2. **Verificar** que los botones de sensor se habiliten automáticamente
3. **Comprobar** en el log que aparezca "Conexión exitosa con ESP32"
4. **Probar** selección de sensor para validar comunicación bidireccional

### Solución de Problemas de Conexión

#### Error: "IP no válida"
- **Causa**: Formato de IP incorrecto
- **Solución**: Verificar formato IPv4 (ej: 192.168.1.100)
- **Ejemplo válido**: 192.168.4.1 (red AP del ESP32)

#### Error: "No se puede conectar al ESP32"
- **Verificar conectividad de red**:
  ```bash
  ping 192.168.1.100
  ```
- **Comprobar puerto 8080**:
  ```bash
  telnet 192.168.1.100 8080
  ```
- **Revisar firewall** del sistema y router

#### Error: "Timeout de conexión"
- **Aumentar timeout** en configuración avanzada
- **Verificar carga** del ESP32 (puede estar ocupado)
- **Reiniciar** el ESP32 y volver a intentar

#### Error: "Respuesta inesperada del ESP32"
- **Verificar versión** del firmware ESP32
- **Comprobar integridad** de la comunicación
- **Reiniciar** tanto la aplicación como el ESP32

### Configuración Avanzada de Red

**Implementación del Cliente TCP**:
```python
class ESP32Client:
    def __init__(self, esp32_ip, port=8080):
        self.esp32_ip = esp32_ip
        self.port = port
    
    def send_command(self, command):
        # Socket TCP con timeout de 3 segundos
        # Codificación UTF-8 para comandos
        # Buffer de recepción: 1024 bytes
        # Manejo de excepciones: return "ERROR: {e}"
```

#### Red de Punto de Acceso (AP Mode)
```python
# Configuración típica para ESP32 en modo AP
SSID: "SensoraCore_ESP32"
Password: "12345678"
IP: 192.168.4.1
Puerto: 8080
```

#### Red de Infraestructura (Station Mode)
```python
# Configuración para red WiFi existente
SSID: "Red_Laboratorio"
Password: "clave_segura"
IP: DHCP asignada automáticamente
Puerto: 8080
```

#### Configuración de Red Industrial
- **VLAN dedicada** para instrumentación
- **Direccionamiento estático** para dispositivos críticos
- **QoS configurado** para priorizar tráfico de instrumentación
- **Redundancia de red** con bonding de interfaces

---

## 5. Selección y Uso de Sensores

### Procedimiento General

#### Selección de Sensor
1. **Asegurar** conexión activa con ESP32 (LED verde)
2. **Hacer clic** en el botón del sensor deseado
3. **Esperar** carga de la interfaz específica del sensor
4. **Verificar** que la información del sensor aparezca correctamente

#### Cambio de Sensor
1. **Hacer clic** en un botón de sensor diferente
2. **Confirmar** automáticamente la limpieza del sensor anterior
3. **Esperar** carga de la nueva interfaz
4. **Verificar** funcionamiento del nuevo sensor

**Proceso Técnico de Cambio de Sensor**:
La función `sensorSeleccionado(sensor_id)` ejecuta la siguiente secuencia:
1. **Limpieza automática**: `_cleanup_active_sensors()` detiene procesos activos
2. **Ocultación de welcome**: `welcome_widget.setVisible(False)`
3. **Gestión de layout**: Eliminación de widgets con `takeAt(0)` y `deleteLater()`
4. **Carga de widget específico**: Instanciación de lógica correspondiente
5. **Verificación de integridad**: Test con `objectName()` y recreación si falla
6. **Fallback automático**: `reconstruirSensorUi()` si hay errores de widget

### Sensores Específicos

#### SENSORA_BRIGHTNESS - Sensor de Luminosidad
**Descripción**: Medición de intensidad lumínica ambiente con sensor LDR calibrado

**Controles Disponibles**:
- **Calibración**: Ajuste de sensibilidad y offset
- **Muestreo**: Configuración de frecuencia de lectura
- **Gráfico en Tiempo Real**: Visualización de tendencias lumínicas
- **Alertas**: Configuración de umbrales de luminosidad

**Procedimiento de Uso**:
1. Seleccionar SENSORA_BRIGHTNESS
2. Configurar frecuencia de muestreo (1-100 Hz)
3. Calibrar según condiciones de iluminación
4. Iniciar monitoreo y observar gráfico
5. Configurar alertas si es necesario

#### SENSORA_THERMOREGULATION - Control Térmico
**Descripción**: Sistema avanzado de control de temperatura con PID integrado

**Controles Disponibles**:
- **Setpoint**: Temperatura objetivo (0-100°C)
- **PID**: Configuración de parámetros proporcional, integral, derivativo
- **Histéresis**: Control de banda muerta para evitar oscilaciones
- **Gráfico de Control**: Visualización de temperatura y salida del controlador

**Procedimiento de Uso**:
1. Seleccionar SENSORA_THERMOREGULATION
2. Establecer temperatura objetivo
3. Configurar parámetros PID según sistema térmico
4. Activar control automático
5. Monitorear estabilidad y ajustar si es necesario

#### SENSORA_ULTRASONIC - Medición de Distancia
**Descripción**: Sensor ultrasónico HC-SR04 para medición precisa de distancias

**Controles Disponibles**:
- **Rango**: Configuración de distancia máxima (2-400 cm)
- **Promediado**: Filtro digital para reducir ruido
- **Calibración**: Compensación de temperatura y humedad
- **Detección de Objetos**: Configuración de umbrales

**Procedimiento de Uso**:
1. Seleccionar SENSORA_ULTRASONIC
2. Configurar rango de medición esperado
3. Activar filtro de promediado si hay ruido
4. Iniciar medición continua
5. Registrar datos o configurar alertas de proximidad

### Funciones Comunes a Todos los Sensores

#### Exportación de Datos
- **Formato CSV**: Compatible con Excel y análisis estadístico
- **Timestamp**: Marca de tiempo precisa para cada medición
- **Metadatos**: Información de configuración y calibración
- **Compresión**: Archivos ZIP para datasets extensos

#### Calibración y Configuración
- **Asistente de Calibración**: Guía paso a paso para cada sensor
- **Perfiles de Configuración**: Guardado y carga de configuraciones típicas
- **Validación de Rango**: Verificación automática de parámetros válidos
- **Backup de Configuración**: Respaldo automático de configuraciones

#### Visualización en Tiempo Real
- **Gráficos Interactivos**: Zoom, pan y selección de rangos
- **Múltiples Series**: Comparación de señales simultáneas
- **Estadísticas en Vivo**: Media, desviación estándar, mín/máx
- **Exportación de Gráficos**: PNG, PDF, SVG para reportes

---

## 6. Sistema de Logging

### Acceso al Sistema de Logging

#### Apertura de Ventana de Log
1. **Hacer clic** en el botón "Log" en la parte inferior de la ventana principal
2. **Observar** apertura de ventana independiente de logging
3. **Redimensionar** la ventana según necesidades de visualización
4. **Configurar** filtros de mensaje si es necesario

#### Cierre de Ventana de Log
1. **Hacer clic** nuevamente en el botón "Log" para alternar visibilidad
2. **Usar** la X de la ventana para cerrar manualmente
3. **El logging** continúa funcionando en segundo plano

### Tipos de Mensajes

#### Mensajes de Información (INFO)
- **Conexiones exitosas** con ESP32
- **Cambios de sensor** realizados correctamente
- **Inicio y fin** de procesos de calibración
- **Estados de sistema** y confirmaciones de operación

#### Mensajes de Advertencia (WARNING)
- **Timeouts de comunicación** no críticos
- **Valores fuera de rango** esperado pero válidos
- **Reconexiones automáticas** exitosas
- **Configuraciones subóptimas** pero funcionales

#### Mensajes de Error (ERROR)
- **Fallos de conexión** con ESP32
- **Errores de comunicación** críticos
- **Fallos de validación** de datos
- **Excepciones de sistema** capturadas

#### Mensajes de Debug (DEBUG)
- **Trazas de función** para desarrollo
- **Estados internos** de variables críticas
- **Secuencias de comandos** enviados/recibidos
- **Información detallada** de objetos

### Interpretación de Logs

#### Formato de Mensajes
```
[TIMESTAMP] [NIVEL] [MÓDULO] - Descripción del mensaje
[2024-01-15 14:30:25] [INFO] [ESP32Client] - Conexión establecida con 192.168.1.100:8080
[2024-01-15 14:30:26] [WARNING] [SensorManager] - Timeout en respuesta de sensor, reintentando...
[2024-01-15 14:30:27] [ERROR] [UltrasonicSensor] - Valor de distancia fuera de rango: 450 cm
```

#### Secuencias Típicas de Operación

**Conexión Exitosa**:
```
[INFO] [MainWindow] - Iniciando conexión con ESP32...
[INFO] [ESP32Client] - Validando dirección IP: 192.168.1.100
[INFO] [ESP32Client] - Estableciendo socket TCP...
[INFO] [ESP32Client] - Enviando comando LED_ON para handshake
[INFO] [ESP32Client] - Respuesta recibida: LED_ON_OK
[INFO] [MainWindow] - Conexión exitosa, habilitando sensores
```

**Cambio de Sensor**:
```
[INFO] [SensorManager] - Limpiando sensor activo anterior
[INFO] [BrightnessSensor] - Deteniendo proceso de monitoreo
[INFO] [BrightnessSensor] - Liberando recursos de interfaz
[INFO] [SensorManager] - Cargando SENSORA_ULTRASONIC
[INFO] [UltrasonicSensor] - Inicializando interfaz de usuario
[INFO] [UltrasonicSensor] - Configuración cargada exitosamente
```

### Uso del Log para Diagnóstico

#### Diagnóstico de Problemas de Conexión
1. **Buscar** mensajes relacionados con "ESP32Client" o "conexión"
2. **Identificar** último mensaje de estado antes del fallo
3. **Verificar** secuencia de comandos enviados/recibidos
4. **Analizar** códigos de error de socket o timeout

#### Diagnóstico de Problemas de Sensor
1. **Filtrar** mensajes por nombre del sensor problemático
2. **Verificar** secuencia de inicialización del sensor
3. **Buscar** errores de validación de datos o comunicación
4. **Analizar** patrones de error para identificar causas recurrentes

#### Análisis de Rendimiento
1. **Observar** timestamps para identificar operaciones lentas
2. **Buscar** mensajes de warning relacionados con timeouts
3. **Analizar** frecuencia de reconexiones automáticas
4. **Verificar** uso de memoria y recursos del sistema

---

## 7. Solución de Problemas

### Problemas Comunes de Conexión

#### Problema: "No se puede conectar al ESP32"

**Síntomas**:
- Botón "Conectar" no responde o muestra error
- LED de conexión permanece rojo
- Mensaje de timeout en el log

**Diagnóstico**:
1. **Verificar conectividad de red**:
   ```bash
   ping [IP_del_ESP32]
   ```
2. **Comprobar puerto específico**:
   ```bash
   telnet [IP_del_ESP32] 8080
   ```
3. **Revisar logs** para identificar punto de fallo específico

**Soluciones**:
1. **Verificar alimentación** del ESP32
2. **Reiniciar el ESP32** desconectando y conectando
3. **Comprobar configuración WiFi** del ESP32
4. **Verificar firewall** del sistema operativo
5. **Cambiar a red directa** (hotspot del ESP32)

#### Problema: "Conexión se pierde frecuentemente"

**Síntomas**:
- Desconexiones aleatorias durante operación
- Reconexiones automáticas frecuentes
- Datos perdidos o mediciones incompletas

**Diagnóstico**:
1. **Analizar calidad de señal WiFi**
2. **Verificar carga de la red** (otros dispositivos)
3. **Comprobar alimentación estable** del ESP32
4. **Revisar logs** para patrones de desconexión

**Soluciones**:
1. **Acercar ESP32 al router** para mejor señal
2. **Usar cable Ethernet** si está disponible
3. **Configurar canal WiFi** menos congestionado
4. **Implementar UPS** para alimentación estable
5. **Aumentar timeout** de conexión en configuración avanzada

### Problemas de Interfaz de Usuario

#### Problema: "Aplicación se congela o no responde"

**Síntomas**:
- Interfaz no responde a clics
- Ventana se marca como "No responde" en Windows
- Gráficos dejan de actualizarse

**Diagnóstico**:
1. **Verificar uso de CPU** en administrador de tareas
2. **Comprobar uso de memoria** RAM disponible
3. **Revisar logs** para excepciones no manejadas
4. **Verificar conexión de red** estable

**Soluciones**:
1. **Cerrar aplicaciones** innecesarias para liberar memoria
2. **Reiniciar la aplicación** SensoraCore
3. **Verificar drivers** de tarjeta gráfica actualizados
4. **Cambiar a sensor menos intensivo** en recursos
5. **Reiniciar el sistema** si el problema persiste

#### Problema: "Botones de sensor no se habilitan"

**Síntomas**:
- Botones permanecen grises después de conectar
- No es posible seleccionar ningún sensor
- LED de conexión muestra verde pero sensores inactivos

**Diagnóstico**:
1. **Verificar respuesta** del ESP32 en logs
2. **Comprobar comando LED_ON** fue exitoso
3. **Revisar integridad** de widgets de interfaz

**Soluciones**:
1. **Hacer clic en "Reset"** para reinicializar interfaz
2. **Desconectar y reconectar** al ESP32
3. **Reiniciar la aplicación** completamente
4. **Verificar versión** de firmware del ESP32

### Problemas Específicos de Sensores

#### Problema: "Datos de sensor erróneos o fuera de rango"

**Síntomas**:
- Mediciones imposibles físicamente
- Valores constantes o que no cambian
- Gráficos muestran ruido excesivo

**Diagnóstico**:
1. **Verificar calibración** del sensor
2. **Comprobar conexiones físicas** en ESP32
3. **Revisar configuración** de rango del sensor
4. **Analizar condiciones ambientales**

**Soluciones**:
1. **Recalibrar el sensor** usando procedimiento estándar
2. **Verificar alimentación** del sensor (3.3V o 5V según especificación)
3. **Comprobar integridad** de cables y conexiones
4. **Ajustar configuración** de rango y sensibilidad
5. **Aislar de interferencias** electromagnéticas

#### Problema: "Sensor no responde o timeout constante"

**Síntomas**:
- Mensajes de timeout en el log
- Interfaz del sensor no muestra datos
- Comandos no ejecutan respuesta del ESP32

**Diagnóstico**:
1. **Verificar sensor** está conectado físicamente
2. **Comprobar pin assignment** en firmware ESP32
3. **Revisar alimentación** del sensor específico
4. **Analizar logs** de comunicación detallados

**Soluciones**:
1. **Verificar cableado** físico del sensor
2. **Reiniciar ESP32** para reinicializar hardware
3. **Comprobar compatibilidad** del sensor con ESP32
4. **Revisar firmware** para soporte del sensor específico
5. **Contactar soporte técnico** si persiste el problema

### Problemas de Rendimiento

#### Problema: "Aplicación lenta o respuesta tardía"

**Síntomas**:
- Clicks tardan en registrarse
- Gráficos se actualizan lentamente
- Cambio de sensores toma mucho tiempo

**Diagnóstico**:
1. **Verificar recursos** del sistema (CPU, RAM)
2. **Comprobar carga de red** y latencia
3. **Revisar procesos** en segundo plano
4. **Analizar logs** para operaciones lentas

**Soluciones**:
1. **Cerrar aplicaciones** innecesarias
2. **Reducir frecuencia** de muestreo de sensores
3. **Optimizar configuración** de gráficos
4. **Considerar hardware** más potente
5. **Contactar soporte** para optimizaciones específicas

### Herramientas de Diagnóstico

#### Verificación de Red
```bash
# Verificar conectividad básica
ping -t [IP_del_ESP32]

# Comprobar puerto específico
telnet [IP_del_ESP32] 8080

# Escanear puertos abiertos
nmap -p 8080 [IP_del_ESP32]

# Verificar latencia de red
tracert [IP_del_ESP32]
```

#### Monitoreo de Sistema
- **Administrador de Tareas** (Windows): Verificar uso de CPU y memoria
- **Activity Monitor** (macOS): Monitorear recursos del sistema
- **htop** (Linux): Análisis detallado de procesos y recursos
- **Wireshark**: Captura de tráfico de red para análisis avanzado

#### Logs de Sistema
- **Windows**: Event Viewer para errores del sistema
- **Linux**: journalctl para logs del sistema
- **macOS**: Console app para logs de aplicación
- **SensoraCore**: Log interno para debugging específico

---

## 8. Especificaciones Técnicas

### Arquitectura del Software

#### Lenguajes y Frameworks
- **Lenguaje Principal**: Python 3.8+ con type hints
- **GUI Framework**: PySide6 (Qt 6.x) para interfaz nativa
- **Networking**: Socket TCP nativo de Python
- **Threading**: QThread para operaciones asíncronas
- **Packaging**: PyInstaller para distribución standalone

#### Componentes Arquitecturales

**Capa de Presentación**:
- Interfaz gráfica modular con carga dinámica de widgets
- Sistema de splash screen con indicadores de progreso
- Gestión de eventos Qt con signals y slots
- Responsive design para diferentes resoluciones

**Capa de Lógica de Negocio**:
- Gestión centralizada de estado de aplicación
- Sistema de plugins para módulos de sensores
- Validación de datos y configuraciones
- Algoritmos de procesamiento de señales

**Capa de Comunicación**:
- Cliente TCP robusto con manejo de reconexión
- Protocolo de comandos personalizado para ESP32
- Gestión de timeouts y errores de red
- Serialización de datos para transmisión

**Capa de Datos**:
- Almacenamiento de configuraciones en archivos locales
- Cache de datos en memoria para rendimiento
- Exportación a formatos estándar (CSV, JSON)
- Logging estructurado para auditoría

### Protocolos de Comunicación

#### Protocolo TCP/IP con ESP32
```
Puerto: 8080
Formato: ASCII text commands
Terminador: \n (newline)
Timeout: 5 segundos (configurable)
Codificación: UTF-8
```

#### Comandos Estándar
```
LED_ON          - Comando de handshake, enciende LED del ESP32
LED_OFF         - Apaga LED del ESP32
GET_STATUS      - Obtiene estado general del microcontrolador
RESET_SYSTEM    - Reinicia el ESP32
```

#### Comandos por Sensor
Cada sensor tiene comandos específicos:
```
BRIGHTNESS_START    - Inicia medición de luminosidad
BRIGHTNESS_STOP     - Detiene medición
ULTRASONIC_MEASURE  - Solicita medición de distancia
THERMOSTAT_SET_TEMP - Configura temperatura objetivo
```

### Requisitos de Hardware

#### Especificaciones Mínimas del PC
```
CPU: Dual-core 2.0 GHz (x86_64)
RAM: 4 GB DDR3
Almacenamiento: 2 GB disponible
GPU: Integrada compatible con OpenGL 3.0
Red: WiFi 802.11n o Ethernet 100Mbps
USB: Puerto USB 2.0 para configuración
```

#### Especificaciones Recomendadas del PC
```
CPU: Quad-core 3.0 GHz+ (Intel i5, AMD Ryzen 5)
RAM: 16 GB DDR4
Almacenamiento: SSD 500 GB NVMe
GPU: Dedicada con 2GB VRAM, OpenGL 4.0+
Red: Gigabit Ethernet + WiFi 802.11ac
USB: Múltiples puertos USB 3.0
```

#### Especificaciones del ESP32
```
Microcontrolador: ESP32-WROOM-32
CPU: Dual-core Tensilica Xtensa LX6 @ 240MHz
RAM: 520 KB SRAM
Flash: 4 MB (mínimo)
WiFi: 802.11 b/g/n 2.4GHz
Bluetooth: v4.2 BR/EDR y BLE
GPIO: 30 pines programables
ADC: 12-bit, múltiples canales
```

### Red de Comunicación

#### Topologías Soportadas

**Red de Infraestructura (Station Mode)**:
```
Internet ←→ Router WiFi ←→ PC + ESP32
Ventajas: Acceso a internet, gestión centralizada
Desventajas: Dependencia del router, configuración más compleja
```

**Red Punto a Punto (AP Mode)**:
```
PC ←→ ESP32 (como Access Point)
Ventajas: Independiente, configuración simple
Desventajas: Sin acceso a internet, limitado a un PC
```

**Red Mixta (Recommended)**:
```
Internet ←→ Router ←→ Switch ←→ PC
                            ←→ ESP32
Ventajas: Máxima flexibilidad y robustez
Desventajas: Requiere switch adicional
```

#### Configuración de Red Recomendada
```
Subred: 192.168.1.0/24
PC: 192.168.1.10 (estática)
ESP32: 192.168.1.100 (estática)
Gateway: 192.168.1.1
DNS: 8.8.8.8, 8.8.4.4
VLAN: Dedicada para instrumentación (opcional)
```

### Rendimiento y Escalabilidad

#### Métricas de Rendimiento
- **Tiempo de inicio**: < 5 segundos en hardware recomendado
- **Latencia de comando**: < 100ms en red local
- **Frecuencia de muestreo**: Hasta 100 Hz por sensor
- **Throughput de datos**: 1 MB/s por canal de sensor
- **Tiempo de reconexión**: < 2 segundos automático

#### Límites de Escalabilidad
- **Sensores simultáneos**: 11 (limitado por ESP32)
- **Sesiones concurrentes**: 1 PC por ESP32
- **Duración de sesión**: Ilimitada (24/7 operation)
- **Almacenamiento de datos**: Limitado por espacio en disco
- **Red de ESP32s**: 254 dispositivos por subred

#### Optimizaciones Implementadas
- Threading asíncrono para UI no bloqueante
- Cache de interfaces para carga rápida
- Compresión de datos para transferencia eficiente
- Garbage collection optimizado para memoria
- Pool de conexiones para múltiples ESP32s (futuro)

---

## 9. Mantenimiento

### Mantenimiento Preventivo

#### Actualizaciones de Software

**Frecuencia Recomendada**: Mensual o según necesidades críticas

**Procedimiento de Actualización**:
1. **Hacer backup** de configuraciones actuales
2. **Cerrar completamente** la aplicación SensoraCore
3. **Descargar** nueva versión del repositorio oficial
4. **Ejecutar instalador** o sobrescribir archivos
5. **Verificar funcionamiento** con test de conectividad
6. **Restaurar configuraciones** personalizadas si es necesario

**Verificación Post-Actualización**:
```bash
# Verificar versión instalada
SensoraCore_Beta1.0.exe --version

# Test de conectividad básica
ping [IP_del_ESP32]

# Verificar integridad de archivos
dir /s SensoraCore\  # Windows
ls -la SensoraCore/  # Linux/macOS
```

#### Limpieza de Sistema

**Limpieza Semanal**:
- **Limpiar logs** antiguos (> 30 días)
- **Verificar espacio** en disco disponible
- **Comprobar actualizaciones** de drivers de red
- **Reiniciar aplicación** para liberación de memoria

**Limpieza Mensual**:
- **Desfragmentar disco** (Windows, HDD)
- **Actualizar sistema operativo** con parches de seguridad
- **Verificar antivirus** y exclusiones para SensoraCore
- **Revisar configuración** de firewall

**Comandos de Limpieza**:
```bash
# Limpiar logs antiguos (Windows)
forfiles /p "C:\SensoraCore\logs" /s /m *.log /d -30 /c "cmd /c del @path"

# Limpiar logs antiguos (Linux)
find /home/user/SensoraCore/logs -name "*.log" -mtime +30 -delete

# Verificar espacio en disco
df -h  # Linux/macOS
dir C: # Windows
```

#### Backup y Recuperación

**Elementos a Respaldar**:
- Configuraciones de sensores: `config/sensors/*.json`
- Perfiles de calibración: `config/calibration/*.cal`
- Logs importantes: `logs/critical/*.log`
- Datos experimentales: `data/*.csv`
- Configuración de red: `config/network.conf`

**Procedimiento de Backup Automatizado**:
```bash
#!/bin/bash
# Script de backup diario
BACKUP_DIR="/backup/sensoracore/$(date +%Y%m%d)"
mkdir -p $BACKUP_DIR

# Copiar configuraciones
cp -r config/ $BACKUP_DIR/
cp -r data/ $BACKUP_DIR/
cp logs/critical/*.log $BACKUP_DIR/

# Comprimir backup
tar -czf $BACKUP_DIR.tar.gz $BACKUP_DIR
rm -rf $BACKUP_DIR

echo "Backup completado: $BACKUP_DIR.tar.gz"
```

**Procedimiento de Restauración**:
1. **Detener aplicación** SensoraCore
2. **Extraer backup** al directorio de instalación
3. **Verificar permisos** de archivos restaurados
4. **Iniciar aplicación** y verificar configuraciones
5. **Probar conectividad** con ESP32

### Mantenimiento Correctivo

#### Diagnóstico de Problemas

**Herramientas de Diagnóstico Integradas**:
- **Sistema de logging** detallado con niveles configurables
- **Monitor de memoria** en tiempo real
- **Test de conectividad** automático
- **Validador de configuraciones** con reparación automática

**Diagnóstico de Red**:
```bash
# Test completo de conectividad
ping -c 4 [IP_ESP32]                    # Conectividad básica
nmap -p 8080 [IP_ESP32]                # Puerto específico
traceroute [IP_ESP32]                   # Ruta de red
netstat -an | grep 8080                # Puerto local
```

**Diagnóstico de Sistema**:
```bash
# Verificar recursos del sistema
top                          # Linux
Get-Process | Sort CPU       # Windows PowerShell
Activity Monitor             # macOS

# Verificar logs del sistema
journalctl -u sensoracore    # Linux systemd
Event Viewer                 # Windows
Console.app                  # macOS
```

#### Reparación de Problemas Comunes

**Problema: Base de datos corrupta**
```bash
# Verificar integridad
sqlite3 sensoracore.db "PRAGMA integrity_check;"

# Reparar si es necesario
sqlite3 sensoracore.db ".dump" | sqlite3 sensoracore_new.db
mv sensoracore_new.db sensoracore.db
```

**Problema: Configuración corrupta**
```bash
# Resetear a configuración de fábrica
rm -rf config/
cp -r config_default/ config/

# Verificar sintaxis JSON
python -m json.tool config/sensors/brightness.json
```

**Problema: Permisos de archivo**
```bash
# Linux/macOS
chown -R $USER:$USER ~/SensoraCore/
chmod -R 755 ~/SensoraCore/
chmod -R 644 ~/SensoraCore/config/*.json

# Windows (PowerShell como Administrador)
icacls C:\SensoraCore /grant Users:F /T
```

### Monitoreo Continuo

#### Métricas de Salud del Sistema

**Indicadores Clave de Rendimiento (KPIs)**:
- **Uptime de aplicación**: % tiempo operativo sin fallos
- **Latencia de comunicación**: Tiempo promedio de respuesta ESP32
- **Tasa de éxito de conexión**: % conexiones exitosas
- **Uso de memoria**: Consumo RAM en operación continua
- **Precisión de sensores**: Desviación de valores de referencia

**Implementación de Monitoreo**:
```python
# Sistema de métricas integrado
class SystemMonitor:
    def collect_metrics(self):
        metrics = {
            'uptime': self.get_uptime(),
            'memory_usage': self.get_memory_usage(),
            'network_latency': self.measure_latency(),
            'connection_success_rate': self.calc_success_rate(),
            'sensor_accuracy': self.validate_sensors()
        }
        return metrics
```

#### Alertas y Notificaciones

**Configuración de Alertas**:
- **Memoria > 90%**: Advertencia de recursos limitados
- **Latencia > 500ms**: Problema de red detectado
- **Fallos de conexión > 5**: ESP32 posiblemente desconectado
- **Sensor fuera de rango**: Posible fallo de hardware
- **Espacio en disco < 1GB**: Backup y limpieza necesarios

**Canales de Notificación**:
- **Alertas visuales** en interfaz de usuario
- **Logs estructurados** para análisis automatizado
- **Email automático** para alertas críticas (configuración avanzada)
- **Integración SNMP** para sistemas de monitoreo empresariales

#### Mantenimiento Predictivo

**Análisis de Tendencias**:
- **Degradación de rendimiento** gradual
- **Aumento de latencia** de red progresivo
- **Frecuencia creciente** de reconexiones
- **Deriva de calibración** de sensores

**Herramientas de Análisis**:
```python
# Análisis de tendencias automático
def analyze_performance_trend(metrics_history):
    import numpy as np
    from scipy import stats
    
    # Detectar tendencias en latencia
    latencies = [m['network_latency'] for m in metrics_history]
    slope, intercept, r_value, p_value, std_err = stats.linregress(
        range(len(latencies)), latencies
    )
    
    if slope > 0.1 and p_value < 0.05:
        return "WARNING: Latencia en aumento, revisar red"
    
    return "OK: Rendimiento estable"
```

---

## 10. Soporte Técnico

### Canales de Soporte

#### Soporte Interno (Autoservicio)

**Documentación Integrada**:
- **Manual de usuario** completo (este documento)
- **Documentación técnica** de APIs y protocolos
- **Base de conocimientos** con problemas comunes
- **Tutoriales interactivos** para operaciones básicas

**Herramientas de Autodiagnóstico**:
- **Sistema de logs** con búsqueda y filtrado
- **Test de conectividad** automático
- **Validador de configuraciones** con sugerencias
- **Monitor de salud** del sistema en tiempo real

#### Soporte Comunitario

**Recursos Disponibles**:
- **Foro de usuarios** para intercambio de experiencias
- **Wiki colaborativa** con trucos y configuraciones
- **Repositorio de ejemplos** de configuración
- **Canal de chat** para soporte entre usuarios

**Contribución a la Comunidad**:
- **Reportar bugs** con información detallada
- **Compartir configuraciones** exitosas
- **Documentar casos de uso** específicos
- **Contribuir mejoras** al código fuente

#### Soporte Profesional

**Niveles de Soporte**:

**Básico (Email)**:
- Tiempo de respuesta: 48-72 horas
- Soporte para instalación y configuración básica
- Resolución de problemas comunes documentados
- Actualizaciones y parches de seguridad

**Estándar (Email + Chat)**:
- Tiempo de respuesta: 24 horas
- Soporte para configuraciones avanzadas
- Análisis de logs y diagnóstico remoto
- Capacitación básica para usuarios

**Premium (Dedicado)**:
- Tiempo de respuesta: 4-8 horas
- Soporte telefónico directo
- Acceso remoto para diagnóstico avanzado
- Desarrollo de características personalizadas
- SLA de uptime y rendimiento

### Procedimiento de Reporte de Problemas

#### Información Requerida

**Información del Sistema**:
```
Versión de SensoraCore: [ej. Beta 1.0]
Sistema Operativo: [ej. Windows 11 Pro 64-bit]
Hardware PC: [CPU, RAM, GPU]
Modelo ESP32: [ej. ESP32-WROOM-32]
Firmware ESP32: [versión]
Configuración de red: [IP, SSID, topología]
```

**Información del Problema**:
- **Descripción detallada** del problema observado
- **Pasos para reproducir** el problema
- **Comportamiento esperado** vs comportamiento actual
- **Frecuencia** del problema (siempre, intermitente, específico)
- **Impacto** en la operación (crítico, moderado, menor)

**Archivos de Soporte**:
- **Logs completos** del período del problema
- **Configuraciones** de sensor involucrado
- **Screenshots** de mensajes de error
- **Archivos de datos** afectados (si aplica)
- **Configuración de red** y firewall

#### Template de Reporte
```
TÍTULO: [Breve descripción del problema]

VERSIÓN: SensoraCore Beta 1.0
SO: Windows 11 Pro 64-bit
ESP32: WROOM-32 con firmware v1.0

DESCRIPCIÓN:
[Descripción detallada del problema]

PASOS PARA REPRODUCIR:
1. [Paso 1]
2. [Paso 2]
3. [Paso 3]

COMPORTAMIENTO ESPERADO:
[Lo que debería suceder]

COMPORTAMIENTO ACTUAL:
[Lo que realmente sucede]

LOGS RELEVANTES:
[Pegar logs importantes aquí]

ARCHIVOS ADJUNTOS:
- screenshot_error.png
- logs_20240115.txt
- config_brightness.json
```

### Base de Conocimientos

#### Problemas Frecuentes y Soluciones

**P1: ESP32 no responde después de funcionar correctamente**
- **Causa**: Watchdog reset o sobrecalentamiento
- **Solución**: Verificar alimentación estable, mejorar ventilación
- **Prevención**: Monitor térmico, UPS para alimentación

**P2: Mediciones de sensor inconsistentes**
- **Causa**: Interferencia electromagnética o calibración perdida
- **Solución**: Recalibrar sensor, mejorar blindaje de cables
- **Prevención**: Revisión periódica de calibración

**P3: Aplicación consume mucha memoria**
- **Causa**: Memory leaks en operación continua
- **Solución**: Reiniciar aplicación, verificar versión actualizada
- **Prevención**: Reinicio programado cada 24 horas

**P4: Conectividad intermitente**
- **Causa**: Saturación de red WiFi o interferencia
- **Solución**: Cambiar canal WiFi, usar cable Ethernet
- **Prevención**: Red dedicada para instrumentación

#### Códigos de Error Comunes

```
ERROR_001: Connection timeout
- Descripción: Timeout al conectar con ESP32
- Acción: Verificar IP, red y firewall

ERROR_002: Invalid sensor response
- Descripción: Respuesta inesperada del sensor
- Acción: Reiniciar ESP32, verificar firmware

ERROR_003: Widget creation failed
- Descripción: Fallo al crear interfaz de sensor
- Acción: Reiniciar aplicación, verificar integridad

ERROR_004: Configuration file corrupt
- Descripción: Archivo de configuración dañado
- Acción: Restaurar configuración de fábrica

ERROR_005: Memory allocation failed
- Descripción: Insuficiente memoria disponible
- Acción: Cerrar aplicaciones, reiniciar sistema
```

### Actualización y Versionado

#### Política de Versiones

**Versionado Semántico (MAJOR.MINOR.PATCH)**:
- **MAJOR**: Cambios incompatibles de API
- **MINOR**: Nuevas funcionalidades compatibles
- **PATCH**: Correcciones de bugs y mejoras

**Tipos de Release**:
- **Alpha**: Desarrollo temprano, testing interno
- **Beta**: Testing público, funcionalidades completas
- **RC (Release Candidate)**: Pre-release, casi lista para producción
- **Stable**: Versión de producción, totalmente probada

#### Ciclo de Actualizaciones

**Actualizaciones de Seguridad**: Inmediatas (24-48 horas)
**Correcciones de Bugs**: Semanales o según criticidad
**Nuevas Funcionalidades**: Mensuales en versiones minor
**Versiones Major**: Anuales con planificación extensa

**Comunicación de Actualizaciones**:
- **Notificaciones in-app** para actualizaciones críticas
- **Email newsletter** para usuarios registrados
- **Release notes** detalladas en repositorio
- **Webinars** para cambios importantes

---

## 11. Apéndices

### Apéndice A: Configuraciones de Red Detalladas

#### Configuración para Red Empresarial
```json
{
  "network_config": {
    "mode": "infrastructure",
    "subnet": "10.0.100.0/24",
    "vlan_id": 100,
    "pc_ip": "10.0.100.10",
    "esp32_ip": "10.0.100.100",
    "gateway": "10.0.100.1",
    "dns_primary": "10.0.100.1",
    "dns_secondary": "8.8.8.8",
    "security": {
      "encryption": "WPA2-Enterprise",
      "certificate": "/etc/ssl/certs/company.crt",
      "firewall_rules": [
        "allow 8080/tcp from 10.0.100.0/24",
        "deny all from any"
      ]
    }
  }
}
```

#### Configuración para Laboratorio Educativo
```json
{
  "network_config": {
    "mode": "access_point",
    "ssid": "SensoraCore_Lab",
    "password": "Lab2024!",
    "channel": 11,
    "subnet": "192.168.4.0/24",
    "ap_ip": "192.168.4.1",
    "dhcp_range": {
      "start": "192.168.4.10",
      "end": "192.168.4.50"
    },
    "security": {
      "encryption": "WPA2-PSK",
      "isolation": true,
      "max_clients": 10
    }
  }
}
```

### Apéndice B: Scripts de Automatización

#### Script de Inicio Automático (Windows)
```batch
@echo off
REM SensoraCore Auto-Start Script
echo Iniciando SensoraCore...

REM Verificar conexión de red
ping -n 1 192.168.1.100 >nul
if errorlevel 1 (
    echo ERROR: ESP32 no disponible
    pause
    exit /b 1
)

REM Iniciar aplicación
cd /d "C:\Program Files\SensoraCore"
start SensoraCore_Beta1.0.exe

echo SensoraCore iniciado exitosamente
timeout /t 3
```

#### Script de Monitoreo (Linux)
```bash
#!/bin/bash
# Sistema de monitoreo de SensoraCore

LOGFILE="/var/log/sensoracore_monitor.log"
ESP32_IP="192.168.1.100"
CHECK_INTERVAL=60

log_message() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> $LOGFILE
}

check_esp32() {
    if ping -c 1 -W 5 $ESP32_IP > /dev/null 2>&1; then
        return 0
    else
        return 1
    fi
}

check_application() {
    if pgrep -f "SensoraCore" > /dev/null; then
        return 0
    else
        return 1
    fi
}

main_loop() {
    while true; do
        if ! check_esp32; then
            log_message "WARNING: ESP32 no responde en $ESP32_IP"
        fi
        
        if ! check_application; then
            log_message "WARNING: Aplicación SensoraCore no está ejecutándose"
        fi
        
        sleep $CHECK_INTERVAL
    done
}

log_message "Monitor de SensoraCore iniciado"
main_loop
```

### Apéndice C: Formatos de Datos de Exportación

#### Formato CSV para Datos de Sensores
```csv
timestamp,sensor_type,sensor_id,value,unit,quality,metadata
2024-01-15T14:30:25.123Z,brightness,SENS_001,542.5,lux,good,{"calibration":"v1.2","temp_comp":true}
2024-01-15T14:30:26.124Z,brightness,SENS_001,543.1,lux,good,{"calibration":"v1.2","temp_comp":true}
2024-01-15T14:30:27.125Z,ultrasonic,SENS_002,25.4,cm,good,{"temp":22.5,"humidity":45}
```

#### Formato JSON para Configuración Completa
```json
{
  "session_info": {
    "session_id": "SES_20240115_143025",
    "start_time": "2024-01-15T14:30:25Z",
    "end_time": "2024-01-15T16:45:30Z",
    "operator": "Dr. Smith",
    "experiment": "Calibración sensor luminosidad",
    "version": "SensoraCore Beta 1.0"
  },
  "system_config": {
    "esp32_ip": "192.168.1.100",
    "sampling_rate": 10,
    "filters_enabled": true,
    "temperature_compensation": true
  },
  "sensors": {
    "brightness": {
      "model": "LDR-5mm",
      "calibration_date": "2024-01-10",
      "range": [0, 1000],
      "accuracy": "±2%"
    }
  },
  "data": [
    {
      "timestamp": "2024-01-15T14:30:25.123Z",
      "brightness": 542.5,
      "quality": "good"
    }
  ]
}
```

### Apéndice D: Esquemas de Conexión Física

#### Conexión ESP32 - Sensor de Luminosidad
```
ESP32 Pin    |  LDR/Resistor  |  Función
-------------|----------------|------------------
3.3V         |  VCC           |  Alimentación
GPIO 36      |  Signal        |  Entrada analógica
GND          |  GND           |  Tierra común

Circuito:
3.3V ─── LDR ─── GPIO 36 ─── 10kΩ ─── GND
```

#### Conexión ESP32 - Sensor Ultrasónico
```
ESP32 Pin    |  HC-SR04 Pin   |  Función
-------------|----------------|------------------
5V           |  VCC           |  Alimentación
GPIO 2       |  Trig          |  Trigger output
GPIO 4       |  Echo          |  Echo input
GND          |  GND           |  Tierra común
```

### Apéndice E: Glosario de Términos

**ADC (Analog-to-Digital Converter)**: Convertidor analógico-digital que transforma señales analógicas en valores digitales.

**API (Application Programming Interface)**: Interfaz de programación que define métodos de comunicación entre componentes de software.

**ESP32**: Microcontrolador de Espressif Systems con WiFi y Bluetooth integrados, base del sistema de instrumentación.

**GPIO (General Purpose Input/Output)**: Pines de propósito general configurables como entrada o salida digital.

**GUI (Graphical User Interface)**: Interfaz gráfica de usuario que permite interacción visual con la aplicación.

**Handshake**: Proceso de establecimiento de comunicación entre dos dispositivos para verificar conectividad.

**I2C (Inter-Integrated Circuit)**: Protocolo de comunicación serie síncrono para comunicación entre microcontroladores y sensores.

**IoT (Internet of Things)**: Red de dispositivos físicos conectados que pueden intercambiar datos.

**Latencia**: Tiempo de retardo entre el envío de un comando y la recepción de su respuesta.

**LDR (Light Dependent Resistor)**: Resistor dependiente de luz, sensor básico de luminosidad.

**PID (Proportional-Integral-Derivative)**: Algoritmo de control automático usado en sistemas de regulación.

**PWM (Pulse Width Modulation)**: Modulación por ancho de pulso, técnica para controlar potencia de salida.

**Qt**: Framework multiplataforma para desarrollo de interfaces gráficas de usuario.

**SensoraCore**: Nombre del sistema completo de instrumentación científica distribuida.

**TCP/IP (Transmission Control Protocol/Internet Protocol)**: Conjunto de protocolos de comunicación para redes.

**Timeout**: Tiempo máximo de espera antes de considerar una operación como fallida.

**UART (Universal Asynchronous Receiver-Transmitter)**: Protocolo de comunicación serie asíncrono.

**UI (User Interface)**: Interfaz de usuario, punto de interacción entre humano y máquina.

**WiFi**: Tecnología de comunicación inalámbrica basada en estándares IEEE 802.11.

### Apéndice F: Referencias y Documentación Adicional

#### Documentación Técnica
- **Qt6 Documentation**: https://doc.qt.io/qt-6/
- **Python Official Documentation**: https://docs.python.org/3/
- **ESP32 Technical Reference**: https://docs.espressif.com/projects/esp-idf/
- **PySide6 Reference**: https://doc.qt.io/qtforpython/

#### Estándares y Protocolos
- **IEEE 802.11 (WiFi)**: Estándares de comunicación inalámbrica
- **RFC 793 (TCP)**: Transmission Control Protocol specification
- **IEEE 754**: Standard for floating-point arithmetic
- **ISO 8601**: Date and time format standard

#### Recursos de Desarrollo
- **GitHub Repository**: [URL del repositorio oficial]
- **Issue Tracker**: [URL para reporte de bugs]
- **Community Forum**: [URL del foro de usuarios]
- **Developer Documentation**: [URL de docs para desarrolladores]

#### Contacto y Soporte
- **Email de Soporte**: support@sensoracore.com
- **Soporte Técnico**: tech@sensoracore.com
- **Ventas y Licencias**: sales@sensoracore.com
- **Documentación**: docs@sensoracore.com

---

*Copyright © 2024 SensoraCore Project. Todos los derechos reservados.*
*Versión del documento: 1.0 | Fecha: Enero 2024*
*Para la versión más actualizada de este manual, visite: [URL oficial]*
