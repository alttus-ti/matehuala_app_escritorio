from PySide6.QtCore import (QCoreApplication,QMetaObject, QSize, Qt)
from PySide6.QtGui import (QFont)
from PySide6.QtWidgets import (QFrame, QGridLayout, QHBoxLayout,
    QLabel, QPushButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class EmpleadoWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(580, 470)
        self.centralwidget = QWidget(MainWindow)
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
"QPushButton#botonrecarga {\n"
"    min-width: 220px;\n"
"    min-height: 54px;\n"
"    font: 700 12pt \"Arial\";\n"
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

        self.rumsaSpacer_empleado = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout.addItem(self.rumsaSpacer_empleado)

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setFamilies([u"Arial"])
        font.setPointSize(18)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setMaximumSize(QSize(16777215, 16777215))
        self.label.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label)


        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.espacio1 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.espacio1)

        self.botonrecarga = QPushButton(self.centralwidget)
        self.botonrecarga.setObjectName(u"botonrecarga")
        font1 = QFont()
        font1.setPointSize(12)
        self.botonrecarga.setFont(font1)

        self.horizontalLayout.addWidget(self.botonrecarga)

        self.espacio2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.espacio2)


        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"RUMSA | Empleado", None))
        self.labelBrand.setText(QCoreApplication.translate("MainWindow", u"RUMSA", None))
        self.labelCompany.setText(QCoreApplication.translate("MainWindow", u"Rutas Urbanas de Matehuala, S.A. de C.V.", None))
        self.labelHeaderInfo.setText(QCoreApplication.translate("MainWindow", u"Rutas Urbanas de Matehuala", None))
        self.labelEstadoConexion.setText(QCoreApplication.translate("MainWindow", u"\u25cf Conectando", None))
#if QT_CONFIG(tooltip)
        self.labelEstadoConexion.setToolTip(QCoreApplication.translate("MainWindow", u"Este texto puede cambiar a: Conectando, Sin conexi\u00f3n, Sincronizando o Conectado.", None))
#endif // QT_CONFIG(tooltip)
        self.label.setText(QCoreApplication.translate("MainWindow", u"Men\u00fa principal", None))
        self.botonrecarga.setText(QCoreApplication.translate("MainWindow", u"Recargar", None))
    # retranslateUi

