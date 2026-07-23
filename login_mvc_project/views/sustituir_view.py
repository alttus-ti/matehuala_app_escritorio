# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'sustituir.ui'
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
from PySide6.QtWidgets import (QApplication, QCalendarWidget, QComboBox, QFrame,
    QGridLayout, QHBoxLayout, QLabel, QLineEdit,
    QMainWindow, QPushButton, QSizePolicy, QSpacerItem,
    QTextBrowser, QToolButton, QVBoxLayout, QWidget)

class SustituirWindow(object):
    def setupUi(self, SustituirWindow):
        if not SustituirWindow.objectName():
            SustituirWindow.setObjectName(u"SustituirWindow")
        SustituirWindow.resize(680, 680)
        SustituirWindow.setStyleSheet(u"background-color: #EAF4FF;")
        self.centralwidget = QWidget(SustituirWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.botonregresar = QPushButton(self.centralwidget)
        self.botonregresar.setObjectName(u"botonregresar")
        self.botonregresar.setMaximumSize(QSize(35, 30))
        font = QFont()
        font.setFamilies([u"Arial"])
        font.setPointSize(10)
        self.botonregresar.setFont(font)
        self.botonregresar.setStyleSheet(u"background-color: #5fa8e8;\n"
"color: #ffffff;\n"
"border: 1px solid #5fa8e8;\n"
"")

        self.horizontalLayout_4.addWidget(self.botonregresar)

        self.horizontalSpacer_3 = QSpacerItem(500, 13, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_3)

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


        self.gridLayout.addLayout(self.horizontalLayout_4, 0, 0, 1, 2)

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
        self.labelBrand = QLabel(self.frame)
        self.labelBrand.setObjectName(u"labelBrand")
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
        self.labelBrand.setPalette(palette)
        font1 = QFont()
        font1.setFamilies([u"Arial"])
        font1.setPointSize(24)
        font1.setBold(True)
        self.labelBrand.setFont(font1)
        self.labelBrand.setStyleSheet(u"background-color: #D7ECFF;\n"
"color: #f0b51d;\n"
"font-weight: bold;")
        self.labelBrand.setAlignment(Qt.AlignCenter)

        self.verticalLayout_8.addWidget(self.labelBrand)

        self.labelCompany = QLabel(self.frame)
        self.labelCompany.setObjectName(u"labelCompany")
        font2 = QFont()
        font2.setFamilies([u"Arial"])
        font2.setPointSize(10)
        font2.setBold(True)
        self.labelCompany.setFont(font2)
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
        font3 = QFont()
        font3.setFamilies([u"Arial"])
        font3.setPointSize(9)
        self.labelHeaderInfo.setFont(font3)
        self.labelHeaderInfo.setStyleSheet(u"color: #6c7b88;\n"
"background-color: #D7ECFF;")
        self.labelHeaderInfo.setAlignment(Qt.AlignCenter)

        self.verticalLayout_8.addWidget(self.labelHeaderInfo)

        self.labelEstadoConexion = QLabel(self.frame)
        self.labelEstadoConexion.setObjectName(u"labelEstadoConexion")
        font4 = QFont()
        font4.setFamilies([u"Arial"])
        font4.setBold(True)
        self.labelEstadoConexion.setFont(font4)
        self.labelEstadoConexion.setStyleSheet(u" background-color: #FFF4D6;\n"
"    color: #0B4A8B;\n"
"    border: 1px solid #E0B13F;\n"
"    border-radius: 10px;\n"
"    padding: 5px;")
        self.labelEstadoConexion.setAlignment(Qt.AlignCenter)

        self.verticalLayout_8.addWidget(self.labelEstadoConexion)


        self.verticalLayout_7.addWidget(self.frame)


        self.gridLayout.addLayout(self.verticalLayout_7, 1, 0, 1, 2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.espacio5 = QSpacerItem(150, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

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
        self.sustituirtarjeta.setMaximumSize(QSize(200, 25))
        font5 = QFont()
        font5.setFamilies([u"Arial"])
        font5.setPointSize(18)
        font5.setBold(True)
        self.sustituirtarjeta.setFont(font5)
        self.sustituirtarjeta.setStyleSheet(u"color: #245e91;")
        self.sustituirtarjeta.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.sustituirtarjeta)

        self.espacio2 = QSpacerItem(150, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.espacio2)


        self.gridLayout.addLayout(self.horizontalLayout, 2, 0, 1, 2)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.espacio7 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout.addItem(self.espacio7)

        self.nombre = QLabel(self.centralwidget)
        self.nombre.setObjectName(u"nombre")
        self.nombre.setMaximumSize(QSize(100, 20))
        self.nombre.setFont(font2)
        self.nombre.setStyleSheet(u"color:#245e91;")

        self.verticalLayout.addWidget(self.nombre)

        self.textonombre = QTextBrowser(self.centralwidget)
        self.textonombre.setObjectName(u"textonombre")
        self.textonombre.setMaximumSize(QSize(300, 30))
        self.textonombre.setStyleSheet(u" background-color: white;\n"
"    border: 3px solid #B7DDF5;\n"
"    color: #2e3a46;\n"
"border-radius: 10px;")

        self.verticalLayout.addWidget(self.textonombre)

        self.curp = QLabel(self.centralwidget)
        self.curp.setObjectName(u"curp")
        self.curp.setMaximumSize(QSize(600, 20))
        self.curp.setFont(font2)
        self.curp.setStyleSheet(u"color:#245e91;")

        self.verticalLayout.addWidget(self.curp)

        self.textocurp = QLabel(self.centralwidget)
        self.textocurp.setObjectName(u"textocurp")
        self.textocurp.setMaximumSize(QSize(600, 20))
        font6 = QFont()
        font6.setFamilies([u"Arial"])
        font6.setPointSize(10)
        font6.setBold(False)
        self.textocurp.setFont(font6)
        self.textocurp.setStyleSheet(u"color:#4b5560;")

        self.verticalLayout.addWidget(self.textocurp)

        self.fechanacimiento = QLabel(self.centralwidget)
        self.fechanacimiento.setObjectName(u"fechanacimiento")
        self.fechanacimiento.setMaximumSize(QSize(600, 20))
        self.fechanacimiento.setFont(font2)
        self.fechanacimiento.setStyleSheet(u"color:#245e91;")

        self.verticalLayout.addWidget(self.fechanacimiento)

        self.textofecha = QLabel(self.centralwidget)
        self.textofecha.setObjectName(u"textofecha")
        self.textofecha.setMaximumSize(QSize(600, 20))
        self.textofecha.setFont(font6)
        self.textofecha.setStyleSheet(u"color:#4b5560;")

        self.verticalLayout.addWidget(self.textofecha)

        self.uid = QLabel(self.centralwidget)
        self.uid.setObjectName(u"uid")
        self.uid.setMaximumSize(QSize(600, 20))
        self.uid.setFont(font2)
        self.uid.setStyleSheet(u"color:#245e91;")

        self.verticalLayout.addWidget(self.uid)

        self.textouid = QLabel(self.centralwidget)
        self.textouid.setObjectName(u"textouid")
        self.textouid.setMaximumSize(QSize(600, 20))
        self.textouid.setFont(font6)
        self.textouid.setStyleSheet(u"color:#4b5560;")

        self.verticalLayout.addWidget(self.textouid)

        self.tipotarjeta = QLabel(self.centralwidget)
        self.tipotarjeta.setObjectName(u"tipotarjeta")
        self.tipotarjeta.setMaximumSize(QSize(600, 20))
        self.tipotarjeta.setFont(font2)
        self.tipotarjeta.setStyleSheet(u"color:#245e91;")

        self.verticalLayout.addWidget(self.tipotarjeta)

        self.textotipo = QLabel(self.centralwidget)
        self.textotipo.setObjectName(u"textotipo")
        self.textotipo.setMaximumSize(QSize(600, 20))
        self.textotipo.setFont(font6)
        self.textotipo.setStyleSheet(u"color:#4b5560;")

        self.verticalLayout.addWidget(self.textotipo)

        self.espacio8 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout.addItem(self.espacio8)


        self.gridLayout.addLayout(self.verticalLayout, 4, 0, 1, 1)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.vigencia = QLabel(self.centralwidget)
        self.vigencia.setObjectName(u"vigencia")
        self.vigencia.setMaximumSize(QSize(100, 20))
        self.vigencia.setFont(font2)
        self.vigencia.setStyleSheet(u"color:#245e91;")

        self.verticalLayout_2.addWidget(self.vigencia)

        self.textovigencia = QTextBrowser(self.centralwidget)
        self.textovigencia.setObjectName(u"textovigencia")
        self.textovigencia.setMaximumSize(QSize(200, 30))
        self.textovigencia.setStyleSheet(u" background-color: white;\n"
"    border: 3px solid #B7DDF5;\n"
"    color: #2e3a46;\n"
"border-radius: 10px;")

        self.verticalLayout_2.addWidget(self.textovigencia)

        self.calendario = QCalendarWidget(self.centralwidget)
        self.calendario.setObjectName(u"calendario")
        self.calendario.setMaximumSize(QSize(380, 280))
        font7 = QFont()
        font7.setBold(False)
        self.calendario.setFont(font7)
        self.calendario.setStyleSheet(u"QCalendarWidget QWidget#qt_calendar_navigationbar {\n"
"    background-color: #0078D7;\n"
"}\n"
"\n"
"QCalendarWidget QToolButton {\n"
"    background-color: #0078D7;\n"
"    color: white;\n"
"    border: none;\n"
"    font-weight: bold;\n"
"}\n"
"\n"
"QCalendarWidget QToolButton#qt_calendar_monthbutton,\n"
"QCalendarWidget QToolButton#qt_calendar_yearbutton {\n"
"    color: white;\n"
"}\n"
"\n"
"QCalendarWidget QSpinBox {\n"
"    background-color: #0078D7;\n"
"    color: white;\n"
"    border: none;\n"
"}\n"
"\n"
"QCalendarWidget QAbstractItemView {\n"
"    background-color: white;\n"
"    color: black;\n"
"    selection-background-color: #E8E8E8;\n"
"    selection-color: black;\n"
"}")

        self.verticalLayout_2.addWidget(self.calendario)


        self.gridLayout.addLayout(self.verticalLayout_2, 4, 1, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.espacio4 = QSpacerItem(80, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.espacio4)

        self.buscar = QLabel(self.centralwidget)
        self.buscar.setObjectName(u"buscar")
        self.buscar.setMaximumSize(QSize(50, 35))
        self.buscar.setFont(font2)
        self.buscar.setStyleSheet(u"color:#245e91;")

        self.horizontalLayout_2.addWidget(self.buscar)

        self.buscador = QLineEdit(self.centralwidget)
        self.buscador.setObjectName(u"buscador")
        self.buscador.setMaximumSize(QSize(350, 30))
        self.buscador.setStyleSheet(u" background-color: white;\n"
"    border: 3px solid #B7DDF5;\n"
"    color: #2e3a46;\n"
"border-radius: 10px;")

        self.horizontalLayout_2.addWidget(self.buscador)

        self.espacio3 = QSpacerItem(80, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.espacio3)


        self.gridLayout.addLayout(self.horizontalLayout_2, 3, 0, 1, 2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.espacio9 = QSpacerItem(20, 50, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.horizontalLayout_3.addItem(self.espacio9)

        self.botonsustituir = QPushButton(self.centralwidget)
        self.botonsustituir.setObjectName(u"botonsustituir")
        self.botonsustituir.setMaximumSize(QSize(200, 40))
        self.botonsustituir.setFont(font2)
        self.botonsustituir.setStyleSheet(u"background-color: #f4c430;\n"
"color: #3e3a32;\n"
"border-radius: 10px;")

        self.horizontalLayout_3.addWidget(self.botonsustituir)

        self.espacio10 = QSpacerItem(20, 50, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.horizontalLayout_3.addItem(self.espacio10)


        self.gridLayout.addLayout(self.horizontalLayout_3, 5, 0, 1, 2)

        SustituirWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(SustituirWindow)

        QMetaObject.connectSlotsByName(SustituirWindow)
    # setupUi

    def retranslateUi(self, SustituirWindow):
        SustituirWindow.setWindowTitle(QCoreApplication.translate("SustituirWindow", u"RUMSA | Sustituir Tarjeta", None))
        self.botonregresar.setText(QCoreApplication.translate("SustituirWindow", u"\u21e6", None))
        self.usuario.setText(QCoreApplication.translate("SustituirWindow", u"Usuario", None))
        self.labelBrand.setText(QCoreApplication.translate("SustituirWindow", u"RUMSA", None))
        self.labelCompany.setText(QCoreApplication.translate("SustituirWindow", u"Rutas Urbanas de Matehuala, S.A. de C.V.", None))
        self.labelHeaderInfo.setText(QCoreApplication.translate("SustituirWindow", u"M\u00f3dulo de sustituci\u00f3n", None))
        self.labelEstadoConexion.setText(QCoreApplication.translate("SustituirWindow", u"\u25cf Conectando", None))
        self.sustituirtarjeta.setText(QCoreApplication.translate("SustituirWindow", u"Sustituir Tarjeta", None))
        self.nombre.setText(QCoreApplication.translate("SustituirWindow", u"Nombre", None))
        self.curp.setText(QCoreApplication.translate("SustituirWindow", u"Curp", None))
        self.textocurp.setText(QCoreApplication.translate("SustituirWindow", u"Curp", None))
        self.fechanacimiento.setText(QCoreApplication.translate("SustituirWindow", u"Fecha de Nacimiento", None))
        self.textofecha.setText(QCoreApplication.translate("SustituirWindow", u"fecha de nacimiento", None))
        self.uid.setText(QCoreApplication.translate("SustituirWindow", u"UID", None))
        self.textouid.setText(QCoreApplication.translate("SustituirWindow", u"uid", None))
        self.tipotarjeta.setText(QCoreApplication.translate("SustituirWindow", u"Tipo de Tarjeta", None))
        self.textotipo.setText(QCoreApplication.translate("SustituirWindow", u"Tipo de tarjeta", None))
        self.vigencia.setText(QCoreApplication.translate("SustituirWindow", u"Vigencia", None))
        self.buscar.setText(QCoreApplication.translate("SustituirWindow", u"Buscar", None))
        self.botonsustituir.setText(QCoreApplication.translate("SustituirWindow", u"Sustituir", None))
    # retranslateUi

