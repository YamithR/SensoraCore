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
    Sensores: 3 potenciómetros (GPIO 32, 33, 25) + sensor capacitivo (GPIO 4)
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
    tittle = QLabel("🦾 Sensor de Brazo Ángulo")
    title.setStyleSheet
    ("""
        font-size: 20px;                    /* Tamaño grande para destacar */
        font-weight: bold;                  /* Negrita para jerarquía visual */
        color: #007bff;                     /* Azul corporativo */
        margin-bottom: 10px;                /* Separación inferior */
    """)
    
    # --- ASEGURAR stackedWidget EXISTE ---
    if not hasattr(self, "stackedWidget"):
        self.stackedWidget = QStackedWidget(self)
        # Si tienes un layout principal, agrégalo allí, por ejemplo:
        # self.setCentralWidget(self.stackedWidget)
    # --- CREAR WIDGET PRINCIPAL ---
    self.anglearm_widget = QWidget()
    layout = QVBoxLayout(self.anglearm_widget)

    # --- TÍTULO ---
    title = QLabel("Simulación Brazo de 3 Grados de Libertad")
    title.setAlignment(Qt.AlignCenter)
    title.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
    layout.addWidget(title)

    # --- SIMULADOR DE BRAZO ---
    class ArmSimulator(QWidget):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.setMinimumSize(400, 400)
            self.angles = [0, 0, 0]  # [base, codo, muñeca]
            self.lengths = [100, 80, 60]  # Longitud de cada segmento

        def set_angles(self, angles):
            self.angles = angles
            self.update()

        def paintEvent(self, event):
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)
            w, h = self.width(), self.height()
            center = QPointF(w/2, h*0.8)
            angle0 = np.deg2rad(self.angles[0])
            angle1 = np.deg2rad(self.angles[1])
            angle2 = np.deg2rad(self.angles[2])

            # Primer segmento (base)
            x1 = center.x() + self.lengths[0]*np.cos(np.pi/2 - angle0)
            y1 = center.y() - self.lengths[0]*np.sin(np.pi/2 - angle0)
            p1 = QPointF(x1, y1)
            painter.setPen(QPen(Qt.blue, 8))
            painter.drawLine(center, p1)

            # Segundo segmento (codo)
            x2 = x1 + self.lengths[1]*np.cos(np.pi/2 - (angle0 + angle1))
            y2 = y1 - self.lengths[1]*np.sin(np.pi/2 - (angle0 + angle1))
            p2 = QPointF(x2, y2)
            painter.setPen(QPen(Qt.green, 8))
            painter.drawLine(p1, p2)

            # Tercer segmento (muñeca)
            x3 = x2 + self.lengths[2]*np.cos(np.pi/2 - (angle0 + angle1 + angle2))
            y3 = y2 - self.lengths[2]*np.sin(np.pi/2 - (angle0 + angle1 + angle2))
            p3 = QPointF(x3, y3)
            painter.setPen(QPen(Qt.red, 8))
            painter.drawLine(p2, p3)

            # Dibujar articulaciones
            for pt in [center, p1, p2, p3]:
                painter.setBrush(Qt.black)
                painter.drawEllipse(pt, 7, 7)

    self.arm_simulator = ArmSimulator()
    layout.addWidget(self.arm_simulator, stretch=1)

    # --- SLIDERS PARA CONTROLAR LOS ÁNGULOS ---
    sliders_layout = QHBoxLayout()
    self.sliders = []
    for i, color in enumerate(["Base (Azul)", "Codo (Verde)", "Muñeca (Rojo)"]):
        vbox = QVBoxLayout()
        label = QLabel(color)
        slider = QSlider(Qt.Vertical)
        slider.setMinimum(-135)
        slider.setMaximum(135)
        slider.setValue(0)
        slider.setTickInterval(15)
        slider.setTickPosition(QSlider.TicksBothSides)
        vbox.addWidget(label, alignment=Qt.AlignCenter)
        vbox.addWidget(slider)
        sliders_layout.addLayout(vbox)
        self.sliders.append(slider)
    layout.addLayout(sliders_layout)

    # --- ACTUALIZAR SIMULADOR AL MOVER SLIDERS ---
    def update_simulator():
        angles = [slider.value() for slider in self.sliders]
        self.arm_simulator.set_angles(angles)
    for slider in self.sliders:
        slider.valueChanged.connect(update_simulator)
    update_simulator()

    # --- AGREGAR AL STACK PRINCIPAL ---
    self.stackedWidget.addWidget(self.anglearm_widget)
    self.stackedWidget.setCurrentWidget(self.anglearm_widget)

















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
class BrazoAnguloMonitor(QThread):
    """
    Hilo para monitorear el sensor de brazo de ángulos
    Propósito: Leer datos del sensor y emitirlos a la interfaz
    Funcionalidad: 
        - Leer valores analógicos del potenciómetro
        - Emitir valores leídos a la interfaz gráfica
        - Manejar reconexiones automáticas
    """
    data_received = Signal(float, float, float)  # Señal de datos leídos
    def __init__(self, esp32_ip, port=8080):
        """
        Constructor del hilo para sensor de ángulo simple
        Parámetros:
        - esp32_ip: Dirección IP del ESP32 (ej: "192.168.1.100")
        - port: Puerto de comunicación TCP (por defecto 8080)
        """
        super().__init__()
        self.running = True  # Controla el ciclo de lectura
        self.sensor = None  # Aquí se inicializará el sensor
    def run(self):
        """
        Método principal del hilo que se ejecuta en segundo plano
        Encargado de leer datos del sensor y emitirlos a la interfaz
        """
    def stop(self):
        """        Detiene el hilo de monitoreo        """
        self.running = False
        self.wait()
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
        self.pot1_value = []       # Lista para almacenar valores del potenciómetro 1
        self.pot2_value = []       # Lista para almacenar valores del potenciómetro 2
        self.pot3_value = []       # Lista para almacenar valores del potenciómetro 3
        self.lectura_pot1 = []     # Lista para almacenar la lectura ADC del potenciómetro 1
        self.lectura_pot2 = []     # Lista para almacenar la lectura ADC del potenciómetro 2
        self.lectura_pot3 = []     # Lista para almacenar la lectura ADC del potenciómetro 3
        self.max_points = 100      # Número máximo de puntos a almacenar
        # SISTEMA DE ACTUALIZACIONES
        self.thread_AngleArm = None             # Hilo para monitorear el sensor de brazo de ángulos
        self.monietoreando_AngleArm = False     # Indica si se está monitoreando el sensor
        self.pending_updates = False            # Indica si hay actualizaciones pendientes
        self.pending_AngleArm_data =None        # Datos pendientes de actualización
        # -- Configuracion de timer --
        self.timer = QTimer()                   # Timer para actualizaciones periódicas de gráfica
        self.timer.timerout.connect(self.on_timer_update_graph)
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
        Inicia el monitoreo del sensor de brazo de ángulos
        
        Propósito: Configurar y arrancar el hilo de monitoreo
        Lógica: Crea hilo, conecta señales y arranca el monitoreo
        UI: Actualiza botón de control y estado visual
        Estado: Cambia flag self.monitoreando_SIMPLE_ANGLE a True
        """
    # MÉTODO: DETENER MONITOREO DEL SENSOR DE BRAZO DE ÁNGULOS
    def stop_angleArm_monitoring(self):
        """
        Detiene el monitoreo del sensor de brazo de ángulos
        
        Propósito: Finalizar el hilo de monitoreo y limpiar estado
        Lógica: Detiene hilo, limpia datos y actualiza UI
        UI: Actualiza botón de control y estado visual
        Estado: Cambia flag self.monitoreando_SIMPLE_ANGLE a False
        """
    # MÉTODO: ACTUALIZAR DATOS DE LOS SENSORES DE BRAZO DE ÁNGULOS
    def update_angleArm_data(self, pot1_ADC, pot1_angulo, pot2_ADC, pot2_angulo, pot3_ADC, pot3_angulo):
        """
        Actualiza los datos de los sensores de brazo de ángulos
        
        Propósito: Almacenar las lecturas actuales de los sensores
        Lógica: Añade nuevos valores a las listas y mantiene el tamaño máximo
        UI: Actualiza visualización en tiempo real
        Estado: No cambia flags, solo actualiza datos
        """
        # -- ALMACENAR DATOS EN HISTORIAL --
        self.lectura_pot1.append(pot1_ADC)
        self.lectura_pot2.append(pot2_ADC)
        self.lectura_pot3.append(pot3_ADC)
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
        # Implementar lógica para limpiar la gráfica del sensor de brazo de ángulos
        pass
    # MÉRODO: EXPORTAR DATOS A EXCEL
    def export_to_excel(self, filepath: str):
        """
        Exporta todos los datos de los sensores a archivo Excel
        
        Propósito: Permitir análisis posterior y respaldo de datos
        Formato: Archivo .xlsx con múltiples columnas y gráfica integrada
        Datos: Lecturas ADC, ángulos calculados, timestamps, numeración
        Gráfica: Incluye gráfico de líneas dentro del archivo Excel
        Validación: Verifica que existan datos antes de exportar
        """
    # MÉTODO: ACTUALIZACIÓN DE GRÁFICAS
    def update_graph_display(self):
        """
        Actualiza la visualización de la gráfica del sensor de brazo de ángulos
        
        Propósito: Refrescar la gráfica con los últimos datos
        Lógica: Verifica si hay datos y actualiza el gráfico
        UI: Muestra los valores actuales en tiempo real
        Estado: No cambia flags, solo actualiza visualización
        """
        # Implementar lógica para actualizar la gráfica del sensor de brazo de ángulos
        pass
    # TIMER DE ACTUALIZACIÓN GRÁFICA
    def on_timer_update_graph(self):
        """
        Método llamado periódicamente por el timer para actualizar la gráfica si hay datos nuevos.
        """
        self.update_graph_display()
