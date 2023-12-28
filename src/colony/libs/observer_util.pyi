from typing import Any, Callable, Mapping, Sequence

HandlersMap = Mapping[str, Sequence[Callable]]

COUNTER: int
MESSAGE_VALUE: str
ACTION_VALUE: str
PROGRESS_VALUE: str
GLOBAL_HANDLERS_MAP: HandlersMap
KAFKA_PRODUCERS: Mapping[str, Any]
_KAFKA_CONFIG: Mapping[str, Any]

def unique() -> int: ...
def notify(
    operation_name: str,
    handlers_map: Mapping[str, Sequence[Callable]] | None = ...,
    *arguments,
    **named_arguments
) -> Any: ...
def message(
    handlers_map: HandlersMap | None = ..., *arguments, **named_arguments
) -> Any: ...
def action(
    handlers_map: HandlersMap | None = ..., *arguments, **named_arguments
) -> Any: ...
def progress(
    handlers_map: HandlersMap | None = ..., *arguments, **named_arguments
) -> Any: ...
def register_g(operation_name: str, handler: Callable): ...
def unregister_g(
    operation_name: str,
    handler: Callable | None = ...,
): ...
def notify_g(operation_name: str, *arguments, **named_arguments) -> Any: ...
def notify_b(operation_name: str, *arguments, **named_arguments): ...
def notify_kafka(operation_name: str, *arguments, **named_arguments): ...
def kafka_config() -> Mapping[str, Any]: ...
def _kafka_producer() -> Any: ...
