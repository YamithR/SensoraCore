# Configuración rápida de SensoraCore

## 🚀 Inicio Rápido

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

### 3. Usar Sensor de Ángulo

1. **Conectar potenciómetro**:
   - Pin + → 3.3V (ESP32)
   - Pin - → GND (ESP32)  
   - Pin S → GPIO 32 (ESP32)

2. **Activar modo**:
   - Marca "Modo Ángulo Simple"
   - Gira el potenciómetro
   - Ve los datos en tiempo real

3. **Exportar datos**:
   - Presiona "Exportar datos a Excel"
   - Elige ubicación del archivo

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
