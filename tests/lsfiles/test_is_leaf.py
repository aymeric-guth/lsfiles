import pytest
import pathlib
import os
import shutil

from lsfiles._lsfiles import is_leaf, LSFilesError


root = pathlib.PurePath(__file__).parent
env_root = root / 'env'


@pytest.fixture(autouse=True, scope='session')
def env_setup():
    try:
        os.makedirs(env_root)
    except OSError:
        shutil.rmtree(env_root)
        os.makedirs(env_root)
    os.makedirs(env_root / 'dir1')
    pathlib.Path(env_root / 'file1.file').touch()
    yield
    try:
        shutil.rmtree(env_root)
    except OSError:
        ...


params = [
    pytest.param(
        str(env_root / 'dir1'), True, 
        id="leaf path dir"
    ),
    pytest.param(
        str(env_root / 'file1.file'), True,
        id="leaf path file"
    ),
    pytest.param(
        str(env_root), False,
        id="non-leaf path dir"
    ),
]
@pytest.mark.parametrize(
    ('path', 'expected'),
    params
)
def test_is_leaf(path, expected):
    assert is_leaf(path) == expected


params = [
    pytest.param(
        str(env_root / "dir2"), LSFilesError,
        id="non-existant path dir"
    ),
    pytest.param(
        str(env_root / "file2.file"), LSFilesError,
        id="non-existant path file"
    ),
]
@pytest.mark.parametrize(
    ('path', 'expected'),
    params
)
def test_is_leaf_error(path, expected):
    with pytest.raises(LSFilesError):
        is_leaf(path)
