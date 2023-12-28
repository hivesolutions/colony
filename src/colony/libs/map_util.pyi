from typing import Any, Callable, Generator, Mapping, Sequence, Type, TypeVar

T = TypeVar("T")
V = TypeVar("V")

def map_clean(map: Mapping[Any, Any]): ...
def map_get(map: Mapping[Any, Any], keys: Sequence[Any] = []): ...
def map_copy(source_map: Mapping[Any, Any], destiny_map: Mapping[Any, Any]): ...
def map_copy_deep(source_map: Mapping[Any, Any], destiny_map: Mapping[Any, Any]): ...
def map_duplicate(item: Any) -> Any: ...
def map_remove(removal_map: Mapping[Any, Any], destiny_map: Mapping[Any, Any]): ...
def map_extend(
    base_map: Mapping[Any, Any],
    extension_map: Mapping[Any, Any],
    override: bool = ...,
    recursive: bool = ...,
    copy_base_map: bool = ...,
): ...
def map_flatten(map: Mapping[str, Any]) -> Mapping[str, Any]: ...
def map_check_parameters(
    map: Mapping[T, Any], parameters_list: Sequence[T], exception: Type[Exception] = ...
): ...
def map_get_value_cast(
    map: Mapping[T, Any], key: T, cast_type: Type = ..., default_value: Any | None = ...
) -> Any: ...
def map_get_values(map: Mapping[T, Any], key: T) -> Sequence[Any]: ...
def map_output(
    map: Mapping[Any, Any],
    output_method: Callable[[bytes | str], Any] = ...,
    indentation: str = ...,
): ...
def map_normalize(item: T, operation: Callable[[T], Any] | None = ...) -> Any: ...
def _map_flatten_pairs(map: Mapping[T, V]) -> Generator[tuple[T, V], None, None]: ...
def _map_reduce(value: Any) -> Any: ...
