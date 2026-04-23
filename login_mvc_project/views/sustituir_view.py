from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCalendarWidget, QComboBox, QGridLayout,
    QHBoxLayout, QLabel, QLineEdit, QMainWindow,
    QPushButton, QSizePolicy, QSpacerItem, QTextBrowser,
    QVBoxLayout, QWidget)

class SustituirWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(662, 538)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.botonregresar = QPushButton(self.centralwidget)
        self.botonregresar.setObjectName(u"botonregresar")
        self.botonregresar.setMaximumSize(QSize(35, 30))
        font = QFont()
        font.setPointSize(30)
        self.botonregresar.setFont(font)

        self.horizontalLayout_4.addWidget(self.botonregresar)

        self.espacio1 = QSpacerItem(700, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.espacio1)


        self.gridLayout.addLayout(self.horizontalLayout_4, 0, 0, 1, 2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.lista = QComboBox(self.centralwidget)
        self.lista.setObjectName(u"lista")
        self.lista.setMaximumSize(QSize(150, 20))

        self.horizontalLayout.addWidget(self.lista)

        self.sustituirtarjeta = QLabel(self.centralwidget)
        self.sustituirtarjeta.setObjectName(u"sustituirtarjeta")
        self.sustituirtarjeta.setMaximumSize(QSize(200, 25))
        font1 = QFont()
        font1.setFamilies([u"MS Sans Serif"])
        font1.setPointSize(14)
        font1.setBold(True)
        self.sustituirtarjeta.setFont(font1)
        self.sustituirtarjeta.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.sustituirtarjeta)

        self.espacio2 = QSpacerItem(150, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.espacio2)


        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 2)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.espacio4 = QSpacerItem(40, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.espacio4)

        self.buscador = QLineEdit(self.centralwidget)
        self.buscador.setObjectName(u"buscador")
        self.buscador.setMaximumSize(QSize(350, 30))

        self.horizontalLayout_2.addWidget(self.buscador)

        self.espacio3 = QSpacerItem(40, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.espacio3)


        self.gridLayout.addLayout(self.horizontalLayout_2, 2, 0, 1, 2)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.nombre = QLabel(self.centralwidget)
        self.nombre.setObjectName(u"nombre")
        self.nombre.setMaximumSize(QSize(100, 20))
        font2 = QFont()
        font2.setFamilies([u"MS Sans Serif"])
        font2.setPointSize(12)
        font2.setBold(True)
        self.nombre.setFont(font2)

        self.verticalLayout.addWidget(self.nombre)

        self.textonombre = QTextBrowser(self.centralwidget)
        self.textonombre.setObjectName(u"textonombre")
        self.textonombre.setMaximumSize(QSize(300, 30))

        self.verticalLayout.addWidget(self.textonombre)

        self.uid = QLabel(self.centralwidget)
        self.uid.setObjectName(u"uid")
        self.uid.setMaximumSize(QSize(600, 20))
        self.uid.setFont(font2)

        self.verticalLayout.addWidget(self.uid)

        self.textouid = QLabel(self.centralwidget)
        self.textouid.setObjectName(u"textouid")
        self.textouid.setMaximumSize(QSize(100, 20))
        font3 = QFont()
        font3.setFamilies([u"MS Sans Serif"])
        font3.setPointSize(10)
        font3.setBold(False)
        self.textouid.setFont(font3)

        self.verticalLayout.addWidget(self.textouid)

        self.tipo = QLabel(self.centralwidget)
        self.tipo.setObjectName(u"tipo")
        self.tipo.setMaximumSize(QSize(600, 20))
        self.tipo.setFont(font2)

        self.verticalLayout.addWidget(self.tipo)

        self.tipotarjeta = QLabel(self.centralwidget)
        self.tipotarjeta.setObjectName(u"tipotarjeta")
        self.tipotarjeta.setMaximumSize(QSize(100, 20))
        self.tipotarjeta.setFont(font3)

        self.verticalLayout.addWidget(self.tipotarjeta)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout.addItem(self.verticalSpacer_2)


        self.gridLayout.addLayout(self.verticalLayout, 3, 0, 1, 1)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.vigencia = QLabel(self.centralwidget)
        self.vigencia.setObjectName(u"vigencia")
        self.vigencia.setMaximumSize(QSize(100, 20))
        self.vigencia.setFont(font2)

        self.verticalLayout_2.addWidget(self.vigencia)

        self.textovigencia = QTextBrowser(self.centralwidget)
        self.textovigencia.setObjectName(u"textovigencia")
        self.textovigencia.setMaximumSize(QSize(200, 30))

        self.verticalLayout_2.addWidget(self.textovigencia)

        self.calendario = QCalendarWidget(self.centralwidget)
        self.calendario.setObjectName(u"calendario")
        self.calendario.setMaximumSize(QSize(380, 280))

        self.verticalLayout_2.addWidget(self.calendario)


        self.gridLayout.addLayout(self.verticalLayout_2, 3, 1, 1, 1)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.botonsustituir = QPushButton(self.centralwidget)
        self.botonsustituir.setObjectName(u"botonsustituir")
        self.botonsustituir.setMaximumSize(QSize(200, 30))

        self.horizontalLayout_3.addWidget(self.botonsustituir)


        self.gridLayout.addLayout(self.horizontalLayout_3, 4, 0, 1, 2)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Sustituir Trarjeta", None))
        self.botonregresar.setText(QCoreApplication.translate("MainWindow", u"\u21e6", None))
        self.sustituirtarjeta.setText(QCoreApplication.translate("MainWindow", u"Sustituir Tarjeta", None))
        self.nombre.setText(QCoreApplication.translate("MainWindow", u"Nombre", None))
        self.uid.setText(QCoreApplication.translate("MainWindow", u"UID", None))
        self.textouid.setText(QCoreApplication.translate("MainWindow", u"uid", None))
        self.tipo.setText(QCoreApplication.translate("MainWindow", u"Tipo de Tarjeta", None))
        self.tipotarjeta.setText(QCoreApplication.translate("MainWindow", u"Tipo de tarjeta", None))
        self.vigencia.setText(QCoreApplication.translate("MainWindow", u"Vigencia", None))
        self.botonsustituir.setText(QCoreApplication.translate("MainWindow", u"Sustituir", None))
    # retranslateUi

