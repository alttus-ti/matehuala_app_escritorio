from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QGridLayout,
    QHBoxLayout, QLabel, QLineEdit, QMainWindow,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class RecargaWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(506, 443)
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
"QPushButton#botonrecargar {\n"
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
"    font: 700 8pt \"Arial\""
                        ";\n"
"}\n"
"")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_4)

        self.comboBox = QComboBox(self.centralwidget)
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setMaximumSize(QSize(300, 40))

        self.horizontalLayout_4.addWidget(self.comboBox)

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")

        self.horizontalLayout_4.addWidget(self.label)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_3)


        self.gridLayout.addLayout(self.horizontalLayout_4, 1, 0, 1, 3)

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

        self.rumsaSpacer_recarga = QSpacerItem(20, 8, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout.addItem(self.rumsaSpacer_recarga)

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


        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 3)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")

        self.gridLayout.addLayout(self.verticalLayout_5, 2, 0, 1, 1)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.otrosdatos = QLabel(self.centralwidget)
        self.otrosdatos.setObjectName(u"otrosdatos")
        self.otrosdatos.setMaximumSize(QSize(200, 20))
        self.otrosdatos.setFont(font)
        self.otrosdatos.setAlignment(Qt.AlignCenter)

        self.verticalLayout_2.addWidget(self.otrosdatos)

        self.espacio6 = QSpacerItem(5, 5, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout_2.addItem(self.espacio6)

        self.uid = QLabel(self.centralwidget)
        self.uid.setObjectName(u"uid")
        self.uid.setMaximumSize(QSize(200, 20))
        self.uid.setFont(font)
        self.uid.setAlignment(Qt.AlignCenter)

        self.verticalLayout_2.addWidget(self.uid)

        self.texto4 = QLabel(self.centralwidget)
        self.texto4.setObjectName(u"texto4")
        self.texto4.setMaximumSize(QSize(200, 20))
        font1 = QFont()
        font1.setFamilies([u"Arial"])
        font1.setPointSize(10)
        font1.setBold(False)
        font1.setItalic(False)
        self.texto4.setFont(font1)
        self.texto4.setAlignment(Qt.AlignCenter)

        self.verticalLayout_2.addWidget(self.texto4)

        self.nombre = QLabel(self.centralwidget)
        self.nombre.setObjectName(u"nombre")
        self.nombre.setMaximumSize(QSize(200, 20))
        self.nombre.setFont(font)
        self.nombre.setAlignment(Qt.AlignCenter)

        self.verticalLayout_2.addWidget(self.nombre)

        self.texto5 = QLabel(self.centralwidget)
        self.texto5.setObjectName(u"texto5")
        self.texto5.setMaximumSize(QSize(200, 20))
        self.texto5.setFont(font1)
        self.texto5.setAlignment(Qt.AlignCenter)

        self.verticalLayout_2.addWidget(self.texto5)

        self.tarjeta = QLabel(self.centralwidget)
        self.tarjeta.setObjectName(u"tarjeta")
        self.tarjeta.setMaximumSize(QSize(200, 20))
        self.tarjeta.setFont(font)
        self.tarjeta.setAlignment(Qt.AlignCenter)

        self.verticalLayout_2.addWidget(self.tarjeta)

        self.texto6 = QLabel(self.centralwidget)
        self.texto6.setObjectName(u"texto6")
        self.texto6.setMaximumSize(QSize(200, 20))
        self.texto6.setFont(font1)
        self.texto6.setAlignment(Qt.AlignCenter)

        self.verticalLayout_2.addWidget(self.texto6)


        self.gridLayout.addLayout(self.verticalLayout_2, 2, 1, 5, 2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.espacio4 = QSpacerItem(13, 13, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.espacio4)

        self.signopeso3 = QLabel(self.centralwidget)
        self.signopeso3.setObjectName(u"signopeso3")
        font2 = QFont()
        font2.setFamilies([u"Arial"])
        font2.setPointSize(16)
        font2.setBold(True)
        font2.setItalic(False)
        self.signopeso3.setFont(font2)

        self.horizontalLayout_3.addWidget(self.signopeso3)

        self.lineEdit = QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setMaximumSize(QSize(300, 40))
        self.lineEdit.setInputMethodHints(Qt.ImhNone)
        self.lineEdit.setDragEnabled(False)

        self.horizontalLayout_3.addWidget(self.lineEdit)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.botonrecargar = QPushButton(self.centralwidget)
        self.botonrecargar.setObjectName(u"botonrecargar")
        font3 = QFont()
        font3.setFamilies([u"Arial"])
        font3.setPointSize(11)
        font3.setBold(True)
        font3.setItalic(False)
        self.botonrecargar.setFont(font3)

        self.horizontalLayout_3.addWidget(self.botonrecargar)

        self.espacio3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.espacio3)


        self.gridLayout.addLayout(self.horizontalLayout_3, 4, 0, 1, 1)

        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")

        self.gridLayout.addLayout(self.verticalLayout_6, 5, 0, 1, 1)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.texto7 = QLabel(self.centralwidget)
        self.texto7.setObjectName(u"texto7")
        self.texto7.setMaximumSize(QSize(900, 20))
        self.texto7.setFont(font1)
        self.texto7.setAlignment(Qt.AlignCenter)

        self.verticalLayout_4.addWidget(self.texto7)


        self.gridLayout.addLayout(self.verticalLayout_4, 7, 0, 1, 3)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.espacio2 = QSpacerItem(10, 10, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.espacio2)

        self.saldo = QLabel(self.centralwidget)
        self.saldo.setObjectName(u"saldo")
        self.saldo.setFont(font)

        self.horizontalLayout.addWidget(self.saldo)

        self.signopeso = QLabel(self.centralwidget)
        self.signopeso.setObjectName(u"signopeso")
        self.signopeso.setMaximumSize(QSize(15, 16777215))
        self.signopeso.setFont(font2)

        self.horizontalLayout.addWidget(self.signopeso)

        self.texto1 = QLabel(self.centralwidget)
        self.texto1.setObjectName(u"texto1")
        self.texto1.setFont(font1)

        self.horizontalLayout.addWidget(self.texto1)

        self.espacio1 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.espacio1)


        self.gridLayout.addLayout(self.horizontalLayout, 3, 0, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.saldonuevo = QLabel(self.centralwidget)
        self.saldonuevo.setObjectName(u"saldonuevo")
        self.saldonuevo.setMaximumSize(QSize(110, 16777215))
        self.saldonuevo.setFont(font)

        self.horizontalLayout_2.addWidget(self.saldonuevo)

        self.signopeso2 = QLabel(self.centralwidget)
        self.signopeso2.setObjectName(u"signopeso2")
        self.signopeso2.setMaximumSize(QSize(15, 16777215))
        self.signopeso2.setFont(font2)

        self.horizontalLayout_2.addWidget(self.signopeso2)

        self.texto2 = QLabel(self.centralwidget)
        self.texto2.setObjectName(u"texto2")
        self.texto2.setMaximumSize(QSize(110, 16777215))
        self.texto2.setFont(font1)

        self.horizontalLayout_2.addWidget(self.texto2)

        self.horizontalSpacer_2 = QSpacerItem(150, 30, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)


        self.gridLayout.addLayout(self.horizontalLayout_2, 6, 0, 1, 2)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"RUMSA | Recarga", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Recargar Tarjeta", None))
        self.botonregresar.setText(QCoreApplication.translate("MainWindow", u"\u21e6", None))
        self.labelBrand.setText(QCoreApplication.translate("MainWindow", u"RUMSA", None))
        self.labelCompany.setText(QCoreApplication.translate("MainWindow", u"Rutas Urbanas de Matehuala, S.A. de C.V.", None))
        self.labelHeaderInfo.setText(QCoreApplication.translate("MainWindow", u"M\u00f3dulo de recargas", None))
#if QT_CONFIG(tooltip)
        self.labelEstadoConexion.setToolTip(QCoreApplication.translate("MainWindow", u"Este texto puede cambiar a: Conectando, Sin conexi\u00f3n, Sincronizando o Conectado.", None))
#endif // QT_CONFIG(tooltip)
        self.labelEstadoConexion.setText(QCoreApplication.translate("MainWindow", u"\u25cf Conectando", None))
        self.otrosdatos.setText(QCoreApplication.translate("MainWindow", u"Otros Datos", None))
        self.uid.setText(QCoreApplication.translate("MainWindow", u"UID", None))
        self.texto4.setText(QCoreApplication.translate("MainWindow", u"Texto", None))
        self.nombre.setText(QCoreApplication.translate("MainWindow", u"Nombre", None))
        self.texto5.setText(QCoreApplication.translate("MainWindow", u"Texto", None))
        self.tarjeta.setText(QCoreApplication.translate("MainWindow", u"Tipo de Tarjeta", None))
        self.texto6.setText(QCoreApplication.translate("MainWindow", u"Texto", None))
        self.signopeso3.setText(QCoreApplication.translate("MainWindow", u"$", None))
        self.lineEdit.setInputMask("")
        self.botonrecargar.setText(QCoreApplication.translate("MainWindow", u"Recargar", None))
        self.texto7.setText(QCoreApplication.translate("MainWindow", u"Texto", None))
        self.saldo.setText(QCoreApplication.translate("MainWindow", u"Saldo", None))
        self.signopeso.setText(QCoreApplication.translate("MainWindow", u"$", None))
        self.texto1.setText(QCoreApplication.translate("MainWindow", u"texto", None))
        self.saldonuevo.setText(QCoreApplication.translate("MainWindow", u"Saldo Nuevo", None))
        self.signopeso2.setText(QCoreApplication.translate("MainWindow", u"$", None))
        self.texto2.setText(QCoreApplication.translate("MainWindow", u"texto", None))
    # retranslateUi

