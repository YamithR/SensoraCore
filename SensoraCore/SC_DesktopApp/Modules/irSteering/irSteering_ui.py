# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'irSteering.ui'
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

class Ui_irSteering(object):
    def setupUi(self, irSteering):
        if not irSteering.objectName():
            irSteering.setObjectName(u"irSteering")
        irSteering.resize(730, 634)
        irSteering.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"border: 1px solid rgb(221, 221, 221);\n"
"border-radius: 5px;\n"
"color: rgb(0, 0, 0);")
        self.gridLayout = QGridLayout(irSteering)
        self.gridLayout.setObjectName(u"gridLayout")
        self.frame = QFrame(irSteering)
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

        self.diagrama = QGroupBox(self.frame)
        self.diagrama.setObjectName(u"diagrama")
        self.diagrama.setMinimumSize(QSize(0, 397))
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
        self.dibujo.setMinimumSize(QSize(0, 292))
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


        self.gridLayout_6.addWidget(self.diagrama, 3, 0, 1, 1)

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


        self.horizontalLayout.addWidget(self.botones)


        self.gridLayout_6.addWidget(self.controles, 2, 0, 1, 1)

        self.MandosEinfogroup = QGroupBox(self.frame)
        self.MandosEinfogroup.setObjectName(u"MandosEinfogroup")
        self.MandosEinfogroup.setMinimumSize(QSize(400, 380))
        self.MandosEinfogroup.setStyleSheet(u"QGroupBox {\n"
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
        self.gridLayout_5 = QGridLayout(self.MandosEinfogroup)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.mandosEInfo = QWidget(self.MandosEinfogroup)
        self.mandosEInfo.setObjectName(u"mandosEInfo")
        self.verticalLayout_2 = QVBoxLayout(self.mandosEInfo)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.infodeRPMs = QWidget(self.mandosEInfo)
        self.infodeRPMs.setObjectName(u"infodeRPMs")
        self.gridLayout_2 = QGridLayout(self.infodeRPMs)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.SensorIzquierdaLabel = QLabel(self.infodeRPMs)
        self.SensorIzquierdaLabel.setObjectName(u"SensorIzquierdaLabel")
        self.SensorIzquierdaLabel.setStyleSheet(u"font-weight: bold;                 /* Texto en negrita */\n"
"color: #a94442;                    /* Rojo oscuro para texto de alerta */\n"
"padding: 8px;                      /* Espacio interno menor */\n"
"background-color: #f2dede;         /* Fondo rojo claro */\n"
"border-radius: 4px;                /* Esquinas redondeadas menores */\n"
"border: 1px solid #ebccd1;         /* Borde rojo suave */\n"
"margin-top: 5px;                   /* Separaci\u00f3n superior */")

        self.gridLayout_2.addWidget(self.SensorIzquierdaLabel, 0, 0, 1, 1)

        self.SensorDerechaLabel = QLabel(self.infodeRPMs)
        self.SensorDerechaLabel.setObjectName(u"SensorDerechaLabel")
        self.SensorDerechaLabel.setStyleSheet(u"font-weight: bold;                 /* Texto en negrita */\n"
"color: #31708f;                    /* Azul profundo para texto */\n"
"padding: 8px;                      /* Espacio interno menor */\n"
"background-color: #d9edf7;         /* Fondo azul claro */\n"
"border-radius: 4px;                /* Esquinas redondeadas menores */\n"
"border: 1px solid #bce8f1;         /* Borde azul suave */\n"
"margin-top: 5px;                   /* Separaci\u00f3n superior */")

        self.gridLayout_2.addWidget(self.SensorDerechaLabel, 0, 1, 1, 1)

        self.RPMizquierdaDt = QLabel(self.infodeRPMs)
        self.RPMizquierdaDt.setObjectName(u"RPMizquierdaDt")
        self.RPMizquierdaDt.setStyleSheet(u"font-weight: bold;                 /* Texto en negrita */\n"
"color: #555555;                    /* Gris oscuro para texto legible */\n"
"padding: 8px;                      /* Espacio interno menor */\n"
"background-color: #f5f5f5;         /* Fondo gris claro */\n"
"border-radius: 4px;                /* Esquinas redondeadas menores */\n"
"border: 1px solid #d6d6d6;         /* Borde gris suave */\n"
"margin-top: 5px;                   /* Separaci\u00f3n superior */")

        self.gridLayout_2.addWidget(self.RPMizquierdaDt, 2, 0, 1, 1)

        self.RPMderechaDt = QLabel(self.infodeRPMs)
        self.RPMderechaDt.setObjectName(u"RPMderechaDt")
        self.RPMderechaDt.setStyleSheet(u"font-weight: bold;                 /* Texto en negrita */\n"
"color: #555555;                    /* Gris oscuro para texto legible */\n"
"padding: 8px;                      /* Espacio interno menor */\n"
"background-color: #f5f5f5;         /* Fondo gris claro */\n"
"border-radius: 4px;                /* Esquinas redondeadas menores */\n"
"border: 1px solid #d6d6d6;         /* Borde gris suave */\n"
"margin-top: 5px;                   /* Separaci\u00f3n superior */")

        self.gridLayout_2.addWidget(self.RPMderechaDt, 2, 1, 1, 1)

        self.RPMsLabel = QLabel(self.infodeRPMs)
        self.RPMsLabel.setObjectName(u"RPMsLabel")
        self.RPMsLabel.setStyleSheet(u"font-weight: bold;                 /* Texto en negrita */\n"
"color: #8a6d3b;                    /* Naranja oscuro para texto */\n"
"padding: 8px;                      /* Espacio interno menor */\n"
"background-color: #fcf8e3;         /* Fondo naranja claro, casi crema */\n"
"border-radius: 4px;                /* Esquinas redondeadas menores */\n"
"border: 1px solid #faebcc;         /* Borde naranja suave */\n"
"margin-top: 5px;                   /* Separaci\u00f3n superior */")

        self.gridLayout_2.addWidget(self.RPMsLabel, 1, 0, 1, 2)


        self.verticalLayout_2.addWidget(self.infodeRPMs)

        self.SensoresIR = QWidget(self.mandosEInfo)
        self.SensoresIR.setObjectName(u"SensoresIR")
        self.gridLayout_4 = QGridLayout(self.SensoresIR)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.SensorIR1 = QLabel(self.SensoresIR)
        self.SensorIR1.setObjectName(u"SensorIR1")
        self.SensorIR1.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.SensorIR1.setStyleSheet(u"font-size: 14px;                    /* Tama\u00f1o menor para informaci\u00f3n secundaria */\n"
"font-weight: bold;                 /* Texto en negrita */\n"
"color: #333333;                    /* Gris oscuro para buen contraste sobre blanco */\n"
"padding: 8px;                      /* Espacio interno menor */\n"
"background-color: #ffffff;         /* Fondo blanco puro */\n"
"border-radius: 4px;                /* Esquinas redondeadas menores */\n"
"border: 1px solid #e0e0e0;         /* Borde gris muy claro */\n"
"margin-top: 5px;                   /* Separaci\u00f3n superior */")

        self.gridLayout_4.addWidget(self.SensorIR1, 0, 0, 1, 1)

        self.SensorIR2 = QLabel(self.SensoresIR)
        self.SensorIR2.setObjectName(u"SensorIR2")
        self.SensorIR2.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.SensorIR2.setStyleSheet(u"font-size: 14px;                    /* Tama\u00f1o menor para informaci\u00f3n secundaria */\n"
"font-weight: bold;                 /* Texto en negrita */\n"
"color: #333333;                    /* Gris oscuro para buen contraste sobre blanco */\n"
"padding: 8px;                      /* Espacio interno menor */\n"
"background-color: #ffffff;         /* Fondo blanco puro */\n"
"border-radius: 4px;                /* Esquinas redondeadas menores */\n"
"border: 1px solid #e0e0e0;         /* Borde gris muy claro */\n"
"margin-top: 5px;                   /* Separaci\u00f3n superior */")

        self.gridLayout_4.addWidget(self.SensorIR2, 0, 1, 1, 1)

        self.SensorIR3 = QLabel(self.SensoresIR)
        self.SensorIR3.setObjectName(u"SensorIR3")
        self.SensorIR3.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.SensorIR3.setStyleSheet(u"font-size: 14px;                    /* Tama\u00f1o menor para informaci\u00f3n secundaria */\n"
"font-weight: bold;                 /* Texto en negrita */\n"
"color: #333333;                    /* Gris oscuro para buen contraste sobre blanco */\n"
"padding: 8px;                      /* Espacio interno menor */\n"
"background-color: #ffffff;         /* Fondo blanco puro */\n"
"border-radius: 4px;                /* Esquinas redondeadas menores */\n"
"border: 1px solid #e0e0e0;         /* Borde gris muy claro */\n"
"margin-top: 5px;                   /* Separaci\u00f3n superior */")

        self.gridLayout_4.addWidget(self.SensorIR3, 0, 2, 1, 1)

        self.SensorIR4 = QLabel(self.SensoresIR)
        self.SensorIR4.setObjectName(u"SensorIR4")
        self.SensorIR4.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.SensorIR4.setStyleSheet(u"font-size: 14px;                    /* Tama\u00f1o menor para informaci\u00f3n secundaria */\n"
"font-weight: bold;                 /* Texto en negrita */\n"
"color: #333333;                    /* Gris oscuro para buen contraste sobre blanco */\n"
"padding: 8px;                      /* Espacio interno menor */\n"
"background-color: #ffffff;         /* Fondo blanco puro */\n"
"border-radius: 4px;                /* Esquinas redondeadas menores */\n"
"border: 1px solid #e0e0e0;         /* Borde gris muy claro */\n"
"margin-top: 5px;                   /* Separaci\u00f3n superior */")

        self.gridLayout_4.addWidget(self.SensorIR4, 0, 3, 1, 1)

        self.SensorIR5 = QLabel(self.SensoresIR)
        self.SensorIR5.setObjectName(u"SensorIR5")
        self.SensorIR5.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.SensorIR5.setStyleSheet(u"font-size: 14px;                    /* Tama\u00f1o menor para informaci\u00f3n secundaria */\n"
"font-weight: bold;                 /* Texto en negrita */\n"
"color: #333333;                    /* Gris oscuro para buen contraste sobre blanco */\n"
"padding: 8px;                      /* Espacio interno menor */\n"
"background-color: #ffffff;         /* Fondo blanco puro */\n"
"border-radius: 4px;                /* Esquinas redondeadas menores */\n"
"border: 1px solid #e0e0e0;         /* Borde gris muy claro */\n"
"margin-top: 5px;                   /* Separaci\u00f3n superior */")

        self.gridLayout_4.addWidget(self.SensorIR5, 0, 4, 1, 1)


        self.verticalLayout_2.addWidget(self.SensoresIR)


        self.gridLayout_5.addWidget(self.mandosEInfo, 0, 0, 1, 1)


        self.gridLayout_6.addWidget(self.MandosEinfogroup, 2, 1, 2, 2)


        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)


        self.retranslateUi(irSteering)

        QMetaObject.connectSlotsByName(irSteering)
    # setupUi

    def retranslateUi(self, irSteering):
        irSteering.setWindowTitle(QCoreApplication.translate("irSteering", u"Form", None))
        self.descripcion.setText(QCoreApplication.translate("irSteering", u"<html><head/><body><p align=\"center\"><span style=\" font-size:10pt; font-style:italic;\">Simula la direcci\u00f3n de dos motores DC usando 5 sensores infrarrojos y PWM. Permite calibraci\u00f3n<br/> de la respuesta por PID</span></p></body></html>", None))
        self.diagrama.setTitle(QCoreApplication.translate("irSteering", u"Diagrama de Conexiones", None))
        self.dibujo.setText(QCoreApplication.translate("irSteering", u"<html><head/><body><pre style=\" margin-top:12px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:140%;\"><span style=\" font-family:'Courier New','monospace'; font-size:12px; color:#495057;\">\u250c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2510<br/>\u2502 ESP32 DevKit V1 \u2192 Sensor        \u2502<br/>\u2502                                 \u2502<br/>\u2502 5V \u25cb \u2500\u2500\u2192 VCC (Encoders)         \u2502<br/>\u2502 5V \u25cb \u2500\u2500\u2192 VCC (Logica Puente H)  \u2502<br/>\u2502 GND \u25cb \u2500\u2500\u2192 GND (Encoders)        \u2502<br/>\u2502 GND \u25cb \u2500\u2500\u2192 GND (Puente H)        \u2502<br/>\u2502 D39 \u25cb \u2500\u2500\u2192 D (Encoder Izquierdo) \u2502<br/>\u2502 D34 \u25cb \u2500\u2500\u2192 D (Encoder Derecho)   \u2502<br/>\u2502 D25 \u25cb \u2500\u2500\u2192 "
                        "IN1 (Motor Izquierdo) \u2502<br/>\u2502 D36 \u25cb \u2500\u2500\u2192 IN2 (Motor Izquierdo) \u2502<br/>\u2502 D32 \u25cb \u2500\u2500\u2192 IN3 (Motor Derecho)   \u2502<br/>\u2502 D33 \u25cb \u2500\u2500\u2192 IN4 (Motor Derecho)   \u2502<br/>\u2502 </span><span style=\" font-family:'Courier New','monospace'; font-size:12px; color:#495057;\">Vin (Puente H) \u25cb \u2500\u2500\u2192 12V(Fuente)</span><span style=\" font-family:'Courier New','monospace'; font-size:12px; color:#495057;\">\u2502<br/>\u2514\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2518</span></pre></body></html>", None))
        self.nota.setText(QCoreApplication.translate("irSteering", u"<html><head/><body><p align=\"justify\"><span style=\" font-size:9pt;\">\ud83d\udca1 </span><span style=\" font-size:9pt; font-weight:700;\">Nota:</span><span style=\" font-size:9pt;\"> Aseg\u00farate de conectar el <br/>potenci\u00f3metro correctamente antes <br/>de iniciar el monitoreo</span></p></body></html>", None))
        self.titulo.setText(QCoreApplication.translate("irSteering", u"<html><head/><body><p align=\"center\"><span style=\" font-size:22pt; font-weight:700; color:#007bff;\">Monitoreo de Velocidad y Direcci\u00f3n</span></p></body></html>", None))
        self.controles.setTitle(QCoreApplication.translate("irSteering", u"Controles", None))
        self.iniciarBt.setText(QCoreApplication.translate("irSteering", u"Iniciar Monitoreo", None))
        self.calibrarBt.setText(QCoreApplication.translate("irSteering", u"No Calibrado", None))
        self.MandosEinfogroup.setTitle(QCoreApplication.translate("irSteering", u"Mandos e Info", None))
        self.SensorIzquierdaLabel.setText(QCoreApplication.translate("irSteering", u"<html><head/><body><p align=\"center\"><span style=\" font-size:28pt;\">L</span></p></body></html>", None))
        self.SensorDerechaLabel.setText(QCoreApplication.translate("irSteering", u"<html><head/><body><p align=\"center\"><span style=\" font-size:28pt;\">R</span></p></body></html>", None))
        self.RPMizquierdaDt.setText(QCoreApplication.translate("irSteering", u"<html><head/><body><p align=\"center\"><span style=\" font-size:16pt; text-decoration: underline;\">--</span></p></body></html>", None))
        self.RPMderechaDt.setText(QCoreApplication.translate("irSteering", u"<html><head/><body><p align=\"center\"><span style=\" font-size:16pt; text-decoration: underline;\">--</span></p></body></html>", None))
        self.RPMsLabel.setText(QCoreApplication.translate("irSteering", u"<html><head/><body><p align=\"center\"><span style=\" font-size:16pt; font-style:italic;\">RPMs</span></p></body></html>", None))
        self.SensorIR1.setText(QCoreApplication.translate("irSteering", u"<html><head/><body><p align=\"center\"><span style=\" font-size:24pt; font-weight:400;\">\u26ab</span></p></body></html>", None))
        self.SensorIR2.setText(QCoreApplication.translate("irSteering", u"<html><head/><body><p align=\"center\"><span style=\" font-size:24pt; font-weight:400;\">\u26ab</span></p></body></html>", None))
        self.SensorIR3.setText(QCoreApplication.translate("irSteering", u"<html><head/><body><p align=\"center\"><span style=\" font-size:24pt; font-weight:400;\">\u26ab</span></p></body></html>", None))
        self.SensorIR4.setText(QCoreApplication.translate("irSteering", u"<html><head/><body><p align=\"center\"><span style=\" font-size:24pt; font-weight:400;\">\u26ab</span></p></body></html>", None))
        self.SensorIR5.setText(QCoreApplication.translate("irSteering", u"<html><head/><body><p align=\"center\"><span style=\" font-size:24pt; font-weight:400;\">\u26ab</span></p></body></html>", None))
    # retranslateUi

