from models.user_model import UserModel


class AuthController:
    """Controlador de autenticacion."""

    def __init__(self):
        self.model = UserModel()

    def check_user(self, username: str) -> bool:
        return self.model.user_exists(username)

    def check_password(self, username: str, password: str) -> bool:
        return self.model.password_matches(username, password)

    def authenticate(self, username: str, password: str) -> tuple[bool, str]:
        return self.model.authenticate(username, password)
    
    def get_user_role(self, username: str) -> str | None:
        return self.model.get_role(username)

    def get_role(self, username: str) -> str | None:
        return self.get_user_role(username)
