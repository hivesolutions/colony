from typing import Any, Mapping, Sequence, Type

TOPPER_VALUE: str
LIST_TYPES: Sequence[Type]
INVALID_ATTRIBUTE_NAMES: Sequence[str]
VALID_ATTRIBUTE_TYPES: Sequence[Type]

def object_attribute_names(instance: Any) -> Sequence[str]: ...
def object_attribute_values(
    instance: Any,
    valid_attribute_names: Sequence[str] | None = ...,
    strict: bool = ...,
) -> Sequence[Any]: ...
def object_flatten(
    instance: Any, flattening_map: Mapping[Any, Any]
) -> Sequence[Any]: ...
def object_print_list(instances_list: Sequence[Any]): ...
def object_print(instance: Any): ...
def _object_flatten(
    instances_list: Sequence[Any], flattening_map: Mapping[Any, Any]
) -> Sequence[Any]: ...
