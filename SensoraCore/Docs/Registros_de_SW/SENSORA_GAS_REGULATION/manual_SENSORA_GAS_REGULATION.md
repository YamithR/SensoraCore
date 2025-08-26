# Manual de Usuario - SENSORA GAS REGULATION

## 1. Introducción

El módulo **SENSORA_GAS_REGULATION** proporciona una solución completa para el monitoreo y análisis de concentraciones de gases utilizando sensores electroquímicos de la serie MQ. Este sistema está diseñado para aplicaciones de seguridad industrial, control ambiental y monitoreo de calidad del aire, ofreciendo mediciones precisas en tiempo real con capacidades de calibración avanzadas.

### Características Principales
- **Sensores**: MQ2 (humo/gases combustibles) y MQ3 (alcohol/etanol)
- **Medición**: Conversión analógica ADC 12-bit (0-4095) y voltaje (0-3.3V)
- **Calibración**: Sistema matemático basado en ecuaciones logarítmicas Rs/Ro
- **Visualización**: Gráficas PPM en tiempo real con dos canales
- **Exportación**: Datos completos en Excel con hoja de calibración
- **Comunicación**: TCP/IP con ESP32 y selección dinámica de sensor

### Aplicaciones
- Detección de humo y gases combustibles (MQ2)
- Monitoreo de concentración de alcohol (MQ3)
- Sistemas de alarma para seguridad industrial
- Control de calidad en procesos industriales
- Monitoreo ambiental continuo
- Aplicaciones educativas en química analítica

## 2. Especificaciones Técnicas

### Sensores MQ2 y MQ3
**MQ2 (Sensor de Humo/Gases Combustibles)**:
- **Gases detectables**: LPG, propano, metano, hidrógeno, humo
- **Rango**: 200-10,000 ppm
- **Temperatura operativa**: -10°C a 50°C
- **Humedad**: 5% a 95% RH (sin condensación)
- **Tiempo de respuesta**: < 10 segundos

**MQ3 (Sensor de Alcohol)**:
- **Gases detectables**: Etanol, alcohol etílico, vapor de alcohol
- **Rango**: 0.05-10 mg/L (equivalente a 50-10,000 ppm)
- **Selectividad**: Alta sensibilidad al alcohol, baja interferencia
- **Tiempo de respuesta**: < 10 segundos
- **Recuperación**: < 30 segundos

### Especificaciones Eléctricas
- **Alimentación**: 5V DC (heater) + 3.3V DC (lógica)
- **Consumo**: 150mA (heater) + 5mA (lógica)
- **Resistencia de carga (RL)**: 10kΩ (configurable)
- **Resistencia sensor (Rs)**: Variable según concentración
- **Salida**: Voltaje analógico 0-3.3V proporcional a concentración

### Sistema de Comunicación
- **Protocolo**: TCP/IP sobre WiFi
- **Comando inicial**: "MODO:GAS_REGULATION"
- **Configuración sensor**: "GR_SET:MQ2" o "GR_SET:MQ3"
- **Streaming**: "GR_START:500" (intervalo configurable 200-5000ms)
- **Formato datos**: "SENSOR:MQ2,ADC:2048,VOLT:1.65"
- **Puerto**: 8080 (estándar)

## 3. Compatibilidad de Hardware

### Microcontrolador Requerido
- **ESP32 DevKit V1** o compatible
- **ADC**: 12-bit resolución (4096 niveles)
- **WiFi**: 802.11 b/g/n para comunicación
- **GPIO**: 2 pines analógicos mínimo
- **Alimentación**: Dual 3.3V + 5V para sensores

### Conexiones Sensores MQ
```
ESP32 Pin    Sensor MQ    Función
5V       →   VCC         Alimentación heater
3V3      →   VCC_Logic   Alimentación lógica
GND      →   GND         Tierra común
D36/VP   ←   A0          Salida analógica MQ2
D39/VN   ←   A0          Salida analógica MQ3
```

### Circuito de Acondicionamiento
```
       Vcc (3.3V)
          |
         RL (10kΩ)
          |
    ------+------ Vout (a ESP32)
          |
        Sensor MQ
          |
         GND
```

### Tiempo de Precalentamiento
- **MQ2**: 20 segundos mínimo, 48 horas estabilización completa
- **MQ3**: 48 horas para calibración inicial
- **Operación continua**: Recomendada para estabilidad

## 4. Instalación y Configuración

### Requisitos del Sistema
- **Python**: 3.8 o superior
- **PySide6**: Framework Qt6 para interfaz gráfica
- **matplotlib**: Visualización científica
- **openpyxl**: Exportación a Excel
- **dataclasses**: Manejo de estructuras de datos (Python 3.7+)

### Instalación de Dependencias
```bash
pip install PySide6 matplotlib openpyxl
```

### Configuración ESP32
1. **Programar firmware**: Incluir soporte GAS_REGULATION
2. **Configurar WiFi**: Conectar a red local
3. **Verificar IP**: Anotar dirección IP asignada
4. **Test comunicación**: Verificar puerto 8080 accesible

### Estructura de Archivos
```
gasRegulation/
├── gasRegulation_logic.py     # Lógica principal y algoritmos
├── gasRegulation_ui.py        # Interfaz gráfica generada Qt
├── gasRegulation.ui           # Diseño visual Qt Designer
└── ~/.sensora_core/gas_calib.json  # Calibraciones persistentes
```

### Configuración de Calibración
El archivo de calibración se guarda automáticamente en:
- **Windows**: `C:\Users\{user}\.sensora_core\gas_calib.json`
- **Linux/Mac**: `~/.sensora_core/gas_calib.json`

## 5. Manual de Usuario

### Inicio del Sistema
1. **Abrir aplicación** SENSORA CORE
2. **Seleccionar módulo** "GAS REGULATION"
3. **Precalentar sensores** MQ2/MQ3 (mínimo 20 segundos)
4. **Introducir IP** del ESP32 en campo principal
5. **Verificar conexión** antes de iniciar monitoreo

### Interfaz de Usuario
- **Panel Superior**: Título y descripción del módulo
- **Panel Izquierdo**: Selector de sensores y datos en tiempo real
- **Panel Central**: Gráfica concentración PPM temporal
- **Controles**: Iniciar/pausar, limpiar, exportar, calibrar

### Selección de Sensor
1. **MQ2**: Presionar botón "MQ2" (activación exclusiva)
2. **MQ3**: Presionar botón "MQ3" (desactiva MQ2)
3. **Indicador visual**: Botón seleccionado se resalta
4. **Cambio dinámico**: Posible durante monitoreo activo

### Proceso de Calibración
**Calibración Básica (Solo Ro)**:
1. **Ambiente limpio**: Colocar sensor en aire puro
2. **Presionar "Calibrar"**: Introducir valor Ro en Ω
3. **Confirmar**: Valor se guarda automáticamente

**Calibración Completa (Ecuación PPM)**:
1. **Iniciar calibración avanzada**: Especificar 2+ puntos
2. **Punto 1**: Introducir Rs actual y PPM de referencia
3. **Punto 2**: Repetir con concentración diferente
4. **Puntos adicionales**: Opcional para mejor precisión
5. **Ajuste automático**: Sistema calcula m y b de ecuación logarítmica

### Monitoreo en Tiempo Real
1. **Iniciar streaming**: Presionar "Iniciar Monitoreo"
2. **Observar datos**: ADC crudo, voltaje y PPM calibrado
3. **Analizar gráfica**: Líneas MQ2 y MQ3 diferenciadas
4. **Cambiar sensor**: Selección dinámica durante operación
5. **Pausar**: Detener streaming manteniendo datos históricos

## 6. Algoritmos y Procesamiento

### Ecuación Fundamental de Sensores MQ
```
Rs = RL * (Vcc - Vout) / Vout
```
Donde:
- **Rs**: Resistencia sensor variable con concentración
- **RL**: Resistencia de carga (10kΩ típico)
- **Vcc**: Voltaje alimentación (3.3V)
- **Vout**: Voltaje medido por ADC

### Modelo Logarítmico de Calibración
```
log10(PPM) = m * log10(Rs/Ro) + b
```
Donde:
- **Ro**: Resistencia en aire limpio (referencia)
- **m, b**: Parámetros determinados por regresión lineal
- **Rs/Ro**: Ratio normalizado para compensar deriva

### Algoritmo de Calibración
```python
def calibrate_sensor(points):
    xs = [log10(rs/ro) for rs, ppm in points]
    ys = [log10(ppm) for rs, ppm in points]
    m, b = linear_regression(xs, ys)
    return m, b

def compute_ppm(adc_value, calibration):
    volt = (adc_value / 4095.0) * 3.3
    Rs = RL * (3.3 - volt) / volt
    ratio = Rs / calibration.Ro
    return 10 ** (calibration.m * log10(ratio) + calibration.b)
```

### Comunicación TCP
```python
# Inicialización
socket.connect((ip, 8080))
socket.sendall(b"MODO:GAS_REGULATION\n")
socket.sendall(b"GR_SET:MQ2\n")  # o MQ3
socket.sendall(b"GR_START:500\n")

# Datos recibidos
"SENSOR:MQ2,ADC:2048,VOLT:1.65"
```

### Visualización en Tiempo Real
- **Líneas diferenciadas**: MQ2 y MQ3 con colores únicos
- **Eje Y**: Concentración en PPM (escala logarítmica opcional)
- **Eje X**: Tiempo relativo en segundos
- **Actualización**: Tiempo real con optimización draw_idle()

## 7. Validación y Calibración

### Protocolo de Validación
1. **Test eléctrico**: Continuidad y alimentación dual
2. **Precalentamiento**: Verificar tiempo mínimo 20 segundos
3. **Test comunicación**: Respuesta TCP y ADC readings
4. **Calibración aire limpio**: Establecer Ro de referencia
5. **Prueba concentraciones conocidas**: Validar ecuación PPM

### Calibración con Gases de Referencia
**MQ2 (Humo/Combustibles)**:
- **Punto 1**: Aire limpio (0 ppm, Rs = Ro)
- **Punto 2**: 1000 ppm LPG (gas de referencia certificado)
- **Punto 3**: 5000 ppm LPG (opcional, mejor linealidad)

**MQ3 (Alcohol)**:
- **Punto 1**: Aire limpio (0 ppm alcohol)
- **Punto 2**: 100 ppm etanol (cámara controlada)
- **Punto 3**: 1000 ppm etanol (validación rango alto)

### Métricas de Calidad
- **Repetibilidad**: CV < 10% en 10 mediciones consecutivas
- **Tiempo respuesta**: 90% valor final en < 30 segundos
- **Deriva temporal**: < 5% cambio en 8 horas continuas
- **Linealidad**: R² > 0.90 en rango calibración

### Mantenimiento de Calibración
- **Frecuencia**: Semanal en uso industrial continuo
- **Condiciones**: Temperatura 20±5°C, HR 45-65%
- **Gases patrón**: Certificados trazables a estándares nacionales
- **Documentación**: Log calibraciones con fecha y condiciones

## 8. Aplicaciones Educativas

### Laboratorio de Química Analítica
- **Principios sensores electroquímicos**: Resistencia variable
- **Calibración instrumental**: Métodos regresión lineal
- **Análisis cuantitativo**: Conversión señal a concentración
- **Control de calidad**: Validación métodos analíticos

### Instrumentación Científica
- **Transductores químicos**: Conversión química-eléctrica
- **Acondicionamiento señales**: Divisores voltaje y amplificación
- **Procesamiento digital**: ADC y algoritmos compensación
- **Sistemas de adquisición**: Comunicación tiempo real

### Proyectos de Ingeniería
- **Sistemas de alarma**: Detección automática y notificaciones
- **Control industrial**: Integración con PLCs y SCADA
- **Monitoreo ambiental**: Redes sensores distribuidos
- **Instrumentación virtual**: Interfaz usuario profesional

### Seguridad e Higiene Industrial
- **LEL (Lower Explosive Limit)**: Detección concentraciones peligrosas
- **Ventilación controlada**: Activación automática extractores
- **Registro histórico**: Cumplimiento normativas ambientales
- **Capacitación personal**: Interpretación mediciones gases

## 9. Mantenimiento y Solución de Problemas

### Mantenimiento Preventivo
- **Limpieza sensores**: Aire comprimido seco mensual
- **Verificación conexiones**: Resistencia contactos < 0.1Ω
- **Actualización firmware**: ESP32 y aplicación PC
- **Backup calibraciones**: Copia archivo gas_calib.json

### Problemas Comunes
**Lecturas errática o inestables**:
- Verificar tiempo precalentamiento mínimo
- Revisar estabilidad alimentación 5V heater
- Comprobar humedad ambiente < 90%
- Recalibrar con gases referencia frescos

**Sin comunicación TCP**:
- Confirmar IP ESP32 y conectividad red
- Verificar puerto 8080 no bloqueado firewall
- Test comunicación con ping y telnet

**Deriva temporal excesiva**:
- Envejecimiento natural sensores (2-3 años vida útil)
- Contaminación permanente por exposición gases
- Variaciones temperatura ambiente > ±10°C
- Necesidad recalibración más frecuente

### Diagnóstico Avanzado
```python
# Verificación hardware
print(f"ADC MQ2: {adc_mq2} (rango 0-4095)")
print(f"Voltaje: {voltage:.3f}V (rango 0-3.3V)")
print(f"Rs calculada: {rs:.0f}Ω")

# Estado calibración
if calibrated:
    print(f"Ro: {cal.Ro:.0f}Ω, m: {cal.m:.4f}, b: {cal.b:.4f}")
    print(f"PPM: {ppm:.2f}")
else:
    print("Sensor requiere calibración")
```

### Procedimientos de Emergencia
- **Concentraciones críticas**: Activar ventilación inmediata
- **Fallo sensor**: Protocolo backup y reemplazo
- **Pérdida comunicación**: Alarmas locales independientes
- **Contaminación masiva**: Procedimiento evacuación

## 10. Seguridad y Consideraciones

### Seguridad Eléctrica
- **Alimentación dual**: 3.3V lógica + 5V heater separadas
- **Consumo controlado**: Fusibles 200mA (lógica) + 500mA (heater)
- **Aislamiento**: Separación galvánica circuitos alta potencia
- **Protección**: Supresores transitorios alimentación

### Seguridad Química
- **Exposición controlada**: Concentraciones sub-LEL únicamente
- **Ventilación**: Circulación aire continua durante pruebas
- **Materiales peligrosos**: Almacenamiento gases patrón seguro
- **Personal capacitado**: Entrenamiento manejo gases combustibles

### Consideraciones Ambientales
- **Temperatura**: 0°C a 40°C operación, evitar gradientes térmicos
- **Humedad**: 10% a 90% RH, evitar condensación
- **Vibración**: < 1g RMS, montaje rígido sensores
- **Interferencias**: Alejar fuentes RF de alta potencia

### Protección de Datos
- **Calibraciones críticas**: Backup automático diario
- **Datos históricos**: Encriptación archivos exportados
- **Acceso controlado**: Autenticación usuarios calibración
- **Trazabilidad**: Log cambios calibración con usuario y fecha

### Normativas Aplicables
- **IEC 61508**: Seguridad funcional sistemas E/E/PE
- **ATEX**: Equipos atmósferas explosivas (donde aplique)
- **ISO 17025**: Competencia laboratorios calibración
- **Normativas locales**: Seguridad industrial específicas país

## 11. Conclusiones

El módulo **SENSORA_GAS_REGULATION** proporciona una solución robusta y versátil para el monitoreo de gases con sensores electroquímicos MQ2 y MQ3. Su diseño modular permite adaptación desde aplicaciones educativas hasta sistemas industriales críticos de seguridad.

### Ventajas Clave
- **Versatilidad**: Soporte dual MQ2/MQ3 con cambio dinámico
- **Precisión**: Calibración matemática con ecuaciones logarítmicas
- **Usabilidad**: Interfaz intuitiva con calibración asistida
- **Robustez**: Comunicación TCP con reconexión automática
- **Integración**: Exportación completa para análisis posteriores

### Limitaciones Identificadas
- **Selectividad**: Interferencias cruzadas entre gases similares
- **Deriva temporal**: Requiere recalibración periódica
- **Tiempo respuesta**: 10-30 segundos para estabilización
- **Vida útil**: Degradación gradual elementos sensores

### Desarrollos Futuros
- Compensación automática temperatura y humedad
- Algoritmos de auto-calibración con referencias internas
- Expansión a sensores MQ adicionales (MQ7, MQ135)
- Integración con sistemas de alarma y control industrial
- Mejoras selectividad mediante arrays de sensores

El sistema establecido proporciona una base sólida para aplicaciones de monitoreo de gases, con potencial de evolución hacia instrumentación analítica avanzada y sistemas de seguridad industrial integrales.
