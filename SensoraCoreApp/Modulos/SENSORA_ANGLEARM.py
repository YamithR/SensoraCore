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
    
    # BOTÓN CALIBRACIÓN - Color azul para función de configuración
    self.brazo_calibrate_btn = QPushButton("⚙️ Calibrar Sensores")
    self.brazo_calibrate_btn.clicked.connect(self.open_calibration_dialog)
    self.brazo_calibrate_btn.setStyleSheet("QPushButton { background-color: #007bff; border-color: #007bff; color: white; padding: 10px; }")
    buttons_layout.addWidget(self.brazo_calibrate_btn)
    
    controls_layout.addLayout(buttons_layout)
    
    # --- ETIQUETA DE CALIBRACIÓN ---
    # Muestra el estado de calibración de los sensores del brazo
    self.brazo_calibration_status_label = QLabel("Calibración: No aplicada")  # Estado inicial
    self.brazo_calibration_status_label.setStyleSheet("""
        font-size: 14px;                    /* Tamaño menor para información secundaria */
        font-weight: bold;                  /* Texto en negrita */
        color: #856404;                     /* Color ámbar para indicar estado */
        padding: 8px;                       /* Espacio interno menor */
        background-color: #fff3cd;          /* Fondo ámbar claro */
        border-radius: 4px;                 /* Esquinas redondeadas menores */
        border: 1px solid #ffeaa7;          /* Borde ámbar */
        margin-top: 5px;                    /* Separación superior */
    """)
    controls_layout.addWidget(self.brazo_calibration_status_label)  # Agregar etiqueta de calibración
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
    
    # --- ACTUALIZAR ESTADO DE CALIBRACIÓN ---
    self.update_calibration_status()         # Mostrar estado actual de calibración    
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
    # Señal para notificar cambios de calibración a la ventana principal
    calibration_updated = Signal(object)
    
    def __init__(self, sensor_name="Sensor", calibration_instance=None, parent=None):
        """
        Inicializar diálogo de calibración
        
        Args:
            sensor_name: Nombre del sensor para personalizar la interfaz
            calibration_instance: Instancia de AngleArm_X3_LinearCalibration existente
            parent: Ventana padre
        """
        super().__init__(parent)
        self.sensor_name = sensor_name
        self.calibration = calibration_instance if calibration_instance else AngleArm_X3_LinearCalibration()
        self.setup_ui()
        self.update_plot()
    
    def setup_ui(self):
        """Configurar la interfaz de usuario del diálogo de calibración"""
        self.setWindowTitle(f"Calibración por Regresión Lineal - {self.sensor_name}")
        self.setFixedSize(1000, 800)  # Tamaño mayor para acomodar 3 sensores
        
        # Layout principal vertical
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        
        # ==================== GRUPO DE ENTRADA DE DATOS ====================
        input_group = QGroupBox("Agregar Punto de Calibración")
        input_group.setFont(QFont("Arial", 10, QFont.Bold))
        input_layout = QGridLayout(input_group)
        
        # Selector de sensor
        input_layout.addWidget(QLabel("Sensor:"), 0, 0)
        self.sensor_combo = QComboBox()
        self.sensor_combo.addItems(["Potenciómetro 1 (Base)", "Potenciómetro 2 (Art. 1)", "Potenciómetro 3 (Art. 2)"])
        input_layout.addWidget(self.sensor_combo, 0, 1)
        
        # Campos de entrada
        input_layout.addWidget(QLabel("Valor Crudo del Sensor:"), 0, 2)
        self.raw_input = QLineEdit()
        self.raw_input.setPlaceholderText("Ej: 512 (lectura ADC)")
        input_layout.addWidget(self.raw_input, 0, 3)
        
        input_layout.addWidget(QLabel("Valor Real (Referencia):"), 0, 4)
        self.ref_input = QLineEdit()
        self.ref_input.setPlaceholderText("Ej: 90.0 (grados reales)")
        input_layout.addWidget(self.ref_input, 0, 5)
        
        # Botón para agregar punto
        self.add_point_btn = QPushButton("➕ Agregar Punto")
        self.add_point_btn.clicked.connect(self.add_calibration_point)
        self.add_point_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        input_layout.addWidget(self.add_point_btn, 0, 6)
        
        layout.addWidget(input_group)
        
        # ==================== TABLA DE PUNTOS DE CALIBRACIÓN ====================
        table_group = QGroupBox("Puntos de Calibración")
        table_group.setFont(QFont("Arial", 10, QFont.Bold))
        table_layout = QVBoxLayout(table_group)
        
        self.points_table = QTableWidget(0, 4)  # 4 columnas: Sensor, Crudo, Referencia, Eliminar
        self.points_table.setHorizontalHeaderLabels(["Sensor", "Valor Crudo", "Valor Referencia", "Acción"])
        
        # Configurar encabezados de tabla
        header = self.points_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.Fixed)
        self.points_table.setColumnWidth(3, 80)
        
        table_layout.addWidget(self.points_table)
        layout.addWidget(table_group)
        
        # ==================== BOTONES DE CONTROL ====================
        buttons_layout = QHBoxLayout()
        
        # Botón calibrar
        self.calibrate_btn = QPushButton("🔧 Realizar Calibración")
        self.calibrate_btn.clicked.connect(self.perform_calibration)
        self.calibrate_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        buttons_layout.addWidget(self.calibrate_btn)
        
        # Botón limpiar
        self.clear_btn = QPushButton("🗑️ Limpiar Datos")
        self.clear_btn.clicked.connect(self.clear_data)
        self.clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF9800;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #F57C00;
            }
        """)
        buttons_layout.addWidget(self.clear_btn)
        
        # Botón guardar
        self.save_btn = QPushButton("💾 Guardar Calibración")
        self.save_btn.clicked.connect(self.save_calibration)
        buttons_layout.addWidget(self.save_btn)
        
        # Botón cargar
        self.load_btn = QPushButton("📂 Cargar Calibración")
        self.load_btn.clicked.connect(self.load_calibration)
        buttons_layout.addWidget(self.load_btn)
        
        layout.addLayout(buttons_layout)
        
        # ==================== INFORMACIÓN DE CALIBRACIÓN ====================
        info_group = QGroupBox("Estado de Calibración")
        info_group.setFont(QFont("Arial", 10, QFont.Bold))
        info_layout = QVBoxLayout(info_group)
        
        self.info_label = QLabel("Ecuación: No calibrado")
        self.info_label.setFont(QFont("Arial", 9))
        self.info_label.setStyleSheet("padding: 5px; background-color: #f0f0f0; border-radius: 3px;")
        info_layout.addWidget(self.info_label)
        
        layout.addWidget(info_group)
        
        # ==================== GRÁFICO ====================
        graph_group = QGroupBox("Visualización de Calibración")
        graph_group.setFont(QFont("Arial", 10, QFont.Bold))
        graph_layout = QVBoxLayout(graph_group)
        
        self.figure = Figure(figsize=(10, 6))
        self.canvas = FigureCanvasQTAgg(self.figure)
        graph_layout.addWidget(self.canvas)
        
        layout.addWidget(graph_group)
        
        # ==================== BOTONES DE DIÁLOGO ====================
        dialog_buttons = QHBoxLayout()
        
        self.apply_btn = QPushButton("✅ Aplicar y Cerrar")
        self.apply_btn.clicked.connect(self.accept)
        self.apply_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 12px 20px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        dialog_buttons.addWidget(self.apply_btn)
        
        self.cancel_btn = QPushButton("❌ Cancelar")
        self.cancel_btn.clicked.connect(self.reject)
        self.cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                padding: 12px 20px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #d32f2f;
            }
        """)
        dialog_buttons.addWidget(self.cancel_btn)
        
        layout.addLayout(dialog_buttons)
        
        # Conectar Enter para agregar puntos
        self.raw_input.returnPressed.connect(self.add_calibration_point)
        self.ref_input.returnPressed.connect(self.add_calibration_point)
    def add_calibration_point(self):
        """Añade un punto de calibración y actualiza la interfaz"""
        try:
            sensor_idx = self.sensor_combo.currentIndex()  # 0, 1, o 2
            raw_val = float(self.raw_input.text())
            ref_val = float(self.ref_input.text())
            
            # Agregar al modelo de calibración
            self.calibration.add_calibration_point(sensor_idx, raw_val, ref_val)
            
            # Actualizar tabla
            row = self.points_table.rowCount()
            self.points_table.insertRow(row)
            self.points_table.setItem(row, 0, QTableWidgetItem(self.sensor_combo.currentText()))
            self.points_table.setItem(row, 1, QTableWidgetItem(f"{raw_val:.2f}"))
            self.points_table.setItem(row, 2, QTableWidgetItem(f"{ref_val:.2f}"))
            
            # Botón eliminar para esta fila
            delete_btn = QPushButton("🗑️")
            delete_btn.clicked.connect(lambda checked, r=row: self.remove_point(r))
            delete_btn.setStyleSheet("QPushButton { background-color: #f44336; color: white; }")
            self.points_table.setCellWidget(row, 3, delete_btn)
            
            # Limpiar campos
            self.raw_input.clear()
            self.ref_input.clear()
            
            # Actualizar gráfico
            self.update_plot()
            
            # Focus al primer campo para siguiente entrada
            self.raw_input.setFocus()
            
        except ValueError:
            QMessageBox.warning(self, "Error de Entrada", 
                              "Por favor ingrese valores numéricos válidos.\n\n"
                              "Ejemplo:\n"
                              "Valor Crudo: 512\n"
                              "Valor Referencia: 90.0")
    
    def remove_point(self, row):
        """Elimina un punto de calibración específico"""
        if row < self.points_table.rowCount():
            # Obtener información de la fila a eliminar
            sensor_text = self.points_table.item(row, 0).text()
            sensor_idx = 0 if "Potenciómetro 1" in sensor_text else (1 if "Potenciómetro 2" in sensor_text else 2)
            
            # Encontrar el índice correcto en los datos de calibración
            if len(self.calibration.calibration_data["raw_values"][sensor_idx]) > 0:
                # Remover el último punto agregado para este sensor (simplificación)
                self.calibration.calibration_data["raw_values"][sensor_idx].pop()
                self.calibration.calibration_data["reference_values"][sensor_idx].pop()
                
                # Recrear tabla completa (más simple que manejar índices)
                self.update_table()
                self.update_plot()
                
                # Resetear calibración si hay cambios
                self.calibration.is_calibrated[sensor_idx] = False
    
    def update_table(self):
        """Actualiza la tabla completa con los datos actuales"""
        self.points_table.setRowCount(0)
        
        for sensor_idx in range(3):
            sensor_names = ["Potenciómetro 1 (Base)", "Potenciómetro 2 (Art. 1)", "Potenciómetro 3 (Art. 2)"]
            raw_vals = self.calibration.calibration_data["raw_values"][sensor_idx]
            ref_vals = self.calibration.calibration_data["reference_values"][sensor_idx]
            
            for i, (raw_val, ref_val) in enumerate(zip(raw_vals, ref_vals)):
                row = self.points_table.rowCount()
                self.points_table.insertRow(row)
                self.points_table.setItem(row, 0, QTableWidgetItem(sensor_names[sensor_idx]))
                self.points_table.setItem(row, 1, QTableWidgetItem(f"{raw_val:.2f}"))
                self.points_table.setItem(row, 2, QTableWidgetItem(f"{ref_val:.2f}"))
                
                # Botón eliminar
                delete_btn = QPushButton("🗑️")
                delete_btn.clicked.connect(lambda checked, r=row: self.remove_point(r))
                delete_btn.setStyleSheet("QPushButton { background-color: #f44336; color: white; }")
                self.points_table.setCellWidget(row, 3, delete_btn)
    
    def perform_calibration(self):
        """Realiza la calibración y actualiza la interfaz"""
        if self.calibration.perform_calibration():
            # Actualizar información de estado
            calibrated_sensors = [i for i in range(3) if self.calibration.is_calibrated[i]]
            if calibrated_sensors:
                equations = []
                for i in calibrated_sensors:
                    equations.append(f"Sensor {i+1}: {self.calibration.get_calibration_equation(i)}")
                
                self.info_label.setText("Ecuaciones:\n" + "\n".join(equations))
                self.info_label.setStyleSheet("padding: 5px; background-color: #c8e6c9; border-radius: 3px; color: #2e7d32;")
                self.update_plot()
                
                # Mostrar estadísticas detalladas
                stats = self.calibration.get_calibration_stats()
                message = "✅ Calibración realizada correctamente\n\n"
                for sensor_name, sensor_stats in stats.items():
                    if sensor_stats["status"] == "Calibrado":
                        message += f"📈 {sensor_name}: {sensor_stats['equation']}\n"
                        message += f"📊 Puntos: {sensor_stats['num_points']} | R²: {sensor_stats['r_squared']:.4f}\n\n"
                
                message += "💡 R² cercano a 1.0 indica mejor ajuste"
                QMessageBox.information(self, "Calibración Exitosa", message)
        else:
            QMessageBox.warning(self, "Error de Calibración", 
                              "❌ Se necesitan al menos 2 puntos por sensor para realizar la calibración.\n\n"
                              "💡 Agregue más puntos de referencia conocidos para cada sensor.")
    
    def clear_data(self):
        """Limpia todos los datos y resetea la interfaz"""
        reply = QMessageBox.question(self, "Confirmar Limpieza", 
                                   "⚠️ ¿Está seguro de que desea eliminar todos los datos de calibración?\n\n"
                                   "Esta acción no se puede deshacer.",
                                   QMessageBox.Yes | QMessageBox.No,
                                   QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            self.calibration.clear_calibration_data()
            self.points_table.setRowCount(0)
            self.info_label.setText("Ecuación: No calibrado")
            self.info_label.setStyleSheet("padding: 5px; background-color: #f0f0f0; border-radius: 3px;")
            self.update_plot()
    
    def update_plot(self):
        """Actualiza el gráfico de calibración en tiempo real"""
        self.figure.clear()
        
        colors = ['blue', 'green', 'red']
        sensor_names = ['Base (Pot 1)', 'Art. 1 (Pot 2)', 'Art. 2 (Pot 3)']
        
        for sensor_idx in range(3):
            ax = self.figure.add_subplot(1, 3, sensor_idx + 1)
            
            raw_vals = self.calibration.calibration_data["raw_values"][sensor_idx]
            ref_vals = self.calibration.calibration_data["reference_values"][sensor_idx]
            
            if len(raw_vals) > 0:
                # Puntos de calibración
                ax.scatter(raw_vals, ref_vals, color=colors[sensor_idx], s=50, alpha=0.7, 
                          label='Puntos de Calibración', zorder=5)
                
                # Línea de regresión si está calibrado
                if self.calibration.is_calibrated[sensor_idx]:
                    x_min, x_max = min(raw_vals), max(raw_vals)
                    x_range = x_max - x_min
                    x_line = np.linspace(x_min - x_range*0.1, x_max + x_range*0.1, 100)
                    y_line = [self.calibration.calibrate_value(sensor_idx, x) for x in x_line]
                    ax.plot(x_line, y_line, 'r-', linewidth=2, 
                           label=f'R² = {self.calibration.r_squared[sensor_idx]:.3f}', zorder=3)
                    
                    # Líneas de grilla para los puntos
                    for raw, ref in zip(raw_vals, ref_vals):
                        ax.axvline(x=raw, color='gray', linestyle='--', alpha=0.3, zorder=1)
                        ax.axhline(y=ref, color='gray', linestyle='--', alpha=0.3, zorder=1)
                    
                    ax.legend()
            else:
                # Mensaje cuando no hay datos
                ax.text(0.5, 0.5, f'No hay puntos\npara {sensor_names[sensor_idx]}', 
                       horizontalalignment='center', verticalalignment='center',
                       transform=ax.transAxes, fontsize=10, 
                       bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgray"))
            
            ax.set_xlabel('Valor Crudo')
            ax.set_ylabel('Valor Real')
            ax.set_title(sensor_names[sensor_idx])
            ax.grid(True, alpha=0.3)
        
        # Mejorar aspecto del gráfico
        self.figure.tight_layout()
        self.canvas.draw()
    
    def save_calibration(self):
        """Guarda la calibración actual en archivo"""
        if not any(self.calibration.is_calibrated):
            QMessageBox.warning(self, "Sin Calibración", 
                              "❌ No hay calibración activa para guardar.\n\n"
                              "💡 Primero realice una calibración con los datos ingresados.")
            return
        
        filename = f"calibration_{self.sensor_name.lower().replace(' ', '_')}.json"
        if self.calibration.save_calibration(filename):
            calibrated_count = sum(self.calibration.is_calibrated)
            QMessageBox.information(self, "Guardado Exitoso", 
                                  f"✅ Calibración guardada correctamente\n\n"
                                  f"📁 Archivo: {filename}\n"
                                  f"📊 Sensores calibrados: {calibrated_count}/3")
        else:
            QMessageBox.warning(self, "Error de Guardado", 
                              f"❌ Error al guardar la calibración en {filename}\n\n"
                              "💡 Verifique permisos de escritura en el directorio.")
    
    def load_calibration(self):
        """Carga una calibración desde archivo"""
        filename = f"calibration_{self.sensor_name.lower().replace(' ', '_')}.json"
        if self.calibration.load_calibration(filename):
            self.update_table()
            
            # Actualizar información de estado
            calibrated_sensors = [i for i in range(3) if self.calibration.is_calibrated[i]]
            if calibrated_sensors:
                equations = []
                for i in calibrated_sensors:
                    equations.append(f"Sensor {i+1}: {self.calibration.get_calibration_equation(i)}")
                
                self.info_label.setText("Ecuaciones:\n" + "\n".join(equations))
                self.info_label.setStyleSheet("padding: 5px; background-color: #c8e6c9; border-radius: 3px; color: #2e7d32;")
            
            self.update_plot()
            
            calibrated_count = sum(self.calibration.is_calibrated)
            QMessageBox.information(self, "Carga Exitosa", 
                                  f"✅ Calibración cargada correctamente\n\n"
                                  f"📁 Archivo: {filename}\n"
                                  f"📊 Sensores calibrados: {calibrated_count}/3")
        else:
            QMessageBox.warning(self, "Error de Carga", 
                              f"❌ No se pudo cargar la calibración\n\n"
                              f"📁 Archivo buscado: {filename}\n"
                              "💡 Verifique que el archivo existe y es válido.")
    
    def accept(self):
        """Acepta el diálogo y emite la señal de calibración actualizada"""
        # Emitir señal con la calibración actual
        self.calibration_updated.emit(self.calibration)
        super().accept()
    
    def set_calibration(self, calibration):
        """Establece una calibración existente en el diálogo"""
        self.calibration = calibration
        self.update_table()
        
        calibrated_sensors = [i for i in range(3) if calibration.is_calibrated[i]]
        if calibrated_sensors:
            equations = []
            for i in calibrated_sensors:
                equations.append(f"Sensor {i+1}: {calibration.get_calibration_equation(i)}")
            
            self.info_label.setText("Ecuaciones:\n" + "\n".join(equations))
            self.info_label.setStyleSheet("padding: 5px; background-color: #c8e6c9; border-radius: 3px; color: #2e7d32;")
        
        self.update_plot()
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
    def perform_calibration(self) -> bool:
        """
        Realiza la calibración por regresión lineal para los tres sensores.
        
        Returns:
            bool: True si la calibración fue exitosa, False si no hay suficientes datos.
        """
        success = True
        for i in range(3):
            if len(self.calibration_data["raw_values"][i]) < 2:
                success = False
                continue
            
            # Preparar datos para scikit-learn (formato matricial)
            X = np.array(self.calibration_data["raw_values"][i]).reshape(-1, 1)
            y = np.array(self.calibration_data["reference_values"][i])
            
            # Realizar regresión lineal
            self.models[i].fit(X, y)
            
            # Extraer parámetros de la ecuación y = mx + b
            self.slopes[i] = self.models[i].coef_[0]
            self.intercepts[i] = self.models[i].intercept_
            self.r_squared[i] = self.models[i].score(X, y)
            self.is_calibrated[i] = True
        
        return success
    
    def calibrate_value(self, sensor_idx, raw_value: float) -> Optional[float]:
        """
        Calibra un valor crudo usando el modelo del sensor indicado.
        
        Args:
            sensor_idx: Índice del sensor (0, 1 o 2)
            raw_value: Valor crudo a calibrar
        
        Returns:
            float: Valor calibrado, o None si no hay calibración activa
        """
        if not self.is_calibrated[sensor_idx]:
            return None
        
        return self.models[sensor_idx].predict([[raw_value]])[0]
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
        # Verificar que al menos un sensor esté calibrado
        if not any(self.is_calibrated):
            return False
        
        # Preparar datos para JSON
        data = {
            "slopes": self.slopes,
            "intercepts": self.intercepts,
            "r_squared": self.r_squared,
            "is_calibrated": self.is_calibrated,
            "calibration_data": self.calibration_data,
            "timestamp": "generated_by_sensoracore_anglearm"
        }
        
        try:
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception:
            return False
    
    def load_calibration(self, filepath: str) -> bool:
        """
        Carga una calibración desde un archivo JSON.
        
        Args:
            filepath: Ruta del archivo a cargar
            
        Returns:
            bool: True si se cargó exitosamente
        """
        if not os.path.exists(filepath):
            return False
        
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            # Restaurar parámetros
            self.slopes = data["slopes"]
            self.intercepts = data["intercepts"]
            self.r_squared = data["r_squared"]
            self.is_calibrated = data["is_calibrated"]
            self.calibration_data = data["calibration_data"]
            
            # Recrear los modelos de scikit-learn
            for i in range(3):
                if self.is_calibrated[i]:
                    X = np.array(self.calibration_data["raw_values"][i]).reshape(-1, 1)
                    y = np.array(self.calibration_data["reference_values"][i])
                    self.models[i].fit(X, y)
            
            return True
        except Exception:
            return False
    
    def get_calibration_stats(self) -> dict:
        """
        Retorna estadísticas de la calibración actual
        
        Returns:
            dict: Diccionario con estadísticas de calibración
        """
        stats = {}
        for i in range(3):
            sensor_name = f"sensor_{i}"
            if self.is_calibrated[i]:
                stats[sensor_name] = {
                    "status": "Calibrado",
                    "equation": self.get_calibration_equation(i),
                    "num_points": len(self.calibration_data["raw_values"][i]),
                    "r_squared": self.r_squared[i],
                    "slope": self.slopes[i],
                    "intercept": self.intercepts[i]
                }
            else:
                stats[sensor_name] = {"status": "No calibrado"}
        
        return stats
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
        self.brazo_calibration = AngleArm_X3_LinearCalibration()  # Sistema de calibración multi-sensor
        
        # --- Variables para almacenar datos de los sensores ---
        self.brazo_angulos = [[], [], []]  # Lista de listas para 3 potenciómetros
        self.brazo_lecturas = [[], [], []]  # Lecturas ADC de los 3 potenciómetros
        self.brazo_capacitive_states = []   # Estados del sensor capacitivo
        self.brazo_max_points = 100      # Número máximo de puntos a almacenar
        
        # SISTEMA DE ACTUALIZACIONES
        self.thread_AngleArm = None             # Hilo para monitorear el sensor de brazo de ángulos
        self.monietoreando_AngleArm = False     # Indica si se está monitoreando el sensor
        self.pending_updates = False            # Indica si hay actualizaciones pendientes
        self.pending_AngleArm_data = None        # Datos pendientes de actualización
        
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
        # --- CREAR DIÁLOGO DE CALIBRACIÓN ---
        dialog = CalibrationDialog("Brazo Ángulos", self.brazo_calibration, self)  # Pasar nombre del sensor, calibración y ventana padre
        
        # --- MOSTRAR DIÁLOGO Y PROCESAR RESULTADO ---
        if dialog.exec() == QDialog.Accepted:    # Si el usuario presiona OK/Aplicar
            # Actualizar estado de calibración en la interfaz
            self.update_calibration_status()
    
    # MÉTODO: ACTUALIZAR ESTADO DE CALIBRACIÓN EN LA INTERFAZ
    def update_calibration_status(self):
        """
        Actualiza el estado de calibración en la interfaz gráfica
        
        Propósito: Reflejar si los sensores están calibrados o no
        Lógica: Verifica el estado de calibración y actualiza etiquetas
        UI: Muestra mensaje de éxito o error según corresponda
        Estado: No cambia flags, solo actualiza visualización
        """
        if hasattr(self, 'brazo_calibration_status_label'):  # Verificar que existe la etiqueta
            # Verificar qué sensores están calibrados
            calibrated_sensors = [i for i in range(3) if self.brazo_calibration.is_calibrated[i]]
            
            if calibrated_sensors:   # Si hay al menos un sensor calibrado
                calibrated_count = len(calibrated_sensors)
                sensor_names = ["Base", "Art.1", "Art.2"]
                calibrated_names = [sensor_names[i] for i in calibrated_sensors]
                
                self.brazo_calibration_status_label.setText(
                    f"Calibración: ✓ {calibrated_count}/3 sensores calibrados ({', '.join(calibrated_names)})"
                )
                # Cambiar estilo a verde para indicar calibración activa
                self.brazo_calibration_status_label.setStyleSheet("""
                    font-size: 14px;
                    font-weight: bold;
                    color: #155724;
                    padding: 8px;
                    background-color: #d4edda;
                    border-radius: 4px;
                    border: 1px solid #c3e6cb;
                    margin-top: 5px;
                """)
            else:
                # Sin calibración activa
                self.brazo_calibration_status_label.setText("Calibración: No aplicada")
                self.brazo_calibration_status_label.setStyleSheet("""
                    font-size: 14px;
                    font-weight: bold;
                    color: #856404;
                    padding: 8px;
                    background-color: #fff3cd;
                    border-radius: 4px;
                    border: 1px solid #ffeaa7;
                    margin-top: 5px;
                """)
    
    def update_angleArm_data(self, pot1_ADC, pot1_angulo, pot2_ADC, pot2_angulo, pot3_ADC, pot3_angulo, sensor_estado):
        """
        Actualiza los datos de los sensores de brazo de ángulos con calibración aplicada
        
        Propósito: Almacenar las lecturas actuales de los sensores con valores calibrados
        Lógica: Añade nuevos valores a las listas, aplica calibración si está disponible
        UI: Actualiza visualización en tiempo real mostrando valores crudos y calibrados
        Estado: No cambia flags, solo actualiza datos
        """
        # --- ALMACENAR DATOS EN HISTORIAL ---
        lecturas = [pot1_ADC, pot2_ADC, pot3_ADC]
        angulos = [pot1_angulo, pot2_angulo, pot3_angulo]
        
        # Aplicar calibración si está disponible
        angulos_calibrados = []
        for i in range(3):
            self.brazo_lecturas[i].append(lecturas[i])
            
            if self.brazo_calibration.is_calibrated[i]:
                angulo_calibrado = self.brazo_calibration.calibrate_value(i, lecturas[i])
                angulos_calibrados.append(angulo_calibrado)
                self.brazo_angulos[i].append(angulo_calibrado)
            else:
                angulos_calibrados.append(angulos[i])
                self.brazo_angulos[i].append(angulos[i])
        
        self.brazo_capacitive_states.append(sensor_estado)
        
        # --- MANTENER TAMAÑO MÁXIMO DE DATOS ---
        for i in range(3):
            if len(self.brazo_lecturas[i]) > self.brazo_max_points:
                self.brazo_lecturas[i].pop(0)
                self.brazo_angulos[i].pop(0)
        
        if len(self.brazo_capacitive_states) > self.brazo_max_points:
            self.brazo_capacitive_states.pop(0)
        
        # --- ACTUALIZAR ETIQUETAS DE ESTADO CON VALORES CALIBRADOS ---
        try:
            if hasattr(self, 'brazo_labels') and self.brazo_labels is not None:
                for i in range(3):
                    pot_key = f'pot{i+1}'
                    if pot_key in self.brazo_labels and self.brazo_labels[pot_key] is not None:
                        if self.brazo_calibration.is_calibrated[i]:
                            self.brazo_labels[pot_key].setText(
                                f"Potenciómetro {i+1}: Lectura: {lecturas[i]} | Ángulo: {angulos[i]}° | Calibrado: {angulos_calibrados[i]:.1f}°"
                            )
                        else:
                            self.brazo_labels[pot_key].setText(
                                f"Potenciómetro {i+1}: Lectura: {lecturas[i]} | Ángulo: {angulos[i]}°"
                            )
                
                # Actualizar sensor capacitivo
                if hasattr(self, 'capacitive_label') and self.capacitive_label is not None:
                    sensor_text = "Activo" if sensor_estado else "Inactivo"
                    self.capacitive_label.setText(f"Sensor Capacitivo: {sensor_text}")
        except RuntimeError:
            # Widget has been deleted, stop monitoring
            if hasattr(self, 'monietoreando_AngleArm'):
                self.monietoreando_AngleArm = False
            return
        
        # --- PREPARAR DATOS PARA GRÁFICA ---
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
        
        # --- MARCAR PARA ACTUALIZACIÓN GRÁFICA ---
        self.pending_updates = True              # Flag para redibujado pendiente
        self.pending_AngleArm_data = (lecturas, angulos_calibrados, sensor_estado)  # Datos específicos pendientes
        
        # --- HABILITAR EXPORTACIÓN SI HAY DATOS ---
        if len(self.brazo_lecturas[0]) > 0:
            self.brazo_export_btn.setEnabled(True)
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
