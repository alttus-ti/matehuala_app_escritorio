from PySide6.QtWidgets import QComboBox, QMainWindow, QMessageBox, QPushButton, QTextEdit

from core.ui_loader import load_ui


class ContadorWindow:
    def __init__(self, controller, username: str):
        self.controller = controller
        self.username = username
        self.window = load_ui("ui/contador.ui")

        if not isinstance(self.window, QMainWindow):
            raise RuntimeError("El archivo contador.ui no contiene un QMainWindow.")

        self.texto = self.window.findChild(QTextEdit, "texto")
        self.combo = self.window.findChild(QComboBox, "comboBox")
        self.contar_button = self.window.findChild(QPushButton, "contador")

        self._validate_widgets()
        self._setup_ui()
        self._connect_events()

    def _validate_widgets(self) -> None:
        missing = []
        if self.texto is None:
            missing.append("texto")
        if self.combo is None:
            missing.append("comboBox")
        if self.contar_button is None:
            missing.append("contador")
        if missing:
            raise RuntimeError("Faltan objectName en contador.ui: " + ", ".join(missing))

    def _setup_ui(self) -> None:
        self.window.setWindowTitle(f"Contador - {self.username}")
        self.combo.addItems(["Caracteres", "Palabras", "Lineas"])
        self.texto.setPlaceholderText("Escribe texto y presiona 'contar'.")

    def _connect_events(self) -> None:
        self.contar_button.clicked.connect(self.contar)

    def show(self) -> None:
        self.window.show()

    def close(self) -> None:
        self.window.close()

    def contar(self) -> None:
        text = self.texto.toPlainText()
        option = self.combo.currentText()

        if option == "Caracteres":
            result = len(text)
        elif option == "Palabras":
            result = len([word for word in text.split() if word])
        else:
            result = len(text.splitlines()) if text else 0

        QMessageBox.information(self.window, "Resultado", f"{option}: {result}")
