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
    QTextEdit, QVBoxLayout, QWidget)

class AltaWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(652, 657)
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
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.botonregresar = QPushButton(self.centralwidget)
        self.botonregresar.setObjectName(u"botonregresar")
        self.botonregresar.setMaximumSize(QSize(35, 30))
        font = QFont()
        font.setFamilies([u"Arial"])
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(False)
        self.botonregresar.setFont(font)

        self.verticalLayout.addWidget(self.botonregresar)

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


        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 2)

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


        self.gridLayout.addLayout(self.horizontalLayout_2, 2, 0, 1, 1)

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


        self.gridLayout.addLayout(self.horizontalLayout_3, 1, 0, 1, 2)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.otrosdatos = QLabel(self.centralwidget)
        self.otrosdatos.setObjectName(u"otrosdatos")
        self.otrosdatos.setMaximumSize(QSize(200, 20))
        self.otrosdatos.setFont(font)
        self.otrosdatos.setAlignment(Qt.AlignCenter)

        self.verticalLayout_3.addWidget(self.otrosdatos)

        self.normal = QRadioButton(self.centralwidget)
        self.normal.setObjectName(u"normal")
        font1 = QFont()
        font1.setFamilies([u"Arial"])
        font1.setPointSize(10)
        font1.setBold(False)
        font1.setItalic(False)
        self.normal.setFont(font1)

        self.verticalLayout_3.addWidget(self.normal)

        self.preferencial = QRadioButton(self.centralwidget)
        self.preferencial.setObjectName(u"preferencial")
        self.preferencial.setFont(font1)

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

        self.verticalLayout_3.addWidget(self.calendario)

        self.espacio5 = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout_3.addItem(self.espacio5)


        self.gridLayout.addLayout(self.verticalLayout_3, 2, 1, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.espacio1 = QSpacerItem(150, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.espacio1)

        self.botonguardar = QPushButton(self.centralwidget)
        self.botonguardar.setObjectName(u"botonguardar")
        self.botonguardar.setMaximumSize(QSize(300, 16777215))
        font2 = QFont()
        font2.setFamilies([u"Arial"])
        font2.setPointSize(11)
        font2.setBold(True)
        font2.setItalic(False)
        self.botonguardar.setFont(font2)

        self.horizontalLayout.addWidget(self.botonguardar)

        self.espacio2 = QSpacerItem(150, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.espacio2)


        self.gridLayout.addLayout(self.horizontalLayout, 4, 0, 1, 2)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"RUMSA | Dar de alta", None))
        self.botonregresar.setText(QCoreApplication.translate("MainWindow", u"\u21e6", None))
        self.labelBrand.setText(QCoreApplication.translate("MainWindow", u"RUMSA", None))
        self.labelCompany.setText(QCoreApplication.translate("MainWindow", u"Rutas Urbanas de Matehuala, S.A. de C.V.", None))
        self.labelHeaderInfo.setText(QCoreApplication.translate("MainWindow", u"M\u00f3dulo de altas", None))
#if QT_CONFIG(tooltip)
        self.labelEstadoConexion.setToolTip(QCoreApplication.translate("MainWindow", u"Este texto puede cambiar a: Conectando, Sin conexi\u00f3n, Sincronizando o Conectado.", None))
#endif // QT_CONFIG(tooltip)
        self.labelEstadoConexion.setText(QCoreApplication.translate("MainWindow", u"\u25cf Conectando", None))
        self.nombre.setText(QCoreApplication.translate("MainWindow", u"Nombre", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Dar de Alta Tarjeta", None))
        self.otrosdatos.setText(QCoreApplication.translate("MainWindow", u"Tipo de Tarjeta", None))
        self.normal.setText(QCoreApplication.translate("MainWindow", u"Normal", None))
        self.preferencial.setText(QCoreApplication.translate("MainWindow", u"Preferencial", None))
        self.vigencia.setText(QCoreApplication.translate("MainWindow", u"Vigencia", None))
        self.botonguardar.setText(QCoreApplication.translate("MainWindow", u"Guardar", None))
    # retranslateUi

