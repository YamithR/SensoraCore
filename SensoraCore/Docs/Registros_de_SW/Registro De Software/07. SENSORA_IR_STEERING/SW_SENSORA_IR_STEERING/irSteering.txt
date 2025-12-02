from __future__ import annotations

from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import QWidget, QMessageBox, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QDoubleSpinBox, QSpinBox, QPushButton, QCheckBox
import socket


class IrSteeringThread(QThread):
    data = Signal(str, float, int, int, int, float, float)  # bits5, err, out_l, out_r, base_speed, rpm_l, rpm_r
    status = Signal(str)

    def __init__(self, esp32_ip: str, port: int = 8080):
        super().__init__()
        self.esp32_ip = esp32_ip
        self.port = port
        self._running = False
        self._stopping = False
        self.sock: socket.socket | None = None

    def run(self):
        self._running = True
        try:
            self.status.emit(f"Conectando a {self.esp32_ip}:{self.port}...")
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.settimeout(5)
            self.sock.connect((self.esp32_ip, self.port))
            self.sock.sendall(b"MODO:IR_STEERING")
            resp = self.sock.recv(64).decode(errors="ignore").strip()
            if "IR_STEERING_OK" not in resp:
                self.status.emit("ESP32 no acepto modo IR_STEERING")
                return
            self.status.emit("Monitoreo IR Steering iniciado")
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
                            bits = kv.get('SENS', kv.get('IR', '00000'))
                            err = float(kv.get('ERR', '0'))
                            out_l = int(float(kv.get('OUT_L', '0')))
                            out_r = int(float(kv.get('OUT_R', '0')))
                            base = int(float(kv.get('SPEED', '0')))
                            rpm_l = float(kv.get('RPM_L', '0'))
                            rpm_r = float(kv.get('RPM_R', '0'))
                            self.data.emit(bits, err, out_l, out_r, base, rpm_l, rpm_r)
                        except Exception:
                            pass
                except socket.timeout:
                    continue
                except Exception as e:
                    if not self._stopping:
                        self.status.emit(f"Error socket IR: {e}")
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

    def set_base(self, percent: int):
        try:
            if self.sock and self._running:
                cmd = f"SET_BASE:{percent}\n".encode()
                self.sock.sendall(cmd)
        except Exception:
            pass

    def set_pid(self, kp: float, ki: float, kd: float):
        try:
            if self.sock and self._running:
                cmd = f"SET_PID:Kp={kp:.3f},Ki={ki:.3f},Kd={kd:.3f}\n".encode()
                self.sock.sendall(cmd)
        except Exception:
            pass


class PidDialog(QDialog):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self.setWindowTitle("Ajustes PID y Velocidad Base")
        # Estilos acorde a la app (tarjeta clara con acentos)
        self.setStyleSheet(
            """
            QDialog { background: #ffffff; }
            QLabel { font: 12px 'Segoe UI'; color: #222; }
            QDoubleSpinBox, QSpinBox { font: 12px 'Segoe UI'; padding: 6px; }
            QPushButton {
                font: 12px 'Segoe UI'; padding: 6px 12px;
                background: #e7f1ff; color: #004085; border: 1px solid #b8daff; border-radius: 4px;
            }
            QPushButton:hover { background: #d6e9ff; }
            QCheckBox { font: 12px 'Segoe UI'; color: #004085; }
            .title { font: bold 14px 'Segoe UI'; color: #004085; }
            """
        )
        layout = QVBoxLayout(self)

        # KP/KI/KD
        self.kp = QDoubleSpinBox()
        self.kp.setRange(0.0, 10.0)
        self.kp.setSingleStep(0.05)
        self.kp.setValue(1.0)
        self.ki = QDoubleSpinBox()
        self.ki.setRange(0.0, 10.0)
        self.ki.setSingleStep(0.01)
        self.ki.setValue(0.0)
        self.kd = QDoubleSpinBox()
        self.kd.setRange(0.0, 10.0)
        self.kd.setSingleStep(0.05)
        self.kd.setValue(0.5)

        # Base speed
        self.base = QSpinBox()
        self.base.setRange(-100, 100)
        self.base.setValue(40)
        # Live apply
        self.live = QCheckBox("Aplicar en vivo")
        self.live.setChecked(True)

        # Helper to arrange rows
        def add_row(lbl_text: str, w: QWidget):
            h = QHBoxLayout()
            h.addWidget(QLabel(lbl_text))
            h.addWidget(w)
            layout.addLayout(h)

        add_row("Kp", self.kp)
        add_row("Ki", self.ki)
        add_row("Kd", self.kd)
        add_row("Velocidad base (%)", self.base)
        layout.addWidget(self.live)

        btns = QHBoxLayout()
        self.applyBtn = QPushButton("Aplicar")
        self.closeBtn = QPushButton("Cerrar")
        btns.addWidget(self.applyBtn)
        btns.addWidget(self.closeBtn)
        layout.addLayout(btns)


class IrSteeringLogic(QWidget):
    def __init__(self, ui_widget, main_window=None):
        super().__init__()
        if ui_widget is None:
            raise ValueError("ui_widget no puede ser None")
        self.ui = ui_widget
        self.main_window = main_window
        self.thread: IrSteeringThread | None = None
        self.monitoring = False
        self._base = 40
        self._kp, self._ki, self._kd = 1.0, 0.0, 0.5
        self._pid_dialog: PidDialog | None = None

        # Wire buttons
        if hasattr(self.ui, 'iniciarBt'):
            self.ui.iniciarBt.clicked.connect(self.toggle)
        if hasattr(self.ui, 'calibrarBt'):
            # Usamos este botón para abrir el diálogo PID
            self.ui.calibrarBt.setText("PID y Velocidad…")
            self.ui.calibrarBt.clicked.connect(self.open_pid_dialog)

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
            self.thread = IrSteeringThread(ip)
            self.thread.data.connect(self._on_data)
            self.thread.status.connect(self._on_status)
            self.thread.start()
            self.monitoring = True
            if hasattr(self.ui, 'iniciarBt'):
                self.ui.iniciarBt.setText('Pausar')
            # Enviar ajustes iniciales
            self._push_pid()
            self._push_base()
        except Exception as e:
            QMessageBox.critical(self, "IR Steering", f"No se pudo iniciar: {e}")

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
        if self._pid_dialog and self._pid_dialog.isVisible():
            try:
                self._pid_dialog.close()
            except Exception:
                pass

    def open_pid_dialog(self):
        if self._pid_dialog is None:
            self._pid_dialog = PidDialog(self.ui)
            self._pid_dialog.kp.setValue(self._kp)
            self._pid_dialog.ki.setValue(self._ki)
            self._pid_dialog.kd.setValue(self._kd)
            self._pid_dialog.base.setValue(self._base)
            self._pid_dialog.applyBtn.clicked.connect(self._on_pid_apply)
            self._pid_dialog.closeBtn.clicked.connect(self._pid_dialog.close)
            # Live updates
            def live_update():
                if self._pid_dialog and self._pid_dialog.live.isChecked():
                    self._read_pid_dialog()
                    self._push_pid()
                    self._push_base()
            self._pid_dialog.kp.valueChanged.connect(lambda _: live_update())
            self._pid_dialog.ki.valueChanged.connect(lambda _: live_update())
            self._pid_dialog.kd.valueChanged.connect(lambda _: live_update())
            self._pid_dialog.base.valueChanged.connect(lambda _: live_update())
        self._pid_dialog.show()

    def _on_pid_apply(self):
        self._read_pid_dialog()
        self._push_pid()
        self._push_base()

    def _read_pid_dialog(self):
        if not self._pid_dialog:
            return
        self._kp = float(self._pid_dialog.kp.value())
        self._ki = float(self._pid_dialog.ki.value())
        self._kd = float(self._pid_dialog.kd.value())
        self._base = int(self._pid_dialog.base.value())

    def _push_pid(self):
        if self.thread and self.thread.isRunning():
            self.thread.set_pid(self._kp, self._ki, self._kd)

    def _push_base(self):
        if self.thread and self.thread.isRunning():
            self.thread.set_base(self._base)

    def _on_status(self, msg: str):
        print(f"[IR] {msg}")

    def _on_data(self, bits: str, err: float, out_l: int, out_r: int, base: int, rpm_l: float, rpm_r: float):
        # Actualizar etiquetas de sensores (1 activo = verde, 0 = gris)
        lbls = [getattr(self.ui, f"SensorIR{i}", None) for i in range(1, 6)]
        bits = (bits or "00000").strip()
        if len(bits) != 5:
            bits = bits[-5:].rjust(5, '0')
        for i, ch in enumerate(bits):
            lbl = lbls[i]
            if not lbl:
                continue
            if ch == '1':
                lbl.setStyleSheet("background-color: #d4edda; color: #155724; border: 1px solid #c3e6cb; font-weight: bold; padding: 8px;")
            else:
                lbl.setStyleSheet("background-color: #ffffff; color: #333333; border: 1px solid #e0e0e0; padding: 8px;")

        # Mostrar salidas como porcentaje en campos de RPM reutilizados
        if hasattr(self.ui, 'RPMizquierdaDt'):
            # Mostrar RPM real a la izquierda y salida debajo si deseas; por simplicidad, RPM
            self.ui.RPMizquierdaDt.setText(f"{rpm_l:.0f}")
        if hasattr(self.ui, 'RPMderechaDt'):
            self.ui.RPMderechaDt.setText(f"{rpm_r:.0f}")

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
