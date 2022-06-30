## lsfiles
find-like file search utility with functional API


## Installation
``` shell
python3 -m pip install "git+https://git.ars-virtualis.org/yul/lsfiles@master"
```

## Usage
```python
import pathlib
import os

from lsfiles import iterativeDFS, iterativeBFS, recursiveDFS, Maybe
from lsfiles import filters as f
from lsfiles import adapters as a


root = pathlib.PurePath(os.getenv('HOME')) / 'Desktop' / 'dev'

filters = lambda x: (
	Maybe
	.unit(x)
	.bind(f.exclude_path(r'excluded/directory/pattern'))
	.bind(f.dotfiles)
	.bind(f.ext({'.pyc', '.py'}))
	.bind(f.regex(r'lsfiles\.py'))
)

files = iterativeDFS(
	filters,
	lambda x: pathlib.PurePath(x),
	root
)

print(f'Found {len(files)} matching files')
for f in files:
	print(f)
```
