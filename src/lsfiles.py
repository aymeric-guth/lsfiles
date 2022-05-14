from __future__ import annotations

from typing import Callable, Optional, Any, Union
import pathlib
import os
from functools import wraps

from ._types import Maybe, Wrapper


def handle_os_exceptions(
    func: Callable[[pathlib.Path], list[pathlib.Path]]
) -> Callable[[pathlib.Path, Optional[int]], list[pathlib.Path]]:
    @wraps(func)
    def inner(*args, **kwargs) -> Any:
        try:
            return func(*args, **kwargs)
        except (PermissionError, OSError):
            ...
    return inner


def lsfiles(
    handlers: Union[Maybe, Callable[[pathlib.Path], Optional[pathlib.Path]]]
) -> Callable[[pathlib.Path, Optional[int]], list[pathlib.Path]]:
    files: list[pathlib.Path] = []

    @handle_os_exceptions
    def inner(path: pathlib.Path, depth: Optional[int]=-1) -> list[pathlib.Path]:
        nonlocal files

        if not depth:
            return files        
        with os.scandir(path) as dir_content:
            for entry in dir_content:
                if entry.is_dir(follow_symlinks=False):
                    inner(pathlib.Path(entry.path), depth-1)
                else:
                    (
                        Maybe
                        .unit(pathlib.Path(entry.path))
                        .bind(handlers)
                        .bind(files.append)
                    )
        return files
    return inner
