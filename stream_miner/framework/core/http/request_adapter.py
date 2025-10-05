from asyncio import Protocol
from typing import Dict, Callable, Set, Any

class HttpResponse:
    status:  int
    headers: Dict[str, str]
    body:    bytes

    def text(self, encoding="utf-8", errors="replace") -> str: ...

    def json(self) -> Any: ...

    def success(self) -> bool: ...

class RequestOptions(Protocol):
    headers:        Dict[str, str] | None
    check_content:  Callable[[HttpResponse], bool] | None
    use_proxy:      bool
    browser:        bool
    timeout:        float
    retries:        int | None
    allow_statuses: Set[int] | None
    delay:          float | None