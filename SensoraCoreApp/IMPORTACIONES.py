# =====================================================================================
# IMPORTACIONES DE BIBLIOTECAS NECESARIAS
# =====================================================================================
# --- Bibliotecas estándar de Python ---
import json
import os
import socket
import sys
from datetime import datetime
from typing import List, Optional, Tuple

# --- Bibliotecas para gráficas científicas ---
import matplotlib
matplotlib.use("QtAgg")
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np

# --- Bibliotecas para exportar datos a Excel ---
import openpyxl
from openpyxl.chart import LineChart, Reference

# --- Bibliotecas para análisis de datos ---
from sklearn.linear_model import LinearRegression

# --- Bibliotecas para la interfaz gráfica (PySide6) ---
from PySide6.QtCore import (QEasingCurve, QPropertyAnimation, 
                            QRect, QThread,QTimer, Qt, Signal)
from PySide6.QtGui import (QColor, QFont, QPalette)
from PySide6.QtWidgets import (QApplication, QDialog, QFileDialog, QFrame, 
                              QGraphicsOpacityEffect, 
                              QGridLayout, QGroupBox, 
                              QHBoxLayout, QHeaderView, QLabel, QLineEdit, 
                              QListWidget, QListWidgetItem, QMainWindow, 
                              QMessageBox, QPushButton, QScrollArea, 
                              QSplitter, QTableWidget, 
                              QTableWidgetItem, QVBoxLayout, QWidget)

# --- Módulos personalizados ---
from network_client import ESP32Client
from ui.main_window import MainWindow
