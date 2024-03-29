from os import PathLike
from typing import Sequence

BUFFER_SIZE: int
LONG_PATH_PREFIX: str
CURRENT_DIRECTORY: str
PARENT_DIRECTORY: str
SEPARATOR: str
NT_PLATFORM_VALUE: str
CE_PLATFORM_VALUE: str
DOS_PLATFORM_VALUE: str
WINDOWS_PLATFORMS_VALUE: Sequence[str]

def normalize_path(path: PathLike[str]) -> PathLike[str]: ...
def align_path(path: PathLike[str]) -> PathLike[str]: ...
def copy_directory(
    source_path: PathLike[str],
    target_path: PathLike[str],
    replace_files: bool = ...,
    copy_hidden: bool = ...,
) -> None: ...
def copy_link(
    source_path: PathLike[str], target_path: PathLike[str], replace_file: bool = ...
): ...
def copy_file(
    source_path: PathLike[str], target_path: PathLike[str], replace_file: bool = ...
): ...
def remove_directory(directory_path: PathLike[str]) -> None: ...
def link(
    target_path: PathLike[str],
    link_path: PathLike[str],
    link_name: bool = ...,
    replace: bool = ...,
): ...
def link_copy(target_path: PathLike[str], link_path: PathLike[str]): ...
def ensure_file_path(file_path: PathLike[str], default_file_path: PathLike[str]): ...
def is_parent_path(path: PathLike[str], parent_path: PathLike[str]) -> bool: ...
def _relative_path_windows(
    path: PathLike[str], start_path: PathLike[str] = ...
) -> PathLike[str]: ...
def _relative_path_posix(
    path: PathLike[str], start: PathLike[str] = ...
) -> PathLike[str]: ...
def _abspath_split(
    path: PathLike[str],
) -> tuple[bool, PathLike[str], Sequence[PathLike[str]]]: ...
