from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import QWidget, QMessageBox
import socket


class OpticalSpeedThread(QThread):
    data = Signal(float, float, int)  # rpm_left, rpm_right, speed_percent (-100..100)
    status = Signal(str)

    def __init__(self, esp32_ip: str, port: int = 8080):
        super().__init__()
        self.esp32_ip = esp32_ip
        self.port = port
        self._running = False
        self._stopping = False
        self.sock = None

    def run(self):
        self._running = True
        try:
            self.status.emit(f"Conectando a {self.esp32_ip}:{self.port}...")
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.settimeout(5)
            self.sock.connect((self.esp32_ip, self.port))
            self.sock.sendall(b"MODO:OPTICAL_SPEED")
            resp = self.sock.recv(64).decode(errors="ignore").strip()
            if "OPTICAL_SPEED_OK" not in resp:
                self.status.emit("ESP32 no acepto modo OPTICAL_SPEED")
                return
            self.status.emit("Monitoreo Optical Speed iniciado")
            self.sock.settimeout(3)
            buffer = ""
            while self._running:
                try:
                    chunk = self.sock.recv(256)
                    if not chunk:
                        break
                    buffer += chunk.decode(errors="ignore")
                    while "\n" in buffer:
                        line, buffer = buffer.split("\n", 1)
                        line = line.strip()
                        if not line:
                            continue
                        try:
                            parts = [p.strip() for p in line.split(',')]
                            kv = {}
                            for p in parts:
                                if ':' in p:
                                    k, v = p.split(':', 1)
                                    kv[k.strip().upper()] = v.strip()
                            rpm_l = float(kv.get('RPM_L', '0'))
                            rpm_r = float(kv.get('RPM_R', '0'))
                            spd = int(float(kv.get('SPEED', '0')))
                            self.data.emit(rpm_l, rpm_r, spd)
                        except Exception:
                            pass
                except socket.timeout:
                    continue
                except Exception as e:
                    if not self._stopping:
                        self.status.emit(f"Error socket OPT: {e}")
                    break
        except Exception as e:
            self.status.emit(f"Error de conexion: {e}")
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

    def set_speed(self, percent: int):
        try:
            if self.sock and self._running:
                cmd = f"SET_SPEED:{percent}\n".encode()
                self.sock.sendall(cmd)
        except Exception:
            pass


class OpticalSpeedLogic(QWidget):
    def __init__(self, ui_widget, main_window=None):
        super().__init__()
        if ui_widget is None:
            raise ValueError("ui_widget no puede ser None")
        self.ui = ui_widget
        self.main_window = main_window
        self.thread: OpticalSpeedThread | None = None
        self.monitoring = False
        self._speed = 0  # -100..100 (negativo = reversa)

        if hasattr(self.ui, 'iniciarBt'):
            self.ui.iniciarBt.clicked.connect(self.toggle)
        if hasattr(self.ui, 'SubirVelocidadBt'):
            self.ui.SubirVelocidadBt.clicked.connect(self._on_inc)
        if hasattr(self.ui, 'BajarVelocidadBt'):
            self.ui.BajarVelocidadBt.clicked.connect(self._on_dec)

        self._update_speed_label()

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
            self.thread = OpticalSpeedThread(ip)
            self.thread.data.connect(self._on_data)
            self.thread.status.connect(self._on_status)
            self.thread.start()
            self.monitoring = True
            if hasattr(self.ui, 'iniciarBt'):
                self.ui.iniciarBt.setText('Pausar')
            self._send_speed()
        except Exception as e:
            QMessageBox.critical(self, "Optical Speed", f"No se pudo iniciar: {e}")

    def stop(self):
        try:
            self.monitoring = False
            if self.thread:
                if self.thread.isRunning():
                    self.thread.stop()
                self.thread = None
            if hasattr(self.ui, 'iniciarBt'):
                self.ui.iniciarBt.setText('Iniciar Monitoreo')
        except Exception:
            pass

    def cleanup(self):
        self.stop()

    def _on_data(self, rpm_l: float, rpm_r: float, speed: int):
        if hasattr(self.ui, 'RPMizquierdaDt'):
            self.ui.RPMizquierdaDt.setText(f"{rpm_l:.0f}")
        if hasattr(self.ui, 'RPMderechaDt'):
            self.ui.RPMderechaDt.setText(f"{rpm_r:.0f}")
        self._speed = max(-100, min(100, int(speed)))
        self._update_speed_label()

    def _on_status(self, msg: str):
        print(f"[OPT] {msg}")

    def _on_inc(self):
        self._speed = min(100, self._speed + 10)
        self._update_speed_label()
        self._send_speed()

    def _on_dec(self):
        self._speed = max(-100, self._speed - 10)
        self._update_speed_label()
        self._send_speed()

    def _update_speed_label(self):
        if hasattr(self.ui, 'AumentosdeVelocidadDt'):
            sign = '+' if self._speed >= 0 else ''
            self.ui.AumentosdeVelocidadDt.setText(
                f"<html><head/><body><p align=\"center\"><span style=\" font-size:26pt;\">{sign}{self._speed}</span></p></body></html>"
            )

    def _send_speed(self):
        if self.thread and self.thread.isRunning():
            self.thread.set_speed(self._speed)

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
