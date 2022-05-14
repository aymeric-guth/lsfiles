from __future__ import annotations

from typing import Callable, List, Set, Any, Optional
import os
import pathlib
from os import DirEntry, scandir, lstat
from os.path import splitext, getsize
from pathlib import Path
from functools import wraps, partial
from datetime import datetime
from dataclasses import dataclass




class File:
    def __init__(self, p: os.DirEntry) -> None:
        self._p = p
        self._cache_path: Optional[pathlib.Path] = None
        self._cache_f: Optional[tuple[str, str]] = None
        self._filename: Optional[str] = None
        self._ext: Optional[str] = None

    def splitext(self) -> None:
        (filename, ext) = splitext(self._p.name)
        self._filename, self._ext = filename, ext.lower()

    @property
    def cache(self) -> str:
        if self._cache is None:
            self._cache = pathlib.Path(self._p.path)
        else:
            return self._cache

    @cache.setter
    def cache(self, value: Any) -> None:
        raise TypeError

    @property
    def filename(self) -> str:
        if self._filename is None:
            self.splitext()
        return self._filename

    @filename.setter
    def filename(self, value: Any) -> None:
        raise TypeError

    @property
    def ext(self) -> str:
        if self._ext is None:
            self.splitext()
        return self._ext

    @ext.setter
    def ext(self, value: Any) -> None:
        raise TypeError

    @property
    def path(self) -> pathlib.Path:
        return self._p.path

    @path.setter
    def path(self, value: Any) -> None:
        raise TypeError

    def __getattr__(self, __name: str) -> Any:
        if __name not in dir(self):
            return self._p.__getattribute__(__name)
        else:
            return self.__getattribute__(__name)



def handle_os_exceptions(
    fnc: Callable[[Any], Any]
) -> Callable[[Any], Any]:
    @wraps(fnc)
    def inner(*args, **kwargs) -> Any:
        try:
            return fnc(*args, **kwargs)
        except (PermissionError, OSError) as err:
            print(f"{fnc.__name__} called *args: {args} **kwargs: {kwargs}\nexception occured: {err}")
            return

    return inner


def lsfiles(
    fnc: Callable[[List[Any], DirEntry], None]
) -> Callable[[str], List[Any]]:
    files_list: List[Any] = []

    @handle_os_exceptions
    @wraps(fnc)
    def _lsfiles(path: File) -> List[Any]:
        nonlocal files_list
        
        with os.scandir(path) as dir_content:
            for i in dir_content:
                if i.is_dir(follow_symlinks=False): 
                    _lsfiles(File(i))
                else:
                    fnc(files_list, File(i))

        return files_list

    return _lsfiles


def filter_extensions(
    extensions: Set[str]
) -> Callable[[List[Any], DirEntry], None]:
    def inner(
        files_list: List[Any], 
        i: DirEntry
    ) -> None:
        """
        filter function according to extensions
        returns inode, path, filename, ext
        """
        nonlocal extensions
        
        file_name, extension = splitext(i.name)
        extension = extension.lower()
        if extension in extensions:
            offset = len(i.path) - len(i.name)
            path = i.path[:offset]
            # res = (
            #     i.inode(), 
            #     (path, file_name, extension)
            # )
            res = (
                path, 
                file_name, 
                extension
            )
            files_list.append(res)

    return inner


def filter_none(
    files_list: List[Any], 
    i: DirEntry
) -> None:
    file_name, extension = splitext(i.name)
    extension = extension.lower()
    offset = len(i.path) - len(i.name)
    path = i.path[:offset]
    res = (
        i.inode(), 
        (path, file_name, extension)
    )
    files_list.append(res)


def filter_meta(
    files_list: List[Any], 
    i: DirEntry
) -> None:
    file_name, extension = splitext(i.name)
    offset = len(i.path) - len(i.name)
    path = i.path[:offset]
    fstat_ = lstat(i)
    res = (
        path, 
        file_name, 
        extension, 
        getsize(i),
        fstat_.st_ino,
        datetime.fromtimestamp(fstat_.st_atime),
        datetime.fromtimestamp(fstat_.st_mtime),
        datetime.fromtimestamp(fstat_.st_ctime)
    )
    files_list.append(res)


def f(files_list: List[Any], i: DirEntry):
    file_name, extension = splitext(i.name)
    if extension in {'.jpeg', '.jpg', '.png'}:
        files_list.append((file_name,extension))
        # files_list.append(f'{file_name}{extension}')


def fmpy(files_list: List[Any], i: DirEntry):
    if '__pycache__' in i.path: return
    elif i.name[0] == '.': return
    else: files_list.append(i.path)


