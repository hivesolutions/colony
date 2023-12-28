from typing import Mapping, Sequence

COUNTRIES: Sequence[str]
COUNTRIES_ISO: Mapping[str, tuple[str, str, str]]

def country_get(
    name: str, relaxed: bool = ...
) -> tuple[str, str, str] | tuple[None, None, None]: ...
