# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'infrared.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QGroupBox,
    QHBoxLayout, QLabel, QPushButton, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_infrared(object):
    def setupUi(self, infrared):
        if not infrared.objectName():
            infrared.setObjectName(u"infrared")
        infrared.resize(737, 638)
        infrared.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"border: 1px solid rgb(221, 221, 221);\n"
"border-radius: 5px;\n"
"color: rgb(0, 0, 0);")
        self.gridLayout_4 = QGridLayout(infrared)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.frame = QFrame(infrared)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_6 = QGridLayout(self.frame)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.diagrama = QGroupBox(self.frame)
        self.diagrama.setObjectName(u"diagrama")
        self.diagrama.setMaximumSize(QSize(300, 16777215))
        self.diagrama.setStyleSheet(u"QGroupBox {\n"
"    color: rgb(102, 102, 102) ;\n"
"    background-color: #f8f9fa;        \n"
"    border-radius: 6px;\n"
"    border: 1px solid rgb(177, 177, 177) ;\n"
"    border-radius: 5px;\n"
"    margin-top: 15px; /* espacio para el t\u00edtulo */\n"
"    font: bold 12px;\n"
"}\n"
"QGroupBox::title {\n"
"    subcontrol-origin: margin;\n"
"    subcontrol-position: top left ;\n"
"    left: 20px;\n"
"    background-color: rgba(255, 255, 255, 255);\n"
"	padding: 2px;\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"")
        self.gridLayout_2 = QGridLayout(self.diagrama)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.dibujo = QLabel(self.diagrama)
        self.dibujo.setObjectName(u"dibujo")
        self.dibujo.setMinimumSize(QSize(0, 0))
        self.dibujo.setMaximumSize(QSize(16777215, 170))
        self.dibujo.setStyleSheet(u"")

        self.gridLayout_2.addWidget(self.dibujo, 0, 0, 1, 1)

        self.nota = QLabel(self.diagrama)
        self.nota.setObjectName(u"nota")
        self.nota.setMaximumSize(QSize(999, 210))
        self.nota.setStyleSheet(u"        font-size: 13px;                    /* Tama\u00f1o menor para nota */\n"
"        color: #856404;                     /* Color \u00e1mbar oscuro */\n"
"        background-color: #fff3cd;          /* Fondo \u00e1mbar claro (alerta) */\n"
"        border: 1px solid #ffeaa7;          /* Borde \u00e1mbar */\n"
"        border-radius: 4px;                 /* Esquinas redondeadas */\n"
"        padding: 8px;                       /* Espacio interno */\n"
"        margin-top: 5px;                    /* Separaci\u00f3n superior */\n"
"")

        self.gridLayout_2.addWidget(self.nota, 1, 0, 1, 1)


        self.gridLayout_6.addWidget(self.diagrama, 3, 0, 1, 1)

        self.titulo = QLabel(self.frame)
        self.titulo.setObjectName(u"titulo")
        self.titulo.setMaximumSize(QSize(16777215, 45))
        self.titulo.setStyleSheet(u"        background-color: #f8f9fa;       \n"
"        border: 2px solid #dee2e6;         \n"
"        border-radius: 6px;              \n"
"   ")

        self.gridLayout_6.addWidget(self.titulo, 0, 0, 1, 3)

        self.descripcion = QLabel(self.frame)
        self.descripcion.setObjectName(u"descripcion")
        self.descripcion.setMaximumSize(QSize(16777215, 60))
        self.descripcion.setStyleSheet(u"        background-color: #f8f9fa;       \n"
"        border: 2px solid #dee2e6;         \n"
"        border-radius: 6px;              \n"
"   ")

        self.gridLayout_6.addWidget(self.descripcion, 1, 0, 1, 3)

        self.controles = QGroupBox(self.frame)
        self.controles.setObjectName(u"controles")
        self.controles.setMinimumSize(QSize(0, 100))
        self.controles.setMaximumSize(QSize(16777215, 100))
        self.controles.setSizeIncrement(QSize(0, 0))
        self.controles.setStyleSheet(u"QGroupBox {\n"
"    color: rgb(102, 102, 102) ;\n"
"    background-color: #f8f9fa;        \n"
"    border-radius: 6px;\n"
"    border: 1px solid rgb(177, 177, 177) ;\n"
"    border-radius: 5px;\n"
"    margin-top: 15px; /* espacio para el t\u00edtulo */\n"
"    font: bold 12px;\n"
"}\n"
"QGroupBox::title {\n"
"    subcontrol-origin: margin;\n"
"    subcontrol-position: top left ;\n"
"    left: 20px;\n"
"    background-color: rgba(255, 255, 255, 255);\n"
"	padding: 2px;\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"")
        self.horizontalLayout = QHBoxLayout(self.controles)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.botones = QWidget(self.controles)
        self.botones.setObjectName(u"botones")
        self.botones.setMaximumSize(QSize(16777215, 65))
        self.verticalLayout = QVBoxLayout(self.botones)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.iniciarBt = QPushButton(self.botones)
        self.iniciarBt.setObjectName(u"iniciarBt")
        self.iniciarBt.setStyleSheet(u"QPushButton {\n"
"    font-size: 14px;                    \n"
"    font-weight: bold;              \n"
"    color: rgb(0, 0, 0);\n"
"    padding: 8px;                 \n"
"    background-color: rgb(236, 236, 236);          \n"
"    border-radius: 4px;            \n"
"    border: 1px solid rgb(0, 0, 0);      \n"
"    margin-top: 5px;         \n"
"}\n"
"\n"
"/* Hover: verde suave */\n"
"QPushButton:hover {\n"
"    background-color: rgb(220, 255, 220);     /* Verde muy claro */\n"
"    border: 1px solid rgb(0, 128, 0);          /* Verde intenso */\n"
"    color: rgb(0, 100, 0);                     /* Verde oscuro para texto */\n"
"}\n"
"\n"
"/* Pressed: verde m\u00e1s profundo */\n"
"QPushButton:pressed {\n"
"    background-color: rgb(200, 240, 200);     /* Verde m\u00e1s saturado */\n"
"    border: 1px solid rgb(0, 100, 0);          /* Borde m\u00e1s oscuro */\n"
"    color: rgb(0, 80, 0);                      /* Texto a\u00fan m\u00e1s profundo */\n"
"}")

        self.verticalLayout.addWidget(self.iniciarBt)


        self.horizontalLayout.addWidget(self.botones)


        self.gridLayout_6.addWidget(self.controles, 2, 0, 1, 1)

        self.info = QGroupBox(self.frame)
        self.info.setObjectName(u"info")
        self.info.setMinimumSize(QSize(400, 0))
        self.info.setStyleSheet(u"QGroupBox {\n"
"    color: rgb(102, 102, 102) ;\n"
"    background-color: #f8f9fa;        \n"
"    border-radius: 6px;\n"
"    border: 1px solid rgb(177, 177, 177) ;\n"
"    border-radius: 5px;\n"
"    margin-top: 15px; /* espacio para el t\u00edtulo */\n"
"    font: bold 12px;\n"
"}\n"
"QGroupBox::title {\n"
"    subcontrol-origin: margin;\n"
"    subcontrol-position: top left ;\n"
"    left: 20px;\n"
"    background-color: rgba(255, 255, 255, 255);\n"
"	padding: 2px;\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"")
        self.gridLayout_5 = QGridLayout(self.info)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.SensorInfrarojo = QWidget(self.info)
        self.SensorInfrarojo.setObjectName(u"SensorInfrarojo")
        self.SensorInfrarojo.setMaximumSize(QSize(99999, 16777215))
        self.verticalLayout_2 = QVBoxLayout(self.SensorInfrarojo)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.SensorInfrarojoLabel = QLabel(self.SensorInfrarojo)
        self.SensorInfrarojoLabel.setObjectName(u"SensorInfrarojoLabel")
        self.SensorInfrarojoLabel.setMinimumSize(QSize(0, 60))
        self.SensorInfrarojoLabel.setMaximumSize(QSize(16777215, 60))
        self.SensorInfrarojoLabel.setStyleSheet(u"font-size: 14px;\n"
"font-weight: bold;\n"
"color: #b85c00;                    /* Naranja quemado para texto */\n"
"padding: 8px;\n"
"background-color: #ffe5cc;         /* Fondo naranja claro */\n"
"border-radius: 6px;\n"
"border: 1px solid #f5c199;         /* Borde suave */\n"
"margin-top: 6px;")

        self.verticalLayout_2.addWidget(self.SensorInfrarojoLabel)

        self.EstadoDeSensorInfrarojo_ON_OFF = QLabel(self.SensorInfrarojo)
        self.EstadoDeSensorInfrarojo_ON_OFF.setObjectName(u"EstadoDeSensorInfrarojo_ON_OFF")
        self.EstadoDeSensorInfrarojo_ON_OFF.setMinimumSize(QSize(0, 120))
        self.EstadoDeSensorInfrarojo_ON_OFF.setMaximumSize(QSize(16777215, 120))
        self.EstadoDeSensorInfrarojo_ON_OFF.setStyleSheet(u"font-size: 14px;                    /* Tama\u00f1o menor para informaci\u00f3n secundaria */\n"
"font-weight: bold;                 /* Texto en negrita */\n"
"color: #4f4f4f;                    /* Gris oscuro para buen contraste */\n"
"padding: 8px;                      /* Espacio interno menor */\n"
"background-color: #f9f9f9;         /* Fondo blanco suave */\n"
"border-radius: 4px;                /* Esquinas redondeadas menores */\n"
"border: 1px solid #e0e0e0;         /* Borde gris claro */\n"
"margin-top: 5px;                   /* Separaci\u00f3n superior */")

        self.verticalLayout_2.addWidget(self.EstadoDeSensorInfrarojo_ON_OFF)

        self.datosSobreSensor = QLabel(self.SensorInfrarojo)
        self.datosSobreSensor.setObjectName(u"datosSobreSensor")
        self.datosSobreSensor.setMaximumSize(QSize(99999, 99999))
        self.datosSobreSensor.setStyleSheet(u"font-size: 14px;                    /* Tama\u00f1o menor para informaci\u00f3n secundaria */\n"
"color: #4f4f4f;                    /* Gris oscuro para buen contraste */\n"
"padding: 8px;                      /* Espacio interno menor */\n"
"background-color: #f9f9f9;         /* Fondo blanco suave */\n"
"border-radius: 4px;                /* Esquinas redondeadas menores */\n"
"border: 1px solid #e0e0e0;         /* Borde gris claro */\n"
"margin-top: 5px;                   /* Separaci\u00f3n superior */")

        self.verticalLayout_2.addWidget(self.datosSobreSensor)


        self.gridLayout_5.addWidget(self.SensorInfrarojo, 0, 0, 1, 1)


        self.gridLayout_6.addWidget(self.info, 2, 1, 2, 2)


        self.gridLayout_4.addWidget(self.frame, 0, 0, 1, 1)


        self.retranslateUi(infrared)

        QMetaObject.connectSlotsByName(infrared)
    # setupUi

    def retranslateUi(self, infrared):
        infrared.setWindowTitle(QCoreApplication.translate("infrared", u"Form", None))
        self.diagrama.setTitle(QCoreApplication.translate("infrared", u"Diagrama de Conexiones", None))
        self.dibujo.setText(QCoreApplication.translate("infrared", u"<html><head/><body><pre style=\" margin-top:12px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:140%;\"><span style=\" font-family:'Courier New','monospace'; font-size:12px; color:#495057;\">\u250c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2510</span></pre><pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:140%;\"><span style=\" font-family:'Courier New','monospace'; font-size:12px; color:#495057;\">\u2502  ESP32 DevKit V1  -&gt; Sensor     \u2502</span></pre><pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:140%;\"><span style=\" font-family:'Courier New','monospace'; font-size:12px; color:#495057;\">\u2502  3V3  \u25cb \u2190\u2500\u2500"
                        " N/A	      (+)  \u2502</span></pre><pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:140%;\"><span style=\" font-family:'Courier New','monospace'; font-size:12px; color:#495057;\">\u2502  GND  \u25cb \u2190\u2500\u2500 GND Cable Azul (-)  \u2502</span></pre><pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:140%;\"><span style=\" font-family:'Courier New','monospace'; font-size:12px; color:#495057;\">\u2502  D25  \u25cb \u2190\u2500\u2500 OUT Cable Negro (D) \u2502</span></pre><pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:140%;\"><span style=\" font-family:'Courier New','monospace'; font-size:12px; color:#495057;\">|---------------------------------|</span></pre><pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0"
                        "; text-indent:0px; line-height:140%;\"><span style=\" font-family:'Courier New','monospace'; font-size:12px; color:#495057;\">\u2502  Fuente de Voltaje -&gt; Sensor    \u2502</span></pre><pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:140%;\"><span style=\" font-family:'Courier New','monospace'; font-size:12px; color:#495057;\">\u2502  5V   </span><span style=\" font-family:'Courier New','monospace'; font-size:12px; color:#495057;\">\u25cb \u2190\u2500\u2500 5V Cable Marr\u00f3n    </span><span style=\" font-family:'Courier New','monospace'; font-size:12px; color:#495057;\"> \u2502</span></pre><pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:140%;\"><span style=\" font-family:'Courier New','monospace'; font-size:12px; color:#495057;\">\u2514\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500"
                        "\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2518</span></pre></body></html>", None))
        self.nota.setText(QCoreApplication.translate("infrared", u"<html><head/><body><p align=\"justify\"><span style=\" font-size:9pt;\">\ud83d\udca1 </span><span style=\" font-size:9pt; font-weight:700;\">Nota:</span><span style=\" font-size:9pt;\"> Aseg\u00farate de conectar los <br/>componentes correctamente antes de <br/>iniciar el monitoreo</span></p><p align=\"justify\"><span style=\" font-size:9pt;\">\ud83d\udd0c</span><span style=\" font-size:9pt; font-weight:700;\">Voltaje: </span><span style=\" font-size:9pt;\">La entrada de alimentaci\u00f3n<br/>del sensor tiene un rango de acci\u00f3n de <br/>5v a 12v, sientete libre de experimentar<br/>con los voltajes dentro de este limite.</span></p><p align=\"justify\"><span style=\" font-size:9pt;\">\ud83d\udd39</span><span style=\" font-size:9pt; font-weight:700;\">GND: </span><span style=\" font-size:9pt;\">Asegurate de compartir la <br/>tierra entre en microcontrolador, la<br/>fuente y el sensor.</span></p></body></html>", None))
        self.titulo.setText(QCoreApplication.translate("infrared", u"<html><head/><body><p align=\"center\"><span style=\" font-size:22pt; font-weight:700; color:#007bff;\">Monitoreo de Proximidad por IR</span></p></body></html>", None))
        self.descripcion.setText(QCoreApplication.translate("infrared", u"<html><head/><body><p align=\"center\"><span style=\" font-size:10pt; font-style:italic;\">Monitorea en tiempo real la se\u00f1al digital del sensor infrarrojo y ofrece informaci\u00f3n did\u00e1ctica para su caracterizaci\u00f3n.</span></p></body></html>", None))
        self.controles.setTitle(QCoreApplication.translate("infrared", u"Controles", None))
        self.iniciarBt.setText(QCoreApplication.translate("infrared", u"Iniciar Monitoreo", None))
        self.info.setTitle(QCoreApplication.translate("infrared", u"Info", None))
        self.SensorInfrarojoLabel.setText(QCoreApplication.translate("infrared", u"<html><head/><body><p align=\"center\"><span style=\" font-size:11pt;\">IRSensor</span></p></body></html>", None))
        self.EstadoDeSensorInfrarojo_ON_OFF.setText(QCoreApplication.translate("infrared", u"<html><head/><body><p align=\"center\"><span style=\" font-size:11pt;\">On/Off</span></p></body></html>", None))
        self.datosSobreSensor.setText(QCoreApplication.translate("infrared", u"<html><head/><body><p align=\"justify\"><span style=\" font-size:9pt; font-style:italic;\">El </span><span style=\" font-size:9pt; font-weight:700; font-style:italic;\">E18 D80NK</span><span style=\" font-size:9pt; font-style:italic;\"> es un </span><span style=\" font-size:9pt; font-weight:700; font-style:italic;\">sensor fotoel\u00e9ctrico infrarrojo reflectivo</span><span style=\" font-size:9pt; font-style:italic;\"> que<br/>detecta objetos cercanos sin contacto f\u00edsico. Funciona emitiendo un<br/>rayo infrarrojo que rebota en superficies pr\u00f3ximas; si el rebote es<br/>detectado, el sensor activa una se\u00f1al digital (ON/OFF). Esto lo<br/>convierte en una herramienta ideal para sistemas que requieren<br/>detecci\u00f3n sin interferencia mec\u00e1nica.</span></p><p><span style=\" font-family:'SEGOE','sans-serif'; font-size:9pt; color:#7d7d7d;\">- Distancia de detecci\u00f3n:\u00a03 cm a 80 cm (ajustable con un tornillo)</span></p><p><span style=\" font-family:'SEGOE','sans-serif'; font-size:9pt; col"
                        "or:#7d7d7d;\">- Salida:\u00a0Digital (ON/OFF)</span></p><p><span style=\" font-family:'SEGOE','sans-serif'; font-size:9pt; color:#7d7d7d;\">- Tipo de sensor:\u00a0Reflectivo infrarrojo</span></p><p><span style=\" font-family:'SEGOE','sans-serif'; font-size:9pt; color:#7d7d7d;\">- Conexi\u00f3n:\u00a03 pines (VCC, GND, OUT)</span></p></body></html>", None))
    # retranslateUi

