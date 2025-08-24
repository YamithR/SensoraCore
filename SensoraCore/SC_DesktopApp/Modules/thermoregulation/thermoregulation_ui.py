# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'thermoregulation.ui'
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

class Ui_thermoregulation(object):
    def setupUi(self, thermoregulation):
        if not thermoregulation.objectName():
            thermoregulation.setObjectName(u"thermoregulation")
        thermoregulation.resize(850, 704)
        thermoregulation.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"border: 1px solid rgb(221, 221, 221);\n"
"border-radius: 5px;\n"
"color: rgb(0, 0, 0);")
        self.gridLayout_2 = QGridLayout(thermoregulation)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.frame = QFrame(thermoregulation)
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
        self.LM35 = QPushButton(self.SelectorDeSensores)
        self.LM35.setObjectName(u"LM35")
        self.LM35.setMinimumSize(QSize(105, 25))
        self.LM35.setMaximumSize(QSize(999, 999))
        self.LM35.setStyleSheet(u"QPushButton {\n"
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

        self.verticalLayout_2.addWidget(self.LM35)

        self.TermoparTipoK = QPushButton(self.SelectorDeSensores)
        self.TermoparTipoK.setObjectName(u"TermoparTipoK")
        self.TermoparTipoK.setMinimumSize(QSize(105, 25))
        self.TermoparTipoK.setMaximumSize(QSize(999, 999))
        self.TermoparTipoK.setStyleSheet(u"QPushButton {\n"
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

        self.verticalLayout_2.addWidget(self.TermoparTipoK)

        self.DS18B20 = QPushButton(self.SelectorDeSensores)
        self.DS18B20.setObjectName(u"DS18B20")
        self.DS18B20.setMinimumSize(QSize(105, 25))
        self.DS18B20.setMaximumSize(QSize(999, 999))
        self.DS18B20.setStyleSheet(u"QPushButton {\n"
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

        self.verticalLayout_2.addWidget(self.DS18B20)

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
        self.LecturaLm35Dt = QLabel(self.datos)
        self.LecturaLm35Dt.setObjectName(u"LecturaLm35Dt")

        self.gridLayout.addWidget(self.LecturaLm35Dt, 1, 1, 1, 1)

        self.LecturaDS18B20Dt = QLabel(self.datos)
        self.LecturaDS18B20Dt.setObjectName(u"LecturaDS18B20Dt")

        self.gridLayout.addWidget(self.LecturaDS18B20Dt, 1, 3, 1, 1)

        self.datosLabel = QLabel(self.datos)
        self.datosLabel.setObjectName(u"datosLabel")

        self.gridLayout.addWidget(self.datosLabel, 0, 0, 1, 1)

        self.Lm35Label = QLabel(self.datos)
        self.Lm35Label.setObjectName(u"Lm35Label")

        self.gridLayout.addWidget(self.Lm35Label, 0, 1, 1, 1)

        self.TypeKLabel = QLabel(self.datos)
        self.TypeKLabel.setObjectName(u"TypeKLabel")

        self.gridLayout.addWidget(self.TypeKLabel, 0, 2, 1, 1)

        self.DS18B20Label = QLabel(self.datos)
        self.DS18B20Label.setObjectName(u"DS18B20Label")

        self.gridLayout.addWidget(self.DS18B20Label, 0, 3, 1, 1)

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

        self.Lm35DtCalibrado = QLabel(self.calBox)
        self.Lm35DtCalibrado.setObjectName(u"Lm35DtCalibrado")
        self.Lm35DtCalibrado.setStyleSheet(u"background-color: rgb(255, 255, 255);")

        self.horizontalLayout_2.addWidget(self.Lm35DtCalibrado)

        self.TypeKDtCalibrado = QLabel(self.calBox)
        self.TypeKDtCalibrado.setObjectName(u"TypeKDtCalibrado")
        self.TypeKDtCalibrado.setStyleSheet(u"background-color: rgb(255, 255, 255);")

        self.horizontalLayout_2.addWidget(self.TypeKDtCalibrado)

        self.DS18B20DtCalibrado = QLabel(self.calBox)
        self.DS18B20DtCalibrado.setObjectName(u"DS18B20DtCalibrado")
        self.DS18B20DtCalibrado.setStyleSheet(u"background-color: rgb(255, 255, 255);")

        self.horizontalLayout_2.addWidget(self.DS18B20DtCalibrado)


        self.gridLayout.addWidget(self.calBox, 4, 0, 1, 4)

        self.LecturaLabel = QLabel(self.datos)
        self.LecturaLabel.setObjectName(u"LecturaLabel")

        self.gridLayout.addWidget(self.LecturaLabel, 1, 0, 1, 1)

        self.TemperaturaLm35Dt = QLabel(self.datos)
        self.TemperaturaLm35Dt.setObjectName(u"TemperaturaLm35Dt")

        self.gridLayout.addWidget(self.TemperaturaLm35Dt, 2, 1, 1, 1)

        self.LecturaTypeKDt = QLabel(self.datos)
        self.LecturaTypeKDt.setObjectName(u"LecturaTypeKDt")

        self.gridLayout.addWidget(self.LecturaTypeKDt, 1, 2, 1, 1)

        self.TemperaturaTypeKDt = QLabel(self.datos)
        self.TemperaturaTypeKDt.setObjectName(u"TemperaturaTypeKDt")

        self.gridLayout.addWidget(self.TemperaturaTypeKDt, 2, 2, 1, 1)

        self.TemperaturaDS18B20Dt = QLabel(self.datos)
        self.TemperaturaDS18B20Dt.setObjectName(u"TemperaturaDS18B20Dt")

        self.gridLayout.addWidget(self.TemperaturaDS18B20Dt, 2, 3, 1, 1)

        self.TemperaturaLabel = QLabel(self.datos)
        self.TemperaturaLabel.setObjectName(u"TemperaturaLabel")

        self.gridLayout.addWidget(self.TemperaturaLabel, 2, 0, 1, 1)


        self.gridLayout_6.addWidget(self.datos, 3, 1, 1, 2)


        self.gridLayout_2.addWidget(self.frame, 0, 0, 1, 1)


        self.retranslateUi(thermoregulation)

        QMetaObject.connectSlotsByName(thermoregulation)
    # setupUi

    def retranslateUi(self, thermoregulation):
        thermoregulation.setWindowTitle(QCoreApplication.translate("thermoregulation", u"Form", None))
        self.titulo.setText(QCoreApplication.translate("thermoregulation", u"<html><head/><body><p align=\"center\"><span style=\" font-size:22pt; font-weight:700; color:#007bff;\">Monitoreo de Temperatura</span></p></body></html>", None))
        self.grafica.setTitle(QCoreApplication.translate("thermoregulation", u"Gr\u00e1fica", None))
        self.descripcion.setText(QCoreApplication.translate("thermoregulation", u"<html><head/><body><p align=\"center\"><span style=\" font-size:10pt; font-style:italic;\">Monitorea temperatura usando 3 tipos de sensores. Traduce a \u00b0C con calibraci\u00f3n por Regresi\u00f3n Polin\u00f3mica.</span></p></body></html>", None))
        self.Info.setTitle(QCoreApplication.translate("thermoregulation", u"Info", None))
        self.LM35.setText(QCoreApplication.translate("thermoregulation", u"LM35", None))
        self.TermoparTipoK.setText(QCoreApplication.translate("thermoregulation", u"TypeK", None))
        self.DS18B20.setText(QCoreApplication.translate("thermoregulation", u"DS18B20", None))
        self.controles.setTitle(QCoreApplication.translate("thermoregulation", u"Controles", None))
        self.calibrarBt.setText(QCoreApplication.translate("thermoregulation", u"No Calibrado", None))
        self.exportarBt.setText(QCoreApplication.translate("thermoregulation", u"Exportal a Exel", None))
        self.limpiarBt.setText(QCoreApplication.translate("thermoregulation", u"Limpiar Gr\u00e1fica", None))
        self.iniciarBt.setText(QCoreApplication.translate("thermoregulation", u"Iniciar Monitoreo", None))
        self.nota.setText(QCoreApplication.translate("thermoregulation", u"<html><head/><body><p align=\"justify\"><span style=\" font-size:9pt;\">\ud83d\udca1 </span><span style=\" font-size:9pt; font-weight:700;\">Nota:</span><span style=\" font-size:9pt;\"> Aseg\u00farate de conectar los <br/>componentes correctamente antes de <br/>iniciar el monitoreo.</span></p><p align=\"justify\"><span style=\" font-size:9pt;\">Selecciona uno de los tipo de <br/>sensor de temperatura y luego<br/>siga con la experiencia de <br/>monitoreo convencional.</span></p></body></html>", None))
        self.LecturaLm35Dt.setText(QCoreApplication.translate("thermoregulation", u"--", None))
        self.LecturaDS18B20Dt.setText(QCoreApplication.translate("thermoregulation", u"--", None))
        self.datosLabel.setText(QCoreApplication.translate("thermoregulation", u"Datos", None))
        self.Lm35Label.setText(QCoreApplication.translate("thermoregulation", u"LM35", None))
        self.TypeKLabel.setText(QCoreApplication.translate("thermoregulation", u"TypeK", None))
        self.DS18B20Label.setText(QCoreApplication.translate("thermoregulation", u"DS18B20", None))
        self.calibradoLabel.setText(QCoreApplication.translate("thermoregulation", u"TempCalibrada", None))
        self.Lm35DtCalibrado.setText(QCoreApplication.translate("thermoregulation", u"--", None))
        self.TypeKDtCalibrado.setText(QCoreApplication.translate("thermoregulation", u"--", None))
        self.DS18B20DtCalibrado.setText(QCoreApplication.translate("thermoregulation", u"--", None))
        self.LecturaLabel.setText(QCoreApplication.translate("thermoregulation", u"Lectura", None))
        self.TemperaturaLm35Dt.setText(QCoreApplication.translate("thermoregulation", u"--", None))
        self.LecturaTypeKDt.setText(QCoreApplication.translate("thermoregulation", u"--", None))
        self.TemperaturaTypeKDt.setText(QCoreApplication.translate("thermoregulation", u"--", None))
        self.TemperaturaDS18B20Dt.setText(QCoreApplication.translate("thermoregulation", u"--", None))
        self.TemperaturaLabel.setText(QCoreApplication.translate("thermoregulation", u"Tempetarura", None))
    # retranslateUi

