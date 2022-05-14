from typing import Optional, Callable
import os
import os.path
import pathlib
import re

from ._types import Wrapper, T


def _ext(
    extensions: set[str]
) -> Callable[[pathlib.Path], Optional[pathlib.Path]]:
    def inner(file: pathlib.Path) ->  Optional[pathlib.Path]:
        return file if file.suffix.lower() in extensions else None
    return inner


def _name(
    name: str
) -> Callable[[pathlib.Path], Optional[pathlib.Path]]:
    def inner(file: pathlib.Path) ->  Optional[pathlib.Path]:
        return file if name in file.name else None
    return inner


def _dotfiles(file: pathlib.Path) ->  Optional[pathlib.Path]:
    return file if file.name[0] != '.' else None


def _regex(
    pattern: str
) -> Callable[[pathlib.Path], Optional[pathlib.Path]]:
    pat = re.compile(pattern) if isinstance(pattern, str) else pattern
    def inner(file: pathlib.Path) -> Optional[pathlib.Path]:
        return file if pat.search(file.name) else None
    return inner


# f_ext = Wrapper(_f_ext)
# f_name = Wrapper(_f_name)
# f_dotfiles = Wrapper(_f_dotfiles)
# f_regex = Wrapper(_f_regex)

ext = _ext
name = _name
dotfiles = _dotfiles
regex = _regex
