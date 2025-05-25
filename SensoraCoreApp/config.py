# config.py - Configuración de la aplicación SensoraCore
"""
Archivo de configuración para personalizar el comportamiento de SensoraCore
"""

# Configuración de red
DEFAULT_ESP32_IP = "192.168.20.25"  # IP por defecto del ESP32
ESP32_PORT = 8080  # Puerto de comunicación
CONNECTION_TIMEOUT = 3  # Timeout de conexión en segundos

# Configuración de gráficas
MAX_GRAPH_POINTS = 100  # Máximo número de puntos en la gráfica
GRAPH_UPDATE_INTERVAL = 100  # Intervalo de actualización en ms
GRAPH_COLORS = {
    'angulo': 'blue',
    'distancia': 'red',
    'velocidad': 'green'
}

# Configuración de sensores
SENSOR_CONFIG = {
    'potenciometer': {
        'name': 'Ángulo Simple (Potenciómetro)',
        'gpio_pin': 32,
        'min_value': 0,
        'max_value': 4095,
        'min_angle': -135,
        'max_angle': 135,
        'unit': '°'
    }
}

# Configuración de exportación
EXPORT_CONFIG = {
    'default_filename_prefix': 'SensoraCore',
    'timestamp_format': '%Y%m%d_%H%M%S',
    'excel_sheet_name': 'Datos Sensor',
    'include_chart': True,
    'include_statistics': True
}

# Configuración de interfaz
UI_CONFIG = {
    'window_title': 'SensoraCore',
    'min_window_size': (800, 600),
    'font_size': {
        'title': 16,
        'subtitle': 14,
        'normal': 12,
        'small': 10
    },
    'colors': {
        'background': '#f0f0f0',
        'border': '#ccc',
        'success': '#4CAF50',
        'error': '#f44336',
        'warning': '#ff9800'
    }
}

# Mensajes de la aplicación
MESSAGES = {
    'connection_success': 'Conexión exitosa con ESP32',
    'connection_error': 'Error al conectar con ESP32',
    'no_data_to_export': 'No hay datos para exportar',
    'export_success': 'Datos exportados correctamente',
    'export_error': 'Error al exportar datos',
    'clear_graph_confirm': 'Se han borrado todos los datos de la gráfica'
}
