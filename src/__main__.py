import pathlib

from .lsfiles import lsfiles
from .filters import f_dotfiles, f_ext, f_name, f_regex
from ._types import Maybe


root = pathlib.Path('/Users/yul/Downloads')
funcs = lambda x: (
    Maybe
    .unit(x)
    .bind(f_dotfiles)
    .bind(f_ext({'.c', 'mp3', '.flac', '.pdf', '.png'}))
    # .bind(f_name('CV'))
    .bind(f_regex(r'GUTH\sAYMERIC\.png'))
)
files = lsfiles(funcs)(root)


# files = lsfiles(
#     f_regex(r'GUTH\sAYMERIC\.png')
#     | f_dotfiles
#     | f_ext({'.c', 'mp3', '.flac', '.pdf', '.png'})
#     | f_name('CV')
# )(root)
