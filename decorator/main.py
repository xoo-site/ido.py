# coding=utf-8
"""
__purpose__ = ...
__author__  = JeeysheLu [Jeeyshe@gmail.com] [https://www.lujianxin.com/] [2020/10/13 20:47]

    Copyright (c) 2020 JeeysheLu

This software is licensed to you under the MIT License. Looking forward to making it better.
"""

import time


def log(f):
    print(time.strftime("%Y-%m-%d"))

    def _wrap(*args, **kwargs):
        return f(*args, **kwargs)

    return _wrap


@log
def show(a, b):
    print(a, b)
    return "OK"


if __name__ == '__main__':
    show(1, 2)
