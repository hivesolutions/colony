from os import PathLike
from re import Pattern
from typing import Literal, Sequence

HashType = Literal["md5", "sha1", "sha256"]

HASH_VALUE: str
VALUE_VALUE: str
PLAIN_VALUE: str
MD5_VALUE: str
SHA1_VALUE: str
SHA256_VALUE: str
MD5_CRYPT_SEPARATOR: str
DEFAULT_MD5_CRYPT_MAGIC: str
DEFAULT_HASH_SET: HashType
INTEGER_TO_ASCII_64: str
PASSWORD_VALUE_REGEX_VALUE: str
NUMBER_REGEX_VALUE: str
LETTER_LOWER_REGEX_VALUE: str
LETTER_UPPER_REGEX_VALUE: str
SPECIAL_CHARACTER_REGEX_VALUE: str
PASSWORD_VALUE_REGEX: Pattern[str]
NUMBER_REGEX: Pattern[str]
LETTER_LOWER_REGEX: Pattern[str]
LETTER_UPPER_REGEX: Pattern[str]
SPECIAL_CHARACTER_REGEX: Pattern[str]

def password_crypt(
    password: str, salt: str = ..., hash_method: HashType = ...
) -> str: ...
def password_match(password_hash: str, password: str, salt: str = ...) -> bool: ...
def password_strength(password: str) -> int: ...
def md5_crypt(password: str, salt: str, magic: str = ...) -> str: ...
def generate_hash_digest_map(
    file_path: PathLike[str], hash_set: Sequence[str] = ...
): ...
