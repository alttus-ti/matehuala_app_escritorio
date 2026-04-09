class UserModel:
    def user_exists(self, username: str) -> bool:
        return username.strip() == "admin"

    def password_matches(self, username: str, password: str) -> bool:
        return self.user_exists(username) and password.strip() == "1234"

    def authenticate(self, username: str, password: str) -> tuple[bool, str]:
        username = username.strip()
        password = password.strip()

        if not username or not password:
            return False, "Debes capturar usuario y contrasena."

        if self.password_matches(username, password):
            return True, "Login correcto."

        return False, "Usuario o contrasena incorrectos."
