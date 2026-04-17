from PySide6.QtCore import (QCoreApplication,QMetaObject, Qt)
from PySide6.QtGui import (QFont)
from PySide6.QtWidgets import (QFrame, QGridLayout, QLabel,
    QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class AdminWindow(object):
    def setupUi(self, mainWindow):
        if not mainWindow.objectName():
            mainWindow.setObjectName(u"mainWindow")
        mainWindow.resize(571, 399)
        self.centralwidget = QWidget(mainWindow)
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
"QPushButton#botonrecarga, QPushButton#botonalta, QPushButton#botonsustituir, QPushButton#botoncancelar {\n"
"    min-width: 120px;\n"
"    min-height: 46px;\n"
"    font: 700 11pt \"Arial\";\n"
"}\n"
"QLabel#labelEstadoConexion {\n"
"    background-color: #FFF7D6;\n"
"    color: #245E91;\n"
"    border: 1px solid #F0C247;\n"
"    bo"
                        "rder-radius: 10px;\n"
"    padding: 4px 10px;\n"
"    font: 700 8pt \"Arial\";\n"
"}\n"
"")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
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


        self.verticalLayout.addWidget(self.frameHeader)

        self.rumsaSpacer_menu = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout.addItem(self.rumsaSpacer_menu)

        self.menu = QLabel(self.centralwidget)
        self.menu.setObjectName(u"menu")
        font = QFont()
        font.setFamilies([u"Arial"])
        font.setPointSize(18)
        font.setBold(True)
        self.menu.setFont(font)
        self.menu.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.menu)


        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.verticalSpacer = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.gridLayout_2.addItem(self.verticalSpacer, 2, 1, 1, 1)

        self.botonrecarga = QPushButton(self.centralwidget)
        self.botonrecarga.setObjectName(u"botonrecarga")

        self.gridLayout_2.addWidget(self.botonrecarga, 1, 3, 1, 1)

        self.botonalta = QPushButton(self.centralwidget)
        self.botonalta.setObjectName(u"botonalta")

        self.gridLayout_2.addWidget(self.botonalta, 1, 1, 1, 1)

        self.botoncancelar = QPushButton(self.centralwidget)
        self.botoncancelar.setObjectName(u"botoncancelar")

        self.gridLayout_2.addWidget(self.botoncancelar, 1, 4, 1, 1)

        self.botonsustituir = QPushButton(self.centralwidget)
        self.botonsustituir.setObjectName(u"botonsustituir")

        self.gridLayout_2.addWidget(self.botonsustituir, 1, 2, 1, 1)

        self.espacio1 = QSpacerItem(10, 10, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.espacio1, 1, 0, 1, 1)

        self.espacio2 = QSpacerItem(10, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.espacio2, 1, 5, 1, 1)

        self.verticalSpacer_3 = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.gridLayout_2.addItem(self.verticalSpacer_3, 2, 3, 1, 1)

        self.verticalSpacer_4 = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.gridLayout_2.addItem(self.verticalSpacer_4, 2, 4, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.gridLayout_2.addItem(self.verticalSpacer_2, 2, 2, 1, 1)

        self.verticalSpacer_5 = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.gridLayout_2.addItem(self.verticalSpacer_5, 0, 4, 1, 1)

        self.verticalSpacer_6 = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.gridLayout_2.addItem(self.verticalSpacer_6, 0, 3, 1, 1)

        self.verticalSpacer_7 = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.gridLayout_2.addItem(self.verticalSpacer_7, 0, 2, 1, 1)

        self.verticalSpacer_8 = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.gridLayout_2.addItem(self.verticalSpacer_8, 0, 1, 1, 1)


        self.gridLayout.addLayout(self.gridLayout_2, 1, 0, 1, 1)

        mainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(mainWindow)

        QMetaObject.connectSlotsByName(mainWindow)
    # setupUi

    def retranslateUi(self, mainWindow):
#if QT_CONFIG(accessibility)
        mainWindow.setAccessibleName("")
#endif // QT_CONFIG(accessibility)
        mainWindow.setWindowTitle(QCoreApplication.translate("mainWindow", u"RUMSA | Administrador", None))
        self.labelBrand.setText(QCoreApplication.translate("mainWindow", u"RUMSA", None))
        self.labelCompany.setText(QCoreApplication.translate("mainWindow", u"Rutas Urbanas de Matehuala, S.A. de C.V.", None))
        self.labelHeaderInfo.setText(QCoreApplication.translate("mainWindow", u"Rutas Urbanas de Matehuala", None))
        self.labelEstadoConexion.setText(QCoreApplication.translate("mainWindow", u"\u25cf Conectando", None))
#if QT_CONFIG(tooltip)
        self.labelEstadoConexion.setToolTip(QCoreApplication.translate("mainWindow", u"Este texto puede cambiar a: Conectando, Sin conexi\u00f3n, Sincronizando o Conectado.", None))
#endif // QT_CONFIG(tooltip)
        self.menu.setText(QCoreApplication.translate("mainWindow", u"Men\u00fa principal", None))
        self.botonrecarga.setText(QCoreApplication.translate("mainWindow", u"Recarga", None))
        self.botonalta.setText(QCoreApplication.translate("mainWindow", u"Alta", None))
        self.botoncancelar.setText(QCoreApplication.translate("mainWindow", u"Cancelar", None))
        self.botonsustituir.setText(QCoreApplication.translate("mainWindow", u"Sustituir", None))
    # retranslateUi

