import pathlib

from .lsfiles import lsfiles
from . import filters as f
from ._types import Maybe


root = pathlib.Path('/Users/yul/Downloads')
funcs = lambda x: (
    Maybe
    .unit(x)
    .bind(f.dotfiles)
    .bind(f.ext({'.c', 'mp3', '.flac', '.pdf', '.png'}))
    # .bind(f_name('CV'))
    .bind(f.regex(r'GUTH\sAYMERIC\.png'))
)
files = lsfiles(funcs)(root, 2)
print(files)

# files = lsfiles(
#     f_regex(r'GUTH\sAYMERIC\.png')
#     | f_dotfiles
#     | f_ext({'.c', 'mp3', '.flac', '.pdf', '.png'})
#     | f_name('CV')
# )(root)
