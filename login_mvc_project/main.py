import sys
from PySide6.QtWidgets import QApplication
from controllers.app_controller import AppController


def main() -> int:
    app = QApplication(sys.argv)

    controller = AppController()
    controller.showLoginWindow()

    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
