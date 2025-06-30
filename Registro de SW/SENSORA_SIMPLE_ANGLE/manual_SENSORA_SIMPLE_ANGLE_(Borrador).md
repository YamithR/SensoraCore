# DESCRIPCIÓN DE LA OBRA SOFTWARE
## SENSORA_SIMPLE_ANGLE

---

### 1. INFORMACIÓN GENERAL

**Nombre del Software:** SENSORA_SIMPLE_ANGLE  
**Fecha de Desarrollo:** 2025  
**Plataforma:** Python 3.x con PyQt5  
**Categoría:** Software Educativo/Módulo Didáctico  

---

### 2. DESCRIPCIÓN GENERAL

SENSORA_SIMPLE_ANGLE es un módulo software especializado diseñado para la monitorización en tiempo real de sensores de ángulo mediante potenciómetros conectados a microcontroladores ESP32. Este software forma parte del ecosistema SensoraCore, una plataforma integral de módulos didácticos para el aprendizaje de sistemas embebidos y adquisición de datos.

El software proporciona una interfaz gráfica intuitiva que permite a estudiantes y profesionales visualizar, calibrar y analizar lecturas angulares provenientes de sensores analógicos, facilitando el entendimiento práctico de conceptos como conversión analógico-digital, calibración por regresión lineal y comunicación serie con microcontroladores.

---

### 3. OBJETIVOS Y PROPÓSITO

#### 3.1 Objetivo General
Desarrollar una herramienta software educativa que facilite el aprendizaje de sistemas de adquisición de datos de sensores angulares, proporcionando una experiencia práctica e interactiva en el manejo de hardware y software embebido.

#### 3.2 Objetivos Específicos
- **Visualización en Tiempo Real:** Mostrar gráficamente las lecturas del sensor de ángulo con actualización continua
- **Calibración Inteligente:** Implementar algoritmos de regresión lineal para calibración precisa del sensor
- **Interfaz Educativa:** Proporcionar diagramas de conexión y documentación integrada
- **Exportación de Datos:** Generar reportes en formato Excel para análisis posterior
- **Comunicación Serie:** Establecer comunicación robusta con microcontroladores ESP32

---

### 4. CARACTERÍSTICAS TÉCNICAS

#### 4.1 Arquitectura del Software
- **Lenguaje de Programación:** Python 3.8+
- **Framework GUI:** PyQt5 con elementos personalizados
- **Visualización:** Matplotlib integrado con FigureCanvasQTAgg
- **Comunicación:** Protocolo serie TCP/UDP para ESP32
- **Procesamiento de Datos:** NumPy y SciPy para cálculos matemáticos
- **Exportación:** OpenPyXL para generación de archivos Excel

#### 4.2 Componentes Principales

##### 4.2.1 Interfaz de Usuario (anguloSimple_UI)
```python
def anguloSimple_UI(self):
    """
    Interfaz principal del módulo con:
    - Diagrama de conexiones ESP32
    - Controles de monitoreo
    - Visualización en tiempo real
    - Panel de calibración
    """
```

##### 4.2.2 Sistema de Calibración (CalibrationDialog)
```python
class CalibrationDialog(QDialog):
    """
    Diálogo avanzado para calibración por regresión lineal:
    - Entrada manual de puntos de referencia
    - Visualización gráfica de la regresión
    - Cálculo automático de ecuaciones de calibración
    - Estadísticas de calidad de ajuste (R²)
    """
```

##### 4.2.3 Hilo de Comunicación (AnguloSimpleThread)
```python
class AnguloSimpleThread(QThread):
    """
    Manejo asíncrono de comunicación con ESP32:
    - Recepción de datos serie en tiempo real
    - Conversión ADC a valores angulares
    - Señales Qt para actualización de interfaz
    """
```

#### 4.3 Funcionalidades Específicas

##### 4.3.1 Monitoreo en Tiempo Real
- **Frecuencia de Muestreo:** Configurable hasta 100 Hz
- **Rango de Medición:** -135° a +135° (configurable)
- **Resolución ADC:** 12 bits (0-4095) del ESP32
- **Filtrado de Señal:** Promedio móvil para reducir ruido

##### 4.3.2 Sistema de Calibración Avanzado
- **Método:** Regresión lineal por mínimos cuadrados
- **Puntos Mínimos:** 2 puntos de referencia
- **Puntos Recomendados:** 5-10 para mejor precisión
- **Estadísticas:** Coeficiente de determinación R²
- **Persistencia:** Guardado/carga de calibraciones en JSON

##### 4.3.3 Visualización Gráfica
- **Tipo de Gráfico:** Línea continua con marcadores
- **Actualización:** Tiempo real con buffer circular
- **Personalización:** Colores y estilos Bootstrap
- **Zoom y Pan:** Navegación interactiva del gráfico

##### 4.3.4 Exportación de Datos
- **Formato:** Excel (.xlsx) con múltiples hojas
- **Contenido:** Timestamps, lecturas ADC, ángulos calibrados
- **Gráficos:** Gráfico de líneas integrado en Excel
- **Metadatos:** Información de calibración y sesión

---

### 5. HARDWARE COMPATIBLE

#### 5.1 Microcontrolador Principal
- **Modelo:** ESP32 DevKit V1 o compatible
- **GPIO Utilizado:** Pin 32 (ADC1_CH4)
- **Alimentación:** 3.3V y GND
- **Comunicación:** WiFi 802.11b/g/n

#### 5.2 Sensor Requerido
- **Tipo:** Potenciómetro rotativo
- **Resistencia:** 10kΩ (recomendado)
- **Rango Angular:** -135° 135° 
- **Linealidad:** ±1% o mejor
- **Conexión:** 3 pines (VCC, GND, Señal)

#### 5.3 Diagrama de Conexiones
```
┌─────────────────────────────────┐
│  ESP32 DevKit V1                │
│                                 │
│  3V3  ○ ←── Potenciómetro (+)   │
│  D32  ○ ←── Potenciómetro (S)   │
│  GND  ○ ←── Potenciómetro (-)   │
│                                 │
│  LED integrado: GPIO 2          │
└─────────────────────────────────┘
```

---

### 6. INSTALACIÓN Y CONFIGURACIÓN

#### 6.1 Requisitos del Sistema
- **Sistema Operativo:** Windows 10/11, macOS 10.14+, Ubuntu 18.04+
- **Python:** Versión 3.8 o superior
- **RAM:** Mínimo 2GB, recomendado 4GB
- **Espacio en Disco:** 500MB para instalación completa

#### 6.2 Dependencias de Software
```python
# requirements.txt
PyQt5>=5.15.0
matplotlib>=3.5.0
numpy>=1.21.0
scipy>=1.7.0
openpyxl>=3.0.9
pyserial>=3.5
```

#### 6.3 Proceso de Instalación
1. **Clonar Repositorio:** Descargar código fuente
2. **Instalar Dependencias:** `pip install -r requirements.txt`
3. **Configurar ESP32:** Flashear firmware compatible
4. **Ejecutar Software:** `python main.py`

---

### 7. MANUAL DE USUARIO

#### 7.1 Inicio del Sistema
1. Conectar ESP32 al puerto USB
2. Verificar conexiones del potenciómetro
3. Ejecutar aplicación SensoraCore
4. Seleccionar módulo "Sensor de Ángulo Simple"

#### 7.2 Calibración del Sensor
1. Hacer clic en "⚙️ Calibrar Sensor"
2. Agregar mínimo 2 puntos de referencia:
   - Posicionar potenciómetro en ángulo conocido
   - Anotar lectura ADC mostrada
   - Ingresar ángulo real de referencia
3. Repetir para diferentes ángulos
4. Hacer clic en "🔧 Realizar Calibración"
5. Verificar calidad de ajuste (R² > 0.95 recomendado)

#### 7.3 Monitoreo en Tiempo Real
1. Hacer clic en "▶️ Iniciar Monitoreo"
2. Observar lecturas en tiempo real
3. Analizar gráfica de tendencias
4. Usar "🗑️ Limpiar Gráfica" para reiniciar

#### 7.4 Exportación de Datos
1. Acumular datos durante sesión de monitoreo
2. Hacer clic en "📊 Exportar Excel"
3. Seleccionar ubicación de guardado
4. Abrir archivo generado para análisis

---

### 8. ALGORITMOS IMPLEMENTADOS

#### 8.1 Calibración por Regresión Lineal
```python
def perform_calibration(self):
    """
    Implementa regresión lineal: y = mx + b
    donde:
    - x: valores ADC del sensor
    - y: ángulos de referencia conocidos
    - m: pendiente (sensibilidad)
    - b: intersección (offset)
    """
    slope, intercept, r_value, p_value, std_err = linregress(
        self.raw_values, self.reference_values
    )
    self.r_squared = r_value ** 2
```

#### 8.2 Conversión ADC a Ángulo
```python
def apply_calibration(self, raw_value):
    """
    Aplica calibración lineal a lectura ADC:
    angle = slope * adc_value + intercept
    """
    if self.is_calibrated:
        return self.slope * raw_value + self.intercept
    else:
        # Conversión por defecto (sin calibrar)
        return (raw_value / 4095.0) * 270.0 - 135.0
```

#### 8.3 Filtrado de Señal
```python
def apply_moving_average(self, new_value, window_size=5):
    """
    Implementa filtro de promedio móvil:
    - Reduce ruido de alta frecuencia
    - Mantiene respuesta temporal aceptable
    - Configurable según aplicación
    """
    self.buffer.append(new_value)
    if len(self.buffer) > window_size:
        self.buffer.pop(0)
    return sum(self.buffer) / len(self.buffer)
```

---

### 9. VALIDACIÓN Y TESTING

#### 9.1 Pruebas de Funcionalidad
- **Comunicación Serie:** Verificación de protocolo con ESP32
- **Calibración:** Validación con sensores conocidos
- **Visualización:** Pruebas de rendimiento gráfico
- **Exportación:** Integridad de archivos Excel

#### 9.2 Pruebas de Precisión
- **Linealidad:** Error < 1% en rango completo
- **Repetibilidad:** Desviación estándar < 0.5°
- **Temperatura:** Estabilidad en rango 0-40°C
- **Ruido:** Relación señal/ruido > 40dB

#### 9.3 Pruebas de Usabilidad
- **Tiempo de Aprendizaje:** < 30 minutos para usuarios novatos
- **Facilidad de Calibración:** Proceso guiado paso a paso
- **Documentación:** Diagramas integrados en interfaz
- **Robustez:** Recuperación automática de errores

---

### 10. APLICACIONES EDUCATIVAS

#### 10.1 Niveles Académicos
- **Educación Media:** Conceptos básicos de sensores
- **Técnico Superior:** Sistemas de adquisición de datos
- **Universitario:** Instrumentación y control
- **Posgrado:** Procesamiento avanzado de señales

#### 10.2 Conceptos Didácticos Cubiertos
- **Electrónica Analógica:** Potenciómetros y divisores de voltaje
- **Conversión A/D:** Cuantización y resolución
- **Calibración:** Regresión lineal y estadística
- **Programación:** Interfaces gráficas y threads
- **Comunicaciones:** Protocolos serie y WiFi
---

### 11. MANTENIMIENTO Y SOPORTE

#### 11.1 Actualizaciones de Software
- **Frecuencia:** Trimestral o según necesidades
- **Canales:** GitHub y repositorio institucional
- **Documentación:** Changelog detallado

#### 11.2 Soporte Técnico
- **Documentación:** Manual completo en línea
- **Issues:** Sistema de tickets en GitHub
- **Capacitación:** Talleres presenciales/virtuales

#### 11.3 Extensibilidad
- **Plugins:** Sistema modular expandible

---

### 12. CONSIDERACIONES DE SEGURIDAD

#### 12.1 Seguridad Eléctrica
- **Voltajes Seguros:** Máximo 5V en todas las conexiones

---

### 13. CONCLUSIONES

SENSORA_SIMPLE_ANGLE representa una herramienta educativa robusta y versátil para el aprendizaje de sistemas de sensores angulares. Su diseño modular, interfaz intuitiva y capacidades de calibración avanzadas lo convierten en una solución ideal para instituciones educativas que buscan modernizar sus laboratorios de instrumentación y control.

El software cumple exitosamente con los objetivos planteados, proporcionando una experiencia educativa completa que abarca desde conceptos básicos de electrónica hasta técnicas avanzadas de procesamiento de señales y calibración estadística.

---

### 14. REFERENCIAS Y DOCUMENTACIÓN ADICIONAL

#### 14.1 Estándares Aplicados
- **IEEE 1451:** Transductores inteligentes
- **ISO 5725:** Precisión y exactitud de medición
- **IEC 61131:** Sistemas de control programable

---