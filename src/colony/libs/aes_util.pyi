BLOCK_SIZE: int

class AesCipher:
    key: bytes | None
    block_size = BLOCK_SIZE
    def __init__(self, key: bytes | None = None, block_size: int = ...): ...
    def encrypt(self, raw: bytes) -> bytes: ...
    def decrypt(self, encoded: bytes) -> bytes: ...
    def pad(self, value: bytes) -> bytes: ...
    def unpad(self, value: bytes) -> bytes: ...
    def get_key(self) -> bytes: ...
    def get_block_size(self) -> int: ...
