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
from Modules.angleArm.angleArm_logic import AngleArmLogic
from Modules.infrared.infrared_logic import InfraredLogic
from Modules.capasitive.capasitive_logic import CapasitiveLogic
from Modules.ultrasonic.ultrasonic_logic import UltrasonicLogic
from Modules.opticalSpeed.opticalSpeed_logic import OpticalSpeedLogic
from Modules.irSteering.irSteering_logic import IrSteeringLogic
from Modules.thermoregulation.thermoregulation_logic import ThermoregulationLogic
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

    def closeEvent(self, event):
        """
        Maneja el evento de cierre de la aplicación principal.
        Detiene todos los procesos activos antes de cerrar.
        """
        print("Cerrando aplicación principal...")
        
        # Detener todos los procesos activos
        self._cleanup_active_sensors()
        
        # Cerrar ventana de log si está abierta
        if hasattr(self, 'log_window') and self.log_window:
            try:
                if self.log_window.isVisible():
                    self.log_window.close()
                # Restaurar stdout y stderr
                sys.stdout = sys.__stdout__
                sys.stderr = sys.__stderr__
            except:
                pass
        
        print("Aplicación cerrada correctamente.")
        event.accept()

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
        Reinicia la conexión y la interfaz completamente.
        Vuelve al estado inicial antes de la conexión con el ESP32.
        Detiene cualquier proceso activo con el ESP32.
        """
        print("Iniciando reset completo de la interfaz...")
        
        # PASO 1: Detener todos los procesos activos con el ESP32
        self._cleanup_active_sensors()
        
        # PASO 2: Cerrar ventana de log si está abierta
        if hasattr(self, 'log_window') and self.log_window:
            try:
                if self.log_window.isVisible():
                    self.log_window.close()
                self.log_window = None
                # Restaurar stdout y stderr
                sys.stdout = sys.__stdout__
                sys.stderr = sys.__stderr__
                print("Ventana de log cerrada y streams restaurados.")
            except RuntimeError:
                pass
        
        # PASO 3: Ocultar lista de sensores
        self.listaSensores.setVisible(False)
        
        # PASO 4: Habilitar botón conectar
        btn = self.findChild(QPushButton, "Conectar")
        if btn:
            btn.setEnabled(True)
            
        # PASO 5: Actualizar status a desconectado
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

        # PASO 6: Deshabilitar todos los botones de sensores
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
        
        for sensor_button in sensor_buttons:
            if sensor_button:
                sensor_button.setEnabled(False)

        # PASO 7: Limpiar completamente el área de sensores
        sensor_ui = self.findChild(QWidget, "SensorUI")
        if sensor_ui:
            # Eliminar el layout actual y todos sus widgets
            layout = sensor_ui.layout()
            if layout is not None:
                while layout.count():
                    child = layout.takeAt(0)
                    if child.widget():
                        child.widget().deleteLater()  # Usar deleteLater() para eliminar correctamente
                layout.deleteLater()
            
            # Crear un nuevo layout limpio
            new_layout = QVBoxLayout()
            sensor_ui.setLayout(new_layout)

        # PASO 8: Recrear todos los widgets de sensores desde cero
        self._recreate_sensor_widgets()

        # PASO 9: Recrear el widget de bienvenida
        if sensor_ui:
            self.welcome_widget = QWidget(sensor_ui)
            self.welcome_widget.setObjectName("Welcome")
            layout = sensor_ui.layout()
            if layout:
                layout.addWidget(self.welcome_widget)
                self.welcome_widget.setVisible(True)
        
        print("Reset completo terminado. Todos los procesos ESP32 detenidos. Interfaz lista para nueva conexión.")

    def _recreate_sensor_widgets(self):
        """
        Recrea todos los widgets de sensores desde cero para evitar problemas con widgets eliminados.
        """
        try:
            print("Recreando widgets de sensores...")
            
            # Limpiar instancias de lógica existentes usando la función de limpieza
            self._cleanup_active_sensors()
            
            loader = QUiLoader()
            
            # Recrear todos los widgets de sensores
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
            
            print("Widgets de sensores recreados exitosamente.")
        except Exception as e:
            print(f"Error al recrear widgets de sensores: {e}")

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
        Detiene cualquier proceso activo antes de cambiar de sensor.
        """
        try:
            print(f"Cambiando a sensor: {sensor_id}")
            
            # PASO 1: Detener cualquier proceso activo del sensor anterior
            self._cleanup_active_sensors()

            # Ocultar el widget de bienvenida si existe
            try:
                if hasattr(self, 'welcome_widget') and self.welcome_widget is not None:
                    if self.welcome_widget.isVisible():
                        self.welcome_widget.setVisible(False)
            except RuntimeError:
                # Widget ha sido eliminado, continuar
                pass

            # Buscar el contenedor donde se muestran los widgets de sensores
            sensor_ui = self.findChild(QWidget, "SensorUI")
            if not sensor_ui:
                print("Error: No se encontró el contenedor SensorUI.")
                return

            # Verificar si el contenedor tiene un layout, si no, asignar uno
            layout = sensor_ui.layout()
            if layout is None:
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
                try:
                    # Limpiar instancia anterior si existe
                    if hasattr(self, 'current_simple_angle_logic'):
                        try:
                            self.current_simple_angle_logic.cleanup()
                        except:
                            pass
                        self.current_simple_angle_logic = None
                    
                    # Recrear el widget UI si no está disponible o es inválido
                    if not hasattr(self, 'simpleAngleUi') or self.simpleAngleUi is None:
                        loader = QUiLoader()
                        self.simpleAngleUi = loader.load("SensoraCore/SC_DesktopApp/Modules/simpleAngle/simpleAngle.ui")
                    
                    # Verificar que el widget UI existe y es válido
                    try:
                        # Test básico para verificar que el widget es válido
                        _ = self.simpleAngleUi.objectName()
                    except RuntimeError:
                        loader = QUiLoader()
                        self.simpleAngleUi = loader.load("SensoraCore/SC_DesktopApp/Modules/simpleAngle/simpleAngle.ui")
                    
                    if self.simpleAngleUi is not None:
                        # Crear nueva instancia de la lógica pasando la referencia a main_window
                        self.current_simple_angle_logic = SimpleAngleLogic(self.simpleAngleUi, self)
                        
                        # Establecer el parent del widget UI al contenedor sensor_ui
                        self.simpleAngleUi.setParent(sensor_ui)
                        
                        # Agregar el widget al layout
                        layout.addWidget(self.simpleAngleUi)
                        
                    else:
                        print("Error: No se pudo crear o cargar simpleAngleUi.")
                        return
                        
                except Exception as e:
                    print(f"Error al cargar SimpleAngleLogic: {e}")
                    # Intentar recrear el widget como fallback
                    try:
                        print("Intentando recrear widget como fallback...")
                        loader = QUiLoader()
                        self.simpleAngleUi = loader.load("SensoraCore/SC_DesktopApp/Modules/simpleAngle/simpleAngle.ui")
                        if self.simpleAngleUi:
                            self.current_simple_angle_logic = SimpleAngleLogic(self.simpleAngleUi, self)
                            self.simpleAngleUi.setParent(sensor_ui)
                            layout.addWidget(self.simpleAngleUi)
                            print("Fallback exitoso.")
                        else:
                            print("Fallback falló.")
                            return
                    except Exception as fallback_error:
                        print(f"Error en fallback: {fallback_error}")
                        return

            elif sensor_id == "angleArm":
                print("Cargando lógica para el sensor angleArm.")
                try:
                    # Limpiar instancia anterior si existe
                    if hasattr(self, 'current_angle_arm_logic') and self.current_angle_arm_logic:
                        try:
                            self.current_angle_arm_logic.cleanup()
                        except:
                            pass
                        self.current_angle_arm_logic = None

                    # Recrear el widget UI si no está disponible o es inválido
                    if not hasattr(self, 'angleArmUi') or self.angleArmUi is None:
                        loader = QUiLoader()
                        self.angleArmUi = loader.load("SensoraCore/SC_DesktopApp/Modules/angleArm/angleArm.ui")

                    # Verificar que el widget UI existe y es válido
                    try:
                        _ = self.angleArmUi.objectName()
                    except RuntimeError:
                        loader = QUiLoader()
                        self.angleArmUi = loader.load("SensoraCore/SC_DesktopApp/Modules/angleArm/angleArm.ui")

                    if self.angleArmUi is not None:
                        # Crear instancia de lógica
                        self.current_angle_arm_logic = AngleArmLogic(self.angleArmUi, self)
                        # Establecer parent y agregar al layout
                        self.angleArmUi.setParent(sensor_ui)
                        layout.addWidget(self.angleArmUi)
                    else:
                        print("Error: No se pudo crear o cargar angleArmUi.")
                        return
                except Exception as e:
                    print(f"Error al cargar AngleArmLogic: {e}")
                    # Intentar recrear el widget como fallback
                    try:
                        print("Intentando recrear widget AngleArm como fallback...")
                        loader = QUiLoader()
                        self.angleArmUi = loader.load("SensoraCore/SC_DesktopApp/Modules/angleArm/angleArm.ui")
                        if self.angleArmUi:
                            self.current_angle_arm_logic = AngleArmLogic(self.angleArmUi, self)
                            self.angleArmUi.setParent(sensor_ui)
                            layout.addWidget(self.angleArmUi)
                            print("Fallback AngleArm exitoso.")
                        else:
                            print("Fallback AngleArm falló.")
                            return
                    except Exception as fallback_error:
                        print(f"Error en fallback AngleArm: {fallback_error}")
                        return

            elif sensor_id == "infrared":
                print("Cargando lógica para el sensor infrared.")
                try:
                    if hasattr(self, 'current_infrared_logic') and self.current_infrared_logic:
                        try:
                            self.current_infrared_logic.cleanup()
                        except:
                            pass
                        self.current_infrared_logic = None

                    if not hasattr(self, 'infraredUi') or self.infraredUi is None:
                        loader = QUiLoader()
                        self.infraredUi = loader.load("SensoraCore/SC_DesktopApp/Modules/infrared/infrared.ui")

                    try:
                        _ = self.infraredUi.objectName()
                    except RuntimeError:
                        loader = QUiLoader()
                        self.infraredUi = loader.load("SensoraCore/SC_DesktopApp/Modules/infrared/infrared.ui")

                    if self.infraredUi is not None:
                        self.current_infrared_logic = InfraredLogic(self.infraredUi, self)
                        self.infraredUi.setParent(sensor_ui)
                        layout.addWidget(self.infraredUi)
                    else:
                        print("Error: No se pudo crear o cargar infraredUi.")
                        return
                except Exception as e:
                    print(f"Error al cargar InfraredLogic: {e}")
                    try:
                        loader = QUiLoader()
                        self.infraredUi = loader.load("SensoraCore/SC_DesktopApp/Modules/infrared/infrared.ui")
                        if self.infraredUi:
                            self.current_infrared_logic = InfraredLogic(self.infraredUi, self)
                            self.infraredUi.setParent(sensor_ui)
                            layout.addWidget(self.infraredUi)
                        else:
                            print("Fallback infrared falló.")
                            return
                    except Exception as fallback_error:
                        print(f"Error en fallback infrared: {fallback_error}")
                        return

            elif sensor_id == "capasitive":
                print("Cargando lógica para el sensor capasitive.")
                try:
                    if hasattr(self, 'current_capasitive_logic') and self.current_capasitive_logic:
                        try:
                            self.current_capasitive_logic.cleanup()
                        except:
                            pass
                        self.current_capasitive_logic = None

                    if not hasattr(self, 'capasitiveUi') or self.capasitiveUi is None:
                        loader = QUiLoader()
                        self.capasitiveUi = loader.load("SensoraCore/SC_DesktopApp/Modules/capasitive/capasitive.ui")

                    try:
                        _ = self.capasitiveUi.objectName()
                    except RuntimeError:
                        loader = QUiLoader()
                        self.capasitiveUi = loader.load("SensoraCore/SC_DesktopApp/Modules/capasitive/capasitive.ui")

                    if self.capasitiveUi is not None:
                        self.current_capasitive_logic = CapasitiveLogic(self.capasitiveUi, self)
                        self.capasitiveUi.setParent(sensor_ui)
                        layout.addWidget(self.capasitiveUi)
                    else:
                        print("Error: No se pudo crear o cargar capasitiveUi.")
                        return
                except Exception as e:
                    print(f"Error al cargar CapasitiveLogic: {e}")
                    try:
                        loader = QUiLoader()
                        self.capasitiveUi = loader.load("SensoraCore/SC_DesktopApp/Modules/capasitive/capasitive.ui")
                        if self.capasitiveUi:
                            self.current_capasitive_logic = CapasitiveLogic(self.capasitiveUi, self)
                            self.capasitiveUi.setParent(sensor_ui)
                            layout.addWidget(self.capasitiveUi)
                        else:
                            print("Fallback capasitive falló.")
                            return
                    except Exception as fallback_error:
                        print(f"Error en fallback capasitive: {fallback_error}")
                        return

            elif sensor_id == "ultrasonic":
                print("Cargando lógica para el sensor ultrasonic.")
                try:
                    if hasattr(self, 'current_ultrasonic_logic') and self.current_ultrasonic_logic:
                        try:
                            self.current_ultrasonic_logic.cleanup()
                        except:
                            pass
                        self.current_ultrasonic_logic = None

                    if not hasattr(self, 'ultrasonicUi') or self.ultrasonicUi is None:
                        loader = QUiLoader()
                        self.ultrasonicUi = loader.load("SensoraCore/SC_DesktopApp/Modules/ultrasonic/ultrasonic.ui")

                    try:
                        _ = self.ultrasonicUi.objectName()
                    except RuntimeError:
                        loader = QUiLoader()
                        self.ultrasonicUi = loader.load("SensoraCore/SC_DesktopApp/Modules/ultrasonic/ultrasonic.ui")

                    if self.ultrasonicUi is not None:
                        self.current_ultrasonic_logic = UltrasonicLogic(self.ultrasonicUi, self)
                        self.ultrasonicUi.setParent(sensor_ui)
                        layout.addWidget(self.ultrasonicUi)
                    else:
                        print("Error: No se pudo crear o cargar ultrasonicUi.")
                        return
                except Exception as e:
                    print(f"Error al cargar UltrasonicLogic: {e}")
                    try:
                        loader = QUiLoader()
                        self.ultrasonicUi = loader.load("SensoraCore/SC_DesktopApp/Modules/ultrasonic/ultrasonic.ui")
                        if self.ultrasonicUi:
                            self.current_ultrasonic_logic = UltrasonicLogic(self.ultrasonicUi, self)
                            self.ultrasonicUi.setParent(sensor_ui)
                            layout.addWidget(self.ultrasonicUi)
                        else:
                            print("Fallback ultrasonic falló.")
                            return
                    except Exception as fallback_error:
                        print(f"Error en fallback ultrasonic: {fallback_error}")
                        return

            elif sensor_id == "opticalSpeed":
                print("Cargando lógica para el sensor opticalSpeed.")
                try:
                    if hasattr(self, 'current_optical_speed_logic') and self.current_optical_speed_logic:
                        try:
                            self.current_optical_speed_logic.cleanup()
                        except:
                            pass
                        self.current_optical_speed_logic = None

                    if not hasattr(self, 'opticalSpeedUi') or self.opticalSpeedUi is None:
                        loader = QUiLoader()
                        self.opticalSpeedUi = loader.load("SensoraCore/SC_DesktopApp/Modules/opticalSpeed/opticalSpeed.ui")

                    try:
                        _ = self.opticalSpeedUi.objectName()
                    except RuntimeError:
                        loader = QUiLoader()
                        self.opticalSpeedUi = loader.load("SensoraCore/SC_DesktopApp/Modules/opticalSpeed/opticalSpeed.ui")

                    if self.opticalSpeedUi is not None:
                        self.current_optical_speed_logic = OpticalSpeedLogic(self.opticalSpeedUi, self)
                        self.opticalSpeedUi.setParent(sensor_ui)
                        layout.addWidget(self.opticalSpeedUi)
                    else:
                        print("Error: No se pudo crear o cargar opticalSpeedUi.")
                        return
                except Exception as e:
                    print(f"Error al cargar OpticalSpeedLogic: {e}")
                    try:
                        loader = QUiLoader()
                        self.opticalSpeedUi = loader.load("SensoraCore/SC_DesktopApp/Modules/opticalSpeed/opticalSpeed.ui")
                        if self.opticalSpeedUi:
                            self.current_optical_speed_logic = OpticalSpeedLogic(self.opticalSpeedUi, self)
                            self.opticalSpeedUi.setParent(sensor_ui)
                            layout.addWidget(self.opticalSpeedUi)
                        else:
                            print("Fallback opticalSpeed falló.")
                            return
                    except Exception as fallback_error:
                        print(f"Error en fallback opticalSpeed: {fallback_error}")
                        return

            elif sensor_id == "irSteering":
                print("Cargando lógica para el sensor irSteering.")
                try:
                    if hasattr(self, 'current_ir_steering_logic') and self.current_ir_steering_logic:
                        try:
                            self.current_ir_steering_logic.cleanup()
                        except:
                            pass
                        self.current_ir_steering_logic = None

                    if not hasattr(self, 'irSteeringUi') or self.irSteeringUi is None:
                        loader = QUiLoader()
                        self.irSteeringUi = loader.load("SensoraCore/SC_DesktopApp/Modules/irSteering/irSteering.ui")

                    try:
                        _ = self.irSteeringUi.objectName()
                    except RuntimeError:
                        loader = QUiLoader()
                        self.irSteeringUi = loader.load("SensoraCore/SC_DesktopApp/Modules/irSteering/irSteering.ui")

                    if self.irSteeringUi is not None:
                        self.current_ir_steering_logic = IrSteeringLogic(self.irSteeringUi, self)
                        self.irSteeringUi.setParent(sensor_ui)
                        layout.addWidget(self.irSteeringUi)
                    else:
                        print("Error: No se pudo crear o cargar irSteeringUi.")
                        return
                except Exception as e:
                    print(f"Error al cargar IrSteeringLogic: {e}")
                    try:
                        loader = QUiLoader()
                        self.irSteeringUi = loader.load("SensoraCore/SC_DesktopApp/Modules/irSteering/irSteering.ui")
                        if self.irSteeringUi:
                            self.current_ir_steering_logic = IrSteeringLogic(self.irSteeringUi, self)
                            self.irSteeringUi.setParent(sensor_ui)
                            layout.addWidget(self.irSteeringUi)
                        else:
                            print("Fallback irSteering falló.")
                            return
                    except Exception as fallback_error:
                        print(f"Error en fallback irSteering: {fallback_error}")
                        return

            elif sensor_id == "thermoregulation":
                print("Cargando lógica para el sensor thermoregulation.")
                try:
                    if hasattr(self, 'current_thermoregulation_logic') and self.current_thermoregulation_logic:
                        try:
                            self.current_thermoregulation_logic.cleanup()
                        except:
                            pass
                        self.current_thermoregulation_logic = None

                    if not hasattr(self, 'thermoregulationUi') or self.thermoregulationUi is None:
                        loader = QUiLoader()
                        self.thermoregulationUi = loader.load("SensoraCore/SC_DesktopApp/Modules/thermoregulation/thermoregulation.ui")

                    try:
                        _ = self.thermoregulationUi.objectName()
                    except RuntimeError:
                        loader = QUiLoader()
                        self.thermoregulationUi = loader.load("SensoraCore/SC_DesktopApp/Modules/thermoregulation/thermoregulation.ui")

                    if self.thermoregulationUi is not None:
                        self.current_thermoregulation_logic = ThermoregulationLogic(self.thermoregulationUi, self)
                        self.thermoregulationUi.setParent(sensor_ui)
                        layout.addWidget(self.thermoregulationUi)
                    else:
                        print("Error: No se pudo crear o cargar thermoregulationUi.")
                        return
                except Exception as e:
                    print(f"Error al cargar ThermoregulationLogic: {e}")
                    try:
                        loader = QUiLoader()
                        self.thermoregulationUi = loader.load("SensoraCore/SC_DesktopApp/Modules/thermoregulation/thermoregulation.ui")
                        if self.thermoregulationUi:
                            self.current_thermoregulation_logic = ThermoregulationLogic(self.thermoregulationUi, self)
                            self.thermoregulationUi.setParent(sensor_ui)
                            layout.addWidget(self.thermoregulationUi)
                        else:
                            print("Fallback thermoregulation falló.")
                            return
                    except Exception as fallback_error:
                        print(f"Error en fallback thermoregulation: {fallback_error}")
                        return

            else:
                # Para otros sensores, usar el método existente
                # Diccionario de widgets de sensores
                sensor_widgets = {
                        # angleArm se maneja arriba con lógica
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
                if widget is not None:
                    try:
                        # Verificar que el widget es válido antes de usarlo
                        widget.setParent(sensor_ui)
                        layout.addWidget(widget)
                        widget.setVisible(True)
                    except RuntimeError as e:
                        # Intentar recrear el widget específico
                        self.reconstruirSensorUi(sensor_id)
                        return
                else:
                    print(f"Error: No se encontró widget para el sensor {sensor_id}")

            print(f"Sensor {sensor_id} seleccionado correctamente.")
        except Exception as e:
            print(f"Error al seleccionar el sensor {sensor_id}: {e}")

    def _cleanup_active_sensors(self):
        """
        Detiene cualquier proceso activo de sensores antes de cambiar o resetear.
        """
        try:
            print("Limpiando procesos activos de sensores...")
            
            # Limpiar SimpleAngle si está activo
            if hasattr(self, 'current_simple_angle_logic') and self.current_simple_angle_logic:
                try:
                    print("Deteniendo procesos de SimpleAngle...")
                    self.current_simple_angle_logic.cleanup()
                except Exception as e:
                    print(f"Error al limpiar SimpleAngle: {e}")
                self.current_simple_angle_logic = None
            # Limpiar AngleArm si está activo
            if hasattr(self, 'current_angle_arm_logic') and self.current_angle_arm_logic:
                try:
                    print("Deteniendo procesos de AngleArm...")
                    self.current_angle_arm_logic.cleanup()
                except Exception as e:
                    print(f"Error al limpiar AngleArm: {e}")
                self.current_angle_arm_logic = None
            # Limpiar Infrared si está activo
            if hasattr(self, 'current_infrared_logic') and self.current_infrared_logic:
                try:
                    print("Deteniendo procesos de Infrared...")
                    self.current_infrared_logic.cleanup()
                except Exception as e:
                    print(f"Error al limpiar Infrared: {e}")
                self.current_infrared_logic = None
            # Limpiar Capasitive si está activo
            if hasattr(self, 'current_capasitive_logic') and self.current_capasitive_logic:
                try:
                    print("Deteniendo procesos de Capasitive...")
                    self.current_capasitive_logic.cleanup()
                except Exception as e:
                    print(f"Error al limpiar Capasitive: {e}")
                self.current_capasitive_logic = None
            # Limpiar Ultrasonic si está activo
            if hasattr(self, 'current_ultrasonic_logic') and self.current_ultrasonic_logic:
                try:
                    print("Deteniendo procesos de Ultrasonic...")
                    self.current_ultrasonic_logic.cleanup()
                except Exception as e:
                    print(f"Error al limpiar Ultrasonic: {e}")
                self.current_ultrasonic_logic = None
            # Limpiar OpticalSpeed si está activo
            if hasattr(self, 'current_optical_speed_logic') and self.current_optical_speed_logic:
                try:
                    print("Deteniendo procesos de OpticalSpeed...")
                    self.current_optical_speed_logic.cleanup()
                except Exception as e:
                    print(f"Error al limpiar OpticalSpeed: {e}")
                self.current_optical_speed_logic = None
            # Limpiar IrSteering si está activo
            if hasattr(self, 'current_ir_steering_logic') and self.current_ir_steering_logic:
                try:
                    print("Deteniendo procesos de IrSteering...")
                    self.current_ir_steering_logic.cleanup()
                except Exception as e:
                    print(f"Error al limpiar IrSteering: {e}")
                self.current_ir_steering_logic = None
            # Limpiar Thermoregulation si está activo
            if hasattr(self, 'current_thermoregulation_logic') and self.current_thermoregulation_logic:
                try:
                    print("Deteniendo procesos de Thermoregulation...")
                    self.current_thermoregulation_logic.cleanup()
                except Exception as e:
                    print(f"Error al limpiar Thermoregulation: {e}")
                self.current_thermoregulation_logic = None
            
            # Aquí se pueden agregar otros sensores cuando tengan lógica propia
            # Por ejemplo:
            # if hasattr(self, 'current_ultrasonic_logic') and self.current_ultrasonic_logic:
            #     self.current_ultrasonic_logic.cleanup()
            
            print("Limpieza de sensores completada.")
        except Exception as e:
            print(f"Error durante la limpieza de sensores: {e}")

    def reconstruirSensorUi(self, sensor_id):
        """
        Recrea un widget específico de sensor si ha sido eliminado.
        """
        try:
            loader = QUiLoader()
            
            if sensor_id == "angleArm":
                self.angleArmUi = loader.load("SensoraCore/SC_DesktopApp/Modules/angleArm/angleArm.ui")
            elif sensor_id == "infrared":
                self.infraredUi = loader.load("SensoraCore/SC_DesktopApp/Modules/infrared/infrared.ui")
            elif sensor_id == "capasitive":
                self.capasitiveUi = loader.load("SensoraCore/SC_DesktopApp/Modules/capasitive/capasitive.ui")
            elif sensor_id == "ultrasonic":
                self.ultrasonicUi = loader.load("SensoraCore/SC_DesktopApp/Modules/ultrasonic/ultrasonic.ui")
            elif sensor_id == "opticalSpeed":
                self.opticalSpeedUi = loader.load("SensoraCore/SC_DesktopApp/Modules/opticalSpeed/opticalSpeed.ui")
            elif sensor_id == "irSteering":
                self.irSteeringUi = loader.load("SensoraCore/SC_DesktopApp/Modules/irSteering/irSteering.ui")
            elif sensor_id == "thermoregulation":
                self.thermoregulationUi = loader.load("SensoraCore/SC_DesktopApp/Modules/thermoregulation/thermoregulation.ui")
            elif sensor_id == "gasRegulation":
                self.gasRegulationUi = loader.load("SensoraCore/SC_DesktopApp/Modules/gasRegulation/gasRegulation.ui")
            elif sensor_id == "brightness":
                self.brightnessUi = loader.load("SensoraCore/SC_DesktopApp/Modules/brightness/brightness.ui")
            elif sensor_id == "colorCNY":
                self.colorCNYUi = loader.load("SensoraCore/SC_DesktopApp/Modules/colorCNY/colorCNY.ui")
            elif sensor_id == "colorTCS":
                self.colorTCSUi = loader.load("SensoraCore/SC_DesktopApp/Modules/colorTCS/colorTCS.ui")
            
            # Volver a intentar seleccionar el sensor
            self.sensorSeleccionado(sensor_id)
            
        except Exception as e:
            print(f"Error al recrear widget para {sensor_id}: {e}")



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