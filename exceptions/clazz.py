# coding=utf-8
"""
__author__  = JeeysheLu [Jeeyshe@gmail.com] [https://www.lujianxin.com/] [2020/11/24 10:24]
__purpose__ = ...

"""
import re
from typing import *

from exceptions.base import BaseError


class DatabaseConnectError(BaseError):
    """
    建议检查数据库监听
    """
    code = 1001
    msg_template = "数据库{dbname}连接错误"


class SSHAccountError(BaseError):
    """
    建议检查用户帐密大小写
    """
    code = 2001
    msg_template = "ssh用户或密码错误"


class CommandError(BaseError):
    """
    这个肯定是doc
    """

    code = 3001
    msg_template = "执行命令错误"
    """
    这个是doc吗
    """


class ParameterNotValid(BaseError):
    code = 4000
    msg_template = "参数{param}不合法"


if __name__ == '__main__':
    """
    1、格式化时如果键值不匹配如何处理。
    """
    try:
        raise DatabaseConnectError
    except DatabaseConnectError as e:
        print(e)
