from __future__ import annotations

from typing import Callable, Optional
import pathlib
import os
from functools import wraps

from ._types import Maybe, Wrapper


def handle_os_exceptions(
    func: Callable[[pathlib.Path], list[pathlib.Path]]
) -> Callable[[pathlib.Path], list[pathlib.Path]]:
    @wraps(func)
    def inner(path: pathlib.Path) -> list[pathlib.Path]:
        try:
            return func(path)
        except (PermissionError, OSError):
            ...
    return inner


@Wrapper
def lsfiles(
    handlers: Callable[[pathlib.Path], Optional[pathlib.Path]]
) -> Callable[[pathlib.Path], list[pathlib.Path]]:
    files: list[pathlib.Path] = []

    @handle_os_exceptions
    @wraps(handlers)
    def inner(path: pathlib.Path) -> list[pathlib.Path]:
        nonlocal files
        
        with os.scandir(path) as dir_content:
            for entry in dir_content:
                if entry.is_dir(follow_symlinks=False):
                    inner(pathlib.Path(entry.path))
                else:
                    (
                        Maybe
                        .unit(pathlib.Path(entry.path))
                        .bind(handlers)
                        .bind(files.append)
                    )
        return files
    return inner
