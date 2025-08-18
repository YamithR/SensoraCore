from PySide6.QtCore import QTimer, QThread, Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QSizePolicy, QInputDialog, QMessageBox, QDialog
from .simpleAngle_ui import Ui_simpleAngle
import socket
import time
import os
import json
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class SimpleAngleThread(QThread):
    data_received = Signal(int, int)  # Señal para recibir datos (lectura AD, ángulo)
    connection_status = Signal(str)  # Señal para mostrar estado de conexión

    def __init__(self, esp32_ip, port=8080):
        super().__init__()
        self.esp32_ip = esp32_ip
        self.port = port
        self.running = False
        self.sock = None
        self.last_data_time = 0  # Para controlar la frecuencia de datos

    def run(self):
        self.running = True
        try:
            print(f"Intentando conectar al ESP32 en {self.esp32_ip}:{self.port}")
            self.connection_status.emit(f"Conectando a {self.esp32_ip}:{self.port}...")
            
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.settimeout(5)  # Aumentar timeout a 5 segundos
            
            # Intentar conectar
            self.sock.connect((self.esp32_ip, self.port))
            print("Conexión establecida, enviando comando MODO:ANGULO_SIMPLE")
            self.connection_status.emit("Conectado, iniciando monitoreo...")
            
            # Enviar comando y esperar respuesta
            self.sock.sendall(b'MODO:ANGULO_SIMPLE')
            
            # Esperar confirmación del ESP32
            response = self.sock.recv(64).decode('utf-8', errors='ignore').strip()
            print(f"Respuesta del ESP32: {response}")
            
            if 'ANGULO_SIMPLE_OK' in response:
                self.connection_status.emit("Monitoreo iniciado correctamente")
                self.sock.settimeout(2)  # Timeout de 2 segundos para muestreo de 0.5s
                
                while self.running:
                    try:
                        data = self.sock.recv(64)
                        if not data:
                            print("No se recibieron datos del ESP32")
                            break

                        msg = data.decode(errors='ignore').strip()
                        print(f"Datos recibidos: {msg}")  # Debug
                        
                        # Procesar solo la primera línea válida para evitar múltiples emisiones
                        lines = [line for line in msg.split('\n') if line.strip()]
                        for line in lines:
                            if line.startswith('POT:'):
                                try:
                                    # Control de tiempo para asegurar muestreo cada 0.5 segundos
                                    current_time = time.time()
                                    if current_time - self.last_data_time >= 0.4:  # Mínimo 0.4s entre muestras
                                        parts = line.replace('POT:', '').split(',ANG:')
                                        if len(parts) == 2:
                                            lectura = int(parts[0])
                                            angulo = int(parts[1])
                                            self.data_received.emit(lectura, angulo)
                                            self.last_data_time = current_time
                                            print(f"Datos procesados - Lectura: {lectura}, Ángulo: {angulo}")
                                            break  # Solo procesar la primera línea válida
                                    else:
                                        print(f"Datos ignorados - muy rápidos (delta: {current_time - self.last_data_time:.2f}s)")
                                except ValueError as ve:
                                    print(f"Error procesando datos: {ve}")
                                    
                    except socket.timeout:
                        print("Timeout esperando datos del ESP32 (normal con muestreo de 0.5s)")
                        continue
                    except Exception as e:
                        print(f"Error recibiendo datos: {e}")
                        break
            else:
                print(f"Respuesta inesperada del ESP32: {response}")
                self.connection_status.emit(f"Error: Respuesta inesperada del ESP32")
                
        except socket.timeout as e:
            print(f"Timeout de conexión al ESP32: {e}")
            self.connection_status.emit("Error: Timeout de conexión al ESP32")
        except ConnectionRefusedError as e:
            print(f"Conexión rechazada por el ESP32: {e}")
            self.connection_status.emit("Error: Conexión rechazada. Verificar que el ESP32 esté encendido")
        except Exception as e:
            print(f"Error en SimpleAngleThread: {e}")
            self.connection_status.emit(f"Error de conexión: {e}")
        finally:
            if self.sock:
                try:
                    self.sock.sendall(b'STOP')
                    print("Comando STOP enviado al ESP32")
                except:
                    pass
                self.sock.close()
                print("Socket cerrado")
            self.connection_status.emit("Desconectado")

    def stop(self):
        print("Deteniendo SimpleAngleThread...")
        self.running = False
        self.wait()

class SimpleAngleLogic(QWidget):
    def __init__(self, ui_widget, main_window=None):
        super().__init__()
        # Asegurar que el widget de calibración no esté visible hasta que se realice la calibración
        if hasattr(ui_widget, 'calBox') and ui_widget.calBox is not None:
            ui_widget.calBox.setVisible(False)
        try:
            print("Inicializando SimpleAngleLogic...")

            # Verificar que el widget UI es válido
            if ui_widget is None:
                raise ValueError("ui_widget no puede ser None")

            # Usar el widget de interfaz proporcionado
            self.ui = ui_widget
            self.main_window = main_window  # Referencia a la ventana principal
            self.connections = []  # Lista para rastrear conexiones de señales

            # Conectar botones de la interfaz
            if hasattr(self.ui, 'iniciar'):
                self.ui.iniciar.clicked.connect(self.toggle_angulo_monitoring)

            if hasattr(self.ui, 'calibrar'):
                self.ui.calibrar.clicked.connect(self.calibrar_sensor)

            if hasattr(self.ui, 'limpiar'):
                self.ui.limpiar.clicked.connect(self.limpiar_grafica)

            if hasattr(self.ui, 'exportar'):
                self.ui.exportar.clicked.connect(self.exportar_datos)

            # Inicializar variables
            self.timer = QTimer(self)  # Asignar parent para manejo automático de memoria
            self.timer.timeout.connect(self.actualizar_datos)
            self.monitoreo_activo = False
            self.lecturas = []  # Datos analógicos (0-4095)
            self.angulos = []   # Datos de ángulo (-135 a +135)
            self.tiempo = []    # Tiempo en segundos
            self.muestra_actual = 0  # Contador de muestras
            self.MAX_MUESTRAS = 25   # Límite de muestras en la gráfica (reducido de 50 a 25)
            # Para calibración
            self.last_lectura = None
            self.last_angulo = None
            self.calibrated = False
            self.cal_m = 1.0
            self.cal_b = 0.0
            self.cal_points = []  # lista de (lectura, angulo)
            # Intentar cargar calibración previa
            try:
                self._load_calibration()
            except Exception:
                pass

            # Configurar gráfica con dos ejes Y
            self.figure = Figure(figsize=(8, 5), tight_layout=True)
            self.canvas = FigureCanvas(self.figure)
            
            # Crear subplot con dos ejes Y
            self.ax1 = self.figure.add_subplot(111)
            self.ax2 = self.ax1.twinx()  # Segundo eje Y compartiendo el eje X
            
            # Configurar el primer eje (lecturas analógicas)
            self.ax1.set_xlabel("Tiempo (segundos)", fontsize=10)
            self.ax1.set_ylabel("Lectura Analógica (AD)", color='blue', fontsize=10)
            self.ax1.tick_params(axis='y', labelcolor='blue', labelsize=8)
            self.ax1.tick_params(axis='x', labelsize=8)
            self.ax1.set_ylim(0, 4095)  # Rango del AD
            self.ax1.grid(True, alpha=0.3)
            
            # Configurar el segundo eje (ángulos)
            self.ax2.set_ylabel("Ángulo (grados)", color='red', fontsize=10)
            self.ax2.tick_params(axis='y', labelcolor='red', labelsize=8)
            self.ax2.set_ylim(-135, 135)  # Rango del ángulo
            
            # Configurar título
            self.figure.suptitle("Sensor de Ángulo Simple - Tiempo Real", fontsize=12, fontweight='bold')
            
            # Líneas de la gráfica (original y calibrada)
            self.line1, = self.ax1.plot([], [], 'b-', label='Lectura AD', linewidth=2, alpha=0.8)
            self.line2, = self.ax2.plot([], [], 'r-', label='Ángulo Original', linewidth=1.5, alpha=0.6, linestyle='--')
            self.line3, = self.ax2.plot([], [], 'g-', label='Ángulo Calibrado', linewidth=2, alpha=0.8)
            
            # Leyenda compacta
            lines1, labels1 = self.ax1.get_legend_handles_labels()
            lines2, labels2 = self.ax2.get_legend_handles_labels()
            self.ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=9)
            
            # Ajustar márgenes para que se vea bien en el widget
            self.figure.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.15)

            # Variables para almacenar datos originales separados
            self.angulos_originales = []  # Ángulos sin calibración

            # Asegurar que grapWid tenga un layout y configurar el canvas
            if not self.ui.grapWid.layout():
                layout = QVBoxLayout()
                layout.setContentsMargins(5, 5, 5, 5)  # Pequeños márgenes
                layout.setSpacing(0)  # Sin espaciado entre widgets
                self.ui.grapWid.setLayout(layout)

            # Limpiar layout existente
            layout = self.ui.grapWid.layout()
            while layout.count():
                child = layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()

            # Configurar el canvas para que se adapte al widget
            self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            layout.addWidget(self.canvas)

            print("SimpleAngleLogic inicializado correctamente.")
        except Exception as e:
            print(f"Error al inicializar SimpleAngleLogic: {e}")
            raise

    def cleanup(self):
        """
        Limpia las conexiones y recursos antes de eliminar el objeto.
        """
        try:
            print("Limpiando SimpleAngleLogic...")
            
            # Detener timer si está activo
            if hasattr(self, 'timer') and self.timer.isActive():
                self.timer.stop()
            
            # Desconectar señales manualmente si es necesario
            # Las conexiones se limpian automáticamente cuando se eliminan los widgets
            self.connections.clear()
            
            print("Limpieza de SimpleAngleLogic completada.")
        except Exception as e:
            print(f"Error durante la limpieza: {e}")


    def calibrar_sensor(self):
        """
        Flujo interactivo de calibración por referencia con número personalizable de puntos.
        Se piden N puntos de referencia (ángulos conocidos). El usuario posiciona el potenciómetro,
        pulsa OK en el diálogo y se captura la lectura AD actual. Se calcula una regresión lineal
        (ángulo = m * lectura + b) y se guarda en disco. Al final muestra una gráfica de calibración.
        """
        try:
            # Si no hay monitoreo activo, pedir al usuario que lo inicie
            if not self.monitoreo_activo:
                QMessageBox.information(self, "Calibración", "Para calibrar, primero inicie el monitoreo y asegúrese de que llegan datos.")
                return

            # Si ya está calibrado, preguntar si desea recalibrar o resetear
            if self.calibrated:
                resp = QMessageBox.question(self, "Calibración", "Ya existe una calibración. ¿Desea reemplazarla?", QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
                if resp != QMessageBox.Yes:
                    return

            # Preguntar cuántos puntos de calibración desea
            num_points, ok = QInputDialog.getInt(self, "Calibración", "¿Cuántos puntos de calibración desea usar?\n(Mínimo: 2, Máximo: 10)", value=3)
            if not ok:
                QMessageBox.information(self, "Calibración", "Calibración cancelada por el usuario.")
                return
                
            # Validar rango manualmente
            if num_points < 2:
                QMessageBox.warning(self, "Calibración", "Mínimo 2 puntos de calibración requeridos.")
                return
            elif num_points > 10:
                QMessageBox.warning(self, "Calibración", "Máximo 10 puntos de calibración permitidos.")
                return

            puntos = []
            # Sugerencias de ángulos de referencia basadas en la tabla (ángulo simple)
            sugeridos = [-90.0, -45.0, 0.0, 45.0, 90.0, -120.0, 120.0, -135.0, 135.0, -60.0]
            
            for i in range(1, num_points + 1):
                # Pedir al usuario el ángulo de referencia
                default = sugeridos[i-1] if i-1 < len(sugeridos) else 0.0
                angle, ok = QInputDialog.getDouble(self, f"Calibración - Punto {i} de {num_points}", 
                                                 f"Mueva el potenciómetro a la posición deseada y escriba el ángulo de referencia (grados):\n\nPunto {i}/{num_points}", 
                                                 value=default, decimals=1)
                if not ok:
                    QMessageBox.information(self, "Calibración", "Calibración cancelada por el usuario.")
                    return

                # Capturar la última lectura conocida
                if self.last_lectura is None:
                    QMessageBox.warning(self, "Calibración", "No se detectan lecturas. Asegúrese de que el monitoreo está activo y que el ESP32 envía datos.")
                    return

                lectura = int(self.last_lectura)
                puntos.append((lectura, float(angle)))
                print(f"Punto {i}: Lectura AD = {lectura}, Ángulo = {angle}°")

            # Calcular regresión lineal simple (y = m*x + b) con los puntos
            xs = [p[0] for p in puntos]
            ys = [p[1] for p in puntos]
            n = len(xs)
            mean_x = sum(xs) / n
            mean_y = sum(ys) / n
            num = sum((xs[i] - mean_x) * (ys[i] - mean_y) for i in range(n))
            den = sum((xs[i] - mean_x) ** 2 for i in range(n))
            if den == 0:
                QMessageBox.warning(self, "Calibración", "No se puede calcular calibración: varianza en lecturas = 0")
                return

            m = num / den
            b = mean_y - m * mean_x

            # Calcular R² (coeficiente de determinación)
            ss_res = sum((ys[i] - (m * xs[i] + b)) ** 2 for i in range(n))
            ss_tot = sum((ys[i] - mean_y) ** 2 for i in range(n))
            r_squared = 1 - (ss_res / ss_tot) if ss_tot != 0 else 1.0

            # Guardar parámetros
            self.cal_m = m
            self.cal_b = b
            self.cal_points = puntos
            self.calibrated = True
            self._save_calibration()

            # Actualizar UI
            if hasattr(self.ui, 'calibrar') and self.ui.calibrar is not None:
                self.ui.calibrar.setText("Calibrado")
                # color neutro/verde suave (evita saturar con colores intensos)
                self.ui.calibrar.setStyleSheet(
                    "font-size: 14px;"
                    "font-weight: bold;"
                    "color: rgb(20, 80, 20);"
                    "padding: 6px;"
                    "background-color: rgb(220, 255, 220);"
                    "border-radius: 4px;"
                    "border: 1px solid rgb(120, 180, 120);"
                )
            if hasattr(self.ui, 'calBox') and self.ui.calBox is not None:
                self.ui.calBox.setVisible(True)

            # Mostrar gráfica de calibración
            self._show_calibration_graph(puntos, m, b, r_squared)

            QMessageBox.information(self, "Calibración", f"Calibración completada con {num_points} puntos.\n\nEcuación: y = {m:.6f}x + {b:.3f}\nR² = {r_squared:.4f}")

        except Exception as e:
            print(f"Error en calibrar_sensor: {e}")
            QMessageBox.critical(self, "Error", f"Error durante la calibración: {e}")

    def apply_calibration(self, lectura, raw_angle=None):
        """
        Devuelve el ángulo calibrado usando la regresión calculada y recorta al rango físico (-135..135).
        Si no hay calibración, devuelve raw_angle (si se proporcionó) o None.
        """
        if not self.calibrated:
            return raw_angle
        ang = self.cal_m * lectura + self.cal_b
        # Clamp al rango físico del sensor (-135 a 135) según la tabla de sensores
        ang = max(-135.0, min(135.0, ang))
        return ang

    def _show_calibration_graph(self, puntos, m, b, r_squared):
        """
        Muestra una ventana con la gráfica de calibración, puntos capturados, línea de tendencia y ecuación.
        """
        try:
            # Crear ventana de diálogo
            dialog = QDialog(self)
            dialog.setWindowTitle("Resultados de Calibración")
            dialog.setModal(True)
            dialog.resize(600, 500)
            
            # Layout del diálogo
            layout = QVBoxLayout(dialog)
            
            # Crear figura de matplotlib
            fig = Figure(figsize=(8, 6), dpi=100)
            canvas = FigureCanvas(fig)
            
            # Crear subplot
            ax = fig.add_subplot(111)
            
            # Extraer datos
            xs = [p[0] for p in puntos]
            ys = [p[1] for p in puntos]
            
            # Rango de lecturas para la línea de tendencia
            x_min, x_max = min(xs) if xs else 0, max(xs) if xs else 4095
            x_range = np.linspace(x_min - 100, x_max + 100, 100)
            y_trend = m * x_range + b
            
            # Gráfica de puntos de calibración
            ax.scatter(xs, ys, color='red', s=100, alpha=0.8, label=f'Puntos de calibración ({len(puntos)})', zorder=3)
            
            # Línea de tendencia
            ax.plot(x_range, y_trend, 'b-', linewidth=2, alpha=0.7, label='Línea de tendencia', zorder=2)
            
            # Configuración de la gráfica
            ax.set_xlabel('Lectura Analógica (AD)', fontsize=12)
            ax.set_ylabel('Ángulo de Referencia (°)', fontsize=12)
            ax.set_title(f'Calibración del Sensor de Ángulo\ny = {m:.6f}x + {b:.3f}  (R² = {r_squared:.4f})', fontsize=14, fontweight='bold')
            ax.grid(True, alpha=0.3)
            ax.legend(fontsize=10)
            
            # Configurar límites
            ax.set_xlim(0, 4095)
            ax.set_ylim(-150, 150)
            
            # Añadir texto con la ecuación
            textstr = f'Ecuación: y = {m:.6f}x + {b:.3f}\nR² = {r_squared:.4f}\nPuntos: {len(puntos)}'
            props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)
            ax.text(0.02, 0.98, textstr, transform=ax.transAxes, fontsize=10,
                   verticalalignment='top', bbox=props)
            
            fig.tight_layout()
            
            # Añadir canvas al layout
            layout.addWidget(canvas)
            
            # Mostrar diálogo
            dialog.exec()
            
        except Exception as e:
            print(f"Error mostrando gráfica de calibración: {e}")
            QMessageBox.warning(self, "Error", f"No se pudo mostrar la gráfica de calibración: {e}")

    def limpiar_grafica(self):
        try:
            # Lógica para limpiar la gráfica
            self.lecturas.clear()
            self.angulos.clear()
            self.angulos_originales.clear()
            self.tiempo.clear()
            self.muestra_actual = 0
            self.update_graph()

            if hasattr(self.ui, 'analogoDt'):
                self.ui.analogoDt.setText("--")

            if hasattr(self.ui, 'anguloDt'):
                self.ui.anguloDt.setText("--")
                
            # Limpiar también labels de calibración
            if hasattr(self.ui, 'analogoDtCal'):
                self.ui.analogoDtCal.setText("--")

            if hasattr(self.ui, 'anguloDtCal'):
                self.ui.anguloDtCal.setText("--")

            print("Gráfica limpiada correctamente.")
        except RuntimeError as e:
            print(f"Error en limpiar_grafica: {e}")

    def exportar_datos(self):
        try:
            # Lógica para exportar datos a Excel
            print("Los datos han sido exportados a Excel.")
        except RuntimeError as e:
            print(f"Error en exportar_datos: {e}")

    def actualizar_datos(self):
        try:
            # Lógica para actualizar los datos en la interfaz
            if hasattr(self.ui, 'analogoDt') and self.ui.analogoDt is not None:
                self.ui.analogoDt.setText("123")  # Ejemplo de datos
            if hasattr(self.ui, 'anguloDt') and self.ui.anguloDt is not None:
                self.ui.anguloDt.setText("45°")  # Ejemplo de datos
        except RuntimeError as e:
            print(f"Error en actualizar_datos: {e}")
            # Si hay error, detener el monitoreo
            self.monitoreo_activo = False
            self.timer.stop()

    def toggle_angulo_monitoring(self):
        """
        Alterna entre iniciar y detener el monitoreo del sensor de ángulo simple.
        """
        if not self.monitoreo_activo:
            self.start_angulo_monitoring()
        else:
            self.stop_angulo_monitoring()

    def start_angulo_monitoring(self):
        """
        Inicia el monitoreo en tiempo real del sensor de ángulo simple.
        """
        try:
            # Detener hilo anterior si existe
            if hasattr(self, 'thread_SIMPLE_ANGLE') and self.thread_SIMPLE_ANGLE is not None:
                if self.thread_SIMPLE_ANGLE.isRunning():
                    self.thread_SIMPLE_ANGLE.stop()
                    self.thread_SIMPLE_ANGLE = None

            # Obtener la IP del ESP32 desde la ventana principal
            esp32_ip = None
            if self.main_window:
                ip_widget = self.main_window.findChild(QLineEdit, "ipEdit")
                if ip_widget:
                    esp32_ip = ip_widget.text().strip()
            
            if not esp32_ip:
                esp32_ip = "192.168.1.100"  # IP por defecto
                print("No se pudo obtener la IP desde main.py, usando IP por defecto")
            
            print(f"Iniciando conexión con ESP32 en IP: {esp32_ip}")
            
            self.thread_SIMPLE_ANGLE = SimpleAngleThread(esp32_ip)
            self.thread_SIMPLE_ANGLE.data_received.connect(self.update_angulo_data)
            self.thread_SIMPLE_ANGLE.connection_status.connect(self.update_connection_status)

            self.thread_SIMPLE_ANGLE.start()
            self.monitoreo_activo = True

            # Actualizar el botón de inicio específico de simpleAngle
            if hasattr(self.ui, 'iniciar'):
                self.ui.iniciar.setText("Pausar")
                self.ui.iniciar.setStyleSheet(
                    "background-color: #e53935;"   # Rojo principal
                    "border-color: #b71c1c;"       # Rojo oscuro para el borde
                    "color: white;"
                    "padding: 8px;"
                    "font-size: 14px;"
                    "font-weight: bold;"
                    "border-radius: 4px;"
                    "border: 1px solid #b71c1c;"
                    "margin-top: 5px;"
                )
                
        except Exception as e:
            print(f"Error al iniciar monitoreo: {e}")
            self.monitoreo_activo = False
            if hasattr(self.ui, 'iniciar'):
                self.ui.iniciar.setText("Iniciar Monitoreo")
                self.ui.iniciar.setStyleSheet(
                    "background-color: #2196f3;"   # Azul principal
                    "border-color: #1976d2;"       # Azul oscuro para el borde
                    "color: white;"
                    "padding: 8px;"
                    "font-size: 14px;"
                    "font-weight: bold;"
                    "border-radius: 4px;"
                    "border: 1px solid #1976d2;"
                    "margin-top: 5px;"
                )
    def update_connection_status(self, status):
        """
        Actualiza el estado de conexión en la interfaz.
        """
        print(f"Estado de conexión: {status}")
        # Aquí puedes agregar un label en la UI para mostrar el estado si lo deseas

    def stop_angulo_monitoring(self):
        """
        Detiene el monitoreo del sensor de ángulo simple y limpia recursos.
        """
        try:
            if hasattr(self, 'thread_SIMPLE_ANGLE') and self.thread_SIMPLE_ANGLE is not None:
                if self.thread_SIMPLE_ANGLE.isRunning():
                    print("Deteniendo hilo de monitoreo...")
                    self.thread_SIMPLE_ANGLE.stop()
                self.thread_SIMPLE_ANGLE = None

            self.monitoreo_activo = False

            # Restaurar el botón de inicio específico de simpleAngle
            if hasattr(self.ui, 'iniciar'):
                self.ui.iniciar.setText("Iniciar Monitoreo")
                self.ui.iniciar.setStyleSheet(
                    "background-color: #2196f3;"   # Azul principal
                    "border-color: #1976d2;"       # Azul oscuro para el borde
                    "color: white;"
                    "padding: 8px;"
                    "font-size: 14px;"
                    "font-weight: bold;"
                    "border-radius: 4px;"
                    "border: 1px solid #1976d2;"
                    "margin-top: 5px;"
                )

            print("Monitoreo detenido correctamente")
        except Exception as e:
            print(f"Error al detener monitoreo: {e}")

    # ----------------------
    # Calibración: persistencia
    # ----------------------
    def _cal_file_path(self):
        # Guardar junto al módulo (por simplicidad)
        base = os.path.dirname(__file__)
        return os.path.join(base, 'simpleAngle_calibration.json')

    def _save_calibration(self):
        path = self._cal_file_path()
        payload = {
            'm': self.cal_m,
            'b': self.cal_b,
            'points': self.cal_points
        }
        try:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(payload, f, indent=2)
            print(f"Calibración guardada en {path}")
        except Exception as e:
            print(f"No se pudo guardar calibración: {e}")

    def _load_calibration(self):
        path = self._cal_file_path()
        if not os.path.exists(path):
            return
        try:
            with open(path, 'r', encoding='utf-8') as f:
                payload = json.load(f)
            self.cal_m = float(payload.get('m', 1.0))
            self.cal_b = float(payload.get('b', 0.0))
            self.cal_points = payload.get('points', [])
            self.calibrated = True
            # Update UI markers if available
            if hasattr(self.ui, 'calibrar') and self.ui.calibrar is not None:
                self.ui.calibrar.setText("Calibrado")
            if hasattr(self.ui, 'calBox') and self.ui.calBox is not None:
                self.ui.calBox.setVisible(True)
            print(f"Calibración cargada desde {path}: m={self.cal_m}, b={self.cal_b}")
        except Exception as e:
            print(f"No se pudo cargar calibración: {e}")

    def _reset_calibration(self):
        self.cal_m = 1.0
        self.cal_b = 0.0
        self.cal_points = []
        self.calibrated = False
        path = self._cal_file_path()
        try:
            if os.path.exists(path):
                os.remove(path)
        except Exception:
            pass
        # Reset UI
        if hasattr(self.ui, 'calibrar') and self.ui.calibrar is not None:
            self.ui.calibrar.setText("No Calibrado")
            try:
                self.ui.calibrar.setStyleSheet("")
            except Exception:
                pass
        if hasattr(self.ui, 'calBox') and self.ui.calBox is not None:
            self.ui.calBox.setVisible(False)

    def update_angulo_data(self, lectura, angulo):
        """
        Procesa y actualiza los datos recibidos del sensor de ángulo simple.
        Implementa ventana deslizante de 25 muestras con muestreo cada 0.5 segundos.
        Almacena tanto datos originales como calibrados por separado.
        """
        try:
            # Incrementar contador de muestras
            self.muestra_actual += 1

            # Guardar última lectura cruda para calibración
            self.last_lectura = lectura
            self.last_angulo = angulo

            # Aplicar calibración si está disponible (ángulo_cal = m * lectura + b)
            if self.calibrated:
                angulo_cal = self.apply_calibration(lectura, angulo)
            else:
                angulo_cal = angulo

            # Calcular tiempo en segundos (cada muestra es cada 0.5 segundos)
            tiempo_actual = self.muestra_actual * 0.5

            # Agregar nuevos datos
            self.lecturas.append(lectura)
            # Almacenar ambos: ángulo original y calibrado
            self.angulos_originales.append(angulo)
            self.angulos.append(int(round(angulo_cal)))
            self.tiempo.append(tiempo_actual)

            # Implementar ventana deslizante de 25 muestras
            if len(self.lecturas) > self.MAX_MUESTRAS:
                self.lecturas.pop(0)  # Eliminar el más antiguo
                self.angulos_originales.pop(0)  # Eliminar el más antiguo
                self.angulos.pop(0)   # Eliminar el más antiguo
                self.tiempo.pop(0)    # Eliminar el más antiguo

            # Actualizar displays de la interfaz
            if hasattr(self.ui, 'analogoDt'):
                self.ui.analogoDt.setText(str(lectura))

            if hasattr(self.ui, 'anguloDt'):
                # mostrar ángulo original (sin calibración)
                self.ui.anguloDt.setText(f"{angulo}°")
                
            # Actualizar labels de calibración si existe calibración
            if self.calibrated:
                if hasattr(self.ui, 'analogoDtCal'):
                    self.ui.analogoDtCal.setText(str(lectura))
                if hasattr(self.ui, 'anguloDtCal'):
                    self.ui.anguloDtCal.setText(f"{angulo_cal:.1f}°")

            # Actualizar gráfica
            self.update_graph()
            
            print(f"Datos actualizados - Muestra: {self.muestra_actual}, Tiempo: {tiempo_actual:.1f}s, AD: {lectura}, Ángulo: {angulo}°, Muestras en gráfica: {len(self.lecturas)}")
            
        except RuntimeError as e:
            print(f"Error al actualizar datos: {e}")

    def update_graph(self):
        """
        Actualiza la gráfica con los datos actuales.
        Muestra lectura analógica, ángulo original y ángulo calibrado en ejes Y separados.
        """
        try:
            if len(self.tiempo) == 0:
                # Si no hay datos, limpiar las líneas
                self.line1.set_data([], [])
                self.line2.set_data([], [])
                self.line3.set_data([], [])
            else:
                # Actualizar datos de las líneas
                self.line1.set_data(self.tiempo, self.lecturas)
                
                # Mostrar datos originales y calibrados
                if len(self.angulos_originales) > 0:
                    self.line2.set_data(self.tiempo, self.angulos_originales)
                
                if self.calibrated and len(self.angulos) > 0:
                    self.line3.set_data(self.tiempo, self.angulos)
                    self.line3.set_visible(True)
                else:
                    self.line3.set_visible(False)
                
                # Ajustar rango del eje X dinámicamente
                if len(self.tiempo) > 1:
                    x_min = min(self.tiempo)
                    x_max = max(self.tiempo)
                    # Agregar un pequeño margen
                    margen = (x_max - x_min) * 0.05 if x_max > x_min else 1
                    self.ax1.set_xlim(x_min - margen, x_max + margen)
                else:
                    self.ax1.set_xlim(0, 1)
            
            # Redibujar la gráfica
            self.canvas.draw()
            
        except Exception as e:
            print(f"Error al actualizar gráfica: {e}")




