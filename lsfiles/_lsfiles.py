from __future__ import annotations

from collections import deque
from typing import Callable, Optional, Any, Union
import os
import os.path
from functools import wraps
import sys
import pathlib

from ._types import Maybe, LSFilesError


def handle_os_exceptions(
    func: Callable[[os.DirEntry, int], list[Any]]
) -> Callable[[os.DirEntry, int], list[Any]]:
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


def _main(cwd: pathlib.PurePath) -> int:
    def l(file):
        p = pathlib.Path(file)
        return p.suffix, p.stat().st_size

    ext: list[str] = list(
        f
        for f in iterativeDFS(
            lambda f: f,
            l,
            cwd,
        )
    )
    from collections import defaultdict
    from rich.console import Console
    from rich.table import Table

    table = Table(title="Size allocation per extension")

    table.add_column("extension", justify="left", style="cyan", no_wrap=True)
    table.add_column("size (bytes)", justify="left", style="magenta")

    res = defaultdict(int)
    import math

    def convert_size(size_bytes):
        if size_bytes == 0:
            return "0B"
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return "%s %s" % (s, size_name[i])

    for e, s in ext:
        res[e] += int(s)
    if sys.stdout.isatty():
        [
            table.add_row(k, convert_size(v))
            for k, v in sorted(
                [(k, v) for k, v in res.items()], key=lambda item: item[1], reverse=True
            )
        ]
        console = Console()
        console.print(table)
    else:
        sys.stdout.write("\n".join([f"{k} {v}" for k, v in res.items()]))

    return 0


def main() -> int:
    cwd = pathlib.PurePath(os.getcwd())
    print(f"{cwd=}")
    if len(sys.argv) != 2 or sys.argv[1] != "ext":
        return 1
    sys.exit(_main(cwd))


# files = lsfiles(
#     f_regex(r'.png') | f_predicate
#     | f_dotfiles
#     | f_ext()
#     | f_name('')
# )(root)
