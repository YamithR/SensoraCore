from PySide6.QtCore import QTimer, QThread, Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QSizePolicy
from .simpleAngle_ui import Ui_simpleAngle
import socket
import time
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
            
            # Líneas de la gráfica
            self.line1, = self.ax1.plot([], [], 'b-', label='Lectura AD', linewidth=2, alpha=0.8)
            self.line2, = self.ax2.plot([], [], 'r-', label='Ángulo (°)', linewidth=2, alpha=0.8)
            
            # Leyenda compacta
            lines1, labels1 = self.ax1.get_legend_handles_labels()
            lines2, labels2 = self.ax2.get_legend_handles_labels()
            self.ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=9)
            
            # Ajustar márgenes para que se vea bien en el widget
            self.figure.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.15)

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
        try:
            # Lógica para calibrar el sensor
            print("El sensor ha sido calibrado.")
            if hasattr(self.ui, 'calibrar') and self.ui.calibrar is not None:
                self.ui.calibrar.setText("Calibrado")
                self.ui.calibrar.setStyleSheet(
                    "font-size: 14px;"
                    "font-weight: bold;"
                    "color: rgb(0, 60, 0);"
                    "padding: 8px;"
                    "background-color: rgb(200, 255, 200);"
                    "border-radius: 4px;"
                    "border: 1px solid rgb(0, 120, 0);"
                    "margin-top: 5px;"
                )
            if hasattr(self.ui, 'calBox') and self.ui.calBox is not None:
                self.ui.calBox.setVisible(True)

        except RuntimeError as e:
            print(f"Error en calibrar_sensor: {e}")

    def limpiar_grafica(self):
        try:
            # Lógica para limpiar la gráfica
            self.lecturas.clear()
            self.angulos.clear()
            self.tiempo.clear()
            self.muestra_actual = 0
            self.update_graph()

            if hasattr(self.ui, 'analogoDt'):
                self.ui.analogoDt.setText("--")

            if hasattr(self.ui, 'anguloDt'):
                self.ui.anguloDt.setText("--")

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

    def update_angulo_data(self, lectura, angulo):
        """
        Procesa y actualiza los datos recibidos del sensor de ángulo simple.
        Implementa ventana deslizante de 25 muestras con muestreo cada 0.5 segundos.
        """
        try:
            # Incrementar contador de muestras
            self.muestra_actual += 1
            
            # Calcular tiempo en segundos (cada muestra es cada 0.5 segundos)
            tiempo_actual = self.muestra_actual * 0.5
            
            # Agregar nuevos datos
            self.lecturas.append(lectura)
            self.angulos.append(angulo)
            self.tiempo.append(tiempo_actual)

            # Implementar ventana deslizante de 25 muestras
            if len(self.lecturas) > self.MAX_MUESTRAS:
                self.lecturas.pop(0)  # Eliminar el más antiguo
                self.angulos.pop(0)   # Eliminar el más antiguo
                self.tiempo.pop(0)    # Eliminar el más antiguo

            # Actualizar displays de la interfaz
            if hasattr(self.ui, 'analogoDt'):
                self.ui.analogoDt.setText(str(lectura))

            if hasattr(self.ui, 'anguloDt'):
                self.ui.anguloDt.setText(f"{angulo}°")

            # Actualizar gráfica
            self.update_graph()
            
            print(f"Datos actualizados - Muestra: {self.muestra_actual}, Tiempo: {tiempo_actual:.1f}s, AD: {lectura}, Ángulo: {angulo}°, Muestras en gráfica: {len(self.lecturas)}")
            
        except RuntimeError as e:
            print(f"Error al actualizar datos: {e}")

    def update_graph(self):
        """
        Actualiza la gráfica con los datos actuales.
        Muestra lectura analógica y ángulo en ejes Y separados.
        """
        try:
            if len(self.tiempo) == 0:
                # Si no hay datos, limpiar las líneas
                self.line1.set_data([], [])
                self.line2.set_data([], [])
            else:
                # Actualizar datos de las líneas
                self.line1.set_data(self.tiempo, self.lecturas)
                self.line2.set_data(self.tiempo, self.angulos)
                
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




