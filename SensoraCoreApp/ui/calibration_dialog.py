# =====================================================================================
# DIÁLOGO DE CALIBRACIÓN POR REGRESIÓN LINEAL PARA SENSORACORE
# =====================================================================================
# Ruta del archivo: ui/calibration_dialog.py
# Función: Interfaz gráfica para calibración de sensores por regresión lineal
# Autor: Sistema SensoraCore
# Propósito: Permitir al usuario calibrar sensores visualmente

from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton, 
                              QTableWidget, QTableWidgetItem, QLabel, QLineEdit,
                              QMessageBox, QGroupBox, QGridLayout, QHeaderView)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
from modules.calibration import LinearCalibration

class CalibrationDialog(QDialog):
    """
    Diálogo para calibración por regresión lineal de sensores
    
    Propósito: Interfaz gráfica completa para calibrar sensores analógicos
    Funcionalidad: 
        - Agregar puntos de calibración manualmente
        - Visualizar datos y regresión en tiempo real
        - Realizar calibración automática
        - Guardar/cargar calibraciones
        - Mostrar estadísticas de calibración
    """
      # Señal para notificar cambios de calibración a la ventana principal
    calibration_updated = Signal(object)
    
    def __init__(self, sensor_name="Sensor", calibration_instance=None, parent=None):
        """
        Inicializar diálogo de calibración
        
        Args:
            sensor_name: Nombre del sensor para personalizar la interfaz
            calibration_instance: Instancia de LinearCalibration existente (opcional)
            parent: Ventana padre
        """
        super().__init__(parent)
        self.sensor_name = sensor_name
        self.calibration = calibration_instance if calibration_instance else LinearCalibration()
        self.setup_ui()
        self.update_plot()
    
    def setup_ui(self):
        """Configurar toda la interfaz de usuario del diálogo"""
        self.setWindowTitle(f"Calibración por Regresión Lineal - {self.sensor_name}")
        self.setFixedSize(900, 700)  # Tamaño fijo para mejor diseño
        
        # Layout principal vertical
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        
        # ==================== GRUPO DE ENTRADA DE DATOS ====================
        input_group = QGroupBox("Agregar Punto de Calibración")
        input_group.setFont(QFont("Arial", 10, QFont.Bold))
        input_layout = QGridLayout(input_group)
        
        # Campos de entrada
        input_layout.addWidget(QLabel("Valor Crudo del Sensor:"), 0, 0)
        self.raw_input = QLineEdit()
        self.raw_input.setPlaceholderText("Ej: 512 (lectura ADC)")
        input_layout.addWidget(self.raw_input, 0, 1)
        
        input_layout.addWidget(QLabel("Valor Real (Referencia):"), 0, 2)
        self.ref_input = QLineEdit()
        self.ref_input.setPlaceholderText("Ej: 90.0 (grados reales)")
        input_layout.addWidget(self.ref_input, 0, 3)
        
        # Botón para agregar punto
        self.add_point_btn = QPushButton("➕ Agregar Punto")
        self.add_point_btn.clicked.connect(self.add_calibration_point)
        self.add_point_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        input_layout.addWidget(self.add_point_btn, 0, 4)
        
        layout.addWidget(input_group)
        
        # ==================== TABLA DE PUNTOS DE CALIBRACIÓN ====================
        table_group = QGroupBox("Puntos de Calibración")
        table_group.setFont(QFont("Arial", 10, QFont.Bold))
        table_layout = QVBoxLayout(table_group)
        
        self.points_table = QTableWidget(0, 3)  # 3 columnas: Crudo, Referencia, Eliminar
        self.points_table.setHorizontalHeaderLabels(["Valor Crudo", "Valor Referencia", "Acción"])
        
        # Configurar encabezados de tabla
        header = self.points_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Fixed)
        self.points_table.setColumnWidth(2, 80)
        
        table_layout.addWidget(self.points_table)
        layout.addWidget(table_group)
        
        # ==================== BOTONES DE CONTROL ====================
        buttons_layout = QHBoxLayout()
        
        # Botón calibrar
        self.calibrate_btn = QPushButton("🔧 Realizar Calibración")
        self.calibrate_btn.clicked.connect(self.perform_calibration)
        self.calibrate_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        buttons_layout.addWidget(self.calibrate_btn)
        
        # Botón limpiar
        self.clear_btn = QPushButton("🗑️ Limpiar Datos")
        self.clear_btn.clicked.connect(self.clear_data)
        self.clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF9800;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #F57C00;
            }
        """)
        buttons_layout.addWidget(self.clear_btn)
        
        # Botón guardar
        self.save_btn = QPushButton("💾 Guardar Calibración")
        self.save_btn.clicked.connect(self.save_calibration)
        buttons_layout.addWidget(self.save_btn)
        
        # Botón cargar
        self.load_btn = QPushButton("📂 Cargar Calibración")
        self.load_btn.clicked.connect(self.load_calibration)
        buttons_layout.addWidget(self.load_btn)
        
        layout.addLayout(buttons_layout)
        
        # ==================== INFORMACIÓN DE CALIBRACIÓN ====================
        info_group = QGroupBox("Estado de Calibración")
        info_group.setFont(QFont("Arial", 10, QFont.Bold))
        info_layout = QVBoxLayout(info_group)
        
        self.info_label = QLabel("Ecuación: No calibrado")
        self.info_label.setFont(QFont("Arial", 9))
        self.info_label.setStyleSheet("padding: 5px; background-color: #f0f0f0; border-radius: 3px;")
        info_layout.addWidget(self.info_label)
        
        layout.addWidget(info_group)
        
        # ==================== GRÁFICO ====================
        graph_group = QGroupBox("Visualización de Calibración")
        graph_group.setFont(QFont("Arial", 10, QFont.Bold))
        graph_layout = QVBoxLayout(graph_group)
        
        self.figure = Figure(figsize=(8, 4))
        self.canvas = FigureCanvas(self.figure)
        graph_layout.addWidget(self.canvas)
        
        layout.addWidget(graph_group)
        
        # ==================== BOTONES DE DIÁLOGO ====================
        dialog_buttons = QHBoxLayout()
        
        self.apply_btn = QPushButton("✅ Aplicar y Cerrar")
        self.apply_btn.clicked.connect(self.accept)
        self.apply_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 12px 20px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        dialog_buttons.addWidget(self.apply_btn)
        
        self.cancel_btn = QPushButton("❌ Cancelar")
        self.cancel_btn.clicked.connect(self.reject)
        self.cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                padding: 12px 20px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #d32f2f;
            }
        """)
        dialog_buttons.addWidget(self.cancel_btn)
        
        layout.addLayout(dialog_buttons)
        
        # Conectar Enter para agregar puntos
        self.raw_input.returnPressed.connect(self.add_calibration_point)
        self.ref_input.returnPressed.connect(self.add_calibration_point)
    
    def add_calibration_point(self):
        """Añade un punto de calibración y actualiza la interfaz"""
        try:
            raw_val = float(self.raw_input.text())
            ref_val = float(self.ref_input.text())
            
            # Agregar al modelo de calibración
            self.calibration.add_calibration_point(raw_val, ref_val)
            
            # Actualizar tabla
            row = self.points_table.rowCount()
            self.points_table.insertRow(row)
            self.points_table.setItem(row, 0, QTableWidgetItem(f"{raw_val:.2f}"))
            self.points_table.setItem(row, 1, QTableWidgetItem(f"{ref_val:.2f}"))
            
            # Botón eliminar para esta fila
            delete_btn = QPushButton("🗑️")
            delete_btn.clicked.connect(lambda checked, r=row: self.remove_point(r))
            delete_btn.setStyleSheet("QPushButton { background-color: #f44336; color: white; }")
            self.points_table.setCellWidget(row, 2, delete_btn)
            
            # Limpiar campos
            self.raw_input.clear()
            self.ref_input.clear()
            
            # Actualizar gráfico
            self.update_plot()
            
            # Focus al primer campo para siguiente entrada
            self.raw_input.setFocus()
            
        except ValueError:
            QMessageBox.warning(self, "Error de Entrada", 
                              "Por favor ingrese valores numéricos válidos.\n\n"
                              "Ejemplo:\n"
                              "Valor Crudo: 512\n"
                              "Valor Referencia: 90.0")
    
    def remove_point(self, row):
        """Elimina un punto de calibración específico"""
        if 0 <= row < len(self.calibration.calibration_data["raw_values"]):
            # Eliminar del modelo
            del self.calibration.calibration_data["raw_values"][row]
            del self.calibration.calibration_data["reference_values"][row]
            
            # Recrear tabla completa (más simple que manejar índices)
            self.update_table()
            self.update_plot()
            
            # Resetear calibración si hay cambios
            self.calibration.is_calibrated = False
            self.info_label.setText("Ecuación: No calibrado (datos modificados)")
    
    def update_table(self):
        """Actualiza la tabla completa con los datos actuales"""
        self.points_table.setRowCount(0)
        raw_vals = self.calibration.calibration_data["raw_values"]
        ref_vals = self.calibration.calibration_data["reference_values"]
        
        for i, (raw_val, ref_val) in enumerate(zip(raw_vals, ref_vals)):
            row = self.points_table.rowCount()
            self.points_table.insertRow(row)
            self.points_table.setItem(row, 0, QTableWidgetItem(f"{raw_val:.2f}"))
            self.points_table.setItem(row, 1, QTableWidgetItem(f"{ref_val:.2f}"))
            
            # Botón eliminar
            delete_btn = QPushButton("🗑️")
            delete_btn.clicked.connect(lambda checked, r=i: self.remove_point(r))
            delete_btn.setStyleSheet("QPushButton { background-color: #f44336; color: white; }")
            self.points_table.setCellWidget(row, 2, delete_btn)
    
    def perform_calibration(self):
        """Realiza la calibración y actualiza la interfaz"""
        if self.calibration.perform_calibration():
            self.info_label.setText(f"Ecuación: {self.calibration.get_calibration_equation()}")
            self.info_label.setStyleSheet("padding: 5px; background-color: #c8e6c9; border-radius: 3px; color: #2e7d32;")
            self.update_plot()
            
            # Mostrar estadísticas detalladas
            stats = self.calibration.get_calibration_stats()
            QMessageBox.information(self, "Calibración Exitosa", 
                                  f"✅ Calibración realizada correctamente\n\n"
                                  f"📈 Ecuación: {stats['equation']}\n"
                                  f"📊 Puntos utilizados: {stats['num_points']}\n"
                                  f"🎯 Calidad (R²): {stats['r_squared']:.4f}\n\n"
                                  f"💡 R² cercano a 1.0 indica mejor ajuste")
        else:
            QMessageBox.warning(self, "Error de Calibración", 
                              "❌ Se necesitan al menos 2 puntos para realizar la calibración.\n\n"
                              "💡 Agregue más puntos de referencia conocidos.")
    
    def clear_data(self):
        """Limpia todos los datos y resetea la interfaz"""
        reply = QMessageBox.question(self, "Confirmar Limpieza", 
                                   "⚠️ ¿Está seguro de que desea eliminar todos los datos de calibración?\n\n"
                                   "Esta acción no se puede deshacer.",
                                   QMessageBox.Yes | QMessageBox.No,
                                   QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            self.calibration.clear_calibration_data()
            self.points_table.setRowCount(0)
            self.info_label.setText("Ecuación: No calibrado")
            self.info_label.setStyleSheet("padding: 5px; background-color: #f0f0f0; border-radius: 3px;")
            self.update_plot()
    
    def update_plot(self):
        """Actualiza el gráfico de calibración en tiempo real"""
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        
        raw_vals = self.calibration.calibration_data["raw_values"]
        ref_vals = self.calibration.calibration_data["reference_values"]
        
        if len(raw_vals) > 0:
            # Puntos de calibración
            ax.scatter(raw_vals, ref_vals, color='blue', s=50, alpha=0.7, 
                      label='Puntos de Calibración', zorder=5)
            
            # Línea de regresión si está calibrado
            if self.calibration.is_calibrated:
                x_min, x_max = min(raw_vals), max(raw_vals)
                x_range = x_max - x_min
                x_line = np.linspace(x_min - x_range*0.1, x_max + x_range*0.1, 100)
                y_line = [self.calibration.calibrate_value(x) for x in x_line]
                ax.plot(x_line, y_line, 'r-', linewidth=2, 
                       label=f'Regresión Lineal (R² = {self.calibration.r_squared:.3f})', zorder=3)
                
                # Líneas de grilla para los puntos
                for raw, ref in zip(raw_vals, ref_vals):
                    ax.axvline(x=raw, color='gray', linestyle='--', alpha=0.3, zorder=1)
                    ax.axhline(y=ref, color='gray', linestyle='--', alpha=0.3, zorder=1)
                
                ax.legend()
        else:
            # Mensaje cuando no hay datos
            ax.text(0.5, 0.5, 'No hay puntos de calibración\n\nAgregue puntos usando los campos de arriba', 
                   horizontalalignment='center', verticalalignment='center',
                   transform=ax.transAxes, fontsize=12, 
                   bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgray"))
        
        ax.set_xlabel('Valor Crudo del Sensor')
        ax.set_ylabel('Valor Real (Referencia)')
        ax.set_title(f'Calibración por Regresión Lineal - {self.sensor_name}')
        ax.grid(True, alpha=0.3)
        
        # Mejorar aspecto del gráfico
        self.figure.tight_layout()
        self.canvas.draw()
    
    def save_calibration(self):
        """Guarda la calibración actual en archivo"""
        if not self.calibration.is_calibrated:
            QMessageBox.warning(self, "Sin Calibración", 
                              "❌ No hay calibración activa para guardar.\n\n"
                              "💡 Primero realice una calibración con los datos ingresados.")
            return
        
        filename = f"calibration_{self.sensor_name.lower().replace(' ', '_')}.json"
        if self.calibration.save_calibration(filename):
            QMessageBox.information(self, "Guardado Exitoso", 
                                  f"✅ Calibración guardada correctamente\n\n"
                                  f"📁 Archivo: {filename}\n"
                                  f"📈 Ecuación: {self.calibration.get_calibration_equation()}")
        else:
            QMessageBox.warning(self, "Error de Guardado", 
                              f"❌ Error al guardar la calibración en {filename}\n\n"
                              "💡 Verifique permisos de escritura en el directorio.")
    
    def load_calibration(self):
        """Carga una calibración desde archivo"""
        filename = f"calibration_{self.sensor_name.lower().replace(' ', '_')}.json"
        if self.calibration.load_calibration(filename):
            self.update_table()
            self.info_label.setText(f"Ecuación: {self.calibration.get_calibration_equation()}")
            self.info_label.setStyleSheet("padding: 5px; background-color: #c8e6c9; border-radius: 3px; color: #2e7d32;")
            self.update_plot()
            
            stats = self.calibration.get_calibration_stats()
            QMessageBox.information(self, "Carga Exitosa", 
                                  f"✅ Calibración cargada correctamente\n\n"
                                  f"📁 Archivo: {filename}\n"
                                  f"📈 Ecuación: {stats['equation']}\n"
                                  f"📊 Puntos: {stats['num_points']}\n"
                                  f"🎯 Calidad (R²): {stats['r_squared']:.4f}")
        else:
            QMessageBox.warning(self, "Error de Carga", 
                              f"❌ No se pudo cargar la calibración\n\n"
                              f"📁 Archivo buscado: {filename}\n"
                              "💡 Verifique que el archivo existe y es válido.")
    
    def accept(self):
        """Acepta el diálogo y emite la señal de calibración actualizada"""
        self.calibration_updated.emit(self.calibration)
        super().accept()
    
    def set_calibration(self, calibration):
        """Establece una calibración existente en el diálogo"""
        self.calibration = calibration
        self.update_table()
        if calibration.is_calibrated:
            self.info_label.setText(f"Ecuación: {calibration.get_calibration_equation()}")
            self.info_label.setStyleSheet("padding: 5px; background-color: #c8e6c9; border-radius: 3px; color: #2e7d32;")
        self.update_plot()
