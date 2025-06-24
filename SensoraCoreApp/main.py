# main.py para SensoraCoreApp
# Punto de entrada de la aplicación
from IMPORTACIONES import *

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
