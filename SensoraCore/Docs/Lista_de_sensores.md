# 📋 Lista de Sensores - SensoraCore

## Pines GPIO-ADC a dispocición
- **GPIO_36** : ADC1_0 
- **GPIO_39** : ADC1_3
- **GPIO_34** : ADC1_6
- **GPIO_35** : ADC1_7
- **GPIO_32** : ADC1_4
- **GPIO_33** : ADC1_5
- **GPIO_25** : ADC1_8 

## Calibración
- Regresión
  - Lineal
  - Polinómica
  - Lineal en el Espacio Logarítmico
- PID
- Caracterización 
## Exactitud
|             |Precisión|Prototipos|Educación|
|-------------|---------|----------|---------|
|Admisibilidad|   ±2%   |    ±5%   |   ±10%  |
|             |         |          |         |

### **Resolución De Microcontrolador**: 12 bits (0-4095)

### 1. Ángulo Simple (Potenciómetro)
- **Hardware**: Potenciómetro rotatorio
- **Tipo**: Analógico
- **Rango**: -135° a 135°
- **Alimentación**: 5V / 3.3V
- **Aplicaciones**: Medición de ángulos, posición angular

### 2. Brazo Robótico (3 Potenciómetros + Sensor Capacitivo)
- **Hardware**: 3 Potenciómetros + Sensor Capacitivo SCA-15
- **Tipo**: Analógico múltiple + Digital
- **Rango**: -135° a 135° (×3) + Estado ON/OFF
- **Alimentación**: 5V / 3.3V (x3) y 5V Fijo
- **Aplicaciones**: Simulación de control de brazo robótico

### 3. Distancia Ultrasónica (HC-SR04)
- **Hardware**: Sensor Ultrasónico HC-SR04
- **Tipo**: Analógico 
- **Rango**: 2-400 cm
- **Alimentación**: 5V
- **Aplicaciones**: Medición de distancia, control de proximidad

### 4. Sensor IR (E18-D80NK)
- **Hardware**: Sensor Infrarrojo E18-D80NK
- **Tipo**: Digital (ON/OFF)
- **Rango**: 3-80 cm 
- **Alimentación**: 5V
- **Aplicaciones**: Detección de objetos, robótica, sistemas de conteo

### 5. Sensor Capacitivo (SCA-15-30K30-WF/ZL)
- **Hardware**: Sensor Capacitivo SCA-15
- **Tipo**: Digital (ON/OFF)
- **Rango**: 0-40 cm (detección digital)
- **Alimentación**: 12-24V
- **Aplicaciones**: Detección industrial (metales-no metales), automatización

### 6. Velocidad Óptica (HC-020K)
- **Hardware**: Encoder óptico HC-020K
- **Tipo**: Digital (pulsos/frecuencia)
- **Rango**: 0-10000 RPM
- **Alimentación**: 5V
- **Aplicaciones**: Medición de velocidad angular, control de motores

### 7. Control Temperatura (Múltiples Sensores)

#### LM35 (Analógico)
- **Rango**: 0-100°C
- **Precisión**: ±0.5°C
- **Salida**: 10mV/°C
- **Conexión**: GPIO ADC
- **Ecuación**: Polinómica de 2° grado

#### DS18B20 (Digital)
- **Rango**: -55 a 125°C
- **Precisión**: ±0.5°C
- **Protocolo**: OneWire
- **Conexión**: GPIO con pull-up
- **Ecuación**: Calibración polinómica

#### Termopar Tipo K
- **Rango**: -200 a 1350°C
- **Precisión**: ±2.2°C
- **Requiere**: Amplificador MAX31855
- **Conexión**: SPI
- **Ecuación**: Polinómica de 3er grado

### 8. Control Gases (Sensores MQ)

#### MQ2 (Gas Combustible)
- **Gases**: LPG, Propano, Hidrógeno
- **Rango**: 200-10000 ppm
- **Tiempo calentamiento**: 20 segundos
- **Conexión**: GPIO ADC
- **Ecuación**: Polinómica (Rs/Ro vs ppm)

#### MQ3 (Alcohol)
- **Gas**: Etanol
- **Rango**: 25-500 ppm
- **Sensibilidad**: 0.05-10 mg/L
- **Conexión**: GPIO ADC
- **Ecuación**: Polinómica exponencial

### 9. Intensidad de Luz (Fotorresistencia)
- **Hardware**: LDR (Light Dependent Resistor)
- **Tipo**: Analógico resistivo
- **Conexión**: GPIO ADC con divisor de voltaje
- **Ecuación**: Polinómica logarítmica
- **Respuesta**: Logarítmica a la intensidad

### 10. Sensor Color CNY70
- **Hardware**: Sensor reflectivo CNY70
- **Tipo**: Analógico (IR + fototransistor)
- **Rango**: Detección de color por reflexión
- **Conexión**: GPIO ADC
- **Aplicaciones**: Detección de colores básicos

### 11. Sensor Color TCS3200 (Avanzado)
- **Hardware**: Sensor de color TCS3200
- **Tipo**: Digital (frecuencia)
- **Salida**: RGB independiente (0-255)
- **Conexión**: 4 GPIO (S0,S1,S2,S3) + entrada frecuencia
- **Filtros**: Rojo, Verde, Azul, Clear
- **Aplicaciones**: Análisis preciso de color RGB

### 12. Control Dirección IR (Híbrido)
- **Hardware**: TCRT5000 + HC-020K
- **Función**: Control de dirección con realimentación
- **Tipo**: Digital + Analógico
- **Aplicaciones**: Navegación robótica, seguimiento

## 📊 Especificaciones 
### Calibración por Tipo

#### Lineal (Sensores simples)
- **Ecuación**: y = mx + b
- **Mínimo puntos**: 2
- **Recomendado**: 3-5 puntos
- **Aplicable a**: Ángulo, distancia, presión

#### Polinómica (Sensores complejos)
- **Ecuación**: y = a₀ + a₁x + a₂x² + a₃x³
- **Mínimo puntos**: grado + 1
- **Recomendado**: 2×grado + 1
- **Aplicable a**: Temperatura, gases, luz, color

#### Lineal en Espacio Logarítmico
- **Ecuación**: y = m·log(x) + b
- **Mínimo puntos**: 2
- **Recomendado**: 3-5 puntos
- **Aplicable a**: Gases (MQ), sensores con respuesta logarítmica

#### PID (Controladores)
- **Ecuación**: u(t) = Kp·e(t) + Ki∫e(t)dt + Kd·de(t)/dt
- **Parámetros**: Kp (proporcional), Ki (integral), Kd (derivativo)
- **Aplicable a**: Control de temperatura, velocidad, dirección
- **Requiere**: Ajuste de parámetros para optimización

## 🔌 Esquemas de Conexión

### Divisor de Voltaje (Sensores 5V)
```
5V ────[R1]────┬────[R2]──── GND
               │
               └────── GPIO ESP32

R1 = R2 para división 1:2 (2.5V máximo)
```



| Módulo de software        | Nombre del software        | Descripción del software                                                                                                                                                                                                                                                                                      | Hardware asociado           | Sensor                                                       | Ecuación aplicada o Caracterización             |
|--------------------------|----------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------|--------------------------------------------------------------|-------------------------------------------------|
| Ángulo simple            | SENSORA_SIMPLE ANGLE       | Monitorea en tiempo real la lectura analógico digital del sensor potenciómetro conectado a un pin GPIO del microcontrolador para traducirlo a Ángulo y su posterior calibración por medio de Regresión Lineal Asistida. Incluye información didáctica para su caracterización.                            | Ángulo Simple               | Potenciómetros                                               | Regresión Lineal                                |
| Brazo Ángulos            | SENSORA_ANGLE ARM          | Monitorea en tiempo real 3 potenciómetros y un sensor capacitivo conectados a pines GPIO para traducirlo a Ángulo, incluyendo detección de presencia y calibración por Regresión Lineal Asistida.                                                                                                              | Brazo de Ángulos            | Potenciómetros y SCA-15-30K30-WF/ZL                         | Regresión Lineal                                |
| Sensor IR                | SENSORA_INFRARED           | Monitorea en tiempo real la señal digital del sensor infrarrojo y ofrece información didáctica para su caracterización.                                                                                                                                                                                       | Distancia IR, US & CC       | E18-D80NK                                                     | Caracterización                                 |
| Sensor Capacitivo        | SENSORA_CAPACITIVE         | Monitorea en tiempo real la señal digital del sensor capacitivo y ofrece información didáctica para su caracterización.                                                                                                                                                                                       | Distancia IR, US & CC       | SCA-15-30K30-WF/ZL                                           | Caracterización                                 |
| Distancia US             | SENSORA_ULTRASONIC         | Monitorea la lectura analógica del sensor ultrasónico para traducirla a distancia con calibración por Regresión Lineal Asistida. Incluye guía didáctica.                                                                                                                                                       | Distancia IR, US & CC       | HC-SR04                                                      | Regresión Lineal                                |
| Velocidad Óptica         | SENSORA_OPTICAL SPEED      | Controla y monitorea la velocidad de dos motores DC mediante PWM y sensores de herradura. Traduce a RPM y permite caracterización del encoder.                                                                                                                                                                 | Simulador Line Follower     | HC-020K                                                      | Caracterización                                 |
| Ctrl Dirección por IR    | SENSORA_IR STEERING        | Simula la dirección de dos motores DC usando 5 sensores infrarrojos y PWM. Permite calibración de la respuesta por PID.                                                                                                                                                                                       | Simulador Line Follower     | TCRT5000 y HC-020K                                           | PID                                             |
| Ctrl Temperatura         | SENSORA_THERMOREGULATION   | Monitorea temperatura usando 3 tipos de sensores. Traduce a °C con calibración por Regresión Polinómica Asistida. Incluye material didáctico.                                                                                                                                                        | Temperatura                 | LM35, Termopar Tipo K y DS18B20                             | Regresión Polinómica                            |
| Ctrl Gases               | SENSORA_GAS REGULATION     | Mide densidad de gases usando MQ2 y MQ3. Traduce a ppm con calibración por Regresión Lineal en Espacio Logarítmico. Incluye contenido didáctico.                                                                                                | Gases                       | MQ2 y MQ3                                                    | Regresión Lineal en el Espacio Logarítmico      |
| Intensidad de luz        | SENSORA_BRIGHTNESS         | Monitorea lectura analógica del sensor de fotorresistencia para su caracterización.                                                                                                                                                                                                                             | Luz & Color                 | Fotorresistencia (LDR)                                              | Caracterización                                 |
| Color CNY                | SENSORA_COLOR CNY          | Monitorea en tiempo real lectura analógica del sensor óptico CNY70 para caracterización.                                                                                                                                                                                                                       | Luz & Color                 | CNY70                                                        | Caracterización                                 |
| Color TCS                | SENSORA_COLOR TCS          | Monitorea la frecuencia de cada color del sensor TCS3200 y permite calibración por Regresión Polinómica Asistida.                                                                                                                                                                 | Luz & Color                 | TCS3200                                                     | Regresión Polinómica                            |
| Interfaz Gráfica         | SENSORA__UI                | Interfaz de usuario para selección de módulos y conexión al microcontrolador.                                                                                                                                                                                                                                   | PC-Windows                  | N/A                                                          | N/A                                             |
| Firmware de ESP32        | SENSORA_ESP FIRMWARE       | Firmware en micro Python para comunicación y adquisición de datos con ESP32.                                                                                                                                                                                                                                    | ESP Wroom 32                | N/A                                                          | N/A                                             |