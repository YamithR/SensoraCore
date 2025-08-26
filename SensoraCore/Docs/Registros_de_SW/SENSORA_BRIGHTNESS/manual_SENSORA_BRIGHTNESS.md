# DESCRIPCIÓN DE LA OBRA SOFTWARE
## SENSORA_BRIGHTNESS

---

### 1. INFORMACIÓN GENERAL

**Nombre del Software:** SENSORA_BRIGHTNESS  
**Fecha de Desarrollo:** 2025  
**Plataforma:** Python 3.x con PySide6  
**Categoría:** Software Educativo/Módulo Didáctico  

---

### 2. INTRODUCCIÓN

#### 2.1 Descripción General

SENSORA_BRIGHTNESS es un módulo software especializado diseñado para el monitoreo en tiempo real de niveles de luminosidad mediante sensores de fotorresistencia (LDR - Light Dependent Resistor). Este software forma parte del ecosistema SensoraCore, una plataforma integral de módulos didácticos para el aprendizaje de sistemas embebidos, sensores analógicos y adquisición de datos.

El software proporciona una interfaz gráfica intuitiva que permite a estudiantes y profesionales monitorear la intensidad lumínica, visualizar datos en formato numérico y de barras de progreso, facilitando el entendimiento práctico de conceptos como conversión analógico-digital, caracterización de sensores ópticos y sistemas de medición luminosa.

#### 2.2 Objetivo General

Desarrollar una herramienta software educativa que facilite el aprendizaje de sistemas de medición de luminosidad, proporcionando una experiencia práctica e interactiva en el manejo de sensores fotorresistivos y procesamiento de señales analógicas.

#### 2.3 Objetivos Específicos

- **Monitoreo de Luminosidad:** Medir y visualizar niveles de luz ambiente en tiempo real
- **Conversión ADC a Porcentaje:** Transformar lecturas analógicas a valores porcentuales comprensibles
- **Visualización Múltiple:** Mostrar datos en formatos numérico, LCD y barra de progreso
- **Comunicación TCP:** Establecer comunicación robusta por sockets TCP con ESP32
- **Exportación de Datos:** Generar reportes en formato Excel para análisis posterior

---

### 3. CARACTERÍSTICAS TÉCNICAS

#### 3.1 Arquitectura del Software

- **Lenguaje de Programación:** Python 3.8+
- **Framework GUI:** PySide6 (Qt6) con widgets especializados
- **Comunicación:** Sockets TCP (puerto 8080) hacia firmware MicroPython en ESP32
- **Visualización:** QLCDNumber, QProgressBar y QLabel para datos múltiples
- **Exportación:** openpyxl para generación de archivos Excel

#### 3.2 Componentes Principales

##### 3.2.1 Interfaz de Usuario (brightness_ui.py)
```python
class Ui_brightness:
    """
    Interfaz principal del módulo con:
    - Display LCD para porcentaje de luminosidad
    - Barra de progreso visual (0-100%)
    - Labels de datos analógicos crudos
    - Controles de monitoreo e inicio/pausa
    """
```

##### 3.2.2 Hilo de Comunicación (_BrightnessThread)
```python
class _BrightnessThread(QObject):
    """
    Manejo asíncrono de comunicación con ESP32:
    - Recepción de datos ADC y voltaje
    - Configuración de intervalo de muestreo
    - Señales Qt para actualización de interfaz
    - Control de estados de conexión
    """
```

##### 3.2.3 Lógica de Control (BrightnessLogic)
```python
class BrightnessLogic(QObject):
    """
    Control principal del módulo:
    - Gestión de estados de monitoreo
    - Procesamiento de datos de luminosidad
    - Actualización de displays múltiples
    - Exportación de datos a Excel
    """
```

#### 3.3 Funcionalidades Específicas

##### 3.3.1 Monitoreo en Tiempo Real
- **Frecuencia de Muestreo:** Configurable (default 200ms)
- **Resolución ADC:** 12 bits (0-4095) del ESP32
- **Conversión:** ADC a porcentaje directo (ADC * 100 / 4095)
- **Protocolo:** Datos formato `SENSOR:LDR,ADC:<valor>,VOLT:<voltaje>`

##### 3.3.2 Visualización Múltiple
- **Display LCD:** Porcentaje de luminosidad grande y visible
- **Barra de Progreso:** Representación gráfica 0-100%
- **Datos Analógicos:** Valor ADC crudo para análisis técnico
- **Actualización Sincronizada:** Todos los displays se actualizan simultáneamente

##### 3.3.3 Exportación de Datos
- **Formato:** Excel (.xlsx) con datos tabulados
- **Contenido:** Tiempo, ADC, voltaje, porcentaje
- **Metadatos:** Información de sesión e intervalo de muestreo
- **Estructura:** Hojas separadas para datos y metadatos

---

### 4. HARDWARE COMPATIBLE

#### 4.1 Microcontrolador Principal
- **Modelo:** ESP32 DevKit V1 o compatible
- **GPIO Utilizado:** Pin analógico ADC (configurable)
- **Alimentación:** 3.3V y GND
- **Comunicación:** WiFi 802.11b/g/n (sockets TCP)

#### 4.2 Sensor Requerido
- **Tipo:** Fotorresistencia (LDR - Light Dependent Resistor)
- **Rango Resistivo:** 1kΩ-10MΩ (según iluminación)
- **Tiempo de Respuesta:** < 100ms para cambios graduales
- **Conexión:** Divisor de voltaje con resistencia fija

#### 4.3 Diagrama de Conexiones
```
┌─────────────────────────────────┐
│  ESP32 DevKit V1                │
│                                 │
│  3V3  ○ ←── VCC (+)             │
│  D34  ○ ←── Señal (LDR + R)     │
│  GND  ○ ←── GND (-)             │
│                                 │
│  Circuito Divisor:              │
│  3V3 ── LDR ── D34 ── R ── GND  │
│                                 │
└─────────────────────────────────┘
```

---

### 5. REQUERIMIENTOS DE INSTALACIÓN Y CONFIGURACIÓN

#### 5.1 Requisitos del Sistema
- **Sistema Operativo:** Windows 10/11, macOS 10.14+, Ubuntu 18.04+
- **Python:** Versión 3.8 o superior
- **RAM:** Mínimo 2GB, recomendado 4GB
- **Espacio en Disco:** 500MB para instalación completa

#### 5.2 Dependencias de Software
```text
PySide6
openpyxl
socket (nativo)
time (nativo)
threading (nativo)
```

#### 5.3 Proceso de Instalación
1. **Clonar Repositorio:** Descargar código fuente
2. **Instalar Dependencias:** `pip install -r requirements.txt`
3. **Configurar ESP32:** Flashear firmware MicroPython y cargar `SensoraCore/SC_Firmware/main.py`
4. **Conectar Hardware:** Cablear LDR según diagrama de divisor de voltaje
5. **Ejecutar Software:** `python main.py`

---

### 6. MANUAL DE USUARIO

#### 6.1 Inicio del Sistema
1. Conectar ESP32 al puerto USB
2. Verificar conexiones de LDR en configuración divisor de voltaje
3. Ejecutar aplicación SensoraCore
4. Seleccionar módulo "Monitoreo de Brillo"

#### 6.2 Monitoreo en Tiempo Real
1. Hacer clic en "Iniciar Monitoreo"
2. Verificar conexión TCP con ESP32
3. Observar actualización en tiempo real de:
   - Display LCD mostrando porcentaje de luminosidad
   - Barra de progreso visual
   - Valores ADC crudos
4. Probar variaciones de luz (cubrir/iluminar sensor)

#### 6.3 Limpieza de Datos
1. Usar botón de limpieza para resetear series de datos
2. Los displays se reinicializan a valores por defecto
3. Se conserva la conexión activa

#### 6.4 Exportación de Datos
1. Acumular datos durante sesión de monitoreo
2. Hacer clic en botón de exportación
3. Seleccionar ubicación de guardado
4. Revisar archivo Excel generado con datos y metadatos

---

### 7. ALGORITMOS IMPLEMENTADOS

#### 7.1 Conversión ADC a Porcentaje
```python
def _on_sample(self, adc: int, volt: float, ts: float):
    """
    Convierte lectura ADC a porcentaje de luminosidad:
    - adc: valor 0-4095 del conversor ADC
    - porcentaje = (adc * 100.0 / 4095.0)
    - rango resultante: 0-100%
    """
    pct = int(round(max(0.0, min(100.0, (adc * 100.0 / 4095.0)))))
```

#### 7.2 Comunicación TCP Especializada
```python
def _run(self):
    """
    Bucle principal de comunicación:
    - Envía comando MODO:BRIGHTNESS
    - Configura intervalo con BR_START:<ms>
    - Procesa flujo de datos formato SENSOR:LDR
    - Extrae ADC y VOLT de respuesta estructurada
    """
```

#### 7.3 Actualización de Displays Múltiples
```python
def _on_sample(self, adc: int, volt: float, ts: float):
    """
    Sincroniza actualización de todos los displays:
    - LCD: muestra porcentaje calculado
    - ProgressBar: establece valor 0-100
    - Label: muestra valor ADC crudo
    """
```

---

### 8. VALIDACIÓN Y TESTING

#### 8.1 Pruebas de Funcionalidad
- **Comunicación TCP:** Verificación de handshake MODO:BRIGHTNESS
- **Conversión ADC:** Validación de cálculos porcentuales
- **Actualización Visual:** Sincronización de múltiples displays
- **Exportación:** Integridad de archivos Excel generados

#### 8.2 Pruebas de Precisión
- **Linealidad:** Respuesta proporcional a cambios de iluminación
- **Resolución:** Capacidad de detectar cambios mínimos de luz
- **Estabilidad:** Lecturas consistentes en condiciones constantes
- **Rango Dinámico:** Operación correcta desde oscuridad total a iluminación intensa

#### 8.3 Pruebas de Usabilidad
- **Tiempo de Aprendizaje:** < 10 minutos para usuarios novatos
- **Claridad Visual:** Displays fáciles de interpretar
- **Documentación:** Notas integradas en interfaz
- **Robustez:** Recuperación automática de errores de comunicación

---

### 9. APLICACIONES EDUCATIVAS

#### 9.1 Niveles Académicos
- **Educación Media:** Conceptos básicos de sensores ópticos
- **Técnico Superior:** Sistemas de adquisición de datos analógicos
- **Universitario:** Instrumentación y caracterización de sensores
- **Posgrado:** Procesamiento de señales y calibración

#### 9.2 Conceptos Didácticos Cubiertos
- **Sensores Ópticos:** Fotorresistencias y su comportamiento
- **Conversión A/D:** Cuantización y resolución de ADC
- **Divisores de Voltaje:** Circuitos de acondicionamiento de señal
- **Comunicaciones:** Protocolos TCP y streaming de datos
- **Visualización:** Múltiples formas de representar datos

---

### 10. MANTENIMIENTO Y SOPORTE

#### 10.1 Actualizaciones de Software
- **Frecuencia:** Trimestral o según necesidades
- **Canales:** GitHub y repositorio institucional
- **Documentación:** Changelog detallado

#### 10.2 Soporte Técnico
- **Documentación:** Manual completo en línea
- **Issues:** Sistema de tickets en GitHub
- **Capacitación:** Talleres presenciales/virtuales

#### 10.3 Extensibilidad
- **Configuración:** Intervalos de muestreo ajustables
- **Calibración:** Posibilidad de implementar factores de corrección

---

### 11. CONSIDERACIONES DE SEGURIDAD

#### 11.1 Seguridad Eléctrica
- **Voltajes Seguros:** Máximo 3.3V en pines ADC del ESP32
- **Protección:** Resistencias limitadoras en divisor de voltaje

#### 11.2 Seguridad Óptica
- **Luz Intensa:** Evitar exposición directa del sensor a fuentes láser
- **Manejo:** Proteger LDR de daños mecánicos

---

### 12. CONCLUSIONES

SENSORA_BRIGHTNESS representa una herramienta educativa efectiva y versátil para el aprendizaje de sistemas de sensores ópticos y medición de luminosidad. Su diseño modular, interfaz clara y capacidades de visualización múltiple lo convierten en una solución ideal para instituciones educativas que buscan enseñar conceptos fundamentales de instrumentación y sensores analógicos.

El software cumple exitosamente con los objetivos planteados, proporcionando una experiencia educativa completa que abarca desde conceptos básicos de fotorresistencias hasta técnicas de procesamiento de señales analógicas y comunicaciones TCP en sistemas embebidos.

---
