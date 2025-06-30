# =====================================================================================
# ARCHIVO PRINCIPAL DE INTERFAZ GRÁFICA PARA SENSORACORE
# =====================================================================================
# Ruta del archivo: main_window.py para SensoraCore/ui
# Función: Define la ventana principal y todas las interfaces de los sensores
# Autor: Sistema SensoraCore
# Propósito: Crear una aplicación desktop para monitoreo de sensores ESP32
from IMPORTACIONES import *  # Importar todo lo necesario desde el módulo de importaciones
from Modulos.SENSORA_SIMPLE_ANGLE import (LinearCalibration, anguloSimple_UI, AnguloSimpleMonitor)

# =====================================================================================
# CLASE PRINCIPAL: VENTANA PRINCIPAL DE LA APLICACIÓN SENSORACORE
# =====================================================================================
# Propósito: Ventana principal que contiene toda la interfaz de usuario
# Funcionalidad: Gestiona conexión ESP32, selección de sensores, y visualización de datos
# Hereda de: QMainWindow (ventana principal de Qt con menús, barras de herramientas, etc.)


class MainWindow(QMainWindow, AnguloSimpleMonitor):
    def __init__(self):
        """
        Constructor de la ventana principal
        Inicializa todos los componentes de la interfaz y variables de estado
        """
        super().__init__()                       # Inicializar la clase padre QMainWindow
        
        # --- CONFIGURACIÓN BÁSICA DE VENTANA ---
        self.setWindowTitle("SensoraCore")       # Título que aparece en la barra de título
        self.setMinimumSize(1000, 700)          # Tamaño mínimo permitido (ancho x alto)
        self.resize(1200, 800)                  # Tamaño inicial de la ventana
        
        # =====================================================================================
        # VARIABLES DE ESTADO PARA CONEXIÓN Y HILOS
        # =====================================================================================
        
        # --- Variables para cliente ESP32 y hilos de sensores ---
        self.esp_client = None                   # Cliente para comunicación básica con ESP32
          # --- Banderas de estado general ---
        self.is_connected = False               # True cuando ESP32 está conectado

        # =====================================================================================
        # INICIALIZACIÓN DE LA INTERFAZ
        # =====================================================================================
        
        # Configurar estilo visual de la aplicación
        self.setup_styles()
        # Crear todos los elementos de la interfaz de usuario
        self.setup_ui()

    # =====================================================================================
    # MÉTODO AUXILIAR: GESTIÓN DEL TIMER DE GRÁFICAS
    # =====================================================================================
    


      # =====================================================================================
    # MÉTODO: CONFIGURACIÓN DE ESTILOS VISUALES
    # =====================================================================================
    def setup_styles(self):
        """
        Configura los estilos globales de la aplicación usando CSS-like syntax
        
        Propósito: Define la apariencia visual de todos los elementos de la interfaz
        Tecnología: QSS (Qt Style Sheets) - similar a CSS para web
        Resultado: Interfaz moderna y profesional con colores consistentes
        """
        self.setStyleSheet("""
            /* ======================== VENTANA PRINCIPAL ======================== */
            /* Configuración del fondo general de toda la aplicación */
            QMainWindow {
                background-color: #f8f9fa;  /* Color de fondo: gris muy claro (#f8f9fa) */
            }
            
            /* ======================== CAJAS DE GRUPO ======================== */
            /* Estilo para todas las cajas de grupo (secciones) de la aplicación */
            /* QGroupBox se usa para agrupar controles relacionados con un borde y título */
            QGroupBox {
                font-weight: bold;              /* Texto en negrita para destacar títulos */
                border: 2px solid #dee2e6;     /* Borde sólido gris claro de 2px de grosor */
                border-radius: 8px;            /* Esquinas redondeadas (8px de radio) */
                margin-top: 1ex;               /* Margen superior para acomodar el título */
                padding-top: 10px;             /* Espacio interno superior (10px) */
                background-color: white;       /* Fondo blanco para contraste */
            }
            
            /* Estilo específico para los títulos de las cajas de grupo */
            QGroupBox::title {
                subcontrol-origin: margin;     /* El título se origina desde el margen */
                left: 10px;                    /* Posición izquierda del título (10px desde borde) */
                padding: 0 8px 0 8px;         /* Padding: arriba=0, derecha=8px, abajo=0, izquierda=8px */
                color: #495057;               /* Color del texto: gris oscuro profesional */
                background-color: white;       /* Fondo blanco para que se vea sobre el borde */
            }
            
            /* ======================== BOTONES ESTÁNDAR ======================== */
            /* Estilo base para todos los botones de la aplicación */
            QPushButton {
                border: 2px solid #007bff;     /* Borde azul Bootstrap de 2px */
                border-radius: 6px;            /* Esquinas redondeadas moderadas */
                padding: 8px 16px;             /* Padding interno: 8px vertical, 16px horizontal */
                background-color: #007bff;     /* Fondo azul primario Bootstrap */
                color: black;                  /* Texto negro para máximo contraste */
                font-weight: bold;             /* Texto en negrita para legibilidad */
                min-height: 20px;             /* Altura mínima para botones uniformes */
            }
            
            /* Estilo cuando el mouse pasa por encima del botón (hover effect) */
            QPushButton:hover {
                background-color: #0056b3;     /* Azul más oscuro al hacer hover */
                border-color: #0056b3;         /* Borde también más oscuro */
            }
            
            /* Estilo cuando el botón está siendo presionado (pressed state) */
            QPushButton:pressed {
                background-color: #004085;     /* Azul muy oscuro para feedback visual */
            }
            
            /* Estilo cuando el botón está deshabilitado (disabled state) */
            QPushButton:disabled {
                background-color: #6c757d;     /* Gris para indicar estado inactivo */
                border-color: #6c757d;         /* Borde gris consistente */
                color: #adb5bd;               /* Texto gris claro para menor contraste */
            }
            
            /* ======================== CAMPOS DE TEXTO ======================== */
            /* Estilo para todos los campos de entrada de texto (QLineEdit) */
            QLineEdit {
                border: 2px solid #ced4da;     /* Borde gris neutro */
                border-radius: 6px;            /* Esquinas redondeadas suaves */
                padding: 8px 12px;             /* Padding: 8px vertical, 12px horizontal */
                font-size: 14px;              /* Tamaño de fuente legible */
                background-color: white;       /* Fondo blanco limpio */
                color: black;                  /* Texto negro para contraste */
            }
            
            /* Estilo cuando el campo de texto tiene foco (usuario está escribiendo) */
            QLineEdit:focus {
                border-color: #007bff;         /* Borde azul para indicar campo activo */
                outline: none;                 /* Remover outline por defecto del sistema */
            }
            
            /* ======================== LISTAS DE SENSORES ======================== */
            /* Estilo para la lista de sensores disponibles (QListWidget) */
            QListWidget {
                border: 1px solid #dee2e6;     /* Borde sutil gris claro */
                border-radius: 6px;            /* Esquinas redondeadas */
                background-color: white;       /* Fondo blanco principal */
                alternate-background-color: #f8f9fa;  /* Color alternativo para filas zebra */
            }
            
            /* Estilo para cada elemento individual de la lista de sensores */
            QListWidget::item {
                padding: 12px;                 /* Espacio interno generoso para legibilidad */
                border-bottom: 1px solid #e9ecef;  /* Línea separadora sutil entre elementos */
                color: black;                  /* Texto negro */
            }
            
            /* Estilo cuando el mouse pasa por encima de un elemento de la lista */
            QListWidget::item:hover {
                background-color: #7db9f9;     /* Azul claro suave para hover */
            }
            
            /* Estilo cuando un elemento de la lista está seleccionado */
            QListWidget::item:selected {
                background-color: #007bff;     /* Azul primario para selección */
                color: black;                  /* Mantener texto negro para contraste */
            }
        """)
    # =====================================================================================
    # MÉTODO: CONFIGURACIÓN DE LA INTERFAZ DE USUARIO
    # =====================================================================================
    def setup_ui(self):
        """
        Configura la estructura principal de la interfaz de usuario
        
        Propósito: Crear el layout principal con panel izquierdo y derecho
        Diseño: Interfaz dividida (split) con conexión/sensores a la izquierda y detalles a la derecha
        Tecnología: QSplitter para división ajustable entre paneles
        """
        
        # --- WIDGET CENTRAL PRINCIPAL ---
        # Toda aplicación QMainWindow necesita un widget central
        central_widget = QWidget()               # Crear widget contenedor principal
        self.setCentralWidget(central_widget)    # Establecer como widget central de la ventana
        
        # --- LAYOUT PRINCIPAL HORIZONTAL ---
        # QHBoxLayout organiza elementos horizontalmente (lado a lado)
        main_layout = QHBoxLayout(central_widget)  # Aplicar layout al widget central
        main_layout.setSpacing(20)               # Espacio entre elementos: 20 píxeles
        main_layout.setContentsMargins(20, 20, 20, 20)  # Márgenes: 20px en todos los lados
        
        # --- CREAR SPLITTER PARA DIVISIÓN RESPONSIVE ---
        # QSplitter permite al usuario ajustar el tamaño de los paneles arrastrando
        splitter = QSplitter(Qt.Horizontal)      # Divisor horizontal (izquierda-derecha)
        main_layout.addWidget(splitter)          # Agregar splitter al layout principal
        
        # --- PANEL IZQUIERDO (conexión y lista de sensores) ---
        self.left_panel = self.create_left_panel()  # Crear panel izquierdo (método separado)
        splitter.addWidget(self.left_panel)     # Agregar al splitter
        
        # --- PANEL DERECHO (detalles del sensor seleccionado) ---
        self.right_panel = self.create_right_panel()  # Crear panel derecho (método separado)
        splitter.addWidget(self.right_panel)    # Agregar al splitter
        
        # --- CONFIGURAR PROPORCIONES DEL SPLITTER ---
        # setStretchFactor define qué tanto espacio ocupa cada panel relativo al otro
        splitter.setStretchFactor(0, 1)         # Panel izquierdo: factor 1 (1/3 del espacio)
        splitter.setStretchFactor(1, 2)         # Panel derecho: factor 2 (2/3 del espacio)
        splitter.setSizes([400, 800])           # Tamaños iniciales en píxeles [izquierdo, derecho]    
    # =====================================================================================
    # MÉTODO: CREACIÓN DEL PANEL IZQUIERDO
    # =====================================================================================
    def create_left_panel(self):
        """
        Crea el panel izquierdo con conexión ESP32 y lista de sensores
        
        Propósito: Interface para conectar al ESP32 y seleccionar sensores disponibles
        Contenido: Título, configuración de conexión, estado, y lista de sensores
        Retorna: QFrame configurado con todos los elementos del panel izquierdo
        """
        
        # --- CONTENEDOR PRINCIPAL DEL PANEL ---
        panel = QFrame()                         # Crear frame contenedor
        panel.setFrameStyle(QFrame.StyledPanel)  # Estilo de panel con borde
        panel.setStyleSheet("QFrame { background-color: white; border-radius: 8px; }")  # Fondo blanco redondeado
        
        # --- LAYOUT VERTICAL DEL PANEL ---
        layout = QVBoxLayout(panel)              # Layout vertical (elementos apilados)
        layout.setSpacing(20)                    # Espacio entre elementos: 20px
        layout.setContentsMargins(20, 20, 20, 20)  # Márgenes internos: 20px todos los lados
        
        # =====================================================================================
        # SECCIÓN: TÍTULO Y SUBTÍTULO DE BIENVENIDA
        # =====================================================================================
        
        # --- TÍTULO PRINCIPAL ---
        title_label = QLabel("SensoraCore")      # Crear etiqueta con nombre de la aplicación
        title_label.setAlignment(Qt.AlignCenter) # Centrar texto horizontalmente
        title_label.setStyleSheet("""
            font-size: 24px;                    /* Tamaño de fuente grande */
            font-weight: bold;                  /* Texto en negrita */
            color: #007bff;                     /* Color azul corporativo */
            margin: 10px 0;                     /* Margen vertical de 10px */
        """)
        layout.addWidget(title_label)           # Agregar título al layout
        
        # --- SUBTÍTULO DESCRIPTIVO ---
        subtitle_label = QLabel("Sistema de Monitoreo de Sensores WiFi")  # Descripción del sistema
        subtitle_label.setAlignment(Qt.AlignCenter)  # Centrar texto
        subtitle_label.setStyleSheet("""
            font-size: 14px;                    /* Tamaño mediano */
            color: #6c757d;                     /* Color gris suave */
            margin-bottom: 20px;                /* Margen inferior para separación */
        """)
        layout.addWidget(subtitle_label)       # Agregar subtítulo al layout
        
        # =====================================================================================
        # SECCIÓN: CONFIGURACIÓN DE CONEXIÓN ESP32
        # =====================================================================================
        
        # --- GRUPO DE CONEXIÓN ---
        connection_group = QGroupBox("Configuración de Conexión")  # Caja agrupada con título
        connection_layout = QVBoxLayout(connection_group)  # Layout vertical para la caja
        
        # --- ETIQUETA PARA CAMPO IP ---
        ip_label = QLabel("IP del ESP32:")       # Etiqueta descriptiva
        ip_label.setStyleSheet("font-weight: bold; color: #495057;")  # Negrita y color oscuro
        connection_layout.addWidget(ip_label)   # Agregar etiqueta al grupo
        
        # --- CAMPO DE ENTRADA DE IP ---
        self.ip_input = QLineEdit()              # Campo de texto para ingresar IP
        self.ip_input.setPlaceholderText("Ejemplo: 192.168.1.100")  # Texto de ayuda
        self.ip_input.setText("192.168.20.27")  # IP predeterminada (cambiar según red)
        connection_layout.addWidget(self.ip_input)  # Agregar campo al grupo
        
        # --- BOTÓN DE CONEXIÓN ---
        self.connect_btn = QPushButton("🔌 Conectar ESP32")  # Botón con emoji para visual
        self.connect_btn.clicked.connect(self.test_connection)  # Conectar señal click al método
        connection_layout.addWidget(self.connect_btn)  # Agregar botón al grupo
        
        # --- INDICADOR DE ESTADO DE CONEXIÓN ---
        self.status_label = QLabel("⚪ Desconectado")  # Etiqueta de estado inicial
        self.status_label.setAlignment(Qt.AlignCenter)  # Centrar texto
        self.status_label.setStyleSheet("""
            padding: 8px;                       /* Espacio interno */
            border-radius: 4px;                 /* Esquinas redondeadas */
            background-color: #f8d7da;          /* Fondo rojo claro (desconectado) */
            color: #721c24;                     /* Texto rojo oscuro */
            font-weight: bold;                  /* Texto en negrita */
        """)
        connection_layout.addWidget(self.status_label)  # Agregar indicador al grupo
        
        layout.addWidget(connection_group)     # Agregar grupo completo al panel
        
        # =====================================================================================
        # SECCIÓN: LISTA DE SENSORES DISPONIBLES
        # =====================================================================================
        
        # --- GRUPO DE SENSORES (inicialmente oculto) ---
        self.sensors_group = QGroupBox("Sensores Disponibles")  # Caja para lista de sensores
        self.sensors_group.setVisible(False)   # Ocultar hasta que se conecte ESP32
        
        sensors_layout = QVBoxLayout(self.sensors_group)  # Layout para el grupo de sensores
        
        # --- LISTA DE SENSORES ---
        self.sensors_list = QListWidget()       # Widget de lista para sensores
        self.sensors_list.itemClicked.connect(self.on_sensor_selected)  # Conectar evento de selección
        
        # --- POBLAR LISTA CON SENSORES DISPONIBLES ---
        self.add_sensor_items()                 # Método que agrega los sensores a la lista
        
        sensors_layout.addWidget(self.sensors_list)  # Agregar lista al grupo
        layout.addWidget(self.sensors_group)   # Agregar grupo al panel principal
          # =====================================================================================
        # SECCIÓN: BOTÓN DE REINICIO EN ESQUINA SUPERIOR IZQUIERDA
        # =====================================================================================
        
        # --- BOTÓN DE REINICIO ---
        self.restart_btn = QPushButton("🔄 Reiniciar Interfaz")  # Botón con emoji de reinicio
        self.restart_btn.setMinimumHeight(40)    # Altura mínima para mayor visibilidad
        self.restart_btn.setMaximumWidth(180)    # Ancho máximo controlado
        self.restart_btn.clicked.connect(self.restart_application)  # Conectar al método de reinicio
        self.restart_btn.setEnabled(False)      # Deshabilitado hasta conectar ESP32
        self.restart_btn.setStyleSheet("""
            QPushButton {
                background-color: #28a745;     /* Verde para acción positiva */
                color: white;                   /* Texto blanco */
                border: none;                   /* Sin borde */
                border-radius: 8px;             /* Esquinas redondeadas */
                font-weight: bold;              /* Texto en negrita */
                font-size: 12px;                /* Tamaño de fuente legible */
                padding: 8px 12px;              /* Espaciado interno */
            }
            QPushButton:hover {
                background-color: #218838;     /* Verde más oscuro al pasar mouse */
            }
            QPushButton:pressed {
                background-color: #1e7e34;     /* Verde aún más oscuro al presionar */
            }
            QPushButton:disabled {
                background-color: #6c757d;     /* Gris cuando está deshabilitado */
                color: #dee2e6;                 /* Texto gris claro */
            }
        """)
        layout.addWidget(self.restart_btn)       # Agregar botón al panel principal
        
        # --- ESPACIADOR FLEXIBLE ---
        layout.addStretch()                     # Agregar espacio flexible al final
        
        return panel                            # Retornar panel completo configurado
    # =====================================================================================
    # MÉTODO: AGREGAR ELEMENTOS A LA LISTA DE SENSORES
    # =====================================================================================
    def add_sensor_items(self):
        """
        Agrega los sensores disponibles a la lista del panel izquierdo
        
        Propósito: Poblar la lista con todos los tipos de sensores soportados
        Funcionalidad: Crear elementos de lista con descripción, emoji y estado de disponibilidad
        Datos: Cada sensor tiene emoji, descripción y ID único para identificación
        """
        
        # --- DEFINIR SENSORES DISPONIBLES ---
        # Tupla con: (emoji_nombre, descripción_funcional, identificador_único)
        sensors = [
            ("🎛️ Ángulo Simple", "Potenciómetro como sensor de ángulo", "angulo_simple"),
            ("🦾 Brazo Ángulo", "Sensor de ángulo para brazo robótico", "brazo_angulo"),
            ("📏 Distancia IR", "Sensor de distancia infrarrojo", "distancia_ir"),
            ("🔍 Distancia Capacitivo", "Sensor de distancia capacitivo", "distancia_cap"),
            ("📡 Distancia Ultrasónico", "Sensor HC-SR04", "distancia_ultra"),
            ("💨 Velocidad Óptica", "Sensor óptico de velocidad", "velocidad_optica")
        ]
        
        # --- CREAR ELEMENTOS DE LISTA PARA CADA SENSOR ---
        for icon_name, description, sensor_id in sensors:  # Iterar por cada sensor definido
            # Crear elemento individual de la lista
            item = QListWidgetItem()             # Nuevo elemento de lista
            item.setText(f"{icon_name}\n{description}")  # Texto: emoji + descripción en 2 líneas
            item.setData(Qt.UserRole, sensor_id) # Guardar ID único en datos del elemento
            
            # --- VERIFICAR DISPONIBILIDAD DEL SENSOR ---
            # Lista de sensores actualmente implementados y funcionales
            if sensor_id not in ["angulo_simple", "brazo_angulo", "distancia_ir", "distancia_cap", "distancia_ultra"]:
                # Para sensores no implementados:
                item.setFlags(item.flags() & ~Qt.ItemIsEnabled)  # Deshabilitar elemento
                item.setText(f"{icon_name}\n{description}\n(Próximamente)")  # Agregar nota de estado
                item.setToolTip("Esta función será implementada en futuras versiones")  # Tooltip informativo
            
            # --- AGREGAR ELEMENTO A LA LISTA ---
            self.sensors_list.addItem(item)      # Añadir elemento configurado a la lista    
    # =====================================================================================
    # MÉTODO: CREACIÓN DEL PANEL DERECHO
    # =====================================================================================
    def create_right_panel(self):
        """
        Crea el panel derecho para mostrar detalles del sensor seleccionado
        
        Propósito: Área principal donde se muestran gráficas, datos y controles del sensor activo
        Estados: Pantalla de bienvenida inicial → Interfaz específica del sensor seleccionado
        Contenido: Mensaje de bienvenida, instrucciones, y espacio para interfaces de sensores
        """
        
        # --- CONTENEDOR PRINCIPAL DEL PANEL DERECHO ---
        panel = QFrame()                         # Frame contenedor principal
        panel.setFrameStyle(QFrame.StyledPanel)  # Estilo de panel con borde
        panel.setStyleSheet("QFrame { background-color: white; border-radius: 8px; }")  # Fondo blanco redondeado
        
        # --- LAYOUT VERTICAL DEL PANEL ---
        layout = QVBoxLayout(panel)              # Layout vertical para apilar elementos
        layout.setContentsMargins(20, 20, 20, 20)  # Márgenes internos de 20px
        
        # =====================================================================================
        # SECCIÓN: MENSAJE DE BIENVENIDA INICIAL
        # =====================================================================================
        
        # --- WIDGET DE BIENVENIDA ---
        self.welcome_widget = QWidget()          # Widget contenedor para la pantalla inicial
        welcome_layout = QVBoxLayout(self.welcome_widget)  # Layout vertical para el contenido
        
        # --- ICONO PRINCIPAL ---
        welcome_icon = QLabel("🔧")              # Emoji de herramienta como icono principal
        welcome_icon.setAlignment(Qt.AlignCenter)  # Centrar icono horizontalmente
        welcome_icon.setStyleSheet("font-size: 72px; margin: 50px;")  # Tamaño grande con margen
        welcome_layout.addWidget(welcome_icon)   # Agregar icono al layout de bienvenida
        
        # --- TEXTO INSTRUCTIVO PRINCIPAL ---
        welcome_text = QLabel("Conecta tu ESP32 y selecciona un sensor\npara comenzar a monitorear datos")
        welcome_text.setAlignment(Qt.AlignCenter)  # Centrar texto
        welcome_text.setStyleSheet("""
            font-size: 16px;                    /* Tamaño de fuente legible */
            color: #6c757d;                     /* Color gris suave */
            line-height: 1.5;                   /* Espaciado entre líneas */
        """)
        welcome_layout.addWidget(welcome_text)  # Agregar texto al layout
        
        # --- INDICACIÓN SOBRE DIAGRAMAS DE CONEXIÓN ---
        diagram_hint = QLabel("📋 Una vez conectado, encontrarás el diagrama\nde conexiones ESP32 en cada sensor")
        diagram_hint.setAlignment(Qt.AlignCenter)  # Centrar texto
        diagram_hint.setStyleSheet("""
            font-size: 14px;                    /* Tamaño menor para texto secundario */
            color: #495057;                     /* Color más oscuro para destacar */
            background-color: #e2f4ff;          /* Fondo azul muy claro */
            border: 1px solid #b3daff;          /* Borde azul claro */
            border-radius: 6px;                 /* Esquinas redondeadas */
            padding: 10px;                      /* Espacio interno */
            margin: 10px 40px;                  /* Margen vertical y horizontal */
        """)
        welcome_layout.addWidget(diagram_hint)  # Agregar hint al layout
        
        # --- ESPACIADOR FLEXIBLE ---
        welcome_layout.addStretch()            # Espacio flexible para centrar contenido verticalmente
        
        layout.addWidget(self.welcome_widget)  # Agregar widget de bienvenida al panel principal
        
        # =====================================================================================
        # SECCIÓN: CONTENEDOR PARA DETALLES DEL SENSOR
        # =====================================================================================
        
        # --- ÁREA DE SCROLL PARA INTERFACES DE SENSORES ---
        self.sensor_details = QScrollArea()     # Área con scroll para contenido largo
        self.sensor_details.setVisible(False)  # Inicialmente oculto (se muestra al seleccionar sensor)
        self.sensor_details.setWidgetResizable(True)  # Permitir redimensionamiento automático
        self.sensor_details.setFrameShape(QFrame.NoFrame)  # Sin marco visible
        layout.addWidget(self.sensor_details)  # Agregar área de scroll al panel
        return panel                           # Retornar panel configurado completo

    # =====================================================================================
    # MÉTODO: MANEJO DE SELECCIÓN DE SENSORES
    # =====================================================================================    
    def on_sensor_selected(self, item):
        """
        Maneja la selección de un sensor de la lista del panel izquierdo
        
        Propósito: Cambiar la interfaz del panel derecho según el sensor seleccionado
        Funcionalidad: Validar conexión ESP32 y mostrar interfaz específica del sensor
        Parámetros: item - QListWidgetItem con datos del sensor seleccionado
        """
        
        # --- VALIDAR CONEXIÓN ANTES DE MOSTRAR SENSOR ---
        if not self.is_connected:                # Verificar si ESP32 está conectado
            QMessageBox.warning(self, "Sin conexión", "Debes conectar al ESP32 primero")
            return                               # Salir sin hacer nada si no hay conexión
                
        # --- OBTENER IDENTIFICADOR DEL SENSOR ---
        sensor_id = item.data(Qt.UserRole)       # Obtener ID único almacenado en el item
        
        # --- MOSTRAR INTERFAZ ESPECÍFICA SEGÚN SENSOR ---
        if sensor_id == "angulo_simple":         # Sensor de ángulo con potenciómetro simple
            anguloSimple_UI(self)  # Mostrar la interfaz de sensor simple
        elif sensor_id == "brazo_angulo":        # Brazo robótico con múltiples sensores
            self.show_brazo_angulo_interface()
        elif sensor_id == "distancia_ir":        # Sensor de distancia infrarrojo
            self.show_distancia_ir_interface()
        elif sensor_id == "distancia_cap":       # Sensor de distancia capacitivo
            self.show_distancia_cap_interface()
        elif sensor_id == "distancia_ultra":     # Sensor ultrasónico HC-SR04
            self.show_distancia_ultra_interface()
        else:                                    # Sensores no implementados aún
            QMessageBox.information(self, "Próximamente", 
                                  "Esta función será implementada en futuras versiones")

    # =====================================================================================
    # SECCIÓN: FUNCIONES DE CONEXIÓN Y GESTIÓN DEL ESP32
    # =====================================================================================    
    # ============================================================================
    # FUNCIONES DE CONEXIÓN Y MONITOREO
    # ============================================================================
    
    # =====================================================================================
    # MÉTODO: PROBAR CONEXIÓN CON ESP32
    # =====================================================================================
    def test_connection(self):
        """
        Prueba la conexión TCP/IP con el ESP32 usando la IP proporcionada
        
        Propósito: Verificar conectividad antes de iniciar cualquier monitoreo
        Funcionamiento: Envía comando LED_ON para probar comunicación
        Validación: Verifica respuesta "LED_ON_OK" del ESP32
        UI: Actualiza estado visual y habilita/deshabilita controles
        Red: Usa cliente TCP para comunicación con ESP32
        """
        
        # --- VALIDAR ENTRADA DE IP ---
        esp32_ip = self.ip_input.text().strip()  # Obtener IP limpia sin espacios
        
        if not esp32_ip:                         # Verificar que no esté vacía
            QMessageBox.warning(self, "IP requerida", "Ingresa la IP del ESP32")
            return                               # Salir si no hay IP
        
        # --- ACTUALIZAR INTERFAZ DURANTE CONEXIÓN ---
        # Deshabilitar botón y mostrar estado de conexión en progreso
        self.connect_btn.setEnabled(False)       # Prevenir múltiples intentos
        self.status_label.setText("🔄 Conectando...")  # Estado visual de progreso
        self.status_label.setStyleSheet("""
            padding: 8px;                        /* Espaciado interno */
            border-radius: 4px;                  /* Esquinas redondeadas */
            background-color: #cce5ff;           /* Fondo azul claro */
            color: #004085;                      /* Texto azul oscuro */
            font-weight: bold;                   /* Texto en negrita */
        """)
        self.repaint()                           # Forzar actualización inmediata de la interfaz
        
        # --- PROBAR CONEXIÓN TCP ---
        # Probar conexión directamente con el ESP32
        try:
            client = ESP32Client(esp32_ip)       # Crear cliente con IP proporcionada
            response = client.led_on()           # Enviar comando de prueba LED_ON
            
            # --- VERIFICAR RESPUESTA DEL ESP32 ---
            if "LED_ON_OK" in response:          # Verificar respuesta esperada
                self.on_connected(esp32_ip)      # Conexión exitosa
            else:
                self.on_disconnected()           # Respuesta inesperada
                
        except Exception as e:
            # --- MANEJAR ERROR DE CONEXIÓN ---
            self.on_disconnected()               # Error de conexión (timeout, red, etc.)    
    # =====================================================================================
    # MÉTODO: CALLBACK DE CONEXIÓN EXITOSA
    # =====================================================================================
    def on_connected(self, esp32_ip):
        """
        Callback ejecutado cuando la conexión con el ESP32 es exitosa
        
        Propósito: Configurar la aplicación para modo conectado
        Funcionalidad: Inicializar cliente ESP32, actualizar UI, mostrar sensores
        Parámetros: esp32_ip - Dirección IP del ESP32 conectado
        UI: Cambia estado visual, habilita lista de sensores
        """
        
        # --- ESTABLECER ESTADO DE CONEXIÓN ---
        self.is_connected = True                 # Flag global de conexión
        self.esp_client = ESP32Client(esp32_ip)  # Cliente para comunicación TCP
          # --- ACTUALIZAR INTERFAZ DE CONEXIÓN ---
        self.connect_btn.setText("🔌 Conectado")  # Cambiar texto del botón
        self.connect_btn.setEnabled(False)       # Deshabilitar botón (ya conectado)
        self.restart_btn.setEnabled(True)        # Habilitar botón de reinicio
        self.status_label.setText("✅ Conectado al ESP32")  # Estado exitoso
        self.status_label.setStyleSheet("""
            padding: 8px;                        /* Espaciado interno */
            border-radius: 4px;                  /* Esquinas redondeadas */
            background-color: #d4edda;           /* Fondo verde claro */
            color: #155724;                      /* Texto verde oscuro */
            font-weight: bold;                   /* Texto en negrita */
        """)
        
        # --- MOSTRAR LISTA DE SENSORES CON ANIMACIÓN ---
        self.show_sensors_with_animation()       # Efecto visual de aparición
    
    # =====================================================================================
    # MÉTODO: CALLBACK DE CONEXIÓN FALLIDA
    # =====================================================================================
    def on_disconnected(self):
        """
        Callback ejecutado cuando la conexión con el ESP32 falla o se pierde
        
        Propósito: Configurar la aplicación para modo desconectado
        Funcionalidad: Limpiar cliente ESP32, actualizar UI, ocultar sensores
        UI: Cambia estado visual, deshabilita funcionalidades que requieren conexión
        Seguridad: Previene operaciones sin conexión válida
        """
        
        # --- LIMPIAR ESTADO DE CONEXIÓN ---
        self.is_connected = False                # Flag global de desconexión
        self.esp_client = None                   # Limpiar cliente TCP
          # --- ACTUALIZAR INTERFAZ DE CONEXIÓN ---
        self.connect_btn.setText("🔌 Conectar al ESP32")  # Restaurar texto original
        self.connect_btn.setEnabled(True)        # Habilitar botón para reconectar
        self.restart_btn.setEnabled(False)       # Deshabilitar botón de reinicio
        self.status_label.setText("❌ Error de conexión")  # Estado de error
        self.status_label.setStyleSheet("""
            padding: 8px;                        /* Espaciado interno */
            border-radius: 4px;                  /* Esquinas redondeadas */
            background-color: #f8d7da;           /* Fondo rojo claro */
            color: #721c24;                      /* Texto rojo oscuro */
            font-weight: bold;                   /* Texto en negrita */
        """)
        
        # --- OCULTAR FUNCIONALIDADES ---
        self.sensors_group.setVisible(False)     # Ocultar lista de sensores
    
    # =====================================================================================
    # MÉTODO: ANIMACIÓN DE LISTA DE SENSORES
    # =====================================================================================
    def show_sensors_with_animation(self):
        """
        Muestra la lista de sensores disponibles con efecto de desvanecimiento suave
        
        Propósito: Proporcionar feedback visual atractivo al usuario
        Animación: Efecto fade-in de 0.8 segundos con curva suave
        UX: Mejora la experiencia visual de la aplicación
        Timing: Activado solo después de conexión exitosa
        """
        
        # --- HACER VISIBLE EL GRUPO DE SENSORES ---
        self.sensors_group.setVisible(True)      # Mostrar contenedor de sensores
        
        # --- CONFIGURAR EFECTO DE OPACIDAD ---
        self.fade_effect = QGraphicsOpacityEffect()  # Efecto de transparencia
        self.sensors_group.setGraphicsEffect(self.fade_effect)  # Aplicar al grupo
        
        # --- CREAR ANIMACIÓN DE APARICIÓN ---
        self.animation = QPropertyAnimation(self.fade_effect, b"opacity")  # Animar opacidad
        self.animation.setDuration(800)          # Duración: 800ms (0.8 segundos)
        self.animation.setStartValue(0.0)        # Inicio: Completamente transparente
        self.animation.setEndValue(1.0)          # Final: Completamente opaco
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)  # Curva suave
        
        # --- INICIAR ANIMACIÓN ---
        self.animation.start()                   # Ejecutar efecto de desvanecimiento

# ============================================================================
    # MÉTODO: DETENER TODOS LOS THREADS DE MONITOREO
    # ============================================================================
    def stop_all_monitoring_threads(self):
        """
        Detiene todos los threads de monitoreo activos de forma segura
        
        Propósito: Limpiar todos los recursos cuando se cambia de sensor o se cierra la aplicación
        Threads afectados: Ángulo simple, brazo robótico, IR, capacitivo, ultrasónico
        Seguridad: Verifica existencia y estado antes de detener cada thread
        Recursos: Libera memoria y conexiones TCP con ESP32
        """
        
        # --- DETENER THREAD DE ÁNGULO SIMPLE ---
        if hasattr(self, 'stop_angulo_monitoring'):
            self.stop_angulo_monitoring()

        

    # =====================================================================================
    # MÉTODO: REINICIO COMPLETO DE LA APLICACIÓN
    # =====================================================================================
    def restart_application(self):
        """
        Reinicia completamente la aplicación manteniendo la conexión ESP32
        
        Propósito: Limpiar toda la interfaz y datos como si acabara de conectar al ESP32
        Funcionamiento: Detiene todos los threads, limpia datos, reinicia la UI
        Conexión: Mantiene la conexión TCP con el ESP32 sin desconectarla
        Estado: Preserva el estado de conexión pero reinicia todo lo demás
        UI: Vuelve a la pantalla de bienvenida y resetea todos los controles
        """
        
        # --- VERIFICAR CONEXIÓN REQUERIDA ---
        if not self.is_connected:
            QMessageBox.warning(self, "Sin conexión", "No hay conexión ESP32 para reiniciar")
            return
        
        # --- CONFIRMAR REINICIO CON EL USUARIO ---
        reply = QMessageBox.question(self, "Confirmar Reinicio", 
                                   "¿Estás seguro de que quieres reiniciar la interfaz?\n\n"
                                   "Se mantendrá la conexión ESP32 pero se limpiarán todos los datos.",
                                   QMessageBox.Yes | QMessageBox.No,
                                   QMessageBox.No)
        
        if reply != QMessageBox.Yes:
            return  # Usuario canceló el reinicio
        
        # --- PASO 1: DETENER TODOS LOS THREADS ACTIVOS ---
        print("🔄 Iniciando reinicio - Deteniendo threads...")
        self.stop_all_monitoring_threads()      # Detener todos los sensores activos
        
        # --- PASO 2: LIMPIAR TODOS LOS DATOS DE SENSORES ---
        print("🧹 Limpiando datos de sensores...")
        self.clear_all_sensor_data()
        
        # --- PASO 3: RESETEAR ESTADO DE LA INTERFAZ ---
        print("🖥️ Reseteando interfaz de usuario...")
        self.reset_interface_state()
        
        # --- PASO 4: MOSTRAR PANTALLA DE BIENVENIDA ---
        print("🏠 Volviendo a pantalla de bienvenida...")
        self.show_welcome_screen()
        
        # --- CONFIRMACIÓN FINAL ---
        print("✅ Reinicio completado - Conexión ESP32 mantenida")
        QMessageBox.information(self, "Reinicio Completado", 
                              "La interfaz se ha reiniciado exitosamente.\n\n"
                              "La conexión ESP32 se mantiene activa.")

    # =====================================================================================
    # MÉTODO: LIMPIAR TODOS LOS DATOS DE SENSORES
    # =====================================================================================
    def clear_all_sensor_data(self):
        """
        Limpia todos los datos almacenados de todos los sensores
        
        Propósito: Borrar historial de lecturas y resetear gráficas
        Sensores: Ángulo simple, brazo robótico, IR, capacitivo, ultrasónico
        Memoria: Libera listas de datos para optimizar memoria
        """
        
        # --- LIMPIAR DATOS DE ÁNGULO SIMPLE ---
        # Limpiar datos y gráfica del sensor de ángulo simple usando método dedicado
        if hasattr(self, 'clear_graph_SIMPLE_ANGLE'):
            self.clear_graph_SIMPLE_ANGLE()
        

    # =====================================================================================
    # MÉTODO: RESETEAR ESTADO DE LA INTERFAZ
    # =====================================================================================
    def reset_interface_state(self):
        """
        Resetea todos los estados de la interfaz a valores iniciales
        
        Propósito: Volver botones y controles a estado original
        Estado: Mantiene conexión pero resetea flags de monitoreo
        UI: Restaura textos de botones y estilos originales
        """
        
        # --- RESETEAR FLAGS DE MONITOREO ---
        self.monitoreando_SIMPLE_ANGLE = False                       # Ángulo simple no monitoreando
        self.brazo_is_monitoring = False                 # Brazo no monitoreando
        self.distancia_ir_is_monitoring = False          # IR no monitoreando
        self.distancia_cap_is_monitoring = False         # Capacitivo no monitoreando
        self.distancia_ultra_is_monitoring = False       # Ultrasónico no monitoreando
        
        # --- RESETEAR DATOS PENDIENTES ---
        self.pending_updates = False
        self.pending_simple_data = None
        self.pending_brazo_data = None
        self.pending_distancia_ir_data = None
        self.pending_distancia_cap_data = None
        self.pending_distancia_ultra_data = None
        
        # --- RESETEAR BOTONES DE EXPORTACIÓN ---
        # Los botones de exportación se habilitarán automáticamente cuando haya datos nuevos
        
        print("🔧 Estado de interfaz reseteado completamente")

    # =====================================================================================
    # MÉTODO: MOSTRAR PANTALLA DE BIENVENIDA
    # =====================================================================================
    def show_welcome_screen(self):
        """
        Muestra la pantalla de bienvenida inicial
        
        Propósito: Volver al estado inicial como si acabara de conectar
        UI: Oculta detalles de sensores y muestra mensaje de bienvenida
        Estado: Mantiene lista de sensores visible pero sin selección
        """
        
        # --- MOSTRAR PANTALLA DE BIENVENIDA ---
        if hasattr(self, 'welcome_widget') and self.welcome_widget:
            self.welcome_widget.setVisible(True)     # Mostrar mensaje de bienvenida
        
        # --- OCULTAR DETALLES DE SENSORES ---
        if hasattr(self, 'sensor_details') and self.sensor_details:
            self.sensor_details.setVisible(False)   # Ocultar área de detalles
        
        # --- DESELECCIONAR ELEMENTOS DE LA LISTA ---
        if hasattr(self, 'sensors_list') and self.sensors_list:
            self.sensors_list.clearSelection()      # Quitar selección de sensores
        
        print("🏠 Pantalla de bienvenida mostrada")
