from signal import Signals
from typing import Sequence

WINDOWS_KILL_COMMAND: str
NT_PLATFORM_VALUE: str
DOS_PLATFORM_VALUE: str
WINDOWS_PLATFORMS_VALUE: Sequence[str]

def kill_process(pid: int, signal: Signals | None = ...): ...
def _kill_process_windows(pid: int): ...
def _kill_process_unix(pid: int, _signal: Signals | None = ...): ...
