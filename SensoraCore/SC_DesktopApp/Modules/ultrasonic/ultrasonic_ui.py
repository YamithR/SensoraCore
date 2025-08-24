# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ultrasonic.ui'
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

class Ui_ultrasonic(object):
    def setupUi(self, ultrasonic):
        if not ultrasonic.objectName():
            ultrasonic.setObjectName(u"ultrasonic")
        ultrasonic.resize(749, 650)
        ultrasonic.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"border: 1px solid rgb(221, 221, 221);\n"
"border-radius: 5px;\n"
"color: rgb(0, 0, 0);")
        self.gridLayout = QGridLayout(ultrasonic)
        self.gridLayout.setObjectName(u"gridLayout")
        self.frame = QFrame(ultrasonic)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_6 = QGridLayout(self.frame)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.titulo = QLabel(self.frame)
        self.titulo.setObjectName(u"titulo")
        self.titulo.setMaximumSize(QSize(16777215, 45))
        self.titulo.setStyleSheet(u"        background-color: #f8f9fa;       \n"
"        border: 2px solid #dee2e6;         \n"
"        border-radius: 6px;              \n"
"   ")

        self.gridLayout_6.addWidget(self.titulo, 0, 0, 1, 3)

        self.controles = QGroupBox(self.frame)
        self.controles.setObjectName(u"controles")
        self.controles.setMinimumSize(QSize(0, 150))
        self.controles.setMaximumSize(QSize(16777215, 150))
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
        self.gridLayout_3 = QGridLayout(self.botones)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
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

        self.gridLayout_3.addWidget(self.iniciarBt, 0, 0, 1, 1)

        self.calibrarBt = QPushButton(self.botones)
        self.calibrarBt.setObjectName(u"calibrarBt")
        self.calibrarBt.setStyleSheet(u"        font-size: 14px;                    /* Tama\u00f1o menor para informaci\u00f3n secundaria */\n"
"        font-weight: bold;                  /* Texto en negrita */\n"
"        color: #856404;                     /* Color \u00e1mbar para indicar estado */\n"
"        padding: 8px;                       /* Espacio interno menor */\n"
"        background-color: #fff3cd;          /* Fondo \u00e1mbar claro */\n"
"        border-radius: 4px;                 /* Esquinas redondeadas menores */\n"
"        border: 1px solid #ffeaa7;          /* Borde \u00e1mbar */\n"
"        margin-top: 5px;                    /* Separaci\u00f3n superior */")

        self.gridLayout_3.addWidget(self.calibrarBt, 0, 1, 1, 1)

        self.limpiarBt = QPushButton(self.botones)
        self.limpiarBt.setObjectName(u"limpiarBt")
        self.limpiarBt.setStyleSheet(u"/* Estilo base con matices rosa y gris degradado */\n"
"QPushButton {\n"
"    font-size: 14px;                         /* Tama\u00f1o menor para informaci\u00f3n secundaria */\n"
"    font-weight: bold;                       /* Texto en negrita */\n"
"    color: #5a5a5a;                          /* Gris medio para texto */\n"
"    padding: 8px;                            /* Espacio interno menor */\n"
"    background: linear-gradient(135deg, #f8e1ec, #d3d3d3); /* Degradado rosa a gris */\n"
"    border-radius: 6px;                      /* Esquinas ligeramente m\u00e1s redondeadas */\n"
"    border: 1px solid #e0b7c6;               /* Borde rosa suave */\n"
"    margin-top: 5px;                         /* Separaci\u00f3n superior */\n"
"}\n"
"\n"
"/* Efecto hover con \u00e9nfasis en el rosa */\n"
"QPushButton:hover {\n"
"    background: linear-gradient(135deg, #fce4ec, #c0c0c0); /* Rosa claro a gris claro */\n"
"    color: #7a4b63;                          /* Rosa oscuro para el texto */\n"
"    border: 1px sol"
                        "id #d48ca3;               /* Borde m\u00e1s intenso en rosa */\n"
"}\n"
"/* Presionado: tono m\u00e1s oscuro y efecto hundido */\n"
"QPushButton:pressed {\n"
"    background-color: #e0b7c6;\n"
"    border: 2px solid #b0b0b0;\n"
"    padding-top: 8px; /* efecto hundido */\n"
"    padding-left: 8px;\n"
"}\n"
"")

        self.gridLayout_3.addWidget(self.limpiarBt, 1, 0, 1, 1)

        self.exportarBt = QPushButton(self.botones)
        self.exportarBt.setObjectName(u"exportarBt")
        self.exportarBt.setStyleSheet(u"        font-size: 14px;                    /* Tama\u00f1o menor para informaci\u00f3n secundaria */\n"
"        font-weight: bold;                  /* Texto en negrita */\n"
"        color: #856404;                     /* Color \u00e1mbar para indicar estado */\n"
"        padding: 8px;                       /* Espacio interno menor */\n"
"        background-color: #fff3cd;          /* Fondo \u00e1mbar claro */\n"
"        border-radius: 4px;                 /* Esquinas redondeadas menores */\n"
"        border: 1px solid #ffeaa7;          /* Borde \u00e1mbar */\n"
"        margin-top: 5px;                    /* Separaci\u00f3n superior */")

        self.gridLayout_3.addWidget(self.exportarBt, 1, 1, 1, 1)


        self.horizontalLayout.addWidget(self.botones)

        self.datos = QWidget(self.controles)
        self.datos.setObjectName(u"datos")
        self.datos.setMaximumSize(QSize(900, 16777215))
        self.gridLayout_4 = QGridLayout(self.datos)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.datosLabel = QLabel(self.datos)
        self.datosLabel.setObjectName(u"datosLabel")

        self.gridLayout_4.addWidget(self.datosLabel, 0, 0, 1, 1)

        self.TiempoDeRespuestaLabel = QLabel(self.datos)
        self.TiempoDeRespuestaLabel.setObjectName(u"TiempoDeRespuestaLabel")

        self.gridLayout_4.addWidget(self.TiempoDeRespuestaLabel, 0, 1, 1, 1)

        self.DiscanciaLabel = QLabel(self.datos)
        self.DiscanciaLabel.setObjectName(u"DiscanciaLabel")

        self.gridLayout_4.addWidget(self.DiscanciaLabel, 0, 2, 1, 1)

        self.lecturaLabel = QLabel(self.datos)
        self.lecturaLabel.setObjectName(u"lecturaLabel")

        self.gridLayout_4.addWidget(self.lecturaLabel, 1, 0, 1, 1)

        self.TiempoDeRespuestaDt = QLabel(self.datos)
        self.TiempoDeRespuestaDt.setObjectName(u"TiempoDeRespuestaDt")

        self.gridLayout_4.addWidget(self.TiempoDeRespuestaDt, 1, 1, 1, 1)

        self.DistanciaDt = QLabel(self.datos)
        self.DistanciaDt.setObjectName(u"DistanciaDt")

        self.gridLayout_4.addWidget(self.DistanciaDt, 1, 2, 1, 1)

        self.calBox = QWidget(self.datos)
        self.calBox.setObjectName(u"calBox")
        self.calBox.setStyleSheet(u"background-color: rgb(14, 255, 34);")
        self.horizontalLayout_2 = QHBoxLayout(self.calBox)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(3, 3, 3, 3)
        self.calibradoLabel = QLabel(self.calBox)
        self.calibradoLabel.setObjectName(u"calibradoLabel")
        self.calibradoLabel.setStyleSheet(u"background-color: rgb(255, 255, 255);")

        self.horizontalLayout_2.addWidget(self.calibradoLabel)

        self.DistanciaDtCalibrada = QLabel(self.calBox)
        self.DistanciaDtCalibrada.setObjectName(u"DistanciaDtCalibrada")
        self.DistanciaDtCalibrada.setStyleSheet(u"background-color: rgb(255, 255, 255);")

        self.horizontalLayout_2.addWidget(self.DistanciaDtCalibrada)


        self.gridLayout_4.addWidget(self.calBox, 2, 0, 1, 3)


        self.horizontalLayout.addWidget(self.datos)


        self.gridLayout_6.addWidget(self.controles, 4, 0, 1, 3)

        self.diagrama = QGroupBox(self.frame)
        self.diagrama.setObjectName(u"diagrama")
        self.diagrama.setMinimumSize(QSize(0, 380))
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
        self.verticalLayout = QVBoxLayout(self.diagrama)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.dibujo = QLabel(self.diagrama)
        self.dibujo.setObjectName(u"dibujo")
        self.dibujo.setMinimumSize(QSize(0, 270))
        self.dibujo.setMaximumSize(QSize(16777215, 300))
        self.dibujo.setStyleSheet(u"")

        self.verticalLayout.addWidget(self.dibujo)

        self.nota = QLabel(self.diagrama)
        self.nota.setObjectName(u"nota")
        self.nota.setMaximumSize(QSize(999, 70))
        self.nota.setStyleSheet(u"        font-size: 13px;                    /* Tama\u00f1o menor para nota */\n"
"        color: #856404;                     /* Color \u00e1mbar oscuro */\n"
"        background-color: #fff3cd;          /* Fondo \u00e1mbar claro (alerta) */\n"
"        border: 1px solid #ffeaa7;          /* Borde \u00e1mbar */\n"
"        border-radius: 4px;                 /* Esquinas redondeadas */\n"
"        padding: 8px;                       /* Espacio interno */\n"
"        margin-top: 5px;                    /* Separaci\u00f3n superior */\n"
"")

        self.verticalLayout.addWidget(self.nota)


        self.gridLayout_6.addWidget(self.diagrama, 2, 0, 1, 1)

        self.grafica = QGroupBox(self.frame)
        self.grafica.setObjectName(u"grafica")
        self.grafica.setMinimumSize(QSize(400, 380))
        self.grafica.setStyleSheet(u"QGroupBox {\n"
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
        self.gridLayout_5 = QGridLayout(self.grafica)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.grapWid = QWidget(self.grafica)
        self.grapWid.setObjectName(u"grapWid")

        self.gridLayout_5.addWidget(self.grapWid, 0, 0, 1, 1)


        self.gridLayout_6.addWidget(self.grafica, 2, 1, 1, 2)

        self.descripcion = QLabel(self.frame)
        self.descripcion.setObjectName(u"descripcion")
        self.descripcion.setMaximumSize(QSize(16777215, 60))
        self.descripcion.setStyleSheet(u"        background-color: #f8f9fa;       \n"
"        border: 2px solid #dee2e6;         \n"
"        border-radius: 6px;              \n"
"   ")

        self.gridLayout_6.addWidget(self.descripcion, 1, 0, 1, 3)


        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)


        self.retranslateUi(ultrasonic)

        QMetaObject.connectSlotsByName(ultrasonic)
    # setupUi

    def retranslateUi(self, ultrasonic):
        ultrasonic.setWindowTitle(QCoreApplication.translate("ultrasonic", u"Form", None))
        self.titulo.setText(QCoreApplication.translate("ultrasonic", u"<html><head/><body><p align=\"center\"><span style=\" font-size:22pt; font-weight:700; color:#007bff;\">Monitoreo de Distancia por Ultrasonido</span></p></body></html>", None))
        self.controles.setTitle(QCoreApplication.translate("ultrasonic", u"Controles", None))
        self.iniciarBt.setText(QCoreApplication.translate("ultrasonic", u"Iniciar Monitoreo", None))
        self.calibrarBt.setText(QCoreApplication.translate("ultrasonic", u"No Calibrado", None))
        self.limpiarBt.setText(QCoreApplication.translate("ultrasonic", u"Limpiar Gr\u00e1fica", None))
        self.exportarBt.setText(QCoreApplication.translate("ultrasonic", u"Exportal a Exel", None))
        self.datosLabel.setText(QCoreApplication.translate("ultrasonic", u"Datos", None))
        self.TiempoDeRespuestaLabel.setText(QCoreApplication.translate("ultrasonic", u"Tiempo Respuesta", None))
        self.DiscanciaLabel.setText(QCoreApplication.translate("ultrasonic", u"Distancia", None))
        self.lecturaLabel.setText(QCoreApplication.translate("ultrasonic", u"Lectura", None))
        self.TiempoDeRespuestaDt.setText(QCoreApplication.translate("ultrasonic", u"--", None))
        self.DistanciaDt.setText(QCoreApplication.translate("ultrasonic", u"--", None))
        self.calibradoLabel.setText(QCoreApplication.translate("ultrasonic", u"Calibrado", None))
        self.DistanciaDtCalibrada.setText(QCoreApplication.translate("ultrasonic", u"--", None))
        self.diagrama.setTitle(QCoreApplication.translate("ultrasonic", u"Diagrama de Conexiones", None))
        self.dibujo.setText(QCoreApplication.translate("ultrasonic", u"<html><head/><body><pre style=\" margin-top:12px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:140%;\"><span style=\" font-family:'Courier New','monospace'; font-size:12px; color:#495057;\">\u250c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2510<br/>\u2502 ESP32 DevKit V1 \u2192 Sensor        \u2502<br/>\u2502                                 \u2502<br/>\u2502 5V \u25cb \u2500\u2500\u2192 VCC (HC-SR04)          \u2502<br/>\u2502 GND \u25cb \u2500\u2500\u2192 GND (HC-SR04)         \u2502<br/>\u2502 D32 \u25cb \u2500\u2500\u2192 TRIG (HC-SR04)        \u2502<br/>\u2502 D33 \u25cb \u2500\u2500\u2192 ECHO (HC-SR04)        \u2502<br/>\u2502                                 \u2502<br/>\u2502 LED integrado: GPIO 2           \u2502<br/>\u2514\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500"
                        "\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2518</span></pre></body></html>", None))
        self.nota.setText(QCoreApplication.translate("ultrasonic", u"<html><head/><body><p align=\"justify\"><span style=\" font-size:9pt;\">\ud83d\udca1 </span><span style=\" font-size:9pt; font-weight:700;\">Nota:</span><span style=\" font-size:9pt;\"> Aseg\u00farate de conectar el <br/>potenci\u00f3metro correctamente antes <br/>de iniciar el monitoreo</span></p></body></html>", None))
        self.grafica.setTitle(QCoreApplication.translate("ultrasonic", u"Gr\u00e1fica", None))
        self.descripcion.setText(QCoreApplication.translate("ultrasonic", u"<html><head/><body><p align=\"center\"><span style=\" font-size:10pt; font-style:italic;\">Monitorea la lectura anal\u00f3gica del sensor ultras\u00f3nico para traducirla a distancia con calibraci\u00f3n por Regresi\u00f3n Lineal Asistida.</span></p></body></html>", None))
    # retranslateUi

