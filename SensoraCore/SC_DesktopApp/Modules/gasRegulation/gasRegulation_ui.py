# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'gasRegulation.ui'
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
    QHBoxLayout, QLabel, QPushButton, QScrollArea,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_gasRegulation(object):
    def setupUi(self, gasRegulation):
        if not gasRegulation.objectName():
            gasRegulation.setObjectName(u"gasRegulation")
        gasRegulation.resize(764, 704)
        gasRegulation.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"border: 1px solid rgb(221, 221, 221);\n"
"border-radius: 5px;\n"
"color: rgb(0, 0, 0);")
        self.gridLayout_2 = QGridLayout(gasRegulation)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.frame = QFrame(gasRegulation)
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

        self.grafica = QGroupBox(self.frame)
        self.grafica.setObjectName(u"grafica")
        self.grafica.setMinimumSize(QSize(400, 470))
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

        self.Info = QGroupBox(self.frame)
        self.Info.setObjectName(u"Info")
        self.Info.setMinimumSize(QSize(320, 0))
        self.Info.setMaximumSize(QSize(300, 16777215))
        self.Info.setStyleSheet(u"QGroupBox {\n"
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
        self.verticalLayout = QVBoxLayout(self.Info)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.scrollArea = QScrollArea(self.Info)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setStyleSheet(u"")
        self.scrollArea.setWidgetResizable(True)
        self.SelectorDeSensores = QWidget()
        self.SelectorDeSensores.setObjectName(u"SelectorDeSensores")
        self.SelectorDeSensores.setGeometry(QRect(0, 0, 298, 191))
        self.verticalLayout_2 = QVBoxLayout(self.SelectorDeSensores)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.MQ2 = QPushButton(self.SelectorDeSensores)
        self.MQ2.setObjectName(u"MQ2")
        self.MQ2.setMinimumSize(QSize(105, 25))
        self.MQ2.setMaximumSize(QSize(999, 999))
        self.MQ2.setStyleSheet(u"QPushButton {\n"
"    font-size: 14px;\n"
"    font-weight: bold;\n"
"    color: rgb(0, 0, 0);\n"
"    background-color: rgb(236, 236, 236);\n"
"    border-radius: 4px;\n"
"}\n"
"\n"
"/* Hover: verde suave */\n"
"QPushButton:hover {\n"
"    background-color: rgb(220, 255, 220);\n"
"    color: rgb(0, 100, 0);\n"
"}\n"
"\n"
"/* Pressed: verde m\u00e1s profundo */\n"
"QPushButton:pressed {\n"
"    background-color: rgb(200, 240, 200);\n"
"    color: rgb(0, 80, 0);\n"
"}\n"
"\n"
"/* Toggle ON (checked): tonos rojos */\n"
"QPushButton:checked {\n"
"    background-color: rgb(255, 200, 200);   /* Rojo claro */\n"
"    color: rgb(120, 0, 0);                  /* Rojo oscuro para texto */\n"
"    border: 2px solid rgb(180, 0, 0);       /* Borde rojo intenso */\n"
"}")

        self.verticalLayout_2.addWidget(self.MQ2)

        self.MQ3 = QPushButton(self.SelectorDeSensores)
        self.MQ3.setObjectName(u"MQ3")
        self.MQ3.setMinimumSize(QSize(105, 25))
        self.MQ3.setMaximumSize(QSize(999, 999))
        self.MQ3.setStyleSheet(u"QPushButton {\n"
"    font-size: 14px;\n"
"    font-weight: bold;\n"
"    color: rgb(0, 0, 0);\n"
"    background-color: rgb(236, 236, 236);\n"
"    border-radius: 4px;\n"
"}\n"
"\n"
"/* Hover: verde suave */\n"
"QPushButton:hover {\n"
"    background-color: rgb(220, 255, 220);\n"
"    color: rgb(0, 100, 0);\n"
"}\n"
"\n"
"/* Pressed: verde m\u00e1s profundo */\n"
"QPushButton:pressed {\n"
"    background-color: rgb(200, 240, 200);\n"
"    color: rgb(0, 80, 0);\n"
"}\n"
"\n"
"/* Toggle ON (checked): tonos rojos */\n"
"QPushButton:checked {\n"
"    background-color: rgb(255, 200, 200);   /* Rojo claro */\n"
"    color: rgb(120, 0, 0);                  /* Rojo oscuro para texto */\n"
"    border: 2px solid rgb(180, 0, 0);       /* Borde rojo intenso */\n"
"}")

        self.verticalLayout_2.addWidget(self.MQ3)

        self.scrollArea.setWidget(self.SelectorDeSensores)

        self.verticalLayout.addWidget(self.scrollArea)

        self.controles = QGroupBox(self.Info)
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


        self.gridLayout_4.addWidget(self.botones, 1, 0, 1, 1)


        self.verticalLayout.addWidget(self.controles)

        self.nota = QLabel(self.Info)
        self.nota.setObjectName(u"nota")
        self.nota.setMinimumSize(QSize(0, 200))
        self.nota.setMaximumSize(QSize(99999, 99999))
        self.nota.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.nota.setStyleSheet(u"        font-size: 13px;                    /* Tama\u00f1o menor para nota */\n"
"        color: #856404;                     /* Color \u00e1mbar oscuro */\n"
"        background-color: #fff3cd;          /* Fondo \u00e1mbar claro (alerta) */\n"
"        border: 1px solid #ffeaa7;          /* Borde \u00e1mbar */\n"
"        border-radius: 4px;                 /* Esquinas redondeadas */\n"
"        padding: 8px;                       /* Espacio interno */\n"
"        margin-top: 5px;                    /* Separaci\u00f3n superior */\n"
"")

        self.verticalLayout.addWidget(self.nota)


        self.gridLayout_6.addWidget(self.Info, 2, 0, 2, 1)

        self.datos = QWidget(self.frame)
        self.datos.setObjectName(u"datos")
        self.datos.setMinimumSize(QSize(0, 0))
        self.datos.setMaximumSize(QSize(9999, 16777215))
        self.gridLayout = QGridLayout(self.datos)
        self.gridLayout.setObjectName(u"gridLayout")
        self.LecturaMQ2Dt = QLabel(self.datos)
        self.LecturaMQ2Dt.setObjectName(u"LecturaMQ2Dt")

        self.gridLayout.addWidget(self.LecturaMQ2Dt, 1, 1, 1, 1)

        self.datosLabel = QLabel(self.datos)
        self.datosLabel.setObjectName(u"datosLabel")

        self.gridLayout.addWidget(self.datosLabel, 0, 0, 1, 1)

        self.MQ2Label = QLabel(self.datos)
        self.MQ2Label.setObjectName(u"MQ2Label")

        self.gridLayout.addWidget(self.MQ2Label, 0, 1, 1, 1)

        self.MQ3Label = QLabel(self.datos)
        self.MQ3Label.setObjectName(u"MQ3Label")

        self.gridLayout.addWidget(self.MQ3Label, 0, 2, 1, 1)

        self.LecturaLabel = QLabel(self.datos)
        self.LecturaLabel.setObjectName(u"LecturaLabel")

        self.gridLayout.addWidget(self.LecturaLabel, 1, 0, 1, 1)

        self.ppmMQ2Dt = QLabel(self.datos)
        self.ppmMQ2Dt.setObjectName(u"ppmMQ2Dt")

        self.gridLayout.addWidget(self.ppmMQ2Dt, 2, 1, 1, 1)

        self.LecturaMQ3Dt = QLabel(self.datos)
        self.LecturaMQ3Dt.setObjectName(u"LecturaMQ3Dt")

        self.gridLayout.addWidget(self.LecturaMQ3Dt, 1, 2, 1, 1)

        self.ppmMQ3Dt = QLabel(self.datos)
        self.ppmMQ3Dt.setObjectName(u"ppmMQ3Dt")

        self.gridLayout.addWidget(self.ppmMQ3Dt, 2, 2, 1, 1)

        self.TemperaturaLabel = QLabel(self.datos)
        self.TemperaturaLabel.setObjectName(u"TemperaturaLabel")

        self.gridLayout.addWidget(self.TemperaturaLabel, 2, 0, 1, 1)

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

        self.ppmMQ2DtCalibrado = QLabel(self.calBox)
        self.ppmMQ2DtCalibrado.setObjectName(u"ppmMQ2DtCalibrado")
        self.ppmMQ2DtCalibrado.setStyleSheet(u"background-color: rgb(255, 255, 255);")

        self.horizontalLayout_2.addWidget(self.ppmMQ2DtCalibrado)

        self.ppmMQ3DtCalibrado = QLabel(self.calBox)
        self.ppmMQ3DtCalibrado.setObjectName(u"ppmMQ3DtCalibrado")
        self.ppmMQ3DtCalibrado.setStyleSheet(u"background-color: rgb(255, 255, 255);")

        self.horizontalLayout_2.addWidget(self.ppmMQ3DtCalibrado)


        self.gridLayout.addWidget(self.calBox, 4, 0, 1, 3)


        self.gridLayout_6.addWidget(self.datos, 3, 1, 1, 2)


        self.gridLayout_2.addWidget(self.frame, 0, 0, 1, 1)


        self.retranslateUi(gasRegulation)

        QMetaObject.connectSlotsByName(gasRegulation)
    # setupUi

    def retranslateUi(self, gasRegulation):
        gasRegulation.setWindowTitle(QCoreApplication.translate("gasRegulation", u"Form", None))
        self.titulo.setText(QCoreApplication.translate("gasRegulation", u"<html><head/><body><p align=\"center\"><span style=\" font-size:22pt; font-weight:700; color:#007bff;\">Monitoreo de Densidad de Gases</span></p></body></html>", None))
        self.grafica.setTitle(QCoreApplication.translate("gasRegulation", u"Gr\u00e1fica", None))
        self.descripcion.setText(QCoreApplication.translate("gasRegulation", u"<html><head/><body><p align=\"center\"><span style=\" font-size:10pt; font-style:italic;\">Mide densidad de gases usando MQ2 y MQ3. Traduce a ppm con calibraci\u00f3n por Regresi\u00f3n Lineal en Espacio Logar\u00edtmico.</span></p></body></html>", None))
        self.Info.setTitle(QCoreApplication.translate("gasRegulation", u"Info", None))
        self.MQ2.setText(QCoreApplication.translate("gasRegulation", u"MQ2", None))
        self.MQ3.setText(QCoreApplication.translate("gasRegulation", u"MQ3", None))
        self.controles.setTitle(QCoreApplication.translate("gasRegulation", u"Controles", None))
        self.calibrarBt.setText(QCoreApplication.translate("gasRegulation", u"No Calibrado", None))
        self.exportarBt.setText(QCoreApplication.translate("gasRegulation", u"Exportal a Exel", None))
        self.limpiarBt.setText(QCoreApplication.translate("gasRegulation", u"Limpiar Gr\u00e1fica", None))
        self.iniciarBt.setText(QCoreApplication.translate("gasRegulation", u"Iniciar Monitoreo", None))
        self.nota.setText(QCoreApplication.translate("gasRegulation", u"<html><head/><body><p align=\"justify\"><span style=\" font-size:9pt;\">\ud83d\udca1 </span><span style=\" font-size:9pt; font-weight:700;\">Nota:</span><span style=\" font-size:9pt;\"> Aseg\u00farate de conectar los <br/>componentes correctamente antes de <br/>iniciar el monitoreo.</span></p><p align=\"justify\"><span style=\" font-size:9pt;\">Selecciona uno de los tipo de <br/>sensor de Gases y luego<br/>siga con la experiencia de <br/>monitoreo convencional.</span></p></body></html>", None))
        self.LecturaMQ2Dt.setText(QCoreApplication.translate("gasRegulation", u"--", None))
        self.datosLabel.setText(QCoreApplication.translate("gasRegulation", u"Datos", None))
        self.MQ2Label.setText(QCoreApplication.translate("gasRegulation", u"MQ2", None))
        self.MQ3Label.setText(QCoreApplication.translate("gasRegulation", u"MQ3", None))
        self.LecturaLabel.setText(QCoreApplication.translate("gasRegulation", u"Lectura", None))
        self.ppmMQ2Dt.setText(QCoreApplication.translate("gasRegulation", u"--", None))
        self.LecturaMQ3Dt.setText(QCoreApplication.translate("gasRegulation", u"--", None))
        self.ppmMQ3Dt.setText(QCoreApplication.translate("gasRegulation", u"--", None))
        self.TemperaturaLabel.setText(QCoreApplication.translate("gasRegulation", u"Particulas x Mill\u00f3n", None))
        self.calibradoLabel.setText(QCoreApplication.translate("gasRegulation", u"TempCalibrada", None))
        self.ppmMQ2DtCalibrado.setText(QCoreApplication.translate("gasRegulation", u"--", None))
        self.ppmMQ3DtCalibrado.setText(QCoreApplication.translate("gasRegulation", u"--", None))
    # retranslateUi

