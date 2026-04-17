from core.database import get_connection


class AltaModel:
    def guardar_alta_local(
        self,
        uid: str,
        nombre_pasajero: str,
        tipo: str,
        vigencia: str,
    ):
        tipo_tarjeta_id = 2 if tipo == "EU" else 1
        nombre_final = (nombre_pasajero or "").strip()
        if not nombre_final:
            nombre_final = f"Tarjeta {uid[-4:]}"

        with get_connection() as connection:
            tarjeta = connection.execute(
                """
                SELECT id, pasajero_id
                FROM tarjetas
                WHERE uid = ?
                LIMIT 1
                """,
                (uid,),
            ).fetchone()

            if tarjeta:
                connection.execute(
                    """
                    UPDATE pasajeros
                    SET nombre = ?
                    WHERE id = ?
                    """,
                    (nombre_final, tarjeta["pasajero_id"]),
                )
                connection.execute(
                    """
                    UPDATE tarjetas
                    SET saldo = ?, tipo_tarjeta_id = ?, vigencia = ?
                    WHERE id = ?
                    """,
                    (0.0, tipo_tarjeta_id, vigencia, tarjeta["id"]),
                )
                return tarjeta["id"]

            cursor_pasajero = connection.execute(
                """
                INSERT INTO pasajeros (nombre, documento)
                VALUES (?, ?)
                """,
                (nombre_final, f"AUTO-{uid}"),
            )
            pasajero_id = cursor_pasajero.lastrowid

            cursor_tarjeta = connection.execute(
                """
                INSERT INTO tarjetas (uid, saldo, tipo_tarjeta_id, pasajero_id, vigencia)
                VALUES (?, ?, ?, ?, ?)
                """,
                (uid, 0.0, tipo_tarjeta_id, pasajero_id, vigencia),
            )
            return cursor_tarjeta.lastrowid
