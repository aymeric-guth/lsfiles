from typing import Optional, Callable, Generic
import os
import os.path
import re

from ._types import EntryWrapper


def _ext(
    extensions: set[str]
) -> Callable[[EntryWrapper], Optional[EntryWrapper]]:
    def inner(file: EntryWrapper) ->  Optional[EntryWrapper]:
        _, ext = os.path.splitext(file.name)
        return file if ext.lower() in extensions else None
    return inner


def _name(
    name: str
) -> Callable[[EntryWrapper], Optional[EntryWrapper]]:
    def inner(file: EntryWrapper) ->  Optional[EntryWrapper]:
        return file if name in file.name else None
    return inner


def _dotfiles(file: EntryWrapper) ->  Optional[EntryWrapper]:
    return file if file.name[0] != '.' else None


def _regex(
    pattern: str
) -> Callable[[EntryWrapper], Optional[EntryWrapper]]:
    pat = re.compile(pattern) if isinstance(pattern, str) else pattern
    def inner(file: EntryWrapper) -> Optional[EntryWrapper]:
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
