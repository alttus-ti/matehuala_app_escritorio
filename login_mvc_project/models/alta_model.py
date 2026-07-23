from datetime import datetime

import requests

from core.database import get_connection
from core.sync_queue import enqueue_sync_event
from core.sync_config import (
    SYNC_API_BASE_URL,
    SYNC_API_TOKEN,
    SYNC_CONNECT_TIMEOUT_SECONDS,
    SYNC_READ_TIMEOUT_SECONDS,
)


class AltaModel:
    def normalizar_curp(self, curp: str) -> str:
        return (curp or "").strip().upper()

    def buscar_curp_local(self, curp: str):
        curp = self.normalizar_curp(curp)

        if not curp or curp == "-":
            return None

        with get_connection() as connection:
            return connection.execute(
                """
                SELECT 
                    p.id,
                    p.nombre,
                    p.curp,
                    t.uid
                FROM pasajeros p
                LEFT JOIN tarjetas t ON t.pasajero_id = p.id
                WHERE UPPER(TRIM(p.curp)) = ?
                LIMIT 1
                """,
                (curp,),
            ).fetchone()

    def buscar_curp_servidor(self, curp: str):
        curp = self.normalizar_curp(curp)

        if not curp or curp == "-":
            return None

        response = requests.get(
            f"{SYNC_API_BASE_URL.rstrip('/')}/api/pasajeros/existe-curp",
            params={"curp": curp},
            headers={
                "Accept": "application/json",
                "Authorization": f"Bearer {SYNC_API_TOKEN}",
                "X-Desktop-Sync-Token": SYNC_API_TOKEN,
            },
            timeout=(SYNC_CONNECT_TIMEOUT_SECONDS, SYNC_READ_TIMEOUT_SECONDS),
        )

        response.raise_for_status()
        data = response.json()

        if data.get("exists"):
            return data.get("pasajero") or {"curp": curp}

        return None

    def guardar_alta_local(
        self,
        uid: str,
        nombre_pasajero: str,
        tipo: str,
        vigencia: str,
        curp: str = "",
        fecha_nacimiento="",
        foto: str = ""
    ):
        curp = self.normalizar_curp(curp)

        if not curp or curp == "-":
            raise ValueError("Captura la CURP.")

        curp_existe = self.buscar_curp_local(curp)
        if curp_existe:
            raise ValueError(
                f"La CURP {curp} ya existe en la base local. "
               
            )

        tipo_tarjeta_id = 2 if tipo == "EU" else 1
        nombre_final = (nombre_pasajero or "").strip()

        if not nombre_final:
            nombre_final = f"Tarjeta {uid[-4:]}"

        documento_auto = "-"
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

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
                    SET nombre = ?, documento = ?, curp = ?, foto = ?, fecha_nacimiento = ?
                    WHERE id = ?
                    """,
                    (
                        nombre_final,
                        documento_auto,
                        curp,
                        foto,
                        fecha_nacimiento,
                        tarjeta["pasajero_id"],
                    ),
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
                    INSERT INTO pasajeros (nombre, documento, curp, foto, fecha_nacimiento)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        nombre_final,
                        documento_auto,
                        curp,
                        foto,
                        fecha_nacimiento,
                    ),
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
                    "curp": curp,
                    "foto": foto,
                    "fecha_nacimiento": fecha_nacimiento,
                    "tipo_codigo_local": tipo,
                    "vigencia": vigencia,
                    "local_created_at": created_at,
                },
            )

            return tarjeta_id