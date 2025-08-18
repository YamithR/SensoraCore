# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'simpleAngle.ui'
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

class Ui_simpleAngle(object):
    def setupUi(self, simpleAngle):
        if not simpleAngle.objectName():
            simpleAngle.setObjectName(u"simpleAngle")
        simpleAngle.resize(749, 696)
        simpleAngle.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"border: 1px solid rgb(221, 221, 221);\n"
"border-radius: 5px;\n"
"color: rgb(0, 0, 0);")
        self.gridLayout = QGridLayout(simpleAngle)
        self.gridLayout.setObjectName(u"gridLayout")
        self.frame = QFrame(simpleAngle)
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
        self.iniciar = QPushButton(self.botones)
        self.iniciar.setObjectName(u"iniciar")
        self.iniciar.setStyleSheet(u"font-size: 14px;                   \n"
"font-weight: bold;             \n"
"color: rgb(0, 0, 0);\n"
"padding: 8px;                \n"
"background-color: rgb(236, 236, 236);         \n"
"border-radius: 4px;           \n"
"border: 1px solid rgb(0, 0, 0);     \n"
"margin-top: 5px;        ")

        self.gridLayout_3.addWidget(self.iniciar, 0, 0, 1, 1)

        self.calibrar = QPushButton(self.botones)
        self.calibrar.setObjectName(u"calibrar")
        self.calibrar.setStyleSheet(u"        font-size: 14px;                    /* Tama\u00f1o menor para informaci\u00f3n secundaria */\n"
"        font-weight: bold;                  /* Texto en negrita */\n"
"        color: #856404;                     /* Color \u00e1mbar para indicar estado */\n"
"        padding: 8px;                       /* Espacio interno menor */\n"
"        background-color: #fff3cd;          /* Fondo \u00e1mbar claro */\n"
"        border-radius: 4px;                 /* Esquinas redondeadas menores */\n"
"        border: 1px solid #ffeaa7;          /* Borde \u00e1mbar */\n"
"        margin-top: 5px;                    /* Separaci\u00f3n superior */")

        self.gridLayout_3.addWidget(self.calibrar, 0, 1, 1, 1)

        self.limpiar = QPushButton(self.botones)
        self.limpiar.setObjectName(u"limpiar")
        self.limpiar.setStyleSheet(u"/* Estilo base con matices rosa y gris degradado */\n"
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

        self.gridLayout_3.addWidget(self.limpiar, 1, 0, 1, 1)

        self.exportar = QPushButton(self.botones)
        self.exportar.setObjectName(u"exportar")
        self.exportar.setStyleSheet(u"        font-size: 14px;                    /* Tama\u00f1o menor para informaci\u00f3n secundaria */\n"
"        font-weight: bold;                  /* Texto en negrita */\n"
"        color: #856404;                     /* Color \u00e1mbar para indicar estado */\n"
"        padding: 8px;                       /* Espacio interno menor */\n"
"        background-color: #fff3cd;          /* Fondo \u00e1mbar claro */\n"
"        border-radius: 4px;                 /* Esquinas redondeadas menores */\n"
"        border: 1px solid #ffeaa7;          /* Borde \u00e1mbar */\n"
"        margin-top: 5px;                    /* Separaci\u00f3n superior */")

        self.gridLayout_3.addWidget(self.exportar, 1, 1, 1, 1)


        self.horizontalLayout.addWidget(self.botones)

        self.datos = QWidget(self.controles)
        self.datos.setObjectName(u"datos")
        self.datos.setMaximumSize(QSize(900, 16777215))
        self.gridLayout_4 = QGridLayout(self.datos)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.datosLabel = QLabel(self.datos)
        self.datosLabel.setObjectName(u"datosLabel")

        self.gridLayout_4.addWidget(self.datosLabel, 0, 0, 1, 1)

        self.analogo = QLabel(self.datos)
        self.analogo.setObjectName(u"analogo")

        self.gridLayout_4.addWidget(self.analogo, 0, 1, 1, 1)

        self.angulo = QLabel(self.datos)
        self.angulo.setObjectName(u"angulo")

        self.gridLayout_4.addWidget(self.angulo, 0, 2, 1, 1)

        self.lectura = QLabel(self.datos)
        self.lectura.setObjectName(u"lectura")

        self.gridLayout_4.addWidget(self.lectura, 1, 0, 1, 1)

        self.analogoDt = QLabel(self.datos)
        self.analogoDt.setObjectName(u"analogoDt")

        self.gridLayout_4.addWidget(self.analogoDt, 1, 1, 1, 1)

        self.anguloDt = QLabel(self.datos)
        self.anguloDt.setObjectName(u"anguloDt")

        self.gridLayout_4.addWidget(self.anguloDt, 1, 2, 1, 1)

        self.calBox = QWidget(self.datos)
        self.calBox.setObjectName(u"calBox")
        self.horizontalLayout_2 = QHBoxLayout(self.calBox)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(3, 3, 3, 3)
        self.calibrado = QLabel(self.calBox)
        self.calibrado.setObjectName(u"calibrado")

        self.horizontalLayout_2.addWidget(self.calibrado)

        self.analogoDtCal = QLabel(self.calBox)
        self.analogoDtCal.setObjectName(u"analogoDtCal")

        self.horizontalLayout_2.addWidget(self.analogoDtCal)

        self.anguloDtCal = QLabel(self.calBox)
        self.anguloDtCal.setObjectName(u"anguloDtCal")

        self.horizontalLayout_2.addWidget(self.anguloDtCal)


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
        self.dibujo.setMinimumSize(QSize(0, 285))
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
        self.grafica.setMinimumSize(QSize(0, 380))
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


        self.retranslateUi(simpleAngle)

        QMetaObject.connectSlotsByName(simpleAngle)
    # setupUi

    def retranslateUi(self, simpleAngle):
        simpleAngle.setWindowTitle(QCoreApplication.translate("simpleAngle", u"Form", None))
        self.titulo.setText(QCoreApplication.translate("simpleAngle", u"<html><head/><body><p align=\"center\"><span style=\" font-size:22pt; font-weight:700; color:#007bff;\">Monitoreo de Sensor de \u00c1ngulo</span></p></body></html>", None))
        self.controles.setTitle(QCoreApplication.translate("simpleAngle", u"Controles", None))
        self.iniciar.setText(QCoreApplication.translate("simpleAngle", u"Iniciar Monitoreo", None))
        self.calibrar.setText(QCoreApplication.translate("simpleAngle", u"No Calibrado", None))
        self.limpiar.setText(QCoreApplication.translate("simpleAngle", u"Limpiar Gr\u00e1fica", None))
        self.exportar.setText(QCoreApplication.translate("simpleAngle", u"Exportal a Exel", None))
        self.datosLabel.setText(QCoreApplication.translate("simpleAngle", u"Datos", None))
        self.analogo.setText(QCoreApplication.translate("simpleAngle", u"An\u00e1logo", None))
        self.angulo.setText(QCoreApplication.translate("simpleAngle", u"\u00c1ngulo", None))
        self.lectura.setText(QCoreApplication.translate("simpleAngle", u"Lectura", None))
        self.analogoDt.setText(QCoreApplication.translate("simpleAngle", u"--", None))
        self.anguloDt.setText(QCoreApplication.translate("simpleAngle", u"--", None))
        self.calibrado.setText(QCoreApplication.translate("simpleAngle", u"Calibrado", None))
        self.analogoDtCal.setText(QCoreApplication.translate("simpleAngle", u"--", None))
        self.anguloDtCal.setText(QCoreApplication.translate("simpleAngle", u"--", None))
        self.diagrama.setTitle(QCoreApplication.translate("simpleAngle", u"Diagrama de Conexiones", None))
        self.dibujo.setText(QCoreApplication.translate("simpleAngle", u"<html><head/><body><pre style=\" margin-top:12px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:140%;\"><span style=\" font-family:'Courier New','monospace'; font-size:12px; color:#495057;\">\u250c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2510</span></pre><pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:140%;\"><span style=\" font-family:'Courier New','monospace'; font-size:12px; color:#495057;\">\u2502  ESP32 DevKit V1                \u2502</span></pre><pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:140%;\"><span style=\" font-family:'Courier New','monospace'; font-size:12px; color:#495057;\">\u2502                                 \u2502"
                        "</span></pre><pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:140%;\"><span style=\" font-family:'Courier New','monospace'; font-size:12px; color:#495057;\">\u2502  3V3  \u25cb \u2190\u2500\u2500 Potenci\u00f3metro (+)   \u2502</span></pre><pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:140%;\"><span style=\" font-family:'Courier New','monospace'; font-size:12px; color:#495057;\">\u2502  D32  \u25cb \u2190\u2500\u2500 Potenci\u00f3metro (S)   \u2502</span></pre><pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:140%;\"><span style=\" font-family:'Courier New','monospace'; font-size:12px; color:#495057;\">\u2502  GND  \u25cb \u2190\u2500\u2500 Potenci\u00f3metro (-)   \u2502</span></pre><pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:"
                        "0px; -qt-block-indent:0; text-indent:0px; line-height:140%;\"><span style=\" font-family:'Courier New','monospace'; font-size:12px; color:#495057;\">\u2502                                 \u2502</span></pre><pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:140%;\"><span style=\" font-family:'Courier New','monospace'; font-size:12px; color:#495057;\">\u2502  LED integrado: GPIO 2          \u2502</span></pre><pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:140%;\"><span style=\" font-family:'Courier New','monospace'; font-size:12px; color:#495057;\">\u2514\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2518</span></pre><pre style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-"
                        "left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:140%; font-family:'Courier New','monospace'; font-size:12px; color:#495057;\"><br/></pre><pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:140%;\"><span style=\" font-family:'Courier New','monospace'; font-size:12px; font-weight:700; color:#495057;\">Potenci\u00f3metro 10k\u03a9:</span></pre><pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:140%;\"><span style=\" font-family:'Courier New','monospace'; font-size:12px; color:#495057;\"> \u2022 Pin (+): Alimentaci\u00f3n 3.3V</span></pre><pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:140%;\"><span style=\" font-family:'Courier New','monospace'; font-size:12px; color:#495057;\"> \u2022 Pin (-): Tierra (GND)  </span></pre><pre style=\" margin"
                        "-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:140%;\"><span style=\" font-family:'Courier New','monospace'; font-size:12px; color:#495057;\"> \u2022 Pin (S): Se\u00f1al anal\u00f3gica \u2192 GPIO 32</span></pre></body></html>", None))
        self.nota.setText(QCoreApplication.translate("simpleAngle", u"<html><head/><body><p align=\"justify\"><span style=\" font-size:9pt;\">\ud83d\udca1 </span><span style=\" font-size:9pt; font-weight:700;\">Nota:</span><span style=\" font-size:9pt;\"> Aseg\u00farate de conectar el <br/>potenci\u00f3metro correctamente antes <br/>de iniciar el monitoreo</span></p></body></html>", None))
        self.grafica.setTitle(QCoreApplication.translate("simpleAngle", u"Gr\u00e1fica", None))
        self.descripcion.setText(QCoreApplication.translate("simpleAngle", u"<html><head/><body><p align=\"center\"><span style=\" font-size:10pt; font-style:italic;\">Monitorea en tiempo real la lectura anal\u00f3gico digital del sensor potenci\u00f3metro conectado a un pin GPIO del microcontrolador <br/>para traducirlo a \u00c1ngulo y su posterior calibraci\u00f3n por medio de Regresi\u00f3n Lineal Asistida. Incluye informaci\u00f3n did\u00e1ctica<br/> para su caracterizaci\u00f3n.</span></p></body></html>", None))
    # retranslateUi

