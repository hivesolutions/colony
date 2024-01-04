from datetime import datetime
from typing import Mapping, Sequence

DAY_VALUE: str
HOUR_VALUE: str
MINUTE_VALUE: str
SECOND_VALUE: str
SIMPLE_VALUE: str
BASIC_VALUE: str
EXTENDED_VALUE: str
EXTENDED_SIMPLE_VALUE: str
MINIMIZE_MULTIPLE: str
MINIMIZE_UNIQUE: str
DEFAULT_INCLUDES: tuple[str, str, str, str]
DEFAULT_FORMAT: str
FORMATS: Mapping[str, Mapping[str, str]]
SEPARATORS: dict[str, str]

def format_seconds_smart(
    seconds: int, mode: str = ..., includes: Sequence[str] = ..., minimize: str = ...
) -> str: ...
def format_seconds(seconds: int, format_string: str = ...) -> str: ...
def timestamp_datetime(timestamp_string: str) -> datetime: ...
