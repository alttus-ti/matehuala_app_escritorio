from core.database import get_connection


class UserModel:
    def user_exists(self, username: str) -> bool:
        username = username.strip()

        if not username:
            return False

        with get_connection() as connection:
            user = connection.execute(
                "SELECT 1 FROM usuarios WHERE username = ? LIMIT 1",
                (username,),
            ).fetchone()

        return user is not None

    def password_matches(self, username: str, password: str) -> bool:
        username = username.strip()
        password = password.strip()

        if not username or not password:
            return False

        with get_connection() as connection:
            user = connection.execute(
                """
                SELECT 1
                FROM usuarios
                WHERE username = ? AND password = ?
                LIMIT 1
                """,
                (username, password),
            ).fetchone()

        return user is not None

    def authenticate(self, username: str, password: str) -> tuple[bool, str]:
        username = username.strip()
        password = password.strip()

        if not username or not password:
            return False, "Debes capturar usuario y contrasena."

        if self.password_matches(username, password):
            return True, "Login correcto."

        return False, "Usuario o contrasena incorrectos."
    
    def get_role(self, username: str) -> str | None:
        username = username.strip()
        
        if not username:
            return None
        
        with get_connection() as connection:
            row = connection.execute(
                """
                SELECT r.nombre
                FROM usuarios u
                INNER JOIN roles r ON r.id = u.role_id
                WHERE u.username = ?
                LIMIT 1
                """,
                (username,),
            ).fetchone()
            
        return row[0] if row else None