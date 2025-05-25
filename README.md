# SensoraCore Alpha 0.1

**Sistema de Monitoreo de Sensores WiFi ESP32 + PySide6** 🚀

⚠️ **VERSIÓN ALPHA 0.1**: Esta es una versión preliminar en desarrollo. Algunas funcionalidades pueden estar incompletas o presentar errores.

SensoraCore es un sistema de monitoreo de sensores que conecta un ESP32 ejecutando MicroPython con una aplicación de escritorio desarrollada en Python usando PySide6. El sistema permite leer datos de sensores en tiempo real a través de WiFi, visualizarlos gráficamente y exportar los datos a Excel.

## ✨ Características Principales

### 🎨 **Interfaz Moderna y Responsive**
- **Layout de dos paneles**: Panel izquierdo para conexión y sensores, panel derecho para detalles
- **Diseño responsive**: Ajustable con splitter, proporción 1/3 - 2/3
- **Animaciones suaves**: Transiciones fade-in al conectar ESP32
- **Colores optimizados**: Mejor visibilidad en gráficas y diagramas

### 🔐 **Experiencia de Usuario Inteligente**
- **Sensores ocultos hasta conexión**: Previene errores de uso prematuro
- **Indicadores visuales de estado**: Verde=conectado, Rojo=desconectado
- **Controles dinámicos**: Botones cambian según el contexto
- **Validación inteligente**: Sistema previene estados inconsistentes

### 📊 **Visualización Avanzada**
- **Gráficas profesionales**: Colores destacados y grid sutil
- **Monitoreo en tiempo real**: Actualización continua de datos
- **Controles de reproducción**: Iniciar/Pausar/Continuar/Detener
- **Exportación Excel mejorada**: Formato profesional con gráficas integradas

### 📡 **Comunicación WiFi Robusta**
- **Conexión inalámbrica estable**: Entre ESP32 y aplicación de escritorio
- **Protocolo de comandos**: Sistema de comunicación estructurado
- **Manejo de errores**: Reconexión automática y timeouts inteligentes
- **Feedback en tiempo real**: Estado de conexión siempre visible

## 📋 Sensores Soportados

### ✅ Implementado
- **Ángulo Simple (Potenciómetro)**: Lee un potenciómetro como sensor de ángulo (0-270°)

### ✅ Implementado
- **Brazo Ángulo**: Sensor multi-ángulo para brazo robótico (3 potenciómetros + sensor capacitivo)

### 🔄 Próximamente
- **DistanciaIR**: Sensor de distancia infrarrojo
- **DistanciaCap**: Sensor de distancia capacitivo
- **DistanciaUltrasonido**: Sensor ultrasonico HC-SR04
- **OpticTestLR_Velocidad**: Sensor óptico de velocidad

## 🏗️ Estructura del Proyecto

```
SensoraCore/
├── README.md
├── SensoraCoreApp/           # Aplicación de escritorio (Python/PySide6)
│   ├── main.py              # Punto de entrada de la aplicación
│   ├── requirements.txt     # Dependencias Python
│   ├── network_client.py    # Cliente de red para comunicación con ESP32
│   └── ui/
│       ├── __init__.py
│       └── main_window.py   # Interfaz gráfica principal
└── SensoraCoreESP32/        # Código para ESP32 (MicroPython)
    ├── main.py              # Servidor principal del ESP32
    └── wifi_config.py       # Configuración WiFi
```

## 🔧 Instalación y Configuración

### Aplicación de Escritorio (Python)

1. **Instalar dependencias:**
```bash
cd SensoraCoreApp
pip install -r requirements.txt
```

2. **Ejecutar la aplicación:**
```bash
python main.py
```

### ESP32 (MicroPython)

1. **Instalar MicroPython** en tu ESP32 DevKit V1
2. **Configurar WiFi** en `wifi_config.py`:
```python
SSID = 'Tu_Red_WiFi'
PASSWORD = 'Tu_Contraseña'
```
3. **Subir archivos** al ESP32:
   - `main.py`
   - `wifi_config.py`

## 🔌 Conexiones Hardware

### ESP32 DevKit V1 + Potenciómetro 10kΩ

```
ESP32 DevKit V1 - Conexiones:

┌─────────────────────────────────┐
│  ESP32 DevKit V1               │
│                                │
│  3V3  ○ ←── Potenciómetro (+)  │
│  GND  ○ ←── Potenciómetro (-)  │
│  D32  ○ ←── Potenciómetro (S)  │
│                                │
│  LED integrado: GPIO 2         │
└─────────────────────────────────┘

Potenciómetro 10kΩ:
• Pin (+): Alimentación 3.3V
• Pin (-): Tierra (GND)  
• Pin (S): Señal analógica
```

## 🖥️ Uso de la Aplicación

1. **Conectar ESP32**: 
   - Enciende el ESP32 y espera que se conecte al WiFi
   - Anota la IP que aparece en el monitor serial

2. **Conectar desde la App**:
   - Ingresa la IP del ESP32 en la aplicación
   - Presiona "Conectar y encender LED integrado"
   - Si la conexión es exitosa, el LED del ESP32 se encenderá

3. **Modo Ángulo Simple**:
   - Activa el checkbox "Modo Ángulo Simple"
   - Gira el potenciómetro para ver los datos en tiempo real
   - Los datos se muestran en la gráfica y en texto

4. **Exportar Datos**:
   - Presiona "Exportar datos a Excel" para guardar los datos
   - El archivo incluye los datos y una gráfica

5. **Limpiar Gráfica**:
   - Usa "Limpiar gráfica" para borrar todos los datos

## 📡 Protocolo de Comunicación

### Comandos ESP32 → Aplicación

| Comando | Descripción | Respuesta |
|---------|-------------|-----------|
| `LED_ON` | Encender LED integrado | `LED_ON_OK` |
| `LED_OFF` | Apagar LED integrado | `LED_OFF_OK` |
| `GET_POT` | Leer potenciómetro una vez | `valor_adc` |
| `MODO:ANGULO_SIMPLE` | Activar modo continuo | `POT:lectura,ANG:angulo` |
| `STOP` | Detener modo continuo | `STOP_OK` |

### Formato de Datos en Tiempo Real

```
POT:2048,ANG:135
POT:1024,ANG:67
POT:3072,ANG:202
```

## 📊 Funcionalidades de Exportación

El archivo Excel exportado contiene:

- **Hoja "Datos Ángulo Simple"**:
  - Columna A: Número de muestra
  - Columna B: Lectura ADC (0-4095)
  - Columna C: Ángulo calculado (0-270°)
  - Columna D: Timestamp
  - Gráfica de líneas automática
  - Estadísticas (min, max, promedio)

## 🛠️ Desarrollo

### Agregar Nuevos Sensores

1. **En ESP32** (`main.py`):
   - Agregar nuevo comando en el bucle principal
   - Implementar función de lectura del sensor
   - Definir formato de respuesta

2. **En Aplicación** (`main_window.py`):
   - Crear nuevo `QGroupBox` para el sensor
   - Implementar thread de comunicación
   - Agregar visualización específica

### Estructura de Threads

- **AnguloSimpleThread**: Maneja comunicación continua con ESP32
- **MainWindow**: Interfaz principal y coordinación
- **ESP32Client**: Cliente de red para comandos individuales

## 🐛 Solución de Problemas

### Error de Conexión ESP32
- Verificar que ESP32 esté encendido y conectado al WiFi
- Comprobar que la IP sea correcta
- Asegurar que no hay firewall bloqueando el puerto 8080

### Error al Exportar Excel
- Verificar que `openpyxl` esté instalado
- Comprobar permisos de escritura en la carpeta destino

### Gráfica no se actualiza
- Verificar que matplotlib esté correctamente instalado
- Reiniciar el modo del sensor

## 📝 Contribuir

1. Fork del repositorio
2. Crear rama para nueva funcionalidad
3. Implementar cambios
4. Ejecutar pruebas
5. Crear Pull Request

## 📄 Licencia

Este proyecto está bajo licencia MIT. Ver archivo LICENSE para más detalles.

## 👥 Créditos

Desarrollado como parte del proyecto de Módulos Didácticos para migrar funcionalidades de Arduino a ESP32 con comunicación WiFi.

---

**Versión**: Alpha 0.1  
**Estado**: Desarrollo preliminar  
**Última actualización**: Mayo 2025
