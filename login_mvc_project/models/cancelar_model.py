from datetime import datetime
from core.database import get_connection
from core.sync_queue import enqueue_sync_event


class CancelarModel:
    def obtener_tarjeta_por_uid(self, uid: str):
        with get_connection() as connection:
            tarjeta = connection.execute(
                """
                SELECT
                    t.id,
                    t.uid,
                    t.saldo,
                    t.vigencia,
                    t.en_lista_negra,
                    t.motivo_baja,
                    t.fecha_baja,
                    t.pasajero_id,
                    p.nombre AS nombre_pasajero,
                    p.curp,
                    p.foto,
                    p.fecha_nacimiento
                FROM tarjetas t
                LEFT JOIN pasajeros p ON p.id = t.pasajero_id
                WHERE t.uid = ?
                LIMIT 1
                """,
                (uid,),
            ).fetchone()
            return tarjeta

    def _asegurar_tarjeta_local(
        self,
        connection,
        uid: str,
        nombre_pasajero: str = "",
        saldo_actual: float = 0.0,
    ):
        tarjeta = connection.execute(
            """
            SELECT id, pasajero_id
            FROM tarjetas
            WHERE uid = ?
            LIMIT 1
            """,
            (uid,),
        ).fetchone()

        nombre_final = (nombre_pasajero or "").strip()
        if not nombre_final:
            nombre_final = f"Tarjeta {uid[-4:]}"

        if tarjeta:
            # Si ya existe, actualiza nombre y saldo local
            if tarjeta["pasajero_id"] and nombre_pasajero.strip():
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
                SET saldo = COALESCE(?, saldo)
                WHERE id = ?
                """,
                (saldo_actual, tarjeta["id"]),
            )
            return tarjeta["id"]

        # Si no existe, crear pasajero + tarjeta
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
            INSERT INTO tarjetas (uid, saldo, tipo_tarjeta_id, pasajero_id, vigencia, en_lista_negra)
            VALUES (?, ?, ?, ?, ?, 0)
            """,
            (
                uid,
                float(saldo_actual or 0),
                1,          # Normal por defecto
                pasajero_id,
                None,
            ),
        )
        return cursor_tarjeta.lastrowid

    def guardar_lectura_si_no_existe(
        self,
        uid: str,
        nombre_pasajero: str = "",
        saldo_actual: float = 0.0,
    ):
        with get_connection() as connection:
            return self._asegurar_tarjeta_local(
                connection=connection,
                uid=uid,
                nombre_pasajero=nombre_pasajero,
                saldo_actual=saldo_actual,
            )

    def cancelar_tarjeta_flexible(
        self,
        uid: str,
        nombre_pasajero: str = "",
        saldo_actual: float = 0.0,
        en_lista_negra: bool = True,
        motivo_baja: str = "Cancelada",
    ):
        with get_connection() as connection:
            tarjeta_id = self._asegurar_tarjeta_local(
                connection=connection,
                uid=uid,
                nombre_pasajero=nombre_pasajero,
                saldo_actual=saldo_actual,
            )

            fecha_baja = datetime.now().strftime("%Y-%m-%d %H:%M:%S") if en_lista_negra else None
            motivo_final = motivo_baja if en_lista_negra else None

            connection.execute(
                """
                UPDATE tarjetas
                SET en_lista_negra = ?,
                    motivo_baja = ?,
                    fecha_baja = ?
                WHERE id = ?
                """,
                (
                    1 if en_lista_negra else 0,
                    motivo_final,
                    fecha_baja,
                    tarjeta_id,
                ),
            )

            enqueue_sync_event(
                connection,
                event_type="cancelacion_tarjeta",
                entity_uid=uid,
                payload={
                    "uid": uid,
                    "nombre_pasajero": (nombre_pasajero or "").strip(),
                    "curp": None,
                    "foto": None,
                    "fecha_nacimiento": None,
                    "saldo_actual": float(saldo_actual or 0),
                    "en_lista_negra": bool(en_lista_negra),
                    "motivo_baja": motivo_final,
                    "fecha_baja": fecha_baja,
                },
            )

            return tarjeta_id
