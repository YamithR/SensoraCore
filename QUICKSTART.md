# Configuración rápida de SensoraCore Alpha 0.2

## 🚀 Inicio Rápido - Interfaces Digital/Analógica Unificada

### 1. Configurar ESP32

1. **WiFi Configuration** - Edita `SensoraCoreESP32/wifi_config.py`:
```python
SSID = 'CanelaYMaya'        # Tu red WiFi
PASSWORD = 'CanelayMayaEner0'  # Tu contraseña WiFi
```

2. **Subir código al ESP32**:
   - Conecta ESP32 por USB
   - Usa Thonny, uPyCraft o ampy para subir:
     - `main.py`
     - `wifi_config.py`

3. **Verificar conexión**:
   - Abre monitor serial
   - Reinicia ESP32
   - Anota la IP que aparece (ej: 192.168.1.100)

### 2. Ejecutar Aplicación

1. **Instalar dependencias**:
```powershell
cd SensoraCoreApp
pip install -r requirements.txt
```

2. **Ejecutar**:
```powershell
python main.py
```

3. **Conectar**:
   - Ingresa la IP del ESP32
   - Presiona "Conectar y encender LED integrado"
   - Si funciona, el LED del ESP32 se enciende

### 3. Usar Sensores Alpha 0.2

1. **Conectar sensores**:
   - **Potenciómetro (Analógico)**: Pin + → 3.3V, Pin - → GND, Pin S → GPIO 32
   - **Sensor IR (Digital)**: VCC → 3.3V, GND → GND, OUT → GPIO 35  
   - **Sensor Capacitivo (Digital)**: VCC → 3.3V, GND → GND, OUT → GPIO 36
   - **Sensor Ultrasónico (Analógico)**: VCC → 5V, GND → GND, Trig → GPIO 5, Echo → GPIO 18

2. **Seleccionar modo**:
   - **Sensores Digitales** (IR/Capacitivo): Estado ON/OFF
   - **Sensores Analógicos** (Ángulo/Distancia): Valores numéricos con gráficas
      - Para **Ángulo Simple**: Gira el potenciómetro (0-270°)
   - Para **Distancia IR Digital**: Estado True/False según detección
   - Para **Distancia Capacitivo Digital**: Estado True/False según proximidad  
   - Para **Distancia Ultrasónica**: Valores en cm con gráficas en tiempo real
   - Ve los datos en tiempo real con interfaces diferenciadas

3. **Exportar datos**:
   - Presiona "Exportar datos a Excel"
   - Elige ubicación del archivo

### 4. Nuevas Funciones Alpha 0.2

1. **Interfaz Digital Unificada**:
   - Sensores IR y Capacitivo ahora con salida digital ON/OFF
   - Indicadores visuales claros para estados digitales
   - Protocolo simplificado: IR_DIGITAL:True/False, CAP_DIGITAL:True/False

2. **Sensor Ultrasónico Implementado**:
   - Medición de distancia con gráficas en tiempo real
   - Comando MODO:DISTANCIA_ULTRA para activación
   - Rango de medición optimizado para aplicaciones didácticas

### 5. Usar Sensores de Distancia Actualizados

1. **Sensor IR Digital (Sharp GP2Y0A21YK)**:   - VCC → 3.3V, GND → GND, OUT → GPIO 35
   - **NUEVO**: Salida digital True/False según detección
   - Ideal para detección de presencia/ausencia

2. **Sensor Capacitivo Digital**:
   - VCC → 3.3V, GND → GND, OUT → GPIO 36  
   - **NUEVO**: Salida digital True/False según proximidad
   - Ideal para detección de materiales no metálicos

3. **Sensor Ultrasónico (HC-SR04)**:
   - VCC → 5V, GND → GND, Trig → GPIO 5, Echo → GPIO 18
   - **NUEVO EN ALPHA 0.2**: Medición analógica con gráficas
   - Rango: 2-400 cm, ideal para mediciones de distancia precisas

## 🔧 Solución de Problemas Comunes

### ESP32 no se conecta al WiFi
- Verifica SSID y contraseña en `wifi_config.py`
- Asegúrate que la red WiFi esté disponible
- Reinicia el ESP32

### App no puede conectar al ESP32
- Verifica que ESP32 esté encendido y conectado al WiFi
- Usa la IP correcta mostrada en el monitor serial
- Verifica que ambos estén en la misma red

### Error al instalar dependencias
```powershell
pip install --upgrade pip
pip install PySide6 matplotlib openpyxl
```

### Potenciómetro no funciona
- Verifica conexiones físicas
- Asegúrate de usar GPIO 32
- Verifica que el potenciómetro esté funcionando (mide con multímetro)

## 📱 IPs de Red Comunes

Si no sabes la IP de tu ESP32, busca dispositivos en tu red:
- Router web interface (usualmente 192.168.1.1 o 192.168.0.1)
- CMD: `arp -a` para ver dispositivos conectados
- Apps móviles como "Network Scanner"

## 🎯 Tips de Uso

- **Estabilidad**: Deja que el potenciómetro se estabilice antes de tomar medidas
- **Calibración**: Los valores van de 0° a 270° (rango típico de potenciómetro)
- **Datos**: La app mantiene máximo 100 puntos en pantalla para rendimiento
- **Excel**: Los archivos incluyen timestamp y estadísticas automáticas

## 📞 Soporte

Si encuentras problemas:
1. Verifica las conexiones físicas
2. Revisa la configuración WiFi
3. Verifica que las dependencias estén instaladas
4. Reinicia tanto ESP32 como la aplicación
