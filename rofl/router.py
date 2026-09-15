import sys

from collections.abc import Sequence, Mapping, Callable
from typing import Any, Protocol

from .exceptions import RofiRoutingException

from .request import RofiRequest
from .request import RofiRequestType as RType


class HasRofiRequest(Protocol):
    def __call__(self, request: RofiRequest, *args: Any, **kwargs: Any) -> Any: ...


class RofiRouter:
    def __init__(self, req: RofiRequest | None):
        self._routes: dict[RType, Callable[..., Any] | None] = {
            RType.INITIAL: None,
            RType.SELECTED: None,
            RType.CUSTOM_INPUT: None,
            RType.DELETED: None,
        }
        self._custom: dict[int, Callable[..., Any]] = {}

        self._request = req
        self._fallback: Callable[..., Any] | None = None


    def run(self, *args: Any, **kwargs: Any) -> None:
        """Finds and executes the bound function securely."""
        if self._request is None:
            raise RofiRoutingException("Cannot route when RofiRequest is None")

        if (handler := self._routes.get(self._request.event)) is not None:
            handler(self._request, *args, **kwargs)
            return

        if (
            self._request.custom_key
            and (handler := self._custom.get(self._request.custom_key)) is not None
        ):
            handler(self._request, *args, **kwargs)
            return

        if self._fallback is not None:
            self._fallback(self._request, *args, **kwargs)
            return

        return

    def write(self, str: str) -> None:
        _ = sys.stdout.write(str)

    def debug(self, *values: object) -> None:
        print(*values, file=sys.stderr)

    @classmethod
    def from_environment(
        cls,
        argv: Sequence[str] | None = None,
        environ: Mapping[str, str] | None = None,
    ) -> "RofiRouter":
        req = RofiRequest.from_environment(argv, environ)
        return RofiRouter(req)

    def bind_fb[F: HasRofiRequest](self) -> Callable[[F], F]:
        """A decorator factory that enforces RofiRequest as the first argument."""

        def decorator(func: F) -> F:
            self._fallback = func
            return func

        return decorator

    def bind[F: HasRofiRequest](self, event_type: RType) -> Callable[[F], F]:
        """A decorator factory that enforces RofiRequest as the first argument."""

        def decorator(func: F) -> F:
            self._routes[event_type] = func
            return func

        return decorator

    def bind_custom[F: HasRofiRequest](self, custom_index: int) -> Callable[[F], F]:

        def decorator(func: F) -> F:
            if 1 > custom_index > 19:
                raise RofiRoutingException("custom index must be between 1-19")

            self._custom[custom_index] = func
            return func

        return decorator
