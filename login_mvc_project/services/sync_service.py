from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import requests

from core.database import get_connection
from core.sync_config import (
    SYNC_API_BASE_URL,
    SYNC_API_TOKEN,
    SYNC_BATCH_PATH,
    SYNC_BATCH_SIZE,
    SYNC_CONNECT_TIMEOUT_SECONDS,
    SYNC_PING_PATH,
    SYNC_READ_TIMEOUT_SECONDS,
    SYNC_UPLOAD_FOTO_PATH,
)


class SyncService:
    def __init__(self) -> None:
        self.base_url = SYNC_API_BASE_URL.rstrip("/")
        self.token = SYNC_API_TOKEN.strip()
        self.timeout = (SYNC_CONNECT_TIMEOUT_SECONDS, SYNC_READ_TIMEOUT_SECONDS)

    def count_pending(self) -> int:
        with get_connection() as connection:
            row = connection.execute(
                """
                SELECT COUNT(*) AS total
                FROM sync_queue
                WHERE status IN ('pending', 'error')
                """
            ).fetchone()

        return int(row["total"] if row else 0)

    def ping(self) -> bool:
        if not self.base_url or not self.token:
            return False

        response = requests.get(
            f"{self.base_url}{SYNC_PING_PATH}",
            headers=self._headers(),
            timeout=self.timeout,
        )
        response.raise_for_status()
        data = response.json()
        return bool(data.get("ok", False))

    def sync_pending_once(self) -> dict[str, Any]:
        self._cleanup_synced_queue()
        pending_before = self.count_pending()

        if pending_before == 0:
            try:
                online = self.ping()
                if online:
                    self.limpiar_tarjetas_locales_ya_subidas()
                return {
                    "state": "connected" if online else "offline",
                    "pending_before": 0,
                    "pending_after": 0,
                    "synced_count": 0,
                    "error_count": 0,
                    "message": "Sin pendientes" if online else "Sin conexión",
                }
            except Exception as error:
                return {
                    "state": "offline",
                    "pending_before": 0,
                    "pending_after": 0,
                    "synced_count": 0,
                    "error_count": 0,
                    "message": str(error),
                }

        operations = self._load_pending_operations(limit=SYNC_BATCH_SIZE)
        if not operations:
            return {
                "state": "connected",
                "pending_before": pending_before,
                "pending_after": 0,
                "synced_count": 0,
                "error_count": 0,
                "message": "Sin pendientes",
            }
            
        operations = self._preparar_fotos_para_subir(operations)

        try:
            response = requests.post(
                f"{self.base_url}{SYNC_BATCH_PATH}",
                json={"operations": operations},
                headers=self._headers(),
                timeout=self.timeout,
            )
            response.raise_for_status()
            payload = response.json()
        except Exception as error:
            return {
                "state": "offline",
                "pending_before": pending_before,
                "pending_after": pending_before,
                "synced_count": 0,
                "error_count": len(operations),
                "message": str(error),
            }

        results = payload.get("results", [])
        synced_count = 0
        error_count = 0

        for result in results:
            operation_uuid = (result or {}).get("operation_uuid")
            status = (result or {}).get("status")
            message = (result or {}).get("message") or "Error desconocido"

            if not operation_uuid:
                continue

            if status in {"ok", "already_synced", "success"}:
                self._mark_synced(operation_uuid)
                synced_count += 1
            else:
                self._mark_error(operation_uuid, message)
                error_count += 1

        pending_after = self.count_pending()
        eliminadas = 0
        if pending_after == 0:
            eliminadas = self.limpiar_tarjetas_locales_ya_subidas()

        return {
            "state": "connected" if error_count == 0 else "connected_with_errors",
            "pending_before": pending_before,
            "pending_after": pending_after,
            "synced_count": synced_count,
            "error_count": error_count,
            "message": "Sincronización completada",
        }

    def _load_pending_operations(self, *, limit: int) -> list[dict[str, Any]]:
        with get_connection() as connection:
            rows = connection.execute(
                """
                SELECT operation_uuid, event_type, entity_uid, payload_json
                FROM sync_queue
                WHERE status IN ('pending', 'error')
                ORDER BY id ASC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()

        operations: list[dict[str, Any]] = []
        for row in rows:
            operations.append(
                {
                    "operation_uuid": row["operation_uuid"],
                    "event_type": row["event_type"],
                    "entity_uid": row["entity_uid"],
                    "payload": json.loads(row["payload_json"]),
                }
            )

        return operations

    def _mark_synced(self, operation_uuid: str) -> None:
        with get_connection() as connection:
            operation = connection.execute(
                """
                SELECT event_type, entity_uid, payload_json
                FROM sync_queue
                WHERE operation_uuid = ?
                LIMIT 1
                """,
                (operation_uuid,),
            ).fetchone()

            connection.execute(
                """
                UPDATE sync_queue
                SET status = 'synced',
                    synced_at = datetime('now'),
                    last_error = NULL
                WHERE operation_uuid = ?
                """,
                (operation_uuid,),
            )

            if operation:
                self._cleanup_synced_local_data(
                    connection=connection,
                    event_type=operation["event_type"],
                    entity_uid=operation["entity_uid"],
                    payload=json.loads(operation["payload_json"]),
                )

            connection.execute(
                """
                DELETE FROM sync_queue
                WHERE operation_uuid = ?
                  AND status = 'synced'
                """,
                (operation_uuid,),
            )

    def _mark_error(self, operation_uuid: str, message: str) -> None:
        with get_connection() as connection:
            connection.execute(
                """
                UPDATE sync_queue
                SET status = 'error',
                    retries = retries + 1,
                    last_error = ?
                WHERE operation_uuid = ?
                """,
                (message[:1000], operation_uuid),
            )

    def _cleanup_synced_queue(self) -> None:
        with get_connection() as connection:
            rows = connection.execute(
                """
                SELECT operation_uuid, event_type, entity_uid, payload_json
                FROM sync_queue
                WHERE status = 'synced'
                ORDER BY id ASC
                """
            ).fetchall()

            for row in rows:
                self._cleanup_synced_local_data(
                    connection=connection,
                    event_type=row["event_type"],
                    entity_uid=row["entity_uid"],
                    payload=json.loads(row["payload_json"]),
                )

                connection.execute(
                    """
                    DELETE FROM sync_queue
                    WHERE operation_uuid = ?
                      AND status = 'synced'
                    """,
                    (row["operation_uuid"],),
                )

    def _headers(self) -> dict[str, str]:
        return {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.token}",
            "X-Desktop-Sync-Token": self.token,
        }
        
    def _preparar_fotos_para_subir(self, operations: list[dict[str, Any]]) -> list[dict[str, Any]]:
        for operation in operations:
            if operation.get("event_type") != "alta_tarjeta":
                continue

            payload = operation.get("payload") or {}

            foto = str(payload.get("foto") or "").strip()

            if not foto:
                continue

            # Si ya es ruta del servidor, no la vuelvas a subir
            if foto.startswith("pasajeros/") or foto.startswith("http://") or foto.startswith("https://"):
                continue

            foto_path = Path(foto)

            if not foto_path.exists():
                payload["foto"] = ""
                self._actualizar_payload_local(operation["operation_uuid"], payload)
                continue

            resultado = self._subir_foto_al_servidor(
                foto_path=foto_path,
                uid=str(payload.get("uid") or operation.get("entity_uid") or "")
            )

            payload["foto"] = resultado["path"]

            operation["payload"] = payload

            self._actualizar_payload_local(operation["operation_uuid"], payload)

        return operations


    def _subir_foto_al_servidor(self, *, foto_path: Path, uid: str) -> dict[str, Any]:
        with foto_path.open("rb") as archivo:
            response = requests.post(
                f"{self.base_url}{SYNC_UPLOAD_FOTO_PATH}",
                headers=self._headers(),
                data={
                    "uid": uid,
                },
                files={
                    "foto": (foto_path.name, archivo),
                },
                timeout=self.timeout,
            )

        response.raise_for_status()

        data = response.json()

        if not data.get("ok") or not data.get("path"):
            raise RuntimeError("El servidor no devolvió la ruta de la foto.")

        return data


    def _actualizar_payload_local(self, operation_uuid: str, payload: dict[str, Any]) -> None:
        with get_connection() as connection:
            connection.execute(
                """
                UPDATE sync_queue
                SET payload_json = ?
                WHERE operation_uuid = ?
                """,
                (
                    json.dumps(payload, ensure_ascii=False),
                    operation_uuid,
                ),
            )


    def _cleanup_synced_local_data(
        self,
        *,
        connection,
        event_type: str,
        entity_uid: str | None,
        payload: dict[str, Any],
    ) -> None:
        uid = str(entity_uid or payload.get("uid") or "").strip().upper()
        if not uid:
            return

        if self._has_unsynced_operations_for_uid(connection, uid):
            return

        if event_type in {
            "alta_tarjeta",
            "recarga_tarjeta",
            "cancelacion_tarjeta",
            "sustitucion_tarjeta",
        }:
            self._delete_local_card_data(connection, uid)


    def _has_unsynced_operations_for_uid(self, connection, uid: str) -> bool:
        row = connection.execute(
            """
            SELECT 1
            FROM sync_queue
            WHERE UPPER(COALESCE(entity_uid, '')) = ?
              AND status IN ('pending', 'error')
            LIMIT 1
            """,
            (uid,),
        ).fetchone()

        return row is not None


    def _delete_local_card_data(self, connection, uid: str) -> None:
        tarjetas = connection.execute(
            """
            SELECT id, pasajero_id
            FROM tarjetas
            WHERE UPPER(uid) = ?
            """,
            (uid,),
        ).fetchall()

        for tarjeta in tarjetas:
            tarjeta_id = tarjeta["id"]
            pasajero_id = tarjeta["pasajero_id"]

            connection.execute(
                """
                DELETE FROM recargas
                WHERE tarjeta_id = ?
                """,
                (tarjeta_id,),
            )

            connection.execute(
                """
                DELETE FROM tarjetas
                WHERE id = ?
                """,
                (tarjeta_id,),
            )

            if pasajero_id:
                self._delete_orphan_passenger(connection, pasajero_id)


    def _delete_orphan_passenger(self, connection, pasajero_id: int) -> None:
        row = connection.execute(
            """
            SELECT 1
            FROM tarjetas
            WHERE pasajero_id = ?
            LIMIT 1
            """,
            (pasajero_id,),
        ).fetchone()

        if row is not None:
            return

        connection.execute(
            """
            DELETE FROM pasajeros
            WHERE id = ?
            """,
            (pasajero_id,),
        )
        
    def limpiar_tarjetas_locales_ya_subidas(self) -> int:
        """
        Borra de SQLite las tarjetas, recargas y pasajeros que ya existen en el servidor.
        Solo borra si:
        1. No hay pendientes/error de esa UID en sync_queue.
        2. La UID ya existe en el servidor.
        """
        eliminadas = 0
        hubo_error_verificacion = False

        with get_connection() as connection:
            tarjetas = connection.execute(
                """
                SELECT DISTINCT uid
                FROM tarjetas
                WHERE uid IS NOT NULL
                AND TRIM(uid) != ''
                AND NOT EXISTS (
                    SELECT 1
                    FROM sync_queue sq
                    WHERE UPPER(COALESCE(sq.entity_uid, '')) = UPPER(tarjetas.uid)
                        AND sq.status IN ('pending', 'error')
                )
                """
            ).fetchall()

            for tarjeta in tarjetas:
                uid = str(tarjeta["uid"] or "").strip().upper()

                if not uid:
                    continue

                existe_en_servidor = self._tarjeta_existe_en_servidor(uid)

                if existe_en_servidor is True:
                    print(f"[SYNC] UID encontrada en servidor, borrando local: {uid}")
                    self._delete_local_card_data(connection, uid)
                    eliminadas += 1
                elif existe_en_servidor is False:
                    print(f"[SYNC] UID no encontrada en servidor, se conserva local: {uid}")
                else:
                    hubo_error_verificacion = True
                    print(f"[SYNC] No se pudo verificar UID, se conserva local: {uid}")

            if not hubo_error_verificacion:
                self._delete_all_orphan_passengers(connection)

        return eliminadas


    def _tarjeta_existe_en_servidor(self, uid: str) -> bool | None:
        uid = (uid or "").strip().upper()

        if not uid:
            return False

        if not self.base_url or not self.token:
            return None

        try:
            response = requests.get(
                f"{self.base_url}/api/tarjetas/buscar",
                params={
                    "texto": uid,
                    "limite": 10,
                    "incluir_lista_negra": 1,
                },
                headers=self._headers(),
                timeout=self.timeout,
            )

            response.raise_for_status()
            data = response.json()

            items = data.get("items", [])

            for item in items:
                if not isinstance(item, dict):
                    continue

                uid_servidor = str(item.get("uid") or "").strip().upper()

                if uid_servidor == uid:
                    return True

            return False

        except Exception as error:
            print(f"[SYNC] No se pudo verificar UID en servidor {uid}: {error}")
            return None


    def _delete_all_orphan_passengers(self, connection) -> None:
        """
        Borra pasajeros que ya no tienen tarjeta relacionada.
        """
        connection.execute(
            """
            DELETE FROM pasajeros
            WHERE id NOT IN (
                SELECT pasajero_id
                FROM tarjetas
                WHERE pasajero_id IS NOT NULL
            )
            """
        )
