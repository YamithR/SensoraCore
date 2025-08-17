from PySide6.QtWidgets import QWidget, QMessageBox
from PySide6.QtCore import QTimer
from SensoraCore.SC_DesktopApp.Modules.simpleAngle.simpleAngle_ui import Ui_simpleAngle

class SimpleAngleLogic(QWidget):
    def __init__(self, ui_widget):
        try:
            print("Inicializando SimpleAngleLogic...")
            super().__init__()

            # Usar el widget de interfaz proporcionado
            self.ui = ui_widget

            # Verificar si los botones están correctamente definidos
            if not hasattr(self.ui, 'iniciar') or not hasattr(self.ui, 'calibrar') or not hasattr(self.ui, 'limpiar') or not hasattr(self.ui, 'exportar'):
                raise AttributeError("Uno o más botones no están definidos correctamente en la interfaz.")

            # Conectar botones a funciones con mensajes de depuración
            self.ui.iniciar.clicked.connect(lambda: print("Botón 'Iniciar' presionado") or self.iniciar_monitoreo())
            self.ui.calibrar.clicked.connect(lambda: print("Botón 'Calibrar' presionado") or self.calibrar_sensor())
            self.ui.limpiar.clicked.connect(lambda: print("Botón 'Limpiar' presionado") or self.limpiar_grafica())
            self.ui.exportar.clicked.connect(lambda: print("Botón 'Exportar' presionado") or self.exportar_datos())

            # Inicializar variables
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.actualizar_datos)
            self.monitoreo_activo = False

            print("SimpleAngleLogic inicializado correctamente.")
        except Exception as e:
            print(f"Error al inicializar SimpleAngleLogic: {e}")

    def iniciar_monitoreo(self):
        if not self.monitoreo_activo:
            self.monitoreo_activo = True
            self.timer.start(1000)  # Actualizar cada segundo
            self.ui.iniciar.setText("Detener Monitoreo")
        else:
            self.monitoreo_activo = False
            self.timer.stop()
            self.ui.iniciar.setText("Iniciar Monitoreo")

    def calibrar_sensor(self):
        # Lógica para calibrar el sensor
        QMessageBox.information(self, "Calibración", "El sensor ha sido calibrado.")
        self.ui.calibrar.setText("Calibrado")

    def limpiar_grafica(self):
        # Lógica para limpiar la gráfica
        QMessageBox.information(self, "Limpieza", "La gráfica ha sido limpiada.")

    def exportar_datos(self):
        # Lógica para exportar datos a Excel
        QMessageBox.information(self, "Exportar", "Los datos han sido exportados a Excel.")

    def actualizar_datos(self):
        # Lógica para actualizar los datos en la interfaz
        self.ui.analogoDt.setText("123")  # Ejemplo de datos
        self.ui.anguloDt.setText("45°")  # Ejemplo de datos