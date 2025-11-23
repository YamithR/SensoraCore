# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'brightness.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
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
    QHBoxLayout, QLCDNumber, QLabel, QProgressBar,
    QPushButton, QSizePolicy, QVBoxLayout, QWidget)

class Ui_brightness(object):
    def setupUi(self, brightness):
        if not brightness.objectName():
            brightness.setObjectName(u"brightness")
        brightness.resize(764, 650)
        brightness.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"border: 1px solid rgb(221, 221, 221);\n"
"border-radius: 5px;\n"
"color: rgb(0, 0, 0);")
        self.gridLayout_2 = QGridLayout(brightness)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.frame = QFrame(brightness)
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

        self.Representacin = QGroupBox(self.frame)
        self.Representacin.setObjectName(u"Representacin")
        self.Representacin.setMinimumSize(QSize(400, 470))
        self.Representacin.setStyleSheet(u"QGroupBox {\n"
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
        self.gridLayout_5 = QGridLayout(self.Representacin)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.RepresentacinWidget = QWidget(self.Representacin)
        self.RepresentacinWidget.setObjectName(u"RepresentacinWidget")
        self.gridLayout_7 = QGridLayout(self.RepresentacinWidget)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.BarraIndicadorDeLuz = QProgressBar(self.RepresentacinWidget)
        self.BarraIndicadorDeLuz.setObjectName(u"BarraIndicadorDeLuz")
        self.BarraIndicadorDeLuz.setValue(24)

        self.gridLayout_7.addWidget(self.BarraIndicadorDeLuz, 1, 0, 1, 1)

        self.PorcentajeDeLuz = QLCDNumber(self.RepresentacinWidget)
        self.PorcentajeDeLuz.setObjectName(u"PorcentajeDeLuz")

        self.gridLayout_7.addWidget(self.PorcentajeDeLuz, 0, 0, 1, 1)


        self.gridLayout_5.addWidget(self.RepresentacinWidget, 1, 0, 1, 1)


        self.gridLayout_6.addWidget(self.Representacin, 2, 1, 1, 2)

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
        self.controles = QGroupBox(self.Info)
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
        self.gridLayout_4 = QGridLayout(self.controles)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.botones = QWidget(self.controles)
        self.botones.setObjectName(u"botones")
        self.botones.setMaximumSize(QSize(16777215, 70))
        self.horizontalLayout = QHBoxLayout(self.botones)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
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

        self.horizontalLayout.addWidget(self.calibrarBt)

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

        self.horizontalLayout.addWidget(self.iniciarBt)


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
        self.LecturaLDRDt = QLabel(self.datos)
        self.LecturaLDRDt.setObjectName(u"LecturaLDRDt")

        self.gridLayout.addWidget(self.LecturaLDRDt, 1, 1, 1, 1)

        self.LDRLabel = QLabel(self.datos)
        self.LDRLabel.setObjectName(u"LDRLabel")

        self.gridLayout.addWidget(self.LDRLabel, 0, 1, 1, 1)

        self.LecturaLabel = QLabel(self.datos)
        self.LecturaLabel.setObjectName(u"LecturaLabel")

        self.gridLayout.addWidget(self.LecturaLabel, 1, 0, 1, 1)

        self.datosLabel = QLabel(self.datos)
        self.datosLabel.setObjectName(u"datosLabel")

        self.gridLayout.addWidget(self.datosLabel, 0, 0, 1, 1)


        self.gridLayout_6.addWidget(self.datos, 3, 1, 1, 2)


        self.gridLayout_2.addWidget(self.frame, 0, 0, 1, 1)


        self.retranslateUi(brightness)

        QMetaObject.connectSlotsByName(brightness)
    # setupUi

    def retranslateUi(self, brightness):
        brightness.setWindowTitle(QCoreApplication.translate("brightness", u"Form", None))
        self.titulo.setText(QCoreApplication.translate("brightness", u"<html><head/><body><p align=\"center\"><span style=\" font-size:22pt; font-weight:700; color:#007bff;\">Monitoreo de Brillo</span></p></body></html>", None))
        self.Representacin.setTitle(QCoreApplication.translate("brightness", u"Representaci\u00f3n", None))
        self.descripcion.setText(QCoreApplication.translate("brightness", u"<html><head/><body><p align=\"center\"><span style=\" font-size:10pt; font-style:italic;\">Monitorea lectura anal\u00f3gica del sensor de fotorresistencia para su caracterizaci\u00f3n.</span></p></body></html>", None))
        self.Info.setTitle(QCoreApplication.translate("brightness", u"Info", None))
        self.controles.setTitle(QCoreApplication.translate("brightness", u"Controles", None))
        self.calibrarBt.setText(QCoreApplication.translate("brightness", u"No Calibrado", None))
        self.iniciarBt.setText(QCoreApplication.translate("brightness", u"Iniciar Monitoreo", None))
        self.nota.setText(QCoreApplication.translate("brightness", u"<html><head/><body><p align=\"justify\"><span style=\" font-size:9pt;\">\U0001f4a1 </span><span style=\" font-size:9pt; font-weight:700;\">Nota:</span><span style=\" font-size:9pt;\"> Aseg\U000000farate de conectar los <br/>componentes correctamente antes de <br/>iniciar el monitoreo.</span></p><p align=\"justify\"><span style=\" font-size:9pt;\">Selecciona uno de los tipo de <br/>sensor de Gases y luego<br/>siga con la experiencia de <br/>monitoreo convencional.</span></p></body></html>", None))
        self.LecturaLDRDt.setText(QCoreApplication.translate("brightness", u"--", None))
        self.LDRLabel.setText(QCoreApplication.translate("brightness", u"LDR", None))
        self.LecturaLabel.setText(QCoreApplication.translate("brightness", u"Lectura", None))
        self.datosLabel.setText(QCoreApplication.translate("brightness", u"Datos", None))
    # retranslateUi

