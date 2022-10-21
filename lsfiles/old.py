from typing import Callable, List, Set, Any
from os import DirEntry, scandir, lstat
from os.path import splitext, getsize
from pathlib import Path
from functools import wraps, partial
from datetime import datetime


def handle_os_exceptions(fnc: Callable[[Any], Any]) -> Callable[[Any], Any]:
    @wraps(fnc)
    def inner(*args, **kwargs) -> Any:
        try:
            return fnc(*args, **kwargs)
        except (PermissionError, OSError) as err:
            print(
                f"{fnc.__name__} called *args: {args} **kwargs: {kwargs}\nexception occured: {err}"
            )
            return

    return inner


def lsfiles(fnc: Callable[[List[Any], DirEntry], None]) -> Callable[[str], List[Any]]:
    files_list: List[Any] = []

    @handle_os_exceptions
    @wraps(fnc)
    def _lsfiles(path: Path) -> List[Any]:
        nonlocal fnc
        nonlocal files_list

        with scandir(path) as dir_content:
            for i in dir_content:
                if i.is_dir(follow_symlinks=False):
                    _lsfiles(Path(i.path))
                else:
                    fnc(files_list, i)

        return files_list

    return _lsfiles


def filter_extensions(extensions: Set[str]) -> Callable[[List[Any], DirEntry], None]:
    def inner(files_list: List[Any], i: DirEntry) -> None:
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
            res = (path, file_name, extension)
            files_list.append(res)

    return inner


def filter_none(files_list: List[Any], i: DirEntry) -> None:
    file_name, extension = splitext(i.name)
    extension = extension.lower()
    offset = len(i.path) - len(i.name)
    path = i.path[:offset]
    res = (i.inode(), (path, file_name, extension))
    files_list.append(res)


def filter_meta(files_list: List[Any], i: DirEntry) -> None:
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
        datetime.fromtimestamp(fstat_.st_ctime),
    )
    files_list.append(res)


def f(files_list: List[Any], i: DirEntry):
    file_name, extension = splitext(i.name)
    if extension in {".jpeg", ".jpg", ".png"}:
        files_list.append((file_name, extension))
        # files_list.append(f'{file_name}{extension}')


def fmpy(files_list: List[Any], i: DirEntry):
    if "__pycache__" in i.path:
        return
    elif i.name[0] == ".":
        return
    else:
        files_list.append(i.path)


if __name__ == "__main__":
    path: Path = Path("/Users/yul/Downloads")
    extensions = {".jpeg", ".jpg", ".png", ".mp3", ".mp4", ".pdf"}
    # fnc = partial(full, extensions=extensions)
    fnc = filter_extensions(extensions=extensions)
    # filter_none
    files_list = lsfiles(fnc=fnc)(path=path)
    print(len(files_list))


# (dirent) -> dirent | None
# (files_list) -> None
# (dirent|None, files_list) -> None
# => filtre => si oui ajoute resutats | si non rien
