# Configuración rápida de SensoraCore Alpha 0.2.3

## 🚀 Inicio Rápido - Interfaces Digital/Analógica Unificada con Correcciones de Dependencias y Excel

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

### 3. Usar Sensores Alpha 0.2.3

1. **Conectar sensores**:
   - **Potenciómetro (Analógico)**: Pin + → 3.3V, Pin - → GND, Pin S → GPIO 32
   - **Sensor IR (Digital)**: VCC → 3.3V, GND → GND, OUT → GPIO 14  
   - **Sensor Capacitivo (Digital)**: VCC → 3.3V, GND → GND, OUT → GPIO 35
   - **Sensor Ultrasónico (Analógico)**: VCC → 5V, GND → GND, Trig → GPIO 26, Echo → GPIO 27

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

4. **Reiniciar interfaz**:
   - Usa el botón "🔄 Reiniciar Interfaz" para limpiar todo
   - Mantiene la conexión ESP32 pero resetea la interfaz completa
   - Ideal para empezar nuevas mediciones sin reconectar

### 4. Nuevas Funciones Alpha 0.2.3

1. **Interfaz Digital Unificada**:
   - Sensores IR y Capacitivo ahora con salida digital ON/OFF
   - Indicadores visuales claros para estados digitales
   - Protocolo simplificado: IR_DIGITAL:True/False, CAP_DIGITAL:True/False

2. **Sensor Ultrasónico Implementado**:
   - Medición de distancia con gráficas en tiempo real
   - Comando MODO:DISTANCIA_ULTRA para activación
   - Rango de medición optimizado para aplicaciones didácticas

3. **Correcciones Críticas Alpha 0.2.3**:
   - ✅ **Dependencias de interfaces resueltas**: Eliminados errores de inicialización
   - ✅ **Exportación Excel corregida**: Nombres de columnas y posicionamiento de gráficas
   - ✅ **Calls setVisible() agregadas**: Interfaces se muestran correctamente
   - ✅ **Indentación corregida**: Código Python sin errores de sintaxis

### 5. Usar Sensores de Distancia Actualizados

1. **Sensor IR Digital (Sharp GP2Y0A21YK)**:   - VCC → 3.3V, GND → GND, OUT → GPIO 14
   - **NUEVO**: Salida digital True/False según detección
   - Ideal para detección de presencia/ausencia

2. **Sensor Capacitivo Digital**:
   - VCC → 3.3V, GND → GND, OUT → GPIO 35  
   - **NUEVO**: Salida digital True/False según proximidad
   - Ideal para detección de materiales no metálicos

3. **Sensor Ultrasónico (HC-SR04)**:
   - VCC → 5V, GND → GND, Trig → GPIO 26, Echo → GPIO 27
   - **NUEVO EN ALPHA 0.2**: Medición analógica con gráficas
   - Rango: 2-400 cm, ideal para mediciones de distancia precisas

### 6. Mejoras en Alpha 0.2.3

1. **Gráficas Corregidas (desde 0.2.2)**:
   - ✅ **Solucionado**: Las gráficas ahora se muestran correctamente desde el primer uso
   - ✅ **Renderizado mejorado**: Canvas inicializado automáticamente
   - ✅ **Sin pantallas en blanco**: Visualización inmediata al seleccionar sensores

2. **Correcciones Críticas Alpha 0.2.3**:
   - ✅ **Interfaces de sensores estables**: Resueltas todas las dependencias faltantes
   - ✅ **Excel totalmente funcional**: Exportación sin errores de columnas
   - ✅ **Posicionamiento correcto**: Gráficas en Excel en posiciones adecuadas
   - ✅ **Código optimizado**: Eliminados errores de indentación y sintaxis

3. **Estabilidad Mejorada**:
   - Interfaces de sensores analógicos más robustas
   - Mejor experiencia de usuario al cambiar entre sensores
   - Corrección completa de problemas de visualización en matplotlib
   - Sistema de exportación Excel completamente estable

## 🔧 Solución de Problemas Comunes

### ❌ Problemas Resueltos en Alpha 0.2.3

1. **Interfaces de sensores no aparecen (SOLUCIONADO)**:
   - **Síntoma**: Ventanas de sensores no se mostraban al seleccionar modos
   - **Causa**: Faltaban llamadas setVisible() en la inicialización
   - **Solución**: Actualiza a Alpha 0.2.3 - problema completamente resuelto

2. **Error al exportar Excel con brazo robótico (SOLUCIONADO)**:
   - **Síntoma**: Crash al exportar datos del sensor "Brazo Ángulos"
   - **Causa**: Nombres de columnas incorrectos en el código de exportación
   - **Solución**: Actualiza a Alpha 0.2.3 - exportación Excel completamente funcional

3. **Gráficas mal posicionadas en Excel (SOLUCIONADO)**:
   - **Síntoma**: Gráficas aparecían en posiciones incorrectas del archivo Excel
   - **Causa**: Coordenadas de inserción incorrectas
   - **Solución**: Actualiza a Alpha 0.2.3 - posicionamiento correcto implementado

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
- **Nueva en 0.2.3**: Todas las interfaces de sensores ahora se muestran correctamente desde el primer uso
- **Exportación estable**: El sistema de exportación Excel funciona sin errores para todos los sensores

## 📞 Soporte

Si encuentras problemas:
1. Verifica las conexiones físicas
2. Revisa la configuración WiFi
3. Verifica que las dependencias estén instaladas
4. Reinicia tanto ESP32 como la aplicación
