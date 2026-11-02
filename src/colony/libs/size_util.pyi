from typing import Sequence

SIZE_UNITS_LIST: Sequence[str]
SIZE_UNITS_LIST_S: Sequence[str]
SIZE_UNIT_COEFFICIENT: int
DEFAULT_MINIMUM: int
DEFAULT_PLACES: int

def size_round_unit(
    size_value: int | float,
    minimum: int = ...,
    space: bool = ...,
    depth: int = ...,
    places: int = ...,
    reduce: bool = ...,
    justify: bool = ...,
    simplified: bool = ...,
) -> str: ...
