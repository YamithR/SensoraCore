from __future__ import annotations

import os
import time
import socket
from typing import Optional

from PySide6.QtCore import QObject, Signal, Slot
from PySide6.QtWidgets import QWidget, QPushButton, QLabel, QLCDNumber, QProgressBar, QMessageBox, QFileDialog, QLineEdit


class _BrightnessThread(QObject):
    sig_status = Signal(str)
    sig_error = Signal(str)
    sig_sample = Signal(int, float, float)  # adc, volt, ts

    def __init__(self, ip: str, port: int = 8080, interval_ms: int = 200):
        super().__init__()
        self.ip = ip
        self.port = port
        self.interval_ms = max(50, int(interval_ms))
        self._running = False
        self._stopping = False
        self.sock: Optional[socket.socket] = None

    def start(self):
        if self._running:
            return
        from threading import Thread
        self._stopping = False
        self._running = True
        Thread(target=self._run, daemon=True).start()

    def stop(self):
        self._stopping = True
        self._running = False
        try:
            if self.sock:
                try:
                    self.sock.sendall(b"BR_STOP\n")
                except Exception:
                    pass
                try:
                    self.sock.close()
                except Exception:
                    pass
        finally:
            self.sock = None

    def _run(self):
        try:
            self.sig_status.emit("[BR] Conectando...")
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5)
            s.connect((self.ip, self.port))
            self.sock = s
            s.sendall(b"MODO:BRIGHTNESS\n")
            resp = s.recv(128).decode(errors="ignore").strip()
            if "BRIGHTNESS_OK" not in resp:
                self.sig_error.emit("[BR] ESP32 no acepto BRIGHTNESS")
                return
            s.sendall(f"BR_START:{self.interval_ms}\n".encode())
            self.sig_status.emit("[BR] Streaming iniciado")
            s.settimeout(1.0)
            buf = ""
            while self._running:
                try:
                    chunk = s.recv(256)
                    if not chunk:
                        break
                    buf += chunk.decode(errors="ignore")
                    while "\n" in buf:
                        line, buf = buf.split("\n", 1)
                        line = line.strip()
                        if not line:
                            continue
                        # SENSOR:LDR,ADC:<n>,VOLT:<v>
                        try:
                            kv = {}
                            for part in line.replace(";", ",").split(","):
                                if ":" in part:
                                    k, v = part.split(":", 1)
                                    kv[k.strip().upper()] = v.strip()
                            adc = int(float(kv.get("ADC", "0")))
                            volt = float(kv.get("VOLT", str((adc/4095.0)*3.3)))
                            self.sig_sample.emit(adc, volt, time.time())
                        except Exception:
                            pass
                except socket.timeout:
                    continue
                except Exception as e:
                    if not self._stopping:
                        self.sig_error.emit(f"[BR] Error socket: {e}")
                    break
        except Exception as e:
            self.sig_error.emit(f"[BR] Error de conexion: {e}")
        finally:
            try:
                if self.sock:
                    try:
                        self.sock.sendall(b"BR_STOP\n")
                    except Exception:
                        pass
                    try:
                        self.sock.close()
                    except Exception:
                        pass
            finally:
                self.sock = None
                self.sig_status.emit("[BR] Desconectado")


class BrightnessLogic(QObject):
    def __init__(self, ui_widget: QWidget, main_window):
        super().__init__(ui_widget)
        self.ui = ui_widget
        self.main = main_window

        # Widgets
        self.btn_start: QPushButton = self.ui.findChild(QPushButton, "iniciarBt")
        self.btn_clear: QPushButton = self.ui.findChild(QPushButton, "limpiarBt")
        self.btn_export: QPushButton = self.ui.findChild(QPushButton, "exportarBt")
        self.lbl_adc: QLabel = self.ui.findChild(QLabel, "LecturaLDRDt")
        self.lcd_pct: QLCDNumber = self.ui.findChild(QLCDNumber, "PorcentajeDeLuz")
        self.bar_pct: QProgressBar = self.ui.findChild(QProgressBar, "BarraIndicadorDeLuz")

        # Estado
        self.interval_ms = 200
        self.thread: Optional[_BrightnessThread] = None
        self.monitoring = False
        self._t0: Optional[float] = None
        self._series = {"t": [], "adc": [], "volt": [], "pct": []}

        # Init
        self._init_widgets()
        if self.btn_start:
            self.btn_start.clicked.connect(self._toggle)
        if self.btn_clear:
            self.btn_clear.clicked.connect(self._clear)
        if self.btn_export:
            self.btn_export.clicked.connect(self._export_excel)

    def _init_widgets(self):
        if self.bar_pct:
            self.bar_pct.setRange(0, 100)
            self.bar_pct.setValue(0)
        if self.lcd_pct:
            self.lcd_pct.display(0)
        if self.lbl_adc:
            self.lbl_adc.setText("--")

    def _get_ip(self) -> Optional[str]:
        ip_edit = self.main.findChild(QLineEdit, "ipEdit") if self.main else None
        if not ip_edit:
            QMessageBox.critical(self.ui, "Error", "No se encontró el campo IP (ipEdit)")
            return None
        ip = ip_edit.text().strip()
        if not ip:
            QMessageBox.warning(self.ui, "Advertencia", "Ingrese la IP del ESP32.")
            return None
        return ip

    def _toggle(self):
        if not self.monitoring:
            ip = self._get_ip()
            if not ip:
                return
            self.thread = _BrightnessThread(ip, interval_ms=self.interval_ms)
            self.thread.sig_status.connect(lambda m: print(m))
            self.thread.sig_error.connect(lambda m: print(m))
            self.thread.sig_sample.connect(self._on_sample)
            self.thread.start()
            self.monitoring = True
            if self.btn_start:
                self.btn_start.setText("Pausar")
            self._t0 = time.time()
        else:
            self._stop()

    def _stop(self):
        try:
            if self.thread:
                self.thread.stop()
        finally:
            self.thread = None
            self.monitoring = False
            if self.btn_start:
                self.btn_start.setText("Iniciar Monitoreo")

    @Slot(int, float, float)
    def _on_sample(self, adc: int, volt: float, ts: float):
        # Percent 0..100 directo desde ADC
        pct = int(round(max(0.0, min(100.0, (adc * 100.0 / 4095.0)))))
        if self.lbl_adc:
            self.lbl_adc.setText(str(adc))
        if self.lcd_pct:
            self.lcd_pct.display(pct)
        if self.bar_pct:
            self.bar_pct.setValue(pct)

        if self._t0 is None:
            self._t0 = ts
        self._series["t"].append(ts - self._t0)
        self._series["adc"].append(adc)
        self._series["volt"].append(volt)
        self._series["pct"].append(pct)

    def _clear(self):
        for k in self._series:
            self._series[k].clear()
        self._init_widgets()

    def _export_excel(self):
        # Sin gráfica, solo datos + metadatos
        try:
            from openpyxl import Workbook
            from openpyxl.styles import Font, PatternFill, Alignment

            path, _ = QFileDialog.getSaveFileName(self.ui, "Exportar a Excel", None, "Excel (*.xlsx)")
            if not path:
                return

            wb = Workbook()
            ws = wb.active
            ws.title = "Datos"
            headers = ["t_s", "adc", "volt", "percent"]
            ws.append(headers)
            for c in ws[1]:
                c.font = Font(bold=True)
                c.fill = PatternFill("solid", fgColor="DDEEFF")
                c.alignment = Alignment(horizontal="center")
            for t, a, v, p in zip(self._series["t"], self._series["adc"], self._series["volt"], self._series["pct"]):
                ws.append([t, a, v, p])

            meta = wb.create_sheet("Metadatos")
            from datetime import datetime
            meta.append(["Fecha", datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
            meta.append(["Intervalo (ms)", self.interval_ms])
            meta.append(["Descripcion", "Lectura de LDR → % de luz (0..100)"])

            # auto ancho simple
            for sheet in (ws, meta):
                for col in sheet.columns:
                    width = 10
                    for cell in col:
                        width = max(width, len(str(cell.value)) if cell.value is not None else 0)
                    sheet.column_dimensions[col[0].column_letter].width = min(30, width + 2)

            wb.save(path)
            QMessageBox.information(self.ui, "Exportar", f"Exportado: {path}")
        except ImportError:
            QMessageBox.critical(self.ui, "Exportar", "Falta librería openpyxl.")
        except Exception as e:
            QMessageBox.critical(self.ui, "Exportar", f"Error exportando: {e}")

    def cleanup(self):
        self._stop()
