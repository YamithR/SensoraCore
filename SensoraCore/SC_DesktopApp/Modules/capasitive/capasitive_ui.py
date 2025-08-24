# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'capasitive.ui'
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

class Ui_capasitive(object):
    def setupUi(self, capasitive):
        if not capasitive.objectName():
            capasitive.setObjectName(u"capasitive")
        capasitive.resize(744, 718)
        capasitive.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"border: 1px solid rgb(221, 221, 221);\n"
"border-radius: 5px;\n"
"color: rgb(0, 0, 0);")
        self.gridLayout = QGridLayout(capasitive)
        self.gridLayout.setObjectName(u"gridLayout")
        self.frame = QFrame(capasitive)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_6 = QGridLayout(self.frame)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.descripcion = QLabel(self.frame)
        self.descripcion.setObjectName(u"descripcion")
        self.descripcion.setMaximumSize(QSize(16777215, 60))
        self.descripcion.setStyleSheet(u"        background-color: #f8f9fa;       \n"
"        border: 2px solid #dee2e6;         \n"
"        border-radius: 6px;              \n"
"   ")

        self.gridLayout_6.addWidget(self.descripcion, 1, 0, 1, 3)

        self.titulo = QLabel(self.frame)
        self.titulo.setObjectName(u"titulo")
        self.titulo.setMaximumSize(QSize(16777215, 45))
        self.titulo.setStyleSheet(u"        background-color: #f8f9fa;       \n"
"        border: 2px solid #dee2e6;         \n"
"        border-radius: 6px;              \n"
"   ")

        self.gridLayout_6.addWidget(self.titulo, 0, 0, 1, 3)

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
        self.SensorCapasitivo = QWidget(self.info)
        self.SensorCapasitivo.setObjectName(u"SensorCapasitivo")
        self.SensorCapasitivo.setMaximumSize(QSize(99999, 16777215))
        self.verticalLayout_2 = QVBoxLayout(self.SensorCapasitivo)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.SensorCapasitivoLabel = QLabel(self.SensorCapasitivo)
        self.SensorCapasitivoLabel.setObjectName(u"SensorCapasitivoLabel")
        self.SensorCapasitivoLabel.setMinimumSize(QSize(0, 60))
        self.SensorCapasitivoLabel.setMaximumSize(QSize(16777215, 60))
        self.SensorCapasitivoLabel.setStyleSheet(u"font-size: 14px;                    /* Tama\u00f1o menor para informaci\u00f3n secundaria */\n"
"font-weight: bold;                 /* Texto en negrita */\n"
"color: #31708f;                    /* Azul medio para indicar estado */\n"
"padding: 4px;                      /* Espacio interno menor */\n"
"background-color: #d9edf7;         /* Fondo azul claro */\n"
"border-radius: 4px;                /* Esquinas redondeadas menores */\n"
"border: 1px solid #bce8f1;         /* Borde azul claro */\n"
"margin-top: 5px;                   /* Separaci\u00f3n superior */")

        self.verticalLayout_2.addWidget(self.SensorCapasitivoLabel)

        self.EstadoDeSensorCapatitivo_ON_OFF = QLabel(self.SensorCapasitivo)
        self.EstadoDeSensorCapatitivo_ON_OFF.setObjectName(u"EstadoDeSensorCapatitivo_ON_OFF")
        self.EstadoDeSensorCapatitivo_ON_OFF.setMinimumSize(QSize(0, 120))
        self.EstadoDeSensorCapatitivo_ON_OFF.setMaximumSize(QSize(16777215, 120))
        self.EstadoDeSensorCapatitivo_ON_OFF.setStyleSheet(u"font-size: 14px;                    /* Tama\u00f1o menor para informaci\u00f3n secundaria */\n"
"font-weight: bold;                 /* Texto en negrita */\n"
"color: #4f4f4f;                    /* Gris oscuro para buen contraste */\n"
"padding: 8px;                      /* Espacio interno menor */\n"
"background-color: #f9f9f9;         /* Fondo blanco suave */\n"
"border-radius: 4px;                /* Esquinas redondeadas menores */\n"
"border: 1px solid #e0e0e0;         /* Borde gris claro */\n"
"margin-top: 5px;                   /* Separaci\u00f3n superior */")

        self.verticalLayout_2.addWidget(self.EstadoDeSensorCapatitivo_ON_OFF)

        self.datosSobreSensor = QLabel(self.SensorCapasitivo)
        self.datosSobreSensor.setObjectName(u"datosSobreSensor")
        self.datosSobreSensor.setMaximumSize(QSize(99999, 99993))
        self.datosSobreSensor.setStyleSheet(u"font-size: 14px;                    /* Tama\u00f1o menor para informaci\u00f3n secundaria */\n"
"color: #4f4f4f;                    /* Gris oscuro para buen contraste */\n"
"padding: 8px;                      /* Espacio interno menor */\n"
"background-color: #f9f9f9;         /* Fondo blanco suave */\n"
"border-radius: 4px;                /* Esquinas redondeadas menores */\n"
"border: 1px solid #e0e0e0;         /* Borde gris claro */\n"
"margin-top: 5px;                   /* Separaci\u00f3n superior */")

        self.verticalLayout_2.addWidget(self.datosSobreSensor)


        self.gridLayout_5.addWidget(self.SensorCapasitivo, 0, 0, 1, 1)


        self.gridLayout_6.addWidget(self.info, 2, 1, 3, 2)

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

        self.diagrama = QGroupBox(self.frame)
        self.diagrama.setObjectName(u"diagrama")
        self.diagrama.setMinimumSize(QSize(280, 0))
        self.diagrama.setMaximumSize(QSize(400, 99999))
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


        self.gridLayout_6.addWidget(self.diagrama, 3, 0, 2, 1)


        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)


        self.retranslateUi(capasitive)

        QMetaObject.connectSlotsByName(capasitive)
    # setupUi

    def retranslateUi(self, capasitive):
        capasitive.setWindowTitle(QCoreApplication.translate("capasitive", u"Form", None))
        self.descripcion.setText(QCoreApplication.translate("capasitive", u"<html><head/><body><p align=\"center\"><span style=\" font-size:10pt; font-style:italic;\">Monitorea en tiempo real la se\u00f1al digital del sensor capacitivo y ofrece informaci\u00f3n did\u00e1ctica para su caracterizaci\u00f3n.</span></p></body></html>", None))
        self.titulo.setText(QCoreApplication.translate("capasitive", u"<html><head/><body><p align=\"center\"><span style=\" font-size:22pt; font-weight:700; color:#007bff;\">Monitoreo de Proximidad Capacitivo</span></p></body></html>", None))
        self.info.setTitle(QCoreApplication.translate("capasitive", u"Info", None))
        self.SensorCapasitivoLabel.setText(QCoreApplication.translate("capasitive", u"<html><head/><body><p align=\"center\"><span style=\" font-size:11pt;\">CapSensor</span></p></body></html>", None))
        self.EstadoDeSensorCapatitivo_ON_OFF.setText(QCoreApplication.translate("capasitive", u"<html><head/><body><p align=\"center\"><span style=\" font-size:11pt;\">On/Off</span></p></body></html>", None))
        self.datosSobreSensor.setText(QCoreApplication.translate("capasitive", u"<html><head/><body><p align=\"justify\"><span style=\" font-size:9pt; font-style:italic;\">Un </span><span style=\" font-size:9pt; font-weight:700; font-style:italic;\">sensor capacitivo tubular</span><span style=\" font-size:9pt; font-style:italic;\"> de la marca </span><span style=\" font-size:9pt; font-weight:700; font-style:italic;\">Tecnotron</span><span style=\" font-size:9pt; font-style:italic;\">,<br/>dise\u00f1ado para aplicaciones industriales donde se requiere<br/>detectar materiales sin contacto f\u00edsico directo.</span></p><p><span style=\" font-size:9pt; font-style:italic;\">\ud83d\udd27 </span><span style=\" font-size:9pt; font-weight:700; font-style:italic;\">Caracter\u00edsticas t\u00e9cnicas destacadas</span><span style=\" font-size:9pt; font-style:italic;\">:</span></p><p><span style=\" font-size:9pt; font-weight:700; font-style:italic;\">Tipo</span><span style=\" font-size:9pt; font-style:italic;\">: Sensor capacitivo tubular</span></p><p><span style=\" font-size:9pt; font-weight:700; fon"
                        "t-style:italic;\">Distancia sensora</span><span style=\" font-size:9pt; font-style:italic;\">: 15 mm</span></p><p><span style=\" font-size:9pt; font-weight:700; font-style:italic;\">Capacidad de carga</span><span style=\" font-size:9pt; font-style:italic;\">: 10 a 500 mA</span></p><p><span style=\" font-size:9pt; font-weight:700; font-style:italic;\">Frecuencia de conmutaci\u00f3n</span><span style=\" font-size:9pt; font-style:italic;\">: 5 Hz</span></p><p><span style=\" font-size:9pt; font-weight:700; font-style:italic;\">Salida</span><span style=\" font-size:9pt; font-style:italic;\">: VCA, l\u00f3gica normalmente cerrada (NF)</span></p><p><span style=\" font-size:9pt; font-weight:700; font-style:italic;\">Protecci\u00f3n</span><span style=\" font-size:9pt; font-style:italic;\">: IP65 (resistente al polvo y chorros de agua)</span></p><p><span style=\" font-size:9pt; font-style:italic;\">Este tipo de sensor es ideal para detectar materiales como<br/>papel, pl\u00e1stico, vidrio, l\u00edquidos o incluso polvo,"
                        " gracias a su<br/>principio de funcionamiento capacitivo. Es muy \u00fatil en<br/>sistemas de automatizaci\u00f3n, control de nivel en tanques, o<br/>detecci\u00f3n en l\u00edneas de producci\u00f3n.</span></p></body></html>", None))
        self.controles.setTitle(QCoreApplication.translate("capasitive", u"Controles", None))
        self.iniciarBt.setText(QCoreApplication.translate("capasitive", u"Iniciar Monitoreo", None))
        self.diagrama.setTitle(QCoreApplication.translate("capasitive", u"Diagrama de Conexiones", None))
        self.dibujo.setText(QCoreApplication.translate("capasitive", u"<html><head/><body><pre style=\" margin-top:12px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:140%;\"><span style=\" font-family:'Courier New','monospace'; font-size:12px; color:#495057;\">\u250c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2510</span></pre><pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:140%;\"><span style=\" font-family:'Courier New','monospace'; font-size:12px; color:#495057;\">\u2502  ESP32 DevKit V1  -&gt; Sensor     \u2502</span></pre><pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:140%;\"><span style=\" font-family:'Courier New','monospace'; font-size:12px; color:#495057;\">\u2502  3V3  \u25cb \u2190\u2500\u2500"
                        " N/A	      (+)  \u2502</span></pre><pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:140%;\"><span style=\" font-family:'Courier New','monospace'; font-size:12px; color:#495057;\">\u2502  GND  \u25cb \u2190\u2500\u2500 GND Cable Azul (-)  \u2502</span></pre><pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:140%;\"><span style=\" font-family:'Courier New','monospace'; font-size:12px; color:#495057;\">\u2502  D25  \u25cb \u2190\u2500\u2500 OUT Cable Negro (D) \u2502</span></pre><pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:140%;\"><span style=\" font-family:'Courier New','monospace'; font-size:12px; color:#495057;\">|---------------------------------|</span></pre><pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0"
                        "; text-indent:0px; line-height:140%;\"><span style=\" font-family:'Courier New','monospace'; font-size:12px; color:#495057;\">\u2502  Fuente de Voltaje -&gt; Sensor    \u2502</span></pre><pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:140%;\"><span style=\" font-family:'Courier New','monospace'; font-size:12px; color:#495057;\">\u2502  5V   </span><span style=\" font-family:'Courier New','monospace'; font-size:12px; color:#495057;\">\u25cb \u2190\u2500\u2500 5V Cable Marr\u00f3n    </span><span style=\" font-family:'Courier New','monospace'; font-size:12px; color:#495057;\"> \u2502</span></pre><pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:140%;\"><span style=\" font-family:'Courier New','monospace'; font-size:12px; color:#495057;\">\u2514\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500"
                        "\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2518</span></pre></body></html>", None))
        self.nota.setText(QCoreApplication.translate("capasitive", u"<html><head/><body><p align=\"justify\"><span style=\" font-size:9pt;\">\ud83d\udca1 </span><span style=\" font-size:9pt; font-weight:700;\">Nota:</span><span style=\" font-size:9pt;\"> Aseg\u00farate de conectar los <br/>componentes correctamente antes de <br/>iniciar el monitoreo</span></p><p align=\"justify\"><span style=\" font-size:9pt;\">\ud83d\udd0c</span><span style=\" font-size:9pt; font-weight:700;\">Voltaje: </span><span style=\" font-size:9pt;\">La entrada de alimentaci\u00f3n<br/>del sensor tiene un rango de acci\u00f3n de <br/>5v a 12v, sientete libre de experimentar<br/>con los voltajes dentro de este limite.</span></p><p align=\"justify\"><span style=\" font-size:9pt;\">\ud83d\udd39</span><span style=\" font-size:9pt; font-weight:700;\">GND: </span><span style=\" font-size:9pt;\">Asegurate de compartir la <br/>tierra entre en microcontrolador, la<br/>fuente y el sensor.</span></p></body></html>", None))
    # retranslateUi

