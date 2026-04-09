from PySide6.QtWidgets import QCheckBox, QLineEdit, QMainWindow, QMessageBox, QPushButton

from controllers.auth_controller import AuthController
from core.ui_loader import load_ui


class LoginWindow:
    """Ventana de login con logica de UI, similar al ejemplo de referencia."""

    def __init__(self, controller):
        self.controller = controller
        self.auth_controller = AuthController()
        self.window = load_ui("ui/login_qtdesigner.ui")

        if not isinstance(self.window, QMainWindow):
            raise RuntimeError("El archivo login_qtdesigner.ui no contiene un QMainWindow.")

        self.usuario_input = self.window.findChild(QLineEdit, "lineEditUser")
        self.contrasena_input = self.window.findChild(QLineEdit, "lineEditPassword")
        self.recordar_check = self.window.findChild(QCheckBox, "checkBoxRemember")
        self.login_button = self.window.findChild(QPushButton, "pushButtonLogin")
        self.cancel_button = self.window.findChild(QPushButton, "pushButtonCancel")
        self.forgot_button = self.window.findChild(QPushButton, "pushButtonForgot")

        self._validate_widgets()
        self._connect_events()
        self.usuario_input.setFocus()

    def _validate_widgets(self) -> None:
        missing = []
        if self.usuario_input is None:
            missing.append("lineEditUser")
        if self.contrasena_input is None:
            missing.append("lineEditPassword")
        if self.recordar_check is None:
            missing.append("checkBoxRemember")
        if self.login_button is None:
            missing.append("pushButtonLogin")
        if self.cancel_button is None:
            missing.append("pushButtonCancel")
        if self.forgot_button is None:
            missing.append("pushButtonForgot")

        if missing:
            raise RuntimeError("Faltan objectName en login_qtdesigner.ui: " + ", ".join(missing))

    def _connect_events(self) -> None:
        self.login_button.clicked.connect(self.validar_credenciales)
        self.cancel_button.clicked.connect(self.close)
        self.forgot_button.clicked.connect(self.forgot_password)
        self.contrasena_input.returnPressed.connect(self.validar_credenciales)
        self.usuario_input.returnPressed.connect(self.contrasena_input.setFocus)

    def show(self) -> None:
        self.window.show()

    def close(self) -> None:
        self.window.close()

    def validar_credenciales(self) -> None:
        username = self.usuario_input.text().strip()
        password = self.contrasena_input.text()

        if not username or not password:
            QMessageBox.warning(self.window, "Error", "Debes capturar usuario y contrasena.")
            self.contrasena_input.clear()
            return

        if not self.auth_controller.check_user(username):
            QMessageBox.warning(self.window, "Error", "El usuario no esta registrado.")
            self.contrasena_input.clear()
            return

        if not self.auth_controller.check_password(username, password):
            QMessageBox.warning(self.window, "Error", "Usuario o contrasena incorrectos.")
            self.contrasena_input.clear()
            return

        self.iniciar_sesion(username)

    def iniciar_sesion(self, username: str) -> None:
        if hasattr(self.controller, "showContadorWindow"):
            self.controller.showContadorWindow(username)
            return

        self.controller.show_contador_window(username)

    def forgot_password(self) -> None:
        QMessageBox.information(
            self.window,
            "Recuperacion",
            "Aqui puedes agregar la logica de recuperacion de contrasena.",
        )
