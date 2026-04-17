from core.database import get_connection


class RecargaModel:
    def obtener_tarjeta_por_uid(self, uid: str):
        with get_connection() as connection:
            row = connection.execute(
                """
                SELECT
                    t.id,
                    t.uid,
                    t.saldo,
                    t.tipo_tarjeta_id,
                    tt.descripcion AS tipo_tarjeta,
                    p.nombre AS nombre_pasajero
                FROM tarjetas t
                INNER JOIN tipo_tarjetas tt ON tt.id = t.tipo_tarjeta_id
                INNER JOIN pasajeros p ON p.id = t.pasajero_id
                WHERE t.uid = ?
                LIMIT 1
                """,
                (uid,),
            ).fetchone()

            return row

    def _obtener_usuario_id(self, connection, username: str):
        row = connection.execute(
            "SELECT id FROM usuarios WHERE username = ? LIMIT 1",
            (username,),
        ).fetchone()

        if row is None:
            raise ValueError("El usuario no existe en la base local.")

        return row["id"]

    def _asegurar_tarjeta_local(
        self,
        connection,
        uid: str,
        nombre_pasajero: str,
        saldo_actual: float,
    ):
        tarjeta = connection.execute(
            "SELECT id FROM tarjetas WHERE uid = ? LIMIT 1",
            (uid,),
        ).fetchone()

        if tarjeta:
            connection.execute(
                "UPDATE tarjetas SET saldo = ? WHERE id = ?",
                (saldo_actual, tarjeta["id"]),
            )
            return tarjeta["id"]

        nombre_final = (nombre_pasajero or "").strip()
        if not nombre_final:
            nombre_final = f"Tarjeta {uid[-4:]}"

        documento_auto = f"AUTO-{uid}"

        cursor_pasajero = connection.execute(
            """
            INSERT INTO pasajeros (nombre, documento)
            VALUES (?, ?)
            """,
            (nombre_final, documento_auto),
        )
        pasajero_id = cursor_pasajero.lastrowid

        cursor_tarjeta = connection.execute(
            """
            INSERT INTO tarjetas (uid, saldo, tipo_tarjeta_id, pasajero_id, vigencia)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                uid,
                saldo_actual,
                1,          # tipo_tarjeta_id = 1 -> Normal
                pasajero_id,
                None,
            ),
        )
        return cursor_tarjeta.lastrowid

    def guardar_recarga_flexible(
        self,
        uid: str,
        username: str,
        monto: float,
        nuevo_saldo: float,
        nombre_pasajero: str = "",
        referencia: str | None = None,
    ):
        with get_connection() as connection:
            usuario_id = self._obtener_usuario_id(connection, username)

            tarjeta_id = self._asegurar_tarjeta_local(
                connection=connection,
                uid=uid,
                nombre_pasajero=nombre_pasajero,
                saldo_actual=nuevo_saldo,
            )

            connection.execute(
                """
                INSERT INTO recargas (tarjeta_id, usuario_id, monto, referencia)
                VALUES (?, ?, ?, ?)
                """,
                (tarjeta_id, usuario_id, monto, referencia),
            )