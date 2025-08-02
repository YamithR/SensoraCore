#Importando componentes necesarios
from PySide6.QtWidgets import *
from PySide6.QtUiTools import QUiLoader

#El modulo sys responsable de procesar los argumentos en las lineas de comandos
import sys

# Crear una aplicación Qt
app = QApplication(sys.argv)

# Crear objeto de loader
loader = QUiLoader()

# Cargar el archivo .ui
ui = loader.load("SensoraCore/SC_DesktopApp/Main/mainWindow.ui")

# Mostrar la ventana
ui.show()

# Ejecutar el bucle de eventos
app.exec()
