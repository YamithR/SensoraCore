from PySide6.QtCore import QThread, Signal, QTimer
from PySide6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy, QMessageBox, QInputDialog, QFileDialog
import socket
import time
import os
import json
import io
from datetime import datetime
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class UltrasonicThread(QThread):
    data = Signal(float, float)  # distancia_cm, dt_ms
    status = Signal(str)

    def __init__(self, esp32_ip: str, port: int = 8080):
        super().__init__()
        self.esp32_ip = esp32_ip
        self.port = port
        self._running = False
        self._stopping = False
        self.sock = None  # type: ignore[assignment]

    def run(self):
        self._running = True
        last_ts = None
        try:
            self.status.emit(f"Conectando a {self.esp32_ip}:{self.port}...")
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.settimeout(5)
            self.sock.connect((self.esp32_ip, self.port))
            # Seleccionar modo ultrasónico
            self.sock.sendall(b"MODO:DISTANCIA_ULTRA")
            resp = self.sock.recv(64).decode(errors="ignore").strip()
            if "DISTANCIA_ULTRA_OK" not in resp:
                self.status.emit("ESP32 no acept modo DISTANCIA_ULTRA")
                return
            self.status.emit("Monitoreo Ultrasnico iniciado")
            self.sock.settimeout(3)
            buffer = ""
            while self._running:
                try:
                    chunk = self.sock.recv(128)
                    if not chunk:
                        break
                    buffer += chunk.decode(errors="ignore")
                    while "\n" in buffer:
                        line, buffer = buffer.split("\n", 1)
                        line = line.strip()
                        if not line:
                            continue
                        # Esperado: ULTRA_CM:<float>
                        try:
                            if ":" in line:
                                k, v = line.split(":", 1)
                                if k.strip().upper() == "ULTRA_CM":
                                    dist = float(v.strip())
                                    now = time.time()
                                    dt_ms = (now - last_ts) * 1000.0 if last_ts else 0.0
                                    last_ts = now
                                    self.data.emit(dist, dt_ms)
                        except Exception:
                            pass
                except socket.timeout:
                    continue
                except Exception as e:
                    if not self._stopping:
                        self.status.emit(f"Error socket ULTRA: {e}")
                    break
        except Exception as e:
            self.status.emit(f"Error de conexión: {e}")
        finally:
            try:
                if self.sock:
                    if not self._stopping:
                        try:
                            self.sock.sendall(b"STOP")
                        except Exception:
                            pass
                    try:
                        self.sock.close()
                    except Exception:
                        pass
            finally:
                self.sock = None
                self.status.emit("Desconectado")

    def stop(self):
        self._stopping = True
        self._running = False
        if self.sock:
            try:
                self.sock.sendall(b"STOP")
            except Exception:
                pass
            try:
                self.sock.close()
            except Exception:
                pass
        self.wait(2000)


class UltrasonicLogic(QWidget):
    """
    Logica para sensor ultrasonico HC-SR04.
    - Conecta al ESP32 (MODO:DISTANCIA_ULTRA)
    - Muestra distancia cruda y calibrada
    - Grfica de distancia en el tiempo
    - Calibracin lineal (y = m*x + b) y exportacin a Excel/CSV
    """

    def __init__(self, ui_widget, main_window=None):
        super().__init__()
        if ui_widget is None:
            raise ValueError("ui_widget no puede ser None")
        self.ui = ui_widget
        self.main_window = main_window

        # Estado
        self.thread: UltrasonicThread | None = None
        self.monitoring = False
        self.cal = {"m": 1.0, "b": 0.0, "ok": False, "points": []}
        self._load_calibration()

        # Series para grfica
        self.time_idx: list[float] = []
        self.dist_raw: list[float] = []
        self.dist_cal: list[float] = []

        # Botones
        if hasattr(self.ui, "iniciarBt"):
            self.ui.iniciarBt.clicked.connect(self.toggle)
        if hasattr(self.ui, "limpiarBt"):
            self.ui.limpiarBt.clicked.connect(self.limpiar)
        if hasattr(self.ui, "calibrarBt"):
            self.ui.calibrarBt.clicked.connect(self.calibrar)
        if hasattr(self.ui, "exportarBt"):
            self.ui.exportarBt.clicked.connect(self.exportar)

        # Grfica
        self.figure = Figure(figsize=(7, 4), tight_layout=True)
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)
        self.ax.set_xlabel("Tiempo (s)")
        self.ax.set_ylabel("Distancia (cm)")
        self.ax.grid(True, alpha=0.3, linestyle='--')
        self.line_raw, = self.ax.plot([], [], color="#1f77b4", label="Distancia cruda")
        self.line_cal, = self.ax.plot([], [], color="#ff7f0e", linestyle="--", label="Distancia calibrada")
        self.ax.legend(loc='upper right', fontsize=8)

        if hasattr(self.ui, 'grapWid') and self.ui.grapWid is not None:
            if not self.ui.grapWid.layout():
                lay = QVBoxLayout()
                lay.setContentsMargins(5, 5, 5, 5)
                lay.setSpacing(0)
                self.ui.grapWid.setLayout(lay)
            lay = self.ui.grapWid.layout()
            while lay.count():
                ch = lay.takeAt(0)
                if ch.widget():
                    ch.widget().deleteLater()
            self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            lay.addWidget(self.canvas)

        # Visibilidad de calibracin
        if hasattr(self.ui, 'calBox') and self.ui.calBox is not None:
            self.ui.calBox.setVisible(self.cal["ok"])
        if hasattr(self.ui, 'calibrarBt'):
            self.ui.calibrarBt.setText("Calibrado" if self.cal["ok"] else "No Calibrado")

        self._t0 = None

    # ---- Control ----
    def toggle(self):
        if self.monitoring:
            self.stop()
        else:
            self.start()

    def start(self):
        try:
            ip = self._get_ip()
            if not ip:
                QMessageBox.information(self, "ESP32", "Ingrese la IP del ESP32 en el campo correspondiente.")
                return
            if self.thread and self.thread.isRunning():
                self.thread.stop()
                self.thread = None
            self.thread = UltrasonicThread(ip)
            self.thread.data.connect(self._on_data)
            self.thread.status.connect(self._on_status)
            self.thread.start()
            self.monitoring = True
            self._t0 = None
            if hasattr(self.ui, "iniciarBt"):
                self.ui.iniciarBt.setText("Pausar")
        except Exception as e:
            QMessageBox.critical(self, "Ultrasonic", f"No se pudo iniciar: {e}")

    def stop(self):
        try:
            self.monitoring = False
            if self.thread:
                if self.thread.isRunning():
                    self.thread.stop()
                self.thread = None
            if hasattr(self.ui, "iniciarBt"):
                self.ui.iniciarBt.setText("Iniciar Monitoreo")
        except Exception:
            pass

    def cleanup(self):
        self.stop()

    # ---- Datos ----
    def _on_status(self, msg: str):
        print(f"[ULTRA] {msg}")

    def _apply_cal(self, d: float) -> float:
        if not self.cal["ok"]:
            return d
        return self.cal["m"] * d + self.cal["b"]

    def _on_data(self, distancia_cm: float, dt_ms: float):
        # Tiempo (s)
        if self._t0 is None:
            self._t0 = time.time()
        t = time.time() - self._t0
        self.time_idx.append(t)
        self.dist_raw.append(distancia_cm)
        dcal = self._apply_cal(distancia_cm)
        self.dist_cal.append(dcal)

        # Ventana deslizante (100 mes recientes)
        for arr in (self.time_idx, self.dist_raw, self.dist_cal):
            if len(arr) > 200:
                arr.pop(0)

        # Labels
        if hasattr(self.ui, 'DistanciaDt'):
            self.ui.DistanciaDt.setText(f"{distancia_cm:.1f} cm")
        if hasattr(self.ui, 'TiempoDeRespuestaDt'):
            self.ui.TiempoDeRespuestaDt.setText(f"{dt_ms:.0f} ms")
        if hasattr(self.ui, 'calBox') and self.ui.calBox is not None and self.cal["ok"]:
            if hasattr(self.ui, 'DistanciaDtCalibrada'):
                self.ui.DistanciaDtCalibrada.setText(f"{dcal:.1f} cm")

        # Grfica
        self.line_raw.set_data(self.time_idx, self.dist_raw)
        self.line_cal.set_data(self.time_idx, self.dist_cal)
        if self.time_idx:
            xmin, xmax = self.time_idx[0], self.time_idx[-1]
            if xmax - xmin < 1:
                xmax = xmin + 1
            self.ax.set_xlim(xmin, xmax)
            # Auto Y en base a cruda
            ymin = min(self.dist_raw) if self.dist_raw else 0
            ymax = max(self.dist_raw) if self.dist_raw else 1
            if ymin == ymax:
                ymax = ymin + 1
            pad = max(1, 0.05 * (ymax - ymin))
            self.ax.set_ylim(ymin - pad, ymax + pad)
        self.canvas.draw()

    # ---- Utilidad ----
    def limpiar(self):
        """Limpia series, resetea labels y refresca la gráfica."""
        try:
            self.time_idx.clear()
            self.dist_raw.clear()
            self.dist_cal.clear()

            # Reset líneas
            self.line_raw.set_data([], [])
            self.line_cal.set_data([], [])

            # Reset labels si existen
            if hasattr(self.ui, 'DistanciaDt'):
                self.ui.DistanciaDt.setText("--")
            if hasattr(self.ui, 'TiempoDeRespuestaDt'):
                self.ui.TiempoDeRespuestaDt.setText("--")
            if hasattr(self.ui, 'DistanciaDtCalibrada'):
                self.ui.DistanciaDtCalibrada.setText("--")

            # Opcional: reset ejes
            self.ax.set_xlim(0, 1)
            self.ax.set_ylim(0, 1)
            self.canvas.draw()
        except Exception:
            pass

    # ---- Calibracin ----
    def calibrar(self):
        if not self.time_idx:
            QMessageBox.information(self, "Calibracin", "Inicia el monitoreo para obtener lecturas.")
            return
        # Pedir n puntos
        num_points, ok = QInputDialog.getInt(self, "Calibracin", "Cue1ntos puntos? (2-10)", 3, 2, 10)
        if not ok:
            return
        puntos: list[tuple[float, float]] = []  # (lectura, distancia real)
        for i in range(1, num_points + 1):
            # Tomar ltima lectura cruda como X
            x = self.dist_raw[-1] if self.dist_raw else 0.0
            y, ok2 = QInputDialog.getDouble(
                self,
                f"Punto {i}/{num_points}",
                "Ingresa distancia real medida (cm) para la lectura actual:",
                float(x), 0.0, 1000.0, 1,
            )
            if not ok2:
                break
            puntos.append((float(x), float(y)))
        if len(puntos) < 2:
            QMessageBox.warning(self, "Calibracin", "Se requieren al menos 2 puntos.")
            return
        # Ajuste lineal y = m x + b
        xs = [p[0] for p in puntos]
        ys = [p[1] for p in puntos]
        n = len(xs)
        mean_x = sum(xs) / n
        mean_y = sum(ys) / n
        num = sum((xs[i] - mean_x) * (ys[i] - mean_y) for i in range(n))
        den = sum((xs[i] - mean_x) ** 2 for i in range(n))
        if den == 0:
            QMessageBox.warning(self, "Calibracin", "Varianza cero en lecturas.")
            return
        m = num / den
        b = mean_y - m * mean_x
        self.cal["m"], self.cal["b"], self.cal["ok"], self.cal["points"] = float(m), float(b), True, puntos
        if hasattr(self.ui, 'calBox') and self.ui.calBox is not None:
            self.ui.calBox.setVisible(True)
        if hasattr(self.ui, 'calibrarBt'):
            self.ui.calibrarBt.setText("Calibrado")
        self._save_calibration()

    # ---- Exportar ----
    def exportar(self):
        try:
            if not self.time_idx:
                QMessageBox.information(self, "Exportar", "No hay datos para exportar.")
                return
            ts = datetime.now().strftime('%Y%m%d_%H%M%S')
            default_name = f"Ultrasonic_{ts}.xlsx"
            filename, _ = QFileDialog.getSaveFileName(
                self,
                "Exportar datos a Excel",
                default_name,
                "Archivos Excel (*.xlsx);;Archivos CSV (*.csv);;Todos los archivos (*.*)"
            )
            if not filename:
                return
            if filename.lower().endswith('.xlsx'):
                self._export_to_excel(filename)
            else:
                self._export_to_csv(filename if filename.lower().endswith('.csv') else filename + '.csv')
            QMessageBox.information(self, "Exportar", f"Datos exportados exitosamente a:\n{filename}")
        except Exception as e:
            QMessageBox.critical(self, "Exportar", f"Error al exportar: {e}")

    def _export_to_excel(self, filename: str):
        try:
            import pandas as pd
            from openpyxl import Workbook
            from openpyxl.styles import Font, PatternFill, Alignment
            from openpyxl.utils.dataframe import dataframe_to_rows

            wb = Workbook()
            ws_data = wb.active
            ws_data.title = "Datos del Sensor"

            data = {
                'Tiempo (s)': self.time_idx.copy(),
                'Distancia (cm)': self.dist_raw.copy(),
            }
            if any(self.cal["ok"] for _ in [0]) and self.dist_cal:
                data['Distancia Calibrada (cm)'] = self.dist_cal.copy()
            df = pd.DataFrame(data)
            for r in dataframe_to_rows(df, index=False, header=True):
                ws_data.append(r)

            header_font = Font(bold=True, color="FFFFFF")
            header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
            for cell in ws_data[1]:
                cell.font = header_font
                cell.fill = header_fill
                cell.alignment = Alignment(horizontal="center")

            # Autoajuste de columnas
            for column in ws_data.columns:
                max_length = 0
                col_letter = column[0].column_letter
                for cell in column:
                    try:
                        max_length = max(max_length, len(str(cell.value)))
                    except Exception:
                        pass
                ws_data.column_dimensions[col_letter].width = min(max_length + 2, 18)

            # Metadatos
            ws_meta = wb.create_sheet("Metadatos")
            intervalo = self._infer_interval()
            metadata = [
                ["INFORMACIN DEL EXPERIMENTO", ""],
                ["Fecha de exportacin", datetime.now().strftime("%d/%m/%Y %H:%M:%S")],
                ["Sensor", "Ultrasonido (HC-SR04)"],
                ["Muestras totales", len(self.time_idx)],
                ["Intervalo de muestreo", f"{intervalo:.3f} segundos"],
                ["Tiempo total", f"{len(self.time_idx) * intervalo:.1f} segundos"],
                ["", ""],
                ["RANGO DE DATOS", ""],
                ["Distancia min (cm)", f"{min(self.dist_raw):.2f}" if self.dist_raw else 0],
                ["Distancia max (cm)", f"{max(self.dist_raw):.2f}" if self.dist_raw else 0],
                ["", ""],
                ["CALIBRACIN", ""],
                ["Estado", "Calibrado" if self.cal["ok"] else "No calibrado"],
                ["Ecuacin", f"y = {self.cal['m']:.6f}x + {self.cal['b']:.3f}" if self.cal["ok"] else "--"],
                ["Puntos", len(self.cal["points"]) if self.cal["points"] else 0],
            ]
            for row in metadata:
                ws_meta.append(row)

            # Grfica
            ws_graph = wb.create_sheet("Grfica")
            graph_image = self._create_export_graph()
            if graph_image:
                from openpyxl.drawing.image import Image
                img = Image(graph_image)
                img.width = 1000
                img.height = 600
                ws_graph['A1'] = "ULTRASONIDO - DATOS EXPORTADOS"
                ws_graph['A1'].font = Font(bold=True, size=16, color="2F5597")
                ws_graph['A1'].alignment = Alignment(horizontal="center")
                ws_graph['A3'] = f"Generada: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
                ws_graph['A4'] = f"Muestras: {len(self.time_idx)}"
                if self.cal["ok"]:
                    ws_graph['A5'] = f"Calibracin: y = {self.cal['m']:.6f}x + {self.cal['b']:.3f}"
                ws_graph.add_image(img, 'A7')
                ws_graph.column_dimensions['A'].width = 60

            wb.save(filename)
            if graph_image:
                try:
                    os.unlink(graph_image)
                except Exception:
                    pass
        except ImportError:
            QMessageBox.warning(self, "Exportar", "Libreras de Excel no disponibles. Exportando a CSV...")
            self._export_to_csv(filename.replace('.xlsx', '.csv'))
        except Exception as e:
            raise Exception(f"Error al crear archivo Excel: {e}")

    def _export_to_csv(self, filename: str):
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                f.write(f"# Ultrasonic exportado: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
                f.write("# t,Distancia,DistanciaCalibrada\n")
                for i, t in enumerate(self.time_idx):
                    d = self.dist_raw[i] if i < len(self.dist_raw) else ''
                    dc = self.dist_cal[i] if i < len(self.dist_cal) else ''
                    f.write(f"{t:.2f},{d},{dc}\n")
        except Exception as e:
            raise Exception(f"Error al crear archivo CSV: {e}")

    def _create_export_graph(self):
        try:
            from matplotlib.figure import Figure as MplFigure
            fig = MplFigure(figsize=(12, 7), dpi=150, facecolor='white')
            ax = fig.add_subplot(111)
            ax.set_title("Ultrasonido - Distancia vs Tiempo")
            ax.set_xlabel("Tiempo (s)")
            ax.set_ylabel("Distancia (cm)")
            ax.grid(True, alpha=0.3, linestyle='--')
            if self.time_idx:
                ax.plot(self.time_idx, self.dist_raw, color='#1f77b4', linewidth=2.0, label='Cruda')
                if self.dist_cal:
                    ax.plot(self.time_idx, self.dist_cal, color='#ff7f0e', linestyle='--', linewidth=2.0, label='Calibrada')
                ax.legend(loc='upper right')

            import tempfile
            img_buffer = io.BytesIO()
            fig.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight', facecolor='white', edgecolor='none')
            img_buffer.seek(0)
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
            temp_file.write(img_buffer.getvalue())
            temp_file.close()
            img_buffer.close()
            fig.clear()
            return temp_file.name
        except Exception as e:
            print(f"Error creando grfica de exportacin: {e}")
            return None

    # ---- Persistencia ----
    def _cal_path(self):
        base = os.path.dirname(__file__)
        return os.path.join(base, 'ultrasonic_calibration.json')

    def _save_calibration(self):
        try:
            with open(self._cal_path(), 'w', encoding='utf-8') as f:
                json.dump(self.cal, f, indent=2)
            print("Calibracin Ultrasonic guardada")
        except Exception as e:
            print(f"No se pudo guardar calibracin Ultrasonic: {e}")

    def _load_calibration(self):
        try:
            path = self._cal_path()
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    self.cal = json.load(f)
        except Exception as e:
            print(f"No se pudo cargar calibracin Ultrasonic: {e}")

    # ---- Aux ----
    def _get_ip(self) -> str | None:
        try:
            from PySide6.QtWidgets import QLineEdit
            if self.main_window:
                ip_widget = self.main_window.findChild(QLineEdit, "ipEdit")
                if ip_widget:
                    return ip_widget.text().strip()
        except Exception:
            pass
        return None

    # ---- Cálculo auxiliar ----
    def _infer_interval(self) -> float:
        """Estima el intervalo de muestreo a partir del eje de tiempo (segundos)."""
        try:
            if len(self.time_idx) < 2:
                return 0.1
            diffs = [self.time_idx[i] - self.time_idx[i-1] for i in range(1, len(self.time_idx))]
            # Evitar valores atípicos simples
            diffs = [d for d in diffs if d > 0]
            return sum(diffs) / len(diffs) if diffs else 0.1
        except Exception:
            return 0.1
