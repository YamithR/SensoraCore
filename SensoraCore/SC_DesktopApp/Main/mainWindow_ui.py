# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainWindow.ui'
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
    QLabel, QLineEdit, QMainWindow, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1127, 762)
        MainWindow.setStyleSheet(u"background-color: rgb(216, 216, 216);")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(20, 20, 20, 20)
        self.PantallaPrincipal = QFrame(self.centralwidget)
        self.PantallaPrincipal.setObjectName(u"PantallaPrincipal")
        self.PantallaPrincipal.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        self.PantallaPrincipal.setStyleSheet(u"border-radius: 10px;\n"
"border-color: rgb(255, 0, 0);\n"
"border-width: 1px;\n"
"border: 2px solid #2ecc71;\n"
"background-color: rgb(255, 255, 255);")
        self.PantallaPrincipal.setFrameShape(QFrame.Shape.StyledPanel)
        self.PantallaPrincipal.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_2 = QGridLayout(self.PantallaPrincipal)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.Mlateral = QWidget(self.PantallaPrincipal)
        self.Mlateral.setObjectName(u"Mlateral")
        self.Mlateral.setMinimumSize(QSize(350, 700))
        self.Mlateral.setMaximumSize(QSize(350, 9999))
        self.verticalLayout_3 = QVBoxLayout(self.Mlateral)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.Titulo = QLabel(self.Mlateral)
        self.Titulo.setObjectName(u"Titulo")

        self.verticalLayout_3.addWidget(self.Titulo)

        self.Conf = QGroupBox(self.Mlateral)
        self.Conf.setObjectName(u"Conf")
        self.Conf.setMaximumSize(QSize(16777215, 250))
        self.Conf.setStyleSheet(u"#Conf {\n"
"    color: rgb(102, 102, 102) ;\n"
"    border: 2px solid rgb(177, 177, 177) ;\n"
"    border-radius: 5px;\n"
"    margin-top: 15px; /* espacio para el t\u00edtulo */\n"
"    font: bold 14px;\n"
"}\n"
"#Conf::title {\n"
"    subcontrol-origin: margin;\n"
"    subcontrol-position: top left ;\n"
"    left: 20px;\n"
"    background-color: rgba(255, 255, 255, 255);\n"
"	padding: 2px;\n"
"\n"
"    border-radius: 5px;\n"
"}")
        self.verticalLayout = QVBoxLayout(self.Conf)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(6, 22, 6, 5)
        self.IP = QGroupBox(self.Conf)
        self.IP.setObjectName(u"IP")
        self.IP.setMaximumSize(QSize(16777215, 75))
        self.IP.setStyleSheet(u"\n"
"#IP {\n"
"    color: rgb(102, 102, 102) ;\n"
"    border: 2px solid rgb(177, 177, 177) ;\n"
"    border-radius: 5px;\n"
"    margin-top: 15px; /* espacio para el t\u00edtulo */\n"
"    font: bold 14px;\n"
"	margin-top:20px;\n"
"	font-size: 13px;\n"
"}\n"
"#IP::title {\n"
"	margin-top:8px;\n"
"    subcontrol-origin: margin;\n"
"    subcontrol-position: top left ;\n"
"	bottom:10px;\n"
"    background-color: rgba(255, 255, 255, 255);\n"
"    border-radius: 5px;\n"
"}")
        self.gridLayout_3 = QGridLayout(self.IP)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setVerticalSpacing(6)
        self.lineEdit = QLineEdit(self.IP)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setMinimumSize(QSize(0, 40))
        self.lineEdit.setMaximumSize(QSize(16777215, 50))
        self.lineEdit.setStyleSheet(u"color: rgb(177, 177, 177);\n"
"font-size: 18px;")

        self.gridLayout_3.addWidget(self.lineEdit, 0, 0, 1, 1)


        self.verticalLayout.addWidget(self.IP)

        self.Conectar = QPushButton(self.Conf)
        self.Conectar.setObjectName(u"Conectar")
        self.Conectar.setMinimumSize(QSize(0, 50))
        self.Conectar.setMaximumSize(QSize(16777215, 50))
        self.Conectar.setStyleSheet(u"#Conectar {\n"
"	background-color: rgb(186, 186, 186);\n"
"	font-size: 18px;\n"
"	color: rgb(0, 0, 0);\n"
"	font-weight: bold;\n"
"}\n"
"#Conectar:hover {\n"
"	color:rgb(255, 255, 255);\n"
"	background-color: rgb(0, 123, 255);\n"
"}\n"
"#Conectar:hover:pressed {\n"
"	color:rrgb(255, 0, 0);\n"
"	background-color: rgb(0, 255, 127)\n"
"}\n"
"")

        self.verticalLayout.addWidget(self.Conectar)

        self.Status = QLabel(self.Conf)
        self.Status.setObjectName(u"Status")
        self.Status.setMinimumSize(QSize(0, 50))
        self.Status.setMaximumSize(QSize(16777215, 50))
        self.Status.setStyleSheet(u"color: rgb(134, 15, 17);\n"
"background-color: rgb(255, 210, 211);")

        self.verticalLayout.addWidget(self.Status)


        self.verticalLayout_3.addWidget(self.Conf)

        self.list = QGroupBox(self.Mlateral)
        self.list.setObjectName(u"list")
        self.list.setMinimumSize(QSize(0, 300))
        self.list.setMaximumSize(QSize(16777215, 90000))
        self.list.setStyleSheet(u"#list {\n"
"    color: rgb(102, 102, 102) ;\n"
"    border: 2px solid rgb(177, 177, 177) ;\n"
"    border-radius: 5px;\n"
"    margin-top: 15px; /* espacio para el t\u00edtulo */\n"
"    font: bold 14px;\n"
"}\n"
"#list::title {\n"
"    subcontrol-origin: margin;\n"
"    subcontrol-position: top left ;\n"
"    left: 20px;\n"
"    background-color: rgba(255, 255, 255, 255);\n"
"	padding: 2px;\n"
"\n"
"    border-radius: 5px;\n"
"}")
        self.verticalLayout_2 = QVBoxLayout(self.list)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.simpleAngle = QWidget(self.list)
        self.simpleAngle.setObjectName(u"simpleAngle")
        self.simpleAngle.setMinimumSize(QSize(0, 20))
        self.simpleAngle.setMaximumSize(QSize(16777215, 60))
        self.simpleAngle.setStyleSheet(u"QWidget{\n"
"color: rgb(0, 0, 0);\n"
"	border-top-color: rgb(222, 222, 222);\n"
"	border-bottom-color: rgb(222, 222, 222);\n"
"  \n"
"	border-left: none;\n"
"	border-right: none;\n"
"\n"
"	border-radius:0px\n"
"}\n"
"QLabel{\n"
"border:none;\n"
"background-color: rgba(0, 0, 0, 0);\n"
"\n"
"}\n"
"QLabel:hover{\n"
"border:none;\n"
"background-color: rgba(0, 0, 0, 0);\n"
"}\n"
"QPushButton{\n"
"border:none;\n"
"background-color: rgba(0, 0, 0, 0);\n"
"}\n"
"QPushButton:hover{\n"
"border:none;\n"
"background-color: rgba(0, 0, 0, 0);\n"
"}\n"
"QPushButton:hover:pressed{\n"
"border:none;\n"
"background-color: rgba(255, 255, 127, 20);\n"
"}\n"
"QWidget:hover{\n"
"	background-color: rgba(0, 123, 255, 20);\n"
"}")
        self.verticalLayout_5 = QVBoxLayout(self.simpleAngle)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.simpleAngleBT = QPushButton(self.simpleAngle)
        self.simpleAngleBT.setObjectName(u"simpleAngleBT")
        self.simpleAngleBT.setMinimumSize(QSize(105, 25))
        self.simpleAngleBT.setMaximumSize(QSize(999, 999))
        self.simpleAngleBT.setStyleSheet(u"text-align: left;\n"
"padding-left: 10px;")

        self.verticalLayout_5.addWidget(self.simpleAngleBT)

        self.text = QLabel(self.simpleAngle)
        self.text.setObjectName(u"text")
        self.text.setMaximumSize(QSize(16777215, 20))

        self.verticalLayout_5.addWidget(self.text)


        self.verticalLayout_2.addWidget(self.simpleAngle)

        self.angleArm = QWidget(self.list)
        self.angleArm.setObjectName(u"angleArm")
        self.angleArm.setMinimumSize(QSize(0, 20))
        self.angleArm.setMaximumSize(QSize(16777215, 60))
        self.angleArm.setStyleSheet(u"QWidget{\n"
"color: rgb(0, 0, 0);\n"
"	border-top-color: rgb(222, 222, 222);\n"
"	border-bottom-color: rgb(222, 222, 222);\n"
"  \n"
"	border-left: none;\n"
"	border-right: none;\n"
"\n"
"	border-radius:0px\n"
"}\n"
"QLabel{\n"
"border:none;\n"
"background-color: rgba(0, 0, 0, 0);\n"
"\n"
"}\n"
"QLabel:hover{\n"
"border:none;\n"
"background-color: rgba(0, 0, 0, 0);\n"
"}\n"
"QPushButton{\n"
"border:none;\n"
"background-color: rgba(0, 0, 0, 0);\n"
"}\n"
"QPushButton:hover{\n"
"border:none;\n"
"background-color: rgba(0, 0, 0, 0);\n"
"}\n"
"QPushButton:hover:pressed{\n"
"border:none;\n"
"background-color: rgba(255, 255, 127, 20);\n"
"}\n"
"QWidget:hover{\n"
"	background-color: rgba(0, 123, 255, 20);\n"
"}")
        self.verticalLayout_6 = QVBoxLayout(self.angleArm)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.angleArmTB = QPushButton(self.angleArm)
        self.angleArmTB.setObjectName(u"angleArmTB")
        self.angleArmTB.setMinimumSize(QSize(105, 25))
        self.angleArmTB.setMaximumSize(QSize(999, 999))
        self.angleArmTB.setStyleSheet(u"text-align: left;\n"
"padding-left: 10px;")

        self.verticalLayout_6.addWidget(self.angleArmTB)

        self.text_2 = QLabel(self.angleArm)
        self.text_2.setObjectName(u"text_2")
        self.text_2.setMaximumSize(QSize(16777215, 20))

        self.verticalLayout_6.addWidget(self.text_2)


        self.verticalLayout_2.addWidget(self.angleArm)


        self.verticalLayout_3.addWidget(self.list)


        self.gridLayout_2.addWidget(self.Mlateral, 0, 1, 1, 1)

        self.SensorUI = QWidget(self.PantallaPrincipal)
        self.SensorUI.setObjectName(u"SensorUI")
        self.SensorUI.setMinimumSize(QSize(700, 700))
        self.SensorUI.setMaximumSize(QSize(900, 16777215))
        self.SensorUI.setStyleSheet(u"QGroupBox {\n"
"    color: rgb(102, 102, 102) ;\n"
"    border: 2px solid rgb(177, 177, 177) ;\n"
"    border-radius: 5px;\n"
"    margin-top: 15px; /* espacio para el t\u00edtulo */\n"
"    font: bold 14px;\n"
"}\n"
"QGroupBox::title {\n"
"    subcontrol-origin: margin;\n"
"    subcontrol-position: top left ;\n"
"    left: 20px;\n"
"    background-color: rgba(255, 255, 255, 255);\n"
"	padding: 2px;\n"
"\n"
"    border-radius: 5px;\n"
"}")
        self.verticalLayout_4 = QVBoxLayout(self.SensorUI)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.Welcome = QWidget(self.SensorUI)
        self.Welcome.setObjectName(u"Welcome")
        self.gridLayout_4 = QGridLayout(self.Welcome)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.label = QLabel(self.Welcome)
        self.label.setObjectName(u"label")

        self.gridLayout_4.addWidget(self.label, 1, 1, 1, 1)

        self.label_2 = QLabel(self.Welcome)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_4.addWidget(self.label_2, 2, 1, 1, 1)

        self.label_3 = QLabel(self.Welcome)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setStyleSheet(u"border-color: rgba(0, 170, 255, 50);\n"
"background-color: rgba(0, 123, 255, 20);")

        self.gridLayout_4.addWidget(self.label_3, 3, 1, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 43, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_4.addItem(self.verticalSpacer, 4, 1, 1, 1)

        self.horizontalSpacer = QSpacerItem(252, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer, 1, 2, 2, 1)

        self.horizontalSpacer_2 = QSpacerItem(253, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_2, 1, 0, 2, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 25, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_4.addItem(self.verticalSpacer_2, 0, 1, 1, 1)


        self.verticalLayout_4.addWidget(self.Welcome)


        self.gridLayout_2.addWidget(self.SensorUI, 0, 3, 1, 1)

        self.line = QFrame(self.PantallaPrincipal)
        self.line.setObjectName(u"line")
        self.line.setStyleSheet(u"background-color: rgb(177, 177, 177);")
        self.line.setFrameShape(QFrame.Shape.VLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_2.addWidget(self.line, 0, 2, 1, 1)


        self.gridLayout.addWidget(self.PantallaPrincipal, 0, 1, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        QWidget.setTabOrder(self.lineEdit, self.Conectar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.Titulo.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-size:24pt; font-weight:700; color:#007bff;\">SensoraCore</span></p><p align=\"center\"><span style=\" font-size:12pt; color:#969696;\">Sistema de Monitoreo de Sensores WiFi</span></p></body></html>", None))
        self.Conf.setTitle(QCoreApplication.translate("MainWindow", u"Configuraci\u00f3n de Conexi\u00f3n", None))
        self.IP.setTitle(QCoreApplication.translate("MainWindow", u"IP del ESP32:", None))
        self.lineEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Ejemplo: 192.168.1.100", None))
        self.Conectar.setText(QCoreApplication.translate("MainWindow", u"\ud83d\udd0c Conectar a ESP32", None))
        self.Status.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-size:14pt;\">\ud83d\udd34</span><span style=\" font-size:14pt; font-weight:700;\">Desconectado</span></p></body></html>", None))
        self.list.setTitle(QCoreApplication.translate("MainWindow", u"Sensores Disponibles", None))
        self.simpleAngleBT.setText(QCoreApplication.translate("MainWindow", u"\ud83c\udf9b\ufe0fSIMPLE ALGLE", None))
        self.text.setText(QCoreApplication.translate("MainWindow", u" Potenciometro como sensor de angulo", None))
        self.angleArmTB.setText(QCoreApplication.translate("MainWindow", u"\ud83e\uddbeANGLE ARM", None))
        self.text_2.setText(QCoreApplication.translate("MainWindow", u"Multiples Potenciometros como simulacion de Brazo", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-size:72pt;\">\ud83d\udd27</span></p></body></html>", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-size:11pt; color:#b1b1b1;\">Conecta tu ESP32 y selecciona un sensor</span></p><p align=\"center\"><span style=\" font-size:11pt; color:#b1b1b1;\">para comenzar a monitorear datos</span></p></body></html>", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-size:11pt; color:#666666;\">\ud83d\uddd2\ufe0fUna vez conectado encontrar\u00e1s el diagrama</span></p><p align=\"center\"><span style=\" font-size:11pt; color:#666666;\">de conecxiones ESP32 en cada sensor y los controles de monitoreo</span></p></body></html>", None))
    # retranslateUi

