"""
ARCHIVO PRINCIPAL DE INTERFAZ GRÁFICA PARA SENSORACORE
Función: Define la ventana principal y todas las interfaces de los sensores
Propósito: Crear una aplicación desktop para monitoreo de sensores ESP32
"""
#Importando componentes necesarios
from PySide6.QtWidgets import *
from PySide6.QtUiTools import QUiLoader
from IMPORTACIONES import *  # Importar todo lo necesario desde el módulo de importaciones
#El modulo sys responsable de procesar los argumentos en las lineas de comandos
import sys

class ui(QMainWindow):
    def __init__(self):
        """
        Constructor de la ventana principal
        Inicializa todos los componentes de la interfaz y variables de estado
        """
        super().__init__()
        # Crear una barra de carga simple
        splash = QSplashScreen()
        splash.setPixmap(QPixmap("SensoraCore/SC_DesktopApp/Assets/loading.png"))
        splash.show()
        
        progress_bar = QProgressBar(splash)
        progress_bar.setGeometry(10, splash.height() - 30, splash.width() - 20, 20)
        progress_bar.setRange(0, 100)
        progress_bar.setValue(0)
        progress_bar.setTextVisible(True)
        progress_bar.setStyleSheet("""
            QProgressBar {
            border: 2px solid #8f8f91;
            border-radius: 5px;
            text-align: center;
            }
            QProgressBar::chunk {
            background-color: #05B8CC;
            width: 20px;
            }
        """)
        
        for i in range(0, 101, 5):
            progress_bar.setValue(i)
            splash.showMessage(f"Cargando... {i}%", Qt.AlignHCenter | Qt.AlignBottom, Qt.black)
            QCoreApplication.processEvents()
            QThread.msleep(100)  # Simular carga
        
        splash.close()

        loader = QUiLoader() # Crear objeto de loader
        loaded_ui = loader.load("SensoraCore/SC_DesktopApp/Main/mainWindow.ui") # Cargar el archivo .ui
        self.setCentralWidget(loaded_ui)
        self.setWindowTitle("SensoraCore") #Titulo de la ventana
        
        # Configurar el grupo de widgets para la lista de sensores
        self.listaSensores = self.findChild(QGroupBox, "list")
        self.listaSensores.setVisible(False)

        # Conectar el botón 'Conectar' a la función conectar
        btn = self.findChild(QPushButton, "Conectar")
        if btn:
            btn.clicked.connect(self.conectar)

    def conectar(self):
        """
        Prueba la conexión TCP/IP con el ESP32 usando la IP proporcionada en el campo ipEdit
        y actualiza la interfaz como en main_window.py.
        """
        # Obtener widgets de la interfaz
        ip = self.findChild(QLineEdit, "ipEdit")
        btn = self.findChild(QPushButton, "Conectar")
        status = self.findChild(QLabel, "Status")
        if ip is None or btn is None or status is None:
            QMessageBox.critical(self, "Error", "No se encontraron los widgets necesarios (ipEdit, Conectar, Status)")
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
            QMessageBox.information(self, "Conexión exitosa", f"Conectado a ESP32 en {esp32_ip}")
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
            QMessageBox.critical(self, "Fallo de conexión", f"No se pudo conectar a la IP: {esp32_ip} \n  Respuesta de log: \n {response}")

    def sensorSeleccionado(self):
        """
        Maneja la selección de un sensor en la interfaz.
        """
        # Obtener el sensor seleccionado
        sensor = self.findChild(QComboBox, "simpleAngleBT")
        if sensor is None:
            return
        sensor_id = sensor.currentData()
        if sensor_id is None:
            return
        # Ocultar el widget de bienvenida si existe
        welcome_widget = self.findChild(QWidget, "Welcome")
        if welcome_widget:
            welcome_widget.setVisible(False)
        # Realizar acción con el sensor seleccionado
        print(f"Sensor seleccionado: {sensor_id}")


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

























if __name__ == "__main__":
    app = QApplication(sys.argv) # Crear una aplicación Qt
    window = ui()
    window.show() # Mostrar la ventana
    app.exec() # Ejecutar el bucle de eventos