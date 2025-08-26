# Manual de Usuario - SENSORA COLOR TCS

## 1. Introducción

El módulo **SENSORA_COLOR_TCS** representa una solución avanzada para la detección y análisis de color utilizando el sensor **TCS3200**. Este sensor de color de alta precisión convierte la intensidad lumínica en frecuencia, permitiendo mediciones RGB exactas para aplicaciones industriales, educativas y de investigación.

### Características Principales
- **Sensor**: TCS3200 con fotodiodos y filtros RGB integrados
- **Medición**: Conversión luz-frecuencia con salida digital
- **Calibración**: Sistema de 5 puntos (blanco, negro, rojo, verde, azul)
- **Visualización**: Gráficas RGB en tiempo real (0-255)
- **Exportación**: Datos completos en formato Excel con metadatos
- **Comunicación**: TCP/IP con ESP32 para streaming continuo

### Aplicaciones
- Control de calidad en producción
- Clasificación automática por color
- Análisis espectral básico
- Monitoreo de procesos industriales
- Educación en óptica y electrónica

## 2. Especificaciones Técnicas

### Sensor TCS3200
- **Rango espectral**: 700-1000 nm
- **Resolución**: 16 fotodiodos con filtros RGB y clear
- **Salida**: Frecuencia proporcional a intensidad lumínica
- **Alimentación**: 3.3V DC
- **Consumo**: < 10 mA
- **Temperatura operativa**: -25°C a +70°C

### Sistema de Comunicación
- **Protocolo**: TCP/IP over WiFi
- **Comando inicial**: "MODO:COLOR_TCS"
- **Streaming**: Configurable desde 150ms
- **Formato datos**: "SENSOR:TCS3200,R:<hz>,G:<hz>,B:<hz>"
- **Puerto**: 8080 (configurable)

### Algoritmo de Calibración
- **Mapeo dinámico**: Min/max por sesión (modo no calibrado)
- **Calibración completa**: Escalado 0-255 con referencias de color
- **Compensación**: Ganancia por canal basada en colores puros
- **Persistencia**: Calibración guardada en JSON local

## 3. Compatibilidad de Hardware

### Microcontrolador Requerido
- **ESP32 DevKit V1** o compatible
- **WiFi**: 802.11 b/g/n
- **Flash**: Mínimo 4MB
- **RAM**: Mínimo 520KB
- **Pines GPIO**: 6 pines digitales

### Conexiones TCS3200
```
ESP32 Pin    TCS3200 Pin    Función
3V3      →   VCC           Alimentación
GND      →   GND           Tierra
D36      ↔   S0            Escala frecuencia
D39      ↔   S1            Escala frecuencia  
D34      ↔   S2            Selección filtro
D35      ↔   S3            Selección filtro
D32      ←   OUT           Salida frecuencia
```

### Configuración de Escalado
- **S0=1, S1=1**: Frecuencia completa (recomendado)
- **S0=1, S1=0**: Frecuencia al 20%
- **S0=0, S1=1**: Frecuencia al 2%
- **S0=0, S1=0**: Sensor apagado

## 4. Instalación y Configuración

### Requisitos del Sistema
- **Python**: 3.8 o superior
- **PySide6**: Framework Qt para interfaz gráfica
- **matplotlib**: Visualización de datos científicos
- **openpyxl**: Exportación a Excel
- **socket**: Comunicación TCP (incluido en Python)

### Instalación de Dependencias
```bash
pip install PySide6 matplotlib openpyxl
```

### Configuración de Red
1. **Configurar ESP32**: Programar con firmware TCS3200
2. **Red WiFi**: Conectar ESP32 y PC a misma red
3. **IP del ESP32**: Anotar dirección asignada
4. **Puerto**: Verificar puerto 8080 abierto

### Estructura de Archivos
```
colorTCS/
├── colorTCS_logic.py        # Lógica principal y comunicación
├── colorTCS_ui.py          # Interfaz gráfica generada
├── colorTCS.ui             # Diseño Qt Designer
└── colorTCS_calibration.json # Datos de calibración (auto-generado)
```

## 5. Manual de Usuario

### Inicio del Sistema
1. **Abrir aplicación** SENSORA CORE
2. **Seleccionar módulo** "COLOR TCS"
3. **Verificar conexión** del sensor TCS3200
4. **Introducir IP** del ESP32 en campo correspondiente

### Interfaz de Usuario
- **Panel Superior**: Título y descripción del módulo
- **Panel Controles**: Botones de operación y datos RGB
- **Panel Diagrama**: Esquema de conexiones
- **Panel Gráfica**: Visualización temporal RGB

### Proceso de Calibración
1. **Iniciar calibración**: Presionar "No Calibrado"
2. **Blanco de referencia**: Colocar objeto blanco y capturar
3. **Negro de referencia**: Colocar objeto negro y capturar
4. **Rojo puro**: Colocar objeto rojo y capturar
5. **Verde puro**: Colocar objeto verde y capturar
6. **Azul puro**: Colocar objeto azul y capturar
7. **Completar**: Calibración guardada automáticamente

### Monitoreo en Tiempo Real
1. **Iniciar streaming**: Presionar "Iniciar Monitoreo"
2. **Observar datos**: Valores Hz (crudo) y 0-255 (calibrado)
3. **Analizar gráfica**: Líneas RGB con ventana deslizante 25s
4. **Pausar**: Detener streaming manteniendo datos

### Exportación de Datos
1. **Recopilar datos**: Ejecutar sesión de monitoreo
2. **Exportar Excel**: Presionar "Exportar a Excel"
3. **Seleccionar ubicación**: Elegir carpeta de destino
4. **Archivo generado**: ColorTCS_YYYYMMDD_HHMMSS.xlsx

## 6. Algoritmos y Procesamiento

### Comunicación TCP
```python
# Inicialización
socket.connect((ip, 8080))
socket.sendall(b"MODO:COLOR_TCS\n")
socket.sendall(f"TCS_START:{interval_ms}\n".encode())

# Recepción de datos
"SENSOR:TCS3200,R:<hz>,G:<hz>,B:<hz>"
```

### Conversión a Escala 0-255
**Modo No Calibrado (Dinámico)**:
```python
def dyn_map(v, ch):
    lo = min_sesion[ch]
    hi = max_sesion[ch]
    x = (v - lo) / (hi - lo)
    return x * 255.0
```

**Modo Calibrado (5 Referencias)**:
```python
def to_255_calibrated(r_hz, g_hz, b_hz):
    # 1. Escalado base [negro, blanco]
    r_base = (r_hz - black_r) / (white_r - black_r)
    g_base = (g_hz - black_g) / (white_g - black_g)
    b_base = (b_hz - black_b) / (white_b - black_b)
    
    # 2. Ganancia por color puro
    gain_r = 1.0 / red_reference_intensity
    gain_g = 1.0 / green_reference_intensity
    gain_b = 1.0 / blue_reference_intensity
    
    # 3. Aplicar compensación
    return 255 * r_base * gain_r, 255 * g_base * gain_g, 255 * b_base * gain_b
```

### Visualización Matplotlib
- **Tres líneas**: Rojo (#ff0000), Verde (#00aa00), Azul (#0000ff)
- **Eje X**: Tiempo relativo en segundos
- **Eje Y**: Valores 0-255 (fijo)
- **Ventana**: 25 segundos deslizante
- **Actualización**: Tiempo real con draw_idle()

## 7. Validación y Calibración

### Protocolo de Validación
1. **Verificación hardware**: Continuidad y alimentación
2. **Test comunicación**: Ping IP y respuesta puerto 8080
3. **Calibración completa**: 5 referencias capturadas
4. **Prueba repetibilidad**: 10 mediciones mismo objeto
5. **Rango dinámico**: Medición blanco-negro extremos

### Métricas de Calidad
- **Estabilidad**: Desviación < 5% en 60 segundos
- **Reproducibilidad**: CV < 3% en 10 repeticiones
- **Linealidad**: R² > 0.95 en degradado gris
- **Resolución**: Mínima diferencia detectable 1 unidad RGB

### Calibración de Mantenimiento
- **Frecuencia**: Semanal en uso continuo
- **Referencias**: Tarjetas de color certificadas
- **Condiciones**: Iluminación controlada D65
- **Documentación**: Log de calibraciones con timestamp

## 8. Aplicaciones Educativas

### Laboratorio de Óptica
- **Espectro visible**: Análisis de componentes RGB
- **Ley Beer-Lambert**: Absorción vs concentración
- **Temperatura color**: Caracterización de fuentes lumínicas
- **Metamerismo**: Colores perceptualmente iguales

### Instrumentación Científica
- **Colorimetría**: Medición objetiva de color
- **Fotometría**: Intensidad lumínica relativa
- **Espectrofotometría**: Análisis espectral básico
- **Sensores**: Principios de transducción

### Proyectos Aplicados
- **Control calidad**: Clasificación automática
- **Robótica**: Seguimiento por color
- **Proceso industrial**: Monitoreo continuo
- **Arte digital**: Análisis de pigmentos

## 9. Mantenimiento y Solución de Problemas

### Mantenimiento Preventivo
- **Limpieza sensor**: Alcohol isopropílico y aire comprimido
- **Verificación conexiones**: Continuidad y soldaduras
- **Actualización firmware**: ESP32 y PC aplicación
- **Backup calibración**: Copia archivos JSON

### Problemas Comunes
**Sin comunicación**:
- Verificar IP y puerto ESP32
- Confirmar conexión WiFi
- Revisar firewall PC

**Mediciones erráticas**:
- Recalibrar sensor completo
- Verificar estabilidad alimentación
- Revisar interferencias lumínicas

**Drift temporal**:
- Tiempo calentamiento 5 minutos
- Compensación temperatura ambiente
- Recalibración periódica

### Diagnóstico Avanzado
```python
# Test de rangos
print(f"R: {min_r}-{max_r} Hz")
print(f"G: {min_g}-{max_g} Hz") 
print(f"B: {min_b}-{max_b} Hz")

# Verificación calibración
if calibrated:
    print("Calibración válida")
else:
    print("Requiere calibración")
```

## 10. Seguridad y Consideraciones

### Seguridad Eléctrica
- **Voltaje seguro**: 3.3V DC únicamente
- **Protección**: Fusible 100mA recomendado
- **Aislamiento**: Evitar contacto con circuitos AC
- **ESD**: Procedimientos antiestáticos

### Seguridad Óptica
- **Intensidad lumínica**: Máximo 1000 lux
- **LED de alta potencia**: Usar difusores
- **Laser**: Prohibido uso directo
- **UV**: Evitar exposición prolongada

### Consideraciones Ambientales
- **Temperatura**: 0°C a 40°C operación
- **Humedad**: < 85% HR sin condensación
- **Vibración**: < 2g RMS
- **Campos magnéticos**: Alejar de motores

### Protección de Datos
- **Calibración**: Backup automático recomendado
- **Datos experimentales**: Encriptación opcional
- **Red**: WPA2 mínimo para WiFi
- **Acceso**: Controlar IP autorizadas

## 11. Conclusiones

El módulo **SENSORA_COLOR_TCS** constituye una herramienta versátil y precisa para aplicaciones de detección y análisis de color. Su diseño modular permite adaptación a diversos entornos, desde laboratorios educativos hasta sistemas industriales de control de calidad.

### Ventajas Clave
- **Precisión**: Calibración multi-punto con referencias certificadas
- **Flexibilidad**: Modo dinámico y calibrado según aplicación
- **Integración**: Comunicación TCP/IP para sistemas distribuidos
- **Usabilidad**: Interfaz intuitiva con visualización tiempo real

### Limitaciones
- **Iluminación**: Sensible a condiciones ambientales
- **Calibración**: Requiere referencias de color de calidad
- **Rango**: Limitado a espectro visible (700-1000 nm)
- **Temperatura**: Deriva térmica requiere compensación

### Desarrollos Futuros
- Compensación automática de temperatura
- Calibración en línea con referencias internas
- Expansión a espectro NIR
- Integración con sistemas de visión artificial

El sistema proporciona una base sólida para el desarrollo de aplicaciones avanzadas en colorimetría, con potencial de expansión hacia instrumentación científica especializada.
