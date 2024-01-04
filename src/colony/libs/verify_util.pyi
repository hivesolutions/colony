from colony.base import exceptions as exceptions

def verify(
    condition,
    message: str | None = ...,
    code: int | None = ...,
    exception: Exception | None = ...,
    **kwargs
) -> None: ...
def verify_equal(
    first,
    second,
    message: str | None = ...,
    code: int | None = ...,
    exception: Exception | None = ...,
    **kwargs
) -> None: ...
def verify_not_equal(
    first,
    second,
    message: str | None = ...,
    code: int | None = ...,
    exception: Exception | None = ...,
    **kwargs
) -> None: ...
def verify_type(
    value,
    types,
    null: bool = ...,
    message: str | None = ...,
    code: Exception | None = ...,
    exception: Exception | None = ...,
    **kwargs
) -> None: ...
def verify_many(
    sequence,
    message: str | None = ...,
    code: int | None = ...,
    exception: Exception | None = ...,
    **kwargs
) -> None: ...
