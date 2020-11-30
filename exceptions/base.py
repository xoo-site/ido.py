# coding=utf-8
"""
__author__  = Jeyrce.Lu [Jeyrce@gmail.com] [https://www.lujianxin.com/] [2020/11/30 17:38]
__purpose__ = 自定义异常基类

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
    处理建议： 联系沃趣科技工程师进行处理
    """
    error_code: int = 0  # 业务逻辑错误码
    message: str = ""  # 错误提示信息或信息模板

    def __init__(self, **context: Any) -> None:
        self.context = context

    def __str__(self) -> str:
        return smart_format(self.message, self.context)

    def __repr__(self) -> str:
        return self.__str__()
