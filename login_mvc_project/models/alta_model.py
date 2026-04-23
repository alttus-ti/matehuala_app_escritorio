from datetime import datetime

from core.database import get_connection
from core.sync_queue import enqueue_sync_event


class AltaModel:
    def guardar_alta_local(
        self,
        uid: str,
        nombre_pasajero: str,
        tipo: str,
        vigencia: str,
        curp: str | None = None,
        foto: str | None = None,
        fecha_nacimiento: str | None = None,
    ):
        tipo_tarjeta_id = 2 if tipo == "EU" else 1
        nombre_final = (nombre_pasajero or "").strip()
        if not nombre_final:
            nombre_final = f"Tarjeta {uid[-4:]}"

        documento_auto = f"AUTO-{uid}"
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
<<<<<<< HEAD
        curp_final = (curp or "").strip() or None
        foto_final = (foto or "").strip() or None
        fecha_nacimiento_final = (fecha_nacimiento or "").strip() or None
=======
>>>>>>> 3b4dc0a666cd5a2194eed821832e1d14eae96219

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
<<<<<<< HEAD
                    SET nombre = ?,
                        documento = ?,
                        curp = ?,
                        foto = ?,
                        fecha_nacimiento = ?
                    WHERE id = ?
                    """,
                    (
                        nombre_final,
                        documento_auto,
                        curp_final,
                        foto_final,
                        fecha_nacimiento_final,
                        tarjeta["pasajero_id"],
                    ),
=======
                    SET nombre = ?, documento = ?
                    WHERE id = ?
                    """,
                    (nombre_final, documento_auto, tarjeta["pasajero_id"]),
>>>>>>> 3b4dc0a666cd5a2194eed821832e1d14eae96219
                )
                connection.execute(
                    """
                    UPDATE tarjetas
                    SET saldo = ?, tipo_tarjeta_id = ?, vigencia = ?
                    WHERE id = ?
                    """,
                    (0.0, tipo_tarjeta_id, vigencia, tarjeta["id"]),
                )
                tarjeta_id = tarjeta["id"]
            else:
                cursor_pasajero = connection.execute(
                    """
<<<<<<< HEAD
                    INSERT INTO pasajeros (nombre, documento, curp, foto, fecha_nacimiento)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        nombre_final,
                        documento_auto,
                        curp_final,
                        foto_final,
                        fecha_nacimiento_final,
                    ),
=======
                    INSERT INTO pasajeros (nombre, documento)
                    VALUES (?, ?)
                    """,
                    (nombre_final, documento_auto),
>>>>>>> 3b4dc0a666cd5a2194eed821832e1d14eae96219
                )
                pasajero_id = cursor_pasajero.lastrowid

                cursor_tarjeta = connection.execute(
                    """
                    INSERT INTO tarjetas (uid, saldo, tipo_tarjeta_id, pasajero_id, vigencia)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (uid, 0.0, tipo_tarjeta_id, pasajero_id, vigencia),
                )
                tarjeta_id = cursor_tarjeta.lastrowid

            enqueue_sync_event(
                connection,
                event_type="alta_tarjeta",
                entity_uid=uid,
                payload={
                    "uid": uid,
                    "saldo": 0.0,
                    "nombre_pasajero": nombre_final,
                    "documento": documento_auto,
<<<<<<< HEAD
                    "curp": curp_final,
                    "foto": foto_final,
                    "fecha_nacimiento": fecha_nacimiento_final,
=======
>>>>>>> 3b4dc0a666cd5a2194eed821832e1d14eae96219
                    "tipo_codigo_local": tipo,
                    "vigencia": vigencia,
                    "local_created_at": created_at,
                },
            )

            return tarjeta_id
