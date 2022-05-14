from __future__ import annotations
import os



files_list = []
extensions = set()

class DirEnt(object):
    def __init__(self, f: os.DirEntry) -> None:
        self.dir_entry: os.DirEntry = f
        self.file_name: str
        self.extension: str
        self.path: str
        self.inode: int = f.inode()
        self.file_name, self.extension = os.path.splitext(f.name)
        self.extension = self.extension.lower()
        self.path = f.path[:-len(f.name)]

    def __str__(self) -> str:
        return f"{self.path}\n{self.file_name}\n{self.extension}"

    def __lt__(self, other: DirEnt):
        assert isinstance(other, DirEnt)
        return self.inode < other.inode

    def __truediv__(self, other: DirEnt):
        assert isinstance(other, DirEnt)
        self.path = f"{self.path}{other.path}"
        return self
    # __floordiv__
    # __truediv__


def handle_os_exceptions(fnc):
    def inner(*args):
        try: return fnc(*args)
        except (PermissionError, FileNotFoundError, NotADirectoryError): pass
    return inner

def _lsfiles_extensions_inode_split(path):
    global extensions
    global files_list

    with os.scandir(path) as dir_content:
        for i in dir_content:
            if i.name[0] == ".":
                continue
            elif i.is_dir(follow_symlinks=False):
                _lsfiles_extensions_inode_split(i)
            else:
                dirEnt: DirEnt = DirEnt(i)
                if dirEnt.extension in extensions:
                    files_list.append(dirEnt)

# @handle_os_exceptions
# def _lsfiles_recursion_depth(path, recursion_depth=0):
#     if recursion_depth < 0: return

#     with os.scandir(path) as dir_content:
#         for i in dir_content:
#             if i.name[0] == ".":
#                 continue
#             elif i.is_dir(follow_symlinks=False):
#                 _lsfiles_recursion_depth(i, recursion_depth-1)
#             else:
#                 files_list.append(i)

# def _lsfiles_recursion_depth_split(path, recursion_depth=0):
#     if recursion_depth < 0: return

#     with os.scandir(path) as dir_content:
#         for i in dir_content:
#             if i.name[0] == ".":
#                 continue
#             elif i.is_dir(follow_symlinks=False):
#                 _lsfiles_recursion_depth_split(i, recursion_depth-1)
#             else:
#                 file_name, extension = os.path.splitext(i.name)
#                 extension = extension.lower()
#                 path = i.path[:-len(i.name)]
#                 files_list.append( (path, file_name, extension) )


class ListFiles(object):
    def __init__(self, args=None):
        pass

    def __call__(self, *args):
        global files_list
        global extensions

        path = args[0]
        if path is None:
            raise Exception("No path provided.")
        # if self.mode_extension and not(extensions):
        #     raise Exception("No extensions provided.")

        if isinstance(path, list):
            buffer = []
            for i in path:
                self.fnc(i)
                buffer.extend(files_list)
                files_list.clear()
        else:
            _lsfiles_extensions_inode_split(*args)

        if isinstance(path, str):
            buffer = files_list.copy()
        files_list.clear()

        return buffer

    def update_extensions(self, ext):
        global extensions

        if isinstance(ext, set): extensions |= ext
        else: raise Exception("pass extensions as a set()")
