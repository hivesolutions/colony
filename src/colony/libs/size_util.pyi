from typing import Sequence

SIZE_UNITS_LIST: Sequence[str]
SIZE_UNIT_COEFFICIENT: int
DEFAULT_MINIMUM: int

def size_round_unit(
    size_value: int, minimum: int = ..., space: bool = ..., depth: int = ...
) -> str: ...
