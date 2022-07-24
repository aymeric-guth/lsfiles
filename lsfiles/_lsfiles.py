from __future__ import annotations

from collections import deque
from typing import Callable, Optional, Any, Union, Generic
import os
import os.path
from functools import wraps

from ._types import Maybe, EntryWrapper, InPath, PathGeneric, LSFilesError


def handle_os_exceptions(
    func: Callable[[os.DirEntry, Optional[int]], list[PathGeneric]]
) -> Callable[[os.DirEntry, Optional[int]], list[PathGeneric]]:
    @wraps(func)
    def inner(*args, **kwargs) -> Any:
        try:
            return func(*args, **kwargs)
        except (PermissionError, OSError):
            ...

    return inner


def recursiveDFS(
    filters: Union[
        Callable[[os.DirEntry], Maybe], Callable[[os.DirEntry], Optional[os.DirEntry]]
    ],
    adapter: Callable[[os.DirEntry], PathGeneric],
) -> Callable[[os.DirEntry, Optional[int]], list[PathGeneric]]:
    files: list[PathGeneric] = []

    @handle_os_exceptions
    def inner(path: os.DirEntry, depth: Optional[int] = -1) -> list[PathGeneric]:
        nonlocal files

        if not depth:
            return files

        with os.scandir(path) as dir_content:
            for entry in dir_content:
                if entry.is_dir(follow_symlinks=False):
                    inner(entry, depth - 1)
                else:
                    (Maybe.unit(entry).bind(filters).bind(adapter).bind(files.append))
        return files

    return inner


# FileNotFoundError, PermissionError, OSError
def iterativeDFS(
    filters: Union[
        Callable[[os.DirEntry], Maybe], Callable[[os.DirEntry], Optional[os.DirEntry]]
    ],
    adapter: Callable[[os.DirEntry], PathGeneric],
    root: os.PathLike,
) -> list[PathGeneric]:
    stack: list[os.PathLike] = [root]
    files: list[PathGeneric] = []

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
    adapter: Callable[[os.DirEntry], PathGeneric],
    root: os.PathLike,
) -> list[PathGeneric]:
    queue: deque[os.PathLike] = deque([root])
    files: list[PathGeneric] = []

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


def is_git_repo(root: os.PathLike) -> bool:
    ...
