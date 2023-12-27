from typing import Literal

CodeSet = Literal["A", "B", "C"]

DIGIT_ENCODING_MAP: dict[str, str]
START_CODE_2_OF_5: str
END_CODE_2_OF_5: str
START_CODES_CODE_128: dict[str, int]
END_CODE_CODE_128: int

def encode_2_of_5(string_value: str) -> str: ...
def encode_code_128(value: str, code_set: CodeSet = ...) -> str: ...
def encode_code_39(value: str) -> str: ...
