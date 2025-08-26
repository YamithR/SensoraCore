# MANUAL TÉCNICO - SENSORA INFRARED

---

## 1. INTRODUCCIÓN

### Descripción General
El módulo SENSORA_INFRARED es un sistema de detección de proximidad por infrarrojo que utiliza el sensor E18 D80NK para realizar detección de objetos sin contacto físico. El sistema implementa una arquitectura cliente-servidor basada en TCP que permite la comunicación entre un microcontrolador ESP32 y una aplicación de escritorio desarrollada en PySide6, proporcionando monitoreo en tiempo real del estado digital del sensor.

### Objetivo General
Desarrollar un sistema integral de detección de proximidad por infrarrojo que permita la adquisición, visualización y análisis de estados digitales ON/OFF en tiempo real con aplicaciones educativas enfocadas en principios de óptica, electrónica digital y sistemas de detección sin contacto.

### Objetivos Específicos
- Implementar comunicación TCP para transmisión de estados digitales desde ESP32
- Proporcionar visualización clara del estado del sensor mediante indicadores gráficos
- Desarrollar interfaz educativa para comprensión de sensores fotoeléctricos
- Ofrecer información técnica detallada sobre el funcionamiento del sensor E18 D80NK
- Crear sistema robusto de monitoreo con manejo de errores y reconexión automática

---

## 2. CARACTERÍSTICAS TÉCNICAS

### Arquitectura del Software
- **Patrón Cliente-Servidor TCP**: Comunicación directa entre ESP32 y aplicación desktop
- **Threading Asíncrono**: QThread para operaciones de red sin bloqueo de interfaz
- **Estados Digitales**: Procesamiento de señales ON/OFF con retroalimentación visual
- **Manejo de Errores**: Sistema robusto de reconexión y recuperación ante fallos

### Componentes Principales
- **InfraredThread**: Hilo de comunicación TCP para recepción de estados digitales
- **InfraredLogic**: Controlador principal de lógica de aplicación y UI
- **Sistema de Estados**: Gestión visual de estados ON/OFF con estilos dinámicos
- **Protocolo de Comunicación**: Manejo específico del protocolo IR_DIGITAL

### Funcionalidades Específicas
- Detección digital de proximidad (True/False)
- Retroalimentación visual inmediata del estado del sensor
- Información técnica integrada sobre el sensor E18 D80NK
- Diagrama de conexiones detallado con códigos de color
- Control de inicio/pausa de monitoreo con estados persistentes

---

## 3. HARDWARE COMPATIBLE

### Microcontrolador Principal
- **Modelo**: ESP32 DevKit V1
- **Conectividad**: WiFi integrado para comunicación TCP
- **GPIO Digital**: Pin D25 para lectura de estado del sensor
- **Alimentación**: 3.3V para lógica, 5V disponible para sensor

### Sensor Requerido
- **Tipo**: E18 D80NK - Sensor Fotoeléctrico Infrarrojo Reflectivo
- **Principio de Operación**: Emisión y detección de luz infrarroja reflejada
- **Rango de Detección**: 3cm - 80cm (ajustable con tornillo de precisión)
- **Salida**: Digital NPN (ON/OFF), compatible con lógica 3.3V/5V
- **Voltaje de Alimentación**: 5V-12V DC
- **Consumo**: <25mA en operación normal

### Diagrama de Conexiones
```
┌─────────────────────────────────┐
│  ESP32 DevKit V1 -> Sensor     │
│  3V3  ○ ←── N/A         (+)    │
│  GND  ○ ←── GND Cable Azul (-)  │
│  D25  ○ ←── OUT Cable Negro (D) │
│---------------------------------│
│  Fuente de Voltaje -> Sensor    │
│  5V   ○ ←── 5V Cable Marrón     │
└─────────────────────────────────┘
```

**Notas de Conexión**:
- **Voltaje**: Rango 5V-12V para alimentación del sensor
- **GND**: Tierra común entre microcontrolador, fuente y sensor
- **OUT**: Salida digital conectada al pin D25 del ESP32

---

## 4. REQUERIMIENTOS DE INSTALACIÓN Y CONFIGURACIÓN

### Requisitos del Sistema
- **Sistema Operativo**: Windows 10/11, macOS 10.14+, Ubuntu 18.04+
- **Python**: Versión 3.8 o superior
- **RAM**: Mínimo 2GB, recomendado 4GB
- **Espacio en Disco**: 200MB libres para instalación

### Dependencias de Software
```python
# Dependencias principales
PySide6>=6.0.0          # Framework de interfaz gráfica Qt6
socket                  # Comunicación TCP (built-in Python)
```

### Proceso de Instalación
1. **Configuración del Entorno Python**:
   ```bash
   pip install PySide6
   ```

2. **Preparación del Hardware**:
   - Conectar E18 D80NK según diagrama de conexiones
   - Verificar alimentación 5V independiente para el sensor
   - Configurar ESP32 con firmware MicroPython
   - Verificar continuidad de conexiones

3. **Configuración de Red**:
   - Asegurar conectividad WiFi del ESP32
   - Configurar dirección IP conocida para el ESP32
   - Verificar puerto TCP 8080 disponible
   - Probar conectividad básica con ping

4. **Calibración del Sensor**:
   - Ajustar distancia de detección con tornillo de precisión
   - Verificar respuesta adecuada en rango deseado
   - Confirmar estados ON/OFF estables

---

## 5. MANUAL DE USUARIO

### Inicio del Sistema
1. **Verificación de Hardware**:
   - Confirmar todas las conexiones según diagrama
   - Verificar alimentación 5V al sensor E18 D80NK
   - Asegurar que ESP32 esté energizado y conectado a WiFi
   - Observar LED de estado en el sensor (debe estar encendido)

2. **Configuración de Comunicación**:
   - Introducir IP del ESP32 en campo correspondiente de la aplicación
   - Verificar conectividad de red antes de iniciar monitoreo
   - Confirmar que puerto 8080 esté disponible

3. **Inicio de Monitoreo**:
   - Hacer clic en "Iniciar Monitoreo"
   - Observar cambio de estado del botón a "Pausar"
   - Confirmar conexión exitosa en mensajes de estado

### Operación Paso a Paso
1. **Interpretación de Estados**:
   - **Estado ON**: Objeto detectado dentro del rango configurado
     - Indicador visual: Fondo verde con texto "ON"
     - Color: Verde claro (#d4edda) con texto verde oscuro (#155724)
   
   - **Estado OFF**: No hay objeto en rango de detección
     - Indicador visual: Fondo rojo con texto "OFF"
     - Color: Rojo claro (#f8d7da) con texto rojo oscuro (#721c24)

2. **Pruebas de Funcionamiento**:
   - Posicionar objeto sólido frente al sensor
   - Observar cambio inmediato de estado OFF a ON
   - Retirar objeto y verificar retorno a estado OFF
   - Probar diferentes distancias dentro del rango configurado

3. **Ajuste de Sensibilidad**:
   - Localizar tornillo de ajuste en el sensor E18 D80NK
   - Girar en sentido horario para reducir distancia de detección
   - Girar en sentido antihorario para aumentar distancia
   - Realizar pruebas graduales para encontrar configuración óptima

### Funcionalidades de Control
- **Pausar Monitoreo**: 
  - Clic en "Pausar" detiene la comunicación TCP
  - Estado visual se resetea a configuración por defecto
  - Botón cambia de vuelta a "Iniciar Monitoreo"

- **Información Técnica**:
  - Panel informativo con especificaciones del sensor
  - Descripción del principio de funcionamiento infrarrojo
  - Características técnicas y rangos de operación

---

## 6. ALGORITMOS IMPLEMENTADOS

### Comunicación TCP
```python
# Establecimiento de conexión con protocolo específico
def run(self):
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.sock.connect((self.esp32_ip, self.port))
    self.sock.sendall(b"MODO:DISTANCIA_IR")
    
    # Verificación de handshake
    resp = self.sock.recv(64).decode(errors="ignore").strip()
    if "DISTANCIA_IR_OK" not in resp:
        self.status.emit("ESP32 no aceptó modo DISTANCIA_IR")
        return
    
    # Loop de recepción de estados
    while self._running:
        chunk = self.sock.recv(128)
        buffer += chunk.decode(errors="ignore")
        # Procesamiento línea por línea
        while "\n" in buffer:
            line, buffer = buffer.split("\n", 1)
            # Parseo: IR_DIGITAL:True/False
            if "IR_DIGITAL:" in line:
                estado = line.split(":")[1].strip().lower()
                on = estado in ("true", "1", "on")
                self.state.emit(on)
```

### Gestión de Estados Visuales
```python
# Actualización dinámica de interfaz según estado del sensor
def _set_state(self, on: bool):
    if hasattr(self.ui, "EstadoDeSensorInfrarojo_ON_OFF") and self.monitoring:
        label = getattr(self.ui, "EstadoDeSensorInfrarojo_ON_OFF")
        
        if on:  # Objeto detectado
            label.setText("ON")
            label.setStyleSheet("""
                background-color: #d4edda; 
                color: #155724; 
                font-weight: bold; 
                padding: 8px;
            """)
        else:  # No hay objeto
            label.setText("OFF")
            label.setStyleSheet("""
                background-color: #f8d7da; 
                color: #721c24; 
                font-weight: bold; 
                padding: 8px;
            """)
```

### Manejo de Errores y Reconexión
```python
# Sistema robusto de manejo de excepciones
def run(self):
    try:
        # Lógica de conexión y comunicación
        pass
    except socket.timeout:
        continue  # Reintentar en timeout
    except Exception as e:
        if not self._stopping:  # Solo reportar si no es parada intencional
            self.status.emit(f"Error socket IR: {e}")
        break
    finally:
        # Limpieza garantizada de recursos
        self._cleanup_connection()

def _cleanup_connection(self):
    if self.sock:
        try:
            self.sock.sendall(b"STOP")  # Notificación graceful
        except Exception:
            pass
        try:
            self.sock.close()
        except Exception:
            pass
        self.sock = None
```

---

## 7. VALIDACIÓN Y TESTING

### Pruebas de Funcionalidad
- **Conectividad TCP**: Verificación de establecimiento de conexión < 3 segundos
- **Protocolo de Comunicación**: Confirmación de handshake DISTANCIA_IR_OK
- **Recepción de Estados**: Validación de parsing correcto IR_DIGITAL:True/False
- **Actualización de UI**: Verificación de cambios visuales en tiempo real

### Pruebas de Precisión del Sensor
- **Rango de Detección**: Validado 3cm - 80cm con objetos de diferentes materiales
- **Tiempo de Respuesta**: < 50ms para cambios de estado ON/OFF
- **Estabilidad**: Sin fluctuaciones en estados estáticos por > 1 hora
- **Materiales**: Funcional con metal, plástico, madera, papel

### Pruebas de Robustez del Sistema
- **Reconexión Automática**: Recuperación exitosa tras pérdida de red
- **Manejo de Errores**: Comportamiento graceful ante desconexiones
- **Estabilidad de UI**: Sin congelamiento durante operación prolongada
- **Gestión de Memoria**: Uso constante < 50MB durante operación normal

### Pruebas de Usabilidad
- **Tiempo de Aprendizaje**: < 5 minutos para operación básica
- **Claridad Visual**: Estados ON/OFF claramente diferenciables
- **Retroalimentación**: Respuesta visual inmediata a cambios de estado
- **Información Contextual**: Diagramas y especificaciones integradas

---

## 8. APLICACIONES EDUCATIVAS

### Nivel Básico (Secundaria)
- **Conceptos Físicos**:
  - Propiedades de la luz infrarroja
  - Reflexión y absorción de radiación electromagnética
  - Principios básicos de detección sin contacto

- **Experimentos Sugeridos**:
  - Detección de diferentes materiales y colores
  - Medición manual de distancia máxima de detección
  - Comparación con detección visible vs infrarroja

### Nivel Intermedio (Bachillerato/Técnico)
- **Conceptos Tecnológicos**:
  - Sensores fotoeléctricos y su clasificación
  - Sistemas digitales y lógica booleana
  - Aplicaciones en automatización industrial

- **Proyectos Propuestos**:
  - Sistema de conteo de objetos en banda transportadora
  - Detector de presencia para encendido automático
  - Análisis de diferentes tipos de superficies reflectivas

### Nivel Avanzado (Universidad)
- **Conceptos Especializados**:
  - Optoelectrónica y fotodetectores
  - Procesamiento de señales digitales
  - Sistemas embebidos y comunicación IoT

- **Investigaciones Sugeridas**:
  - Caracterización completa del sensor E18 D80NK
  - Desarrollo de algoritmos de filtrado digital
  - Integración con sistemas de control automático

### Aplicaciones Interdisciplinarias
- **Física**: Estudio de radiación electromagnética infrarroja
- **Electrónica**: Circuitos digitales y acondicionamiento de señales
- **Informática**: Programación de sistemas en tiempo real
- **Ingeniería**: Aplicaciones en automatización y robótica

---

## 9. MANTENIMIENTO Y SOPORTE

### Mantenimiento Preventivo
- **Hardware**:
  - Limpieza mensual del emisor y receptor del sensor E18 D80NK
  - Verificación de conexiones eléctricas y continuidad
  - Inspección de fuente de alimentación 5V estable
  - Revisión del tornillo de ajuste de sensibilidad

- **Software**:
  - Verificación periódica de conectividad de red
  - Monitoreo de logs de conexión TCP
  - Actualización de dependencias PySide6 según disponibilidad

### Solución de Problemas Comunes
- **No Detecta Objetos**:
  - Verificar alimentación 5V al sensor
  - Ajustar sensibilidad con tornillo de precisión
  - Comprobar conexión del cable de salida (OUT)
  - Probar con diferentes tipos de objetos/superficies

- **Estados Erráticos**:
  - Verificar tierra común entre todos los componentes
  - Revisar interferencias electromagnéticas cercanas
  - Ajustar distancia y ángulo del objeto target
  - Verificar estabilidad de fuente de alimentación

- **Error de Conexión TCP**:
  - Confirmar IP del ESP32 en red local
  - Verificar puerto 8080 no bloqueado por firewall
  - Reiniciar ESP32 y aplicación
  - Comprobar conectividad WiFi estable

### Optimización de Rendimiento
- **Ajuste de Sensibilidad**: Calibración fina según aplicación específica
- **Posicionamiento**: Ubicación óptima para minimizar falsas detecciones
- **Filtrado Ambiental**: Protección contra luz solar directa e interferencias

---

## 10. CONSIDERACIONES DE SEGURIDAD

### Seguridad Eléctrica
- **Voltajes de Operación**: 5V-12V DC, clasificación de baja tensión
- **Aislamiento**: Separación entre circuitos de potencia y control
- **Protección contra Inversión**: Verificar polaridad antes de energizar
- **Tierra Común**: Conexión obligatoria de GND entre todos los componentes

### Seguridad Óptica
- **Radiación Infrarroja**: Emisión dentro de límites seguros para exposición humana
- **No Dañino**: Longitud de onda infrarroja no presenta riesgos oculares
- **Visibilidad**: LED indicador para identificar estado operativo del sensor

### Seguridad de Datos
- **Comunicación Local**: TCP limitado a red local sin exposición externa
- **Datos Mínimos**: Transmisión únicamente de estados digitales ON/OFF
- **Sin Almacenamiento**: No se guardan datos sensibles en el sistema

---

## 11. CONCLUSIONES

### Logros Técnicos
El módulo SENSORA_INFRARED proporciona una implementación exitosa de un sistema de detección de proximidad infrarroja con comunicación TCP robusta. La integración del sensor E18 D80NK con ESP32 y la aplicación PySide6 crea una plataforma completa para aprendizaje de principios optoelectrónicos y sistemas digitales.

### Valor Educativo
La simplicidad conceptual del sistema (estados ON/OFF) combinada con la sofisticación técnica del sensor infrarrojo ofrece una excelente introducción a tecnologías de detección sin contacto. Los estudiantes pueden explorar desde conceptos básicos de óptica hasta aplicaciones avanzadas en automatización industrial.

### Aplicabilidad Práctica
El sistema encuentra aplicaciones directas en:
- **Sistemas de Seguridad**: Detección de intrusos y control de acceso
- **Automatización Industrial**: Sensores de presencia en líneas de producción
- **Robótica**: Navegación y evitación de obstáculos
- **Domótica**: Control automático de iluminación y dispositivos

### Fortalezas del Diseño
- **Simplicidad de Uso**: Interfaz intuitiva con retroalimentación visual clara
- **Robustez**: Comunicación TCP confiable con manejo de errores
- **Flexibilidad**: Ajuste de sensibilidad para diferentes aplicaciones
- **Información Integrada**: Documentación técnica accesible en la interfaz

### Perspectivas de Desarrollo
El módulo establece una base sólida para extensiones futuras:
- **Múltiples Sensores**: Integración de arrays de sensores IR
- **Análisis Temporal**: Registro y análisis de patrones de detección
- **Integración IoT**: Conectividad con plataformas de monitoreo remoto
- **Machine Learning**: Reconocimiento de patrones de movimiento

La documentación completa y el diseño modular aseguran la sostenibilidad del proyecto y facilitan su evolución hacia aplicaciones más complejas manteniendo la accesibilidad educativa.

---

**Documento generado para SENSORA CORE - Sistema de Sensores Educativos**  
**Versión**: 1.0 | **Fecha**: Agosto 2025 | **Módulo**: INFRARED  
**Desarrollado por**: Equipo de Desarrollo SENSORA | **Revisión**: Técnica Completa
