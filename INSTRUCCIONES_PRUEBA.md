# Instrucciones para Probar SensoraCore Mejorado

## 🚀 Cómo Probar las Nuevas Características

### 1. Ejecutar la Aplicación
```bash
cd "c:\Users\yamit\Documents\VisualStudioCode\Modulos_Didacticos\SensoraCore\SensoraCoreApp"
python main.py
```

### 2. Lo que Verás al Abrir la Aplicación

#### **Estado Inicial - Sin Conexión**
- 🏠 **Panel izquierdo**: Formulario de conexión con estado "🔴 Desconectado"
- 🔧 **Panel derecho**: Mensaje de bienvenida con icono de herramienta
- ❌ **Lista de sensores**: **OCULTA** (no aparece hasta conectar)

#### **Después de Conectar al ESP32**
- 🟢 **Indicador de estado**: Cambia a "🟢 Conectado"
- ✨ **Lista de sensores**: Aparece con **animación fade-in**
- 📋 **Sensores disponibles**:
  - 🎛️ **Ángulo Simple** (habilitado y seleccionable)
  - 🦾 **Brazo Ángulo** (deshabilitado - "Próximamente")
  - 📏 **Distancia IR** (deshabilitado - "Próximamente")
  - 🔍 **Distancia Capacitivo** (deshabilitado - "Próximamente")
  - 📡 **Distancia Ultrasónico** (deshabilitado - "Próximamente")
  - 💨 **Velocidad Óptica** (deshabilitado - "Próximamente")

#### **Al Seleccionar "Ángulo Simple"**
- 🎛️ **Panel derecho**: Muestra interfaz específica del sensor
- 📊 **Gráfica mejorada**: Fondo claro, líneas azules destacadas
- 🎮 **Controles modernos**:
  - ▶️ **"Iniciar Monitoreo"** (verde)
  - ⏹️ **"Detener"** (rojo, inicialmente deshabilitado)
  - 🗑️ **"Limpiar Gráfica"**
  - 📊 **"Exportar Excel"** (se habilita con datos)

### 3. Características Destacadas a Probar

#### **Conexión Mejorada**
- Prueba ingresar una IP incorrecta → verás el error y estado permanece "🔴 Desconectado"
- Conecta correctamente → botón cambia a "🔄 Reconectar", estado a "🟢 Conectado"

#### **Flujo de Sensores**
- Sin conexión: intentar acceder a sensores muestra advertencia
- Con conexión: sensores aparecen automáticamente con animación suave

#### **Monitoreo Dinámico**
- Inicia monitoreo → botón cambia a "⏸️ Pausar" (amarillo)
- Pausa → botón cambia a "▶️ Continuar" (verde)
- Detener → reinicia todos los controles

#### **Gráfica Profesional**
- Colores optimizados para mejor visibilidad
- Línea azul destacada con marcadores blancos
- Grid sutil que no interfiere con los datos
- Escalado automático inteligente

#### **Exportación Excel**
- Se habilita solo cuando hay datos
- Formato profesional con encabezados azules
- Gráfica integrada y estadísticas completas
- Nombre de archivo automático con timestamp

## 🎯 Puntos Clave de la Experiencia

### ✅ **Antes** vs **🚀 Ahora**

| Característica | Antes | Ahora |
|----------------|-------|-------|
| **Inicio** | Todas las funciones visibles | Solo conexión visible |
| **Conexión** | Botón básico | Indicador visual + animaciones |
| **Sensores** | Lista estática | Lista dinámica post-conexión |
| **Gráfica** | Colores básicos | Colores profesionales optimizados |
| **Controles** | Básicos | Dinámicos con estados visuales |
| **Exportación** | Funcional | Formato profesional completo |

### 🎨 **Elementos Visuales Nuevos**
- **Iconos descriptivos** en toda la interfaz
- **Colores semánticos** (verde=éxito, rojo=error, azul=acción)
- **Animaciones suaves** que mejoran la experiencia
- **Layout responsive** que se adapta al tamaño de ventana
- **Tipografía mejorada** con jerarquía visual clara

---

**¡Disfruta explorando la nueva experiencia SensoraCore!** 🎉
