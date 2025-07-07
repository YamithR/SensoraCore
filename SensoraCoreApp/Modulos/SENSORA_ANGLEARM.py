from IMPORTACIONES import *  # Importar todo lo necesario desde el módulo de importaciones
#| Despcripción del software: |
"""
El software SENSORA_ANGLEARM es un módulo que forma parte del ecosistema SensoraCore, diseñado para la monitorización de tres sensores angulares mediante tres potenciómetros conectados al ESP32 DevKit V1 de manera simultanea. A través de esta plataforma, el ESP32 ejecuta firmware en MicroPython que lee valores analógicos del potenciómetro conectado a un pin GPIO y los transmite mediante socket TCP a través de WiFi. La interacción con el sistema se realiza mediante una aplicación de escritorio desarrollada en Python con PySide6 que actúa como cliente TCP para recibir y procesar los datos.
"""
# MÉTODO: INTERFAZ DEL SENSOR DE ÁNGULO SIMPLE
def brazoAngulo_UI(self):
    """
    Crea y muestra la interfaz para el brazo robótico con múltiples sensores
    
    Propósito: Interfaz completa para monitorear brazo con 3 potenciómetros + sensor capacitivo
    Funcionalidad: Diagrama de conexiones, controles de monitoreo, visualización multi-canal
    Sensores: 3 potenciómetros (GPIO) + sensor capacitivo (GPIO)
    """
    # --- OCULTAL PANTALLA DE BIENBENIDA ---
    self.welcome_widget.setVisible(False)
    # --- CREAR WIDGET PRINCIPAL ---
    sensor_widget = QWidget()
    layout = QVBoxLayout(sensor_widget)
    layout.setSpacing(10)
    sensor_widget.setStyleSheet
    ("""background-color: #e2f4ff;
    border: 2px solid #0056b3;
    border-radius: 12px;""")
    # SECCIÓN: TÍTULO Y DESCRIPCIÓN
    title = QLabel("🦾 Sensor de Brazo Ángulo")
    title.setStyleSheet
    ("""
        font-size: 20px;                    /* Tamaño grande para destacar */
        font-weight: bold;                  /* Negrita para jerarquía visual */
        color: #007bff;                     /* Azul corporativo */
        margin-bottom: 10px;                /* Separación inferior */
    """)
    layout.addWidget(title)                 # Agregar título al layout principal
    # --- DESCRIPCIÓN FUNCIONAL ---
    description = QLabel("Monitorea 3 ángulos simultáneamente usando potenciómetros en GPIO 32, 33, 34 y sensor capacitivo en GPIO 25 del ESP32")
    description.setStyleSheet("""
        font-size: 14px;                    /* Tamaño legible */
        color: #6c757d;                     /* Gris suave */
        margin-bottom: 20px;                /* Separación inferior generosa */
    """)
    description.setWordWrap(True)           # Permitir salto de línea automático
    layout.addWidget(description)           # Agregar descripción al layout
    # SECCIÓN: DIAGRAMA DE CONEXIONES MÚLTIPLES ESP32
    # --- GRUPO DEL DIAGRAMA PARA BRAZO ---
    diagram_group = QGroupBox("🔌 Diagrama de Conexiones ESP32 - Brazo Ángulo")  # Título específico
    diagram_layout = QVBoxLayout(diagram_group)  # Layout vertical para el contenido
    # --- DIAGRAMA ASCII PARA MÚLTIPLES SENSORES ---
    diagram_text = QLabel("""
<pre style="font-family: 'Courier New', monospace; font-size: 12px; line-height: 1.4; color: #495057;">
┌─────────────────────────────────┐
│  ESP32 DevKit V1                │
│                                 │
│  3V3  ○ ←── Potenciómetros (+)  │
│  GND  ○ ←── Potenciómetros (-)  │
│  D32  ○ ←── Potenciómetro 1 (S) │
│  D33  ○ ←── Potenciómetro 2 (S) │
│  D34  ○ ←── Potenciómetro 3 (S) │
│  D25  ○ ←── Sensor Capacitivo   │
│                                 │
│  LED integrado: GPIO 2          │
└─────────────────────────────────┘

<b>3 Potenciómetros 10kΩ:</b>
• Pin (+): Alimentación 3.3V (todos)
• Pin (S): Señales analógicas:
• Pin (-): Tierra (GND) (todos)
- Potenciómetro 1 → GPIO 32 (Base)
- Potenciómetro 2 → GPIO 33 (Articulación 1)  
- Potenciómetro 3 → GPIO 34 (Articulación 2)

<b>Sensor Capacitivo:</b>
• Señal digital → GPIO 25 (con pull-up interno)
</pre>
    """)
    diagram_text.setWordWrap(True)          # Permitir ajuste de texto
    diagram_text.setStyleSheet("""
        background-color: #f8f9fa;          /* Fondo gris muy claro para diagrama */
        border: 2px solid #dee2e6;          /* Borde gris para definir área */
        border-radius: 6px;                 /* Esquinas redondeadas */
        padding: 15px;                      /* Espacio interno generoso */
        margin: 5px;                        /* Margen exterior pequeño */
    """)
    diagram_layout.addWidget(diagram_text)  # Agregar diagrama al grupo
    # --- NOTA ESPECÍFICA PARA BRAZO ROBÓTICO ---
    note_label = QLabel("💡 <b>Nota:</b> Este sensor simula un brazo robótico con 3 articulaciones. El sensor capacitivo simula el agarre.")
    note_label.setStyleSheet("""
        font-size: 13px;                    /* Tamaño menor para nota */
        color: #856404;                     /* Color ámbar oscuro */
        background-color: #fff3cd;          /* Fondo ámbar claro (alerta) */
        border: 1px solid #ffeaa7;          /* Borde ámbar */
        border-radius: 4px;                 /* Esquinas redondeadas */
        padding: 8px;                       /* Espacio interno */
        margin-top: 5px;                    /* Separación superior */
    """)
    note_label.setWordWrap(True)            # Permitir ajuste de línea
    diagram_layout.addWidget(note_label)    # Agregar nota al grupo
    
    layout.addWidget(diagram_group)         # Agregar grupo completo al layout principal
    # SECCIÓN: CONTROLES DE MONITOREO MÚLTIPLE
    # --- GRUPO DE CONTROLES ---
    controls_group = QGroupBox("Controles")  # Caja agrupada para controles
    controls_layout = QVBoxLayout(controls_group)  # Layout vertical para controles
    # SUB-SECCIÓN: ESTADO DE MÚLTIPLES POTENCIÓMETROS
    # Muestra el estado de los 3 potenciómetros del brazo robótico en tiempo real
    self.brazo_labels = {}                  # Diccionario para almacenar referencias a etiquetas
    for i in range(1, 4):                   # Crear etiquetas para potenciómetros 1, 2 y 3
        label = QLabel(f"Potenciómetro {i}: Lectura: -- | Ángulo: --°")  # Texto inicial
        # --- ESTILO PARA ETIQUETAS DE ESTADO DE POTENCIÓMETROS ---
        label.setStyleSheet("""
            font-size: 14px;                /* Tamaño de fuente legible */
            font-weight: bold;              /* Texto en negrita para destacar */
            color: #495057;                 /* Color gris oscuro para el texto */
            padding: 8px;                   /* Espaciado interno de 8px */
            background-color: #f8f9fa;      /* Fondo gris muy claro */
            border-radius: 6px;             /* Esquinas redondeadas de 6px */
            border: 2px solid #dee2e6;      /* Borde gris claro de 2px */
            margin: 2px;                    /* Margen externo pequeño */            """)
        self.brazo_labels[f'pot{i}'] = label
        controls_layout.addWidget(label)    # Agregar etiqueta al layout de controles
    # SUB-SECCIÓN: ESTADO DEL SENSOR CAPACITIVO
    # Muestra el estado digital (True/False) del sensor capacitivo del brazo
    self.capacitive_label = QLabel("Sensor Capacitivo: --")  # Etiqueta para sensor capacitivo
    # --- ESTILO PARA ETIQUETA DE SENSOR CAPACITIVO ---
    self.capacitive_label.setStyleSheet("""
        font-size: 14px;                    /* Tamaño consistente con otros sensores */
        font-weight: bold;                  /* Texto en negrita */
        color: #495057;                     /* Color gris oscuro */
        padding: 8px;                       /* Espaciado interno */
        background-color: #f8f9fa;          /* Fondo gris claro igual que potenciómetros */
        border-radius: 6px;                 /* Esquinas redondeadas */
        border: 2px solid #dee2e6;          /* Borde gris claro */
        margin: 2px;                        /* Margen pequeño */
    """)
    controls_layout.addWidget(self.capacitive_label)
    # ==================== BOTONES DE CONTROL PARA BRAZO ROBÓTICO ====================
    buttons_layout = QHBoxLayout()
    # BOTÓN INICIAR MONITOREO - Verde para acción positiva
    self.brazo_start_btn = QPushButton("▶️ Iniciar Monitoreo")
    self.brazo_start_btn.clicked.connect(self.toggle_angleArm_monitoring)
    self.brazo_start_btn.setStyleSheet("QPushButton { background-color: #28a745; border-color: #28a745; }")
    buttons_layout.addWidget(self.brazo_start_btn)
    controls_layout.addLayout(buttons_layout)
    # ==================== BOTONES DE ACCIONES SECUNDARIAS ==================== 
    actions_layout = QHBoxLayout()
    # BOTÓN LIMPIAR GRÁFICA - Para borrar datos del brazo robótico
    self.brazo_clear_btn = QPushButton("🗑️ Limpiar Gráfica")
    self.brazo_clear_btn.clicked.connect(self.clear_graph_angleArm)
    actions_layout.addWidget(self.brazo_clear_btn)
    # BOTÓN EXPORTAR - Para guardar datos en Excel (3 potenciómetros + capacitivo)
    self.brazo_export_btn = QPushButton("📊 Exportar Excel")
    self.brazo_export_btn.clicked.connect(self.export_brazo_to_excel)
    self.brazo_export_btn.setEnabled(False)  # Se habilita solo cuando hay datos
    actions_layout.addWidget(self.brazo_export_btn)
    controls_layout.addLayout(actions_layout)
    layout.addWidget(controls_group)
    # Gráfica mejorada para múltiples canales
    graph_group = QGroupBox("Gráfica en Tiempo Real - Múltiples Ángulos")
    graph_layout = QVBoxLayout(graph_group)
    # Configurar matplotlib con colores mejorados para múltiples líneas
    self.brazo_figure = Figure(figsize=(10, 6), dpi=100, facecolor='white')
    self.brazo_canvas = FigureCanvasQTAgg(self.brazo_figure)
    self.brazo_ax = self.brazo_figure.add_subplot(111)
    # Mejorar colores y estilo del gráfico
    self.brazo_ax.set_facecolor('#f8f9fa')
    self.brazo_ax.grid(True, linestyle='--', alpha=0.7, color='#dee2e6')
    self.brazo_ax.set_xlabel('Muestras', fontsize=12, fontweight='bold', color='#495057')
    self.brazo_ax.set_ylabel('Ángulo (°)', fontsize=12, fontweight='bold', color='#495057')
    self.brazo_ax.set_title('Monitoreo de Brazo Robótico - 3 Ángulos', fontsize=14, fontweight='bold', color='#007bff')
    # Líneas de datos con diferentes colores para cada potenciómetro
    colors = ["#cce744", "#00dafb", "#f500cc"]  # Azul, Verde, Rojo
    labels = ['Base (Pot 1)', 'Articulación 1 (Pot 2)', 'Articulación 2 (Pot 3)']
    self.brazo_lines = []
    for i, (color, label) in enumerate(zip(colors, labels)):
        line, = self.brazo_ax.plot([], [], 'o-', linewidth=3, markersize=4,
                                    color=color, label=label,
                                    markerfacecolor=color, 
                                    markeredgecolor='white', markeredgewidth=1)
        self.brazo_lines.append(line)
    # Agregar leyenda
    self.brazo_ax.legend(loc='upper right', fontsize=10)
        # Configurar límites iniciales
    self.brazo_ax.set_xlim(0, 100)
    self.brazo_ax.set_ylim(-135, 135)  # Rango de -135° a +135°
    # Mejorar el layout del gráfico
    self.brazo_figure.tight_layout(pad=2.0)
    # Inicializar el canvas con un dibujo inicial
    self.brazo_canvas.draw()
    graph_layout.addWidget(self.brazo_canvas)
    layout.addWidget(graph_group)
    # Inicializar listas de datos para los 3 potenciómetros
    self.brazo_angulos = [[], [], []]  # Listas para cada potenciómetro
    self.brazo_lecturas = [[], [], []]
    self.brazo_capacitive_states = []
    self.brazo_max_points = 100
    self.monietoreando_AngleArm = False
        # Mostrar en el panel derecho
    self.sensor_details.setWidget(sensor_widget)
    self.sensor_details.setVisible(True)    
# DIÁLOGO DE CALIBRACIÓN POR REGRESIÓN LINEAL PARA BRAZO DE ÁNGULOS
class CalibrationDialog(QDialog):
    """
    Diálogo para calibración por regresión lineal de sensores
    
    Propósito: Interfaz gráfica para calibrar sensores analógicos
    Funcionalidad: 
        - Agregar puntos de calibración manualmente
        - Visualizar datos y regresión en tiempo real
        - Realizar calibración automática
        - Guardar/cargar calibraciones
        - Mostrar estadísticas de calibración
    """
    def __init__(self, sensor_name="Sensor", calibration_instance=None, parent=None):
        """
        Inicializar diálogo de calibración
        
        Args:
            sensor_name: Nombre del sensor para personalizar la interfaz
            calibration_instance: Instancia de TripleAngleArmLinearCalibration existente
            parent: Ventana padre
        """
        super().__init__(parent)
        self.sensor_name = sensor_name
        self.calibration = calibration_instance if calibration_instance else AngleArm_X3_LinearCalibration()
        self.setup_ui()
        self.update_plot()
    def setup_ui(self):
        """Configurar la interfaz de usuario del diálogo de calibració"""
        # Crear layout principal
        pass
    def add_calibration_point(self):
        """Añade un punto de calibración y actualiza la interfaz"""
        # Implementar lógica para agregar punto de calibración
        pass
    def remove_point(self, row):
        """Elimina un punto de calibración específico"""
        # Implementar lógica para eliminar punto de calibración
        pass
    def update_table(self):
        """Actualiza la tabla completa con los datos actuales"""
        # Implementar lógica para actualizar la tabla de puntos de calibración
        pass
    def perform_calibration(self):
        """Realiza la calibración y actualiza la interfaz"""
        # Implementar lógica para realizar calibración automática
        pass
    def clear_data(self):
        """Limpia todos los datos y resetea la interfaz"""
        # Implementar lógica para limpiar datos de calibración
        pass
    def update_plot(self):
        """Actualiza el gráfico de calibración en tiempo real"""
        # Implementar lógica para actualizar el gráfico con los datos actuales
        pass
    def save_calibration(self, filepath: str) -> bool:
        """
        Guarda la calibración actual en archivo
        
        Args:
            filepath: Ruta donde guardar el archivo
            
        Returns:
            bool: True si se guardó exitosamente
        """
        # Implementar lógica para guardar calibración en archivo
        pass
    def load_calibration(self):
        """Carga una calibración desde archivo"""
        # Implementar lógica para cargar calibración desde archivo
        pass
    def accept(self):
        """Acepta el diálogo y emite la señal de calibración actualizada"""
        # Emitir señal con la calibración actual
        self.calibration_updated.emit(self.calibration)
        super().accept()
        pass
    def set_calibration(self, calibration):
        """Establece una calibración existente en el diálogo"""
        self.calibration = calibration
        self.update_table()
        if calibration.is_calibrated:
            self.info_label.setText(f"Ecuación: {calibration.get_calibration_equation()}")
            self.info_label.setStyleSheet("padding: 5px; background-color: #c8e6c9; border-radius: 3px; color: #2e7d32;")
        self.update_plot()
        pass
# CLASE: HILO PARA SENSOR DE BRAZO DE ÁNGULOS
class BrazoAnguloThread(QThread):
    """
    Hilo para monitorear el sensor de brazo de ángulos
    Propósito: Leer datos del sensor y emitirlos a la interfaz
    Funcionalidad: 
        - Leer valores analógicos del potenciómetro
        - Emitir valores leídos a la interfaz gráfica
        - Manejar reconexiones automáticas
    """
    data_received = Signal(int, int, int, int, int, int, bool) # Lecturas y angulos de los 3 potenciómetros y estado del sensor capacitivo
    def __init__(self, esp32_ip, port=8080):
        """
        Constructor del hilo para sensor de ángulo simple
        Parámetros:
        - esp32_ip: Dirección IP del ESP32 (ej: "192.168.1.100")
        - port: Puerto de comunicación TCP (por defecto 8080)
        """
        super().__init__()
        self.esp32_ip = esp32_ip                 # Guardar IP del ESP32 para conectar
        self.port = port                         # Guardar puerto de comunicación
        self.running = False                     # Flag para controlar el bucle principal
        self.sock = None                         # Variable para el socket de conexión
    def run(self):
        """
        Método principal - maneja comunicación con brazo multi-sensor
        Formato esperado: "POT1:val,ANG1:ang,POT2:val,ANG2:ang,POT3:val,ANG3:ang,SENSOR:state"
        """
        self.running = True                      # Activar bandera de ejecución
        try:
            # --- ESTABLECER CONEXIÓN ---
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Socket TCP
            self.sock.settimeout(3)              # 3 segundos para conectar
            self.sock.connect((self.esp32_ip, self.port))  # Conectar al ESP32
            
            # --- ACTIVAR MODO BRAZO ---
            self.sock.sendall(b'MODO:BRAZO_ANGULO')  # Comando para modo brazo multi-sensor
            self.sock.settimeout(1)              # 1 segundo para datos
            
            # --- BUCLE DE RECEPCIÓN DE DATOS ---
            while self.running:
                try:
                    # Recibir hasta 128 bytes (más datos que sensor simple)
                    data = self.sock.recv(128)
                    if not data:                 # Conexión cerrada
                        break
                    
                    # --- PROCESAR MENSAJE COMPLETO ---
                    msg = data.decode(errors='ignore').strip()  # Bytes a string
                    for line in msg.split('\n'):               # Cada línea por separado
                        if line.startswith('POT1:'):            # Identificar datos del brazo
                            try:
                                # --- PARSEAR DATOS COMPLEJOS ---
                                # Formato: POT1:val,ANG1:ang,POT2:val,ANG2:ang,POT3:val,ANG3:ang,SENSOR:state
                                parts = line.split(',')         # Separar por comas
                                
                                # Extraer valores de cada potenciómetro y ángulo
                                lectura1 = int(parts[0].split(':')[1])  # Lectura ADC potenciómetro 1
                                angulo1 = int(parts[1].split(':')[1])   # Ángulo calculado 1
                                lectura2 = int(parts[2].split(':')[1])  # Lectura ADC potenciómetro 2
                                angulo2 = int(parts[3].split(':')[1])   # Ángulo calculado 2
                                lectura3 = int(parts[4].split(':')[1])  # Lectura ADC potenciómetro 3
                                angulo3 = int(parts[5].split(':')[1])   # Ángulo calculado 3
                                
                                # Estado del sensor capacitivo (True/False)
                                sensor_estado = parts[6].split(':')[1] == 'True'
                                
                                # --- EMITIR TODOS LOS DATOS ---
                                self.data_received.emit(lectura1, angulo1, lectura2, angulo2, 
                                                      lectura3, angulo3, sensor_estado)
                            except:
                                pass                             # Ignorar errores de formato
                                
                except socket.timeout:                          # Timeout en recepción
                    continue                                    # Continuar esperando
                    
        except Exception as e:                                  # Error de conexión
            pass                                                # Ignorar y terminar
            
        finally:
            # --- LIMPIEZA DE RECURSOS ---
            if self.sock:
                try:
                    self.sock.sendall(b'STOP')                 # Detener modo brazo
                except:
                    pass
                self.sock.close()                              # Cerrar socket
    
    def stop(self):
        """Detener hilo del brazo de forma segura"""
        self.running = False                                   # Desactivar bucle
        self.wait()                                           # Esperar finalización
# MÓDULO DE CALIBRACIÓN POR REGRESIÓN LINEAL PARA ÁNGULO SIMPLE
class AngleArm_X3_LinearCalibration:
    """
    Clase para calibración por regresión lineal de brazo de ángulos con tres sensores.
    Propósito: Calibrar tres sensores angulares conectados al brazo robótico de forma simultánea.
    """
    def __init__(self):
        """Inicializar sistema de calibración vacío para tres sensores."""
        self.models = [LinearRegression(), LinearRegression(), LinearRegression()]  # Un modelo por sensor
        self.is_calibrated = [False, False, False]  # Un flag por sensor
        self.calibration_data = {
            "raw_values": [[], [], []],         # Lista de valores crudos para cada sensor
            "reference_values": [[], [], []]    # Lista de valores de referencia para cada sensor
        }
        # Parámetros de la ecuación y = mx + b para cada sensor
        self.slopes = [None, None, None]        # Pendiente (m) para cada sensor
        self.intercepts = [None, None, None]    # Intercepto (b) para cada sensor
        self.r_squared = [None, None, None]     # R^2 para cada sensor
    def add_calibration_point(self, sensor_idx, raw_value, reference_value):
        """Agrega un punto de calibración para el sensor indicado (0, 1 o 2)."""
        self.calibration_data["raw_values"][sensor_idx].append(raw_value)
        self.calibration_data["reference_values"][sensor_idx].append(reference_value)
        self.is_calibrated[sensor_idx] = False
    def clear_calibration_data(self):
        """Limpia todos los datos de calibración."""
        self.calibration_data = {
            "raw_values": [[], [], []],
            "reference_values": [[], [], []]
        }
        self.is_calibrated = [False, False, False]
        self.slopes = [None, None, None]
        self.intercepts = [None, None, None]
        self.r_squared = [None, None, None]
    def perform_calibrate(self) -> bool:
        """
        Realiza la calibración por regresión lineal para los tres sensores.
        
        Returns:
            bool: True si la calibración fue exitosa, False si no hay suficientes datos.
        """
        for i in range(3):
            if len(self.calibration_data["raw_values"][i]) < 2:
                return False
    def calibrate_value(self, sensor_idx, raw_value: float) -> Optional[float]:
        """
        Calibra un valor crudo usando el modelo del sensor indicado.
        
        Args:
            sensor_idx: Índice del sensor (0, 1 o 2)
            raw_value: Valor crudo a calibrar
        """
    def get_calibration_equation(self, sensor_idx: int) -> str:
        """
        Obtiene la ecuación de calibración para el sensor indicado.
        
        Args:
            sensor_idx: Índice del sensor (0, 1 o 2)
        
        Returns:
            str: Ecuación en formato "y = mx + b"
        """
        if not self.is_calibrated[sensor_idx]:
            return "Sensor no calibrado"
        m = self.slopes[sensor_idx]
        b = self.intercepts[sensor_idx]
        return f"y = {m:.4f}x + {b:.4f}"
    def save_calibration(self, filepath: str) -> bool:
        """
        Guarda la calibración actual en un archivo JSON.
        
        Args:
            filepath: Ruta donde guardar el archivo
            
        Returns:
            bool: True si se guardó exitosamente
        """
    def load_calibration(self, filepath: str) -> bool:
        """
        Carga una calibración desde un archivo JSON.
        
        Args:
            filepath: Ruta del archivo a cargar
            
        Returns:
            bool: True si se cargó exitosamente
        """
    def get_calibration_stats(self) -> str:
        """
        Retorna estadísticas de la calibración actual
        
        Returns:
            dict: Diccionario con estadísticas de calibración
        """
#| SECCIÓN: FUNCIONES DE MONITOREO - SENSOR DE BRAZO DE ANGULOS  |
class BrazoAnguloMonitor():
    """
    Clase para monitorear el sensor de brazo de ángulos.
    
    Propósito: Leer datos del sensor y emitirlos a la interfaz.
    Funcionalidad: 
        - Leer valores analógicos del potenciómetro
        - Emitir valores leídos a la interfaz gráfica
        - Manejar reconexiones automáticas
    """
    def __init__(self):
        """        Inicializa el monitor de sensor de ángulo simple
        Propósito: Configurar variables y objetos necesarios para monitoreo
        Lógica: Prepara sistema de calibración y variables para almacenar datos
        """
        # SISTEMA DE CALIBRACIÓN
        # --- Instancia de calibración para sensor de brazo de ángulos ---
        self.pot1_calibration = AngleArm_X3_LinearCalibration()
        self.pot2_calibration = AngleArm_X3_LinearCalibration()
        self.pot3_calibration = AngleArm_X3_LinearCalibration()
        # --- Variables para almacenar datos de los sensores ---
        self.angleArm_angulos = [[], [], []]  # Lista de listas para 3 potenciómetros
        self.angleArm_lecturas = [[], [], []]  # Lecturas ADC de los 3 potenciómetros
        self.angleArm_capStates = []   # Estados del sensor capacitivo
        self.max_points = 100      # Número máximo de puntos a almacenar
        # SISTEMA DE ACTUALIZACIONES
        self.thread_AngleArm = None             # Hilo para monitorear el sensor de brazo de ángulos
        self.monietoreando_AngleArm = False     # Indica si se está monitoreando el sensor
        self.pending_updates = False            # Indica si hay actualizaciones pendientes
        self.pending_AngleArm_data =None        # Datos pendientes de actualización
        # -- Configuracion de timer --
        self.timer = QTimer()                   # Timer para actualizaciones periódicas de gráfica
        self.timer.timeout.connect(self.on_timer_update_graph)
        self.timer.setInterval(100)
    # MÉTODO: ALTERNAR MONITOREO DEL SENSOR DE BRAZO DE ÁNGULOS
    def toggle_angleArm_monitoring(self):
        """
        Alterna entre iniciar y detener el monitoreo del sensor de ángulo simple
        
        Propósito: Función de conveniencia para un solo botón de control
        Lógica: Verifica estado actual y ejecuta acción opuesta
        UI: Permite usar un solo botón para iniciar/pausar monitoreo
        Estado: Basado en flag self.monietoreando_AngleArm
        """
        if not self.monietoreando_AngleArm:     # Si no se está monitoreando
            self.start_angleArm_monitoring()    # Iniciar monitoreo del sensor de brazo de ángulos
        else:                                   # Si ya se está monitoreando
            self.stop_angleArm_monitoring()     # Detener monitoreo del sensor de brazo de ángulos
    # MÉTODO: INICIAR MONITOREO DEL SENSOR DE BRAZO DE ÁNGULOS
    def start_angleArm_monitoring(self):
        """
        Inicia el monitoreo en tiempo real del brazo robótico con múltiples sensores
        
        Propósito: Comenzar adquisición simultánea de 3 potenciómetros + sensor capacitivo
        Thread: Crea BrazoAnguloThread para comunicación compleja con ESP32
        Datos: Recibe 3 lecturas ADC + estado capacitivo en un solo paquete
        Protocolo: "BRAZO_ANGULO" - comando especializado para múltiples sensores
        UI: Actualiza botones y habilita exportación
        Gráfica: Inicia visualización de 3 líneas simultáneamente
        """
        
        # --- VERIFICAR CONEXIÓN REQUERIDA ---
        if not self.is_connected:                # Verificar conexión TCP activa
            QMessageBox.warning(self, "Sin conexión", "Debes conectar al ESP32 primero")
            return                               # Salir si no hay conexión
        
        try:
            # --- CREAR Y CONFIGURAR THREAD MULTI-SENSOR ---
            self.thread_AngleArm = BrazoAnguloThread(self.esp_client.esp32_ip)  # Thread especializado
            self.thread_AngleArm.data_received.connect(self.update_angleArm_data)  # Conectar señal compleja
            
            # --- INICIAR MONITOREO ---
            self.thread_AngleArm.start()            # Iniciar thread de comunicación
            self.monietoreando_AngleArm = True      # Marcar estado como monitoreando brazo            
              # --- ACTUALIZAR INTERFAZ DE CONTROL ---
            self.brazo_start_btn.setText("⏸️ Pausar")  # Cambiar botón a pausar
            self.brazo_start_btn.setStyleSheet("QPushButton { background-color: #ffc107; border-color: #ffc107; }")  # Amarillo pausa
            self.brazo_export_btn.setEnabled(True)  # Habilitar exportación multi-datos
              # --- INICIAR ACTUALIZACIÓN GRÁFICA MULTI-LÍNEA ---
            self.timer.start()  # Iniciar timer para actualizaciones periódicas
            
        except Exception as e:
            # --- MANEJAR ERRORES DE INICIALIZACIÓN MULTI-SENSOR ---
            QMessageBox.critical(self, "Error", f"Error al iniciar monitoreo: {str(e)}")
    # MÉTODO: DETENER MONITOREO DEL SENSOR DE BRAZO DE ÁNGULOS
    def stop_angleArm_monitoring(self):
        """
        Detiene el monitoreo del brazo robótico multi-sensor y limpia recursos
        
        Propósito: Parar adquisición de múltiples sensores y liberar thread
        Thread: Detiene BrazoAnguloThread de forma segura
        UI: Restaura botones a estado inicial
        Recursos: Limpia objetos para evitar memory leaks
        """
        
        # --- DETENER THREAD MULTI-SENSOR ---
        if self.thread_AngleArm and self.thread_AngleArm.isRunning():  # Si existe y está corriendo
            self.thread_AngleArm.stop()             # Detener thread de forma segura
            self.thread_AngleArm = None             # Limpiar referencia
          # --- ACTUALIZAR ESTADO Y TIMERS ---
        self.monietoreando_AngleArm = False         # Marcar como no monitoreando brazo
        self.timer.stop()                     # Detener timer de actualización gráfica
          # --- RESTAURAR INTERFAZ DE CONTROL ---
        self.brazo_start_btn.setText("▶️ Iniciar Monitoreo")  # Restaurar texto inicial
        self.brazo_start_btn.setStyleSheet("QPushButton { background-color: #28a745; border-color: #28a745; }")  # Verde inicial
    # MÉTODO: ACTUALIZAR DATOS DE LOS SENSORES DE BRAZO DE ÁNGULOS
    def update_angleArm_data(self, pot1_ADC, pot1_angulo, pot2_ADC, pot2_angulo, pot3_ADC, pot3_angulo, sensor_estado):
        """
        Actualiza los datos de los sensores de brazo de ángulos
        
        Propósito: Almacenar las lecturas actuales de los sensores
        Lógica: Añade nuevos valores a las listas y mantiene el tamaño máximo
        UI: Actualiza visualización en tiempo real
        Estado: No cambia flags, solo actualiza datos
        """
        # --- ALMACENAR DATOS EN HISTORIAL ---
        self.brazo_lecturas[0].append(pot1_ADC)
        self.brazo_lecturas[1].append(pot2_ADC)
        self.brazo_lecturas[2].append(pot3_ADC)
        
        self.brazo_angulos[0].append(pot1_angulo)
        self.brazo_angulos[1].append(pot2_angulo)
        self.brazo_angulos[2].append(pot3_angulo)
        
        self.brazo_capacitive_states.append(sensor_estado)
        
        # --- MANTENER TAMAÑO MÁXIMO DE DATOS ---
        for i in range(3):
            if len(self.brazo_lecturas[i]) > self.brazo_max_points:
                self.brazo_lecturas[i].pop(0)
                self.brazo_angulos[i].pop(0)
        
        if len(self.brazo_capacitive_states) > self.brazo_max_points:
            self.brazo_capacitive_states.pop(0)
        
        # --- ACTUALIZAR ETIQUETAS DE ESTADO ---
        self.brazo_labels['pot1'].setText(f"Potenciómetro 1: Lectura: {pot1_ADC} | Ángulo: {pot1_angulo}°")
        self.brazo_labels['pot2'].setText(f"Potenciómetro 2: Lectura: {pot2_ADC} | Ángulo: {pot2_angulo}°")
        self.brazo_labels['pot3'].setText(f"Potenciómetro 3: Lectura: {pot3_ADC} | Ángulo: {pot3_angulo}°")
        
        sensor_text = "Activo" if sensor_estado else "Inactivo"
        self.capacitive_label.setText(f"Sensor Capacitivo: {sensor_text}")
        
        # --- ACTUALIZAR GRÁFICA ---
        self.update_brazo_graph()
        
        # --- HABILITAR EXPORTACIÓN SI HAY DATOS ---
        if len(self.brazo_lecturas[0]) > 0:
            self.brazo_export_btn.setEnabled(True)
    # MÉTODO: ABRIR DIALOGO DE CALIBRACIÓN
    def open_calibration_dialog(self):
        """
        Abre el diálogo de calibración para los sensores de brazo de ángulos
        
        Propósito: Permitir al usuario calibrar los sensores mediante regresión lineal
        Lógica: Crea instancia del diálogo y lo muestra
        UI: Permite agregar puntos de calibración y ver resultados en tiempo real
        Estado: No cambia flags, solo abre diálogo
        """
    # MÉTODO: ACTUALIZAR ESTADO DE CALIBRACIÓN EN LA INTERFAZ
    def update_calibration_status(self):
        """
        Actualiza el estado de calibración en la interfaz gráfica
        
        Propósito: Reflejar si los sensores están calibrados o no
        Lógica: Verifica el estado de calibración y actualiza etiquetas
        UI: Muestra mensaje de éxito o error según corresponda
        Estado: No cambia flags, solo actualiza visualización
        """
        # Implementar lógica para actualizar estado de calibración en la UI
        pass
    # MÉTODO: LIMPIAR GRÁFICA DEL SENSOR DE ÁNGULO
    def clear_graph_angleArm(self):
        """
        Limpia la gráfica del sensor de brazo de ángulos
        
        Propósito: Reiniciar la visualización de datos
        Lógica: Elimina todos los puntos y reinicia el gráfico
        UI: Permite empezar de nuevo con una gráfica limpia
        Estado: No cambia flags, solo limpia visualización
        """
        # --- LIMPIAR DATOS ALMACENADOS ---
        self.brazo_angulos = [[], [], []]       # Limpiar ángulos de los 3 potenciómetros
        self.brazo_lecturas = [[], [], []]      # Limpiar lecturas ADC
        self.brazo_capacitive_states = []       # Limpiar estados del sensor capacitivo
        
        # --- RESETEAR GRÁFICA ---
        if hasattr(self, 'brazo_lines') and len(self.brazo_lines) == 3:
            for line in self.brazo_lines:
                line.set_data([], [])           # Limpiar datos de cada línea
            self.brazo_ax.set_xlim(0, 100)      # Restaurar límites iniciales
            self.brazo_ax.set_ylim(-135, 135)   # Restaurar límites de ángulo
            self.brazo_canvas.draw()            # Redibujar canvas limpio
        
        # --- RESTAURAR ETIQUETAS ---
        for i in range(1, 4):
            self.brazo_labels[f'pot{i}'].setText(f"Potenciómetro {i}: Lectura: -- | Ángulo: --°")
        self.capacitive_label.setText("Sensor Capacitivo: --")
        
        # --- DESHABILITAR EXPORTACIÓN SIN DATOS ---
        self.brazo_export_btn.setEnabled(False)
    def export_brazo_to_excel(self):
        """
        Exporta todos los datos de los sensores de brazo a archivo Excel
        
        Propósito: Permitir análisis posterior y respaldo de datos
        Formato: Archivo .xlsx con múltiples columnas y gráfica integrada
        Datos: Lecturas ADC, ángulos calculados, estados capacitivos, timestamps
        Gráfica: Incluye gráfico de líneas dentro del archivo Excel
        Validación: Verifica que existan datos antes de exportar
        """
        
        # --- VERIFICAR DATOS DISPONIBLES ---
        if not self.brazo_lecturas[0]:  # Si no hay datos que exportar
            QMessageBox.information(self, "Sin datos", "No hay datos para exportar")
            return
        
        try:
            # --- GENERAR NOMBRE DE ARCHIVO ÚNICO ---
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename, _ = QFileDialog.getSaveFileName(
                self, "Guardar datos del brazo",
                f"SensoraCore_BrazoAngulo_{timestamp}.xlsx",
                "Excel files (*.xlsx)"
            )
            
            if filename:
                # --- CREAR WORKBOOK Y WORKSHEET ---
                wb = openpyxl.Workbook()
                ws = wb.active
                ws.title = "Datos Brazo de Ángulos"
                
                # --- CREAR HEADERS DE COLUMNAS ---
                ws['A1'] = "Muestra"
                ws['B1'] = "Pot1_ADC"
                ws['C1'] = "Pot1_Angulo"
                ws['D1'] = "Pot2_ADC"
                ws['E1'] = "Pot2_Angulo"
                ws['F1'] = "Pot3_ADC"
                ws['G1'] = "Pot3_Angulo"
                ws['H1'] = "Sensor_Capacitivo"
                ws['I1'] = "Timestamp"
                
                # --- ESCRIBIR DATOS FILA POR FILA ---
                max_len = len(self.brazo_lecturas[0])
                for i in range(max_len):
                    row = i + 2  # Empezar en fila 2 (después del header)
                    ws[f'A{row}'] = i + 1  # Número de muestra
                    
                    # Datos de los 3 potenciómetros
                    for j in range(3):
                        if i < len(self.brazo_lecturas[j]):
                            ws[f'{chr(66 + j*2)}{row}'] = self.brazo_lecturas[j][i]  # ADC
                            ws[f'{chr(67 + j*2)}{row}'] = self.brazo_angulos[j][i]   # Ángulo
                    
                    # Estado del sensor capacitivo
                    if i < len(self.brazo_capacitive_states):
                        ws[f'H{row}'] = "Activo" if self.brazo_capacitive_states[i] else "Inactivo"
                    
                    # Timestamp
                    ws[f'I{row}'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # --- GUARDAR ARCHIVO ---
                wb.save(filename)
                QMessageBox.information(self, "Éxito", f"Datos exportados exitosamente a:\n{filename}")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al exportar datos: {str(e)}")
    # MÉTODO: ACTUALIZACIÓN DE GRÁFICAS
    def update_graph_display(self):
        """
        Actualiza todas las gráficas de sensores de forma optimizada usando timer
        
        Propósito: Centralizar y optimizar la actualización de múltiples gráficas
        Funcionamiento: Usa flags de datos pendientes para evitar actualizaciones innecesarias
        Optimización: Solo redibuja canvas cuando hay datos nuevos pendientes
        Rendimiento: Evita bloqueos de UI con actualizaciones frecuentes
        Sensores: Ángulo simple, brazo robótico, IR, capacitivo, ultrasónico
        """
        # --- VERIFICAR SI HAY DATOS PENDIENTES ---
        if not self.pending_updates:           # Si no hay actualizaciones pendientes
            return                             # Salir sin procesar nada
        try:
            # ==================== ACTUALIZAR GRÁFICA BRAZO DE ÁNGULOS ====================
            if (self.pending_AngleArm_data is not None and 
                hasattr(self, 'brazo_canvas') and hasattr(self, 'brazo_lines')):
                self.brazo_canvas.draw()       # Redibujar canvas del brazo robótico (3 líneas)
            # --- LIMPIAR FLAGS DE ACTUALIZACIÓN ---
            self.pending_updates = False              # Resetear flag principal de actualizaciones
            self.pending_AngleArm_data = None            # Limpiar datos pendientes de brazo
        except Exception as e:
            pass

    # TIMER DE ACTUALIZACIÓN GRÁFICA
    def on_timer_update_graph(self):
        """
        Método llamado periódicamente por el timer para actualizar la gráfica si hay datos nuevos.
        """
        self.update_graph_display()
        
    def update_brazo_graph(self):
        """
        Actualiza el gráfico de múltiples líneas del brazo robótico
        
        Propósito: Mostrar los 3 ángulos en tiempo real
        Lógica: Actualiza las líneas de datos con los valores actuales
        UI: Redibuja el canvas con los nuevos datos
        """
        if hasattr(self, 'brazo_lines') and len(self.brazo_lines) == 3:
            # Actualizar cada línea con sus respectivos datos
            for i in range(3):
                if self.brazo_angulos[i]:
                    x_data = list(range(len(self.brazo_angulos[i])))
                    y_data = self.brazo_angulos[i]
                    self.brazo_lines[i].set_data(x_data, y_data)
            
            # Ajustar límites del gráfico
            if self.brazo_angulos[0]:  # Si hay datos
                max_points = max(len(self.brazo_angulos[i]) for i in range(3))
                self.brazo_ax.set_xlim(0, max(max_points, 100))
                
                # Obtener rango de todos los valores
                all_values = []
                for i in range(3):
                    all_values.extend(self.brazo_angulos[i])
                
                if all_values:
                    min_val = min(all_values)
                    max_val = max(all_values)
                    margin = (max_val - min_val) * 0.1
                    self.brazo_ax.set_ylim(min_val - margin, max_val + margin)
            
            # Redibujar el canvas
            self.brazo_canvas.draw()
