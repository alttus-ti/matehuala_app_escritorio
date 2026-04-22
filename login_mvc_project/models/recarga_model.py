from datetime import datetime

from core.database import get_connection
from core.sync_queue import enqueue_sync_event


class RecargaModel:
    def obtener_tarjeta_por_uid(self, uid: str):
        with get_connection() as connection:
            row = connection.execute(
                """
                SELECT
                    t.id,
                    t.uid,
                    t.saldo,
                    t.vigencia,
                    t.tipo_tarjeta_id,
                    t.en_lista_negra,
                    tt.descripcion AS tipo_tarjeta,
                    p.nombre AS nombre_pasajero,
                    p.curp,
                    p.foto,
                    p.fecha_nacimiento
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
            INSERT INTO pasajeros (nombre, documento, curp, foto, fecha_nacimiento)
            VALUES (?, ?, NULL, NULL, NULL)
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
                1,
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
        oficina: str | None = None,
    ):
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        nombre_final = (nombre_pasajero or "").strip() or f"Tarjeta {uid[-4:]}"
        oficina_final = (oficina or "").strip() or None

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
                INSERT INTO recargas (tarjeta_id, usuario_id, monto, oficina, referencia)
                VALUES (?, ?, ?, ?, ?)
                """,
                (tarjeta_id, usuario_id, monto, oficina_final, referencia),
            )

            enqueue_sync_event(
                connection,
                event_type="recarga_tarjeta",
                entity_uid=uid,
                payload={
                    "uid": uid,
                    "username": username,
                    "monto": float(monto),
                    "nuevo_saldo": float(nuevo_saldo),
                    "oficina": oficina_final,
                    "nombre_pasajero": nombre_final,
                    "documento": f"AUTO-{uid}",
                    "curp": None,
                    "foto": None,
                    "fecha_nacimiento": None,
                    "referencia": referencia,
                    "local_created_at": created_at,
                },
            )
