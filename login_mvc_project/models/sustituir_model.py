import requests

from core.sync_config import (
    SYNC_API_BASE_URL,
    SYNC_API_TOKEN,
    SYNC_CONNECT_TIMEOUT_SECONDS,
    SYNC_READ_TIMEOUT_SECONDS,
)


class SustituirModel:
    def __init__(self) -> None:
        self.base_url = SYNC_API_BASE_URL.rstrip("/")
        self.token = SYNC_API_TOKEN.strip()
        self.timeout = (SYNC_CONNECT_TIMEOUT_SECONDS, SYNC_READ_TIMEOUT_SECONDS)
        
    def _headers(self) -> dict[str, str]:
        return {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.token}",
            "X-Desktop-Sync-Token": self.token,
        }
        
    def buscar_tarjetas_por_nombre(self, texto: str, limite: int = 15):
        termino = (texto or "").strip()
        if not termino:
            return []
        
        response = requests.get(
             f"{self.base_url}/api/tarjetas/buscar",
            params={
                "texto": termino,
                "limite": limite,
            },
            headers=self._headers(),
            timeout=self.timeout,
        )
        response.raise_for_status()
        data = response.json()
        return data.get("items", [])
    
    def sustituir_tarjeta(
        self,
        *,
        uid_anterior: str,
        uid_nueva: str,
        nueva_vigencia: str,
    ):
        payload = {
            "uid_anterior": (uid_anterior or "").strip().upper(),
            "uid_nueva": (uid_nueva or "").strip().upper(),
            "nueva_vigencia": (nueva_vigencia or "").strip(),
        }
        response = requests.post(
            f"{self.base_url}/api/tarjetas/sustituir",
            json=payload,
            headers=self._headers(),
            timeout=self.timeout,
        )
        response.raise_for_status()
        data = response.json()

        if not data.get("ok", False):
            raise ValueError(data.get("message", "No se pudo sustituir la tarjeta."))

        return data