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

    def _raise_for_status_con_mensaje(self, response: requests.Response) -> None:
        if response.status_code < 400:
            return

        mensaje = ""
        try:
            data = response.json()
            if isinstance(data, dict):
                mensaje = str(data.get("message") or data.get("error") or "").strip()
        except ValueError:
            mensaje = response.text.strip()

        if not mensaje:
            mensaje = f"HTTP {response.status_code}"

        raise RuntimeError(mensaje)
        
    def buscar_tarjetas_por_nombre(self, texto: str = "", limite: int = 50):
        termino = (texto or "").strip()
        
        response = requests.get(
             f"{self.base_url}/api/tarjetas/buscar",
            params={
                "texto": termino,
                "limite": limite,
                "incluir_lista_negra": 0,
            },
            headers=self._headers(),
            timeout=self.timeout,
        )
        self._raise_for_status_con_mensaje(response)
        data = response.json()
        return [
            self._normalizar_item_busqueda(item)
            for item in data.get("items", [])
            if not self._esta_en_lista_negra(item)
        ]

    def _esta_en_lista_negra(self, item: dict) -> bool:
        if not isinstance(item, dict):
            return False

        pasajero = item.get("pasajero")
        if not isinstance(pasajero, dict):
            pasajero = {}

        for value in (
            item.get("en_lista_negra"),
            item.get("lista_negra"),
            item.get("bloqueada"),
            pasajero.get("en_lista_negra"),
            pasajero.get("lista_negra"),
            pasajero.get("bloqueada"),
        ):
            if isinstance(value, bool):
                return value
            if isinstance(value, (int, float)):
                return value == 1

            texto = str(value or "").strip().lower()
            if texto in {"1", "true", "si", "yes", "y"}:
                return True

        return False

    def _normalizar_item_busqueda(self, item: dict) -> dict:
        if not isinstance(item, dict):
            return {}

        pasajero = item.get("pasajero")
        if not isinstance(pasajero, dict):
            pasajero = {}

        item = dict(item)
        item["curp"] = (
            item.get("curp")
            or item.get("curp_pasajero")
            or pasajero.get("curp")
            or ""
        )
        item["fecha_nacimiento"] = (
            item.get("fecha_nacimiento")
            or item.get("fecha_nacimiento_pasajero")
            or pasajero.get("fecha_nacimiento")
            or ""
        )
        return item
    
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
    
    def sustituir_tarjeta_servidor(
        self,
        *,
        uid_anterior: str,
        uid_nueva: str,
        nueva_vigencia: str,
        nombre_pasajero: str = "",
        tipo_codigo_local: str | None = None,
    ):
        payload = {
            "uid_anterior": (uid_anterior or "").strip().upper(),
            "uid_nueva": (uid_nueva or "").strip().upper(),
            "nueva_vigencia": (nueva_vigencia or "").strip(),
            "nombre_pasajero": (nombre_pasajero or "").strip(),
            "tipo_codigo_local": (tipo_codigo_local or "NO").strip().upper(),
        }

        response = requests.post(
            f"{self.base_url}/api/tarjetas/sustituir",
            json=payload,
            headers=self._headers(),
            timeout=self.timeout,
        )
        self._raise_for_status_con_mensaje(response)
        data = response.json()

        if not data.get("ok", False):
            raise ValueError(data.get("message", "No se pudo sustituir la tarjeta."))

        return data
