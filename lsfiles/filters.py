from typing import Optional, Callable, Generic
import os
import os.path
import re


def _ext(extensions: set[str]) -> Callable[[os.DirEntry], Optional[os.DirEntry]]:
    def inner(file: os.DirEntry) -> Optional[os.DirEntry]:
        _, ext = os.path.splitext(file.name)
        return file if ext.lower() in extensions else None

    return inner


def _name(name: str) -> Callable[[os.DirEntry], Optional[os.DirEntry]]:
    def inner(file: os.DirEntry) -> Optional[os.DirEntry]:
        return file if name in file.name else None

    return inner


def _dotfiles(file: os.DirEntry) -> Optional[os.DirEntry]:
    return file if file.name[0] != "." else None


def _regex(
    pattern: str | re.Pattern,
) -> Callable[[os.DirEntry], Optional[os.DirEntry]]:
    pat = re.compile(pattern) if isinstance(pattern, str) else pattern

    def inner(file: os.DirEntry) -> Optional[os.DirEntry]:
        return file if pat.search(file.name) else None

    return inner


def _exclude_path(
    pattern: str | re.Pattern,
) -> Callable[[os.DirEntry], Optional[os.DirEntry]]:
    pat = re.compile(pattern) if isinstance(pattern, str) else pattern

    def inner(file: os.DirEntry) -> Optional[os.DirEntry]:
        return None if pat.search(file.path) else file

    return inner


# f_ext = Wrapper(_f_ext)
# f_name = Wrapper(_f_name)
# f_dotfiles = Wrapper(_f_dotfiles)
# f_regex = Wrapper(_f_regex)

ext = _ext
name = _name
dotfiles = _dotfiles
regex = _regex
exclude_path = _exclude_path
