# /usr/bin/env python
# coding=utf-8
"""
Created by Jeeyshe 2020/7/22 下午7:24, contact me with https://www.lujianxin.com/.
----------------------------------------------------------------------------------
# purpose of the file...
"""

from typing import *

PointY = NamedTuple('PointY', [('x', str), ('y', int)])


class PointX(NamedTuple):
    x: str
    y: int


def f_() -> Union[Tuple[str, int, List[float], Dict[str, AnyStr]], Dict[str, float]]:
    return {"x": 12}


X = Union[Tuple[str, int, List[float], Dict[str, AnyStr]], Dict[str, float]]


def f__() -> X:
    return {"y": 77}


def f(x: Optional[int] = None) -> Optional[int]:
    return x


def f_x(x: Optional[int] = None) -> Union[int, NoReturn]:
    return x


def call(f: Callable[..., int]):
    f()


def add(x: str, y: int) -> float:
    return 1.0


def run(x: str, y: int, f: Callable[[str, int], float]) -> float:
    return f(x, y)


x: Tuple[int, ...] = 1, 2, 3


def union(x: Union[int, float, str]):
    print(x)


def final(f: Final):
    pass


def classvar(v: ClassVar):
    pass


def any_(x: Any):
    pass


class User(object):
    def __init__(self, name: AnyStr, age: Optional[int] = 0):
        self.name = name
        self.age = age

    def show(self):
        print(self.name, self.age)

    def do(self):
        pass


def say(user: User) -> AnyStr:
    return user.name


def shop(item: Dict[str, float]):
    for k, v in item.items():
        print(k, v)


def tuple_(items: Tuple[int, str]):
    pass


def process_items(items: List[str]) -> NoReturn:
    for item in items:
        print(item)


def do_reg(name: AnyStr, age: int, children: List[AnyStr]) -> Tuple[AnyStr, Tuple[float]]:
    return "", (1.0,)


def do_something(name: str, age: int, children: list) -> (str, tuple):
    print(name, age, children)
    return "xx", (1,)


if __name__ == '__main__':
    do_something("Jeeyshe", 50, [])
    pass
