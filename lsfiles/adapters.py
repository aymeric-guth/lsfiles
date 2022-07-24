import os
import os.path
import pathlib


def vanilla(file: os.DirEntry) -> os.DirEntry:
    return file


def triplet(file: os.DirEntry) -> tuple[str, str, str]:
    (filename, ext) = os.path.splitext(file.name)
    path = file.path[: -len(file.name)]
    return (path, filename, ext)


def pathlib_purepath(file: os.DirEntry) -> pathlib.PurePath:
    return pathlib.PurePath(file)


def pathlib_path(file: os.DirEntry) -> pathlib.Path:
    return pathlib.Path(file)


def to_str(file: os.DirEntry) -> str:
    return file.path
