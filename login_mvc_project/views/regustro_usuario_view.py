# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'regitro_usuario.ui'
##
## Created by: Qt User Interface Compiler version 6.11.0
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QGridLayout,
    QHBoxLayout, QLabel, QMainWindow, QPushButton,
    QSizePolicy, QSpacerItem, QTextEdit, QToolButton,
    QVBoxLayout, QWidget)

class RegistroUsuarioWindow(object):
    def setupUi(self, RegistroUsuarioWindow):
        if not RegistroUsuarioWindow.objectName():
            RegistroUsuarioWindow.setObjectName(u"RegistroUsuarioWindow")
        RegistroUsuarioWindow.resize(680, 694)
        RegistroUsuarioWindow.setStyleSheet(u"background-color: #EAF4FF;")
        self.centralwidget = QWidget(RegistroUsuarioWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_2 = QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setStyleSheet(u"QFrame#frame {\n"
"    background-color: #D9ECFF;\n"
"    border: 1px solid #7BB7F0;\n"
"    border-radius: 12px;\n"
"}")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_8 = QVBoxLayout(self.frame)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.Rumsa = QLabel(self.frame)
        self.Rumsa.setObjectName(u"Rumsa")
        palette = QPalette()
        brush = QBrush(QColor(240, 181, 29, 255))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText, brush)
        brush1 = QBrush(QColor(215, 236, 255, 255))
        brush1.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Button, brush1)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Text, brush)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.ButtonText, brush)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Base, brush1)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Window, brush1)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.WindowText, brush)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Button, brush1)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Text, brush)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.ButtonText, brush)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Base, brush1)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Window, brush1)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, brush)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Button, brush1)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, brush)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, brush)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Base, brush1)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Window, brush1)
        self.Rumsa.setPalette(palette)
        font = QFont()
        font.setFamilies([u"Arial"])
        font.setPointSize(24)
        font.setBold(True)
        self.Rumsa.setFont(font)
        self.Rumsa.setStyleSheet(u"background-color: #D7ECFF;\n"
"color: #f0b51d;\n"
"font-weight: bold;")
        self.Rumsa.setAlignment(Qt.AlignCenter)

        self.verticalLayout_8.addWidget(self.Rumsa)

        self.labelCompany = QLabel(self.frame)
        self.labelCompany.setObjectName(u"labelCompany")
        font1 = QFont()
        font1.setFamilies([u"Arial"])
        font1.setPointSize(10)
        font1.setBold(True)
        self.labelCompany.setFont(font1)
        self.labelCompany.setStyleSheet(u"color: #1E73BE;\n"
"font-size: 10;\n"
"font-weight: bold;\n"
"\n"
"background-color: #D7ECFF;\n"
"\n"
"\n"
"\n"
"\n"
"")
        self.labelCompany.setAlignment(Qt.AlignCenter)

        self.verticalLayout_8.addWidget(self.labelCompany)

        self.labelHeaderInfo = QLabel(self.frame)
        self.labelHeaderInfo.setObjectName(u"labelHeaderInfo")
        font2 = QFont()
        font2.setFamilies([u"Arial"])
        font2.setPointSize(9)
        self.labelHeaderInfo.setFont(font2)
        self.labelHeaderInfo.setStyleSheet(u"color: #6c7b88;\n"
"background-color: #D7ECFF;")
        self.labelHeaderInfo.setAlignment(Qt.AlignCenter)

        self.verticalLayout_8.addWidget(self.labelHeaderInfo)

        self.labelEstadoConexion = QLabel(self.frame)
        self.labelEstadoConexion.setObjectName(u"labelEstadoConexion")
        font3 = QFont()
        font3.setFamilies([u"Arial"])
        font3.setBold(True)
        self.labelEstadoConexion.setFont(font3)
        self.labelEstadoConexion.setStyleSheet(u" background-color: #FFF4D6;\n"
"    color: #0B4A8B;\n"
"    border: 1px solid #E0B13F;\n"
"    border-radius: 10px;\n"
"    padding: 5px;")
        self.labelEstadoConexion.setAlignment(Qt.AlignCenter)

        self.verticalLayout_8.addWidget(self.labelEstadoConexion)


        self.verticalLayout_7.addWidget(self.frame)


        self.gridLayout_2.addLayout(self.verticalLayout_7, 1, 0, 1, 1)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.correo = QLabel(self.centralwidget)
        self.correo.setObjectName(u"correo")
        self.correo.setMaximumSize(QSize(100, 35))
        self.correo.setFont(font1)
        self.correo.setStyleSheet(u"color:#245e91;")

        self.gridLayout.addWidget(self.correo, 0, 0, 1, 1)

        self.rol = QLabel(self.centralwidget)
        self.rol.setObjectName(u"rol")
        self.rol.setMaximumSize(QSize(100, 35))
        self.rol.setFont(font1)
        self.rol.setStyleSheet(u"color:#245e91;")

        self.gridLayout.addWidget(self.rol, 3, 0, 1, 1)

        self.nombre = QLabel(self.centralwidget)
        self.nombre.setObjectName(u"nombre")
        self.nombre.setMaximumSize(QSize(100, 35))
        self.nombre.setFont(font1)
        self.nombre.setStyleSheet(u"color:#245e91;")

        self.gridLayout.addWidget(self.nombre, 1, 0, 1, 1)

        self.listaroles = QComboBox(self.centralwidget)
        self.listaroles.setObjectName(u"listaroles")
        self.listaroles.setMaximumSize(QSize(350, 35))
        self.listaroles.setStyleSheet(u" background-color: white;\n"
"    border: 3px solid #B7DDF5;\n"
"    color: #2e3a46;\n"
"border-radius: 10px;")

        self.gridLayout.addWidget(self.listaroles, 3, 1, 1, 1)

        self.textonombre = QTextEdit(self.centralwidget)
        self.textonombre.setObjectName(u"textonombre")
        self.textonombre.setMaximumSize(QSize(350, 35))
        self.textonombre.setStyleSheet(u" background-color: white;\n"
"    border: 3px solid #B7DDF5;\n"
"    color: #2e3a46;\n"
"border-radius: 10px;")

        self.gridLayout.addWidget(self.textonombre, 1, 1, 1, 1)

        self.textopassword = QTextEdit(self.centralwidget)
        self.textopassword.setObjectName(u"textopassword")
        self.textopassword.setMaximumSize(QSize(350, 35))
        self.textopassword.setStyleSheet(u" background-color: white;\n"
"    border: 3px solid #B7DDF5;\n"
"    color: #2e3a46;\n"
"border-radius: 10px;")

        self.gridLayout.addWidget(self.textopassword, 2, 1, 1, 1)

        self.textocorreo = QTextEdit(self.centralwidget)
        self.textocorreo.setObjectName(u"textocorreo")
        self.textocorreo.setMaximumSize(QSize(350, 35))
        self.textocorreo.setStyleSheet(u" background-color: white;\n"
"    border: 3px solid #B7DDF5;\n"
"    color: #2e3a46;\n"
"border-radius: 10px;")

        self.gridLayout.addWidget(self.textocorreo, 0, 1, 1, 1)

        self.password = QLabel(self.centralwidget)
        self.password.setObjectName(u"password")
        self.password.setMaximumSize(QSize(100, 35))
        self.password.setFont(font1)
        self.password.setStyleSheet(u"color:#245e91;")

        self.gridLayout.addWidget(self.password, 2, 0, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout, 4, 0, 1, 1)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.botonregresar = QPushButton(self.centralwidget)
        self.botonregresar.setObjectName(u"botonregresar")
        self.botonregresar.setMaximumSize(QSize(35, 30))
        font4 = QFont()
        font4.setFamilies([u"Arial"])
        font4.setPointSize(10)
        self.botonregresar.setFont(font4)
        self.botonregresar.setStyleSheet(u"background-color: #5fa8e8;\n"
"color: #ffffff;\n"
"border: 1px solid #5fa8e8;\n"
"")

        self.horizontalLayout_4.addWidget(self.botonregresar)

        self.espacio1 = QSpacerItem(500, 13, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.espacio1)

        self.usuario = QToolButton(self.centralwidget)
        self.usuario.setObjectName(u"usuario")
        self.usuario.setMaximumSize(QSize(16777215, 40))
        self.usuario.setStyleSheet(u"QToolButton {\n"
"    background-color: transparent;\n"
"    border: none;\n"
"    color: #245E91;\n"
"    padding: 0px;\n"
"    margin: 0px;\n"
"    font: 700 10pt \"Arial\";\n"
"}\n"
"\n"
"QToolButton:hover {\n"
"    color: #F4C430;\n"
"    text-decoration: underline;\n"
"}\n"
"\n"
"QToolButton:pressed {\n"
"    background-color: #F4C430;\n"
"    color: #245E91;\n"
"    border-radius: 8px;\n"
"    padding: 4px 8px;\n"
"}")

        self.horizontalLayout_4.addWidget(self.usuario)


        self.gridLayout_2.addLayout(self.horizontalLayout_4, 0, 0, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.espacio4 = QSpacerItem(250, 45, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.espacio4)

        self.botonguardar = QPushButton(self.centralwidget)
        self.botonguardar.setObjectName(u"botonguardar")
        self.botonguardar.setMaximumSize(QSize(300, 35))
        self.botonguardar.setFont(font1)
        self.botonguardar.setStyleSheet(u"background-color: #f4c430;\n"
"color: #3e3a32;\n"
"border-radius: 10px;")

        self.horizontalLayout_2.addWidget(self.botonguardar)

        self.espacio3 = QSpacerItem(250, 45, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.espacio3)


        self.gridLayout_2.addLayout(self.horizontalLayout_2, 5, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.espacio5 = QSpacerItem(150, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.espacio5)

        self.lista = QComboBox(self.centralwidget)
        self.lista.setObjectName(u"lista")
        self.lista.setMaximumSize(QSize(200, 50))
        self.lista.setStyleSheet(u" background-color: white;\n"
"    border: 3px solid #B7DDF5;\n"
"    color: #2e3a46;\n"
"border-radius: 10px;")

        self.horizontalLayout.addWidget(self.lista)

        self.sustituirtarjeta = QLabel(self.centralwidget)
        self.sustituirtarjeta.setObjectName(u"sustituirtarjeta")
        self.sustituirtarjeta.setMaximumSize(QSize(320, 25))
        font5 = QFont()
        font5.setFamilies([u"Arial"])
        font5.setPointSize(18)
        font5.setBold(True)
        self.sustituirtarjeta.setFont(font5)
        self.sustituirtarjeta.setStyleSheet(u"color: #245e91;")
        self.sustituirtarjeta.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.sustituirtarjeta)

        self.espacio2 = QSpacerItem(150, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.espacio2)


        self.gridLayout_2.addLayout(self.horizontalLayout, 2, 0, 1, 1)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")

        self.gridLayout_2.addLayout(self.verticalLayout_2, 3, 0, 1, 1)

        RegistroUsuarioWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(RegistroUsuarioWindow)

        QMetaObject.connectSlotsByName(RegistroUsuarioWindow)
    # setupUi

    def retranslateUi(self, RegistroUsuarioWindow):
        RegistroUsuarioWindow.setWindowTitle(QCoreApplication.translate("RegistroUsuarioWindow", u"MainWindow", None))
        self.Rumsa.setText(QCoreApplication.translate("RegistroUsuarioWindow", u"RUMSA", None))
        self.labelCompany.setText(QCoreApplication.translate("RegistroUsuarioWindow", u"Rutas Urbanas de Matehuala, S.A. de C.V.", None))
        self.labelHeaderInfo.setText(QCoreApplication.translate("RegistroUsuarioWindow", u"M\u00f3dulo de Registro Empleados", None))
        self.labelEstadoConexion.setText(QCoreApplication.translate("RegistroUsuarioWindow", u"\u25cf Conectando", None))
        self.correo.setText(QCoreApplication.translate("RegistroUsuarioWindow", u"Correo", None))
        self.rol.setText(QCoreApplication.translate("RegistroUsuarioWindow", u"Rol", None))
        self.nombre.setText(QCoreApplication.translate("RegistroUsuarioWindow", u"Nombre", None))
        self.password.setText(QCoreApplication.translate("RegistroUsuarioWindow", u"Contrase\u00f1a", None))
        self.botonregresar.setText(QCoreApplication.translate("RegistroUsuarioWindow", u"\u21e6", None))
        self.usuario.setText(QCoreApplication.translate("RegistroUsuarioWindow", u"Usuario", None))
        self.botonguardar.setText(QCoreApplication.translate("RegistroUsuarioWindow", u"Guardar", None))
        self.sustituirtarjeta.setText(QCoreApplication.translate("RegistroUsuarioWindow", u"Registro Empleados", None))
    # retranslateUi

