#!/usr/bin/env python3
# test_imports.py - Verificar que todos los imports funcionen correctamente

print("🔍 Probando imports de SensoraCore...")

try:
    print("📦 Importando PySide6...")
    from PySide6.QtWidgets import (QMainWindow, QLabel, QVBoxLayout, QWidget, 
                                   QPushButton, QLineEdit, QMessageBox, QGroupBox,
                                   QHBoxLayout, QFileDialog, QScrollArea, QFrame,
                                   QListWidget, QListWidgetItem, QSplitter,
                                   QGraphicsOpacityEffect)
    print("✅ PySide6.QtWidgets OK")
    
    from PySide6.QtCore import QThread, Signal, Qt, QEasingCurve, QPropertyAnimation, QRect
    print("✅ PySide6.QtCore OK")
    
    from PySide6.QtGui import QFont, QPalette, QColor
    print("✅ PySide6.QtGui OK")
    
    print("📡 Importando network_client...")
    from network_client import ESP32Client
    print("✅ network_client OK")
    
    print("📊 Importando matplotlib...")
    import matplotlib
    matplotlib.use('QtAgg')
    from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
    from matplotlib.figure import Figure
    print("✅ matplotlib OK")
    
    print("📄 Importando openpyxl...")
    import openpyxl
    from openpyxl.chart import LineChart, Reference
    print("✅ openpyxl OK")
    
    print("🎯 Importando MainWindow...")
    from ui.main_window import MainWindow
    print("✅ MainWindow OK")
    
    print("\n🎉 ¡Todos los imports fueron exitosos!")
    print("🚀 La aplicación debería funcionar correctamente")
    
except ImportError as e:
    print(f"❌ Error de import: {e}")
except Exception as e:
    print(f"❌ Error inesperado: {e}")
