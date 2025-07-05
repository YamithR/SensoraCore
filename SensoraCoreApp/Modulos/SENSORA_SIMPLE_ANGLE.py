from IMPORTACIONES import *  # Importar todo lo necesario desde el módulo de importaciones

#|------------------------|
#| Interfaz del programa: |
#|------------------------|

# =====================================================================================
# MÉTODO: INTERFAZ DEL SENSOR DE ÁNGULO SIMPLE
# =====================================================================================

def anguloSimple_UI(self):
    """
    Crea y muestra la interfaz específica para el sensor de ángulo simple

    Propósito: Interfaz completa para monitorear potenciómetro conectado al ESP32
    Funcionalidad: Diagrama de conexiones, controles de monitoreo, visualización de datos
    Sensor: Potenciómetro 10kΩ en GPIO 32 del ESP32
    """
    # --- OCULTAR PANTALLA DE BIENVENIDA ---
    self.welcome_widget.setVisible(False)   # Esconder mensaje inicial
    
    # --- CREAR WIDGET PRINCIPAL DEL SENSOR ---
    sensor_widget = QWidget()               # Contenedor principal de la interfaz
    layout = QVBoxLayout(sensor_widget)     # Layout vertical para organizar elementos
    layout.setSpacing(20)                   # Espacio entre secciones: 20px
    
    # =====================================================================================
    # SECCIÓN: TÍTULO Y DESCRIPCIÓN DEL SENSOR
    # =====================================================================================
    
    # --- TÍTULO PRINCIPAL ---
    title = QLabel("🎛️ Sensor de Ángulo Simple")  # Título con emoji identificativo
    title.setStyleSheet("""
        font-size: 20px;                    /* Tamaño grande para destacar */
        font-weight: bold;                  /* Negrita para jerarquía visual */
        color: #007bff;                     /* Azul corporativo */
        margin-bottom: 10px;                /* Separación inferior */
    """)
    layout.addWidget(title)                 # Agregar título al layout principal
    
    # --- DESCRIPCIÓN FUNCIONAL ---
    description = QLabel("Monitorea el ángulo en tiempo real usando un potenciómetro conectado al GPIO 32 del ESP32")
    description.setStyleSheet("""
        font-size: 14px;                    /* Tamaño legible */
        color: #6c757d;                     /* Gris suave */
        margin-bottom: 20px;                /* Separación inferior generosa */
    """)
    description.setWordWrap(True)           # Permitir salto de línea automático
    layout.addWidget(description)           # Agregar descripción al layout
    
    # =====================================================================================
    # SECCIÓN: DIAGRAMA DE CONEXIONES ESP32
    # =====================================================================================
    
    # --- GRUPO DEL DIAGRAMA ---
    diagram_group = QGroupBox("🔌 Diagrama de Conexiones ESP32")  # Caja agrupada con título
    diagram_layout = QVBoxLayout(diagram_group)  # Layout vertical para el contenido
    
    # --- DIAGRAMA ASCII DETALLADO ---
    diagram_text = QLabel("""
<pre style="font-family: 'Courier New', monospace; font-size: 12px; line-height: 1.4; color: #495057;">
┌─────────────────────────────────┐
│  ESP32 DevKit V1                │
│                                 │
│  3V3  ○ ←── Potenciómetro (+)   │
│  D32  ○ ←── Potenciómetro (S)   │
│  GND  ○ ←── Potenciómetro (-)   │
│                                 │
│  LED integrado: GPIO 2          │
└─────────────────────────────────┘

<b>Potenciómetro 10kΩ:</b>
• Pin (+): Alimentación 3.3V
• Pin (-): Tierra (GND)  
• Pin (S): Señal analógica → GPIO 32
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
    
    # --- NOTA IMPORTANTE DE SEGURIDAD ---
    note_label = QLabel("💡 <b>Nota:</b> Asegúrate de conectar el potenciómetro correctamente antes de iniciar el monitoreo")
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
    
    # =====================================================================================
    # SECCIÓN: CONTROLES DE MONITOREO
    # =====================================================================================
    
    # --- GRUPO DE CONTROLES ---
    controls_group = QGroupBox("Controles")  # Caja agrupada para controles
    controls_layout = QVBoxLayout(controls_group)  # Layout vertical para controles
    # --- ETIQUETA DE ESTADO EN TIEMPO REAL ---
    # Muestra lectura ADC y ángulo calculado en tiempo real
    self.angulo_label = QLabel("Lectura ADC: -- | Ángulo: --")  # Texto inicial placeholder
    self.angulo_label.setStyleSheet("""
        font-size: 16px;                    /* Tamaño de fuente: 16px para visibilidad */
        font-weight: bold;                  /* Texto en negrita para destacar */
        color: #495057;                     /* Color gris oscuro para legibilidad */
        padding: 10px;                      /* Espacio interno: 10px en todos los lados */
        background-color: #f8f9fa;          /* Fondo gris muy claro */
        border-radius: 6px;                 /* Esquinas redondeadas modernas */
        border: 2px solid #dee2e6;          /* Borde gris claro de 2px */
    """)
    controls_layout.addWidget(self.angulo_label)  # Agregar etiqueta a controles
    
    # --- ETIQUETA DE CALIBRACIÓN ---
    # Muestra el estado de calibración y valores calibrados
    self.calibration_status_label = QLabel("Calibración: No aplicada")  # Estado inicial
    self.calibration_status_label.setStyleSheet("""
        font-size: 14px;                    /* Tamaño menor para información secundaria */
        font-weight: bold;                  /* Texto en negrita */
        color: #856404;                     /* Color ámbar para indicar estado */
        padding: 8px;                       /* Espacio interno menor */
        background-color: #fff3cd;          /* Fondo ámbar claro */
        border-radius: 4px;                 /* Esquinas redondeadas menores */
        border: 1px solid #ffeaa7;          /* Borde ámbar */
        margin-top: 5px;                    /* Separación superior */
    """)
    controls_layout.addWidget(self.calibration_status_label)  # Agregar etiqueta de calibración
    
    # --- BOTONES DE CONTROL PRINCIPAL ---
    buttons_layout = QHBoxLayout()           # Layout horizontal para botones principales
    # BOTÓN INICIAR - Color verde para indicar acción positiva
    self.start_btn = QPushButton("▶️ Iniciar Monitoreo")  # Botón con emoji de play
    self.start_btn.clicked.connect(self.toggle_angulo_monitoring)  # Conectar a método de control        
    self.start_btn.setStyleSheet("QPushButton { background-color: #28a745; border-color: #28a745; }")  # Verde Bootstrap
    buttons_layout.addWidget(self.start_btn)  # Agregar al layout de botones
    
    # BOTÓN CALIBRACIÓN - Color azul para función de configuración
    self.calibrate_btn = QPushButton("⚙️ Calibrar Sensor")  # Botón con emoji de configuración
    self.calibrate_btn.clicked.connect(self.open_calibration_dialog)  # Conectar a método de calibración
    self.calibrate_btn.setStyleSheet("QPushButton { background-color: #007bff; border-color: #007bff; color: white; padding: 10px; }")  # Azul Bootstrap
    buttons_layout.addWidget(self.calibrate_btn)  # Agregar al layout de botones
    
    controls_layout.addLayout(buttons_layout)  # Agregar botones principales a controles
    
    # --- BOTONES DE ACCIONES SECUNDARIAS ---
    actions_layout = QHBoxLayout()           # Layout horizontal para acciones secundarias
    
    # BOTÓN LIMPIAR - Para borrar datos de la gráfica
    self.clear_btn = QPushButton("🗑️ Limpiar Gráfica")  # Botón con emoji de papelera
    self.clear_btn.clicked.connect(self.clear_graph_SIMPLE_ANGLE)  # Conectar a método de limpieza
    actions_layout.addWidget(self.clear_btn)  # Agregar al layout de acciones
    # BOTÓN EXPORTAR - Para guardar datos en Excel
    self.export_btn = QPushButton("📊 Exportar Excel")  # Botón con emoji de gráfica
    self.export_btn.clicked.connect(self.export_to_excel)  # Conectar a método de exportación
    self.export_btn.setEnabled(False)       # Se habilita solo cuando hay datos
    actions_layout.addWidget(self.export_btn)  # Agregar al layout de acciones
    
    controls_layout.addLayout(actions_layout)  # Agregar acciones secundarias a controles
    layout.addWidget(controls_group)         # Agregar grupo de controles al layout principal
    
    # =====================================================================================
    # SECCIÓN: GRÁFICA EN TIEMPO REAL
    # =====================================================================================
    
    # --- GRUPO DE GRÁFICA ---
    graph_group = QGroupBox("Gráfica en Tiempo Real")  # Caja agrupada para la gráfica
    graph_layout = QVBoxLayout(graph_group)  # Layout vertical para la gráfica
    
    # --- CONFIGURAR MATPLOTLIB CON COLORES MEJORADOS ---
    self.figure = Figure(figsize=(10, 6), dpi=100, facecolor='white')  # Figura de matplotlib
    self.canvas = FigureCanvasQTAgg(self.figure)  # Canvas para renderizar la figura
    self.ax = self.figure.add_subplot(111)   # Subplot principal (1 fila, 1 columna, posición 1)
    
    # --- PERSONALIZACIÓN VISUAL DE LA GRÁFICA ---
    self.ax.set_facecolor('#f8f9fa')         # Fondo gris muy claro
    self.ax.grid(True, linestyle='--', alpha=0.7, color='#dee2e6')  # Grid con líneas punteadas
    self.ax.set_xlabel('Muestras', fontsize=12, fontweight='bold', color='#495057')  # Etiqueta eje X
    self.ax.set_ylabel('Ángulo (°)', fontsize=12, fontweight='bold', color='#495057')  # Etiqueta eje Y
    self.ax.set_title('Monitoreo de Ángulo en Tiempo Real', fontsize=14, fontweight='bold', color='#007bff')  # Título
    
    # --- LÍNEA DE DATOS CON ESTILO DESTACADO ---
    self.line, = self.ax.plot([], [], 'o-', linewidth=3, markersize=6,  # Línea con marcadores circulares
                            color='#007bff', markerfacecolor='#0056b3',  # Colores azules
                            markeredgecolor='white', markeredgewidth=2)  # Borde blanco en marcadores
    
    # --- CONFIGURAR LÍMITES INICIALES ---
    self.ax.set_xlim(0, 100)                 # Eje X: 0 a 100 muestras
    self.ax.set_ylim(-135, 135)                 # Eje Y: -135 a 135 grados (rango del potenciómetro)
    
    # --- OPTIMIZAR LAYOUT DE LA GRÁFICA ---
    self.figure.tight_layout(pad=2.0)        # Ajuste automático con padding de 2.0
    
    # --- INICIALIZAR CANVAS CON DIBUJO INICIAL ---
    self.canvas.draw()                       # Renderizar gráfica inicial vacía
    
    graph_layout.addWidget(self.canvas)      # Agregar canvas al grupo de gráfica
    layout.addWidget(graph_group)           # Agregar grupo de gráfica al layout principal
    
    # =====================================================================================
    # FINALIZACIÓN: MOSTRAR INTERFAZ EN PANEL DERECHO
    # =====================================================================================
    # --- CONFIGURAR PANEL DERECHO ---
    self.sensor_details.setWidget(sensor_widget)  # Establecer widget como contenido del área de scroll
    self.sensor_details.setVisible(True)     # Hacer visible el área de detalles del sensor
    
    # --- ACTUALIZAR ESTADO DE CALIBRACIÓN ---
    self.update_calibration_status()         # Mostrar estado actual de calibración

# =====================================================================================
# DIÁLOGO DE CALIBRACIÓN POR REGRESIÓN LINEAL PARA ÁNGULO SIMPLE
# =====================================================================================

# Propósito: Permitir al usuario calibrar sensores visualmente
# Función: Interfaz gráfica para calibración de sensores por regresión lineal

class CalibrationDialog(QDialog):
    """
    Diálogo para calibración por regresión lineal de sensores
    
    Propósito: Interfaz gráfica completa para calibrar sensores analógicos
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
            calibration_instance: Instancia de LinearCalibration existente (opcional)
            parent: Ventana padre
        """
        super().__init__(parent)
        self.sensor_name = sensor_name
        self.calibration = calibration_instance if calibration_instance else LinearCalibration()
        self.setup_ui()
        self.update_plot()
    
    def setup_ui(self):
        """Configurar toda la interfaz de usuario del diálogo"""
        self.setWindowTitle(f"Calibración por Regresión Lineal - {self.sensor_name}")
        self.setFixedSize(900, 700)  # Tamaño fijo para mejor diseño
        
        # Layout principal vertical
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        
        # ==================== GRUPO DE ENTRADA DE DATOS ====================
        input_group = QGroupBox("Agregar Punto de Calibración")
        input_group.setFont(QFont("Arial", 10, QFont.Bold))
        input_layout = QGridLayout(input_group)
        
        # Campos de entrada
        input_layout.addWidget(QLabel("Valor Crudo del Sensor:"), 0, 0)
        self.raw_input = QLineEdit()
        self.raw_input.setPlaceholderText("Ej: 512 (lectura ADC)")
        input_layout.addWidget(self.raw_input, 0, 1)
        
        input_layout.addWidget(QLabel("Valor Real (Referencia):"), 0, 2)
        self.ref_input = QLineEdit()
        self.ref_input.setPlaceholderText("Ej: 90.0 (grados reales)")
        input_layout.addWidget(self.ref_input, 0, 3)
        
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
        input_layout.addWidget(self.add_point_btn, 0, 4)
        
        layout.addWidget(input_group)
        
        # ==================== TABLA DE PUNTOS DE CALIBRACIÓN ====================
        table_group = QGroupBox("Puntos de Calibración")
        table_group.setFont(QFont("Arial", 10, QFont.Bold))
        table_layout = QVBoxLayout(table_group)
        
        self.points_table = QTableWidget(0, 3)  # 3 columnas: Crudo, Referencia, Eliminar
        self.points_table.setHorizontalHeaderLabels(["Valor Crudo", "Valor Referencia", "Acción"])
        
        # Configurar encabezados de tabla
        header = self.points_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Fixed)
        self.points_table.setColumnWidth(2, 80)
        
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
        
        self.figure = Figure(figsize=(8, 4))
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
            raw_val = float(self.raw_input.text())
            ref_val = float(self.ref_input.text())
            
            # Agregar al modelo de calibración
            self.calibration.add_calibration_point(raw_val, ref_val)
            
            # Actualizar tabla
            row = self.points_table.rowCount()
            self.points_table.insertRow(row)
            self.points_table.setItem(row, 0, QTableWidgetItem(f"{raw_val:.2f}"))
            self.points_table.setItem(row, 1, QTableWidgetItem(f"{ref_val:.2f}"))
            
            # Botón eliminar para esta fila
            delete_btn = QPushButton("🗑️")
            delete_btn.clicked.connect(lambda checked, r=row: self.remove_point(r))
            delete_btn.setStyleSheet("QPushButton { background-color: #f44336; color: white; }")
            self.points_table.setCellWidget(row, 2, delete_btn)
            
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
        if 0 <= row < len(self.calibration.calibration_data["raw_values"]):
            # Eliminar del modelo
            del self.calibration.calibration_data["raw_values"][row]
            del self.calibration.calibration_data["reference_values"][row]
            
            # Recrear tabla completa (más simple que manejar índices)
            self.update_table()
            self.update_plot()
            
            # Resetear calibración si hay cambios
            self.calibration.is_calibrated = False
            self.info_label.setText("Ecuación: No calibrado (datos modificados)")
    
    def update_table(self):
        """Actualiza la tabla completa con los datos actuales"""
        self.points_table.setRowCount(0)
        raw_vals = self.calibration.calibration_data["raw_values"]
        ref_vals = self.calibration.calibration_data["reference_values"]
        
        for i, (raw_val, ref_val) in enumerate(zip(raw_vals, ref_vals)):
            row = self.points_table.rowCount()
            self.points_table.insertRow(row)
            self.points_table.setItem(row, 0, QTableWidgetItem(f"{raw_val:.2f}"))
            self.points_table.setItem(row, 1, QTableWidgetItem(f"{ref_val:.2f}"))
            
            # Botón eliminar
            delete_btn = QPushButton("🗑️")
            delete_btn.clicked.connect(lambda checked, r=i: self.remove_point(r))
            delete_btn.setStyleSheet("QPushButton { background-color: #f44336; color: white; }")
            self.points_table.setCellWidget(row, 2, delete_btn)
    
    def perform_calibration(self):
        """Realiza la calibración y actualiza la interfaz"""
        if self.calibration.perform_calibration():
            self.info_label.setText(f"Ecuación: {self.calibration.get_calibration_equation()}")
            self.info_label.setStyleSheet("padding: 5px; background-color: #c8e6c9; border-radius: 3px; color: #2e7d32;")
            self.update_plot()
            
            # Mostrar estadísticas detalladas
            stats = self.calibration.get_calibration_stats()
            QMessageBox.information(self, "Calibración Exitosa", 
                                  f"✅ Calibración realizada correctamente\n\n"
                                  f"📈 Ecuación: {stats['equation']}\n"
                                  f"📊 Puntos utilizados: {stats['num_points']}\n"
                                  f"🎯 Calidad (R²): {stats['r_squared']:.4f}\n\n"
                                  f"💡 R² cercano a 1.0 indica mejor ajuste")
        else:
            QMessageBox.warning(self, "Error de Calibración", 
                              "❌ Se necesitan al menos 2 puntos para realizar la calibración.\n\n"
                              "💡 Agregue más puntos de referencia conocidos.")
    
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
        ax = self.figure.add_subplot(111)
        
        raw_vals = self.calibration.calibration_data["raw_values"]
        ref_vals = self.calibration.calibration_data["reference_values"]
        
        if len(raw_vals) > 0:
            # Puntos de calibración
            ax.scatter(raw_vals, ref_vals, color='blue', s=50, alpha=0.7, 
                      label='Puntos de Calibración', zorder=5)
            
            # Línea de regresión si está calibrado
            if self.calibration.is_calibrated:
                x_min, x_max = min(raw_vals), max(raw_vals)
                x_range = x_max - x_min
                x_line = np.linspace(x_min - x_range*0.1, x_max + x_range*0.1, 100)
                y_line = [self.calibration.calibrate_value(x) for x in x_line]
                ax.plot(x_line, y_line, 'r-', linewidth=2, 
                       label=f'Regresión Lineal (R² = {self.calibration.r_squared:.3f})', zorder=3)
                
                # Líneas de grilla para los puntos
                for raw, ref in zip(raw_vals, ref_vals):
                    ax.axvline(x=raw, color='gray', linestyle='--', alpha=0.3, zorder=1)
                    ax.axhline(y=ref, color='gray', linestyle='--', alpha=0.3, zorder=1)
                
                ax.legend()
        else:
            # Mensaje cuando no hay datos
            ax.text(0.5, 0.5, 'No hay puntos de calibración\n\nAgregue puntos usando los campos de arriba', 
                   horizontalalignment='center', verticalalignment='center',
                   transform=ax.transAxes, fontsize=12, 
                   bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgray"))
        
        ax.set_xlabel('Valor Crudo del Sensor')
        ax.set_ylabel('Valor Real (Referencia)')
        ax.set_title(f'Calibración por Regresión Lineal - {self.sensor_name}')
        ax.grid(True, alpha=0.3)
        
        # Mejorar aspecto del gráfico
        self.figure.tight_layout()
        self.canvas.draw()
    
    def save_calibration(self, filepath: str) -> bool:
        """
        Guarda la calibración actual en archivo
        
        Args:
            filepath: Ruta donde guardar el archivo
            
        Returns:
            bool: True si se guardó exitosamente
        """
        if not self.calibration.is_calibrated:
            QMessageBox.warning(self, "Sin Calibración", 
                              "❌ No hay calibración activa para guardar.\n\n"
                              "💡 Primero realice una calibración con los datos ingresados.")
            return
        
        filename = f"calibration_{self.sensor_name.lower().replace(' ', '_')}.json"
        if self.calibration.save_calibration(filename):
            QMessageBox.information(self, "Guardado Exitoso", 
                                  f"✅ Calibración guardada correctamente\n\n"
                                  f"📁 Archivo: {filename}\n"
                                  f"📈 Ecuación: {self.calibration.get_calibration_equation()}")
        else:
            QMessageBox.warning(self, "Error de Guardado", 
                              f"❌ Error al guardar la calibración en {filename}\n\n"
                              "💡 Verifique permisos de escritura en el directorio.")
    
    def load_calibration(self):
        """Carga una calibración desde archivo"""
        filename = f"calibration_{self.sensor_name.lower().replace(' ', '_')}.json"
        if self.calibration.load_calibration(filename):
            self.update_table()
            self.info_label.setText(f"Ecuación: {self.calibration.get_calibration_equation()}")
            self.info_label.setStyleSheet("padding: 5px; background-color: #c8e6c9; border-radius: 3px; color: #2e7d32;")
            self.update_plot()
            
            stats = self.calibration.get_calibration_stats()
            QMessageBox.information(self, "Carga Exitosa", 
                                  f"✅ Calibración cargada correctamente\n\n"
                                  f"📁 Archivo: {filename}\n"
                                  f"📈 Ecuación: {stats['equation']}\n"
                                  f"📊 Puntos: {stats['num_points']}\n"
                                  f"🎯 Calidad (R²): {stats['r_squared']:.4f}")
        else:
            QMessageBox.warning(self, "Error de Carga", 
                              f"❌ No se pudo cargar la calibración\n\n"
                              f"📁 Archivo buscado: {filename}\n"
                              "💡 Verifique que el archivo existe y es válido.")
    
    def accept(self):
        """Acepta el diálogo y emite la señal de calibración actualizada"""
        self.calibration_updated.emit(self.calibration)
        super().accept()
    
    def set_calibration(self, calibration):
        """Establece una calibración existente en el diálogo"""
        self.calibration = calibration
        self.update_table()
        if calibration.is_calibrated:
            self.info_label.setText(f"Ecuación: {calibration.get_calibration_equation()}")
            self.info_label.setStyleSheet("padding: 5px; background-color: #c8e6c9; border-radius: 3px; color: #2e7d32;")
        self.update_plot()

#|------------------------|
#| Lógica del programa:   |
#|------------------------|

# =====================================================================================
# CLASE: HILO PARA SENSOR DE ÁNGULO SIMPLE
# =====================================================================================

# Propósito: Maneja la comunicación con ESP32 para el sensor de ángulo simple
# Funcionalidad: Recibe datos de potenciómetro y los convierte a ángulos

class AnguloSimpleThread(QThread):
    
    # --- SEÑAL PERSONALIZADA ---
    # Definir señal que emitirá datos cuando lleguen del ESP32
    # Signal(int, int) significa: (lectura_potenciometro, angulo_calculado)
        
    data_received = Signal(int, int)  # lectura, angulo
    
    def __init__(self, esp32_ip, port=8080):
        """
        Constructor del hilo para sensor de ángulo simple
        
        Parámetros:
        - esp32_ip: Dirección IP del ESP32 (ej: "192.168.1.100")
        - port: Puerto de comunicación TCP (por defecto 8080)
        """
        super().__init__()                        # Inicializar la clase padre QThread
        self.esp32_ip = esp32_ip                 # Guardar IP del ESP32 para conectar
        self.port = port                         # Guardar puerto de comunicación
        self.running = False                     # Flag para controlar el bucle principal
        self.sock = None                         # Variable para el socket de conexión
    
    def run(self):
        """
        Método principal del hilo - se ejecuta cuando se llama start()
        Este método corre en segundo plano y maneja toda la comunicación
        """
        self.running = True                      # Activar flag de ejecución
        try:
            # --- ESTABLECER CONEXIÓN TCP ---
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Crear socket TCP
            self.sock.settimeout(3)              # Timeout de 3 segundos para conexión inicial
            self.sock.connect((self.esp32_ip, self.port))  # Conectar al ESP32
            
            # --- CONFIGURAR MODO DE SENSOR ---
            self.sock.sendall(b'MODO:ANGULO_SIMPLE')  # Enviar comando para activar modo ángulo simple
            self.sock.settimeout(1)              # Timeout de 1 segundo para recepción de datos
            
            # --- BUCLE PRINCIPAL DE RECEPCIÓN ---
            while self.running:                  # Continuar mientras el hilo esté activo
                try:
                    # Recibir datos del ESP32 (máximo 64 bytes)
                    data = self.sock.recv(64)
                    if not data:                 # Si no llegan datos, terminar conexión
                        break
                    
                    # --- PROCESAR DATOS RECIBIDOS ---
                    msg = data.decode(errors='ignore').strip()  # Convertir bytes a string y limpiar
                    for line in msg.split('\n'):               # Procesar cada línea por separado
                        if line.startswith('POT:'):             # Buscar líneas con datos del potenciómetro
                            try:
                                # Parsear formato: "POT:1234,ANG:90"
                                parts = line.replace('POT:', '').split(',ANG:')  # Separar lectura y ángulo
                                lectura = int(parts[0])          # Convertir lectura a entero
                                angulo = int(parts[1])           # Convertir ángulo a entero
                                
                                # --- EMITIR SEÑAL CON DATOS ---
                                self.data_received.emit(lectura, angulo)  # Enviar datos a la interfaz principal
                            except:
                                pass                             # Ignorar errores de formato
                                
                except socket.timeout:                          # Si hay timeout, continuar esperando
                    continue
                    
        except Exception as e:                                  # Capturar cualquier error de conexión
            pass                                                # Ignorar errores (conexión perdida, etc.)
            
        finally:
            # --- LIMPIEZA AL TERMINAR ---
            if self.sock:                                       # Si hay socket activo
                try:
                    self.sock.sendall(b'STOP')                 # Enviar comando de parada al ESP32
                except:
                    pass                                        # Ignorar errores al enviar STOP
                self.sock.close()                              # Cerrar conexión TCP
    
    def stop(self):
        """
        Método para detener el hilo de forma segura
        Se llama desde el hilo principal para terminar la ejecución
        """
        self.running = False                                   # Desactivar flag de ejecución
        self.wait()                                           # Esperar a que termine el hilo

# =====================================================================================
# MÓDULO DE CALIBRACIÓN POR REGRESIÓN LINEAL PARA ÁNGULO SIMPLE
# =====================================================================================

# Propósito: Mejorar precisión de lecturas de sensores mediante calibración
# Función: Implementa calibración por regresión lineal para sensores analógicos

class LinearCalibration:
    """
    Clase para manejar calibración por regresión lineal de sensores
    
    Propósito: Aplicar calibración matemática a lecturas de sensores analógicos
    Funcionalidad: Permite agregar puntos de calibración, calcular regresión y aplicar corrección
    Uso típico: Para sensores de ángulo, distancia, presión que requieren precisión mejorada
    """
    
    def __init__(self):
        """Inicializar sistema de calibración vacío"""
        self.model = LinearRegression()          # Modelo de regresión lineal de scikit-learn
        self.is_calibrated = False              # Flag para saber si ya se calibró
        self.calibration_data = {               # Datos de calibración almacenados
            "raw_values": [],                   # Valores crudos del sensor (ADC, voltaje, etc.)
            "reference_values": []              # Valores de referencia conocidos (exactos)
        }
        # Parámetros de la ecuación y = mx + b
        self.slope = None                       # Pendiente (m)
        self.intercept = None                   # Intercepto (b)
        self.r_squared = None                   # Coeficiente de determinación (calidad del ajuste)
    
    def add_calibration_point(self, raw_value: float, reference_value: float):
        """
        Añade un punto de calibración al conjunto de datos
        
        Args:
            raw_value: Valor crudo leído del sensor (sin calibrar)
            reference_value: Valor exacto conocido (medido con instrumento preciso)
        
        Ejemplo:
            # Sensor lee 512 ADC, pero sabemos que corresponde a 90°
            calibration.add_calibration_point(512, 90.0)
        """
        self.calibration_data["raw_values"].append(raw_value)
        self.calibration_data["reference_values"].append(reference_value)
    
    def clear_calibration_data(self):
        """Limpia todos los datos de calibración y resetea el estado"""
        self.calibration_data = {"raw_values": [], "reference_values": []}
        self.is_calibrated = False
        self.slope = None
        self.intercept = None
        self.r_squared = None
    
    def perform_calibration(self) -> bool:
        """
        Realiza la calibración con los datos actuales usando regresión lineal
        
        Returns:
            bool: True si la calibración fue exitosa, False si no hay suficientes datos
        
        Proceso:
            1. Verifica que hay al menos 2 puntos (mínimo para línea)
            2. Aplica regresión lineal usando scikit-learn
            3. Extrae parámetros de la ecuación (pendiente, intercepto, R²)
            4. Marca el sistema como calibrado
        """
        if len(self.calibration_data["raw_values"]) < 2:
            return False  # Necesitamos mínimo 2 puntos para hacer una línea
        
        # Preparar datos para scikit-learn (formato matricial)
        X = np.array(self.calibration_data["raw_values"]).reshape(-1, 1)  # Valores X (crudos)
        y = np.array(self.calibration_data["reference_values"])           # Valores Y (referencia)
        
        # Realizar regresión lineal
        self.model.fit(X, y)
        
        # Extraer parámetros de la ecuación y = mx + b
        self.slope = self.model.coef_[0]           # Pendiente (m)
        self.intercept = self.model.intercept_     # Intercepto (b)
        self.r_squared = self.model.score(X, y)   # R² (calidad del ajuste: 0-1, 1 es perfecto)
        self.is_calibrated = True
        
        return True
    
    def calibrate_value(self, raw_value: float) -> Optional[float]:
        """
        Aplica calibración a un valor crudo del sensor
        
        Args:
            raw_value: Valor sin calibrar del sensor
            
        Returns:
            float: Valor calibrado, o None si no hay calibración activa
            
        Ejemplo:
            # Si calibración es y = 0.176x - 90.112
            # raw_value = 1000 → calibrated = 0.176*1000 - 90.112 = 85.888
        """
        if not self.is_calibrated:
            return None  # No se puede calibrar sin datos
        
        return self.model.predict([[raw_value]])[0]
    
    def get_calibration_equation(self) -> str:
        """
        Retorna la ecuación de calibración como string legible
        
        Returns:
            str: Ecuación en formato "y = mx + b (R² = valor)"
        """
        if not self.is_calibrated:
            return "No calibrado"
        
        # Formatear ecuación con 4 decimales
        sign = "+" if self.intercept >= 0 else ""  # Manejar signo del intercepto
        return f"y = {self.slope:.4f}x {sign}{self.intercept:.4f} (R² = {self.r_squared:.4f})"
    
    def save_calibration(self, filepath: str) -> bool:
        """
        Guarda la calibración en un archivo JSON
        
        Args:
            filepath: Ruta donde guardar el archivo
            
        Returns:
            bool: True si se guardó exitosamente
        """
        if not self.is_calibrated:
            return False
        
        # Preparar datos para JSON
        data = {
            "slope": self.slope,
            "intercept": self.intercept,
            "r_squared": self.r_squared,
            "calibration_data": self.calibration_data,
            "timestamp": "generated_by_sensoracore"
        }
        
        try:
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception:
            return False
    
    def load_calibration(self, filepath: str) -> bool:
        """
        Carga una calibración desde archivo JSON
        
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
            self.slope = data["slope"]
            self.intercept = data["intercept"]
            self.r_squared = data["r_squared"]
            self.calibration_data = data["calibration_data"]
            
            # Recrear el modelo de scikit-learn
            X = np.array(self.calibration_data["raw_values"]).reshape(-1, 1)
            y = np.array(self.calibration_data["reference_values"])
            self.model.fit(X, y)
            self.is_calibrated = True
            
            return True
        except Exception:
            return False
    
    def get_calibration_stats(self) -> dict:
        """
        Retorna estadísticas de la calibración actual
        
        Returns:
            dict: Diccionario con estadísticas de calibración
        """
        if not self.is_calibrated:
            return {"status": "No calibrado"}
        
        return {
            "status": "Calibrado",
            "equation": self.get_calibration_equation(),
            "num_points": len(self.calibration_data["raw_values"]),
            "r_squared": self.r_squared,
            "slope": self.slope,
            "intercept": self.intercept
        }

#| -----------------------------------------------------------|
#| SECCIÓN: FUNCIONES DE MONITOREO - SENSOR DE ÁNGULO SIMPLE  |
#|------------------------------------------------------------|

class AnguloSimpleMonitor:
    def __init__(self):
        """        Inicializa el monitor de sensor de ángulo simple
        Propósito: Configurar variables y objetos necesarios para monitoreo
        Lógica: Prepara sistema de calibración y variables para almacenar datos
        """
        # =====================================================================================
        # SISTEMA DE CALIBRACIÓN
        # =====================================================================================
        
        # --- Instancia de calibración para sensor de ángulo simple ---
        self.angulo_calibration = LinearCalibration()  # Sistema de calibración lineal
        # =====================================================================================
        # VARIABLES PARA DATOS DE SENSOR DE ÁNGULO SIMPLE 
        # =====================================================================================
        
        self.angulos = []                       # Lista para almacenar ángulos medidos
        self.lecturas = []                      # Lista para almacenar lecturas ADC
        self.max_points = 100                   # Límite máximo de puntos en gráfica
        
        # =====================================================================================
        # SISTEMA DE ACTUALIZACIONES 
        # =====================================================================================
 
        self.thread_SIMPLE_ANGLE = None            # Thread para monitoreo de sensor de ángulo
        self.monitoreando_SIMPLE_ANGLE = False              # True cuando el sensor está monitoreando
        self.pending_updates = False            # Flag para indicar si hay actualizaciones pendientes
        self.pending_simpleAngle_data =None
 
        self.timer = QTimer()                # Timer para actualizaciones periódicas de gráfica
        self.timer.timeout.connect(self.on_timer_update_graph)  # Conectar a nuevo método
        self.timer.setInterval(100)           # Intervalo de actualización (100 ms)
    # =====================================================================================
    # MÉTODO: ALTERNAR MONITOREO DEL SENSOR DE ÁNGULO
    # =====================================================================================
    def toggle_angulo_monitoring(self):
        """
        Alterna entre iniciar y detener el monitoreo del sensor de ángulo simple
        
        Propósito: Función de conveniencia para un solo botón de control
        Lógica: Verifica estado actual y ejecuta acción opuesta
        UI: Permite usar un solo botón para iniciar/pausar monitoreo
        Estado: Basado en flag self.monitoreando_SIMPLE_ANGLE
        """
        
        if not self.monitoreando_SIMPLE_ANGLE:               # Si no está monitoreando
            self.start_angulo_monitoring()       # Iniciar monitoreo
        else:                                    # Si ya está monitoreando
            self.stop_angulo_monitoring()        # Detener monitoreo
    # =====================================================================================
    # MÉTODO: INICIAR MONITOREO DEL SENSOR DE ÁNGULO
    # =====================================================================================
    def start_angulo_monitoring(self):
        """
        Inicia el monitoreo en tiempo real del sensor de ángulo simple
        
        Propósito: Comenzar adquisición continua de datos del potenciómetro
        Thread: Crea AnguloSimpleThread para comunicación asíncrona con ESP32
        Datos: Recibe lecturas ADC y convierte a grados (-135° a +135°)
        UI: Actualiza botones y habilita exportación
        Gráfica: Inicia timer de actualización visual
        """
        
        # --- VERIFICAR CONEXIÓN REQUERIDA ---
        if not self.is_connected:                # Verificar conexión TCP activa
            QMessageBox.warning(self, "Sin conexión", "Debes conectar al ESP32 primero")
            return                               # Salir si no hay conexión
        
        try:
            # --- CREAR Y CONFIGURAR THREAD DE MONITOREO ---
            self.thread_SIMPLE_ANGLE = AnguloSimpleThread(self.esp_client.esp32_ip)  # Thread con IP
            self.thread_SIMPLE_ANGLE.data_received.connect(self.update_angulo_data)  # Conectar señal
            
            # --- INICIAR MONITOREO ASÍNCRONO ---
            self.thread_SIMPLE_ANGLE.start()           # Iniciar thread de comunicación
            self.monitoreando_SIMPLE_ANGLE = True            # Marcar estado como monitoreando
            # --- ACTUALIZAR INTERFAZ DE CONTROL ---
            self.start_btn.setText("⏸️ Pausar")   # Cambiar botón a pausar
            self.start_btn.setStyleSheet("QPushButton { background-color: #ffc107; border-color: #ffc107; }")  # Amarillo pausa
            self.export_btn.setEnabled(True)     # Habilitar exportación
            # --- INICIAR ACTUALIZACIÓN GRÁFICA ---
            self.timer.start()  # <--- Iniciar el timer de actualización de gráfica
        except Exception as e:
            # --- MANEJAR ERRORES DE INICIALIZACIÓN ---
            QMessageBox.critical(self, "Error", f"Error al iniciar monitoreo: {str(e)}")
    # =====================================================================================
    # MÉTODO: DETENER MONITOREO DEL SENSOR DE ÁNGULO
    # =====================================================================================
    def stop_angulo_monitoring(self):
        """
        Detiene el monitoreo del sensor de ángulo simple y limpia recursos
        
        Propósito: Parar adquisición de datos y liberar thread
        Thread: Detiene AnguloSimpleThread de forma segura
        UI: Restaura botones a estado inicial
        Recursos: Limpia objetos para evitar memory leaks
        """
        
        # --- DETENER THREAD DE MONITOREO ---
        if self.thread_SIMPLE_ANGLE and self.thread_SIMPLE_ANGLE.isRunning():  # Si existe y está corriendo
            self.thread_SIMPLE_ANGLE.stop()            # Detener thread de forma segura
            self.thread_SIMPLE_ANGLE = None            # Limpiar referencia
            # --- ACTUALIZAR ESTADO Y TIMERS ---
        self.monitoreando_SIMPLE_ANGLE = False               # Marcar como no monitoreando
        self.timer.stop()  # <--- Detener el timer al pausar el monitoreo
        # --- RESTAURAR INTERFAZ DE CONTROL ---
        self.start_btn.setText("▶️ Iniciar Monitoreo")  # Restaurar texto inicial
        self.start_btn.setStyleSheet("QPushButton { background-color: #28a745; border-color: #28a745; }")  # Verde inicial
    # =====================================================================================
    # MÉTODO: ACTUALIZAR DATOS DEL SENSOR DE ÁNGULO
    # =====================================================================================
    def update_angulo_data(self, lectura, angulo):
        """
        Procesa y actualiza los datos recibidos del sensor de ángulo simple
        
        Propósito: Manejar datos en tiempo real del thread de comunicación
        Parámetros: lectura (int) - Valor ADC crudo (0-4095)
                    angulo (float) - Ángulo calculado en grados (-135° a +135°)
        Almacenamiento: Mantiene listas con historial limitado de datos
        UI: Actualiza etiquetas de lectura actual
        Gráfica: Prepara datos para redibujado optimizado
        """
            # --- ALMACENAR DATOS EN HISTORIAL ---
        self.lecturas.append(lectura)            # Agregar lectura ADC a lista
        
        # --- APLICAR CALIBRACIÓN SI ESTÁ DISPONIBLE ---
        if self.angulo_calibration.is_calibrated:  # Si hay calibración activa
            angulo_calibrado = self.angulo_calibration.calibrate_value(lectura)  # Aplicar calibración a lectura cruda
            self.angulos.append(angulo_calibrado)    # Usar ángulo calibrado para gráfica y almacenamiento
        else:
            self.angulos.append(angulo)              # Usar ángulo original si no hay calibración
        
        # --- MANTENER LÍMITE DE PUNTOS EN MEMORIA ---
        if len(self.lecturas) > self.max_points:  # Si excede límite máximo
            self.lecturas.pop(0)                 # Eliminar primer elemento (más antiguo)
            self.angulos.pop(0)                  # Eliminar primer ángulo        # --- ACTUALIZAR ETIQUETA DE LECTURA ACTUAL CON VERIFICACIÓN DEFENSIVA ---
        try:
            if hasattr(self, 'angulo_label') and self.angulo_label is not None:
                if self.angulo_calibration.is_calibrated:  # Si hay calibración activa
                    angulo_calibrado = self.angulo_calibration.calibrate_value(lectura)  # Calcular valor calibrado
                    self.angulo_label.setText(
                        f"Lectura: {lectura} | Ángulo: {angulo}° | Calibrado: {angulo_calibrado:.1f}°"
                    )
                else:
                    self.angulo_label.setText(f"Lectura: {lectura} | Ángulo: {angulo}°")  # Sin calibración
        except RuntimeError:
            # Widget has been deleted, stop monitoring
            if hasattr(self, 'monitoreando_SIMPLE_ANGLE'):
                self.monitoreando_SIMPLE_ANGLE = False
            return
        
        # --- PREPARAR DATOS PARA GRÁFICA ---
        # Actualizar gráfica de forma optimizada
        if hasattr(self, 'line'):                # Verificar que existe línea de datos
            x_data = list(range(len(self.angulos)))  # Índices para eje X
            self.line.set_data(x_data, self.angulos)  # Actualizar datos de línea
            
            # --- AJUSTAR LÍMITES DINÁMICOS DEL EJE X ---
            if len(x_data) > 0:                  # Si hay datos que mostrar
                self.ax.set_xlim(0, max(100, len(x_data)))  # Mínimo 100 puntos visibles
            # --- MARCAR PARA ACTUALIZACIÓN GRÁFICA ---
        self.pending_updates = True              # Flag para redibujado pendiente
        self.pending_simpleAngle_data = (lectura, angulo)  # Datos específicos pendientes
    # =====================================================================================
    # MÉTODO: ABRIR DIÁLOGO DE CALIBRACIÓN
    # =====================================================================================
    def open_calibration_dialog(self):
        """
        Abre el diálogo de calibración para el sensor de ángulo simple
        
        Propósito: Permitir al usuario configurar la calibración lineal del sensor
        Funcionalidad: Crear puntos de calibración, realizar regresión lineal, guardar/cargar calibraciones
        UI: Diálogo modal con tabla de puntos, gráfica en tiempo real y controles
        Calibración: Sistema de regresión lineal que mejora la precisión del sensor
        """        # --- CREAR DIÁLOGO DE CALIBRACIÓN ---
        dialog = CalibrationDialog("Ángulo Simple", self.angulo_calibration, self)  # Pasar nombre del sensor, calibración y ventana padre
        
        # --- MOSTRAR DIÁLOGO Y PROCESAR RESULTADO ---
        if dialog.exec() == QDialog.Accepted:    # Si el usuario presiona OK/Aplicar
            # Actualizar estado de calibración en la interfaz
            self.update_calibration_status()
    # =====================================================================================
    # MÉTODO: ACTUALIZAR ESTADO DE CALIBRACIÓN EN LA INTERFAZ
    # =====================================================================================
    def update_calibration_status(self):
        """
        Actualiza la etiqueta de estado de calibración en la interfaz
        
        Propósito: Mostrar al usuario si hay calibración activa y sus estadísticas
        Estado: Indica si la calibración está aplicada y muestra información relevante
        UI: Actualiza color y texto de la etiqueta según el estado de calibración
        """
        
        if hasattr(self, 'calibration_status_label'):  # Verificar que existe la etiqueta
            if self.angulo_calibration.is_calibrated:   # Si hay calibración activa
                stats = self.angulo_calibration.get_calibration_stats()  # Obtener estadísticas
                if stats and 'r_squared' in stats and 'equation' in stats:
                    # Mostrar información de calibración activa
                    r2_percent = stats['r_squared'] * 100
                    self.calibration_status_label.setText(
                        f"Calibración: ✓ Activa | R² = {r2_percent:.1f}% | {stats['equation']}"
                    )
                    # Cambiar estilo a verde para indicar calibración activa
                    self.calibration_status_label.setStyleSheet("""
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
                    # Calibración sin estadísticas válidas
                    self.calibration_status_label.setText("Calibración: ⚠️ Aplicada (sin estadísticas)")
                    self.calibration_status_label.setStyleSheet("""
                        font-size: 14px;
                        font-weight: bold;
                        color: #856404;
                        padding: 8px;
                        background-color: #fff3cd;
                        border-radius: 4px;
                        border: 1px solid #ffeaa7;
                        margin-top: 5px;
                    """)
            else:
                # Sin calibración activa
                self.calibration_status_label.setText("Calibración: No aplicada")
                self.calibration_status_label.setStyleSheet("""
                    font-size: 14px;
                    font-weight: bold;
                    color: #856404;
                    padding: 8px;
                    background-color: #fff3cd;
                    border-radius: 4px;
                    border: 1px solid #ffeaa7;
                    margin-top: 5px;
                """)
    # =====================================================================================
    # MÉTODO: LIMPIAR GRÁFICA DEL SENSOR DE ÁNGULO
    # =====================================================================================
    def clear_graph_SIMPLE_ANGLE(self):
        """
        Limpia todos los datos y gráfica del sensor de ángulo simple
        
        Propósito: Resetear visualización y datos almacenados
        Datos: Borra historial completo de lecturas y ángulos
        Gráfica: Resetea líneas de datos y límites de ejes
        UI: Restaura etiquetas a estado inicial
        Exportación: Deshabilita botón hasta que haya nuevos datos
        """
        
        # --- LIMPIAR DATOS ALMACENADOS ---
        self.lecturas.clear()                    # Borrar todas las lecturas ADC
        self.angulos.clear()                     # Borrar todos los ángulos
        
        # --- RESETEAR GRÁFICA ---
        if hasattr(self, 'line'):                # Si existe línea de datos
            self.line.set_data([], [])           # Limpiar datos de la línea
            self.ax.set_xlim(0, 100)             # Restaurar límites iniciales
            self.canvas.draw()                   # Redibujar canvas limpio
        
        # --- RESTAURAR ETIQUETAS ---
        self.angulo_label.setText("Lectura: -- | Ángulo: --°")  # Texto inicial
        self.export_btn.setEnabled(False)       # Deshabilitar exportación sin datos
    # =====================================================================================
    # MÉTODO: EXPORTAR DATOS A EXCEL
    # =====================================================================================
    def export_to_excel(self):
            """
            Exporta todos los datos del sensor de ángulo simple a archivo Excel
            
            Propósito: Permitir análisis posterior y respaldo de datos
            Formato: Archivo .xlsx con múltiples columnas y gráfica integrada
            Datos: Lecturas ADC, ángulos calculados, timestamps, numeración
            Gráfica: Incluye gráfico de líneas dentro del archivo Excel
            Validación: Verifica que existan datos antes de exportar
            """
            
            # --- VERIFICAR DATOS DISPONIBLES ---
            if not self.lecturas:                    # Si no hay datos que exportar
                QMessageBox.information(self, "Sin datos", "No hay datos para exportar")
                return                               # Salir sin hacer nada
            
            try:
                # --- GENERAR NOMBRE DE ARCHIVO ÚNICO ---
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")  # Formato: YYYYMMDD_HHMMSS
                filename, _ = QFileDialog.getSaveFileName(
                    self, "Guardar datos",           # Título del diálogo
                    f"SensoraCore_Angulo_{timestamp}.xlsx",  # Nombre sugerido
                    "Excel files (*.xlsx)"           # Filtro de archivos
                )
                
                if filename:                         # Si usuario seleccionó archivo
                    # --- CREAR WORKBOOK Y WORKSHEET ---
                    wb = openpyxl.Workbook()         # Nuevo libro de Excel
                    ws = wb.active                   # Hoja activa
                    ws.title = "Datos Ángulo Simple"  # Título de la hoja
                    
                    # --- CREAR HEADERS DE COLUMNAS ---
                    ws['A1'] = "Muestra"             # Número de muestra
                    ws['B1'] = "Lectura ADC"         # Valor ADC crudo
                    ws['C1'] = "Ángulo (°)"          # Ángulo calculado
                    ws['D1'] = "Timestamp"           # Fecha y hora
                    
                    # --- ESCRIBIR DATOS FILA POR FILA ---
                    for i, (lectura, angulo) in enumerate(zip(self.lecturas, self.angulos)):
                        ws[f'A{i+2}'] = i+1          # Número de muestra (1, 2, 3...)
                        ws[f'B{i+2}'] = lectura      # Lectura ADC
                        ws[f'C{i+2}'] = angulo       # Ángulo en grados
                        ws[f'D{i+2}'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Timestamp
                    
                    # --- CREAR GRÁFICA EN EXCEL ---
                    chart = LineChart()              # Gráfico de líneas
                    chart.title = "Ángulo vs Tiempo"  # Título del gráfico
                    chart.y_axis.title = "Ángulo (°)"  # Etiqueta eje Y
                    chart.x_axis.title = "Muestra"   # Etiqueta eje X
                    
                    # --- CONFIGURAR DATOS DEL GRÁFICO ---
                    data = Reference(ws, min_col=3, min_row=1, max_row=len(self.angulos)+1)  # Columna C
                    categories = Reference(ws, min_col=1, min_row=2, max_row=len(self.angulos)+1)  # Columna A
                    chart.add_data(data, titles_from_data=True)  # Agregar datos
                    chart.set_categories(categories)  # Establecer categorías
                    
                    # --- INSERTAR GRÁFICO EN HOJA ---
                    ws.add_chart(chart, "F2")        # Posición F2 para el gráfico
                    
                    # --- GUARDAR ARCHIVO ---
                    wb.save(filename)                # Guardar en ubicación seleccionada
                    QMessageBox.information(self, "Éxito", f"Datos exportados a {filename}")
                    
            except Exception as e:
                # --- MANEJAR ERRORES DE EXPORTACIÓN ---
                QMessageBox.critical(self, "Error", f"Error al exportar: {str(e)}")
        # =====================================================================================
    # MÉTODO: ACTUALIZACIÓN OPTIMIZADA DE GRÁFICAS
    # =====================================================================================
    def update_graph_display(self):
        """
        Actualiza todas las gráficas de sensores usando timer
        
        Propósito: Centralizar y optimizar la actualización de múltiples gráficas
        Funcionamiento: Usa flags de datos pendientes para evitar actualizaciones innecesarias
        Optimización: Solo redibuja canvas cuando hay datos nuevos pendientes
        Rendimiento: Evita bloqueos de UI con actualizaciones frecuentes
        Sensores: Ángulo simple, brazo robótico, IR, capacitivo, ultrasónico
        """
        
        # --- VERIFICAR SI HAY DATOS PENDIENTES ---
        # Solo actualizar si hay datos pendientes y la aplicación está activa
        if not self.pending_updates:           # Si no hay actualizaciones pendientes
            return                             # Salir sin procesar nada
            
        try:
            # ==================== ACTUALIZAR GRÁFICA ÁNGULO SIMPLE ====================
            # Actualizar gráfica de ángulo simple si hay datos pendientes
            if (self.pending_simpleAngle_data is not None and 
                hasattr(self, 'canvas') and hasattr(self, 'line')):
                self.canvas.draw()             # Redibujar canvas del sensor de ángulo                
                           
            # --- LIMPIAR FLAGS DE ACTUALIZACIÓN ---
            # Limpiar flags de datos pendientes para próxima iteración
            self.pending_updates = False              # Resetear flag principal de actualizaciones
            self.pending_simpleAngle_data = None           # Limpiar datos del ángulo simple
        except Exception as e:
            # --- MANEJO DE ERRORES SILENCIOSO ---
            # Continuar silenciosamente si hay errores de actualización gráfica
            # Esto evita crashes por problemas temporales de rendering
            pass
    
    def on_timer_update_graph(self):
        """
        Método llamado periódicamente por el timer para actualizar la gráfica si hay datos nuevos.
        """
        self.update_graph_display()