from os import PathLike
from typing import Any, Iterator, Mapping, Sequence, TypeVar

T = TypeVar("T")
K = TypeVar("K")
V = TypeVar("V")

FLOAT_PRECISION: int

class Decimal(float):
    places: int

    def __new__(cls, value: float = ...): ...

class JournaledList[T](list):
    def __init__(self, *args, **kwargs): ...
    def append(self, object: T): ...
    def remove(self, object: T): ...
    def clear_journal(self): ...
    def get_appends(self) -> Sequence[T]: ...
    def get_removes(self) -> Sequence[T]: ...

class OrderedMap[K, V]:
    tuples_list: Sequence[tuple[K, V]]

    def __init__(
        self, ordered_keys: bool = ..., map: Mapping[Any, Any] | None = ...
    ): ...
    def get(self, key: K, default_value: V | None = ...) -> V: ...
    def values(self) -> Sequence[V]: ...
    def items(self) -> Sequence[tuple[K, V]]: ...
    def extend(self, map: Mapping[K, V]): ...
    def keys(self) -> Sequence[K]: ...
    def itervalues(self) -> Iterator[V]: ...
    def iteritems(self) -> Iterator[tuple[K, V]]: ...
    def iterkeys(self) -> Iterator[K]: ...

class OrderedMapIterator[K, V]:
    ordered_map: OrderedMap[K, V]
    current_index: int

    def __init__(self, ordered_map: OrderedMap[K, V]): ...
    def next(self) -> V: ...

class MultipleValueMap[K, V]:
    def __init__(self): ...
    def get(
        self, key: K, default_value: V | Sequence[V] | None = ...
    ) -> V | Sequence[V]: ...
    def values(self) -> Sequence[V]: ...
    def items(self) -> Sequence[tuple[K, V]]: ...
    def keys(self) -> Sequence[K]: ...
    def itervalues(self) -> Iterator[V]: ...
    def iteritems(self) -> Iterator[tuple[K, V]]: ...
    def iterkeys(self) -> Iterator[K]: ...
    def unset(self, key: K, value: V): ...

class FormatTuple:
    format_string: str
    arguments: Sequence[Any]

    def __init__(self, format_string: str, *args): ...
    @staticmethod
    def build(format_string: str, *args) -> FormatTuple: ...
    def json_v(self, format: bool = ...): ...
    def format(self, format_string: str | None = ...): ...
    def get_format_string(self) -> str: ...
    def set_format_string(self, format_string: str): ...

class FileReference:
    path: PathLike[str]
    encoding: str | None

    def __init__(self, path: PathLike[str], encoding: str | None = ...): ...
    def read_all(self, mode: str = ...): ...

def is_dictionary(object: Any) -> bool: ...
