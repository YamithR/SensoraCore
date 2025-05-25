# main_window.py para SensoraCore/ui
from PySide6.QtWidgets import (QMainWindow, QLabel, QVBoxLayout, QWidget, 
                               QPushButton, QLineEdit, QMessageBox, QGroupBox,
                               QHBoxLayout, QFileDialog, QScrollArea, QFrame,
                               QListWidget, QListWidgetItem, QSplitter,
                               QGraphicsOpacityEffect)
from PySide6.QtCore import QThread, Signal, Qt, QEasingCurve, QPropertyAnimation, QRect
from PySide6.QtGui import QFont, QPalette, QColor
from network_client import ESP32Client
import socket
import matplotlib
matplotlib.use('QtAgg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import openpyxl
from openpyxl.chart import LineChart, Reference
from datetime import datetime
import os

class AnguloSimpleThread(QThread):
    data_received = Signal(int, int)  # lectura, angulo
    
    def __init__(self, esp32_ip, port=8080):
        super().__init__()
        self.esp32_ip = esp32_ip
        self.port = port
        self.running = False
        self.sock = None
    
    def run(self):
        self.running = True
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.settimeout(3)
            self.sock.connect((self.esp32_ip, self.port))
            self.sock.sendall(b'MODO:ANGULO_SIMPLE')
            self.sock.settimeout(1)
            
            while self.running:
                try:
                    data = self.sock.recv(64)
                    if not data:
                        break
                    msg = data.decode(errors='ignore').strip()
                    for line in msg.split('\n'):
                        if line.startswith('POT:'):
                            try:
                                parts = line.replace('POT:', '').split(',ANG:')
                                lectura = int(parts[0])
                                angulo = int(parts[1])
                                self.data_received.emit(lectura, angulo)
                            except:
                                pass
                except socket.timeout:
                    continue
        except Exception as e:
            pass
        finally:
            if self.sock:
                try:
                    self.sock.sendall(b'STOP')
                except:
                    pass
                self.sock.close()
    
    def stop(self):
        self.running = False
        self.wait()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SensoraCore")
        self.setMinimumSize(1000, 700)
        self.resize(1200, 800)
        
        # Variables de estado
        self.esp_client = None
        self.angulo_thread = None
        self.is_connected = False
        self.is_monitoring = False
        
        # Variables para gráfica
        self.angulos = []
        self.lecturas = []
        self.max_points = 100
        
        # Configurar estilo de la aplicación
        self.setup_styles()
        
        # Crear la interfaz
        self.setup_ui()

    def setup_styles(self):
        """Configura los estilos globales de la aplicación"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f8f9fa;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #dee2e6;
                border-radius: 8px;
                margin-top: 1ex;
                padding-top: 10px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 8px 0 8px;
                color: #495057;
                background-color: white;
            }
            QPushButton {
                border: 2px solid #007bff;
                border-radius: 6px;
                padding: 8px 16px;
                background-color: #007bff;
                color: black;
                font-weight: bold;
                min-height: 20px;
            }
            QPushButton:hover {
                background-color: #0056b3;
                border-color: #0056b3;
            }
            QPushButton:pressed {
                background-color: #004085;
            }
            QPushButton:disabled {
                background-color: #6c757d;
                border-color: #6c757d;
                color: #adb5bd;
            }
            QLineEdit {
                border: 2px solid #ced4da;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 14px;
                background-color: white;
                color:black;
            }
            QLineEdit:focus {
                border-color: #007bff;
                outline: none;
            }
            QListWidget {
                border: 1px solid #dee2e6;
                border-radius: 6px;
                background-color: white;
                alternate-background-color: #f8f9fa;
            }
            QListWidget::item {
                padding: 12px;
                border-bottom: 1px solid #e9ecef;
                color: black;
            }
            QListWidget::item:hover {
                background-color: #7db9f9;
            }
            QListWidget::item:selected {
                background-color: #007bff;
                color: black;
            }
        """)

    def setup_ui(self):
        """Configura la interfaz de usuario"""
        # Widget central principal
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal horizontal
        main_layout = QHBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Crear splitter para división responsive
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)
        
        # Panel izquierdo (conexión y lista de sensores)
        self.left_panel = self.create_left_panel()
        splitter.addWidget(self.left_panel)
        
        # Panel derecho (detalles del sensor)
        self.right_panel = self.create_right_panel()
        splitter.addWidget(self.right_panel)
        
        # Configurar proporciones del splitter
        splitter.setStretchFactor(0, 1)  # Panel izquierdo: 1/3
        splitter.setStretchFactor(1, 2)  # Panel derecho: 2/3
        splitter.setSizes([400, 800])

    def create_left_panel(self):
        """Crea el panel izquierdo con conexión y lista de sensores"""
        panel = QFrame()
        panel.setFrameStyle(QFrame.StyledPanel)
        panel.setStyleSheet("QFrame { background-color: white; border-radius: 8px; }")
        
        layout = QVBoxLayout(panel)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Título de bienvenida
        title_label = QLabel("SensoraCore")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            font-size: 24px; 
            font-weight: bold; 
            color: #007bff;
            margin: 10px 0;
        """)
        layout.addWidget(title_label)
        
        subtitle_label = QLabel("Sistema de Monitoreo de Sensores WiFi")
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setStyleSheet("""
            font-size: 14px; 
            color: #6c757d;
            margin-bottom: 20px;
        """)
        layout.addWidget(subtitle_label)
        
        # Sección de conexión
        connection_group = QGroupBox("Configuración de Conexión")
        connection_layout = QVBoxLayout(connection_group)
        
        # Campo IP
        ip_label = QLabel("IP del ESP32:")
        ip_label.setStyleSheet("font-weight: bold; color: #495057;")
        connection_layout.addWidget(ip_label)
        
        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText("Ejemplo: 192.168.1.100")
        self.ip_input.setText("192.168.20.25")
        connection_layout.addWidget(self.ip_input)
        
        # Botón de conexión
        self.connect_btn = QPushButton("🔌 Conectar ESP32")
        self.connect_btn.clicked.connect(self.test_connection)
        connection_layout.addWidget(self.connect_btn)
        
        # Indicador de estado
        self.status_label = QLabel("⚪ Desconectado")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("""
            padding: 8px;
            border-radius: 4px;
            background-color: #f8d7da;
            color: #721c24;
            font-weight: bold;
        """)
        connection_layout.addWidget(self.status_label)
        
        layout.addWidget(connection_group)
        
        # Lista de sensores (inicialmente oculta)
        self.sensors_group = QGroupBox("Sensores Disponibles")
        self.sensors_group.setVisible(False)  # Oculto hasta conectar
        
        sensors_layout = QVBoxLayout(self.sensors_group)
        
        self.sensors_list = QListWidget()
        self.sensors_list.itemClicked.connect(self.on_sensor_selected)
        
        # Agregar sensores disponibles
        self.add_sensor_items()
        
        sensors_layout.addWidget(self.sensors_list)
        layout.addWidget(self.sensors_group)
        
        # Espaciador
        layout.addStretch()
        
        return panel

    def add_sensor_items(self):
        """Agrega los sensores disponibles a la lista"""
        sensors = [
            ("🎛️ Ángulo Simple", "Potenciómetro como sensor de ángulo", "angulo_simple"),
            ("🦾 Brazo Ángulo", "Sensor de ángulo para brazo robótico", "brazo_angulo"),
            ("📏 Distancia IR", "Sensor de distancia infrarrojo", "distancia_ir"),
            ("🔍 Distancia Capacitivo", "Sensor de distancia capacitivo", "distancia_cap"),
            ("📡 Distancia Ultrasónico", "Sensor HC-SR04", "distancia_ultra"),
            ("💨 Velocidad Óptica", "Sensor óptico de velocidad", "velocidad_optica")
        ]
        
        for icon_name, description, sensor_id in sensors:
            item = QListWidgetItem()
            item.setText(f"{icon_name}\n{description}")
            item.setData(Qt.UserRole, sensor_id)
            
            # Deshabilitar sensores no implementados
            if sensor_id != "angulo_simple":
                item.setFlags(item.flags() & ~Qt.ItemIsEnabled)
                item.setText(f"{icon_name}\n{description}\n(Próximamente)")
                item.setToolTip("Esta función será implementada en futuras versiones")
            
            self.sensors_list.addItem(item)

    def create_right_panel(self):
        """Crea el panel derecho para detalles del sensor"""
        panel = QFrame()
        panel.setFrameStyle(QFrame.StyledPanel)
        panel.setStyleSheet("QFrame { background-color: white; border-radius: 8px; }")
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Mensaje inicial
        self.welcome_widget = QWidget()
        welcome_layout = QVBoxLayout(self.welcome_widget)
        
        welcome_icon = QLabel("🔧")
        welcome_icon.setAlignment(Qt.AlignCenter)
        welcome_icon.setStyleSheet("font-size: 72px; margin: 50px;")
        welcome_layout.addWidget(welcome_icon)
        welcome_text = QLabel("Conecta tu ESP32 y selecciona un sensor\npara comenzar a monitorear datos")
        welcome_text.setAlignment(Qt.AlignCenter)
        welcome_text.setStyleSheet("""
            font-size: 16px;
            color: #6c757d;
            line-height: 1.5;
        """)
        welcome_layout.addWidget(welcome_text)
        
        # Agregar indicación sobre diagrama de conexiones
        diagram_hint = QLabel("📋 Una vez conectado, encontrarás el diagrama\nde conexiones ESP32 en cada sensor")
        diagram_hint.setAlignment(Qt.AlignCenter)
        diagram_hint.setStyleSheet("""
            font-size: 14px;
            color: #495057;
            background-color: #e2f4ff;
            border: 1px solid #b3daff;
            border-radius: 6px;
            padding: 10px;
            margin: 10px 40px;
        """)
        welcome_layout.addWidget(diagram_hint)
        
        welcome_layout.addStretch()
        
        layout.addWidget(self.welcome_widget)
        
        # Contenedor para detalles del sensor (inicialmente oculto)
        self.sensor_details = QScrollArea()
        self.sensor_details.setVisible(False)
        self.sensor_details.setWidgetResizable(True)
        self.sensor_details.setFrameShape(QFrame.NoFrame)
        layout.addWidget(self.sensor_details)
        
        return panel

    def on_sensor_selected(self, item):
        """Maneja la selección de un sensor de la lista"""
        if not self.is_connected:
            QMessageBox.warning(self, "Sin conexión", "Debes conectar al ESP32 primero")
            return
            
        sensor_id = item.data(Qt.UserRole)
        
        if sensor_id == "angulo_simple":
            self.show_angulo_simple_interface()
        else:
            QMessageBox.information(self, "Próximamente", 
                                  "Esta función será implementada en futuras versiones")

    def show_angulo_simple_interface(self):
        """Muestra la interfaz del sensor de ángulo simple"""
        # Ocultar mensaje de bienvenida
        self.welcome_widget.setVisible(False)
        
        # Crear interfaz específica del sensor
        sensor_widget = QWidget()
        layout = QVBoxLayout(sensor_widget)
        layout.setSpacing(20)
        
        # Título del sensor
        title = QLabel("🎛️ Sensor de Ángulo Simple")
        title.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #007bff;
            margin-bottom: 10px;
        """)
        layout.addWidget(title)
          # Descripción
        description = QLabel("Monitorea el ángulo en tiempo real usando un potenciómetro conectado al GPIO 32 del ESP32")
        description.setStyleSheet("""
            font-size: 14px;
            color: #6c757d;
            margin-bottom: 20px;
        """)
        description.setWordWrap(True)
        layout.addWidget(description)
        
        # Diagrama de conexiones ESP32
        diagram_group = QGroupBox("🔌 Diagrama de Conexiones ESP32")
        diagram_layout = QVBoxLayout(diagram_group)
        
        diagram_text = QLabel("""
<pre style="font-family: 'Courier New', monospace; font-size: 12px; line-height: 1.4; color: #495057;">
┌─────────────────────────────────┐
│  ESP32 DevKit V1               │
│                                │
│  3V3  ○ ←── Potenciómetro (+)  │
│  GND  ○ ←── Potenciómetro (-)  │
│  D32  ○ ←── Potenciómetro (S)  │
│                                │
│  LED integrado: GPIO 2         │
└─────────────────────────────────┘

<b>Potenciómetro 10kΩ:</b>
• Pin (+): Alimentación 3.3V
• Pin (-): Tierra (GND)  
• Pin (S): Señal analógica → GPIO 32
</pre>
        """)
        diagram_text.setWordWrap(True)
        diagram_text.setStyleSheet("""
            background-color: #f8f9fa;
            border: 2px solid #dee2e6;
            border-radius: 6px;
            padding: 15px;
            margin: 5px;
        """)
        diagram_layout.addWidget(diagram_text)
        
        # Nota importante
        note_label = QLabel("💡 <b>Nota:</b> Asegúrate de conectar el potenciómetro correctamente antes de iniciar el monitoreo")
        note_label.setStyleSheet("""
            font-size: 13px;
            color: #856404;
            background-color: #fff3cd;
            border: 1px solid #ffeaa7;
            border-radius: 4px;
            padding: 8px;
            margin-top: 5px;
        """)
        note_label.setWordWrap(True)
        diagram_layout.addWidget(note_label)
        
        layout.addWidget(diagram_group)
        
        # Grupo de controles
        controls_group = QGroupBox("Controles")
        controls_layout = QVBoxLayout(controls_group)
        
        # Estado del sensor
        self.angulo_label = QLabel("Lectura: -- | Ángulo: --")
        self.angulo_label.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            color: #495057;
            padding: 10px;
            background-color: #f8f9fa;
            border-radius: 6px;
            border: 2px solid #dee2e6;
        """)
        controls_layout.addWidget(self.angulo_label)
        
        # Botones de control
        buttons_layout = QHBoxLayout()
        
        self.start_btn = QPushButton("▶️ Iniciar Monitoreo")
        self.start_btn.clicked.connect(self.toggle_angulo_monitoring)
        self.start_btn.setStyleSheet("QPushButton { background-color: #28a745; border-color: #28a745; }")
        buttons_layout.addWidget(self.start_btn)
        
        self.stop_btn = QPushButton("⏹️ Detener")
        self.stop_btn.clicked.connect(self.stop_angulo_monitoring)
        self.stop_btn.setEnabled(False)
        self.stop_btn.setStyleSheet("QPushButton { background-color: #dc3545; border-color: #dc3545; }")
        buttons_layout.addWidget(self.stop_btn)
        
        controls_layout.addLayout(buttons_layout)
        
        # Botones de acciones
        actions_layout = QHBoxLayout()
        
        self.clear_btn = QPushButton("🗑️ Limpiar Gráfica")
        self.clear_btn.clicked.connect(self.clear_graph)
        actions_layout.addWidget(self.clear_btn)
        
        self.export_btn = QPushButton("📊 Exportar Excel")
        self.export_btn.clicked.connect(self.export_to_excel)
        self.export_btn.setEnabled(False)
        actions_layout.addWidget(self.export_btn)
        
        controls_layout.addLayout(actions_layout)
        layout.addWidget(controls_group)
        
        # Gráfica mejorada
        graph_group = QGroupBox("Gráfica en Tiempo Real")
        graph_layout = QVBoxLayout(graph_group)
        
        # Configurar matplotlib con colores mejorados
        self.figure = Figure(figsize=(10, 6), dpi=100, facecolor='white')
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)
        
        # Mejorar colores y estilo del gráfico
        self.ax.set_facecolor('#f8f9fa')
        self.ax.grid(True, linestyle='--', alpha=0.7, color='#dee2e6')
        self.ax.set_xlabel('Muestras', fontsize=12, fontweight='bold', color='#495057')
        self.ax.set_ylabel('Ángulo (°)', fontsize=12, fontweight='bold', color='#495057')
        self.ax.set_title('Monitoreo de Ángulo en Tiempo Real', fontsize=14, fontweight='bold', color='#007bff')
        
        # Línea de datos con color destacado
        self.line, = self.ax.plot([], [], 'o-', linewidth=3, markersize=6, 
                                 color='#007bff', markerfacecolor='#0056b3', 
                                 markeredgecolor='white', markeredgewidth=2)
        
        # Configurar límites iniciales
        self.ax.set_xlim(0, 100)
        self.ax.set_ylim(0, 270)
        
        # Mejorar el layout del gráfico
        self.figure.tight_layout(pad=2.0)
        
        graph_layout.addWidget(self.canvas)
        layout.addWidget(graph_group)
        
        # Mostrar en el panel derecho
        self.sensor_details.setWidget(sensor_widget)
        self.sensor_details.setVisible(True)

    def toggle_angulo_monitoring(self):
        """Inicia o detiene el monitoreo de ángulo"""
        if not self.is_monitoring:
            # Iniciar monitoreo
            if not self.esp_client:
                QMessageBox.warning(self, "Error", "Primero conecta al ESP32")
                return
                
            ip = self.ip_input.text().strip()
            self.angulo_thread = AnguloSimpleThread(ip)
            self.angulo_thread.data_received.connect(self.update_angulo_data)
            self.angulo_thread.start()
            
            # Limpiar gráfica al iniciar
            self.angulos.clear()
            self.lecturas.clear()
            self.line.set_data([], [])
            self.canvas.draw()
            
            # Actualizar UI
            self.is_monitoring = True
            self.start_btn.setText("⏸️ Pausar")
            self.start_btn.setStyleSheet("QPushButton { background-color: #ffc107; border-color: #ffc107; color: #212529; }")
            self.stop_btn.setEnabled(True)
            
        else:
            # Pausar monitoreo
            if self.angulo_thread:
                self.angulo_thread.stop()
                self.angulo_thread = None
            
            self.is_monitoring = False
            self.start_btn.setText("▶️ Continuar")
            self.start_btn.setStyleSheet("QPushButton { background-color: #28a745; border-color: #28a745; }")

    def stop_angulo_monitoring(self):
        """Detiene completamente el monitoreo"""
        if self.angulo_thread:
            self.angulo_thread.stop()
            self.angulo_thread = None
        
        self.is_monitoring = False
        self.start_btn.setText("▶️ Iniciar Monitoreo")
        self.start_btn.setStyleSheet("QPushButton { background-color: #28a745; border-color: #28a745; }")
        self.stop_btn.setEnabled(False)
        self.angulo_label.setText("Lectura: -- | Ángulo: --")

    def test_connection(self):
        """Prueba la conexión con el ESP32"""
        ip = self.ip_input.text().strip()
        if not ip:
            QMessageBox.warning(self, "Error", "Debes ingresar la IP del ESP32")
            return
            
        # Cambiar texto del botón mientras conecta
        self.connect_btn.setText("🔄 Conectando...")
        self.connect_btn.setEnabled(False)
        
        self.esp_client = ESP32Client(ip)
        result = self.esp_client.led_on()
        
        if "OK" in result:
            # Conexión exitosa
            self.is_connected = True
            self.update_connection_status(True)
            self.show_sensors_panel()
            QMessageBox.information(self, "Conexión exitosa", 
                                  f"LED integrado encendido!\nESP32 conectado en: {ip}")
        else:
            # Fallo de conexión
            self.is_connected = False
            self.update_connection_status(False)
            QMessageBox.critical(self, "Fallo de conexión", 
                               f"No se pudo encender el LED.\nVerifica la IP y que el ESP32 esté encendido.\nRespuesta: {result}")
        
        # Restaurar botón
        self.connect_btn.setText("🔌 Conectar ESP32")
        self.connect_btn.setEnabled(True)

    def update_connection_status(self, connected):
        """Actualiza el indicador visual de conexión"""
        if connected:
            self.status_label.setText("🟢 Conectado")
            self.status_label.setStyleSheet("""
                padding: 8px;
                border-radius: 4px;
                background-color: #d4edda;
                color: #155724;
                font-weight: bold;
            """)
            self.connect_btn.setText("🔄 Reconectar")
        else:
            self.status_label.setText("🔴 Desconectado")
            self.status_label.setStyleSheet("""
                padding: 8px;
                border-radius: 4px;
                background-color: #f8d7da;
                color: #721c24;
                font-weight: bold;
            """)
            self.connect_btn.setText("🔌 Conectar ESP32")

    def show_sensors_panel(self):
        """Muestra el panel de sensores con animación"""
        self.sensors_group.setVisible(True)
        
        # Crear animación de fade-in
        self.opacity_effect = QGraphicsOpacityEffect()
        self.sensors_group.setGraphicsEffect(self.opacity_effect)
        
        self.animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.animation.setDuration(500)
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)
        self.animation.setEasingCurve(QEasingCurve.InOutCubic)
        self.animation.start()

    def update_angulo_data(self, lectura, angulo):
        """Actualiza los datos del sensor de ángulo en tiempo real"""
        # Actualizar etiqueta con datos en tiempo real
        self.angulo_label.setText(f"Lectura: {lectura} | Ángulo: {angulo}°")
        
        # Agregar datos a las listas
        self.lecturas.append(lectura)
        self.angulos.append(angulo)
        
        # Habilitar botón de exportar cuando hay datos
        if len(self.angulos) > 0:
            self.export_btn.setEnabled(True)
        
        # Mantener solo los últimos puntos para mejor rendimiento
        if len(self.angulos) > self.max_points:
            self.angulos = self.angulos[-self.max_points:]
            self.lecturas = self.lecturas[-self.max_points:]
        
        # Actualizar gráfica con colores mejorados
        x_data = range(len(self.angulos))
        self.line.set_data(x_data, self.angulos)
        
        # Ajustar límites dinámicamente
        if self.angulos:
            self.ax.set_xlim(0, max(self.max_points, len(self.angulos)))
            min_ang = min(self.angulos)
            max_ang = max(self.angulos)
            padding = max(10, (max_ang - min_ang) * 0.1)
            self.ax.set_ylim(min_ang - padding, max_ang + padding)
        
        # Actualizar canvas
        self.canvas.draw()

    def export_to_excel(self):
        """Exporta los datos a un archivo Excel con gráficas mejoradas"""
        if not self.angulos or not self.lecturas:
            QMessageBox.warning(self, "Sin datos", "No hay datos para exportar")
            return
        
        # Solicitar ubicación del archivo
        file_path, _ = QFileDialog.getSaveFileName(
            self, 
            "Guardar datos como Excel", 
            f"SensoraCore_AnguloSimple_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
            "Excel Files (*.xlsx)"
        )
        
        if not file_path:
            return
        
        try:
            # Crear libro de trabajo
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = "Datos Ángulo Simple"
            
            # Encabezados con estilo
            headers = ["Muestra", "Lectura ADC", "Ángulo (°)", "Timestamp"]
            for col, header in enumerate(headers, 1):
                cell = ws.cell(row=1, column=col, value=header)
                cell.font = openpyxl.styles.Font(bold=True)
                cell.fill = openpyxl.styles.PatternFill(start_color="366092", end_color="366092", fill_type="solid")
                cell.font = openpyxl.styles.Font(color="FFFFFF", bold=True)
            
            # Datos
            for i, (lectura, angulo) in enumerate(zip(self.lecturas, self.angulos)):
                ws[f'A{i+2}'] = i + 1
                ws[f'B{i+2}'] = lectura
                ws[f'C{i+2}'] = angulo
                ws[f'D{i+2}'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Crear gráfica en Excel
            chart = LineChart()
            chart.title = "Ángulo vs Tiempo"
            chart.style = 13
            chart.x_axis.title = 'Muestra'
            chart.y_axis.title = 'Ángulo (°)'
            chart.width = 15
            chart.height = 10
            
            # Datos para la gráfica
            data = Reference(ws, min_col=3, min_row=1, max_row=len(self.angulos)+1)
            cats = Reference(ws, min_col=1, min_row=2, max_row=len(self.angulos)+1)
            chart.add_data(data, titles_from_data=True)
            chart.set_categories(cats)
            
            # Añadir gráfica a la hoja
            ws.add_chart(chart, "F2")
            
            # Información adicional con formato
            info_row = 1
            info_data = [
                ("Información del ESP32:", ""),
                (f"IP: {self.ip_input.text()}", ""),
                (f"Total de muestras: {len(self.angulos)}", ""),
                (f"Ángulo mínimo: {min(self.angulos)}°", ""),
                (f"Ángulo máximo: {max(self.angulos)}°", ""),
                (f"Ángulo promedio: {sum(self.angulos)/len(self.angulos):.2f}°", ""),
                (f"Fecha de exportación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", "")
            ]
            
            for i, (label, value) in enumerate(info_data):
                cell = ws.cell(row=info_row + i, column=6, value=label)
                if i == 0:  # Título
                    cell.font = openpyxl.styles.Font(bold=True, size=14)
                else:
                    cell.font = openpyxl.styles.Font(size=11)
            
            # Ajustar ancho de columnas
            for column in ws.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = min(max_length + 2, 50)
                ws.column_dimensions[column_letter].width = adjusted_width
            
            # Guardar archivo
            wb.save(file_path)
            
            QMessageBox.information(
                self, 
                "Exportación exitosa", 
                f"Datos exportados correctamente a:\n{file_path}\n\nTotal de muestras: {len(self.angulos)}"
            )
            
        except Exception as e:
            QMessageBox.critical(self, "Error al exportar", f"Error al guardar el archivo:\n{str(e)}")

    def clear_graph(self):
        """Limpia la gráfica y los datos"""
        # Limpiar datos
        self.angulos.clear()
        self.lecturas.clear()
        
        # Limpiar gráfica
        self.line.set_data([], [])
        self.ax.set_xlim(0, self.max_points)
        self.ax.set_ylim(0, 270)
        self.canvas.draw()
        
        # Actualizar etiqueta
        self.angulo_label.setText("Lectura: -- | Ángulo: --")
        
        # Deshabilitar botón de exportar
        self.export_btn.setEnabled(False)
        
        QMessageBox.information(self, "Gráfica limpia", "Se han borrado todos los datos de la gráfica")

    def closeEvent(self, event):
        """Maneja el cierre de la aplicación"""
        # Asegurar que se cierre el hilo al cerrar la ventana
        if self.angulo_thread:
            self.angulo_thread.stop()
        event.accept()
