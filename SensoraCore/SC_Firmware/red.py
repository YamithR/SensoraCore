# red.py - SensoraCore
# Configuración centralizada de red WiFi
# Autor: SensoraCore Team
# Fecha: 2025-11-23

# ============================================================================
# CONFIGURACIÓN DE RED WiFi
# ============================================================================

# Credenciales de red WiFi
# Modifica estos valores según tu red
SSID = 'Oniris_G5-ID'
PASSWORD = 'Oniri$2025'

# Puerto del servidor TCP
PORT = 8080

# Configuración adicional (opcional)
# Timeout de conexión WiFi en segundos
WIFI_TIMEOUT = 15

# Máximo número de intentos de conexión
WIFI_MAX_ATTEMPTS = 5

# ============================================================================
# NOTAS
# ============================================================================
# Este archivo centraliza la configuración de red para todos los módulos
# del firmware SensoraCore. Para cambiar la red WiFi, solo edita este archivo.
#
# Uso en los módulos:
#   from red import SSID, PASSWORD
#
# O para importar todo:
#   import red
#   red.SSID
#   red.PASSWORD
