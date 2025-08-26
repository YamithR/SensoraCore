# Manual de Usuario - SENSORA IR STEERING

## 1. Introducción

El módulo **SENSORA_IR_STEERING** representa una solución avanzada para el control automático de dirección basado en sensores infrarrojos. Este sistema implementa algoritmos de control PID para seguimiento de línea y navegación autónoma, diseñado específicamente para aplicaciones robóticas educativas, vehículos autónomos de escala reducida y sistemas de control automático de dirección.

### Características Principales
- **Sensores**: Array de 5 sensores IR para detección de línea
- **Control**: Algoritmo PID configurable en tiempo real
- **Actuadores**: Control diferencial de motores izquierdo y derecho
- **Visualización**: Estado de sensores y parámetros de control en tiempo real
- **Configuración**: Interfaz gráfica para ajuste de parámetros PID y velocidad base
- **Comunicación**: TCP/IP con ESP32 para control continuo

### Aplicaciones
- Robots seguidores de línea educativos
- Vehículos autónomos guiados
- Sistemas de control automático de dirección
- Plataformas de investigación en robótica
- Enseñanza de sistemas de control retroalimentado
- Competencias de robótica y seguimiento de trayectorias

## 2. Especificaciones Técnicas

### Array de Sensores IR
- **Cantidad**: 5 sensores infrarrojos digitales
- **Configuración**: Línea recta con espaciado uniforme
- **Tipo**: LED IR + fotodiodo con comparador
- **Salida**: Digital (0/1) por cada sensor
- **Alcance**: 3-15mm para detección de línea
- **Resolución**: Detección binaria superficie clara/oscura

### Sistema de Control PID
- **Parámetros**: Kp (proporcional), Ki (integral), Kd (derivativo)
- **Rango Kp**: 0.0 - 10.0 (paso 0.05)
- **Rango Ki**: 0.0 - 10.0 (paso 0.01)
- **Rango Kd**: 0.0 - 10.0 (paso 0.05)
- **Velocidad base**: -100% a +100% (control direccional)
- **Actualización**: Tiempo real con aplicación inmediata

### Control de Motores
- **Tipo**: Control PWM diferencial
- **Motores**: Izquierdo y derecho independientes
- **Retroalimentación**: RPM por encoder óptico
- **Rango salida**: -100% a +100% por motor
- **Frecuencia PWM**: 1kHz típica
- **Resolución**: 8-bit (0-255 niveles internos)

### Comunicación ESP32
- **Protocolo**: TCP/IP sobre WiFi
- **Comando inicial**: "MODO:IR_STEERING"
- **Comandos control**: "SET_BASE:<percent>", "SET_PID:Kp=X,Ki=Y,Kd=Z"
- **Datos recibidos**: "SENS:xxxxx,ERR:X.X,OUT_L:XXX,OUT_R:XXX,SPEED:XX,RPM_L:XXX,RPM_R:XXX"
- **Puerto**: 8080 (estándar SENSORA)

## 3. Compatibilidad de Hardware

### Microcontrolador Requerido
- **ESP32 DevKit V1** o compatible
- **GPIO**: Mínimo 7 pines (5 sensores + 2 motores)
- **PWM**: 2 canales para control motores
- **Timers**: Para encoders RPM y control PID
- **WiFi**: 802.11 b/g/n para comunicación

### Conexiones Sensores IR
```
ESP32 Pin    Sensor IR    Función
D12      ←   IR1          Sensor extremo izquierdo
D13      ←   IR2          Sensor izquierdo
D14      ←   IR3          Sensor central
D15      ←   IR4          Sensor derecho
D16      ←   IR5          Sensor extremo derecho
```

### Conexiones Sistema Motor
```
ESP32 Pin    Función           Conexión
D18      →   PWM Motor Izq     Driver L298N IN1
D19      →   DIR Motor Izq     Driver L298N IN2
D21      →   PWM Motor Der     Driver L298N IN3
D22      →   DIR Motor Der     Driver L298N IN4
D25      ←   Encoder Izq       Sensor RPM izquierdo
D26      ←   Encoder Der       Sensor RPM derecho
```

### Driver de Motores L298N
- **Alimentación**: 12V para motores, 5V lógica
- **Corriente**: Hasta 2A por canal
- **Control**: PWM + Dirección por motor
- **Protección**: Diodos flyback integrados
- **Enable**: Jumpers habilitación canales

## 4. Instalación y Configuración

### Requisitos del Sistema
- **Python**: 3.8 o superior
- **PySide6**: Framework Qt6 para interfaz gráfica
- **socket**: Comunicación TCP (incluido en Python)
- **typing**: Type hints (Python 3.5+)

### Instalación Dependencias
```bash
pip install PySide6
```

### Configuración ESP32
1. **Programar firmware**: Incluir modo IR_STEERING
2. **Calibrar sensores**: Ajustar umbral detección línea
3. **Configurar red**: Conectar WiFi y anotar IP
4. **Test motores**: Verificar dirección y encoders

### Estructura de Archivos
```
irSteering/
├── irSteering_logic.py        # Lógica principal y control PID
├── irSteering_ui.py          # Interfaz gráfica generada
└── irSteering.ui             # Diseño Qt Designer
```

### Configuración Mecánica
- **Distancia sensores**: 10-15mm para línea estándar
- **Altura sensores**: 3-8mm sobre superficie
- **Ancho chasis**: Compatible con separación ruedas
- **Centro gravedad**: Bajo para estabilidad direccional

## 5. Manual de Usuario

### Inicio del Sistema
1. **Encender robot**: Verificar alimentación motores y ESP32
2. **Abrir aplicación** SENSORA CORE
3. **Seleccionar módulo** "IR STEERING"
4. **Introducir IP** del ESP32
5. **Verificar sensores**: Observar estado en interfaz

### Interfaz de Usuario
- **Panel Superior**: Título y descripción del módulo
- **Panel Izquierdo**: Diagrama conexiones y notas técnicas
- **Panel Derecho**: Estado sensores IR y lecturas RPM
- **Controles**: Iniciar/pausar y configuración PID

### Estado de Sensores IR
Los 5 sensores se muestran como indicadores visuales:
- **Verde**: Sensor detecta línea (estado '1')
- **Gris**: Sensor no detecta línea (estado '0')
- **Patrón típico**: Solo sensores sobre línea activos

### Configuración PID y Velocidad
1. **Abrir diálogo**: Presionar "PID y Velocidad..."
2. **Ajustar Kp**: Respuesta proporcional (1.0 típico)
3. **Ajustar Ki**: Acumulación error (0.0-0.1 típico)
4. **Ajustar Kd**: Anticipación (0.5 típico)
5. **Velocidad base**: 20-60% para inicio
6. **Aplicar en vivo**: Checkbox para ajuste tiempo real

### Proceso de Operación
1. **Posicionar robot**: Sensores centrados sobre línea
2. **Iniciar monitoreo**: Presionar "Iniciar Monitoreo"
3. **Observar comportamiento**: Robot debe seguir línea suavemente
4. **Ajustar PID**: Modificar parámetros según respuesta
5. **Monitorear RPM**: Verificar funcionamiento motores

## 6. Algoritmos y Procesamiento

### Algoritmo de Detección de Error
```python
def calculate_error(sensors):
    # Sensores: [IR1, IR2, IR3, IR4, IR5]
    # Posiciones: [-2, -1, 0, 1, 2]
    positions = [-2, -1, 0, 1, 2]
    weighted_sum = 0
    total_active = 0
    
    for i, sensor in enumerate(sensors):
        if sensor == '1':
            weighted_sum += positions[i]
            total_active += 1
    
    if total_active > 0:
        error = weighted_sum / total_active
    else:
        error = 0  # Sin línea detectada
    
    return error
```

### Control PID Implementado
```python
class PIDController:
    def __init__(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.prev_error = 0
        self.integral = 0
    
    def calculate(self, error, dt):
        # Proporcional
        P = self.kp * error
        
        # Integral
        self.integral += error * dt
        I = self.ki * self.integral
        
        # Derivativo
        derivative = (error - self.prev_error) / dt
        D = self.kd * derivative
        
        # Salida PID
        output = P + I + D
        self.prev_error = error
        
        return output
```

### Control Diferencial de Motores
```python
def calculate_motor_speeds(base_speed, pid_output):
    # Aplicar corrección diferencial
    left_speed = base_speed - pid_output
    right_speed = base_speed + pid_output
    
    # Limitar a rango [-100, 100]
    left_speed = max(-100, min(100, left_speed))
    right_speed = max(-100, min(100, right_speed))
    
    return left_speed, right_speed
```

### Comunicación TCP
```python
# Comandos enviados al ESP32
"MODO:IR_STEERING"
"SET_BASE:40"
"SET_PID:Kp=1.000,Ki=0.000,Kd=0.500"

# Datos recibidos del ESP32
"SENS:00100,ERR:0.0,OUT_L:40,OUT_R:40,SPEED:40,RPM_L:85,RPM_R:88"
```

## 7. Validación y Calibración

### Calibración de Sensores IR
1. **Superficie clara**: Todos sensores deben leer '0'
2. **Línea negra**: Solo sensores sobre línea leen '1'
3. **Umbral detección**: Ajustar comparadores para línea específica
4. **Espaciado**: Verificar detección gradual al cruzar línea

### Calibración del Sistema PID
**Método Ziegler-Nichols Simplificado**:
1. **Ki = Kd = 0**: Anular integral y derivativo
2. **Aumentar Kp**: Hasta oscilación sostenida
3. **Kp crítico**: Valor donde inicia oscilación
4. **Ajuste fino**: Kp = 0.6 * Kp_crítico
5. **Agregar Kd**: 10-20% de Kp para suavizar
6. **Agregar Ki**: Pequeño (0.01-0.1) si hay error residual

### Validación de Rendimiento
- **Tiempo respuesta**: Robot debe corregir en < 0.5 segundos
- **Overshoot**: Máximo 20% sobrepaso en curvas
- **Estabilidad**: Sin oscilaciones en rectas largas
- **Precisión**: Mantener línea central ±10mm

### Métricas de Control
- **Error RMS**: < 0.5 unidades promedio
- **Velocidad máxima**: Sin pérdida seguimiento
- **Radio curva mínimo**: Dependiente velocidad base
- **Tiempo establecimiento**: < 1 segundo después perturbación

## 8. Aplicaciones Educativas

### Sistemas de Control Automático
- **Control retroalimentado**: Conceptos PID prácticos
- **Estabilidad sistemas**: Análisis respuesta temporal
- **Sintonización controladores**: Métodos experimentales
- **Robustez**: Respuesta a perturbaciones

### Robótica Móvil
- **Navegación autónoma**: Seguimiento trayectorias
- **Sensores de proximidad**: Detección obstáculos
- **Control diferencial**: Cinemática robot móvil
- **Planificación movimiento**: Algoritmos path-following

### Instrumentación y Medición
- **Sensores IR**: Principios optoelectrónicos
- **Encoders**: Medición velocidad angular
- **PWM**: Modulación ancho pulso para control
- **Comunicación**: Protocolos tiempo real

### Proyectos de Ingeniería
- **Robot seguidor línea**: Competencias estudiantiles
- **Vehículo autónomo**: Prototipo escalado
- **Sistema control**: Implementación industrial
- **Investigación**: Algoritmos control avanzado

## 9. Mantenimiento y Solución de Problemas

### Mantenimiento Preventivo
- **Limpieza sensores**: Alcohol isopropílico semanal
- **Calibración**: Verificar umbral detección mensual
- **Mecánica**: Lubricar rodamientos y alineación ruedas
- **Eléctrica**: Verificar conexiones y soldaduras

### Problemas Comunes
**Robot no sigue línea**:
- Verificar calibración sensores IR
- Ajustar altura sensores (3-8mm)
- Revisar parámetros PID iniciales
- Confirmar funcionamiento motores

**Oscilaciones excesivas**:
- Reducir Kp (ganancia proporcional)
- Aumentar Kd (amortiguamiento)
- Verificar rigidez mecánica chasis
- Reducir velocidad base

**Pérdida línea en curvas**:
- Aumentar velocidad base moderadamente
- Reducir Kd para respuesta más rápida
- Verificar espaciado sensores
- Ajustar radio curvas del circuito

**Motores no responden**:
- Verificar alimentación 12V driver L298N
- Comprobar conexiones PWM y dirección
- Test individual motores con comandos directos
- Revisar enable jumpers driver

### Diagnóstico Avanzado
```python
# Verificación estado sensores
print(f"Sensores IR: {sensors_binary}")
print(f"Error calculado: {error:.3f}")
print(f"Salida PID: {pid_output:.3f}")

# Verificación motores
print(f"Motor izq: {left_pwm}% ({left_rpm} RPM)")
print(f"Motor der: {right_pwm}% ({right_rpm} RPM)")

# Estado comunicación
print(f"TCP conectado: {connected}")
print(f"Latencia: {latency_ms}ms")
```

## 10. Seguridad y Consideraciones

### Seguridad Eléctrica
- **Alimentación dual**: 12V motores aislada de 3.3V lógica
- **Protección**: Fusibles 3A (motores) + 500mA (lógica)
- **Driver motores**: L298N con protección térmica
- **Conexiones**: Terminales seguros para alta corriente

### Seguridad Mecánica
- **Velocidad limitada**: Máximo 1 m/s para seguridad
- **Parada emergencia**: Comando STOP inmediato
- **Bordes redondeados**: Evitar lesiones por contacto
- **Base estable**: Centro gravedad bajo

### Consideraciones Operativas
- **Superficie**: Lisa y uniforme para sensores IR
- **Iluminación**: Evitar IR externo (sol directo)
- **Espacio operación**: Área libre de obstáculos
- **Supervisión**: Operador presente durante pruebas

### Protección del Sistema
- **Límites software**: Velocidad y aceleración máximas
- **Timeout comunicación**: Parada automática si se pierde TCP
- **Monitoreo térmico**: Detección sobrecalentamiento motores
- **Watchdog**: Reset automático en caso de bloqueo

## 11. Conclusiones

El módulo **SENSORA_IR_STEERING** proporciona una plataforma completa para el aprendizaje y desarrollo de sistemas de control automático aplicados a robótica móvil. Su diseño modular permite desde aplicaciones educativas básicas hasta investigación avanzada en algoritmos de control.

### Ventajas Clave
- **Flexibilidad**: Parámetros PID ajustables en tiempo real
- **Robustez**: Control diferencial con retroalimentación RPM
- **Usabilidad**: Interfaz gráfica intuitiva para configuración
- **Escalabilidad**: Base para desarrollos más complejos

### Limitaciones Conocidas
- **Dependencia iluminación**: Sensores IR sensibles a luz ambiente
- **Tipo línea**: Optimizado para líneas negras sobre fondo claro
- **Velocidad máxima**: Limitada por tiempo respuesta sistema
- **Curvas cerradas**: Radio mínimo dependiente de configuración

### Desarrollos Futuros
- Algoritmos control adaptativo auto-sintonizable
- Integración sensores adicionales (ultrasonido, cámara)
- Control predictivo basado en modelo (MPC)
- Navegación por waypoints con GPS
- Comunicación multi-robot para enjambres

### Impacto Educativo
El sistema establecido proporciona una base sólida para la comprensión práctica de conceptos fundamentales en:
- Teoría de control automático
- Robótica móvil y navegación
- Integración hardware-software
- Instrumentación y sistemas embebidos

Esta plataforma facilita la transición desde conceptos teóricos hacia implementaciones prácticas, preparando a estudiantes para desafíos reales en ingeniería de control y robótica.
