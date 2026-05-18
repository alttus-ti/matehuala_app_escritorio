# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'cancelar.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFrame,
    QGridLayout, QHBoxLayout, QLabel, QMainWindow,
    QPlainTextEdit, QPushButton, QSizePolicy, QSpacerItem,
    QToolButton, QVBoxLayout, QWidget)

class CancelarWindow(object):
    def setupUi(self, CancelarWindow):
        if not CancelarWindow.objectName():
            CancelarWindow.setObjectName(u"CancelarWindow")
        CancelarWindow.resize(678, 680)
        CancelarWindow.setStyleSheet(u"background-color: #EAF4FF;")
        self.centralwidget = QWidget(CancelarWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.botonregresar = QPushButton(self.centralwidget)
        self.botonregresar.setObjectName(u"botonregresar")
        self.botonregresar.setMaximumSize(QSize(35, 30))
        palette = QPalette()
        brush = QBrush(QColor(255, 255, 255, 255))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText, brush)
        brush1 = QBrush(QColor(95, 168, 232, 255))
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
        self.botonregresar.setPalette(palette)
        font = QFont()
        font.setFamilies([u"Arial"])
        font.setPointSize(10)
        font.setBold(True)
        self.botonregresar.setFont(font)
        self.botonregresar.setStyleSheet(u"background-color: #5fa8e8;\n"
"color: #ffffff;\n"
"border: 1px solid #5fa8e8;\n"
"")

        self.horizontalLayout_2.addWidget(self.botonregresar)

        self.horizontalSpacer_3 = QSpacerItem(500, 40, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_3)

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

        self.horizontalLayout_2.addWidget(self.usuario)


        self.gridLayout.addLayout(self.horizontalLayout_2, 0, 0, 1, 2)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        palette1 = QPalette()
        brush2 = QBrush(QColor(0, 0, 0, 255))
        brush2.setStyle(Qt.BrushStyle.SolidPattern)
        palette1.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText, brush2)
        brush3 = QBrush(QColor(217, 236, 255, 255))
        brush3.setStyle(Qt.BrushStyle.SolidPattern)
        palette1.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Button, brush3)
        palette1.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Light, brush)
        brush4 = QBrush(QColor(227, 227, 227, 255))
        brush4.setStyle(Qt.BrushStyle.SolidPattern)
        palette1.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Midlight, brush4)
        brush5 = QBrush(QColor(107, 118, 127, 255))
        brush5.setStyle(Qt.BrushStyle.SolidPattern)
        palette1.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Dark, brush5)
        brush6 = QBrush(QColor(143, 157, 170, 255))
        brush6.setStyle(Qt.BrushStyle.SolidPattern)
        palette1.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Mid, brush6)
        palette1.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Text, brush2)
        palette1.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.BrightText, brush)
        palette1.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.ButtonText, brush2)
        palette1.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Base, brush3)
        palette1.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Window, brush3)
        brush7 = QBrush(QColor(105, 105, 105, 255))
        brush7.setStyle(Qt.BrushStyle.SolidPattern)
        palette1.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Shadow, brush7)
        brush8 = QBrush(QColor(235, 245, 255, 255))
        brush8.setStyle(Qt.BrushStyle.SolidPattern)
        palette1.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.AlternateBase, brush8)
        brush9 = QBrush(QColor(255, 255, 220, 255))
        brush9.setStyle(Qt.BrushStyle.SolidPattern)
        palette1.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.ToolTipBase, brush9)
        palette1.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.ToolTipText, brush2)
        palette1.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.WindowText, brush2)
        palette1.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Button, brush3)
        palette1.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Light, brush)
        palette1.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Midlight, brush4)
        palette1.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Dark, brush5)
        palette1.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Mid, brush6)
        palette1.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Text, brush2)
        palette1.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.BrightText, brush)
        palette1.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.ButtonText, brush2)
        palette1.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Base, brush3)
        palette1.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Window, brush3)
        palette1.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Shadow, brush7)
        palette1.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.AlternateBase, brush8)
        palette1.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.ToolTipBase, brush9)
        palette1.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.ToolTipText, brush2)
        palette1.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, brush5)
        palette1.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Button, brush3)
        palette1.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Light, brush)
        palette1.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Midlight, brush4)
        palette1.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Dark, brush5)
        palette1.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Mid, brush6)
        palette1.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, brush5)
        palette1.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.BrightText, brush)
        palette1.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, brush5)
        palette1.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Base, brush3)
        palette1.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Window, brush3)
        palette1.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Shadow, brush7)
        brush10 = QBrush(QColor(215, 236, 255, 255))
        brush10.setStyle(Qt.BrushStyle.SolidPattern)
        palette1.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.AlternateBase, brush10)
        palette1.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ToolTipBase, brush9)
        palette1.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ToolTipText, brush2)
        self.frame.setPalette(palette1)
        self.frame.setStyleSheet(u"QFrame#frame {\n"
"    background-color: #D9ECFF;\n"
"    border: 1px solid #7BB7F0;\n"
"    border-radius: 12px;\n"
"}")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.frame)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.labelBrand = QLabel(self.frame)
        self.labelBrand.setObjectName(u"labelBrand")
        self.labelBrand.setMaximumSize(QSize(16777215, 16777215))
        palette2 = QPalette()
        brush11 = QBrush(QColor(240, 181, 29, 255))
        brush11.setStyle(Qt.BrushStyle.SolidPattern)
        palette2.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText, brush11)
        palette2.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Button, brush10)
        palette2.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Text, brush11)
        palette2.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.ButtonText, brush11)
        palette2.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Base, brush10)
        palette2.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Window, brush10)
        palette2.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.WindowText, brush11)
        palette2.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Button, brush10)
        palette2.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Text, brush11)
        palette2.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.ButtonText, brush11)
        palette2.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Base, brush10)
        palette2.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Window, brush10)
        brush12 = QBrush(QColor(120, 120, 120, 255))
        brush12.setStyle(Qt.BrushStyle.SolidPattern)
        palette2.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, brush12)
        palette2.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Button, brush10)
        palette2.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, brush12)
        palette2.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, brush12)
        palette2.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Base, brush10)
        palette2.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Window, brush10)
        self.labelBrand.setPalette(palette2)
        font1 = QFont()
        font1.setFamilies([u"Arial"])
        font1.setPointSize(24)
        font1.setBold(True)
        self.labelBrand.setFont(font1)
        self.labelBrand.setStyleSheet(u"background-color: #D7ECFF;")
        self.labelBrand.setAlignment(Qt.AlignCenter)

        self.verticalLayout_6.addWidget(self.labelBrand)

        self.labelCompany = QLabel(self.frame)
        self.labelCompany.setObjectName(u"labelCompany")
        palette3 = QPalette()
        brush13 = QBrush(QColor(30, 115, 190, 255))
        brush13.setStyle(Qt.BrushStyle.SolidPattern)
        palette3.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText, brush13)
        palette3.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Button, brush10)
        palette3.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Text, brush13)
        palette3.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.ButtonText, brush13)
        palette3.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Base, brush10)
        palette3.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Window, brush10)
        palette3.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.WindowText, brush13)
        palette3.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Button, brush10)
        palette3.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Text, brush13)
        palette3.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.ButtonText, brush13)
        palette3.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Base, brush10)
        palette3.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Window, brush10)
        palette3.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, brush13)
        palette3.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Button, brush10)
        palette3.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, brush13)
        palette3.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, brush13)
        palette3.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Base, brush10)
        palette3.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Window, brush10)
        self.labelCompany.setPalette(palette3)
        self.labelCompany.setFont(font)
        self.labelCompany.setStyleSheet(u"color: #1E73BE;\n"
"font-size: 10;\n"
"font-weight: bold;\n"
"background-color: #D7ECFF;")
        self.labelCompany.setAlignment(Qt.AlignCenter)
        self.labelCompany.setWordWrap(True)

        self.verticalLayout_6.addWidget(self.labelCompany)

        self.labelHeaderInfo = QLabel(self.frame)
        self.labelHeaderInfo.setObjectName(u"labelHeaderInfo")
        font2 = QFont()
        font2.setFamilies([u"Arial"])
        font2.setPointSize(9)
        font2.setBold(False)
        self.labelHeaderInfo.setFont(font2)
        self.labelHeaderInfo.setStyleSheet(u"color: #6c7b88;\n"
"background-color: #D7ECFF;")
        self.labelHeaderInfo.setAlignment(Qt.AlignCenter)

        self.verticalLayout_6.addWidget(self.labelHeaderInfo)

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

        self.verticalLayout_6.addWidget(self.labelEstadoConexion)


        self.verticalLayout_5.addWidget(self.frame)


        self.verticalLayout.addLayout(self.verticalLayout_5)


        self.gridLayout.addLayout(self.verticalLayout, 1, 0, 1, 2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.puerto = QComboBox(self.centralwidget)
        self.puerto.setObjectName(u"puerto")
        self.puerto.setMaximumSize(QSize(200, 50))
        palette4 = QPalette()
        brush14 = QBrush(QColor(46, 58, 70, 255))
        brush14.setStyle(Qt.BrushStyle.SolidPattern)
        palette4.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText, brush14)
        palette4.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Button, brush)
        palette4.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Text, brush14)
        palette4.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.ButtonText, brush14)
        palette4.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Base, brush)
        palette4.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Window, brush)
        palette4.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.WindowText, brush14)
        palette4.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Button, brush)
        palette4.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Text, brush14)
        palette4.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.ButtonText, brush14)
        palette4.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Base, brush)
        palette4.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Window, brush)
        palette4.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, brush14)
        palette4.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Button, brush)
        palette4.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, brush14)
        palette4.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, brush14)
        palette4.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Base, brush)
        palette4.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Window, brush)
        self.puerto.setPalette(palette4)
        self.puerto.setStyleSheet(u" background-color: white;\n"
"    border: 3px solid #B7DDF5;\n"
"    color: #2e3a46;\n"
"border-radius: 10px;")

        self.horizontalLayout.addWidget(self.puerto)

        self.textocancelar = QLabel(self.centralwidget)
        self.textocancelar.setObjectName(u"textocancelar")
        self.textocancelar.setMaximumSize(QSize(16777215, 16777215))
        font4 = QFont()
        font4.setFamilies([u"Arial"])
        font4.setPointSize(18)
        font4.setBold(True)
        self.textocancelar.setFont(font4)
        self.textocancelar.setStyleSheet(u"color: #245e91;")

        self.horizontalLayout.addWidget(self.textocancelar)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.gridLayout.addLayout(self.horizontalLayout, 2, 0, 1, 2)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.espacio4 = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout_2.addItem(self.espacio4)

        self.nombre = QLabel(self.centralwidget)
        self.nombre.setObjectName(u"nombre")
        self.nombre.setMaximumSize(QSize(450, 20))
        font5 = QFont()
        font5.setFamilies([u"Arial"])
        font5.setPointSize(10)
        font5.setBold(True)
        font5.setItalic(False)
        self.nombre.setFont(font5)
        self.nombre.setStyleSheet(u"color:#245e91;")

        self.verticalLayout_2.addWidget(self.nombre)

        self.textonombre = QPlainTextEdit(self.centralwidget)
        self.textonombre.setObjectName(u"textonombre")
        self.textonombre.setMaximumSize(QSize(300, 40))
        self.textonombre.setStyleSheet(u" background-color: white;\n"
"    border: 3px solid #B7DDF5;\n"
"    color: #2e3a46;\n"
"border-radius: 10px;")

        self.verticalLayout_2.addWidget(self.textonombre)

        self.espacio3 = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout_2.addItem(self.espacio3)

        self.uid = QLabel(self.centralwidget)
        self.uid.setObjectName(u"uid")
        self.uid.setMaximumSize(QSize(450, 20))
        self.uid.setFont(font5)
        self.uid.setStyleSheet(u"color:#245e91;")

        self.verticalLayout_2.addWidget(self.uid)

        self.textouid = QLabel(self.centralwidget)
        self.textouid.setObjectName(u"textouid")
        self.textouid.setMaximumSize(QSize(450, 20))
        font6 = QFont()
        font6.setFamilies([u"Arial"])
        font6.setPointSize(12)
        font6.setBold(False)
        font6.setItalic(True)
        self.textouid.setFont(font6)
        self.textouid.setStyleSheet(u"color:#4b5560;")

        self.verticalLayout_2.addWidget(self.textouid)

        self.listanegra = QCheckBox(self.centralwidget)
        self.listanegra.setObjectName(u"listanegra")
        font7 = QFont()
        font7.setFamilies([u"Arial"])
        font7.setPointSize(10)
        font7.setBold(False)
        font7.setItalic(False)
        self.listanegra.setFont(font7)
        self.listanegra.setStyleSheet(u"color:#4b5560;")

        self.verticalLayout_2.addWidget(self.listanegra)

        self.espaio5 = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout_2.addItem(self.espaio5)


        self.gridLayout.addLayout(self.verticalLayout_2, 3, 0, 1, 1)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.espacio4_2 = QSpacerItem(20, 60, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout_3.addItem(self.espacio4_2)

        self.motivo = QLabel(self.centralwidget)
        self.motivo.setObjectName(u"motivo")
        self.motivo.setMaximumSize(QSize(450, 20))
        self.motivo.setFont(font5)
        self.motivo.setStyleSheet(u"color:#245e91;")

        self.verticalLayout_3.addWidget(self.motivo)

        self.textomotivo = QPlainTextEdit(self.centralwidget)
        self.textomotivo.setObjectName(u"textomotivo")
        self.textomotivo.setMaximumSize(QSize(250, 125))
        self.textomotivo.setStyleSheet(u" background-color: white;\n"
"    border: 3px solid #B7DDF5;\n"
"    color: #2e3a46;\n"
"border-radius: 10px;")

        self.verticalLayout_3.addWidget(self.textomotivo)

        self.espacio4_3 = QSpacerItem(40, 60, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout_3.addItem(self.espacio4_3)


        self.gridLayout.addLayout(self.verticalLayout_3, 3, 1, 1, 1)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.espacio2 = QSpacerItem(20, 50, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.horizontalLayout_4.addItem(self.espacio2)

        self.botoncancelar = QPushButton(self.centralwidget)
        self.botoncancelar.setObjectName(u"botoncancelar")
        self.botoncancelar.setMaximumSize(QSize(150, 40))
        self.botoncancelar.setFont(font)
        self.botoncancelar.setStyleSheet(u"background-color: #f4c430;\n"
"color: #3e3a32;\n"
"border-radius: 10px;")

        self.horizontalLayout_4.addWidget(self.botoncancelar)

        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setMaximumSize(QSize(150, 40))
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet(u"background-color: #f4c430;\n"
"color: #3e3a32;\n"
"border-radius: 10px;")

        self.horizontalLayout_4.addWidget(self.pushButton)

        self.espacio1 = QSpacerItem(20, 50, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.horizontalLayout_4.addItem(self.espacio1)


        self.gridLayout.addLayout(self.horizontalLayout_4, 4, 0, 1, 2)

        CancelarWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(CancelarWindow)

        QMetaObject.connectSlotsByName(CancelarWindow)
    # setupUi

    def retranslateUi(self, CancelarWindow):
        CancelarWindow.setWindowTitle(QCoreApplication.translate("CancelarWindow", u"RUMA | Cancelar", None))
        self.botonregresar.setText(QCoreApplication.translate("CancelarWindow", u"\u21e6", None))
        self.usuario.setText(QCoreApplication.translate("CancelarWindow", u"Usuario", None))
        self.labelBrand.setText(QCoreApplication.translate("CancelarWindow", u"RUMSA", None))
        self.labelCompany.setText(QCoreApplication.translate("CancelarWindow", u"Rutas Urbanas de Matehuala, S.A. de C.V.", None))
        self.labelHeaderInfo.setText(QCoreApplication.translate("CancelarWindow", u"M\u00f3dulo de cancelaci\u00f3n", None))
        self.labelEstadoConexion.setText(QCoreApplication.translate("CancelarWindow", u"\u25cf Conectando", None))
        self.textocancelar.setText(QCoreApplication.translate("CancelarWindow", u"Cancelar Tarjeta", None))
        self.nombre.setText(QCoreApplication.translate("CancelarWindow", u"Nombre", None))
        self.uid.setText(QCoreApplication.translate("CancelarWindow", u"UID", None))
        self.textouid.setText(QCoreApplication.translate("CancelarWindow", u"UID", None))
        self.listanegra.setText(QCoreApplication.translate("CancelarWindow", u"Lista Negra", None))
        self.motivo.setText(QCoreApplication.translate("CancelarWindow", u"Motivo", None))
        self.botoncancelar.setText(QCoreApplication.translate("CancelarWindow", u"Cancelar Tarjeta", None))
        self.pushButton.setText(QCoreApplication.translate("CancelarWindow", u"Reactivar Tarjeta", None))
    # retranslateUi

