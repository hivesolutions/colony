from typing import Any, Iterator, TypeVar

T = TypeVar("T")

class LazyClass:
    def __repr__(self) -> str: ...
    def __hash__(self) -> int: ...
    def __eq__(self, other: Any) -> bool: ...
    def __ne__(self, other: Any) -> bool: ...
    def __add__(self, other: Any) -> Any: ...
    def __radd__(self, other: Any) -> Any: ...
    def __nonzero__(self) -> bool: ...
    def __len__(self) -> int: ...
    def __iter__(self) -> Iterator[Any]: ...

class LazyIteratorClass[T]:
    def __iter__(self) -> Iterator: ...
    def __next__(self) -> T: ...
    def next(self) -> T: ...

def is_lazy(value: Any) -> bool: ...

Lazy: LazyClass
LazyIterator: LazyIteratorClass
