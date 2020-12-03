# coding=utf-8
"""
__author__  = JeeysheLu [Jeeyshe@gmail.com] [https://www.lujianxin.com/] [2020/11/24 10:32]
__purpose__ = ...

"""

from exceptions.base import BaseError


class xxx(BaseError):
    pass


class fff(BaseError):
    pass


class XXX(BaseError):
    pass



if __name__ == '__main__':
    errors = BaseError.__subclasses__()
    for clazz in errors:
        print(clazz.__name__, clazz.error_code, clazz(), clazz.__doc__.strip() if clazz.__doc__ else "请联系沃趣科技工程师处理")
