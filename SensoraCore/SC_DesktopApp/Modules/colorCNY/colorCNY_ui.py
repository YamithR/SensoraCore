# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'colorCNY.ui'
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
    QLabel, QPushButton, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_colorCNY(object):
    def setupUi(self, colorCNY):
        if not colorCNY.objectName():
            colorCNY.setObjectName(u"colorCNY")
        colorCNY.resize(737, 501)
        colorCNY.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"border: 1px solid rgb(221, 221, 221);\n"
"border-radius: 5px;\n"
"color: rgb(0, 0, 0);")
        self.gridLayout_7 = QGridLayout(colorCNY)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.frame = QFrame(colorCNY)
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
        self.botones = QWidget(self.controles)
        self.botones.setObjectName(u"botones")
        self.gridLayout_3 = QGridLayout(self.botones)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
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

        self.gridLayout_3.addWidget(self.iniciarBt, 0, 0, 1, 2)


        self.gridLayout_4.addWidget(self.botones, 0, 0, 1, 1)

        self.datos = QWidget(self.controles)
        self.datos.setObjectName(u"datos")
        self.datos.setMinimumSize(QSize(0, 0))
        self.datos.setMaximumSize(QSize(9999, 16777215))
        self.gridLayout = QGridLayout(self.datos)
        self.gridLayout.setObjectName(u"gridLayout")
        self.CNY70Label = QLabel(self.datos)
        self.CNY70Label.setObjectName(u"CNY70Label")

        self.gridLayout.addWidget(self.CNY70Label, 1, 0, 1, 1)

        self.porcentajeDeNegroLabel = QLabel(self.datos)
        self.porcentajeDeNegroLabel.setObjectName(u"porcentajeDeNegroLabel")

        self.gridLayout.addWidget(self.porcentajeDeNegroLabel, 0, 3, 1, 1)

        self.analogoDtCny70 = QLabel(self.datos)
        self.analogoDtCny70.setObjectName(u"analogoDtCny70")

        self.gridLayout.addWidget(self.analogoDtCny70, 1, 1, 1, 1)

        self.porcentajeDeBlancoDt = QLabel(self.datos)
        self.porcentajeDeBlancoDt.setObjectName(u"porcentajeDeBlancoDt")

        self.gridLayout.addWidget(self.porcentajeDeBlancoDt, 1, 2, 1, 1)

        self.porcentajeDeNegroDt = QLabel(self.datos)
        self.porcentajeDeNegroDt.setObjectName(u"porcentajeDeNegroDt")

        self.gridLayout.addWidget(self.porcentajeDeNegroDt, 1, 3, 1, 1)

        self.analogoLabel = QLabel(self.datos)
        self.analogoLabel.setObjectName(u"analogoLabel")

        self.gridLayout.addWidget(self.analogoLabel, 0, 1, 1, 1)

        self.porcentajeDeBlancoLabel = QLabel(self.datos)
        self.porcentajeDeBlancoLabel.setObjectName(u"porcentajeDeBlancoLabel")

        self.gridLayout.addWidget(self.porcentajeDeBlancoLabel, 0, 2, 1, 1)

        self.datosLabel = QLabel(self.datos)
        self.datosLabel.setObjectName(u"datosLabel")

        self.gridLayout.addWidget(self.datosLabel, 0, 0, 1, 1)


        self.gridLayout_4.addWidget(self.datos, 0, 1, 1, 1)


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
        self.verticalLayout = QVBoxLayout(self.diagrama)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.dibujo = QLabel(self.diagrama)
        self.dibujo.setObjectName(u"dibujo")
        self.dibujo.setMinimumSize(QSize(0, 120))
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


        self.gridLayout_7.addWidget(self.frame, 0, 0, 1, 1)


        self.retranslateUi(colorCNY)

        QMetaObject.connectSlotsByName(colorCNY)
    # setupUi

    def retranslateUi(self, colorCNY):
        colorCNY.setWindowTitle(QCoreApplication.translate("colorCNY", u"Form", None))
        self.titulo.setText(QCoreApplication.translate("colorCNY", u"<html><head/><body><p align=\"center\"><span style=\" font-size:22pt; font-weight:700; color:#007bff;\">Detecci\u00f3n B&amp;W</span></p></body></html>", None))
        self.controles.setTitle(QCoreApplication.translate("colorCNY", u"Controles", None))
        self.exportarBt.setText(QCoreApplication.translate("colorCNY", u"Exportal a Exel", None))
        self.limpiarBt.setText(QCoreApplication.translate("colorCNY", u"Limpiar Gr\u00e1fica", None))
        self.iniciarBt.setText(QCoreApplication.translate("colorCNY", u"Iniciar Monitoreo", None))
        self.CNY70Label.setText(QCoreApplication.translate("colorCNY", u"CNY70", None))
        self.porcentajeDeNegroLabel.setText(QCoreApplication.translate("colorCNY", u"%Negro", None))
        self.analogoDtCny70.setText(QCoreApplication.translate("colorCNY", u"--", None))
        self.porcentajeDeBlancoDt.setText(QCoreApplication.translate("colorCNY", u"--", None))
        self.porcentajeDeNegroDt.setText(QCoreApplication.translate("colorCNY", u"--", None))
        self.analogoLabel.setText(QCoreApplication.translate("colorCNY", u"An\u00e1logo", None))
        self.porcentajeDeBlancoLabel.setText(QCoreApplication.translate("colorCNY", u"%Blanco", None))
        self.datosLabel.setText(QCoreApplication.translate("colorCNY", u"Datos", None))
        self.diagrama.setTitle(QCoreApplication.translate("colorCNY", u"Diagrama de Conexiones", None))
        self.dibujo.setText(QCoreApplication.translate("colorCNY", u"<html><head/><body><pre style=\" margin-top:12px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New','monospace'; font-size:12px; color:#495057;\">\u250c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2510</span></pre><pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New','monospace'; font-size:12px; color:#495057;\">\u2502  ESP32 DevKit V1                   \u2502</span></pre><pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New','monospace'; font-size:12px; color:#495057;\">\u2502                                    \u2502</span></pre><pre style=\""
                        " margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New','monospace'; font-size:12px; color:#495057;\">\u2502  3V3  \u25cb \u2500\u2500\u2192 LED \u00c1nodo (con R 180\u03a9) \u2502</span></pre><pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New','monospace'; font-size:12px; color:#495057;\">\u2502  GND  \u25cb \u2500\u2500\u2192 LED C\u00e1todo             \u2502</span></pre><pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New','monospace'; font-size:12px; color:#495057;\">\u2502  GND  \u25cb \u2500\u2500\u2192 Colector  (R 10k)      \u2502</span></pre><pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:"
                        "'Courier New','monospace'; font-size:12px; color:#495057;\">\u2502  D25  \u25cb \u2190\u2500 Emisor Fototransistor   \u2502</span></pre><pre style=\" margin-top:0px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New','monospace'; font-size:12px; color:#495057;\">\u2514\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2518</span></pre></body></html>", None))
        self.nota.setText(QCoreApplication.translate("colorCNY", u"<html><head/><body><p align=\"justify\"><span style=\" font-size:9pt;\">\ud83d\udca1 </span><span style=\" font-size:9pt; font-weight:700;\">Nota:</span><span style=\" font-size:9pt;\"> Aseg\u00farate de conectar los <br/>componentes correctamente antes de <br/>iniciar el monitoreo</span></p></body></html>", None))
        self.grafica.setTitle(QCoreApplication.translate("colorCNY", u"Gr\u00e1fica", None))
        self.descripcion.setText(QCoreApplication.translate("colorCNY", u"<html><head/><body><p align=\"center\"><span style=\" font-size:10pt; font-style:italic;\">Monitorea en tiempo real lectura anal\u00f3gica del sensor \u00f3ptico CNY70 para caracterizaci\u00f3n.</span></p></body></html>", None))
    # retranslateUi

