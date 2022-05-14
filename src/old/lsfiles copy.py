import os


files_list = []
extensions = set()

def handle_os_exceptions(fnc):
    def inner(*args):
        try: return fnc(*args)
        except (PermissionError, FileNotFoundError, NotADirectoryError): pass
    return inner

@handle_os_exceptions
def _lsfiles_all(path):
    global files_list

    with os.scandir(path) as dir_content:
        for i in dir_content:
            if i.name[0] == ".": continue
            elif i.is_dir(follow_symlinks=False): _lsfiles_all(i)
            else: files_list.append(i)

@handle_os_exceptions
def _lsfiles_all_split(path):
    global files_list

    with os.scandir(path) as dir_content:
        for i in dir_content:
            if i.name[0] == ".": continue
            elif i.is_dir(follow_symlinks=False): _lsfiles_all_split(i)
            else:
                file_name, extension = os.path.splitext(i.name)
                extension = extension.lower()
                path = i.path[:-len(i.name)]
                files_list.append( (path, file_name, extension) )

@handle_os_exceptions
def _lsfiles_extensions(path):
    global extensions
    global files_list

    with os.scandir(path) as dir_content:
        for i in dir_content:
            if i.name[0] == ".": continue
            elif i.is_dir(follow_symlinks=False): _lsfiles_extensions(i)
            else:
                file_name, extension = os.path.splitext(i.name)
                if extension.lower() in extensions:
                    files_list.append(i)

@handle_os_exceptions
def _lsfiles_extensions_split(path):
    global extensions
    global files_list

    with os.scandir(path) as dir_content:
        for i in dir_content:
            if i.name[0] == ".": continue
            elif i.is_dir(follow_symlinks=False): _lsfiles_extensions_split(i)
            else:
                file_name, extension = os.path.splitext(i.name)
                extension = extension.lower()
                if extension in extensions:
                    path = i.path[:-len(i.name)]
                    files_list.append( (path, file_name, extension) )

@handle_os_exceptions
def _lsfiles_inode(path):
    global files_list

    with os.scandir(path) as dir_content:
        for i in dir_content:
            if i.name[0] == ".": continue
            elif i.is_dir(follow_symlinks=False): _lsfiles_inode(i)
            else: files_list.append((i.inode(), i))

@handle_os_exceptions
def _lsfiles_inode_split(path):
    global files_list

    with os.scandir(path) as dir_content:
        for i in dir_content:
            if i.name[0] == ".": continue
            elif i.is_dir(follow_symlinks=False): _lsfiles_inode_split(i)
            else:
                file_name, extension = os.path.splitext(i.name)
                extension = extension.lower()
                path = i.path[:-len(i.name)]
                files_list.append( (i.inode(), (path, file_name, extension)) )

@handle_os_exceptions
def _lsfiles_extensions_inode(path):
    global extensions
    global files_list

    with os.scandir(path) as dir_content:
        for i in dir_content:
            if i.name[0] == ".": continue
            elif i.is_dir(follow_symlinks=False): _lsfiles_extensions_inode(i)
            else:
                file_name, extension = os.path.splitext(i.name)
                if extension.lower() in extensions:
                    files_list.append((i.inode(), i))

@handle_os_exceptions
def _lsfiles_extensions_inode_split(path):
    global extensions
    global files_list

    with os.scandir(path) as dir_content:
        for i in dir_content:
            if i.name[0] == ".": continue
            elif i.is_dir(follow_symlinks=False): _lsfiles_extensions_inode_split(i)
            else:
                file_name, extension = os.path.splitext(i.name)
                extension = extension.lower()
                if extension in extensions:
                    path = i.path[:-len(i.name)]
                    files_list.append( (i.inode(), (path, file_name, extension)) )

@handle_os_exceptions
def _lsfiles_recursion_depth(path, recursion_depth=0):
    if recursion_depth < 0: return

    with os.scandir(path) as dir_content:
        for i in dir_content:
            if i.name[0] == ".":
                continue
            elif i.is_dir(follow_symlinks=False):
                _lsfiles_recursion_depth(i, recursion_depth-1)
            else:
                files_list.append(i)

def _lsfiles_recursion_depth_split(path, recursion_depth=0):
    if recursion_depth < 0: return

    with os.scandir(path) as dir_content:
        for i in dir_content:
            if i.name[0] == ".":
                continue
            elif i.is_dir(follow_symlinks=False):
                _lsfiles_recursion_depth_split(i, recursion_depth-1)
            else:
                file_name, extension = os.path.splitext(i.name)
                extension = extension.lower()
                path = i.path[:-len(i.name)]
                files_list.append( (path, file_name, extension) )


# def split_path(f: posix.DirEntry) -> (str, str, str):
#     file_name, extension = os.path.splitext(i.name)
#     extension = extension.lower()
#     path = i.path[:-len(i.name)]
#     return(path, file_name, extension)

class DirEnt(object):
    def __init__(self, f: os.DirEntry):
        self.dir_entry: os.DirEntry = f
        self.file_name: str
        self.extension: str
        self.path: str
        self.inode: int = f.inode()
        self.file_name, self.extension = os.path.splitext(i.name)
        self.extension = extension.lower()
        self.path = f.path[:-len(i.name)]

class ListFiles(object):
    function_mapper = {
        "ei": _lsfiles_extensions_inode,
        "ie": _lsfiles_extensions_inode,
        "eis": _lsfiles_extensions_inode_split,
        "ies": _lsfiles_extensions_inode_split,
        "sei": _lsfiles_extensions_inode_split,
        "sie": _lsfiles_extensions_inode_split,
        "esi": _lsfiles_extensions_inode_split,
        "ise": _lsfiles_extensions_inode_split,

        "e": _lsfiles_extensions,
        "es": _lsfiles_extensions_split,
        "se": _lsfiles_extensions_split,
        "i": _lsfiles_inode,
        "is": _lsfiles_inode_split,
        "si": _lsfiles_inode_split,
        "": _lsfiles_all,
        "s": _lsfiles_all_split,

        "r": _lsfiles_recursion_depth,
        "rs": _lsfiles_recursion_depth_split,
        "sr": _lsfiles_recursion_depth_split,
    }
    def __init__(self, args=None):
        self.args = args
        if self.args not in self.function_mapper:
            raise Exception("""'ei': extensions + inode,\n'e': extensions,\n'i': all files + inode,\n'': all files""")
        self.fnc = self.function_mapper[self.args]

        self.mode_extension = "e" in self.args
        self.mode_inode = "i" in self.args
        self.mode_split = "s" in self.args
        self.mode_recursion = "r" in self.args

    def __call__(self, *args):
        global files_list
        global extensions

        path = args[0]
        if path is None:
            raise Exception("No path provided.")
        if self.mode_extension and not(extensions):
            raise Exception("No extensions provided.")

        if isinstance(path, list):
            buffer = []
            for i in path:
                self.fnc(i)
                buffer.extend(files_list)
                files_list.clear()
        else:
            self.fnc(*args)

        if self.mode_inode:
            files_list.sort()
            buffer = [ i[1] for i in files_list ]
        elif isinstance(path, str):
            buffer = files_list.copy()
        files_list.clear()

        return buffer

    def update_extensions(self, ext):
        global extensions

        if isinstance(ext, set): extensions |= ext
        else: raise Exception("pass extensions as a set()")
