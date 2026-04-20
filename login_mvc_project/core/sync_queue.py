from __future__ import annotations

import json
import uuid
from typing import Any


def enqueue_sync_event(
    connection,
    *,
    event_type: str,
    entity_uid: str | None,
    payload: dict[str, Any],
) -> str:
    operation_uuid = str(uuid.uuid4())

    connection.execute(
        """
        INSERT INTO sync_queue (
            operation_uuid,
            event_type,
            entity_uid,
            payload_json,
            status,
            retries,
            last_error
        )
        VALUES (?, ?, ?, ?, 'pending', 0, NULL)
        """,
        (
            operation_uuid,
            event_type,
            entity_uid,
            json.dumps(payload, ensure_ascii=False),
        ),
    )

    return operation_uuid
