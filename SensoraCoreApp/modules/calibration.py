# =====================================================================================
# MÓDULO DE CALIBRACIÓN POR REGRESIÓN LINEAL PARA SENSORACORE
# =====================================================================================
# Ruta del archivo: modules/calibration.py
# Función: Implementa calibración por regresión lineal para sensores analógicos
# Autor: Sistema SensoraCore
# Propósito: Mejorar precisión de lecturas de sensores mediante calibración

import numpy as np
from sklearn.linear_model import LinearRegression
from typing import List, Tuple, Optional
import json
import os

class LinearCalibration:
    """
    Clase para manejar calibración por regresión lineal de sensores
    
    Propósito: Aplicar calibración matemática a lecturas de sensores analógicos
    Funcionalidad: Permite agregar puntos de calibración, calcular regresión y aplicar corrección
    Uso típico: Para sensores de ángulo, distancia, presión que requieren precisión mejorada
    """
    
    def __init__(self):
        """Inicializar sistema de calibración vacío"""
        self.model = LinearRegression()          # Modelo de regresión lineal de scikit-learn
        self.is_calibrated = False              # Flag para saber si ya se calibró
        self.calibration_data = {               # Datos de calibración almacenados
            "raw_values": [],                   # Valores crudos del sensor (ADC, voltaje, etc.)
            "reference_values": []              # Valores de referencia conocidos (exactos)
        }
        # Parámetros de la ecuación y = mx + b
        self.slope = None                       # Pendiente (m)
        self.intercept = None                   # Intercepto (b)
        self.r_squared = None                   # Coeficiente de determinación (calidad del ajuste)
    
    def add_calibration_point(self, raw_value: float, reference_value: float):
        """
        Añade un punto de calibración al conjunto de datos
        
        Args:
            raw_value: Valor crudo leído del sensor (sin calibrar)
            reference_value: Valor exacto conocido (medido con instrumento preciso)
        
        Ejemplo:
            # Sensor lee 512 ADC, pero sabemos que corresponde a 90°
            calibration.add_calibration_point(512, 90.0)
        """
        self.calibration_data["raw_values"].append(raw_value)
        self.calibration_data["reference_values"].append(reference_value)
    
    def clear_calibration_data(self):
        """Limpia todos los datos de calibración y resetea el estado"""
        self.calibration_data = {"raw_values": [], "reference_values": []}
        self.is_calibrated = False
        self.slope = None
        self.intercept = None
        self.r_squared = None
    
    def perform_calibration(self) -> bool:
        """
        Realiza la calibración con los datos actuales usando regresión lineal
        
        Returns:
            bool: True si la calibración fue exitosa, False si no hay suficientes datos
        
        Proceso:
            1. Verifica que hay al menos 2 puntos (mínimo para línea)
            2. Aplica regresión lineal usando scikit-learn
            3. Extrae parámetros de la ecuación (pendiente, intercepto, R²)
            4. Marca el sistema como calibrado
        """
        if len(self.calibration_data["raw_values"]) < 2:
            return False  # Necesitamos mínimo 2 puntos para hacer una línea
        
        # Preparar datos para scikit-learn (formato matricial)
        X = np.array(self.calibration_data["raw_values"]).reshape(-1, 1)  # Valores X (crudos)
        y = np.array(self.calibration_data["reference_values"])           # Valores Y (referencia)
        
        # Realizar regresión lineal
        self.model.fit(X, y)
        
        # Extraer parámetros de la ecuación y = mx + b
        self.slope = self.model.coef_[0]           # Pendiente (m)
        self.intercept = self.model.intercept_     # Intercepto (b)
        self.r_squared = self.model.score(X, y)   # R² (calidad del ajuste: 0-1, 1 es perfecto)
        self.is_calibrated = True
        
        return True
    
    def calibrate_value(self, raw_value: float) -> Optional[float]:
        """
        Aplica calibración a un valor crudo del sensor
        
        Args:
            raw_value: Valor sin calibrar del sensor
            
        Returns:
            float: Valor calibrado, o None si no hay calibración activa
            
        Ejemplo:
            # Si calibración es y = 0.176x - 90.112
            # raw_value = 1000 → calibrated = 0.176*1000 - 90.112 = 85.888
        """
        if not self.is_calibrated:
            return None  # No se puede calibrar sin datos
        
        return self.model.predict([[raw_value]])[0]
    
    def get_calibration_equation(self) -> str:
        """
        Retorna la ecuación de calibración como string legible
        
        Returns:
            str: Ecuación en formato "y = mx + b (R² = valor)"
        """
        if not self.is_calibrated:
            return "No calibrado"
        
        # Formatear ecuación con 4 decimales
        sign = "+" if self.intercept >= 0 else ""  # Manejar signo del intercepto
        return f"y = {self.slope:.4f}x {sign}{self.intercept:.4f} (R² = {self.r_squared:.4f})"
    
    def save_calibration(self, filepath: str) -> bool:
        """
        Guarda la calibración en un archivo JSON
        
        Args:
            filepath: Ruta donde guardar el archivo
            
        Returns:
            bool: True si se guardó exitosamente
        """
        if not self.is_calibrated:
            return False
        
        # Preparar datos para JSON
        data = {
            "slope": self.slope,
            "intercept": self.intercept,
            "r_squared": self.r_squared,
            "calibration_data": self.calibration_data,
            "timestamp": "generated_by_sensoracore"
        }
        
        try:
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception:
            return False
    
    def load_calibration(self, filepath: str) -> bool:
        """
        Carga una calibración desde archivo JSON
        
        Args:
            filepath: Ruta del archivo a cargar
            
        Returns:
            bool: True si se cargó exitosamente
        """
        if not os.path.exists(filepath):
            return False
        
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            # Restaurar parámetros
            self.slope = data["slope"]
            self.intercept = data["intercept"]
            self.r_squared = data["r_squared"]
            self.calibration_data = data["calibration_data"]
            
            # Recrear el modelo de scikit-learn
            X = np.array(self.calibration_data["raw_values"]).reshape(-1, 1)
            y = np.array(self.calibration_data["reference_values"])
            self.model.fit(X, y)
            self.is_calibrated = True
            
            return True
        except Exception:
            return False
    
    def get_calibration_stats(self) -> dict:
        """
        Retorna estadísticas de la calibración actual
        
        Returns:
            dict: Diccionario con estadísticas de calibración
        """
        if not self.is_calibrated:
            return {"status": "No calibrado"}
        
        return {
            "status": "Calibrado",
            "equation": self.get_calibration_equation(),
            "num_points": len(self.calibration_data["raw_values"]),
            "r_squared": self.r_squared,
            "slope": self.slope,
            "intercept": self.intercept
        }
