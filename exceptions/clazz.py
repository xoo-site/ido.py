# coding=utf-8
"""
__author__  = JeeysheLu [Jeeyshe@gmail.com] [https://www.lujianxin.com/] [2020/11/24 10:24]
__purpose__ = ...

"""
import re
from typing import *


def smart_format(raw: str, dic: dict) -> str:
    """
    Example:
        smart_format("{name}-{c}-{age}", {"name": "Jeyrce.Lu"})
        > Jeyrce.Lu-{c}-{age}
    :param raw: 待格式化字符串
    :param dic: 传入的格式化字典
    :return 格式化完成的字符串
    """
    keys = re.findall("{(.*?)}", raw)
    for k in keys:
        if k not in dic:
            dic[k] = f"{{{k}}}"
    return raw.format(**dic)


class BaseError(Exception):
    """
    请联系沃趣科技工程师处理
    """
    code: str
    msg_template: str

    def __init__(self, **ctx: Any) -> None:
        self.__dict__ = ctx

    def __str__(self) -> str:
        return smart_format(self.msg_template, self.__dict__)

    def __repr__(self):
        return self.__str__()


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
