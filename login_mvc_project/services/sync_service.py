from __future__ import annotations

import json
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
        pending_before = self.count_pending()

        if pending_before == 0:
            try:
                online = self.ping()
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

            if status in {"ok", "already_synced"}:
                self._mark_synced(operation_uuid)
                synced_count += 1
            else:
                self._mark_error(operation_uuid, message)
                error_count += 1

        pending_after = self.count_pending()

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

    def _headers(self) -> dict[str, str]:
        return {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.token}",
            "X-Desktop-Sync-Token": self.token,
        }
