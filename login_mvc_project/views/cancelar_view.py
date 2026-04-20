from PySide6.QtCore import (QCoreApplication, QMetaObject, QSize, Qt)
from PySide6.QtGui import (QFont)
from PySide6.QtWidgets import (QComboBox, QGridLayout, QHBoxLayout,
    QLabel, QPushButton, QSizePolicy,
    QSpacerItem, QTextBrowser, QVBoxLayout, QWidget)

class CancelarWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(635, 475)
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


        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.lista = QComboBox(self.centralwidget)
        self.lista.setObjectName(u"lista")
        self.lista.setMaximumSize(QSize(150, 20))

        self.horizontalLayout.addWidget(self.lista)

        self.cancelar = QLabel(self.centralwidget)
        self.cancelar.setObjectName(u"cancelar")
        self.cancelar.setMaximumSize(QSize(200, 25))
        font1 = QFont()
        font1.setFamilies([u"MS Sans Serif"])
        font1.setPointSize(14)
        font1.setBold(True)
        self.cancelar.setFont(font1)
        self.cancelar.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.cancelar)

        self.espacio1 = QSpacerItem(150, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.espacio1)


        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.espacio2 = QSpacerItem(40, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.espacio2)

        self.textocancelar = QTextBrowser(self.centralwidget)
        self.textocancelar.setObjectName(u"textocancelar")
        self.textocancelar.setMaximumSize(QSize(500, 30))

        self.horizontalLayout_2.addWidget(self.textocancelar)

        self.espacio3 = QSpacerItem(40, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.espacio3)


        self.gridLayout.addLayout(self.horizontalLayout_2, 2, 0, 1, 1)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.botoncancelar = QPushButton(self.centralwidget)
        self.botoncancelar.setObjectName(u"botoncancelar")
        self.botoncancelar.setMaximumSize(QSize(250, 16777215))

        self.horizontalLayout_3.addWidget(self.botoncancelar)


        self.gridLayout.addLayout(self.horizontalLayout_3, 3, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Cancelar", None))
        self.botonregresar.setText(QCoreApplication.translate("MainWindow", u"\u21e6", None))
        self.cancelar.setText(QCoreApplication.translate("MainWindow", u"Cancelar Tarjeta", None))
        self.botoncancelar.setText(QCoreApplication.translate("MainWindow", u"Cancelar", None))
    # retranslateUi

