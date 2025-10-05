from __future__ import annotations
from typing import Any, Protocol

# ── Вспомогательные протоколы (минимум для IDE и тайпчекера) ───────────

class _RuntimeConfig(Protocol):
    task_alias: str
    parser_alias: str
    max_concurrent_tasks: int
    request_delay_sec: float
    use_proxy: bool
    extra: dict[str, Any] | None

class _Logger(Protocol):
    def debug(self, msg: str, *args: Any, **kwargs: Any) -> None: ...
    def info(self, msg: str, *args: Any, **kwargs: Any) -> None: ...
    def warning(self, msg: str, *args: Any, **kwargs: Any) -> None: ...
    def error(self, msg: str, *args: Any, **kwargs: Any) -> None: ...

class _QueryQueue(Protocol):
    async def push(self, item: Any) -> None: ...

class _ProxyController(Protocol):
    async def current(self) -> Any: ...
    async def ban(self) -> None: ...

class _RequestOptions(Protocol):
    timeout: float | int | None
    retries: int | None

class _HTTPResult(Protocol):
    status: int | None
    body: Any
    def success(self) -> bool: ...
    @property
    def retried(self) -> int: ...

# ── Публичный контракт BaseParser для клиентов ─────────────────────────

class BaseParser:
    # Доступные атрибуты
    config: _RuntimeConfig
    logger: _Logger
    queue: _QueryQueue
    proxy: _ProxyController | None

    # Класс-константы (если нужны в аннотациях)
    DEFAULT_EXTRA: dict[str, Any]
    DEFAULT_PLUGINS: dict[str, Any]
    RESOURCE_PERIOD: float

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

    # HTTP запросы
    async def request(
        self,
        method: str,
        url: str,
        params: dict[str, Any] | None = ...,
        body: Any | None = ...,
        options: _RequestOptions | None = ...,
    ) -> _HTTPResult: ...
