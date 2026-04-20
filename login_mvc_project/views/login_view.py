from PySide6.QtCore import (QCoreApplication,QMetaObject,QRect,
    QSize, Qt)
from PySide6.QtWidgets import ( QCheckBox, QFormLayout, QFrame,
    QHBoxLayout, QLabel, QLineEdit,
    QMainWindow, QMenuBar, QMessageBox, QPushButton, QSizePolicy, QSpacerItem,
    QStatusBar, QVBoxLayout, QWidget)

from controllers.login_controller import LoginController


class LoginWindow(QMainWindow):
    def __init__(self, controller=None):
        super().__init__()
        self.controller = controller
        self.login_controller = LoginController()

        self.setupUi(self)
        self.pushButtonLogin.clicked.connect(self.login)
        self.pushButtonCancel.clicked.connect(self.close)
        self.pushButtonForgot.clicked.connect(self.forgot_password)
        self.lineEditUser.returnPressed.connect(self.lineEditPassword.setFocus)
        self.lineEditPassword.returnPressed.connect(self.login)

    def login(self):
        username = self.lineEditUser.text().strip()
        password = self.lineEditPassword.text().strip()

        ok, message = self.login_controller.authenticate(username, password)
        if not ok:
            QMessageBox.warning(self, "Login", message)
            return

        role = self.login_controller.get_role(username)
        if not role:
            QMessageBox.warning(self, "Login", "El usuario no tiene rol asignado.")
            return

        if self.controller is not None:
            self.controller.show_window_by_role(username, role)
        else:
            QMessageBox.information(self, "Login", "Login correcto.")

    def forgot_password(self):
        QMessageBox.information(
            self,
            "Recuperacion",
            "Aqui puedes agregar la logica de recuperacion de contrasena.",
        )

    def setupUi(self, LoginWindow):
        if not LoginWindow.objectName():
            LoginWindow.setObjectName(u"LoginWindow")
        LoginWindow.resize(560, 430)
        self.centralwidget = QWidget(LoginWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setStyleSheet(u"QWidget#centralwidget {\n"
"    background-color: #EEF3F7;\n"
"}\n"
"\n"
"QFrame#frameHeader {\n"
"    background-color: #D9ECFA;\n"
"    border: 2px solid #7FB6E6;\n"
"    border-radius: 18px;\n"
"}\n"
"\n"
"QLabel#labelBrand {\n"
"    color: #F3B21A;\n"
"    font: 700 28pt \"Arial\";\n"
"    letter-spacing: 2px;\n"
"}\n"
"\n"
"QLabel#labelCompany {\n"
"    color: #5E98CC;\n"
"    font: 700 11pt \"Arial\";\n"
"}\n"
"\n"
"QLabel#labelWelcome {\n"
"    color: #6F7E8B;\n"
"    font: 10pt \"Arial\";\n"
"}\n"
"\n"
"QLabel#labelTitle {\n"
"    color: #4979A9;\n"
"    font: 700 18pt \"Arial\";\n"
"}\n"
"\n"
"QLabel#labelSubtitle {\n"
"    color: #6B7B8C;\n"
"    font: 10pt \"Arial\";\n"
"}\n"
"\n"
"QLabel#labelUser, QLabel#labelPassword {\n"
"    color: #4979A9;\n"
"    font: 700 10pt \"Arial\";\n"
"}\n"
"\n"
"QLineEdit {\n"
"    background-color: #FFFFFF;\n"
"    border: 2px solid #B8D8F3;\n"
"    border-radius: 12px;\n"
"    padding: 8px 10px;\n"
"    color: #2E3A46;\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    border"
                        ": 2px solid #F3C623;\n"
"}\n"
"\n"
"QCheckBox {\n"
"    color: #5E6A77;\n"
"    font: 9pt \"Arial\";\n"
"}\n"
"\n"
"QPushButton#pushButtonForgot {\n"
"    color: #E2A61C;\n"
"    font: 700 9pt \"Arial\";\n"
"    border: none;\n"
"}\n"
"\n"
"QPushButton#pushButtonForgot:hover {\n"
"    color: #C98900;\n"
"}\n"
"\n"
"QPushButton#pushButtonLogin {\n"
"    background-color: #F3C623;\n"
"    color: #3D3D3D;\n"
"    border: none;\n"
"    border-radius: 12px;\n"
"    font: 700 10pt \"Arial\";\n"
"    padding: 8px 16px;\n"
"}\n"
"\n"
"QPushButton#pushButtonLogin:hover {\n"
"    background-color: #E4B61A;\n"
"}\n"
"\n"
"QPushButton#pushButtonCancel {\n"
"    background-color: #7FB6E6;\n"
"    color: #FFFFFF;\n"
"    border: none;\n"
"    border-radius: 12px;\n"
"    font: 700 10pt \"Arial\";\n"
"    padding: 8px 16px;\n"
"}\n"
"\n"
"QPushButton#pushButtonCancel:hover {\n"
"    background-color: #6AA6DA;\n"
"}")
        self.verticalLayout_main = QVBoxLayout(self.centralwidget)
        self.verticalLayout_main.setSpacing(14)
        self.verticalLayout_main.setObjectName(u"verticalLayout_main")
        self.verticalLayout_main.setContentsMargins(34, 24, 34, 24)
        self.frameHeader = QFrame(self.centralwidget)
        self.frameHeader.setObjectName(u"frameHeader")
        self.frameHeader.setFrameShape(QFrame.StyledPanel)
        self.frameHeader.setFrameShadow(QFrame.Raised)
        self.verticalLayout_header = QVBoxLayout(self.frameHeader)
        self.verticalLayout_header.setSpacing(4)
        self.verticalLayout_header.setObjectName(u"verticalLayout_header")
        self.verticalLayout_header.setContentsMargins(18, 18, 18, 18)
        self.labelBrand = QLabel(self.frameHeader)
        self.labelBrand.setObjectName(u"labelBrand")
        self.labelBrand.setAlignment(Qt.AlignCenter)

        self.verticalLayout_header.addWidget(self.labelBrand)

        self.labelCompany = QLabel(self.frameHeader)
        self.labelCompany.setObjectName(u"labelCompany")
        self.labelCompany.setAlignment(Qt.AlignCenter)
        self.labelCompany.setWordWrap(True)

        self.verticalLayout_header.addWidget(self.labelCompany)

        self.labelWelcome = QLabel(self.frameHeader)
        self.labelWelcome.setObjectName(u"labelWelcome")
        self.labelWelcome.setAlignment(Qt.AlignCenter)

        self.verticalLayout_header.addWidget(self.labelWelcome)


        self.verticalLayout_main.addWidget(self.frameHeader)

        self.verticalSpacerTop = QSpacerItem(20, 6, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_main.addItem(self.verticalSpacerTop)

        self.labelTitle = QLabel(self.centralwidget)
        self.labelTitle.setObjectName(u"labelTitle")
        self.labelTitle.setAlignment(Qt.AlignCenter)

        self.verticalLayout_main.addWidget(self.labelTitle)

        self.labelSubtitle = QLabel(self.centralwidget)
        self.labelSubtitle.setObjectName(u"labelSubtitle")
        self.labelSubtitle.setAlignment(Qt.AlignCenter)

        self.verticalLayout_main.addWidget(self.labelSubtitle)

        self.verticalSpacer1 = QSpacerItem(20, 6, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_main.addItem(self.verticalSpacer1)

        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setLabelAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.formLayout.setFormAlignment(Qt.AlignHCenter|Qt.AlignTop)
        self.formLayout.setHorizontalSpacing(14)
        self.formLayout.setVerticalSpacing(16)
        self.labelUser = QLabel(self.centralwidget)
        self.labelUser.setObjectName(u"labelUser")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.labelUser)

        self.lineEditUser = QLineEdit(self.centralwidget)
        self.lineEditUser.setObjectName(u"lineEditUser")
        self.lineEditUser.setMinimumSize(QSize(260, 38))

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.lineEditUser)

        self.labelPassword = QLabel(self.centralwidget)
        self.labelPassword.setObjectName(u"labelPassword")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.labelPassword)

        self.lineEditPassword = QLineEdit(self.centralwidget)
        self.lineEditPassword.setObjectName(u"lineEditPassword")
        self.lineEditPassword.setMinimumSize(QSize(260, 38))
        self.lineEditPassword.setEchoMode(QLineEdit.Password)

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.lineEditPassword)


        self.verticalLayout_main.addLayout(self.formLayout)

        self.horizontalLayoutOptions = QHBoxLayout()
        self.horizontalLayoutOptions.setObjectName(u"horizontalLayoutOptions")
        self.horizontalSpacerLeft = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayoutOptions.addItem(self.horizontalSpacerLeft)

        self.checkBoxRemember = QCheckBox(self.centralwidget)
        self.checkBoxRemember.setObjectName(u"checkBoxRemember")

        self.horizontalLayoutOptions.addWidget(self.checkBoxRemember)

        self.horizontalSpacerMid = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayoutOptions.addItem(self.horizontalSpacerMid)

        self.pushButtonForgot = QPushButton(self.centralwidget)
        self.pushButtonForgot.setObjectName(u"pushButtonForgot")
        self.pushButtonForgot.setFlat(True)

        self.horizontalLayoutOptions.addWidget(self.pushButtonForgot)

        self.horizontalSpacerRight = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayoutOptions.addItem(self.horizontalSpacerRight)


        self.verticalLayout_main.addLayout(self.horizontalLayoutOptions)

        self.horizontalLayoutButtons = QHBoxLayout()
        self.horizontalLayoutButtons.setObjectName(u"horizontalLayoutButtons")
        self.horizontalSpacerButtonsLeft = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayoutButtons.addItem(self.horizontalSpacerButtonsLeft)

        self.pushButtonLogin = QPushButton(self.centralwidget)
        self.pushButtonLogin.setObjectName(u"pushButtonLogin")
        self.pushButtonLogin.setMinimumSize(QSize(135, 38))

        self.horizontalLayoutButtons.addWidget(self.pushButtonLogin)

        self.pushButtonCancel = QPushButton(self.centralwidget)
        self.pushButtonCancel.setObjectName(u"pushButtonCancel")
        self.pushButtonCancel.setMinimumSize(QSize(100, 38))

        self.horizontalLayoutButtons.addWidget(self.pushButtonCancel)

        self.horizontalSpacerButtonsRight = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayoutButtons.addItem(self.horizontalSpacerButtonsRight)


        self.verticalLayout_main.addLayout(self.horizontalLayoutButtons)

        self.verticalSpacerBottom = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_main.addItem(self.verticalSpacerBottom)

        LoginWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(LoginWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 560, 22))
        LoginWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(LoginWindow)
        self.statusbar.setObjectName(u"statusbar")
        LoginWindow.setStatusBar(self.statusbar)

        self.retranslateUi(LoginWindow)

        QMetaObject.connectSlotsByName(LoginWindow)
    # setupUi

    def retranslateUi(self, LoginWindow):
        LoginWindow.setWindowTitle(QCoreApplication.translate("LoginWindow", u"RUMSA | Iniciar sesi\u00f3n", None))
        self.labelBrand.setText(QCoreApplication.translate("LoginWindow", u"RUMSA", None))
        self.labelCompany.setText(QCoreApplication.translate("LoginWindow", u"Rutas Urbanas de Matehuala, S.A. de C.V.", None))
        self.labelWelcome.setText(QCoreApplication.translate("LoginWindow", u"Acceso al sistema", None))
        self.labelTitle.setText(QCoreApplication.translate("LoginWindow", u"Iniciar sesi\u00f3n", None))
        self.labelSubtitle.setText(QCoreApplication.translate("LoginWindow", u"Ingresa tus credenciales para continuar", None))
        self.labelUser.setText(QCoreApplication.translate("LoginWindow", u"Usuario:", None))
        self.lineEditUser.setPlaceholderText(QCoreApplication.translate("LoginWindow", u"Escribe tu usuario", None))
        self.labelPassword.setText(QCoreApplication.translate("LoginWindow", u"Contrase\u00f1a:", None))
        self.lineEditPassword.setPlaceholderText(QCoreApplication.translate("LoginWindow", u"Escribe tu contrase\u00f1a", None))
        self.checkBoxRemember.setText(QCoreApplication.translate("LoginWindow", u"Recordarme", None))
        self.pushButtonForgot.setText(QCoreApplication.translate("LoginWindow", u"\u00bfOlvidaste tu contrase\u00f1a?", None))
        self.pushButtonLogin.setText(QCoreApplication.translate("LoginWindow", u"Iniciar sesi\u00f3n", None))
        self.pushButtonCancel.setText(QCoreApplication.translate("LoginWindow", u"Cancelar", None))
    # retranslateUi

