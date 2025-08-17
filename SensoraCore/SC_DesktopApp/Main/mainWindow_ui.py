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
    QHBoxLayout, QLabel, QLineEdit, QMainWindow,
    QPushButton, QScrollArea, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1236, 758)
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
"border: 0px solid #2ecc71;\n"
"background-color: rgb(255, 255, 255);")
        self.PantallaPrincipal.setFrameShape(QFrame.Shape.StyledPanel)
        self.PantallaPrincipal.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_2 = QGridLayout(self.PantallaPrincipal)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.SensorUI = QWidget(self.PantallaPrincipal)
        self.SensorUI.setObjectName(u"SensorUI")
        self.SensorUI.setMinimumSize(QSize(700, 700))
        self.SensorUI.setMaximumSize(QSize(999999, 16777215))
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
        self.label_2 = QLabel(self.Welcome)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_4.addWidget(self.label_2, 3, 1, 1, 1)

        self.label = QLabel(self.Welcome)
        self.label.setObjectName(u"label")

        self.gridLayout_4.addWidget(self.label, 2, 1, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 43, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_4.addItem(self.verticalSpacer, 5, 1, 1, 1)

        self.horizontalSpacer = QSpacerItem(252, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer, 2, 2, 2, 1)

        self.horizontalSpacer_2 = QSpacerItem(253, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_2, 2, 0, 2, 1)

        self.label_3 = QLabel(self.Welcome)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setStyleSheet(u"border-color: rgba(0, 170, 255, 50);\n"
"background-color: rgba(0, 123, 255, 20);")

        self.gridLayout_4.addWidget(self.label_3, 4, 1, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 25, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_4.addItem(self.verticalSpacer_2, 1, 1, 1, 1)


        self.verticalLayout_4.addWidget(self.Welcome)


        self.gridLayout_2.addWidget(self.SensorUI, 0, 3, 1, 1)

        self.line = QFrame(self.PantallaPrincipal)
        self.line.setObjectName(u"line")
        self.line.setStyleSheet(u"background-color: rgb(177, 177, 177);")
        self.line.setFrameShape(QFrame.Shape.VLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_2.addWidget(self.line, 0, 2, 1, 1)

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
        self.ipEdit = QLineEdit(self.IP)
        self.ipEdit.setObjectName(u"ipEdit")
        self.ipEdit.setMinimumSize(QSize(0, 40))
        self.ipEdit.setMaximumSize(QSize(16777215, 50))
        self.ipEdit.setStyleSheet(u"color: rgb(177, 177, 177);\n"
"font-size: 18px;")

        self.gridLayout_3.addWidget(self.ipEdit, 0, 0, 1, 1)

        self.Terminal = QPushButton(self.IP)
        self.Terminal.setObjectName(u"Terminal")
        self.Terminal.setMinimumSize(QSize(27, 20))
        self.Terminal.setMaximumSize(QSize(16777215, 16777215))
        self.Terminal.setSizeIncrement(QSize(0, 0))
        self.Terminal.setStyleSheet(u"#Terminal{\n"
"background-color: rgb(0, 0, 0);\n"
"border-color:none;\n"
"}\n"
"\n"
"#Terminal:hover {\n"
"	color:rgb(255, 255, 255);\n"
"	background-color: rgb(0, 123, 255);\n"
"}\n"
"#Terminal:hover:pressed {\n"
"	color:rrgb(255, 0, 0);\n"
"background-color: rgb(0, 255, 127);\n"
"}")

        self.gridLayout_3.addWidget(self.Terminal, 0, 1, 1, 1)


        self.verticalLayout.addWidget(self.IP)

        self.Conectar = QPushButton(self.Conf)
        self.Conectar.setObjectName(u"Conectar")
        self.Conectar.setMinimumSize(QSize(0, 50))
        self.Conectar.setMaximumSize(QSize(16777215, 50))
        self.Conectar.setStyleSheet(u"#Conectar {\n"
"	background-color: rgba(0, 255, 0, 20);\n"
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
"	background-color: rgb(0, 255, 127);\n"
"}\n"
"#Conectar:disabled{\n"
"	background-color: rgb(186, 186, 186);\n"
"}\n"
"")

        self.verticalLayout.addWidget(self.Conectar)

        self.widget = QWidget(self.Conf)
        self.widget.setObjectName(u"widget")
        self.widget.setMinimumSize(QSize(0, 67))
        self.widget.setStyleSheet(u"")
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setSpacing(1)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(1, 1, 1, 1)
        self.Status = QLabel(self.widget)
        self.Status.setObjectName(u"Status")
        self.Status.setMinimumSize(QSize(0, 50))
        self.Status.setMaximumSize(QSize(250, 55))
        self.Status.setStyleSheet(u"color: rgb(134, 15, 17);\n"
"background-color: rgb(255, 210, 211);")

        self.horizontalLayout.addWidget(self.Status)

        self.resetBT = QPushButton(self.widget)
        self.resetBT.setObjectName(u"resetBT")
        self.resetBT.setEnabled(True)
        self.resetBT.setMaximumSize(QSize(55, 55))
        self.resetBT.setCursor(QCursor(Qt.CursorShape.CrossCursor))
#if QT_CONFIG(tooltip)
        self.resetBT.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.resetBT.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.resetBT.setStyleSheet(u"background-color: rgba(255, 255, 255, 0);\n"
"font-size:40px;\n"
"text-align: center;\n"
"")
        self.resetBT.setCheckable(False)
        self.resetBT.setAutoDefault(False)

        self.horizontalLayout.addWidget(self.resetBT)


        self.verticalLayout.addWidget(self.widget)


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
        self.gridLayout_5 = QGridLayout(self.list)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(2, -1, 2, -1)
        self.scrollArea = QScrollArea(self.list)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 312, 804))
        self.verticalLayout_2 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.simpleAngle = QWidget(self.scrollAreaWidgetContents)
        self.simpleAngle.setObjectName(u"simpleAngle")
        self.simpleAngle.setMinimumSize(QSize(0, 60))
        self.simpleAngle.setMaximumSize(QSize(290, 60))
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
        self.verticalLayout_15 = QVBoxLayout(self.simpleAngle)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.simpleAngleBT = QPushButton(self.simpleAngle)
        self.simpleAngleBT.setObjectName(u"simpleAngleBT")
        self.simpleAngleBT.setMinimumSize(QSize(105, 25))
        self.simpleAngleBT.setMaximumSize(QSize(999, 999))
        self.simpleAngleBT.setStyleSheet(u"text-align: left;\n"
"padding-left: 10px;")

        self.verticalLayout_15.addWidget(self.simpleAngleBT)

        self.simpleAngletext = QLabel(self.simpleAngle)
        self.simpleAngletext.setObjectName(u"simpleAngletext")
        self.simpleAngletext.setMaximumSize(QSize(16777215, 20))

        self.verticalLayout_15.addWidget(self.simpleAngletext)


        self.verticalLayout_2.addWidget(self.simpleAngle)

        self.angleArm = QWidget(self.scrollAreaWidgetContents)
        self.angleArm.setObjectName(u"angleArm")
        self.angleArm.setMinimumSize(QSize(0, 60))
        self.angleArm.setMaximumSize(QSize(290, 60))
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
        self.angleArmBT = QPushButton(self.angleArm)
        self.angleArmBT.setObjectName(u"angleArmBT")
        self.angleArmBT.setMinimumSize(QSize(105, 25))
        self.angleArmBT.setMaximumSize(QSize(999, 999))
        self.angleArmBT.setStyleSheet(u"text-align: left;\n"
"padding-left: 10px;")

        self.verticalLayout_6.addWidget(self.angleArmBT)

        self.angleArmtext = QLabel(self.angleArm)
        self.angleArmtext.setObjectName(u"angleArmtext")
        self.angleArmtext.setMaximumSize(QSize(16777215, 20))

        self.verticalLayout_6.addWidget(self.angleArmtext)


        self.verticalLayout_2.addWidget(self.angleArm)

        self.infrared = QWidget(self.scrollAreaWidgetContents)
        self.infrared.setObjectName(u"infrared")
        self.infrared.setMinimumSize(QSize(0, 60))
        self.infrared.setMaximumSize(QSize(290, 60))
        self.infrared.setStyleSheet(u"QWidget{\n"
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
        self.verticalLayout_7 = QVBoxLayout(self.infrared)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.infraredBT = QPushButton(self.infrared)
        self.infraredBT.setObjectName(u"infraredBT")
        self.infraredBT.setMinimumSize(QSize(105, 25))
        self.infraredBT.setMaximumSize(QSize(999, 999))
        self.infraredBT.setStyleSheet(u"text-align: left;\n"
"padding-left: 10px;")

        self.verticalLayout_7.addWidget(self.infraredBT)

        self.infraredtext = QLabel(self.infrared)
        self.infraredtext.setObjectName(u"infraredtext")
        self.infraredtext.setMaximumSize(QSize(16777215, 20))

        self.verticalLayout_7.addWidget(self.infraredtext)


        self.verticalLayout_2.addWidget(self.infrared)

        self.capasitive = QWidget(self.scrollAreaWidgetContents)
        self.capasitive.setObjectName(u"capasitive")
        self.capasitive.setMinimumSize(QSize(0, 60))
        self.capasitive.setMaximumSize(QSize(290, 60))
        self.capasitive.setStyleSheet(u"QWidget{\n"
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
        self.verticalLayout_8 = QVBoxLayout(self.capasitive)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.capasitiveBT = QPushButton(self.capasitive)
        self.capasitiveBT.setObjectName(u"capasitiveBT")
        self.capasitiveBT.setMinimumSize(QSize(105, 25))
        self.capasitiveBT.setMaximumSize(QSize(999, 999))
        self.capasitiveBT.setStyleSheet(u"text-align: left;\n"
"padding-left: 10px;")

        self.verticalLayout_8.addWidget(self.capasitiveBT)

        self.capasitivetext = QLabel(self.capasitive)
        self.capasitivetext.setObjectName(u"capasitivetext")
        self.capasitivetext.setMaximumSize(QSize(16777215, 20))

        self.verticalLayout_8.addWidget(self.capasitivetext)


        self.verticalLayout_2.addWidget(self.capasitive)

        self.ultrasonic = QWidget(self.scrollAreaWidgetContents)
        self.ultrasonic.setObjectName(u"ultrasonic")
        self.ultrasonic.setMinimumSize(QSize(0, 60))
        self.ultrasonic.setMaximumSize(QSize(290, 60))
        self.ultrasonic.setStyleSheet(u"QWidget{\n"
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
        self.verticalLayout_9 = QVBoxLayout(self.ultrasonic)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.ultrasonicBT = QPushButton(self.ultrasonic)
        self.ultrasonicBT.setObjectName(u"ultrasonicBT")
        self.ultrasonicBT.setMinimumSize(QSize(105, 25))
        self.ultrasonicBT.setMaximumSize(QSize(999, 999))
        self.ultrasonicBT.setStyleSheet(u"text-align: left;\n"
"padding-left: 10px;")

        self.verticalLayout_9.addWidget(self.ultrasonicBT)

        self.ultrasonictext = QLabel(self.ultrasonic)
        self.ultrasonictext.setObjectName(u"ultrasonictext")
        self.ultrasonictext.setMaximumSize(QSize(16777215, 20))

        self.verticalLayout_9.addWidget(self.ultrasonictext)


        self.verticalLayout_2.addWidget(self.ultrasonic)

        self.OpticalSpeed = QWidget(self.scrollAreaWidgetContents)
        self.OpticalSpeed.setObjectName(u"OpticalSpeed")
        self.OpticalSpeed.setMinimumSize(QSize(0, 60))
        self.OpticalSpeed.setMaximumSize(QSize(290, 60))
        self.OpticalSpeed.setStyleSheet(u"QWidget{\n"
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
        self.verticalLayout_10 = QVBoxLayout(self.OpticalSpeed)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.OpticalSpeedBT = QPushButton(self.OpticalSpeed)
        self.OpticalSpeedBT.setObjectName(u"OpticalSpeedBT")
        self.OpticalSpeedBT.setMinimumSize(QSize(105, 25))
        self.OpticalSpeedBT.setMaximumSize(QSize(999, 999))
        self.OpticalSpeedBT.setStyleSheet(u"text-align: left;\n"
"padding-left: 10px;")

        self.verticalLayout_10.addWidget(self.OpticalSpeedBT)

        self.OpticalSpeedtext = QLabel(self.OpticalSpeed)
        self.OpticalSpeedtext.setObjectName(u"OpticalSpeedtext")
        self.OpticalSpeedtext.setMaximumSize(QSize(16777215, 20))

        self.verticalLayout_10.addWidget(self.OpticalSpeedtext)


        self.verticalLayout_2.addWidget(self.OpticalSpeed)

        self.irSteering = QWidget(self.scrollAreaWidgetContents)
        self.irSteering.setObjectName(u"irSteering")
        self.irSteering.setMinimumSize(QSize(0, 60))
        self.irSteering.setMaximumSize(QSize(290, 60))
        self.irSteering.setStyleSheet(u"QWidget{\n"
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
        self.verticalLayout_5 = QVBoxLayout(self.irSteering)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.irSteeringBT = QPushButton(self.irSteering)
        self.irSteeringBT.setObjectName(u"irSteeringBT")
        self.irSteeringBT.setMinimumSize(QSize(105, 25))
        self.irSteeringBT.setMaximumSize(QSize(999, 999))
        self.irSteeringBT.setStyleSheet(u"text-align: left;\n"
"padding-left: 10px;")

        self.verticalLayout_5.addWidget(self.irSteeringBT)

        self.irSteeringtext = QLabel(self.irSteering)
        self.irSteeringtext.setObjectName(u"irSteeringtext")
        self.irSteeringtext.setMaximumSize(QSize(16777215, 20))

        self.verticalLayout_5.addWidget(self.irSteeringtext)


        self.verticalLayout_2.addWidget(self.irSteering)

        self.thermoregulation = QWidget(self.scrollAreaWidgetContents)
        self.thermoregulation.setObjectName(u"thermoregulation")
        self.thermoregulation.setMinimumSize(QSize(0, 60))
        self.thermoregulation.setMaximumSize(QSize(290, 60))
        self.thermoregulation.setStyleSheet(u"QWidget{\n"
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
        self.verticalLayout_16 = QVBoxLayout(self.thermoregulation)
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.thermoregulationBT = QPushButton(self.thermoregulation)
        self.thermoregulationBT.setObjectName(u"thermoregulationBT")
        self.thermoregulationBT.setMinimumSize(QSize(105, 25))
        self.thermoregulationBT.setMaximumSize(QSize(999, 999))
        self.thermoregulationBT.setStyleSheet(u"text-align: left;\n"
"padding-left: 10px;")

        self.verticalLayout_16.addWidget(self.thermoregulationBT)

        self.thermoregulationtext = QLabel(self.thermoregulation)
        self.thermoregulationtext.setObjectName(u"thermoregulationtext")
        self.thermoregulationtext.setMaximumSize(QSize(16777215, 20))

        self.verticalLayout_16.addWidget(self.thermoregulationtext)


        self.verticalLayout_2.addWidget(self.thermoregulation)

        self.gasRegulation = QWidget(self.scrollAreaWidgetContents)
        self.gasRegulation.setObjectName(u"gasRegulation")
        self.gasRegulation.setMinimumSize(QSize(0, 60))
        self.gasRegulation.setMaximumSize(QSize(290, 60))
        self.gasRegulation.setStyleSheet(u"QWidget{\n"
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
        self.verticalLayout_14 = QVBoxLayout(self.gasRegulation)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.gasRegulationBT = QPushButton(self.gasRegulation)
        self.gasRegulationBT.setObjectName(u"gasRegulationBT")
        self.gasRegulationBT.setMinimumSize(QSize(105, 25))
        self.gasRegulationBT.setMaximumSize(QSize(999, 999))
        self.gasRegulationBT.setStyleSheet(u"text-align: left;\n"
"padding-left: 10px;")

        self.verticalLayout_14.addWidget(self.gasRegulationBT)

        self.gasRegulationtext = QLabel(self.gasRegulation)
        self.gasRegulationtext.setObjectName(u"gasRegulationtext")
        self.gasRegulationtext.setMaximumSize(QSize(16777215, 20))

        self.verticalLayout_14.addWidget(self.gasRegulationtext)


        self.verticalLayout_2.addWidget(self.gasRegulation)

        self.brightness = QWidget(self.scrollAreaWidgetContents)
        self.brightness.setObjectName(u"brightness")
        self.brightness.setMinimumSize(QSize(0, 60))
        self.brightness.setMaximumSize(QSize(290, 60))
        self.brightness.setStyleSheet(u"QWidget{\n"
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
        self.verticalLayout_13 = QVBoxLayout(self.brightness)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.brightnessBT = QPushButton(self.brightness)
        self.brightnessBT.setObjectName(u"brightnessBT")
        self.brightnessBT.setMinimumSize(QSize(105, 25))
        self.brightnessBT.setMaximumSize(QSize(999, 999))
        self.brightnessBT.setStyleSheet(u"text-align: left;\n"
"padding-left: 10px;")

        self.verticalLayout_13.addWidget(self.brightnessBT)

        self.brightnesstext = QLabel(self.brightness)
        self.brightnesstext.setObjectName(u"brightnesstext")
        self.brightnesstext.setMaximumSize(QSize(16777215, 20))

        self.verticalLayout_13.addWidget(self.brightnesstext)


        self.verticalLayout_2.addWidget(self.brightness)

        self.colorCNY = QWidget(self.scrollAreaWidgetContents)
        self.colorCNY.setObjectName(u"colorCNY")
        self.colorCNY.setMinimumSize(QSize(0, 60))
        self.colorCNY.setMaximumSize(QSize(290, 60))
        self.colorCNY.setStyleSheet(u"QWidget{\n"
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
        self.verticalLayout_12 = QVBoxLayout(self.colorCNY)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.colorCNYBT = QPushButton(self.colorCNY)
        self.colorCNYBT.setObjectName(u"colorCNYBT")
        self.colorCNYBT.setMinimumSize(QSize(105, 25))
        self.colorCNYBT.setMaximumSize(QSize(999, 999))
        self.colorCNYBT.setStyleSheet(u"text-align: left;\n"
"padding-left: 10px;")

        self.verticalLayout_12.addWidget(self.colorCNYBT)

        self.colorCNYtext = QLabel(self.colorCNY)
        self.colorCNYtext.setObjectName(u"colorCNYtext")
        self.colorCNYtext.setMaximumSize(QSize(16777215, 20))

        self.verticalLayout_12.addWidget(self.colorCNYtext)


        self.verticalLayout_2.addWidget(self.colorCNY)

        self.colorTCS = QWidget(self.scrollAreaWidgetContents)
        self.colorTCS.setObjectName(u"colorTCS")
        self.colorTCS.setMinimumSize(QSize(0, 60))
        self.colorTCS.setMaximumSize(QSize(290, 60))
        self.colorTCS.setStyleSheet(u"QWidget{\n"
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
        self.verticalLayout_11 = QVBoxLayout(self.colorTCS)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.colorTCSBT = QPushButton(self.colorTCS)
        self.colorTCSBT.setObjectName(u"colorTCSBT")
        self.colorTCSBT.setMinimumSize(QSize(105, 25))
        self.colorTCSBT.setMaximumSize(QSize(999, 999))
        self.colorTCSBT.setStyleSheet(u"text-align: left;\n"
"padding-left: 10px;")

        self.verticalLayout_11.addWidget(self.colorTCSBT)

        self.colorTCStext = QLabel(self.colorTCS)
        self.colorTCStext.setObjectName(u"colorTCStext")
        self.colorTCStext.setMaximumSize(QSize(16777215, 20))

        self.verticalLayout_11.addWidget(self.colorTCStext)


        self.verticalLayout_2.addWidget(self.colorTCS)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.gridLayout_5.addWidget(self.scrollArea, 0, 1, 1, 1)


        self.verticalLayout_3.addWidget(self.list)


        self.gridLayout_2.addWidget(self.Mlateral, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.PantallaPrincipal, 0, 1, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-size:11pt; color:#b1b1b1;\">Conecta tu ESP32 y selecciona un sensor</span></p><p align=\"center\"><span style=\" font-size:11pt; color:#b1b1b1;\">para comenzar a monitorear datos</span></p></body></html>", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-size:72pt;\">\ud83d\udd27</span></p></body></html>", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-size:11pt; color:#666666;\">\ud83d\uddd2\ufe0fUna vez conectado encontrar\u00e1s el diagrama</span></p><p align=\"center\"><span style=\" font-size:11pt; color:#666666;\">de conecxiones ESP32 en cada sensor y los controles de monitoreo</span></p></body></html>", None))
        self.Titulo.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-size:24pt; font-weight:700; color:#007bff;\">SensoraCore</span></p><p align=\"center\"><span style=\" font-size:12pt; color:#969696;\">Sistema de Monitoreo de Sensores WiFi</span></p></body></html>", None))
        self.Conf.setTitle(QCoreApplication.translate("MainWindow", u"Configuraci\u00f3n de Conexi\u00f3n", None))
        self.IP.setTitle(QCoreApplication.translate("MainWindow", u"IP del ESP32:", None))
        self.ipEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Ejemplo: 192.168.1.100", None))
        self.Terminal.setText(QCoreApplication.translate("MainWindow", u"_", None))
        self.Conectar.setText(QCoreApplication.translate("MainWindow", u"\ud83d\udd0c Conectar a ESP32", None))
        self.Status.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-size:14pt;\">\ud83d\udd34</span><span style=\" font-size:14pt; font-weight:700;\">Desconectado</span></p></body></html>", None))
        self.resetBT.setText(QCoreApplication.translate("MainWindow", u"\ud83d\udd3b", None))
        self.list.setTitle(QCoreApplication.translate("MainWindow", u"Sensores Disponibles", None))
        self.simpleAngleBT.setText(QCoreApplication.translate("MainWindow", u"SIMPLE ALGLE", None))
        self.simpleAngletext.setText(QCoreApplication.translate("MainWindow", u" Potenciometro como sensor de angulo", None))
        self.angleArmBT.setText(QCoreApplication.translate("MainWindow", u"ANGLE ARM", None))
        self.angleArmtext.setText(QCoreApplication.translate("MainWindow", u"Potenciometros como simulacion de Brazo", None))
        self.infraredBT.setText(QCoreApplication.translate("MainWindow", u"INFRARED", None))
        self.infraredtext.setText(QCoreApplication.translate("MainWindow", u"Sensor de proximidad con Infrarojos", None))
        self.capasitiveBT.setText(QCoreApplication.translate("MainWindow", u"CAPASITIVE", None))
        self.capasitivetext.setText(QCoreApplication.translate("MainWindow", u"Sensor de proximidad con sensor Capasitivo", None))
        self.ultrasonicBT.setText(QCoreApplication.translate("MainWindow", u"ULTRASONIC", None))
        self.ultrasonictext.setText(QCoreApplication.translate("MainWindow", u"Sensor de distancia con Ultrasonidos", None))
        self.OpticalSpeedBT.setText(QCoreApplication.translate("MainWindow", u"OPTICAL SPEED", None))
        self.OpticalSpeedtext.setText(QCoreApplication.translate("MainWindow", u"Control y monitoreo de Velocidad", None))
        self.irSteeringBT.setText(QCoreApplication.translate("MainWindow", u"IR STEERING", None))
        self.irSteeringtext.setText(QCoreApplication.translate("MainWindow", u"Direccion de seg\u00fan infrarojos", None))
        self.thermoregulationBT.setText(QCoreApplication.translate("MainWindow", u"THERMOREGULATION", None))
        self.thermoregulationtext.setText(QCoreApplication.translate("MainWindow", u"Control y monitoreo de temperatura", None))
        self.gasRegulationBT.setText(QCoreApplication.translate("MainWindow", u"GAS REGULATION", None))
        self.gasRegulationtext.setText(QCoreApplication.translate("MainWindow", u"Control de flujo de aire y densidad de gases", None))
        self.brightnessBT.setText(QCoreApplication.translate("MainWindow", u"BRIGHTNESS", None))
        self.brightnesstext.setText(QCoreApplication.translate("MainWindow", u"Sensor de brillo", None))
        self.colorCNYBT.setText(QCoreApplication.translate("MainWindow", u"COLOR CNY", None))
        self.colorCNYtext.setText(QCoreApplication.translate("MainWindow", u"Color seg\u00fan infrarojos", None))
        self.colorTCSBT.setText(QCoreApplication.translate("MainWindow", u"COLOR TCS", None))
        self.colorTCStext.setText(QCoreApplication.translate("MainWindow", u"Color seg\u00fan TCS3200", None))
    # retranslateUi

