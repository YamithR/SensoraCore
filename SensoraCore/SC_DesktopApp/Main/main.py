"""
ARCHIVO PRINCIPAL DE INTERFAZ GRÁFICA PARA SENSORACORE
Función: Define la ventana principal y todas las interfaces de los sensores
Propósito: Crear una aplicación desktop para monitoreo de sensores ESP32
"""
#Importando componentes necesarios
import sys
import os
# Agregar el directorio padre al path para poder importar módulos
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
#from PySide6.QtWidgets import *
from Modules.simpleAngle.simpleAngle_logic import SimpleAngleLogic
from IMPORTACIONES import *  # Importar todo lo necesario desde el módulo de importaciones
#El modulo sys responsable de procesar los argumentos en las lineas de comandos


class LoadingSplashScreen(QSplashScreen):
    """
    Pantalla de carga con barra de progreso.
    """
    def __init__(self):
        super().__init__()
        self.setWindowFlag(Qt.FramelessWindowHint)  # Sin bordes
        self.setWindowFlag(Qt.WindowStaysOnTopHint)  # Siempre encima
        self.setWindowFlag(Qt.SubWindow)  # Permitir mover la ventana
        self.setWindowTitle("Bienvenido a SensoraCore")
        self.setFixedSize(400, 100)  # Tamaño de la pantalla de carga
        self.setStyleSheet("background-color: white; border: 2px solid gray;")
        self.progress = 0  # Progreso inicial
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_progress)
        self.timer.start(50)  # Actualizar cada 50 ms

    def update_progress(self):
        """
        Actualiza el progreso de la barra y redibuja la pantalla.
        """
        self.progress += 1  # Incrementar el progreso
        if self.progress > 100:
            self.timer.stop()  # Detener el temporizador cuando llegue al 100%
        self.update()  # Redibujar la pantalla

    def paintEvent(self, event):
        """
        Dibuja la barra de progreso en la pantalla de carga.
        """
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Dibujar fondo
        painter.setBrush(QColor(240, 240, 240))
        painter.drawRect(self.rect())

        # Dibujar barra de progreso
        bar_width = int(self.width() * (self.progress / 100))
        painter.setBrush(QColor(100, 180, 255))
        painter.drawRect(0, self.height() - 30, bar_width, 30)

        # Dibujar texto
        painter.setPen(Qt.black)
        painter.setFont(QFont("Arial", 12, QFont.Bold))
        painter.drawText(self.rect(), Qt.AlignCenter, f"Bienvenido a SensoraCore... {self.progress}%")

        painter.end()

    def mousePressEvent(self, event):
        """
        Permite mover la ventana al hacer clic y arrastrar.
        """
        if event.button() == Qt.LeftButton:
            self.drag_position = self.mapToGlobal(event.position().toPoint()) - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        """
        Actualiza la posición de la ventana mientras se arrastra.
        """
        if event.buttons() == Qt.LeftButton:
            self.move(self.mapToGlobal(event.position().toPoint()) - self.drag_position)
            event.accept()


###
class ui(QMainWindow):
    def __init__(self):
        """
        Constructor de la ventana principal
        Inicializa todos los componentes de la interfaz y variables de estado
        """
        super().__init__()
  
        app = QApplication.instance()
        if app:
            app.processEvents()
        loader = QUiLoader() # Crear objeto de loader
        loaded_ui = loader.load("SensoraCore/SC_DesktopApp/Main/mainWindow.ui") # Cargar el archivo .ui
        self.setCentralWidget(loaded_ui)
        self.setWindowTitle("SensoraCore") #Titulo de la ventana
        # Configuracion de widgets de modulos
        self.simpleAngleUi = loader.load("SensoraCore/SC_DesktopApp/Modules/simpleAngle/simpleAngle.ui")
        self.angleArmUi = loader.load("SensoraCore/SC_DesktopApp/Modules/angleArm/angleArm.ui")
        self.infraredUi = loader.load("SensoraCore/SC_DesktopApp/Modules/infrared/infrared.ui")
        self.capasitiveUi = loader.load("SensoraCore/SC_DesktopApp/Modules/capasitive/capasitive.ui")
        self.ultrasonicUi = loader.load("SensoraCore/SC_DesktopApp/Modules/ultrasonic/ultrasonic.ui")
        self.opticalSpeedUi = loader.load("SensoraCore/SC_DesktopApp/Modules/opticalSpeed/opticalSpeed.ui")
        self.irSteeringUi = loader.load("SensoraCore/SC_DesktopApp/Modules/irSteering/irSteering.ui")
        self.thermoregulationUi = loader.load("SensoraCore/SC_DesktopApp/Modules/thermoregulation/thermoregulation.ui")
        self.gasRegulationUi = loader.load("SensoraCore/SC_DesktopApp/Modules/gasRegulation/gasRegulation.ui")
        self.brightnessUi = loader.load("SensoraCore/SC_DesktopApp/Modules/brightness/brightness.ui")
        self.colorCNYUi = loader.load("SensoraCore/SC_DesktopApp/Modules/colorCNY/colorCNY.ui")
        self.colorTCSUi = loader.load("SensoraCore/SC_DesktopApp/Modules/colorTCS/colorTCS.ui")
        
        
        # Configurar el grupo de widgets para la lista de sensores
        self.listaSensores = self.findChild(QGroupBox, "list")
        self.listaSensores.setVisible(False)

        # Conectar el botón 'Conectar' a la función conectar
        btn = self.findChild(QPushButton, "Conectar")
        if btn:
            btn.clicked.connect(self.conectar)

        # Conectar el QPushButton 'Terminal' para abrir/cerrar la ventana de log
        terminal_button = self.findChild(QPushButton, "Terminal")
        if terminal_button:
            terminal_button.clicked.connect(self.toggle_ventana_log)

        # Inicializar la ventana de log como None
        self.log_window = None

        #Inicializar boton de reinicio
        reset_btn = self.findChild(QPushButton, "resetBT")
        if reset_btn:
            reset_btn.clicked.connect(self.reset)




        # Definir los nombres de los botones de sensores y sus atributos
        sensor_button_info = [
            ("simple_angle_btn", "simpleAngleBT"),
            ("angle_arm_btn", "angleArmBT"),
            ("infrared_btn", "infraredBT"),
            ("capasitive_btn", "capasitiveBT"),
            ("ultrasonic_btn", "ultrasonicBT"),
            ("optical_speed_btn", "OpticalSpeedBT"),
            ("ir_steering_btn", "irSteeringBT"),
            ("thermoregulation_btn", "thermoregulationBT"),
            ("gas_regulation_btn", "gasRegulationBT"),
            ("brightness_btn", "brightnessBT"),
            ("color_cny_btn", "colorCNYBT"),
            ("color_tcs_btn", "colorTCSBT"),
        ]

        # Recorrer la lista y asignar los atributos dinámicamente
        for attr_name, btn_name in sensor_button_info:
            setattr(self, attr_name, self.findChild(QPushButton, btn_name))
        # Mapeo de botones a sus IDs de sensor
        sensor_buttons_map = {
            self.simple_angle_btn: "simpleAngle",
            self.angle_arm_btn: "angleArm",
            self.infrared_btn: "infrared",
            self.capasitive_btn: "capasitive",
            self.ultrasonic_btn: "ultrasonic",
            self.optical_speed_btn: "opticalSpeed",
            self.ir_steering_btn: "irSteering",
            self.thermoregulation_btn: "thermoregulation",
            self.gas_regulation_btn: "gasRegulation",
            self.brightness_btn: "brightness",
            self.color_cny_btn: "colorCNY",
            self.color_tcs_btn: "colorTCS"
        }
        for btn, sensor_id in sensor_buttons_map.items():
            if btn:
                btn.clicked.connect(lambda _, sid=sensor_id: self.sensorSeleccionado(sid))

        # Definir el widget de bienvenida
        self.welcome_widget = self.findChild(QWidget, "Welcome")

    def toggle_ventana_log(self):
        """
        Abre o cierra la ventana de log al presionar el botón 'terminal'.
        """
        if self.log_window and self.log_window.isVisible():
            self.log_window.close()
            self.log_window = None
        else:
            self.abrir_ventana_log()

    def reset(self):
        """
        Reinicia la conexión y la interfaz.
        """
        self.listaSensores.setVisible(False)
        btn = self.findChild(QPushButton, "Conectar")
        if btn:
            btn.setEnabled(True)
        status = self.findChild(QLabel, "Status")
        if status:
            status.setText("🔴Desconectado")
            status.setStyleSheet("""
                padding: 8px;
                border-radius: 4px;
                background-color: #f8d7da;
                color: #721c24;
                font-size: 18px;
                font-weight: bold;
                qproperty-alignment: 'AlignCenter';
            """)

        # Si hay widgets de sensores abiertos, cerrarlos
        sensor_ui = self.findChild(QWidget, "SensorUI")
        if sensor_ui:
            layout = sensor_ui.layout()
            if layout is not None:
                while layout.count():
                    child = layout.takeAt(0)
                    if child.widget():
                        child.widget().setParent(None)

        # Verificar si el widget de bienvenida sigue siendo válido
        welcome_widget_valid = False
        try:
            # Intentar acceder al widget de bienvenida de forma segura
            if self.welcome_widget is not None and self.welcome_widget.isVisible():
                welcome_widget_valid = True
        except RuntimeError:
            # El widget ha sido eliminado, necesitamos recrearlo
            print("Widget de bienvenida eliminado, recreando...")
            self.welcome_widget = None
        
        if not welcome_widget_valid:
            print("Recreando el widget de bienvenida...")
            if sensor_ui:
                self.welcome_widget = QWidget(sensor_ui)
                self.welcome_widget.setObjectName("Welcome")

        # Volver a hacer visible la ventana de "welcome"
        if sensor_ui and self.welcome_widget:
            layout = sensor_ui.layout()
            if layout is not None:
                self.welcome_widget.setParent(sensor_ui)
                layout.addWidget(self.welcome_widget)
                self.welcome_widget.setVisible(True)
        
        print("Interfaz reiniciada. Listo para una nueva conexión.")

    def conectar(self):
        """
        Prueba la conexión TCP/IP con el ESP32 usando la IP proporcionada en el campo ipEdit
        y actualiza la interfaz como en main_window.py.
        """
        # Obtener widgets de la interfaz
        ip = self.findChild(QLineEdit, "ipEdit")
        btn = self.findChild(QPushButton, "Conectar")
        status = self.findChild(QLabel, "Status")
        ###<---------DEFINICION DE BOTONES DE SENSORES--------->###
        sensor_buttons = [
            self.simple_angle_btn,
            self.angle_arm_btn,
            self.infrared_btn,
            self.capasitive_btn,
            self.ultrasonic_btn,
            self.optical_speed_btn,
            self.ir_steering_btn,
            self.thermoregulation_btn,
            self.gas_regulation_btn,
            self.brightness_btn,
            self.color_cny_btn,
            self.color_tcs_btn
        ]
        if ip is None or btn is None or status is None or any(b is None for b in sensor_buttons):
            QMessageBox.critical(self, "Error", "No se encontraron los widgets necesarios (ipEdit, Conectar, Status, Sensores)")
            return

        esp32_ip = ip.text().strip()
        if not esp32_ip:
            QMessageBox.warning(self, "Advertencia", "Por favor ingrese la IP del ESP32.")
            return

        # Deshabilitar botón y mostrar estado de conexión en progreso
        btn.setEnabled(False)
        status.setText("🔄 Conectando...")
        status.setStyleSheet("""
            padding: 8px;
            border-radius: 4px;
            background-color: #cce5ff;
            color: #004085;
            font-size: 18px;
            font-weight: bold;
        """)
        self.repaint()

        # Crear cliente y probar conexión
        client = ESP32Client(esp32_ip)
        response = client.led_on()
        if response == "LED_ON_OK":
            status.setText("✅ Conectado al ESP32")
            status.setStyleSheet("""
                padding: 8px;
                border-radius: 4px;
                background-color: #d4edda;
                color: #155724;
                font-size: 18px;
                font-weight: bold;
            """)
            btn.setEnabled(False)
            self.listaSensores.setVisible(True)
            # Habilitar botones de sensores
            for sensor_button in sensor_buttons:
                sensor_button.setEnabled(True)

            QMessageBox.information(self, "Conexión exitosa", f"Conectado a ESP32 en {esp32_ip}")
            print(f"Conexión exitosa: {esp32_ip}")
            print("Sensor UI habilitada.")
            print("Botones de sensores habilitados.")
            print("Interfaz lista para uso.")
            print("Ya puede seleccionar un sensor.")
        else:
            status.setText("❌ Error de conexión")
            status.setStyleSheet("""
                padding: 8px;
                border-radius: 4px;
                background-color: #f8d7da;
                color: #721c24;
                font-size: 18px;
                font-weight: bold;
            """)
            btn.setEnabled(True)

            # Deshabilitar botones de sensores
            for sensor_button in sensor_buttons:
                sensor_button.setEnabled(False)

            QMessageBox.critical(self, "Fallo de conexión", f"No se pudo conectar a la IP: {esp32_ip} \n  Respuesta de log: \n {response}")
            print(f"Error de conexión: {response} \n No se pudo conectar al ESP32 en la IP: {esp32_ip} \n Verifique la IP y el estado del dispositivo.")

    def abrir_ventana_log(self):
        """
        Abre una ventana de log para mostrar todos los prints y mensajes de depuración.
        """
        self.log_window = QMainWindow(self)
        self.log_window.setWindowTitle("Log de Depuración")
        self.log_window.setGeometry(100, 100, 600, 400)

        # Crear un widget de texto para mostrar el log
        self.log_text_edit = QTextEdit(self.log_window)
        self.log_text_edit.setReadOnly(True)
        self.log_text_edit.setStyleSheet("background-color: black; color: white; font-family: Consolas; font-size: 12px;")

        # Establecer el widget de texto como el central de la ventana
        self.log_window.setCentralWidget(self.log_text_edit)
        self.log_window.show()

        # Redirigir la salida estándar y de error a la ventana de log
        sys.stdout = EmittingStream(self.log_text_edit)
        sys.stderr = EmittingStream(self.log_text_edit)

    def sensorSeleccionado(self, sensor_id):
        """
        Maneja la selección de un sensor en la interfaz.
        """
        try:
            print(f"Intentando seleccionar el sensor: {sensor_id}")

            # Ocultar el widget de bienvenida si existe
            welcome_widget = self.findChild(QWidget, "Welcome")
            try:
                if welcome_widget and welcome_widget.isVisible():
                    welcome_widget.setVisible(False)
            except RuntimeError:
                # Widget ha sido eliminado, continuar
                print("Widget de bienvenida ya eliminado.")
                pass

            # Buscar el contenedor donde se muestran los widgets de sensores
            sensor_ui = self.findChild(QWidget, "SensorUI")
            if not sensor_ui:
                print("Error: No se encontró el contenedor SensorUI.")
                return

            # Verificar si el contenedor tiene un layout, si no, asignar uno
            layout = sensor_ui.layout()
            if layout is None:
                print("El contenedor SensorUI no tiene un layout. Asignando uno nuevo.")
                layout = QVBoxLayout()
                sensor_ui.setLayout(layout)

            # Eliminar widgets existentes en el contenedor
            while layout.count():
                child = layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()

            # Cargar el widget correspondiente al sensor seleccionado
            if sensor_id == "simpleAngle":
                print("Cargando lógica para el sensor simpleAngle.")
                # Usar directamente la lógica de SimpleAngleLogic como widget
                simple_angle_logic = SimpleAngleLogic(self.simpleAngleUi)
                layout.addWidget(self.simpleAngleUi)  # Agregar el widget de la interfaz directamente
                print("SimpleAngleLogic integrado en el layout correctamente.")

            print(f"Sensor {sensor_id} seleccionado correctamente.")
        except Exception as e:
            print(f"Error al seleccionar el sensor {sensor_id}: {e}")

        # Buscar el contenedor donde se muestran los widgets de sensores
        sensor_ui = self.findChild(QWidget, "SensorUI")
        if sensor_ui:
            layout = sensor_ui.layout()
            if layout is not None:
            # Eliminar widgets existentes
                while layout.count():
                    child = layout.takeAt(0)
                    if child.widget():
                        child.widget().setParent(None)

                # Diccionario de widgets de sensores
                sensor_widgets = {
                "simpleAngle": self.simpleAngleUi,
                "angleArm": self.angleArmUi,
                "infrared": self.infraredUi,
                "capasitive": self.capasitiveUi,
                "ultrasonic": self.ultrasonicUi,
                "opticalSpeed": self.opticalSpeedUi,
                "irSteering": self.irSteeringUi,
                "thermoregulation": self.thermoregulationUi,
                "gasRegulation": self.gasRegulationUi,
                "brightness": self.brightnessUi,
                "colorCNY": self.colorCNYUi,
                "colorTCS": self.colorTCSUi,
                }

                # Obtener el widget correspondiente al sensor seleccionado
                widget = sensor_widgets.get(sensor_id)
                if widget is not None and layout is not None:
                    widget.setParent(sensor_ui)
                    layout.addWidget(widget)
                    widget.setVisible(True)






###
class ESP32Client:
    """
    Clase controladora para la coneccion por wifi con el microcontrolador ESP32
    Puerto predeterminado : 8080
    """
    def __init__(self, esp32_ip, port=8080):
        self.esp32_ip = esp32_ip
        self.port = port

    def send_command(self, command):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(3)
                s.connect((self.esp32_ip, self.port))
                s.sendall(command.encode())
                data = s.recv(1024)
                return data.decode()
        except Exception as e:
            return f"ERROR: {e}"

    def led_on(self):
        return self.send_command('LED_ON')

    def led_off(self):
        return self.send_command('LED_OFF')
    

###
class EmittingStream:
    """
    Clase para redirigir la salida estándar y de error a un QTextEdit.
    """
    def __init__(self, text_edit):
        self.text_edit = text_edit

    def write(self, text):
        self.text_edit.append(text)

    def flush(self):
        pass


###
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Crear la pantalla de carga
    splash = LoadingSplashScreen()
    splash.show()

    for _ in range(100):
        time.sleep(0.05) 
        app.processEvents() 

    # Cargar la ventana principal
    window = ui()
    splash.close()  # Cerrar la pantalla de carga
    window.show()

    app.exec()