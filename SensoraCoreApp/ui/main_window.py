# main_window.py para SensoraCore/ui
from PySide6.QtWidgets import (QMainWindow, QLabel, QVBoxLayout, QWidget, 
                               QPushButton, QLineEdit, QMessageBox, QGroupBox,
                               QHBoxLayout, QFileDialog, QScrollArea, QFrame,
                               QListWidget, QListWidgetItem, QSplitter,
                               QGraphicsOpacityEffect)
from PySide6.QtCore import QThread, Signal, Qt, QEasingCurve, QPropertyAnimation, QRect, QTimer
from PySide6.QtGui import QFont, QPalette, QColor
from network_client import ESP32Client
import socket
import matplotlib
matplotlib.use('Qt5Agg')  # Optimización: usar Qt5Agg backend
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

class BrazoAnguloThread(QThread):
    data_received = Signal(int, int, int, int, int, int, bool)  # lectura1, angulo1, lectura2, angulo2, lectura3, angulo3, sensor_cap
    
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
            self.sock.sendall(b'MODO:BRAZO_ANGULO')
            self.sock.settimeout(1)
            
            while self.running:
                try:
                    data = self.sock.recv(128)
                    if not data:
                        break
                    msg = data.decode(errors='ignore').strip()
                    for line in msg.split('\n'):
                        if line.startswith('POT1:'):
                            try:
                                # Parsear formato: POT1:val,ANG1:ang,POT2:val,ANG2:ang,POT3:val,ANG3:ang,SENSOR:state
                                parts = line.split(',')
                                lectura1 = int(parts[0].split(':')[1])
                                angulo1 = int(parts[1].split(':')[1])
                                lectura2 = int(parts[2].split(':')[1])
                                angulo2 = int(parts[3].split(':')[1])
                                lectura3 = int(parts[4].split(':')[1])
                                angulo3 = int(parts[5].split(':')[1])
                                sensor_estado = parts[6].split(':')[1] == 'True'
                                
                                self.data_received.emit(lectura1, angulo1, lectura2, angulo2, lectura3, angulo3, sensor_estado)
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

class DistanciaIRThread(QThread):
    data_received = Signal(bool)  # Solo estado digital ON/OFF
    
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
            self.sock.sendall(b'MODO:DISTANCIA_IR')
            self.sock.settimeout(1)
            
            while self.running:
                try:
                    data = self.sock.recv(128)
                    if not data:
                        break
                    msg = data.decode(errors='ignore').strip()
                    for line in msg.split('\n'):
                        if line.startswith('IR_DIGITAL:'):
                            try:
                                # Parsear formato: IR_DIGITAL:True/False
                                estado = line.split(':')[1] == 'True'
                                self.data_received.emit(estado)
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

class DistanciaCapThread(QThread):
    data_received = Signal(bool)  # Solo estado digital ON/OFF
    
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
            self.sock.sendall(b'MODO:DISTANCIA_CAP')
            self.sock.settimeout(1)
            
            while self.running:
                try:
                    data = self.sock.recv(128)
                    if not data:
                        break
                    msg = data.decode(errors='ignore').strip()
                    for line in msg.split('\n'):
                        if line.startswith('CAP_DIGITAL:'):
                            try:                                # Parsear formato: CAP_DIGITAL:True/False
                                estado = line.split(':')[1] == 'True'
                                self.data_received.emit(estado)
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

class DistanciaUltrasonicThread(QThread):
    data_received = Signal(int, float, float)  # lectura_adc, voltaje, distancia_cm
    
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
            self.sock.sendall(b'MODO:DISTANCIA_ULTRA')
            self.sock.settimeout(1)
            
            while self.running:
                try:
                    data = self.sock.recv(128)
                    if not data:
                        break
                    msg = data.decode(errors='ignore').strip()
                    for line in msg.split('\n'):
                        if line.startswith('ULTRA_ADC:'):
                            try:
                                # Parsear formato: ULTRA_ADC:val,ULTRA_V:volt,ULTRA_CM:dist
                                parts = line.split(',')
                                lectura_adc = int(parts[0].split(':')[1])
                                voltaje = float(parts[1].split(':')[1])
                                distancia_cm = float(parts[2].split(':')[1])
                                
                                self.data_received.emit(lectura_adc, voltaje, distancia_cm)
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
        self.brazo_thread = None
        self.distancia_ir_thread = None
        self.distancia_cap_thread = None
        self.is_connected = False
        self.is_monitoring = False
          # Variables para gráfica con optimización de memoria
        self.angulos = []
        self.lecturas = []
        self.max_points = 200  # Máximo de puntos en la gráfica
        
        # Timer para optimizar actualizaciones de gráfica
        self.graph_update_timer = QTimer()
        self.graph_update_timer.timeout.connect(self.update_graph_display)
        self.graph_update_timer.setInterval(100)  # Actualizar cada 100ms
          # Variables para brazo con optimización
        self.brazo_angulos = [[], [], []]
        self.brazo_lecturas = [[], [], []]
        self.brazo_capacitive_states = []
        self.brazo_max_points = 50  # Reducido para mejor rendimiento
        self.brazo_is_monitoring = False
          # Variables para sensores de distancia
        self.distancia_ir_lecturas = []
        self.distancia_ir_voltajes = []
        self.distancia_ir_cm = []
        self.distancia_cap_lecturas = []
        self.distancia_cap_voltajes = []
        self.distancia_cap_cm = []
        # Variables para sensor ultrasonico
        self.distancia_ultra_lecturas = []
        self.distancia_ultra_voltajes = []
        self.distancia_ultra_cm = []
        self.distancia_max_points = 100
        self.distancia_ir_is_monitoring = False
        self.distancia_cap_is_monitoring = False
        self.distancia_ultra_is_monitoring = False
          # Sistema de updates optimizado con timer
        self.pending_updates = False
        self.pending_simple_data = None
        self.pending_brazo_data = None
        self.pending_distancia_ir_data = None
        self.pending_distancia_cap_data = None
        self.pending_distancia_ultra_data = None
        
        # Configurar estilo de la aplicación
        self.setup_styles()
          # Crear la interfaz
        self.setup_ui()
    
    def setup_styles(self):
        """Configura los estilos globales de la aplicación"""
        self.setStyleSheet("""
            /* ======================== VENTANA PRINCIPAL ======================== */
            /* Fondo general de toda la aplicación */
            QMainWindow {
                background-color: #f8f9fa;  /* Color de fondo: gris muy claro */
            }
            
            /* ======================== CAJAS DE GRUPO ======================== */
            /* Estilo para todas las cajas de grupo (secciones) de la aplicación */
            QGroupBox {
                font-weight: bold;              /* Texto en negrita */
                border: 2px solid #dee2e6;     /* Borde gris claro de 2px */
                border-radius: 8px;            /* Esquinas redondeadas */
                margin-top: 1ex;               /* Margen superior para el título */
                padding-top: 10px;             /* Espacio interno superior */
                background-color: white;       /* Fondo blanco para las secciones */
            }
            
            /* Estilo específico para los títulos de las cajas de grupo */
            QGroupBox::title {
                subcontrol-origin: margin;     /* Origen del título */
                left: 10px;                    /* Posición izquierda del título */
                padding: 0 8px 0 8px;         /* Espacio alrededor del título */
                color: #495057;               /* Color del texto del título: gris oscuro */
                background-color: white;       /* Fondo blanco para el título */
            }
            
            /* ======================== BOTONES ESTÁNDAR ======================== */
            /* Estilo base para todos los botones de la aplicación */
            QPushButton {
                border: 2px solid #007bff;     /* Borde azul de 2px */
                border-radius: 6px;            /* Esquinas redondeadas */
                padding: 8px 16px;             /* Espacio interno: 8px arriba/abajo, 16px izq/der */
                background-color: #007bff;     /* Fondo azul */
                color: black;                  /* Texto negro */
                font-weight: bold;             /* Texto en negrita */
                min-height: 20px;             /* Altura mínima del botón */
            }
            
            /* Estilo cuando el mouse pasa por encima del botón */
            QPushButton:hover {
                background-color: #0056b3;     /* Fondo azul más oscuro al pasar el mouse */
                border-color: #0056b3;         /* Borde azul más oscuro */
            }
            
            /* Estilo cuando el botón está siendo presionado */
            QPushButton:pressed {
                background-color: #004085;     /* Fondo azul muy oscuro al presionar */
            }
            
            /* Estilo cuando el botón está deshabilitado */
            QPushButton:disabled {
                background-color: #6c757d;     /* Fondo gris cuando está deshabilitado */
                border-color: #6c757d;         /* Borde gris cuando está deshabilitado */
                color: #adb5bd;               /* Texto gris claro cuando está deshabilitado */
            }
            
            /* ======================== CAMPOS DE TEXTO ======================== */
            /* Estilo para todos los campos de entrada de texto */
            QLineEdit {
                border: 2px solid #ced4da;     /* Borde gris claro de 2px */
                border-radius: 6px;            /* Esquinas redondeadas */
                padding: 8px 12px;             /* Espacio interno */
                font-size: 14px;              /* Tamaño de fuente */
                background-color: white;       /* Fondo blanco */
                color: black;                  /* Texto negro */
            }
            
            /* Estilo cuando el campo de texto tiene foco (está activo) */
            QLineEdit:focus {
                border-color: #007bff;         /* Borde azul cuando está activo */
                outline: none;                 /* Sin contorno adicional */
            }
            
            /* ======================== LISTAS DE SENSORES ======================== */
            /* Estilo para la lista de sensores disponibles */
            QListWidget {
                border: 1px solid #dee2e6;     /* Borde gris claro de 1px */
                border-radius: 6px;            /* Esquinas redondeadas */
                background-color: white;       /* Fondo blanco */
                alternate-background-color: #f8f9fa;  /* Color alternativo para filas */
            }
            
            /* Estilo para cada elemento de la lista de sensores */
            QListWidget::item {
                padding: 12px;                 /* Espacio interno de cada elemento */
                border-bottom: 1px solid #e9ecef;  /* Línea separadora entre elementos */
                color: black;                  /* Texto negro */
            }
            
            /* Estilo cuando el mouse pasa por encima de un elemento de la lista */
            QListWidget::item:hover {
                background-color: #7db9f9;     /* Fondo azul claro al pasar el mouse */
            }
            
            /* Estilo cuando un elemento de la lista está seleccionado */
            QListWidget::item:selected {
                background-color: #007bff;     /* Fondo azul cuando está seleccionado */
                color: black;                  /* Texto negro */
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
            item.setData(Qt.UserRole, sensor_id)            # Deshabilitar sensores no implementados
            if sensor_id not in ["angulo_simple", "brazo_angulo", "distancia_ir", "distancia_cap", "distancia_ultra"]:
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
        elif sensor_id == "brazo_angulo":
            self.show_brazo_angulo_interface()
        elif sensor_id == "distancia_ir":
            self.show_distancia_ir_interface()
        elif sensor_id == "distancia_cap":
            self.show_distancia_cap_interface()
        elif sensor_id == "distancia_ultra":
            self.show_distancia_ultra_interface()
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
│  ESP32 DevKit V1                │
│                                 │
│  3V3  ○ ←── Potenciómetro (+)   │
│  GND  ○ ←── Potenciómetro (-)   │
│  D32  ○ ←── Potenciómetro (S)   │
│                                 │
│  LED integrado: GPIO 2          │
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
          # ==================== ETIQUETA DE ESTADO DEL SENSOR ==================== 
        # Muestra lectura ADC y ángulo calculado en tiempo real
        self.angulo_label = QLabel("Lectura: -- | Ángulo: --")
        self.angulo_label.setStyleSheet("""
            font-size: 16px;               /* Tamaño de fuente: 16px para que sea visible */
            font-weight: bold;             /* Texto en negrita para destacar */
            color: #495057;               /* Color gris oscuro para buena legibilidad */
            padding: 10px;                /* Espacio interno: 10px en todos los lados */
            background-color: #f8f9fa;    /* Fondo gris muy claro */
            border-radius: 6px;           /* Esquinas redondeadas para apariencia moderna */
            border: 2px solid #dee2e6;    /* Borde gris claro de 2px */
        """)
        controls_layout.addWidget(self.angulo_label)
        
        # ==================== BOTONES DE CONTROL PRINCIPAL ==================== 
        buttons_layout = QHBoxLayout()
        
        # BOTÓN INICIAR - Color verde para indicar acción positiva
        self.start_btn = QPushButton("▶️ Iniciar Monitoreo")
        self.start_btn.clicked.connect(self.toggle_angulo_monitoring)
        self.start_btn.setStyleSheet("QPushButton { background-color: #28a745; border-color: #28a745; }")
        buttons_layout.addWidget(self.start_btn)
        
        # BOTÓN DETENER - Color rojo para indicar acción de parada
        self.stop_btn = QPushButton("⏹️ Detener")
        self.stop_btn.clicked.connect(self.stop_angulo_monitoring)
        self.stop_btn.setEnabled(False)  # Inicialmente deshabilitado
        self.stop_btn.setStyleSheet("QPushButton { background-color: #dc3545; border-color: #dc3545; }")
        buttons_layout.addWidget(self.stop_btn)
        
        controls_layout.addLayout(buttons_layout)
        
        # ==================== BOTONES DE ACCIONES SECUNDARIAS ==================== 
        actions_layout = QHBoxLayout()
        
        # BOTÓN LIMPIAR - Para borrar datos de la gráfica
        self.clear_btn = QPushButton("🗑️ Limpiar Gráfica")
        self.clear_btn.clicked.connect(self.clear_graph)
        actions_layout.addWidget(self.clear_btn)
        
        # BOTÓN EXPORTAR - Para guardar datos en Excel
        self.export_btn = QPushButton("📊 Exportar Excel")
        self.export_btn.clicked.connect(self.export_to_excel)
        self.export_btn.setEnabled(False)  # Se habilita solo cuando hay datos
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
        
        # Inicializar el canvas con un dibujo inicial
        self.canvas.draw()
        
        graph_layout.addWidget(self.canvas)
        layout.addWidget(graph_group)
        
        # Mostrar en el panel derecho
        self.sensor_details.setWidget(sensor_widget)
        self.sensor_details.setVisible(True)

    def show_brazo_angulo_interface(self):
        """Muestra la interfaz del sensor de brazo con múltiples ángulos"""
        # Ocultar mensaje de bienvenida
        self.welcome_widget.setVisible(False)
        
        # Crear interfaz específica del sensor
        sensor_widget = QWidget()
        layout = QVBoxLayout(sensor_widget)
        layout.setSpacing(20)
        
        # Título del sensor
        title = QLabel("🦾 Sensor de Brazo Ángulo")
        title.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #007bff;
            margin-bottom: 10px;
        """)
        layout.addWidget(title)
        
        # Descripción
        description = QLabel("Monitorea 3 ángulos simultáneamente usando potenciómetros en GPIO 32, 33, 34 y sensor capacitivo en GPIO 25 del ESP32")
        description.setStyleSheet("""
            font-size: 14px;
            color: #6c757d;
            margin-bottom: 20px;
        """)
        description.setWordWrap(True)
        layout.addWidget(description)
        
        # Diagrama de conexiones ESP32 para Brazo Ángulo
        diagram_group = QGroupBox("🔌 Diagrama de Conexiones ESP32 - Brazo Ángulo")
        diagram_layout = QVBoxLayout(diagram_group)
        
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
• Pin (-): Tierra (GND) (todos)
• Pin (S): Señales analógicas:
  - Potenciómetro 1 → GPIO 32 (Base)
  - Potenciómetro 2 → GPIO 33 (Articulación 1)  
  - Potenciómetro 3 → GPIO 34 (Articulación 2)

<b>Sensor Capacitivo:</b>
• Señal digital → GPIO 25 (con pull-up interno)
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
        note_label = QLabel("💡 <b>Nota:</b> Este sensor simula un brazo robótico con 3 articulaciones. El sensor capacitivo simula el agarre.")
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
        
        # ==================== ESTADO DE SENSORES MÚLTIPLES ====================
        # Muestra el estado de los 3 potenciómetros del brazo robótico en tiempo real
        self.brazo_labels = {}
        for i in range(1, 4):
            label = QLabel(f"Potenciómetro {i}: Lectura: -- | Ángulo: --°")
            # ESTILO PARA ETIQUETAS DE ESTADO DE POTENCIÓMETROS
            label.setStyleSheet("""
                font-size: 14px;               /* Tamaño de fuente legible */
                font-weight: bold;              /* Texto en negrita para destacar */
                color: #495057;                 /* Color gris oscuro para el texto */
                padding: 8px;                   /* Espaciado interno de 8px */
                background-color: #f8f9fa;      /* Fondo gris muy claro */
                border-radius: 6px;             /* Esquinas redondeadas de 6px */
                border: 2px solid #dee2e6;      /* Borde gris claro de 2px */
                margin: 2px;                    /* Margen externo pequeño */
            """)
            self.brazo_labels[f'pot{i}'] = label
            controls_layout.addWidget(label)
        
        # ==================== ESTADO DEL SENSOR CAPACITIVO ====================
        # Muestra el estado digital (True/False) del sensor capacitivo del brazo
        self.capacitive_label = QLabel("Sensor Capacitivo: --")
        # ESTILO PARA ETIQUETA DE SENSOR CAPACITIVO
        self.capacitive_label.setStyleSheet("""
            font-size: 14px;               /* Tamaño de fuente consistente con otros sensores */
            font-weight: bold;              /* Texto en negrita */
            color: #495057;                 /* Color gris oscuro */
            padding: 8px;                   /* Espaciado interno */
            background-color: #f8f9fa;      /* Fondo gris claro igual que potenciómetros */
            border-radius: 6px;             /* Esquinas redondeadas */
            border: 2px solid #dee2e6;      /* Borde gris claro */
            margin: 2px;                    /* Margen pequeño */
        """)
        controls_layout.addWidget(self.capacitive_label)
        
        # ==================== BOTONES DE CONTROL PARA BRAZO ROBÓTICO ====================
        buttons_layout = QHBoxLayout()
        
        # BOTÓN INICIAR MONITOREO - Verde para acción positiva
        self.brazo_start_btn = QPushButton("▶️ Iniciar Monitoreo")
        self.brazo_start_btn.clicked.connect(self.toggle_brazo_monitoring)
        # ESTILO: Color verde (#28a745) para indicar acción de inicio
        self.brazo_start_btn.setStyleSheet("QPushButton { background-color: #28a745; border-color: #28a745; }")
        buttons_layout.addWidget(self.brazo_start_btn)
        
        # BOTÓN DETENER - Rojo para acción de parada
        self.brazo_stop_btn = QPushButton("⏹️ Detener")
        self.brazo_stop_btn.clicked.connect(self.stop_brazo_monitoring)
        self.brazo_stop_btn.setEnabled(False)  # Inicialmente deshabilitado
        # ESTILO: Color rojo (#dc3545) para indicar acción de detención
        self.brazo_stop_btn.setStyleSheet("QPushButton { background-color: #dc3545; border-color: #dc3545; }")
        buttons_layout.addWidget(self.brazo_stop_btn)
        
        controls_layout.addLayout(buttons_layout)
        
        # ==================== BOTONES DE ACCIONES SECUNDARIAS ==================== 
        actions_layout = QHBoxLayout()
        
        # BOTÓN LIMPIAR GRÁFICA - Para borrar datos del brazo robótico
        self.brazo_clear_btn = QPushButton("🗑️ Limpiar Gráfica")
        self.brazo_clear_btn.clicked.connect(self.clear_brazo_graph)
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
        self.brazo_figure = Figure(figsize=(12, 8), dpi=100, facecolor='white')
        self.brazo_canvas = FigureCanvas(self.brazo_figure)
        self.brazo_ax = self.brazo_figure.add_subplot(111)
        
        # Mejorar colores y estilo del gráfico
        self.brazo_ax.set_facecolor('#f8f9fa')
        self.brazo_ax.grid(True, linestyle='--', alpha=0.7, color='#dee2e6')
        self.brazo_ax.set_xlabel('Muestras', fontsize=12, fontweight='bold', color='#495057')
        self.brazo_ax.set_ylabel('Ángulo (°)', fontsize=12, fontweight='bold', color='#495057')
        self.brazo_ax.set_title('Monitoreo de Brazo Robótico - 3 Ángulos', fontsize=14, fontweight='bold', color='#007bff')
        
        # Líneas de datos con diferentes colores para cada potenciómetro
        colors = ['#007bff', '#28a745', '#dc3545']  # Azul, Verde, Rojo
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
        self.brazo_is_monitoring = False
          # Mostrar en el panel derecho
        self.sensor_details.setWidget(sensor_widget)
        self.sensor_details.setVisible(True)

    def show_distancia_ir_interface(self):
        """Muestra la interfaz del sensor de distancia infrarrojo DIGITAL"""
        # Ocultar mensaje de bienvenida
        self.welcome_widget.setVisible(False)
        
        # Crear interfaz específica del sensor
        sensor_widget = QWidget()
        layout = QVBoxLayout(sensor_widget)
        layout.setSpacing(20)
          # ==================== TÍTULO DEL SENSOR IR DIGITAL ====================
        title = QLabel("📡 Sensor Infrarrojo Digital (IR)")
        # ESTILO PARA TÍTULO - Gradiente rojo temático del sensor IR
        title.setStyleSheet("""
            font-size: 24px;                   /* Tamaño grande para título principal */
            font-weight: bold;                  /* Texto en negrita */
            color: #2c3e50;                     /* Color base (se sobrescribe) */
            background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0, 
                                      stop: 0 #e74c3c, stop: 1 #c0392b);  /* Gradiente rojo IR */
            color: white;                       /* Texto blanco sobre fondo rojo */
            padding: 15px;                      /* Espaciado interno generoso */
            border-radius: 10px;                /* Esquinas muy redondeadas */
            margin-bottom: 10px;                /* Margen inferior */
        """)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Layout horizontal para contenido principal
        main_layout = QHBoxLayout()
        
        # Panel izquierdo - Diagrama de conexión
        left_panel = QGroupBox("🔌 Diagrama de Conexión")
        left_layout = QVBoxLayout(left_panel)
        
        connection_diagram = QLabel()
        connection_text = """
        <div style='font-family: monospace; font-size: 12px; line-height: 1.5;'>
        <b>ESP32 ↔ Sensor IR Digital</b><br><br>
        
        <table border='1' style='border-collapse: collapse; width: 100%;'>
        <tr style='background-color: #f39c12; color: white;'>
            <th style='padding: 8px;'>ESP32</th>
            <th style='padding: 8px;'>Sensor IR</th>
            <th style='padding: 8px;'>Cable</th>
        </tr>
        <tr>
            <td style='padding: 8px;'>3.3V</td>
            <td style='padding: 8px;'>VCC</td>
            <td style='padding: 8px; color: red;'>🔴 Rojo</td>
        </tr>
        <tr style='background-color: #ecf0f1;'>
            <td style='padding: 8px;'>GND</td>
            <td style='padding: 8px;'>GND</td>
            <td style='padding: 8px;'>⚫ Negro</td>
        </tr>        <tr>
            <td style='padding: 8px;'>GPIO 14</td>
            <td style='padding: 8px;'>OUT</td>
            <td style='padding: 8px; color: orange;'>🟠 Amarillo</td>
        </tr>
        </table><br>
        
        <b>Especificaciones:</b><br>
        • Tipo: Digital (ON/OFF)<br>
        • Voltaje: 3.3V<br>
        • Pull-up interno: Activo<br>
        • Detección: Presencia/Ausencia
        </div>
        """        # ==================== DIAGRAMA DE CONEXIÓN IR ====================
        connection_diagram.setText(connection_text)
        connection_diagram.setWordWrap(True)
        # ESTILO PARA DIAGRAMA - Marco rojo temático del sensor IR
        connection_diagram.setStyleSheet("""
            background-color: #ffffff;         /* Fondo blanco para legibilidad */
            border: 2px solid #e74c3c;         /* Borde rojo tema IR */
            border-radius: 8px;                /* Esquinas redondeadas */
            padding: 15px;                     /* Espaciado interno */
            color: black;                      /* Texto negro sobre fondo blanco */
        """)
        left_layout.addWidget(connection_diagram)
        left_panel.setMaximumWidth(400)
        main_layout.addWidget(left_panel)
        
        # Panel derecho - Estado digital
        right_panel = QGroupBox("🎛️ Estado Digital")
        right_layout = QVBoxLayout(right_panel)
        
        # Estado actual
        status_group = QGroupBox("🔍 Estado Actual")
        status_layout = QVBoxLayout(status_group)
          # ==================== ESTADO DIGITAL DEL SENSOR IR ====================
        # Etiqueta que muestra DETECCIÓN (verde) o SIN DETECCIÓN (rojo)
        self.distancia_ir_status = QLabel("🔴 SIN DETECCIÓN")
        # ESTILO PARA ESTADO DIGITAL - Indicador visual grande y claro
        self.distancia_ir_status.setStyleSheet("""
            font-size: 28px;                   /* Tamaño grande para máxima visibilidad */
            font-weight: bold;                  /* Texto en negrita */
            color: #dc3545;                     /* Color rojo para estado 'sin detección' */
            padding: 20px;                      /* Espaciado interno generoso */
            background-color: #f8f9fa;          /* Fondo gris muy claro */
            border-radius: 12px;                /* Esquinas muy redondeadas */
            border: 3px solid #dc3545;          /* Borde rojo grueso para énfasis */
            text-align: center;                 /* Texto centrado */
        """)
        self.distancia_ir_status.setAlignment(Qt.AlignCenter)
        status_layout.addWidget(self.distancia_ir_status)
        right_layout.addWidget(status_group)
        
        # Controles de monitoreo
        controls_group = QGroupBox("🕹️ Controles")
        controls_layout = QVBoxLayout(controls_group)
        
        buttons_layout = QHBoxLayout()
          # ==================== BOTÓN INICIAR MONITOREO IR ====================
        self.start_distancia_ir_btn = QPushButton("▶️ Iniciar Monitoreo")
        self.start_distancia_ir_btn.clicked.connect(self.toggle_distancia_ir_monitoring)
        # ESTILO: Color rojo temático del sensor IR para consistencia visual
        self.start_distancia_ir_btn.setStyleSheet("QPushButton { background-color: #e74c3c; border-color: #e74c3c; color: white; padding: 10px; }")
        buttons_layout.addWidget(self.start_distancia_ir_btn)
          # BOTÓN DETENER - Rojo estándar para acción de parada
        self.stop_distancia_ir_btn = QPushButton("⏹️ Detener")
        self.stop_distancia_ir_btn.clicked.connect(self.stop_distancia_ir_monitoring)
        self.stop_distancia_ir_btn.setEnabled(False)  # Inicialmente deshabilitado
        # ESTILO: Color rojo para detener, ligeramente diferente al color temático
        self.stop_distancia_ir_btn.setStyleSheet("QPushButton { background-color: #dc3545; border-color: #dc3545; color: white; padding: 10px; }")
        buttons_layout.addWidget(self.stop_distancia_ir_btn)
        
        controls_layout.addLayout(buttons_layout)
        right_layout.addWidget(controls_group)
        
        # Información adicional
        info_group = QGroupBox("ℹ️ Información")
        info_layout = QVBoxLayout(info_group)
          # ==================== INFORMACIÓN DEL SENSOR IR ====================
        info_text = QLabel("""
        <b>Sensor IR Digital:</b><br>
        • Detección simple de presencia/ausencia<br>
        • No mide distancia exacta<br>
        • Ideal para detección de obstáculos<br>
        • Bajo consumo de energía<br>
        • Respuesta rápida ON/OFF
        """)
        info_text.setWordWrap(True)
        # ESTILO PARA INFORMACIÓN - Fondo amarillo suave para destacar info importante
        info_text.setStyleSheet("padding: 10px; background-color: #fff3cd; border-radius: 5px; color: #856404;")
        info_layout.addWidget(info_text)
        right_layout.addWidget(info_group)
        
        main_layout.addWidget(right_panel)
        layout.addLayout(main_layout)
          # Configurar el widget en el área principal
        self.sensor_details.setWidget(sensor_widget)
    
    def show_distancia_cap_interface(self):
        """Muestra la interfaz del sensor de distancia capacitivo DIGITAL"""
        # Ocultar mensaje de bienvenida
        self.welcome_widget.setVisible(False)
        
        # Crear interfaz específica del sensor
        sensor_widget = QWidget()
        layout = QVBoxLayout(sensor_widget)
        layout.setSpacing(20)
          # ==================== TÍTULO DEL SENSOR CAPACITIVO ====================
        title = QLabel("📡 Sensor Capacitivo Digital")
        # ESTILO PARA TÍTULO - Gradiente azul temático del sensor capacitivo
        title.setStyleSheet("""
            font-size: 24px;                   /* Tamaño grande para título principal */
            font-weight: bold;                  /* Texto en negrita */
            color: #2c3e50;                     /* Color base (se sobrescribe) */
            background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0, 
                                      stop: 0 #3498db, stop: 1 #2980b9);  /* Gradiente azul capacitivo */
            color: white;                       /* Texto blanco sobre fondo azul */
            padding: 15px;                      /* Espaciado interno generoso */
            border-radius: 10px;                /* Esquinas muy redondeadas */
            margin-bottom: 10px;                /* Margen inferior */
        """)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Layout horizontal para contenido principal
        main_layout = QHBoxLayout()
        
        # Panel izquierdo - Diagrama de conexión
        left_panel = QGroupBox("🔌 Diagrama de Conexión")
        left_layout = QVBoxLayout(left_panel)
        
        connection_diagram = QLabel()
        connection_text = """
        <div style='font-family: monospace; font-size: 12px; line-height: 1.5;'>
        <b>ESP32 ↔ Sensor Capacitivo Digital</b><br><br>
        
        <table border='1' style='border-collapse: collapse; width: 100%;'>
        <tr style='background-color: #3498db; color: white;'>
            <th style='padding: 8px;'>ESP32</th>
            <th style='padding: 8px;'>Sensor Cap.</th>
            <th style='padding: 8px;'>Cable</th>
        </tr>
        <tr>
            <td style='padding: 8px;'>3.3V</td>
            <td style='padding: 8px;'>VCC</td>
            <td style='padding: 8px; color: red;'>🔴 Rojo</td>
        </tr>
        <tr style='background-color: #ecf0f1;'>
            <td style='padding: 8px;'>GND</td>
            <td style='padding: 8px;'>GND</td>
            <td style='padding: 8px;'>⚫ Negro</td>
        </tr>        <tr>
            <td style='padding: 8px;'>GPIO 35</td>
            <td style='padding: 8px;'>OUT</td>
            <td style='padding: 8px; color: blue;'>🔵 Azul</td>
        </tr>
        </table><br>
        
        <b>Especificaciones:</b><br>
        • Tipo: Digital (ON/OFF)<br>
        • Voltaje: 3.3V<br>
        • Pull-up interno: Activo<br>
        • Detección: Presencia/Ausencia
        </div>
        """        # ==================== DIAGRAMA DE CONEXIÓN CAPACITIVO ====================
        connection_diagram.setText(connection_text)
        connection_diagram.setWordWrap(True)
        # ESTILO PARA DIAGRAMA - Marco azul temático del sensor capacitivo
        connection_diagram.setStyleSheet("""
            background-color: #ffffff;         /* Fondo blanco para legibilidad */
            border: 2px solid #3498db;         /* Borde azul tema capacitivo */
            border-radius: 8px;                /* Esquinas redondeadas */
            padding: 15px;                     /* Espaciado interno */
            color: black;                      /* Texto negro sobre fondo blanco */
        """)
        left_layout.addWidget(connection_diagram)
        left_panel.setMaximumWidth(400)
        main_layout.addWidget(left_panel)
        
        # Panel derecho - Estado digital
        right_panel = QGroupBox("🎛️ Estado Digital")
        right_layout = QVBoxLayout(right_panel)
        
        # Estado actual
        status_group = QGroupBox("🔍 Estado Actual")
        status_layout = QVBoxLayout(status_group)
          # ==================== ESTADO DIGITAL DEL SENSOR CAPACITIVO ====================
        # Etiqueta que muestra DETECCIÓN (verde) o SIN DETECCIÓN (rojo)
        self.distancia_cap_status = QLabel("🔴 SIN DETECCIÓN")
        # ESTILO PARA ESTADO DIGITAL - Indicador visual grande y claro (idéntico al IR)
        self.distancia_cap_status.setStyleSheet("""
            font-size: 28px;                   /* Tamaño grande para máxima visibilidad */
            font-weight: bold;                  /* Texto en negrita */
            color: #dc3545;                     /* Color rojo para estado 'sin detección' */
            padding: 20px;                      /* Espaciado interno generoso */
            background-color: #f8f9fa;          /* Fondo gris muy claro */
            border-radius: 12px;                /* Esquinas muy redondeadas */
            border: 3px solid #dc3545;          /* Borde rojo grueso para énfasis */
            text-align: center;                 /* Texto centrado */
        """)
        self.distancia_cap_status.setAlignment(Qt.AlignCenter)
        status_layout.addWidget(self.distancia_cap_status)
        right_layout.addWidget(status_group)
        
        # Controles de monitoreo
        controls_group = QGroupBox("🕹️ Controles")
        controls_layout = QVBoxLayout(controls_group)
        
        buttons_layout = QHBoxLayout()
          # ==================== BOTÓN INICIAR MONITOREO CAPACITIVO ====================
        self.start_distancia_cap_btn = QPushButton("▶️ Iniciar Monitoreo")
        self.start_distancia_cap_btn.clicked.connect(self.toggle_distancia_cap_monitoring)
        # ESTILO: Color azul temático del sensor capacitivo para consistencia visual
        self.start_distancia_cap_btn.setStyleSheet("QPushButton { background-color: #3498db; border-color: #3498db; color: white; padding: 10px; }")
        buttons_layout.addWidget(self.start_distancia_cap_btn)
          # BOTÓN DETENER - Rojo estándar para acción de parada
        self.stop_distancia_cap_btn = QPushButton("⏹️ Detener")
        self.stop_distancia_cap_btn.clicked.connect(self.stop_distancia_cap_monitoring)
        self.stop_distancia_cap_btn.setEnabled(False)  # Inicialmente deshabilitado
        # ESTILO: Color rojo para detener, consistente con otros sensores
        self.stop_distancia_cap_btn.setStyleSheet("QPushButton { background-color: #dc3545; border-color: #dc3545; color: white; padding: 10px; }")
        buttons_layout.addWidget(self.stop_distancia_cap_btn)
        
        controls_layout.addLayout(buttons_layout)
        right_layout.addWidget(controls_group)
        
        # Información adicional
        info_group = QGroupBox("ℹ️ Información")
        info_layout = QVBoxLayout(info_group)
          # ==================== INFORMACIÓN DEL SENSOR CAPACITIVO ====================
        info_text = QLabel("""
        <b>Sensor Capacitivo Digital:</b><br>
        • Detección simple de presencia/ausencia<br>
        • No mide distancia exacta<br>
        • Ideal para detección de proximidad<br>
        • Sensible a materiales no metálicos<br>
        • Respuesta rápida ON/OFF
        """)
        info_text.setWordWrap(True)
        # ESTILO PARA INFORMACIÓN - Fondo azul suave para destacar info del sensor capacitivo
        info_text.setStyleSheet("padding: 10px; background-color: #d1ecf1; border-radius: 5px; color: black;")
        info_layout.addWidget(info_text)
        right_layout.addWidget(info_group)
        
        main_layout.addWidget(right_panel)
        layout.addLayout(main_layout)
        
        # Configurar el widget en el área principal
        self.sensor_details.setWidget(sensor_widget)

    def show_distancia_ultra_interface(self):
        """Muestra la interfaz del sensor de distancia ultrasónico HC-SR04"""
        # Ocultar mensaje de bienvenida
        self.welcome_widget.setVisible(False)
        
        # Crear interfaz específica del sensor
        sensor_widget = QWidget()
        layout = QVBoxLayout(sensor_widget)
        layout.setSpacing(20)
          # ==================== TÍTULO DEL SENSOR ULTRASÓNICO ====================
        title = QLabel("📏 Sensor Ultrasónico HC-SR04")
        # ESTILO PARA TÍTULO - Gradiente verde azulado temático del sensor ultrasónico
        title.setStyleSheet("""
            font-size: 24px;                   /* Tamaño grande para título principal */
            font-weight: bold;                  /* Texto en negrita */
            color: #2c3e50;                     /* Color base (se sobrescribe) */
            background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0, 
                                      stop: 0 #17a2b8, stop: 1 #138496);  /* Gradiente cyan ultrasónico */
            color: white;                       /* Texto blanco sobre fondo cyan */
            padding: 15px;                      /* Espaciado interno generoso */
            border-radius: 10px;                /* Esquinas muy redondeadas */
            margin-bottom: 10px;                /* Margen inferior */
        """)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Layout horizontal para contenido principal
        main_layout = QHBoxLayout()
        
        # Panel izquierdo - Diagrama de conexión
        left_panel = QGroupBox("🔌 Diagrama de Conexión")
        left_layout = QVBoxLayout(left_panel)
        
        connection_diagram = QLabel()
        connection_text = """
        <div style='font-family: monospace; font-size: 12px; line-height: 1.5;'>
        <b>ESP32 ↔ Sensor HC-SR04</b><br><br>
        
        <table border='1' style='border-collapse: collapse; width: 100%;'>
        <tr style='background-color: #17a2b8; color: white;'>
            <th style='padding: 8px;'>ESP32</th>
            <th style='padding: 8px;'>HC-SR04</th>
            <th style='padding: 8px;'>Cable</th>
        </tr>
        <tr>
            <td style='padding: 8px;'>5V</td>
            <td style='padding: 8px;'>VCC</td>
            <td style='padding: 8px; color: red;'>🔴 Rojo</td>
        </tr>
        <tr style='background-color: #ecf0f1;'>
            <td style='padding: 8px;'>GND</td>
            <td style='padding: 8px;'>GND</td>
            <td style='padding: 8px;'>⚫ Negro</td>
        </tr>        <tr>
            <td style='padding: 8px;'>GPIO 26</td>
            <td style='padding: 8px;'>TRIG</td>
            <td style='padding: 8px; color: green;'>🟢 Verde</td>
        </tr>
        <tr style='background-color: #ecf0f1;'>
            <td style='padding: 8px;'>GPIO 27</td>
            <td style='padding: 8px;'>ECHO</td>
            <td style='padding: 8px; color: blue;'>🔵 Azul</td>
        </tr>
        </table><br>
        
        <b>Especificaciones:</b><br>
        • Rango: 2-400 cm<br>
        • Voltaje: 5V<br>
        • Tipo: Analógico<br>
        • Precisión: ±3mm<br>
        • Frecuencia: 40kHz
        </div>
        """        # ==================== DIAGRAMA DE CONEXIÓN ULTRASÓNICO ====================
        connection_diagram.setText(connection_text)
        connection_diagram.setWordWrap(True)
        # ESTILO PARA DIAGRAMA - Marco cyan temático del sensor ultrasónico
        connection_diagram.setStyleSheet("""
            background-color: #ffffff;         /* Fondo blanco para legibilidad */
            border: 2px solid #17a2b8;         /* Borde cyan tema ultrasónico */
            border-radius: 8px;                /* Esquinas redondeadas */
            padding: 15px;                     /* Espaciado interno */
            color: black;
        """)
        left_layout.addWidget(connection_diagram)
        left_panel.setMaximumWidth(400)
        main_layout.addWidget(left_panel)
        
        # Panel derecho - Controles y lecturas
        right_panel = QGroupBox("🎛️ Control y Monitoreo")
        right_layout = QVBoxLayout(right_panel)
        
        # Lecturas actuales
        readings_group = QGroupBox("📊 Lecturas Actuales")
        readings_layout = QVBoxLayout(readings_group)        # ==================== LECTURAS DEL SENSOR ULTRASÓNICO ====================
        # Etiqueta que muestra distancia, velocidad del sonido y ecuación de cálculo
        self.distancia_ultra_label = QLabel("Distancia: -- cm")
        # ESTILO PARA LECTURAS - Color cyan temático con diseño destacado
        self.distancia_ultra_label.setStyleSheet("""
            font-size: 18px;                   /* Tamaño de fuente grande para lecturas */
            font-weight: bold;                  /* Texto en negrita */
            color: #17a2b8;                     /* Color cyan tema ultrasónico */
            padding: 15px;                      /* Espaciado interno generoso */
            background-color: #f8f9fa;          /* Fondo gris muy claro */
            border-radius: 8px;                 /* Esquinas redondeadas */
            border: 2px solid #17a2b8;          /* Borde cyan para consistencia */
        """)
        readings_layout.addWidget(self.distancia_ultra_label)
        
        # Información sobre velocidad del sonido y cálculo
        self.sound_speed_label = QLabel("Velocidad del sonido: 343 m/s (20°C)")
        self.sound_speed_label.setStyleSheet("""
            font-size: 14px;
            color: #495057;
            padding: 10px;
            background-color: #e9ecef;
            border-radius: 6px;
            margin: 5px 0px;
        """)
        readings_layout.addWidget(self.sound_speed_label)
        
        # Ecuación de cálculo
        self.equation_label = QLabel("Cálculo: Distancia = (Tiempo × 343 m/s) / 2")
        self.equation_label.setStyleSheet("""
            font-size: 13px;
            color: #6c757d;
            padding: 8px;
            background-color: #f8f9fa;
            border-radius: 4px;
            border-left: 4px solid #17a2b8;
            margin: 5px 0px;
        """)
        readings_layout.addWidget(self.equation_label)
        right_layout.addWidget(readings_group)
        
        # Controles de monitoreo
        controls_group = QGroupBox("🕹️ Controles")
        controls_layout = QVBoxLayout(controls_group)
        
        buttons_layout = QHBoxLayout()
          # ==================== BOTÓN INICIAR MONITOREO ULTRASÓNICO ====================
        self.start_distancia_ultra_btn = QPushButton("▶️ Iniciar Monitoreo")
        self.start_distancia_ultra_btn.clicked.connect(self.toggle_distancia_ultra_monitoring)
        # ESTILO: Color cyan temático del sensor ultrasónico para consistencia visual
        self.start_distancia_ultra_btn.setStyleSheet("QPushButton { background-color: #17a2b8; border-color: #17a2b8; color: white; padding: 10px; }")
        buttons_layout.addWidget(self.start_distancia_ultra_btn)
        
        # BOTÓN DETENER - Rojo estándar para acción de parada
        self.stop_distancia_ultra_btn = QPushButton("⏹️ Detener")
        self.stop_distancia_ultra_btn.clicked.connect(self.stop_distancia_ultra_monitoring)
        self.stop_distancia_ultra_btn.setEnabled(False)  # Inicialmente deshabilitado
        # ESTILO: Color rojo para detener, consistente con otros sensores
        self.stop_distancia_ultra_btn.setStyleSheet("QPushButton { background-color: #dc3545; border-color: #dc3545; color: white; padding: 10px; }")
        buttons_layout.addWidget(self.stop_distancia_ultra_btn)
        
        controls_layout.addLayout(buttons_layout)
        
        # Acciones adicionales
        actions_layout = QHBoxLayout()
          # ==================== BOTONES DE ACCIONES SECUNDARIAS ULTRASÓNICO ====================
        # BOTÓN LIMPIAR GRÁFICA - Para borrar datos del sensor ultrasónico
        self.clear_distancia_ultra_btn = QPushButton("🗑️ Limpiar Gráfica")
        self.clear_distancia_ultra_btn.clicked.connect(self.clear_distancia_ultra_graph)
        actions_layout.addWidget(self.clear_distancia_ultra_btn)
        
        # BOTÓN EXPORTAR - Para guardar datos en Excel (ADC, voltaje, distancia)
        self.export_distancia_ultra_btn = QPushButton("📊 Exportar Excel")
        self.export_distancia_ultra_btn.clicked.connect(self.export_distancia_ultra_to_excel)
        self.export_distancia_ultra_btn.setEnabled(False)  # Se habilita solo cuando hay datos
        actions_layout.addWidget(self.export_distancia_ultra_btn)
        
        controls_layout.addLayout(actions_layout)
        right_layout.addWidget(controls_group)
        
        # Información adicional
        info_group = QGroupBox("ℹ️ Información")
        info_layout = QVBoxLayout(info_group)
          # ==================== INFORMACIÓN DEL SENSOR ULTRASÓNICO ====================
        info_text = QLabel("""
        <b>Sensor HC-SR04:</b><br>
        • Alta precisión en medición de distancia<br>
        • Ideal para navegación de robots<br>
        • No afectado por color o transparencia<br>
        • Funciona con ondas ultrasónicas<br>
        • Excelente para distancias largas
        """)
        info_text.setWordWrap(True)
        # ESTILO PARA INFORMACIÓN - Fondo cyan suave para destacar info del sensor ultrasónico
        info_text.setStyleSheet("padding: 10px; background-color: #d1ecf1; border-radius: 5px; color: black;")
        info_layout.addWidget(info_text)
        right_layout.addWidget(info_group)
        
        main_layout.addWidget(right_panel)
        layout.addLayout(main_layout)
        
        # Gráfica
        graph_group = QGroupBox("📈 Gráfica en Tiempo Real")
        graph_layout = QVBoxLayout(graph_group)
          # ==================== CONFIGURACIÓN GRÁFICA ULTRASÓNICA ====================
        # Configurar matplotlib para sensor ultrasónico con tema cyan
        self.figure_ultra = Figure(figsize=(12, 6), dpi=100, facecolor='white')
        self.canvas_ultra = FigureCanvas(self.figure_ultra)
        self.ax_ultra = self.figure_ultra.add_subplot(111)
        
        # CONFIGURACIÓN DE ESTILO PARA GRÁFICA ULTRASÓNICA
        self.ax_ultra.set_title('Sensor Ultrasónico HC-SR04 - Tiempo Real', fontsize=14, fontweight='bold', color='#17a2b8')  # Título cyan
        self.ax_ultra.set_xlabel('Tiempo (s)', fontsize=12)        # Etiqueta eje X
        self.ax_ultra.set_ylabel('Distancia (cm)', fontsize=12)    # Etiqueta eje Y
        self.ax_ultra.grid(True, alpha=0.3)                        # Rejilla sutil
        self.ax_ultra.set_facecolor('#f8f9fa')                     # Fondo gris claro
        
        # LÍNEA DE DATOS - Color cyan para consistencia temática
        self.line_ultra, = self.ax_ultra.plot([], [], 'c-', linewidth=2, label='Distancia Ultrasónica')
        self.ax_ultra.legend()
          # CONFIGURAR LÍMITES INICIALES
        self.ax_ultra.set_xlim(0, 60)     # 60 segundos de visualización
        self.ax_ultra.set_ylim(0, 400)    # Rango 0-400 cm (rango del HC-SR04)
        
        self.figure_ultra.tight_layout()
        
        # Inicializar el canvas con un dibujo inicial
        self.canvas_ultra.draw()
        
        graph_layout.addWidget(self.canvas_ultra)
        layout.addWidget(graph_group)
        
        # Configurar el widget en el área principal
        self.sensor_details.setWidget(sensor_widget)

    def update_graph_display(self):
        """Actualiza las gráficas de forma optimizada usando el timer"""
        # Solo actualizar si hay datos pendientes y la aplicación está activa
        if not self.pending_updates:
            return
            
        try:
            # Actualizar gráfica de ángulo simple si hay datos pendientes
            if (self.pending_simple_data is not None and 
                hasattr(self, 'canvas') and hasattr(self, 'line')):
                self.canvas.draw()
                
            # Actualizar gráfica de brazo si hay datos pendientes  
            if (self.pending_brazo_data is not None and 
                hasattr(self, 'brazo_canvas') and hasattr(self, 'brazo_lines')):
                self.brazo_canvas.draw()
                
            # Actualizar gráfica IR si hay datos pendientes
            if (self.pending_distancia_ir_data is not None and 
                hasattr(self, 'canvas_ir') and hasattr(self, 'line_ir')):
                self.canvas_ir.draw()
                
            # Actualizar gráfica capacitiva si hay datos pendientes
            if (self.pending_distancia_cap_data is not None and 
                hasattr(self, 'canvas_cap') and hasattr(self, 'line_cap')):
                self.canvas_cap.draw()
                
            # Actualizar gráfica ultrasónica si hay datos pendientes
            if (self.pending_distancia_ultra_data is not None and 
                hasattr(self, 'canvas_ultra') and hasattr(self, 'line_ultra')):
                self.canvas_ultra.draw()
                
            # Limpiar flags de datos pendientes
            self.pending_updates = False
            self.pending_simple_data = None
            self.pending_brazo_data = None
            self.pending_distancia_ir_data = None  
            self.pending_distancia_cap_data = None
            self.pending_distancia_ultra_data = None
            
        except Exception as e:
            # Continuar silenciosamente si hay errores de actualización
            pass    # ============================================================================
    # FUNCIONES DE CONEXIÓN Y MONITOREO
    # ============================================================================
    def test_connection(self):
        """Prueba la conexión con el ESP32"""
        esp32_ip = self.ip_input.text().strip()
        
        if not esp32_ip:
            QMessageBox.warning(self, "IP requerida", "Ingresa la IP del ESP32")
            return
        
        # Deshabilitar botón y mostrar estado de conexión
        self.connect_btn.setEnabled(False)
        self.status_label.setText("🔄 Conectando...")
        self.status_label.setStyleSheet("""
            padding: 8px;
            border-radius: 4px;
            background-color: #cce5ff;
            color: #004085;
            font-weight: bold;
        """)
        self.repaint()  # Forzar actualización de la interfaz
        
        # Probar conexión directamente
        try:
            client = ESP32Client(esp32_ip)
            response = client.led_on()  # Probar con comando LED_ON
            
            if "LED_ON_OK" in response:
                # Conexión exitosa
                self.on_connected(esp32_ip)
            else:
                # Respuesta inesperada
                self.on_disconnected()
                
        except Exception as e:
            # Error de conexión
            self.on_disconnected()
    
    def on_connected(self, esp32_ip):
        """Callback cuando la conexión es exitosa"""
        self.is_connected = True
        self.esp_client = ESP32Client(esp32_ip)
        
        # Actualizar interfaz
        self.connect_btn.setText("🔌 Conectado")
        self.connect_btn.setEnabled(False)
        self.status_label.setText("✅ Conectado al ESP32")
        self.status_label.setStyleSheet("""
            padding: 8px;
            border-radius: 4px;
            background-color: #d4edda;
            color: #155724;
            font-weight: bold;
        """)
        
        # Mostrar lista de sensores con animación
        self.show_sensors_with_animation()
    
    def on_disconnected(self):
        """Callback cuando la conexión falla"""
        self.is_connected = False
        self.esp_client = None
        
        # Actualizar interfaz
        self.connect_btn.setText("🔌 Conectar al ESP32")
        self.connect_btn.setEnabled(True)
        self.status_label.setText("❌ Error de conexión")
        self.status_label.setStyleSheet("""
            padding: 8px;
            border-radius: 4px;
            background-color: #f8d7da;
            color: #721c24;
            font-weight: bold;
        """)
        
        # Ocultar lista de sensores
        self.sensors_group.setVisible(False)
    
    def show_sensors_with_animation(self):
        """Muestra la lista de sensores con efecto de desvanecimiento"""
        self.sensors_group.setVisible(True)
        
        # Crear efecto de opacidad
        self.fade_effect = QGraphicsOpacityEffect()
        self.sensors_group.setGraphicsEffect(self.fade_effect)
        
        # Crear animación
        self.animation = QPropertyAnimation(self.fade_effect, b"opacity")
        self.animation.setDuration(800)
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)
        
        # Iniciar animación
        self.animation.start()

    # ============================================================================
    # FUNCIONES DE MONITOREO - ÁNGULO SIMPLE
    # ============================================================================
    
    def toggle_angulo_monitoring(self):
        """Inicia o detiene el monitoreo del sensor de ángulo simple"""
        if not self.is_monitoring:
            self.start_angulo_monitoring()
        else:
            self.stop_angulo_monitoring()
    
    def start_angulo_monitoring(self):
        """Inicia el monitoreo del sensor de ángulo simple"""
        if not self.is_connected:
            QMessageBox.warning(self, "Sin conexión", "Debes conectar al ESP32 primero")
            return
        
        try:
            # Crear y configurar thread
            self.angulo_thread = AnguloSimpleThread(self.esp_client.esp32_ip)
            self.angulo_thread.data_received.connect(self.update_angulo_data)
            
            # Iniciar monitoreo
            self.angulo_thread.start()
            self.is_monitoring = True
            
            # Actualizar interfaz
            self.start_btn.setText("⏸️ Pausar")
            self.start_btn.setStyleSheet("QPushButton { background-color: #ffc107; border-color: #ffc107; }")
            self.stop_btn.setEnabled(True)
            self.export_btn.setEnabled(True)
            
            # Iniciar timer de actualización gráfica
            self.graph_update_timer.start()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al iniciar monitoreo: {str(e)}")
    
    def stop_angulo_monitoring(self):
        """Detiene el monitoreo del sensor de ángulo simple"""
        if self.angulo_thread and self.angulo_thread.isRunning():
            self.angulo_thread.stop()
            self.angulo_thread = None
        
        self.is_monitoring = False
        self.graph_update_timer.stop()
        
        # Actualizar interfaz
        self.start_btn.setText("▶️ Iniciar Monitoreo")
        self.start_btn.setStyleSheet("QPushButton { background-color: #28a745; border-color: #28a745; }")
        self.stop_btn.setEnabled(False)
    
    def update_angulo_data(self, lectura, angulo):
        """Actualiza los datos del sensor de ángulo simple"""
        # Agregar datos a las listas
        self.lecturas.append(lectura)
        self.angulos.append(angulo)
        
        # Mantener máximo de puntos
        if len(self.lecturas) > self.max_points:
            self.lecturas.pop(0)
            self.angulos.pop(0)
        
        # Actualizar etiqueta
        self.angulo_label.setText(f"Lectura: {lectura} | Ángulo: {angulo}°")
        
        # Actualizar gráfica de forma optimizada
        if hasattr(self, 'line'):
            x_data = list(range(len(self.angulos)))
            self.line.set_data(x_data, self.angulos)
            
            # Ajustar límites del eje X
            if len(x_data) > 0:
                self.ax.set_xlim(0, max(100, len(x_data)))
        
        # Marcar para actualización
        self.pending_updates = True
        self.pending_simple_data = (lectura, angulo)
    
    def clear_graph(self):
        """Limpia la gráfica del sensor de ángulo simple"""
        self.lecturas.clear()
        self.angulos.clear()
        
        if hasattr(self, 'line'):
            self.line.set_data([], [])
            self.ax.set_xlim(0, 100)
            self.canvas.draw()
        
        self.angulo_label.setText("Lectura: -- | Ángulo: --°")
        self.export_btn.setEnabled(False)
    
    def export_to_excel(self):
        """Exporta los datos del sensor de ángulo simple a Excel"""
        if not self.lecturas:
            QMessageBox.information(self, "Sin datos", "No hay datos para exportar")
            return
        
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename, _ = QFileDialog.getSaveFileName(
                self, "Guardar datos",
                f"SensoraCore_Angulo_{timestamp}.xlsx",
                "Excel files (*.xlsx)"
            )
            
            if filename:
                # Crear workbook
                wb = openpyxl.Workbook()
                ws = wb.active
                ws.title = "Datos Ángulo Simple"
                
                # Headers
                ws['A1'] = "Muestra"
                ws['B1'] = "Lectura ADC"
                ws['C1'] = "Ángulo (°)"
                ws['D1'] = "Timestamp"
                
                # Datos
                for i, (lectura, angulo) in enumerate(zip(self.lecturas, self.angulos)):
                    ws[f'A{i+2}'] = i+1
                    ws[f'B{i+2}'] = lectura
                    ws[f'C{i+2}'] = angulo
                    ws[f'D{i+2}'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # Crear gráfica
                chart = LineChart()
                chart.title = "Ángulo vs Tiempo"
                chart.y_axis.title = "Ángulo (°)"
                chart.x_axis.title = "Muestra"
                
                data = Reference(ws, min_col=3, min_row=1, max_row=len(self.angulos)+1)
                categories = Reference(ws, min_col=1, min_row=2, max_row=len(self.angulos)+1)
                chart.add_data(data, titles_from_data=True)
                chart.set_categories(categories)
                
                ws.add_chart(chart, "F2")
                
                # Guardar
                wb.save(filename)
                QMessageBox.information(self, "Éxito", f"Datos exportados a {filename}")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al exportar: {str(e)}")

    # ============================================================================
    # FUNCIONES DE MONITOREO - BRAZO ÁNGULO
    # ============================================================================
    
    def toggle_brazo_monitoring(self):
        """Inicia o detiene el monitoreo del sensor de brazo"""
        if not self.brazo_is_monitoring:
            self.start_brazo_monitoring()
        else:
            self.stop_brazo_monitoring()
    
    def start_brazo_monitoring(self):
        """Inicia el monitoreo del sensor de brazo"""
        if not self.is_connected:
            QMessageBox.warning(self, "Sin conexión", "Debes conectar al ESP32 primero")
            return
        
        try:
            # Crear y configurar thread
            self.brazo_thread = BrazoAnguloThread(self.esp_client.esp32_ip)
            self.brazo_thread.data_received.connect(self.update_brazo_data)
            
            # Iniciar monitoreo
            self.brazo_thread.start()
            self.brazo_is_monitoring = True
            
            # Actualizar interfaz
            self.brazo_start_btn.setText("⏸️ Pausar")
            self.brazo_start_btn.setStyleSheet("QPushButton { background-color: #ffc107; border-color: #ffc107; }")
            self.brazo_stop_btn.setEnabled(True)
            self.brazo_export_btn.setEnabled(True)
            
            # Iniciar timer de actualización gráfica
            self.graph_update_timer.start()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al iniciar monitoreo: {str(e)}")
    
    def stop_brazo_monitoring(self):
        """Detiene el monitoreo del sensor de brazo"""
        if self.brazo_thread and self.brazo_thread.isRunning():
            self.brazo_thread.stop()
            self.brazo_thread = None
        
        self.brazo_is_monitoring = False
        self.graph_update_timer.stop()
        
        # Actualizar interfaz
        self.brazo_start_btn.setText("▶️ Iniciar Monitoreo")
        self.brazo_start_btn.setStyleSheet("QPushButton { background-color: #28a745; border-color: #28a745; }")
        self.brazo_stop_btn.setEnabled(False)
    
    def update_brazo_data(self, lectura1, angulo1, lectura2, angulo2, lectura3, angulo3, sensor_estado):
        """Actualiza los datos del sensor de brazo"""
        # Agregar datos a las listas
        for i, (lectura, angulo) in enumerate([(lectura1, angulo1), (lectura2, angulo2), (lectura3, angulo3)]):
            self.brazo_lecturas[i].append(lectura)
            self.brazo_angulos[i].append(angulo)
            
            # Mantener máximo de puntos
            if len(self.brazo_lecturas[i]) > self.brazo_max_points:
                self.brazo_lecturas[i].pop(0)
                self.brazo_angulos[i].pop(0)
        
        # Agregar estado del sensor capacitivo
        self.brazo_capacitive_states.append(sensor_estado)
        if len(self.brazo_capacitive_states) > self.brazo_max_points:
            self.brazo_capacitive_states.pop(0)
        
        # Actualizar etiquetas
        self.brazo_labels['pot1'].setText(f"Potenciómetro 1: Lectura: {lectura1} | Ángulo: {angulo1}°")
        self.brazo_labels['pot2'].setText(f"Potenciómetro 2: Lectura: {lectura2} | Ángulo: {angulo2}°")
        self.brazo_labels['pot3'].setText(f"Potenciómetro 3: Lectura: {lectura3} | Ángulo: {angulo3}°")
        self.capacitive_label.setText(f"Sensor Capacitivo: {'Activado' if sensor_estado else 'Desactivado'}")
        
        # Actualizar gráfica de forma optimizada
        if hasattr(self, 'brazo_lines'):
            for i, line in enumerate(self.brazo_lines):
                x_data = list(range(len(self.brazo_angulos[i])))
                line.set_data(x_data, self.brazo_angulos[i])
            
            # Ajustar límites del eje X
            if len(self.brazo_angulos[0]) > 0:
                max_len = max(len(angles) for angles in self.brazo_angulos)
                self.brazo_ax.set_xlim(0, max(100, max_len))
        
        # Marcar para actualización
        self.pending_updates = True
        self.pending_brazo_data = (lectura1, angulo1, lectura2, angulo2, lectura3, angulo3, sensor_estado)
    
    def clear_brazo_graph(self):
        """Limpia la gráfica del sensor de brazo"""
        for i in range(3):
            self.brazo_lecturas[i].clear()
            self.brazo_angulos[i].clear()
        self.brazo_capacitive_states.clear()
        
        if hasattr(self, 'brazo_lines'):
            for line in self.brazo_lines:
                line.set_data([], [])
            self.brazo_ax.set_xlim(0, 100)
            self.brazo_canvas.draw()
        
        # Resetear etiquetas
        for i in range(1, 4):
            self.brazo_labels[f'pot{i}'].setText(f"Potenciómetro {i}: Lectura: -- | Ángulo: --°")
        self.capacitive_label.setText("Sensor Capacitivo: --")
        self.brazo_export_btn.setEnabled(False)
    
    def export_brazo_to_excel(self):
        """Exporta los datos del sensor de brazo a Excel"""
        if not any(self.brazo_lecturas):
            QMessageBox.information(self, "Sin datos", "No hay datos para exportar")
            return
        
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename, _ = QFileDialog.getSaveFileName(
                self, "Guardar datos",
                f"SensoraCore_Brazo_{timestamp}.xlsx",
                "Excel files (*.xlsx)"
            )
            
            if filename:
                # Crear workbook
                wb = openpyxl.Workbook()
                ws = wb.active
                ws.title = "Datos Brazo Ángulo"
                
                # Headers
                headers = ["Muestra", "Lectura1", "Ángulo1", "Lectura2", "Ángulo2", 
                          "Lectura3", "Ángulo3", "Sensor_Cap", "Timestamp"]
                for i, header in enumerate(headers):
                    ws.cell(row=1, column=i+1, value=header)
                
                # Datos
                max_len = max(len(angles) for angles in self.brazo_angulos if angles)
                for i in range(max_len):
                    row = i + 2
                    ws.cell(row=row, column=1, value=i+1)
                    
                    for j in range(3):
                        if i < len(self.brazo_lecturas[j]):
                            ws.cell(row=row, column=j*2+2, value=self.brazo_lecturas[j][i])
                            ws.cell(row=row, column=j*2+3, value=self.brazo_angulos[j][i])
                    
                    if i < len(self.brazo_capacitive_states):
                        ws.cell(row=row, column=8, value=self.brazo_capacitive_states[i])
                    
                    ws.cell(row=row, column=9, value=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                
                # Crear gráficas para cada potenciómetro
                colors = ["0000FF", "00FF00", "FF0000"]
                for j in range(3):
                    chart = LineChart()
                    chart.title = f"Ángulo Potenciómetro {j+1} vs Tiempo"
                    chart.y_axis.title = "Ángulo (°)"
                    chart.x_axis.title = "Muestra"
                    
                    data = Reference(ws, min_col=j*2+3, min_row=1, max_row=max_len+1)
                    categories = Reference(ws, min_col=1, min_row=2, max_row=max_len+1)
                    chart.add_data(data, titles_from_data=True)
                    chart.set_categories(categories)
                    
                    ws.add_chart(chart, f"{chr(75+j*8)}2")  # K2, S2, AA2
                
                # Guardar
                wb.save(filename)
                QMessageBox.information(self, "Éxito", f"Datos exportados a {filename}")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al exportar: {str(e)}")

    # ============================================================================
    # FUNCIONES DE MONITOREO - DISTANCIA IR
    # ============================================================================
    
    def toggle_distancia_ir_monitoring(self):
        """Inicia o detiene el monitoreo del sensor de distancia IR"""
        if not self.distancia_ir_is_monitoring:
            self.start_distancia_ir_monitoring()
        else:
            self.stop_distancia_ir_monitoring()
    
    def start_distancia_ir_monitoring(self):
        """Inicia el monitoreo del sensor de distancia IR"""
        if not self.is_connected:
            QMessageBox.warning(self, "Sin conexión", "Debes conectar al ESP32 primero")
            return
        
        try:
            # Crear y configurar thread
            self.distancia_ir_thread = DistanciaIRThread(self.esp_client.esp32_ip)
            self.distancia_ir_thread.data_received.connect(self.update_distancia_ir_data)
            
            # Iniciar monitoreo
            self.distancia_ir_thread.start()
            self.distancia_ir_is_monitoring = True
            
            # Actualizar interfaz
            self.start_distancia_ir_btn.setText("⏸️ Pausar")
            self.start_distancia_ir_btn.setStyleSheet("QPushButton { background-color: #ffc107; border-color: #ffc107; color: white; padding: 10px; }")
            self.stop_distancia_ir_btn.setEnabled(True)
            if hasattr(self, 'export_distancia_ir_btn'):
                self.export_distancia_ir_btn.setEnabled(True)
            
            # Iniciar timer de actualización gráfica
            self.graph_update_timer.start()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al iniciar monitoreo: {str(e)}")
    
    def stop_distancia_ir_monitoring(self):
        """Detiene el monitoreo del sensor de distancia IR"""
        if self.distancia_ir_thread and self.distancia_ir_thread.isRunning():
            self.distancia_ir_thread.stop()
            self.distancia_ir_thread = None
        
        self.distancia_ir_is_monitoring = False
        self.graph_update_timer.stop()
        
        # Actualizar interfaz
        self.start_distancia_ir_btn.setText("▶️ Iniciar Monitoreo")
        self.start_distancia_ir_btn.setStyleSheet("QPushButton { background-color: #e74c3c; border-color: #e74c3c; color: white; padding: 10px; }")
        self.stop_distancia_ir_btn.setEnabled(False)
    
    def update_distancia_ir_data(self, estado_digital):
        """Actualiza los datos del sensor de distancia IR (digital)"""
        # Actualizar etiqueta con estado digital
        estado_texto = "DETECTADO" if estado_digital else "NO DETECTADO"
        color = "#e74c3c" if estado_digital else "#27ae60"
        
        self.distancia_ir_label.setText(f"Estado: {estado_texto}")
        self.distancia_ir_label.setStyleSheet(f"""
            font-size: 18px;
            font-weight: bold;
            color: {color};
            padding: 15px;
            background-color: #f8f9fa;
            border-radius: 8px;
            border: 2px solid {color};
        """)
        
        # No necesitamos gráficas para sensores digitales, solo estado actual
        # Marcar para actualización si es necesario
        self.pending_updates = True
        self.pending_distancia_ir_data = estado_digital
    
    def clear_distancia_ir_graph(self):
        """Limpia la gráfica del sensor de distancia IR"""
        self.distancia_ir_lecturas.clear()
        self.distancia_ir_voltajes.clear()
        self.distancia_ir_cm.clear()
        
        if hasattr(self, 'line_ir'):
            self.line_ir.set_data([], [])
            self.ax_ir.set_xlim(0, 100)
            self.canvas_ir.draw()
        
        self.distancia_ir_label.setText("ADC: -- | Voltaje: -- V | Distancia: -- cm")
        if hasattr(self, 'export_distancia_ir_btn'):
            self.export_distancia_ir_btn.setEnabled(False)
    
    def export_distancia_ir_to_excel(self):
        """Exporta los datos del sensor de distancia IR a Excel"""
        if not self.distancia_ir_lecturas:
            QMessageBox.information(self, "Sin datos", "No hay datos para exportar")
            return
        
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename, _ = QFileDialog.getSaveFileName(
                self, "Guardar datos",
                f"SensoraCore_DistanciaIR_{timestamp}.xlsx",
                "Excel files (*.xlsx)"
            )
            
            if filename:
                # Crear workbook
                wb = openpyxl.Workbook()
                ws = wb.active
                ws.title = "Datos Distancia IR"
                
                # Headers
                ws['A1'] = "Muestra"
                ws['B1'] = "Lectura ADC"
                ws['C1'] = "Voltaje (V)"
                ws['D1'] = "Distancia (cm)"
                ws['E1'] = "Timestamp"
                
                # Datos
                for i, (lectura, voltaje, distancia) in enumerate(zip(self.distancia_ir_lecturas, self.distancia_ir_voltajes, self.distancia_ir_cm)):
                    ws[f'A{i+2}'] = i+1
                    ws[f'B{i+2}'] = lectura
                    ws[f'C{i+2}'] = voltaje
                    ws[f'D{i+2}'] = distancia
                    ws[f'E{i+2}'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # Crear gráfica
                chart = LineChart()
                chart.title = "Distancia IR vs Tiempo"
                chart.y_axis.title = "Distancia (cm)"
                chart.x_axis.title = "Muestra"
                
                data = Reference(ws, min_col=4, min_row=1, max_row=len(self.distancia_ir_cm)+1)
                categories = Reference(ws, min_col=1, min_row=2, max_row=len(self.distancia_ir_cm)+1)
                chart.add_data(data, titles_from_data=True)
                chart.set_categories(categories)
                
                ws.add_chart(chart, "G2")
                
                # Guardar
                wb.save(filename)
                QMessageBox.information(self, "Éxito", f"Datos exportados a {filename}")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al exportar: {str(e)}")

    # ============================================================================
    # FUNCIONES DE MONITOREO - DISTANCIA CAPACITIVO
    # ============================================================================
    
    def toggle_distancia_cap_monitoring(self):
        """Inicia o detiene el monitoreo del sensor de distancia capacitivo"""
        if not self.distancia_cap_is_monitoring:
            self.start_distancia_cap_monitoring()
        else:
            self.stop_distancia_cap_monitoring()
    
    def start_distancia_cap_monitoring(self):
        """Inicia el monitoreo del sensor de distancia capacitivo"""
        if not self.is_connected:
            QMessageBox.warning(self, "Sin conexión", "Debes conectar al ESP32 primero")
            return
        
        try:
            # Crear y configurar thread
            self.distancia_cap_thread = DistanciaCapThread(self.esp_client.esp32_ip)
            self.distancia_cap_thread.data_received.connect(self.update_distancia_cap_data)
            
            # Iniciar monitoreo
            self.distancia_cap_thread.start()
            self.distancia_cap_is_monitoring = True
            
            # Actualizar interfaz
            self.start_distancia_cap_btn.setText("⏸️ Pausar")
            self.start_distancia_cap_btn.setStyleSheet("QPushButton { background-color: #ffc107; border-color: #ffc107; color: white; padding: 10px; }")
            self.stop_distancia_cap_btn.setEnabled(True)
            if hasattr(self, 'export_distancia_cap_btn'):
                self.export_distancia_cap_btn.setEnabled(True)
            
            # Iniciar timer de actualización gráfica
            self.graph_update_timer.start()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al iniciar monitoreo: {str(e)}")
    
    def stop_distancia_cap_monitoring(self):
        """Detiene el monitoreo del sensor de distancia capacitivo"""
        if self.distancia_cap_thread and self.distancia_cap_thread.isRunning():
            self.distancia_cap_thread.stop()
            self.distancia_cap_thread = None
        
        self.distancia_cap_is_monitoring = False
        self.graph_update_timer.stop()
          # Actualizar interfaz
        self.start_distancia_cap_btn.setText("▶️ Iniciar Monitoreo")
        self.start_distancia_cap_btn.setStyleSheet("QPushButton { background-color: #3498db; border-color: #3498db; color: white; padding: 10px; }")
        self.stop_distancia_cap_btn.setEnabled(False)
    
    def update_distancia_cap_data(self, estado_digital):
        """Actualiza los datos del sensor de distancia capacitivo (digital)"""
        # Actualizar etiqueta con estado digital
        estado_texto = "🟢 DETECTADO" if estado_digital else "🔴 SIN DETECCIÓN"
        color = "#28a745" if estado_digital else "#dc3545"
        
        self.distancia_cap_status.setText(estado_texto)
        self.distancia_cap_status.setStyleSheet(f"""
            font-size: 28px;
            font-weight: bold;
            color: {color};
            padding: 20px;
            background-color: #f8f9fa;
            border-radius: 12px;
            border: 3px solid {color};
            text-align: center;
        """)
        
        # No necesitamos gráficas para sensores digitales, solo estado actual
        # Marcar para actualización si es necesario        self.pending_updates = True
        self.pending_distancia_cap_data = estado_digital
    
    def clear_distancia_cap_graph(self):
        """Resetea el estado del sensor de distancia capacitivo digital"""
        # Para sensores digitales, no hay datos continuos que exportar
        # Solo exportamos el estado actual si está disponible
        QMessageBox.information(self, "Sensor Digital", 
            "Los sensores digitales no generan datos continuos para exportar.\n\n"
            "El sensor capacitivo solo proporciona estado ON/OFF en tiempo real.\n"
            "Estado actual visible en la interfaz.")
        return

    # ============================================================================
    # FUNCIONES DE MONITOREO - DISTANCIA ULTRASONICO
    # ============================================================================
    
    def toggle_distancia_ultra_monitoring(self):
        """Inicia o detiene el monitoreo del sensor de distancia ultrasónico"""
        if not self.distancia_ultra_is_monitoring:
            self.start_distancia_ultra_monitoring()
        else:
            self.stop_distancia_ultra_monitoring()
    
    def start_distancia_ultra_monitoring(self):
        """Inicia el monitoreo del sensor de distancia ultrasónico"""
        if not self.is_connected:
            QMessageBox.warning(self, "Sin conexión", "Debes conectar al ESP32 primero")
            return
        
        try:
            # Crear y configurar thread
            self.distancia_ultrasonic_thread = DistanciaUltrasonicThread(self.esp_client.esp32_ip)
            self.distancia_ultrasonic_thread.data_received.connect(self.update_distancia_ultra_data)
            
            # Iniciar monitoreo
            self.distancia_ultrasonic_thread.start()
            self.distancia_ultra_is_monitoring = True
            
            # Actualizar interfaz
            self.start_distancia_ultra_btn.setText("⏸️ Pausar")
            self.start_distancia_ultra_btn.setStyleSheet("QPushButton { background-color: #ffc107; border-color: #ffc107; color: white; padding: 10px; }")
            self.stop_distancia_ultra_btn.setEnabled(True)
            if hasattr(self, 'export_distancia_ultra_btn'):
                self.export_distancia_ultra_btn.setEnabled(True)
            
            # Iniciar timer de actualización gráfica
            self.graph_update_timer.start()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al iniciar monitoreo: {str(e)}")
    
    def stop_distancia_ultra_monitoring(self):
        """Detiene el monitoreo del sensor de distancia ultrasónico"""
        if self.distancia_ultrasonic_thread and self.distancia_ultrasonic_thread.isRunning():
            self.distancia_ultrasonic_thread.stop()
            self.distancia_ultrasonic_thread = None
        
        self.distancia_ultra_is_monitoring = False
        self.graph_update_timer.stop()
        
        # Actualizar interfaz
        self.start_distancia_ultra_btn.setText("▶️ Iniciar Monitoreo")
        self.start_distancia_ultra_btn.setStyleSheet("QPushButton { background-color: #17a2b8; border-color: #17a2b8; color: white; padding: 10px; }")
        self.stop_distancia_ultra_btn.setEnabled(False)
    
    def update_distancia_ultra_data(self, lectura_adc, voltaje, distancia_cm):
        """Actualiza los datos del sensor de distancia ultrasónico"""
        # Agregar datos a las listas
        self.distancia_ultra_lecturas.append(lectura_adc)
        self.distancia_ultra_voltajes.append(voltaje)
        self.distancia_ultra_cm.append(distancia_cm)
        
        # Mantener máximo de puntos
        if len(self.distancia_ultra_lecturas) > self.distancia_max_points:
            self.distancia_ultra_lecturas.pop(0)
            self.distancia_ultra_voltajes.pop(0)
            self.distancia_ultra_cm.pop(0)
        
        # Actualizar etiqueta con el nuevo formato simplificado
        self.distancia_ultra_label.setText(f"Distancia: {distancia_cm:.1f} cm")
        
        # Actualizar gráfica de forma optimizada
        if hasattr(self, 'line_ultra'):
            x_data = list(range(len(self.distancia_ultra_cm)))
            self.line_ultra.set_data(x_data, self.distancia_ultra_cm)
            
            # Ajustar límites del eje X
            if len(x_data) > 0:
                self.ax_ultra.set_xlim(0, max(100, len(x_data)))
          # Marcar para actualización
        self.pending_updates = True
        self.pending_distancia_ultra_data = (lectura_adc, voltaje, distancia_cm)
    
    def clear_distancia_ultra_graph(self):
        """Limpia la gráfica del sensor de distancia ultrasónico"""
        self.distancia_ultra_lecturas.clear()
        self.distancia_ultra_voltajes.clear()
        self.distancia_ultra_cm.clear()
        
        if hasattr(self, 'line_ultra'):
            self.line_ultra.set_data([], [])
            self.ax_ultra.set_xlim(0, 100)
            self.canvas_ultra.draw()
        
        self.distancia_ultra_label.setText("Distancia: -- cm")
        if hasattr(self, 'export_distancia_ultra_btn'):
            self.export_distancia_ultra_btn.setEnabled(False)
    
    def export_distancia_ultra_to_excel(self):
        """Exporta los datos del sensor de distancia ultrasónico a Excel"""
        if not self.distancia_ultra_lecturas:
            QMessageBox.information(self, "Sin datos", "No hay datos para exportar")
            return
        
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename, _ = QFileDialog.getSaveFileName(
                self, "Guardar datos",
                f"SensoraCore_DistanciaUltra_{timestamp}.xlsx",
                "Excel files (*.xlsx)"
            )
            
            if filename:
                # Crear workbook
                wb = openpyxl.Workbook()
                ws = wb.active
                ws.title = "Datos Distancia Ultrasónico"
                
                # Headers
                ws['A1'] = "Muestra"
                ws['B1'] = "Lectura ADC"
                ws['C1'] = "Voltaje (V)"
                ws['D1'] = "Distancia (cm)"
                ws['E1'] = "Timestamp"
                
                # Datos
                for i, (lectura, voltaje, distancia) in enumerate(zip(self.distancia_ultra_lecturas, self.distancia_ultra_voltajes, self.distancia_ultra_cm)):
                    ws[f'A{i+2}'] = i+1
                    ws[f'B{i+2}'] = lectura
                    ws[f'C{i+2}'] = voltaje
                    ws[f'D{i+2}'] = distancia
                    ws[f'E{i+2}'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # Crear gráfica
                chart = LineChart()
                chart.title = "Distancia Ultrasónico vs Tiempo"
                chart.y_axis.title = "Distancia (cm)"
                chart.x_axis.title = "Muestra"
                
                data = Reference(ws, min_col=4, min_row=1, max_row=len(self.distancia_ultra_cm)+1)
                categories = Reference(ws, min_col=1, min_row=2, max_row=len(self.distancia_ultra_cm)+1)
                chart.add_data(data, titles_from_data=True)
                chart.set_categories(categories)
                
                ws.add_chart(chart, "G2")
                
                # Guardar
                wb.save(filename)
                QMessageBox.information(self, "Éxito", f"Datos exportados a {filename}")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al exportar: {str(e)}")
