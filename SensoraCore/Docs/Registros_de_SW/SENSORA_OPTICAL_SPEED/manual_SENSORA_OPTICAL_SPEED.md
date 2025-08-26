# DESCRIPCIÓN DE LA OBRA SOFTWARE
## SENSORA_OPTICAL_SPEED

---

### 1. INFORMACIÓN GENERAL

**Nombre del Software:** SENSORA_OPTICAL_SPEED  
**Fecha de Desarrollo:** 2025  
**Plataforma:** Python 3.x con PySide6  
**Categoría:** Software Educativo/Módulo Didáctico  

---

### 2. INTRODUCCIÓN

#### 2.1 Descripción General

SENSORA_OPTICAL_SPEED es un módulo software especializado diseñado para el control y monitoreo en tiempo real de sistemas de velocidad dual mediante motores DC con sensores ópticos tipo encoder. Este software forma parte del ecosistema SensoraCore, una plataforma integral de módulos didácticos para el aprendizaje de sistemas embebidos, control de motores y adquisición de datos.

El software proporciona una interfaz gráfica intuitiva que permite a estudiantes y profesionales controlar la velocidad de dos motores DC independientes, monitorear sus RPM mediante encoders ópticos, y visualizar datos en tiempo real, facilitando el entendimiento práctico de conceptos como control PWM, medición de velocidad angular, y sistemas de retroalimentación.

#### 2.2 Objetivo General

Desarrollar una herramienta software educativa que facilite el aprendizaje de sistemas de control de velocidad de motores, proporcionando una experiencia práctica e interactiva en el manejo de control PWM, sensores ópticos y sistemas de retroalimentación en tiempo real.

#### 2.3 Objetivos Específicos

- **Control de Velocidad Dual:** Controlar independientemente la velocidad y dirección de dos motores DC mediante PWM
- **Monitoreo en Tiempo Real:** Mostrar las RPM de ambos motores con actualización continua
- **Interface de Control Intuitiva:** Proporcionar controles visuales para ajuste dinámico de velocidad
- **Comunicación TCP:** Establecer comunicación robusta por sockets TCP con ESP32
- **Educación en Control:** Enseñar conceptos de control de motores, PWM y retroalimentación

---

### 3. CARACTERÍSTICAS TÉCNICAS

#### 3.1 Arquitectura del Software

- **Lenguaje de Programación:** Python 3.8+
- **Framework GUI:** PySide6 (Qt6) con elementos personalizados
- **Comunicación:** Sockets TCP (puerto 8080) hacia firmware MicroPython en ESP32
- **Control de Motores:** Señales PWM bidireccionales (-100% a +100%)
- **Sensores:** Procesamiento de señales de encoders ópticos digitales

#### 3.2 Componentes Principales

##### 3.2.1 Interfaz de Usuario (opticalSpeed_ui.py)
```python
class Ui_opticalSpeed:
    """
    Interfaz principal del módulo con:
    - Diagrama de conexiones L298N y encoders
    - Controles de monitoreo e inicio/pausa
    - Visualización de RPM en tiempo real
    - Panel de control de velocidad bidireccional
    """
```

##### 3.2.2 Hilo de Comunicación (OpticalSpeedThread)
```python
class OpticalSpeedThread(QThread):
    """
    Manejo asíncrono de comunicación con ESP32:
    - Recepción de datos de RPM en tiempo real
    - Envío de comandos de velocidad (-100 a +100)
    - Señales Qt para actualización de interfaz
    - Control de estados de conexión
    """
```

##### 3.2.3 Lógica de Control (OpticalSpeedLogic)
```python
class OpticalSpeedLogic(QWidget):
    """
    Control principal del módulo:
    - Gestión de estados de monitoreo
    - Procesamiento de comandos de velocidad
    - Actualización de displays de RPM
    - Manejo de eventos de interfaz
    """
```

#### 3.3 Funcionalidades Específicas

##### 3.3.1 Monitoreo en Tiempo Real
- **Frecuencia de Muestreo:** Variable según configuración firmware (~200ms)
- **Medición:** RPM individual de motor izquierdo y derecho
- **Resolución:** Basada en pulsos por revolución (PPR) configurables
- **Protocolo:** Datos formato `RPM_L:<izq>,RPM_R:<der>,SPEED:<actual>`

##### 3.3.2 Control de Velocidad Bidireccional
- **Rango de Control:** -100% a +100% (negativo = reversa)
- **Incrementos:** Ajuste de ±10% por comando
- **Actualización:** Envío inmediato de comandos al ESP32
- **Feedback:** Visualización de velocidad comandada y real

##### 3.3.3 Interface Visual Avanzada
- **Displays RPM:** Indicadores numéricos grandes para cada motor
- **Control de Velocidad:** Botones de incremento/decremento con feedback visual
- **Diagrama de Conexiones:** Esquema integrado L298N y encoders
- **Estados de Conexión:** Indicadores visuales de estado TCP

---

### 4. HARDWARE COMPATIBLE

#### 4.1 Microcontrolador Principal
- **Modelo:** ESP32 DevKit V1 o compatible
- **GPIO Encoders:** Pin 39 (Motor Izquierdo), Pin 34 (Motor Derecho)
- **GPIO PWM:** Pines 25, 36, 32, 33 para control L298N
- **Alimentación:** 3.3V lógica, VIN para puente H
- **Comunicación:** WiFi 802.11b/g/n (sockets TCP)

#### 4.2 Sistema de Motores
- **Motores:** Dos motores DC de 6-12V con encoders ópticos
- **Controlador:** Puente H L298N para control bidireccional
- **Encoders:** Sensores ópticos tipo herradura con discos ranurados
- **Alimentación Externa:** 12V para motores, masa común con ESP32

#### 4.3 Diagrama de Conexiones
```
┌─────────────────────────────────┐
│  ESP32 DevKit V1                │
│                                 │
│  5V   ○ ←── VCC (Encoders)      │
│  5V   ○ ←── VCC (Lógica L298N)  │
│  GND  ○ ←── GND (Común)         │
│  D39  ○ ←── D (Encoder Izq.)    │
│  D34  ○ ←── D (Encoder Der.)    │
│  D25  ○ ←── IN1 (Motor Izq.)    │
│  D36  ○ ←── IN2 (Motor Izq.)    │
│  D32  ○ ←── IN3 (Motor Der.)    │
│  D33  ○ ←── IN4 (Motor Der.)    │
│  VIN  ○ ←── 12V (Puente H)      │
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
socket (nativo)
threading (nativo)
```

#### 5.3 Proceso de Instalación
1. **Clonar Repositorio:** Descargar código fuente
2. **Instalar Dependencias:** `pip install -r requirements.txt`
3. **Configurar ESP32:** Flashear firmware MicroPython y cargar `SensoraCore/SC_Firmware/main.py`
4. **Conectar Hardware:** Cablear L298N, motores y encoders según diagrama
5. **Ejecutar Software:** `python main.py`

---

### 6. MANUAL DE USUARIO

#### 6.1 Inicio del Sistema
1. Conectar ESP32 al puerto USB
2. Verificar conexiones de L298N y encoders
3. Conectar alimentación de 12V para motores
4. Ejecutar aplicación SensoraCore
5. Seleccionar módulo "Optical Speed"

#### 6.2 Monitoreo en Tiempo Real
1. Hacer clic en "Iniciar Monitoreo"
2. Verificar conexión TCP con ESP32
3. Observar lecturas RPM en displays L y R
4. Monitorear valores en tiempo real

#### 6.3 Control de Velocidad
1. Usar botón "🔼" para incrementar velocidad (+10%)
2. Usar botón "🔽" para decrementar velocidad (-10%)
3. Observar valor central mostrando velocidad comandada
4. Valores negativos indican rotación en reversa
5. Rango válido: -100% a +100%

#### 6.4 Pausa y Detención
1. Hacer clic en "Pausar" para detener comunicación
2. Los motores se detendrán automáticamente
3. Reiniciar con "Iniciar Monitoreo"

---

### 7. ALGORITMOS IMPLEMENTADOS

#### 7.1 Control PWM Bidireccional
```python
def set_speed(self, percent: int):
    """
    Envía comando de velocidad al ESP32:
    - percent: -100 a +100
    - negativo: rotación reversa
    - positivo: rotación adelante
    """
    cmd = f"SET_SPEED:{percent}\n".encode()
    self.sock.sendall(cmd)
```

#### 7.2 Procesamiento de Datos RPM
```python
def _on_data(self, rpm_l: float, rpm_r: float, speed: int):
    """
    Procesa datos recibidos del ESP32:
    - rpm_l: RPM motor izquierdo
    - rpm_r: RPM motor derecho  
    - speed: velocidad actual comandada
    """
    # Actualizar displays en interfaz
    self.ui.RPMizquierdaDt.setText(f"{rpm_l:.0f}")
    self.ui.RPMderechaDt.setText(f"{rpm_r:.0f}")
```

#### 7.3 Comunicación TCP Robusta
```python
def run(self):
    """
    Bucle principal de comunicación:
    - Establece conexión TCP
    - Envía comando MODO:OPTICAL_SPEED
    - Procesa flujo de datos continuo
    - Maneja errores y reconexiones
    """
```

---

### 8. VALIDACIÓN Y TESTING

#### 8.1 Pruebas de Funcionalidad
- **Comunicación TCP:** Verificación de handshake MODO:OPTICAL_SPEED
- **Control PWM:** Validación de comandos SET_SPEED
- **Lectura Encoders:** Pruebas de conteo de pulsos precisos
- **Interface Gráfica:** Verificación de actualización en tiempo real

#### 8.2 Pruebas de Precisión
- **Medición RPM:** Comparación con tacómetro externo
- **Control Velocidad:** Linealidad de respuesta PWM
- **Estabilidad:** Pruebas de funcionamiento continuo
- **Exactitud:** Error < 2% en mediciones RPM

#### 8.3 Pruebas de Usabilidad
- **Tiempo de Aprendizaje:** < 15 minutos para usuarios novatos
- **Facilidad de Control:** Interface intuitiva con feedback visual
- **Documentación:** Diagramas integrados en interfaz
- **Robustez:** Recuperación automática de errores de comunicación

---

### 9. APLICACIONES EDUCATIVAS

#### 9.1 Niveles Académicos
- **Educación Media:** Conceptos básicos de motores y control
- **Técnico Superior:** Sistemas de control y retroalimentación
- **Universitario:** Control automático y sistemas embebidos
- **Posgrado:** Algoritmos de control avanzado

#### 9.2 Conceptos Didácticos Cubiertos
- **Control de Motores:** PWM, puentes H y control bidireccional
- **Sensores Ópticos:** Encoders, conteo de pulsos y medición de velocidad
- **Sistemas de Retroalimentación:** Control en lazo cerrado
- **Comunicaciones:** Protocolos TCP y sistemas distribuidos
- **Programación:** Hilos, interfaces gráficas y procesamiento en tiempo real

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
- **Plugins:** Sistema modular expandible
- **Configuración:** Parámetros ajustables de encoders

---

### 11. CONSIDERACIONES DE SEGURIDAD

#### 11.1 Seguridad Eléctrica
- **Alimentación Separada:** 12V para motores aislada de 3.3V lógica
- **Masa Común:** Conexión GND entre todos los módulos
- **Protección:** Fusibles recomendados en alimentación de motores

#### 11.2 Seguridad Mecánica
- **Montaje Seguro:** Fijación adecuada de motores y encoders
- **Protección:** Resguardos en partes móviles
- **Parada de Emergencia:** Desconexión rápida de alimentación

---

### 12. CONCLUSIONES

SENSORA_OPTICAL_SPEED representa una herramienta educativa robusta y versátil para el aprendizaje de sistemas de control de motores con retroalimentación óptica. Su diseño modular, interfaz intuitiva y capacidades de control en tiempo real lo convierten en una solución ideal para instituciones educativas que buscan modernizar sus laboratorios de control automático y sistemas embebidos.

El software cumple exitosamente con los objetivos planteados, proporcionando una experiencia educativa completa que abarca desde conceptos básicos de control PWM hasta técnicas avanzadas de sistemas de retroalimentación y comunicaciones TCP en sistemas embebidos distribuidos.

---
