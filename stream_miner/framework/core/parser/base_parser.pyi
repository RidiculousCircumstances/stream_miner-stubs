from __future__ import annotations

from http.client import HTTPResponse
from pathlib import Path
from typing import Any, Protocol

from stream_miner.framework.core.http.request_adapter import RequestOptions


# ── Вспомогательные протоколы (минимум для IDE и тайпчекера) ───────────

class _Logger(Protocol):
    def debug(self, msg, *args, **kwargs) -> None: ...

    def info(self, msg, *args, **kwargs) -> None: ...

    def warning(self, msg, *args, **kwargs) -> None: ...

    def error(self, msg, *args, **kwargs) -> None: ...

    def exception(self, msg, *args, exc_info=True, **kwargs): ...

    def critical(self, msg, *args, **kwargs) -> None: ...

    def log(self, level, msg, *args, **kwargs) -> None: ...


class _QueryQueue(Protocol):
    async def push(self, item: str) -> None: ...

    def len(self) -> int: ...


class _ProxyController(Protocol):
    async def current(self) -> str: ...

    async def ban(self) -> str: ...

    async def next(self) -> str: ...


# ── Публичный контракт BaseParser для клиентов ─────────────────────────

class BaseParser:
    logger: _Logger
    queue: _QueryQueue
    proxy: _ProxyController | None

    # Класс-константы (если нужны в аннотациях)
    DEFAULT_EXTRA: dict[str, Any]

    def __init__(self, *args: Any, **kwargs: Any) -> None: ...

    # Жизненный цикл — то, что клиент может переопределять
    async def init(self) -> None: ...

    async def destroy(self) -> None: ...

    async def init_thread(self) -> None: ...

    async def destroy_thread(self) -> None: ...

    # Главный абстрактный метод клиента
    async def parse(self, query: Any) -> None: ...

    # Утилиты
    def thread_id(self) -> str: ...

    @property
    def local(self) -> dict[str, Any]: ...

    def results_dir(self) -> Path: ...

    # HTTP запросы
    async def request(
            self,
            method: str,
            url: str,
            params: dict[str, Any] | None = ...,
            body: Any | None = ...,
            options: RequestOptions | None = ...,
    ) -> HTTPResponse: ...
