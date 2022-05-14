from __future__ import annotations
from typing import TypeVar, Callable, Any


# T = TypeVar('T', bound='Wrapper')
T = TypeVar('T')


class Maybe(object):
    def __init__(self, value):
        self.value = value

    @classmethod
    def unit(cls, value):
        return cls(value)
    
    def bind(self, f):
        if self.value is None:
            return self

        result = f(self.value)
        if isinstance(result, Maybe):
            return result
        else:
            return Maybe.unit(result)

    def __getattr__(self, name):
        field = getattr(self.value, name)
        if not callable(field):
            return self.bind(lambda _: field)
        return lambda *args, **kwargs: self.bind(lambda _: field(*args, **kwargs))


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


# class Wrapper:
#     def __init__(self, func: Callable) -> None:
#         self.func = type_check(func)
#         self.name = func.__name__
#         annotations = func.__annotations__
#         self.ret_type = annotations.get('return')
#         self.arg_name = (set(annotations.keys()) - {'return',}).pop()
#         self.arg_type = annotations.get(self.arg_name)

#     def __call__(self, arg: Any) -> Any:
#         # print(f'Calling: {self.name} ({arg})')
#         return self.func(arg)

#     def __or__(self, other: T) -> T:
#         if not isinstance(other, Wrapper):
#             raise TypeError(f'Must be an instance of Wrapper\nGot: {other}')
#         # if not self.ret_type == other.arg_type:
#         #     raise TypeError(f'Incompatible types:\n{self!r}\n{other!r}')
#         func = lambda x: other(self.func(x))
#         func.__annotations__ = {self.arg_name: self.arg_type, 'return': other.ret_type}
#         func.__name__ = f'{self.name} | {other.name}'
#         return Wrapper(func)
    
#     def __lt__(self, other: T) -> T:
#         if not isinstance(other, Wrapper):
#             raise TypeError(f'Must be an instance of Wrapper\nGot: {other}')
#         if not self.arg_type == other.ret_type:
#             raise TypeError(f'Incompatible types:\n{other!r}\n{self!r}')
#         func = lambda x: self.func(other(x))
#         func.__annotations__ = {other.arg_name: other.arg_type, 'return': self.ret_type}
#         func.__name__ = f'{other.name} | {self.name}'
#         return Wrapper(func)

#     def __gt__(self, other: T) -> T:
#         return self.__or__(other)

#     def __repr__(self) -> str:
#         return f'{self.func.__name__}({self.arg_name}: {self.arg_type.__name__}) -> {self.ret_type.__name__}'


class Wrapper:
    def __init__(self, func: Callable) -> None:
        self.func = type_check(func)
        self.name = func.__name__
        annotations = func.__annotations__
        self.ret_type = annotations.get('return')
        self.arg_name = (set(annotations.keys()) - {'return',}).pop()
        self.arg_type = annotations.get(self.arg_name)

    def __call__(self, arg: Any) -> Any:
        return arg if arg is None else self.func(arg)

    def __or__(self, other: Wrapper) -> Wrapper:
        if not isinstance(other, Wrapper):
            raise TypeError(f'Must be an instance of Wrapper\nGot: {other}')
        # if not self.ret_type == other.arg_type:
        #     raise TypeError(f'Incompatible types:\n{self!r}\n{other!r}')
        func = lambda x: other(self.func(x))
        func.__annotations__ = {self.arg_name: self.arg_type, 'return': other.ret_type}
        func.__name__ = f'{self.name} | {other.name}'
        return Wrapper(func)

    def __lt__(self, other: Wrapper) -> Wrapper:
        if not isinstance(other, Wrapper):
            raise TypeError(f'Must be an instance of Wrapper\nGot: {other}')
        if not self.arg_type == other.ret_type:
            raise TypeError(f'Incompatible types:\n{other!r}\n{self!r}')
        func = lambda x: self.func(other(x))
        func.__annotations__ = {other.arg_name: other.arg_type, 'return': self.ret_type}
        func.__name__ = f'{other.name} | {self.name}'
        return Wrapper(func)

    def __repr__(self) -> str:
        return f'{self.func.__name__}({self.arg_name}: {self.arg_type.__name__}) -> {self.ret_type.__name__}'


# class File(pathlib.Path):
#     def __init__(self, p: os.DirEntry|pathlib.Path|str) -> None:
#         self._p = p
#         if isinstance(p, os.DirEntry|pathlib.Path):
#             self._p = p
#         elif isinstance(p, str):
#             self._p = pathlib.Path(p)
#         else:
#             raise TypeError
#         self._cache_path: Optional[pathlib.Path] = None
#         self._cache_f: Optional[tuple[str, str]] = None
#         self._filename: Optional[str] = None
#         self._ext: Optional[str] = None

#     def splitext(self) -> None:
#         (filename, ext) = splitext(self._p.name)
#         self._filename, self._ext = filename, ext.lower()

#     @property
#     def cache(self) -> str:
#         if self._cache is None:
#             self._cache = pathlib.Path(self._p.path)
#         else:
#             return self._cache

#     @cache.setter
#     def cache(self, value: Any) -> None:
#         raise TypeError

#     @property
#     def filename(self) -> str:
#         if self._filename is None:
#             self.splitext()
#         return self._filename

#     @filename.setter
#     def filename(self, value: Any) -> None:
#         raise TypeError

#     @property
#     def ext(self) -> str:
#         if self._ext is None:
#             self.splitext()
#         return self._ext

#     @ext.setter
#     def ext(self, value: Any) -> None:
#         raise TypeError

#     @property
#     def path(self) -> str:
#         return self._p.path

#     @path.setter
#     def path(self, value: Any) -> None:
#         raise TypeError

#     # def __getattr__(self, name: str) -> Any:
#     #     if (attr := self.__getattribute__(name)) is None:
#     #         return self._p.__getattribute__(name)
#     #     else:
#     #         attr

#     @classmethod
#     def from_path(cls, p: pathlib.Path):
#         ...

#     @classmethod
#     def from_str(cls, p: str):
#         ...


