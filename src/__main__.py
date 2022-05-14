import pathlib
import time
from collections import deque

from .lsfiles import lsfiles, iterativeDFS
from . import filters as f
from . import adapters as a
from ._types import Maybe, EntryWrapper
import pdb


root = pathlib.Path('/Users/yul/Desktop')
extensions = {'.c', 'mp3', '.flac', '.pdf', '.png'}
filters = lambda x: (
    Maybe
    .unit(x)
    .bind(f.dotfiles)
    .bind(f.ext(extensions))
    # .bind(f_name('CV'))
    # .bind(f.regex(r'GUTH\sAYMERIC\.png'))
)


start = time.perf_counter()
files = lsfiles(filters, a.pathlib_purepath)(root)
print(f'Found {len(files)} Files, Took: {time.perf_counter()-start}s')


start = time.perf_counter()
files = iterativeDFS(
    filters,
    lambda x: pathlib.PurePath(x),
    root
)
print(f'Found {len(files)} Files, Took: {time.perf_counter()-start}s')
# print(files)

# files = lsfiles(
#     f_regex(r'GUTH\sAYMERIC\.png')
#     | f_dotfiles
#     | f_ext({'.c', 'mp3', '.flac', '.pdf', '.png'})
#     | f_name('CV')
# )(root)
