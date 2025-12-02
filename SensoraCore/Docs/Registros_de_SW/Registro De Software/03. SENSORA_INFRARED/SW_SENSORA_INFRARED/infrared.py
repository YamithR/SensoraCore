from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import QWidget, QMessageBox
from .infrared_ui import Ui_infrared  # Solo para tipos/nombres
import socket


class InfraredThread(QThread):
    state = Signal(bool)
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
        try:
            self.status.emit(f"Conectando a {self.esp32_ip}:{self.port}...")
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.settimeout(5)
            self.sock.connect((self.esp32_ip, self.port))
            self.sock.sendall(b"MODO:DISTANCIA_IR")
            resp = self.sock.recv(64).decode(errors="ignore").strip()
            if "DISTANCIA_IR_OK" not in resp:
                self.status.emit("ESP32 no aceptó modo DISTANCIA_IR")
                return
            self.status.emit("Monitoreo IR iniciado")
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
                        # Formato: IR_DIGITAL:True/False
                        try:
                            if ":" in line:
                                key, val = line.split(":", 1)
                                if key.strip().upper() == "IR_DIGITAL":
                                    on = val.strip().lower() in ("true", "1", "on")
                                    self.state.emit(on)
                        except Exception:
                            pass
                except socket.timeout:
                    continue
                except Exception as e:
                    # Si estamos deteniendo intencionalmente, no emitir error ruidoso
                    if not self._stopping:
                        self.status.emit(f"Error socket IR: {e}")
                    break
        except Exception as e:
            self.status.emit(f"Error de conexión: {e}")
        finally:
            try:
                if self.sock:
                    # Enviar STOP solo si no se está deteniendo intencionalmente (ya se envía en stop())
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
                # Notificar al firmware antes de cerrar
                self.sock.sendall(b"STOP")
            except Exception:
                pass
            try:
                self.sock.close()
            except Exception:
                pass
        self.wait(2000)


class InfraredLogic(QWidget):
    """
    Lógica para sensor de proximidad infrarrojo (digital ON/OFF).
    Conecta al ESP32 (MODO:DISTANCIA_IR) y actualiza el label de estado.
    """

    def __init__(self, ui_widget, main_window=None):
        super().__init__()
        if ui_widget is None:
            raise ValueError("ui_widget no puede ser None")
        self.ui = ui_widget
        self.main_window = main_window
        self.thread: InfraredThread | None = None
        self.monitoring = False

        if hasattr(self.ui, "iniciarBt"):
            self.ui.iniciarBt.clicked.connect(self.toggle)

    # Estado inicial: respetar estilo/texto por defecto del UI (no cambiar hasta iniciar monitoreo)

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
            self.thread = InfraredThread(ip)
            self.thread.state.connect(self._on_state)
            self.thread.status.connect(self._on_status)
            self.thread.start()
            self.monitoring = True
            if hasattr(self.ui, "iniciarBt"):
                self.ui.iniciarBt.setText("Pausar")
        except Exception as e:
            QMessageBox.critical(self, "Infrared", f"No se pudo iniciar: {e}")

    def stop(self):
        try:
            self.monitoring = False
            if self.thread:
                if self.thread.isRunning():
                    self.thread.stop()
                self.thread = None
            if hasattr(self.ui, "iniciarBt"):
                self.ui.iniciarBt.setText("Iniciar Monitoreo")
            # Restaurar estado visual por defecto del label
            label_name = "EstadoDeSensorInfrarojo_ON_OFF"
            if hasattr(self.ui, label_name):
                lbl = getattr(self.ui, label_name)
                lbl.setText("On/Off")
                lbl.setStyleSheet("")
        except Exception:
            pass

    def cleanup(self):
        self.stop()

    # Handlers
    def _on_state(self, on: bool):
        self._set_state(on)

    def _on_status(self, msg: str):
        print(f"[IR] {msg}")

    def _set_state(self, on: bool):
        label_name = "EstadoDeSensorInfrarojo_ON_OFF"
        if hasattr(self.ui, label_name) and self.monitoring:
            lbl = getattr(self.ui, label_name)
            lbl.setText("ON" if on else "OFF")
            # Estilos simples de estado
            if on:
                lbl.setStyleSheet("background-color:#d4edda; color:#155724; font-weight:bold; padding:8px;")
            else:
                lbl.setStyleSheet("background-color:#f8d7da; color:#721c24; font-weight:bold; padding:8px;")

    # Aux
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
