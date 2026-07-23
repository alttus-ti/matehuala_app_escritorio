# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dar_de_alta.ui'
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
    QGridLayout, QHBoxLayout, QLabel, QMainWindow,
    QPushButton, QRadioButton, QSizePolicy, QSpacerItem,
    QTextEdit, QToolButton, QVBoxLayout, QWidget)

class AltaWindow(object):
    def setupUi(self, AltaWindow):
        if not AltaWindow.objectName():
            AltaWindow.setObjectName(u"AltaWindow")
        AltaWindow.resize(680, 680)
        self.centralwidget = QWidget(AltaWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setStyleSheet(u"QWidget#centralwidget {\n"
"    background-color: #EAF4FF;\n"
"}\n"
"QFrame#frameHeader {\n"
"    background-color: #D7ECFF;\n"
"    border: 2px solid #92BEE5;\n"
"    border-radius: 18px;\n"
"}\n"
"QLabel#labelBrand {\n"
"    color: #F0B51D;\n"
"    font: 700 24pt \"Arial\";\n"
"    letter-spacing: 2px;\n"
"}\n"
"QLabel#labelCompany {\n"
"    color: #2E79BD;\n"
"    font: 700 10pt \"Arial\";\n"
"}\n"
"QLabel#labelHeaderInfo {\n"
"    color: #6C7B88;\n"
"    font: 9pt \"Arial\";\n"
"}\n"
"QLabel#menu, QLabel#label, QLabel#Recargar, QLabel#alta {\n"
"    color: #245E91;\n"
"    font: 700 18pt \"Arial\";\n"
"}\n"
"QLabel#otrosdatos, QLabel#nombre, QLabel#uid, QLabel#tarjeta, QLabel#saldo, QLabel#saldonuevo, QLabel#vigencia {\n"
"    color: #245E91;\n"
"    font: 700 10pt \"Arial\";\n"
"}\n"
"QLabel#texto1, QLabel#texto2, QLabel#texto4, QLabel#texto5, QLabel#texto6, QLabel#texto7 {\n"
"    color: #4B5560;\n"
"    font: 10pt \"Arial\";\n"
"}\n"
"QLabel#signopeso, QLabel#signopeso2, QLabel#signopeso3 {\n"
"    colo"
                        "r: #F0B51D;\n"
"    font: 700 16pt \"Arial\";\n"
"}\n"
"QPushButton {\n"
"    background-color: #F4C430;\n"
"    color: #3E3A32;\n"
"    border: none;\n"
"    border-radius: 12px;\n"
"    padding: 10px 16px;\n"
"    font: 700 10pt \"Arial\";\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #E7B91C;\n"
"}\n"
"QPushButton#botonregresar {\n"
"    background-color: #5FA8E8;\n"
"    color: white;\n"
"    border-radius: 12px;\n"
"    padding: 0px;\n"
"}\n"
"QPushButton#botonregresar:hover {\n"
"    background-color: #6CA8DB;\n"
"}\n"
"QLineEdit, QTextEdit, QTextBrowser, QComboBox, QCalendarWidget QAbstractItemView {\n"
"    background-color: white;\n"
"    color: #2E3A46;\n"
"}\n"
"QTextEdit, QTextBrowser, QComboBox, QCalendarWidget, QLineEdit {\n"
"    border: 2px solid #B8D8F3;\n"
"    border-radius: 12px;\n"
"    padding: 6px 8px;\n"
"}\n"
"QTextEdit:focus, QComboBox:focus, QLineEdit:focus {\n"
"    border: 2px solid #F3C623;\n"
"}\n"
"QRadioButton {\n"
"    color: #4B5560;\n"
"    font: 10pt \"Arial\";\n"
""
                        "}\n"
"QRadioButton::indicator:checked {\n"
"    background-color: #F4C430;\n"
"    border: 2px solid #E0AE12;\n"
"    width: 12px;\n"
"    height: 12px;\n"
"    border-radius: 7px;\n"
"}\n"
"QCalendarWidget QWidget {\n"
"    alternate-background-color: #EAF4FF;\n"
"}\n"
"QCalendarWidget QToolButton {\n"
"    color: #245E91;\n"
"    font: 700 10pt \"Arial\";\n"
"}\n"
"QCalendarWidget QMenu {\n"
"    background-color: white;\n"
"}\n"
"QCalendarWidget QSpinBox {\n"
"    background-color: white;\n"
"    color: #2E3A46;\n"
"}\n"
"QHeaderView::section {\n"
"    background-color: #D7ECFF;\n"
"    color: #245E91;\n"
"    font: 700 9pt \"Arial\";\n"
"    border: 1px solid #B8D8F3;\n"
"}\n"
"QPushButton#botonguardar {\n"
"    min-width: 180px;\n"
"    min-height: 44px;\n"
"    font: 700 11pt \"Arial\";\n"
"}\n"
"QLabel#labelEstadoConexion {\n"
"    background-color: #FFF7D6;\n"
"    color: #245E91;\n"
"    border: 1px solid #F0C247;\n"
"    border-radius: 10px;\n"
"    padding: 4px 10px;\n"
"    font: 700 8pt \"Arial\";"
                        "\n"
"}\n"
"")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.botonregresar = QPushButton(self.centralwidget)
        self.botonregresar.setObjectName(u"botonregresar")
        self.botonregresar.setMaximumSize(QSize(35, 30))
        font = QFont()
        font.setFamilies([u"Arial"])
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(False)
        self.botonregresar.setFont(font)

        self.horizontalLayout_6.addWidget(self.botonregresar)

        self.horizontalSpacer_3 = QSpacerItem(500, 40, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_3)

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

        self.horizontalLayout_6.addWidget(self.usuario)


        self.gridLayout.addLayout(self.horizontalLayout_6, 0, 0, 1, 3)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.frameHeader = QFrame(self.centralwidget)
        self.frameHeader.setObjectName(u"frameHeader")
        self.frameHeader.setFrameShape(QFrame.StyledPanel)
        self.frameHeader.setFrameShadow(QFrame.Raised)
        self.verticalLayout_header = QVBoxLayout(self.frameHeader)
        self.verticalLayout_header.setSpacing(2)
        self.verticalLayout_header.setObjectName(u"verticalLayout_header")
        self.verticalLayout_header.setContentsMargins(16, 14, 16, 14)
        self.labelBrand = QLabel(self.frameHeader)
        self.labelBrand.setObjectName(u"labelBrand")
        self.labelBrand.setAlignment(Qt.AlignCenter)

        self.verticalLayout_header.addWidget(self.labelBrand)

        self.labelCompany = QLabel(self.frameHeader)
        self.labelCompany.setObjectName(u"labelCompany")
        self.labelCompany.setAlignment(Qt.AlignCenter)
        self.labelCompany.setWordWrap(True)

        self.verticalLayout_header.addWidget(self.labelCompany)

        self.labelHeaderInfo = QLabel(self.frameHeader)
        self.labelHeaderInfo.setObjectName(u"labelHeaderInfo")
        self.labelHeaderInfo.setAlignment(Qt.AlignCenter)

        self.verticalLayout_header.addWidget(self.labelHeaderInfo)

        self.labelEstadoConexion = QLabel(self.frameHeader)
        self.labelEstadoConexion.setObjectName(u"labelEstadoConexion")
        self.labelEstadoConexion.setAlignment(Qt.AlignCenter)

        self.verticalLayout_header.addWidget(self.labelEstadoConexion)

        self.mensajeInternet = QLabel(self.frameHeader)
        self.mensajeInternet.setObjectName(u"mensajeInternet")
        font1 = QFont()
        font1.setBold(True)
        self.mensajeInternet.setFont(font1)
        self.mensajeInternet.setStyleSheet(u"color:red;")
        self.mensajeInternet.setAlignment(Qt.AlignCenter)
        self.mensajeInternet.setVisible(False)

        self.verticalLayout_header.addWidget(self.mensajeInternet)


        self.verticalLayout.addWidget(self.frameHeader)


        self.gridLayout.addLayout(self.verticalLayout, 1, 0, 1, 3)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)

        self.comboBox = QComboBox(self.centralwidget)
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setMaximumSize(QSize(300, 40))

        self.horizontalLayout_3.addWidget(self.comboBox)

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")

        self.horizontalLayout_3.addWidget(self.label)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)


        self.gridLayout.addLayout(self.horizontalLayout_3, 2, 0, 1, 2)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.otrosdatos = QLabel(self.centralwidget)
        self.otrosdatos.setObjectName(u"otrosdatos")
        self.otrosdatos.setMaximumSize(QSize(16777215, 20))
        self.otrosdatos.setFont(font)
        self.otrosdatos.setAlignment(Qt.AlignCenter)

        self.verticalLayout_3.addWidget(self.otrosdatos)

        self.normal = QRadioButton(self.centralwidget)
        self.normal.setObjectName(u"normal")
        self.normal.setMaximumSize(QSize(100, 50))
        font2 = QFont()
        font2.setFamilies([u"Arial"])
        font2.setPointSize(10)
        font2.setBold(False)
        font2.setItalic(False)
        self.normal.setFont(font2)

        self.verticalLayout_3.addWidget(self.normal)

        self.preferencial = QRadioButton(self.centralwidget)
        self.preferencial.setObjectName(u"preferencial")
        self.preferencial.setMaximumSize(QSize(100, 50))
        self.preferencial.setFont(font2)

        self.verticalLayout_3.addWidget(self.preferencial)

        self.vigencia = QLabel(self.centralwidget)
        self.vigencia.setObjectName(u"vigencia")
        self.vigencia.setMaximumSize(QSize(16777215, 20))
        self.vigencia.setFont(font)

        self.verticalLayout_3.addWidget(self.vigencia)

        self.textovigencia = QTextEdit(self.centralwidget)
        self.textovigencia.setObjectName(u"textovigencia")
        self.textovigencia.setMaximumSize(QSize(300, 40))

        self.verticalLayout_3.addWidget(self.textovigencia)

        self.calendario = QCalendarWidget(self.centralwidget)
        self.calendario.setObjectName(u"calendario")
        self.calendario.setMaximumSize(QSize(300, 16777215))
        palette = QPalette()
        self.calendario.setPalette(palette)
        self.calendario.setStyleSheet(u"QCalendarWidget QToolButton#qt_calendar_monthbutton {\n"
"    color: white;\n"
"}\n"
"\n"
"QCalendarWidget QToolButton#qt_calendar_yearbutton {\n"
"    color: white;\n"
"}")

        self.verticalLayout_3.addWidget(self.calendario)

        self.espacio5 = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout_3.addItem(self.espacio5)


        self.gridLayout.addLayout(self.verticalLayout_3, 2, 2, 6, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.espacio3 = QSpacerItem(10, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.espacio3)

        self.nombre = QLabel(self.centralwidget)
        self.nombre.setObjectName(u"nombre")
        self.nombre.setFont(font)

        self.horizontalLayout_2.addWidget(self.nombre)

        self.textonombre = QTextEdit(self.centralwidget)
        self.textonombre.setObjectName(u"textonombre")
        self.textonombre.setMaximumSize(QSize(500, 40))

        self.horizontalLayout_2.addWidget(self.textonombre)

        self.espacio4 = QSpacerItem(10, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.espacio4)


        self.gridLayout.addLayout(self.horizontalLayout_2, 3, 0, 1, 2)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.espacio7 = QSpacerItem(10, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.espacio7)

        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMaximumSize(QSize(200, 20))
        palette1 = QPalette()
        brush = QBrush(QColor(36, 94, 145, 255))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette1.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText, brush)
        palette1.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Text, brush)
        palette1.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.ButtonText, brush)
        palette1.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.WindowText, brush)
        palette1.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Text, brush)
        palette1.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.ButtonText, brush)
        brush1 = QBrush(QColor(120, 120, 120, 255))
        brush1.setStyle(Qt.BrushStyle.SolidPattern)
        palette1.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, brush1)
        palette1.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, brush1)
        palette1.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, brush1)
        self.label_2.setPalette(palette1)
        font3 = QFont()
        font3.setFamilies([u"Arial"])
        font3.setPointSize(12)
        font3.setBold(True)
        self.label_2.setFont(font3)

        self.horizontalLayout_4.addWidget(self.label_2)

        self.textocurp = QTextEdit(self.centralwidget)
        self.textocurp.setObjectName(u"textocurp")
        self.textocurp.setMaximumSize(QSize(500, 40))

        self.horizontalLayout_4.addWidget(self.textocurp)

        self.espacio6 = QSpacerItem(10, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.espacio6)


        self.gridLayout.addLayout(self.horizontalLayout_4, 4, 0, 1, 2)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.curpstatus = QLabel(self.centralwidget)
        self.curpstatus.setObjectName(u"curpstatus")
        self.curpstatus.setMaximumSize(QSize(16777215, 30))
        font4 = QFont()
        font4.setFamilies([u"Arial"])
        font4.setPointSize(9)
        self.curpstatus.setFont(font4)

        self.verticalLayout_5.addWidget(self.curpstatus)


        self.gridLayout.addLayout(self.verticalLayout_5, 5, 0, 1, 1)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.espacio10 = QSpacerItem(10, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.espacio10)

        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMaximumSize(QSize(200, 20))
        palette2 = QPalette()
        palette2.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText, brush)
        palette2.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Text, brush)
        palette2.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.ButtonText, brush)
        palette2.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.WindowText, brush)
        palette2.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Text, brush)
        palette2.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.ButtonText, brush)
        palette2.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, brush1)
        palette2.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, brush1)
        palette2.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, brush1)
        self.label_3.setPalette(palette2)
        self.label_3.setFont(font3)

        self.horizontalLayout_5.addWidget(self.label_3)

        self.textofechanacimiento = QTextEdit(self.centralwidget)
        self.textofechanacimiento.setObjectName(u"textofechanacimiento")
        self.textofechanacimiento.setMaximumSize(QSize(500, 40))

        self.horizontalLayout_5.addWidget(self.textofechanacimiento)

        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setMaximumSize(QSize(40, 40))
        icon = QIcon()
        icon.addFile(u"../assets/calendario.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton.setIcon(icon)

        self.horizontalLayout_5.addWidget(self.pushButton)

        self.espacio9 = QSpacerItem(10, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.espacio9)


        self.gridLayout.addLayout(self.horizontalLayout_5, 6, 0, 1, 2)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMaximumSize(QSize(200, 20))
        palette3 = QPalette()
        palette3.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText, brush)
        palette3.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Text, brush)
        palette3.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.ButtonText, brush)
        palette3.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.WindowText, brush)
        palette3.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Text, brush)
        palette3.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.ButtonText, brush)
        palette3.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, brush1)
        palette3.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, brush1)
        palette3.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, brush1)
        self.label_4.setPalette(palette3)
        self.label_4.setFont(font3)

        self.verticalLayout_2.addWidget(self.label_4)

        self.fotoimagen = QLabel(self.centralwidget)
        self.fotoimagen.setObjectName(u"fotoimagen")
        self.fotoimagen.setMaximumSize(QSize(200, 200))

        self.verticalLayout_2.addWidget(self.fotoimagen)


        self.gridLayout.addLayout(self.verticalLayout_2, 7, 0, 1, 1)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.espacio11 = QSpacerItem(10, 25, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout_4.addItem(self.espacio11)

        self.botonsubir = QPushButton(self.centralwidget)
        self.botonsubir.setObjectName(u"botonsubir")
        self.botonsubir.setMaximumSize(QSize(120, 30))

        self.verticalLayout_4.addWidget(self.botonsubir)

        self.botontomar = QPushButton(self.centralwidget)
        self.botontomar.setObjectName(u"botontomar")
        self.botontomar.setMaximumSize(QSize(120, 30))
        palette4 = QPalette()
        brush2 = QBrush(QColor(62, 58, 50, 255))
        brush2.setStyle(Qt.BrushStyle.SolidPattern)
        palette4.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText, brush2)
        brush3 = QBrush(QColor(244, 196, 48, 255))
        brush3.setStyle(Qt.BrushStyle.SolidPattern)
        palette4.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Button, brush3)
        palette4.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Text, brush2)
        palette4.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.ButtonText, brush2)
        palette4.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Base, brush3)
        palette4.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Window, brush3)
        palette4.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.WindowText, brush2)
        palette4.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Button, brush3)
        palette4.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Text, brush2)
        palette4.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.ButtonText, brush2)
        palette4.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Base, brush3)
        palette4.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Window, brush3)
        palette4.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, brush2)
        palette4.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Button, brush3)
        palette4.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, brush2)
        palette4.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, brush2)
        palette4.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Base, brush3)
        palette4.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Window, brush3)
        self.botontomar.setPalette(palette4)

        self.verticalLayout_4.addWidget(self.botontomar)

        self.espacio12 = QSpacerItem(10, 25, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout_4.addItem(self.espacio12)


        self.gridLayout.addLayout(self.verticalLayout_4, 7, 1, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.espacio1 = QSpacerItem(150, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.espacio1)

        self.botonguardar = QPushButton(self.centralwidget)
        self.botonguardar.setObjectName(u"botonguardar")
        self.botonguardar.setMaximumSize(QSize(300, 16777215))
        font5 = QFont()
        font5.setFamilies([u"Arial"])
        font5.setPointSize(11)
        font5.setBold(True)
        font5.setItalic(False)
        self.botonguardar.setFont(font5)

        self.horizontalLayout.addWidget(self.botonguardar)

        self.espacio2 = QSpacerItem(150, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.espacio2)


        self.gridLayout.addLayout(self.horizontalLayout, 8, 0, 1, 3)

        AltaWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(AltaWindow)

        QMetaObject.connectSlotsByName(AltaWindow)
    # setupUi

    def retranslateUi(self, AltaWindow):
        AltaWindow.setWindowTitle(QCoreApplication.translate("AltaWindow", u"RUMSA | Dar de alta", None))
        self.botonregresar.setText(QCoreApplication.translate("AltaWindow", u"\u21e6", None))
        self.usuario.setText(QCoreApplication.translate("AltaWindow", u"Usuario", None))
        self.labelBrand.setText(QCoreApplication.translate("AltaWindow", u"RUMSA", None))
        self.labelCompany.setText(QCoreApplication.translate("AltaWindow", u"Rutas Urbanas de Matehuala, S.A. de C.V.", None))
        self.labelHeaderInfo.setText(QCoreApplication.translate("AltaWindow", u"M\u00f3dulo de altas", None))
#if QT_CONFIG(tooltip)
        self.labelEstadoConexion.setToolTip(QCoreApplication.translate("AltaWindow", u"Este texto puede cambiar a: Conectando, Sin conexi\u00f3n, Sincronizando o Conectado.", None))
#endif // QT_CONFIG(tooltip)
        self.labelEstadoConexion.setText(QCoreApplication.translate("AltaWindow", u"\u25cf Conectando", None))
        self.mensajeInternet.setText("")
        self.label.setText(QCoreApplication.translate("AltaWindow", u"Dar de Alta Tarjeta", None))
        self.otrosdatos.setText(QCoreApplication.translate("AltaWindow", u"Tipo de Tarjeta", None))
        self.normal.setText(QCoreApplication.translate("AltaWindow", u"Normal", None))
        self.preferencial.setText(QCoreApplication.translate("AltaWindow", u"Preferencial", None))
        self.vigencia.setText(QCoreApplication.translate("AltaWindow", u"Vigencia", None))
        self.nombre.setText(QCoreApplication.translate("AltaWindow", u"Nombre", None))
        self.label_2.setText(QCoreApplication.translate("AltaWindow", u"Curp", None))
        self.curpstatus.setText(QCoreApplication.translate("AltaWindow", u"Curp", None))
        self.label_3.setText(QCoreApplication.translate("AltaWindow", u"Fecha Nacimineto", None))
        self.pushButton.setText("")
        self.label_4.setText(QCoreApplication.translate("AltaWindow", u"Foto", None))
        self.fotoimagen.setText(QCoreApplication.translate("AltaWindow", u"foto imagen", None))
        self.botonsubir.setText(QCoreApplication.translate("AltaWindow", u"Seleccionar", None))
        self.botontomar.setText(QCoreApplication.translate("AltaWindow", u"Cancelar", None))
        self.botonguardar.setText(QCoreApplication.translate("AltaWindow", u"Guardar", None))
    # retranslateUi

