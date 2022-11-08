from __future__ import annotations

from collections import deque
from typing import Callable, Optional, Any, Union
import os
import os.path
from functools import wraps

from ._types import Maybe, LSFilesError


def handle_os_exceptions(
    func: Callable[[os.DirEntry, int], list[Any]]
) -> Callable[[os.DirEntry, int], list[Any]]:
    @wraps(func)
    def inner(*args, **kwargs) -> Any:
        try:
            return func(*args, **kwargs)
        except (FileNotFoundError, PermissionError, OSError):
            ...

    return inner


def recursiveDFS(
    filters: Union[
        Callable[[os.DirEntry], Maybe], Callable[[os.DirEntry], Optional[os.DirEntry]]
    ],
    adapter: Callable[[os.DirEntry], Any],
) -> Callable[[os.DirEntry, int], list[Any]]:
    files: list[Any] = []

    @handle_os_exceptions
    def inner(path: os.DirEntry, depth: int = -1) -> list[Any]:
        nonlocal files

        if depth == 0:
            return files

        with os.scandir(path) as dir_content:
            for entry in dir_content:
                if entry.is_dir(follow_symlinks=False):
                    if entry.name[0] != ".":
                        inner(entry, depth - 1)
                else:
                    (Maybe.unit(entry).bind(filters).bind(adapter).bind(files.append))
        return files

    return inner


def iterativeDFS(
    filters: Union[
        Callable[[os.DirEntry], Maybe], Callable[[os.DirEntry], Optional[os.DirEntry]]
    ],
    adapter: Callable[[os.DirEntry], Any],
    root: os.PathLike,
) -> list[Any]:
    stack: list[os.PathLike] = [root]
    files: list[Any] = []

    while stack:
        path = stack.pop()
        if not os.path.isdir(path):
            continue
        with os.scandir(path) as dir_content:
            for entry in dir_content:
                if entry.is_dir(follow_symlinks=False):
                    stack.append(entry)
                else:
                    (Maybe.unit(entry).bind(filters).bind(adapter).bind(files.append))
    return files


def iterativeBFS(
    filters: Union[
        Callable[[os.DirEntry], Maybe], Callable[[os.DirEntry], Optional[os.DirEntry]]
    ],
    adapter: Callable[[os.DirEntry], Any],
    root: os.PathLike,
) -> list[Any]:
    queue: deque[os.PathLike] = deque([root])
    files: list[Any] = []

    while queue:
        path = queue.popleft()
        if not os.path.isdir(path):
            continue
        with os.scandir(path) as dir_content:
            for entry in dir_content:
                if entry.is_dir(follow_symlinks=False):
                    queue.append(entry)
                else:
                    (Maybe.unit(entry).bind(filters).bind(adapter).bind(files.append))
    return files


def inode_exists(entry: os.PathLike) -> None:
    try:
        os.stat(entry)
    except FileNotFoundError as err:
        raise LSFilesError(str(err))


def is_leaf(root: os.PathLike) -> bool:
    stack: list[os.PathLike] = [root]
    inode_exists(root)

    if os.path.isfile(root):
        return True

    while stack:
        path = stack.pop()
        inode_exists(path)

        with os.scandir(path) as dir_content:
            for entry in dir_content:
                if entry.is_dir(follow_symlinks=False):
                    return False
    return True
