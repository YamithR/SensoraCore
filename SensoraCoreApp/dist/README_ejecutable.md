# SensoraCore Alpha 0.1 - Ejecutable Portable

## 📋 Descripción
SensoraCore.exe es la versión ejecutable portable Alpha 0.1 de la aplicación SensoraCore para monitoreo de sensores ESP32.

⚠️ **NOTA**: Esta es una versión Alpha preliminar. Pueden existir errores o funcionalidades incompletas.

## 🚀 Cómo usar

### 1. Requisitos
- Windows 10/11
- ESP32 configurado y conectado a la misma red WiFi que tu computadora

### 2. Instalación
1. Copia `SensoraCore.exe` a cualquier carpeta de tu computadora
2. No requiere instalación adicional

### 3. Uso
1. Asegúrate que tu ESP32 esté encendido y conectado a WiFi
2. Ejecuta `SensoraCore.exe` haciendo doble clic
3. En la aplicación:
   - Ingresa la IP de tu ESP32 en el campo correspondiente
   - Haz clic en "🔗 Conectar" 
   - Selecciona el sensor que deseas monitorear:
     - **Ángulo Simple**: Potenciómetro único (0-270°)
     - **Brazo Ángulo**: 3 potenciómetros + sensor capacitivo

### 4. Sensores Disponibles

#### 🎛️ Ángulo Simple
- Monitorea un potenciómetro como sensor de ángulo
- Rango: 0° a 270°
- Gráfica en tiempo real
- Exportación a Excel

#### 🦾 Brazo Ángulo  
- Simula un brazo robótico con 3 articulaciones
- 3 potenciómetros para diferentes ángulos
- Sensor capacitivo para simulación de agarre
- Gráfica multi-canal en tiempo real
- Exportación completa a Excel

### 5. Controles
- **▶️ Iniciar/Continuar**: Comienza o reanuda el monitoreo
- **⏸️ Pausar**: Pausa temporalmente el monitoreo
- **⏹️ Detener**: Detiene completamente el monitoreo
- **🗑️ Limpiar**: Limpia la gráfica y datos
- **📊 Exportar Excel**: Guarda los datos en formato Excel

## 🔧 Configuración ESP32

### Para Ángulo Simple:
```
GPIO 32 ← Potenciómetro (señal)
3V3     ← Potenciómetro (+)
GND     ← Potenciómetro (-)
```

### Para Brazo Ángulo:
```
GPIO 32 ← Potenciómetro 1 (Base)
GPIO 33 ← Potenciómetro 2 (Articulación 1)  
GPIO 34 ← Potenciómetro 3 (Articulación 2)
GPIO 25 ← Sensor Capacitivo
3V3     ← Alimentación (+)
GND     ← Tierra (-)
```

## 📁 Archivos del Proyecto
- `SensoraCore.exe` - Aplicación principal
- `README_ejecutable.md` - Este archivo de instrucciones

## 🆘 Solución de Problemas

### La aplicación no inicia
- Verifica que tengas Windows 10/11
- Ejecuta como administrador si es necesario
- Verifica que no esté bloqueada por antivirus

### No se conecta al ESP32
- Verifica que el ESP32 esté encendido
- Confirma que estén en la misma red WiFi
- Verifica la IP del ESP32 (puedes usar el monitor serie)
- Asegúrate que el puerto 8080 no esté bloqueado

### Datos erróneos
- Verifica las conexiones de los sensores
- Confirma que los potenciómetros estén conectados correctamente
- Revisa la configuración en el código del ESP32

## 📞 Soporte
Para soporte técnico o reportar problemas, contacta al desarrollador del proyecto SensoraCore.

---
**SensoraCore Alpha 0.1** - Sistema de Monitoreo de Sensores ESP32 (Versión Preliminar)
