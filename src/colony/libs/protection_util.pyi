from typing import Callable, TypeVar

PUBLIC_VALUE: str

C = TypeVar("C", bound=Callable)

def public(function: C) -> C: ...

class Protected:
    def __new__(cls, *args, **kwargs): ...
