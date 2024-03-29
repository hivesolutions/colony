from typing import Any, Mapping, TypeVar

GLOBALS: Mapping[str, Any] = ...

T = TypeVar("T")

def set_global(name: str, value: Any) -> None: ...
def get_global(name: str, default: T | None = ...) -> T | None: ...
def has_global(name: str) -> bool: ...
