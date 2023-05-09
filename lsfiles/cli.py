import os
import sys
import pathlib
import math
import pdb

from collections import defaultdict
from rich.console import Console
from rich.table import Table
from utils import cli

from ._lsfiles import iterativeDFS
from . import filters


def main(pwd: str) -> tuple[str, int]:
    """
    usage:
    lsf ext
    recursively lists all extension and total size on disk per extension
    """
    cwd: pathlib.PurePath = pathlib.PurePath(pwd)
    ext: list[str] = list(
        f
        for f in iterativeDFS(
            filters=lambda f: f,
            adapter=lambda f: (lambda p: (p.suffix, p.stat().st_size))(pathlib.Path(f)),
            root=cwd,
        )
    )

    table = Table(title="Size allocation per extension")

    table.add_column("extension", justify="left", style="cyan", no_wrap=True)
    table.add_column("size (bytes)", justify="left", style="magenta")

    res = defaultdict(int)

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
        return cli.success()
    return cli.success("\n".join([f"{k} {v}" for k, v in res.items()]))


def ext_finder(pwd: str, *args) -> tuple[str, int]:
    """
    usage:
    lsf ext [ext1, ext2, ...]
    recursively lists all files matching list of extensions
    """

    cwd: pathlib.PurePath = pathlib.PurePath(pwd)

    files: list[pathlib.Path] = iterativeDFS(
        filters=filters.ext({f".{i}" for i in args}),
        adapter=pathlib.Path,
        root=cwd,
    )
    if not files:
        return cli.failure()
    return cli.success("\n".join([str(f) for f in files]))


def dir_finder(pwd: str) -> tuple[str, int]:
    cwd: pathlib.PurePath = pathlib.PurePath(pwd)
    files: list[str] = list(
        {
            i
            for i in iterativeDFS(
                filters=lambda f: f,
                adapter=lambda f: str(pathlib.Path(f).parent),
                root=cwd,
            )
        }
    )
    if not files:
        return cli.failure()

    files.sort()
    return cli.success("\n".join(files))


def files_finder(pwd: str) -> tuple[str, int]:
    cwd: pathlib.PurePath = pathlib.PurePath(pwd)
    files: list[str] = list(
        {
            i
            for i in iterativeDFS(
                filters=lambda f: f,
                adapter=lambda f: str(pathlib.Path(f)),
                root=cwd,
            )
        }
    )
    if not files:
        return cli.failure()

    files.sort()
    return cli.success("\n".join(files))


def file_density(pwd: str) -> tuple[str, int]:
    cwd: pathlib.PurePath = pathlib.PurePath(pwd)
    raise NotImplementedError


def _main() -> int:
    match sys.argv[1:]:
        case []:
            return cli.sh_fnc(files_finder)(os.getcwd())
        case ["ext"]:
            return cli.sh_fnc(main)(os.getcwd())
        case ["ext", *args]:
            return cli.sh_fnc(ext_finder)(os.getcwd(), *args)
        case ["dir"]:
            return cli.sh_fnc(dir_finder)(os.getcwd())
        case ["files"]:
            return cli.sh_fnc(file_density)(os.getcwd())
        case _:
            return cli.sh_fnc(cli.failure)(f"{main.__doc__}")
