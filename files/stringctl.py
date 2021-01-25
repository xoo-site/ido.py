#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
#=============================================================================
# FileName: stringctl.py
# Desc:
# Author: Jeyrce.Lu
# Email: jianxin.lu@woqutech.com
# HomePage: www.woqutech.com
# Version: 0.0.1
# LastChange:  2021/1/25 下午4:20
# History:
#=============================================================================
"""
from typing import Any
from collections import Iterable


def to_string(anything: Any) -> Any:
    """
    将对象中所有子对象都转为str类型
    """
    # 简单类型 int, float, bytes 以及自定义class
    if isinstance(anything, (float, int, str, bytes)):
        return str(anything)

    # dict 对k, v 分别递归
    if isinstance(anything, dict):
        return {
            to_string(key): to_string(value)
            for key, value in anything.items()
        }
    # 其余可迭代类型则递归处理
    elif isinstance(anything, Iterable):
        return [to_string(element) for element in anything]

    return str(anything)


class A(object):
    def __str__(self):
        return self.__class__.__name__


if __name__ == '__main__':
    s = {
        "list_dict": [
            A(),
            3.1415926,
            {
                5: "1234",
                6: "1234",
                7: "1234",
            }
        ],
    }
    r = to_string(s)
    print(type(r))
    print(r)
