from os.path import splitext
from pathlib import Path
import lsfiles
from typing import Any, Callable
from math import log, exp
from typing import TypeVar, Callable

T = TypeVar('T', bound='Wrapper')

def win_path(
    files_list, i
) -> None:
    localpath = 'c:\\...'
    localpath = ''
    if i.name[0] != '.':
        filename, extension = splitext(i.name)
        path = i.path[:-(len(filename)+len(extension))]
        path = path[len('/Volumes/aaa'):]
        path = '\\'.join(path.split('/'))
        files_list.append(f'{localpath}{path}{filename}{extension}')


# def unix_path(
#     files_list, i
# ) -> None:
#     localpath = '/Game/Mods/Hyperion'
#     if i.name[0] != '.':
#         filename, extension = splitext(i.name)
#         p = f'{localpath}{i.path[len("/Volumes/aaa"):-(len(filename)+len(extension))]}{filename}.{filename}'
#         files_list.append(p)


# path = '/Volumes/aaa/Sound'
# files_list = lsfiles.lsfiles(fnc=unix_path)(path)
# for i in files_list:
#     print(i)


# with open('morrowind_sounds.txt', 'w') as f:
#     f.write('\n'.join(files_list))


def type_check(func: Callable) -> Callable:
    if not callable(func):
        raise TypeError(f'Object is not callable\nGot: {func!r}')
    elif getattr(func, '__annotations__') is None:
        raise TypeError(f'Function must declare arg and return type\nGot: {func!r}')
    elif len(func.__annotations__) != 2:
        raise TypeError(f'Function must take 1 argument and return 1 value\nGot: {func!r} {func.__annotations__}')
    elif func.__annotations__.get('return') is None:
        raise TypeError(f'Function return value must be non-None\nGot: {func!r} {func.__annotations__}')
    else:
        return func


class Wrapper:
    def __init__(self, func: Callable) -> None:
        self.func = type_check(func)
        self.name = func.__name__
        annotations = func.__annotations__
        self.ret_type = annotations.get('return')
        self.arg_name = (set(annotations.keys()) - {'return',}).pop()
        self.arg_type = annotations.get(self.arg_name)

    def __call__(self, arg: Any) -> Any:
        print(f'Calling: {self.name} ({arg})')
        return self.func(arg)

    def __or__(self, other: T) -> T:
        if not isinstance(other, Wrapper):
            raise TypeError(f'Must be an instance of Wrapper\nGot: {other}')
        # if not self.ret_type == other.arg_type:
        #     raise TypeError(f'Incompatible types:\n{self!r}\n{other!r}')
        func = lambda x: other(self.func(x))
        func.__annotations__ = {self.arg_name: self.arg_type, 'return': other.ret_type}
        func.__name__ = f'{self.name} | {other.name}'
        return Wrapper(func)
    
    def __lt__(self, other: T) -> T:
        if not isinstance(other, Wrapper):
            raise TypeError(f'Must be an instance of Wrapper\nGot: {other}')
        if not self.arg_type == other.ret_type:
            raise TypeError(f'Incompatible types:\n{other!r}\n{self!r}')
        func = lambda x: self.func(other(x))
        func.__annotations__ = {other.arg_name: other.arg_type, 'return': self.ret_type}
        func.__name__ = f'{other.name} | {self.name}'
        return Wrapper(func)

    def __gt__(self, other: T) -> T:
        return self.__or__(other)

    def __repr__(self) -> str:
        return f'{self.func.__name__}({self.arg_name}: {self.arg_type.__name__}) -> {self.ret_type.__name__}'


@Wrapper
def f(x: int) -> int:
    return x ** 2

@Wrapper
def g(x: int) -> float:
    return log(x)

@Wrapper
def h(x: float) -> float:
    return exp(x)

@Wrapper
def i(x: int) -> int:
    return x // 2

def j(x: int, y: float) -> int:
    return int(x // y)

# x: int -> Callable[[int], int]

(f | g | h)(10)
# (g | f)(10)
# print()
# print(g(10))

print((f > i)(10))
print((f | i)(10))
print((f < i)(10))

