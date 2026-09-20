"""Keepalive para mantener el servicio activo entre consultas.

En entornos como Render (plan gratuito/free) el servicio se suspende por
inactividad tras varios minutos sin peticiones. Este módulo mantiene el
proceso despierto lanzando peticiones HTTP periódicas a una URL mediante un
cliente asíncrono gestionado por el ciclo de vida de la aplicación
(`lifespan` de FastAPI).

La configuración se realiza exclusivamente mediante variables de entorno:

- ``KEEPALIVE_URL``: URL a pinguear (normalmente la propia
  ``PUBLIC_SITE_URL/keepalive`` o ``PUBLIC_SITE_URL/health``).
  Si está vacía o no se define, el keepalive se desactiva por completo y no
  se inicia el cliente: no afecta al entorno local ni a los tests.
- ``KEEPALIVE_INTERVAL_SECONDS``: segundos entre peticiones (default ``300``).
- ``KEEPALIVE_TIMEOUT_SECONDS``: timeout de cada petición en segundos
  (default ``10``).

Ejemplo en ``.env``::

    KEEPALIVE_URL=https://midominio.com/keepalive
    KEEPALIVE_INTERVAL_SECONDS=300
    KEEPALIVE_TIMEOUT_SECONDS=10
"""

from __future__ import annotations

import asyncio
import logging
import os
from typing import Any

import httpx

logger = logging.getLogger(__name__)

DEFAULT_INTERVAL_SECONDS = 300
DEFAULT_TIMEOUT_SECONDS = 10


def _env_int(name: str, default: int) -> int:
    """Lee un entero de entorno con fallback seguro al valor por defecto."""
    raw = os.getenv(name, "").strip()
    if not raw:
        return default
    try:
        value = int(raw)
        return value if value > 0 else default
    except ValueError:
        return default


def keep_alive_config() -> dict[str, Any]:
    """Lee la configuración de keepalive del entorno.

    Devuelve ``enabled=False`` cuando ``KEEPALIVE_URL`` no está definida o
    está vacía, de modo que el resto del sistema se desactive limpio.
    """
    url = os.getenv("KEEPALIVE_URL", "").strip()
    return {
        "enabled": bool(url),
        "url": url,
        "interval": _env_int("KEEPALIVE_INTERVAL_SECONDS", DEFAULT_INTERVAL_SECONDS),
        "timeout": _env_int("KEEPALIVE_TIMEOUT_SECONDS", DEFAULT_TIMEOUT_SECONDS),
    }


class KeepAliveClient:
    """Cliente HTTP asíncrono que pinguea periódicamente una URL.

    El bucle se detiene de forma limpia cuando se solicita ``stop()`` y/o al
    cerrarse el cliente HTTP al finalizar el ``async with`` interno.
    """

    def __init__(
        self,
        url: str,
        interval: int = DEFAULT_INTERVAL_SECONDS,
        timeout: int = DEFAULT_TIMEOUT_SECONDS,
    ) -> None:
        self.url = url
        self.interval = interval
        self.timeout = timeout
        self._client: httpx.AsyncClient | None = None
        self._task: asyncio.Task | None = None
        self._stop: asyncio.Event | None = None

    async def _loop(self) -> None:
        timeout = httpx.Timeout(self.timeout)
        async with httpx.AsyncClient(timeout=timeout) as client:
            self._client = client
            self._stop = asyncio.Event()
            while not self._stop.is_set():
                try:
                    response = await client.get(self.url)
                    logger.debug(
                        "keepalive: %s -> %s", self.url, response.status_code
                    )
                except Exception:
                    # Nunca debe propagarse: un ping fallido no debe morir el proceso.
                    logger.warning(
                        "keepalive: falló petición a %s", self.url, exc_info=True
                    )
                # Duerme `interval` segundos, pero se despierta al instante si se pide parar.
                try:
                    await asyncio.wait_for(self._stop.wait(), timeout=self.interval)
                except asyncio.TimeoutError:
                    # El intervalo expiró: repetir el ping.
                    continue

    async def start(self) -> None:
        """Inicia la tarea de keepalive en segundo plano."""
        if self._task is not None:
            return
        self._task = asyncio.create_task(self._loop(), name="keepalive")
        logger.info(
            "keepalive activado -> %s cada %ss (timeout %ss)",
            self.url,
            self.interval,
            self.timeout,
        )

    async def stop(self) -> None:
        """Detiene la tarea de keepalive de forma ordenada."""
        if self._task is None:
            return
        if self._stop is not None:
            self._stop.set()
        try:
            await self._task
        except Exception:  # noqa: BLE001
            logger.warning("keepalive: el bucle terminó con excepción", exc_info=True)
        finally:
            self._task = None
            self._client = None
            self._stop = None