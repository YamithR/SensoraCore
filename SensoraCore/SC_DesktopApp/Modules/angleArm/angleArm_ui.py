# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'angleArm.ui'
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

class Ui_angleArm(object):
    def setupUi(self, angleArm):
        if not angleArm.objectName():
            angleArm.setObjectName(u"angleArm")
        angleArm.resize(723, 683)
        angleArm.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"border: 1px solid rgb(221, 221, 221);\n"
"border-radius: 5px;\n"
"color: rgb(0, 0, 0);")
        self.verticalLayout = QVBoxLayout(angleArm)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.frame = QFrame(angleArm)
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
        self.gridLayout_4 = QGridLayout(self.controles)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.datos = QWidget(self.controles)
        self.datos.setObjectName(u"datos")
        self.datos.setMinimumSize(QSize(0, 0))
        self.datos.setMaximumSize(QSize(9999, 16777215))
        self.gridLayout = QGridLayout(self.datos)
        self.gridLayout.setObjectName(u"gridLayout")
        self.datosLabel = QLabel(self.datos)
        self.datosLabel.setObjectName(u"datosLabel")

        self.gridLayout.addWidget(self.datosLabel, 0, 0, 1, 1)

        self.POT1Label = QLabel(self.datos)
        self.POT1Label.setObjectName(u"POT1Label")

        self.gridLayout.addWidget(self.POT1Label, 0, 1, 1, 1)

        self.POT2Label = QLabel(self.datos)
        self.POT2Label.setObjectName(u"POT2Label")

        self.gridLayout.addWidget(self.POT2Label, 0, 2, 1, 1)

        self.POT3Label = QLabel(self.datos)
        self.POT3Label.setObjectName(u"POT3Label")

        self.gridLayout.addWidget(self.POT3Label, 0, 3, 1, 1)

        self.analogoLabel = QLabel(self.datos)
        self.analogoLabel.setObjectName(u"analogoLabel")

        self.gridLayout.addWidget(self.analogoLabel, 1, 0, 1, 1)

        self.analogoDtPOT1 = QLabel(self.datos)
        self.analogoDtPOT1.setObjectName(u"analogoDtPOT1")

        self.gridLayout.addWidget(self.analogoDtPOT1, 1, 1, 1, 1)

        self.analogoDtPOT2 = QLabel(self.datos)
        self.analogoDtPOT2.setObjectName(u"analogoDtPOT2")

        self.gridLayout.addWidget(self.analogoDtPOT2, 1, 2, 1, 1)

        self.analogoDtPOT3 = QLabel(self.datos)
        self.analogoDtPOT3.setObjectName(u"analogoDtPOT3")

        self.gridLayout.addWidget(self.analogoDtPOT3, 1, 3, 1, 1)

        self.anguloLabel = QLabel(self.datos)
        self.anguloLabel.setObjectName(u"anguloLabel")

        self.gridLayout.addWidget(self.anguloLabel, 2, 0, 1, 1)

        self.anguloDtPOT1 = QLabel(self.datos)
        self.anguloDtPOT1.setObjectName(u"anguloDtPOT1")

        self.gridLayout.addWidget(self.anguloDtPOT1, 2, 1, 1, 1)

        self.anguloDtPOT2 = QLabel(self.datos)
        self.anguloDtPOT2.setObjectName(u"anguloDtPOT2")

        self.gridLayout.addWidget(self.anguloDtPOT2, 2, 2, 1, 1)

        self.anguloDtPOT3 = QLabel(self.datos)
        self.anguloDtPOT3.setObjectName(u"anguloDtPOT3")

        self.gridLayout.addWidget(self.anguloDtPOT3, 2, 3, 1, 1)

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

        self.analogoDtCalibradoPOT1 = QLabel(self.calBox)
        self.analogoDtCalibradoPOT1.setObjectName(u"analogoDtCalibradoPOT1")
        self.analogoDtCalibradoPOT1.setStyleSheet(u"background-color: rgb(255, 255, 255);")

        self.horizontalLayout_2.addWidget(self.analogoDtCalibradoPOT1)

        self.analogoDtCalibradoPOT2 = QLabel(self.calBox)
        self.analogoDtCalibradoPOT2.setObjectName(u"analogoDtCalibradoPOT2")
        self.analogoDtCalibradoPOT2.setStyleSheet(u"background-color: rgb(255, 255, 255);")

        self.horizontalLayout_2.addWidget(self.analogoDtCalibradoPOT2)

        self.analogoDtCalibradoPOT3 = QLabel(self.calBox)
        self.analogoDtCalibradoPOT3.setObjectName(u"analogoDtCalibradoPOT3")
        self.analogoDtCalibradoPOT3.setStyleSheet(u"background-color: rgb(255, 255, 255);")

        self.horizontalLayout_2.addWidget(self.analogoDtCalibradoPOT3)


        self.gridLayout.addWidget(self.calBox, 3, 0, 1, 4)


        self.gridLayout_4.addWidget(self.datos, 0, 2, 1, 1)

        self.EstadoDeSensorCapasitivo = QWidget(self.controles)
        self.EstadoDeSensorCapasitivo.setObjectName(u"EstadoDeSensorCapasitivo")
        self.EstadoDeSensorCapasitivo.setMaximumSize(QSize(106, 16777215))
        self.verticalLayout_2 = QVBoxLayout(self.EstadoDeSensorCapasitivo)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.SensorCapasitivoLabel = QLabel(self.EstadoDeSensorCapasitivo)
        self.SensorCapasitivoLabel.setObjectName(u"SensorCapasitivoLabel")
        self.SensorCapasitivoLabel.setStyleSheet(u"font-size: 14px;                    /* Tama\u00f1o menor para informaci\u00f3n secundaria */\n"
"font-weight: bold;                 /* Texto en negrita */\n"
"color: #31708f;                    /* Azul medio para indicar estado */\n"
"padding: 4px;                      /* Espacio interno menor */\n"
"background-color: #d9edf7;         /* Fondo azul claro */\n"
"border-radius: 4px;                /* Esquinas redondeadas menores */\n"
"border: 1px solid #bce8f1;         /* Borde azul claro */\n"
"margin-top: 5px;                   /* Separaci\u00f3n superior */")

        self.verticalLayout_2.addWidget(self.SensorCapasitivoLabel)

        self.EstadoDeSensorCapatitivo_ON_OFF = QLabel(self.EstadoDeSensorCapasitivo)
        self.EstadoDeSensorCapatitivo_ON_OFF.setObjectName(u"EstadoDeSensorCapatitivo_ON_OFF")
        self.EstadoDeSensorCapatitivo_ON_OFF.setStyleSheet(u"font-size: 14px;                    /* Tama\u00f1o menor para informaci\u00f3n secundaria */\n"
"font-weight: bold;                 /* Texto en negrita */\n"
"color: #4f4f4f;                    /* Gris oscuro para buen contraste */\n"
"padding: 8px;                      /* Espacio interno menor */\n"
"background-color: #f9f9f9;         /* Fondo blanco suave */\n"
"border-radius: 4px;                /* Esquinas redondeadas menores */\n"
"border: 1px solid #e0e0e0;         /* Borde gris claro */\n"
"margin-top: 5px;                   /* Separaci\u00f3n superior */")

        self.verticalLayout_2.addWidget(self.EstadoDeSensorCapatitivo_ON_OFF)


        self.gridLayout_4.addWidget(self.EstadoDeSensorCapasitivo, 0, 1, 1, 1)

        self.botones = QWidget(self.controles)
        self.botones.setObjectName(u"botones")
        self.gridLayout_3 = QGridLayout(self.botones)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
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

        self.gridLayout_3.addWidget(self.exportarBt, 2, 1, 1, 1)

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

        self.gridLayout_3.addWidget(self.limpiarBt, 2, 0, 1, 1)

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


        self.gridLayout_4.addWidget(self.botones, 0, 0, 1, 1)


        self.gridLayout_6.addWidget(self.controles, 4, 0, 1, 3)

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
        self.dibujo.setMinimumSize(QSize(0, 285))
        self.dibujo.setStyleSheet(u"")

        self.gridLayout_2.addWidget(self.dibujo, 0, 0, 1, 1)

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

        self.gridLayout_2.addWidget(self.nota, 1, 0, 1, 1)


        self.gridLayout_6.addWidget(self.diagrama, 2, 0, 1, 1)

        self.grafica = QGroupBox(self.frame)
        self.grafica.setObjectName(u"grafica")
        self.grafica.setMinimumSize(QSize(400, 0))
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


        self.verticalLayout.addWidget(self.frame)


        self.retranslateUi(angleArm)

        QMetaObject.connectSlotsByName(angleArm)
    # setupUi

    def retranslateUi(self, angleArm):
        angleArm.setWindowTitle(QCoreApplication.translate("angleArm", u"Form", None))
        self.titulo.setText(QCoreApplication.translate("angleArm", u"<html><head/><body><p align=\"center\"><span style=\" font-size:22pt; font-weight:700; color:#007bff;\">Monitoreo de \u00c1ngulo y Proximidad</span></p></body></html>", None))
        self.controles.setTitle(QCoreApplication.translate("angleArm", u"Controles", None))
        self.datosLabel.setText(QCoreApplication.translate("angleArm", u"Datos", None))
        self.POT1Label.setText(QCoreApplication.translate("angleArm", u"POT-1", None))
        self.POT2Label.setText(QCoreApplication.translate("angleArm", u"POT-2", None))
        self.POT3Label.setText(QCoreApplication.translate("angleArm", u"POT-3", None))
        self.analogoLabel.setText(QCoreApplication.translate("angleArm", u"An\u00e1logo", None))
        self.analogoDtPOT1.setText(QCoreApplication.translate("angleArm", u"--", None))
        self.analogoDtPOT2.setText(QCoreApplication.translate("angleArm", u"--", None))
        self.analogoDtPOT3.setText(QCoreApplication.translate("angleArm", u"--", None))
        self.anguloLabel.setText(QCoreApplication.translate("angleArm", u"\u00c1ngulo", None))
        self.anguloDtPOT1.setText(QCoreApplication.translate("angleArm", u"--", None))
        self.anguloDtPOT2.setText(QCoreApplication.translate("angleArm", u"--", None))
        self.anguloDtPOT3.setText(QCoreApplication.translate("angleArm", u"--", None))
        self.calibradoLabel.setText(QCoreApplication.translate("angleArm", u"Calibrado", None))
        self.analogoDtCalibradoPOT1.setText(QCoreApplication.translate("angleArm", u"--", None))
        self.analogoDtCalibradoPOT2.setText(QCoreApplication.translate("angleArm", u"--", None))
        self.analogoDtCalibradoPOT3.setText(QCoreApplication.translate("angleArm", u"--", None))
        self.SensorCapasitivoLabel.setText(QCoreApplication.translate("angleArm", u"<html><head/><body><p align=\"center\"><span style=\" font-size:11pt;\">CapSensor</span></p></body></html>", None))
        self.EstadoDeSensorCapatitivo_ON_OFF.setText(QCoreApplication.translate("angleArm", u"<html><head/><body><p align=\"center\"><span style=\" font-size:11pt;\">On/Off</span></p></body></html>", None))
        self.calibrarBt.setText(QCoreApplication.translate("angleArm", u"No Calibrado", None))
        self.exportarBt.setText(QCoreApplication.translate("angleArm", u"Exportal a Exel", None))
        self.limpiarBt.setText(QCoreApplication.translate("angleArm", u"Limpiar Gr\u00e1fica", None))
        self.iniciarBt.setText(QCoreApplication.translate("angleArm", u"Iniciar Monitoreo", None))
        self.diagrama.setTitle(QCoreApplication.translate("angleArm", u"Diagrama de Conexiones", None))
        self.dibujo.setText(QCoreApplication.translate("angleArm", u"<html><head/><body><pre style=\" margin-top:12px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:140%;\"><span style=\" font-family:'Courier New','monospace'; font-size:12px; color:#495057;\">\u250c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2510</span></pre><pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:140%;\"><span style=\" font-family:'Courier New','monospace'; font-size:12px; color:#495057;\">\u2502  ESP32 DevKit V1                \u2502</span></pre><pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:140%;\"><span style=\" font-family:'Courier New','monospace'; font-size:12px; color:#495057;\">\u2502  3V3  \u25cb \u2190\u2500\u2500 P"
                        "otenci\u00f3metros (+)  \u2502</span></pre><pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:140%;\"><span style=\" font-family:'Courier New','monospace'; font-size:12px; color:#495057;\">\u2502  GND  \u25cb \u2190\u2500\u2500 Potenci\u00f3metros (-)  \u2502</span></pre><pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:140%;\"><span style=\" font-family:'Courier New','monospace'; font-size:12px; color:#495057;\">\u2502  D32  \u25cb \u2190\u2500\u2500 Potenci\u00f3metro 1 (S) \u2502</span></pre><pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:140%;\"><span style=\" font-family:'Courier New','monospace'; font-size:12px; color:#495057;\">\u2502  D33  \u25cb \u2190\u2500\u2500 Potenci\u00f3metro 2 (S) \u2502</span></pre><pre style=\" margin-top:0px; margin-bottom:0px; "
                        "margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:140%;\"><span style=\" font-family:'Courier New','monospace'; font-size:12px; color:#495057;\">\u2502  D34  \u25cb \u2190\u2500\u2500 Potenci\u00f3metro 3 (S) \u2502</span></pre><pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:140%;\"><span style=\" font-family:'Courier New','monospace'; font-size:12px; color:#495057;\">\u2502  D25  \u25cb \u2190\u2500\u2500 Sensor Capacitivo   \u2502</span></pre><pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:140%;\"><span style=\" font-family:'Courier New','monospace'; font-size:12px; color:#495057;\">\u2502  LED integrado: GPIO 2          \u2502</span></pre><pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:140%;\"><span style=\" font-family:'Co"
                        "urier New','monospace'; font-size:12px; color:#495057;\">\u2514\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2518</span></pre><pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:140%;\"><span style=\" font-family:'Courier New','monospace'; font-size:12px; font-weight:700; color:#495057;\">3 Potenci\u00f3metros 10k\u03a9:</span></pre><pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:140%;\"><span style=\" font-family:'Courier New','monospace'; font-size:12px; color:#495057;\">\u2022 Pin (+): Alimentaci\u00f3n 3.3V (todos)</span></pre><pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:140%;\"><span style=\" font-family:"
                        "'Courier New','monospace'; font-size:12px; color:#495057;\">\u2022 Pin (S): Se\u00f1ales anal\u00f3gicas:</span></pre><pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:140%;\"><span style=\" font-family:'Courier New','monospace'; font-size:12px; color:#495057;\">\u2022 Pin (-): Tierra (GND) (todos)</span></pre></body></html>", None))
        self.nota.setText(QCoreApplication.translate("angleArm", u"<html><head/><body><p align=\"justify\"><span style=\" font-size:9pt;\">\ud83d\udca1 </span><span style=\" font-size:9pt; font-weight:700;\">Nota:</span><span style=\" font-size:9pt;\"> Aseg\u00farate de conectar los <br/>componentes correctamente antes de <br/>iniciar el monitoreo</span></p></body></html>", None))
        self.grafica.setTitle(QCoreApplication.translate("angleArm", u"Gr\u00e1fica", None))
        self.descripcion.setText(QCoreApplication.translate("angleArm", u"<html><head/><body><p align=\"center\"><span style=\" font-size:10pt; font-style:italic;\">Monitorea en tiempo real 3 potenci\u00f3metros y un sensor capacitivo conectados a pines GPIO para traducirlo a \u00c1ngulo,<br/> incluyendo detecci\u00f3n de presencia y calibraci\u00f3n por Regresi\u00f3n Lineal Asistida.</span></p></body></html>", None))
    # retranslateUi

