# main_debug.py para SensoraCoreApp
# Versión con debug para verificar que la aplicación funcione correctamente
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow
import sys

if __name__ == "__main__":
    print("🚀 Iniciando SensoraCore...")
    print("📱 Creando aplicación Qt...")
    
    app = QApplication(sys.argv)
    
    print("🖥️ Creando ventana principal...")
    window = MainWindow()
    
    print("👁️ Mostrando ventana...")
    window.show()
    
    print("✅ Aplicación lista!")
    print("📌 Para cerrar la aplicación, cierra la ventana o presiona Ctrl+C aquí")
    print("🔧 Si ves este mensaje, la aplicación se ejecutó exitosamente!")
    
    # Ejecutar el loop de eventos
    sys.exit(app.exec())
