from views.contador_view import ContadorWindow
from views.login_view import LoginWindow


class AppController:
    """Controlador principal de ventanas."""

    def __init__(self):
        self.current_window = None

    def show_login_window(self) -> None:
        self._close_current_window()
        self.current_window = LoginWindow(controller=self)
        self.current_window.show()

    def showLoginWindow(self) -> None:
        self.show_login_window()

    def show_contador_window(self, username: str) -> None:
        self._close_current_window()
        self.current_window = ContadorWindow(controller=self, username=username)
        self.current_window.show()

    def showContadorWindow(self, username: str) -> None:
        self.show_contador_window(username)

    def _close_current_window(self) -> None:
        if self.current_window is not None:
            self.current_window.close()
