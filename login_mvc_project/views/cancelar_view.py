from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QGridLayout,
    QHBoxLayout, QLabel, QMainWindow, QPlainTextEdit,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class CancelarWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(642, 478)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.botonregresar = QPushButton(self.centralwidget)
        self.botonregresar.setObjectName(u"botonregresar")
        self.botonregresar.setMaximumSize(QSize(35, 30))
        font = QFont()
        font.setPointSize(30)
        self.botonregresar.setFont(font)

        self.verticalLayout.addWidget(self.botonregresar)


        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.puerto = QComboBox(self.centralwidget)
        self.puerto.setObjectName(u"puerto")
        self.puerto.setMaximumSize(QSize(200, 50))

        self.horizontalLayout.addWidget(self.puerto)

        self.textocancelar = QLabel(self.centralwidget)
        self.textocancelar.setObjectName(u"textocancelar")
        self.textocancelar.setMaximumSize(QSize(180, 30))
        font1 = QFont()
        font1.setPointSize(14)
        font1.setBold(True)
        self.textocancelar.setFont(font1)

        self.horizontalLayout.addWidget(self.textocancelar)


        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 2)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.espacio4 = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout_2.addItem(self.espacio4)

        self.nombre = QLabel(self.centralwidget)
        self.nombre.setObjectName(u"nombre")
        self.nombre.setMaximumSize(QSize(450, 20))
        font2 = QFont()
        font2.setFamilies([u"MS Sans Serif"])
        font2.setPointSize(12)
        font2.setBold(True)
        font2.setItalic(True)
        self.nombre.setFont(font2)

        self.verticalLayout_2.addWidget(self.nombre)

        self.textonombre = QPlainTextEdit(self.centralwidget)
        self.textonombre.setObjectName(u"textonombre")
        self.textonombre.setMaximumSize(QSize(300, 40))

        self.verticalLayout_2.addWidget(self.textonombre)

        self.espacio3 = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout_2.addItem(self.espacio3)

        self.uid = QLabel(self.centralwidget)
        self.uid.setObjectName(u"uid")
        self.uid.setMaximumSize(QSize(450, 20))
        self.uid.setFont(font2)

        self.verticalLayout_2.addWidget(self.uid)

        self.textouid = QLabel(self.centralwidget)
        self.textouid.setObjectName(u"textouid")
        self.textouid.setMaximumSize(QSize(450, 20))
        font3 = QFont()
        font3.setFamilies([u"MS Sans Serif"])
        font3.setPointSize(12)
        font3.setBold(False)
        font3.setItalic(True)
        self.textouid.setFont(font3)

        self.verticalLayout_2.addWidget(self.textouid)

        self.listanegra = QCheckBox(self.centralwidget)
        self.listanegra.setObjectName(u"listanegra")
        font4 = QFont()
        font4.setFamilies([u"MS Shell Dlg 2"])
        font4.setPointSize(10)
        font4.setBold(False)
        font4.setItalic(False)
        self.listanegra.setFont(font4)

        self.verticalLayout_2.addWidget(self.listanegra)

        self.espaio5 = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout_2.addItem(self.espaio5)


        self.gridLayout.addLayout(self.verticalLayout_2, 2, 0, 1, 1)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.espacio2 = QSpacerItem(100, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.espacio2)

        self.botoncancelar = QPushButton(self.centralwidget)
        self.botoncancelar.setObjectName(u"botoncancelar")
        self.botoncancelar.setMaximumSize(QSize(150, 35))

        self.horizontalLayout_4.addWidget(self.botoncancelar)

        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setMaximumSize(QSize(150, 35))

        self.horizontalLayout_4.addWidget(self.pushButton)

        self.espacio1 = QSpacerItem(100, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.espacio1)


        self.gridLayout.addLayout(self.horizontalLayout_4, 3, 0, 1, 2)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.espacio4_2 = QSpacerItem(20, 60, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout_3.addItem(self.espacio4_2)

        self.motivo = QLabel(self.centralwidget)
        self.motivo.setObjectName(u"motivo")
        self.motivo.setMaximumSize(QSize(450, 20))
        self.motivo.setFont(font2)

        self.verticalLayout_3.addWidget(self.motivo)

        self.textomotivo = QPlainTextEdit(self.centralwidget)
        self.textomotivo.setObjectName(u"textomotivo")
        self.textomotivo.setMaximumSize(QSize(250, 125))

        self.verticalLayout_3.addWidget(self.textomotivo)

        self.espacio4_3 = QSpacerItem(40, 60, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout_3.addItem(self.espacio4_3)


        self.gridLayout.addLayout(self.verticalLayout_3, 2, 1, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Cancelar", None))
        self.botonregresar.setText(QCoreApplication.translate("MainWindow", u"\u21e6", None))
        self.textocancelar.setText(QCoreApplication.translate("MainWindow", u"Cancelar Tarjeta", None))
        self.nombre.setText(QCoreApplication.translate("MainWindow", u"Nombre", None))
        self.uid.setText(QCoreApplication.translate("MainWindow", u"UID", None))
        self.textouid.setText(QCoreApplication.translate("MainWindow", u"UID", None))
        self.listanegra.setText(QCoreApplication.translate("MainWindow", u"Lista Negra", None))
        self.botoncancelar.setText(QCoreApplication.translate("MainWindow", u"Cancelar Tarjeta", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Reactivar Tarjeta", None))
        self.motivo.setText(QCoreApplication.translate("MainWindow", u"Motivo", None))
    # retranslateUi

