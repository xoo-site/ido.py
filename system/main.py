# coding=utf-8
"""
__purpose__ = ...
__author__  = JeeysheLu [Jeeyshe@gmail.com] [https://www.lujianxin.com/] [2020/8/12 10:18]

    Copyright (c) 2020 JeeysheLu

This software is licensed to you under the MIT License. Looking forward to making it better.
"""

import sys

if __name__ == '__main__':
    arg = sys.argv
    print(arg)

    s = [
        {"code": 1000, "message": "xxx"},
        {"code": 1003, "message": "xxx"},
        {"code": 1004, "message": "xxx"},
        {"code": 1002, "message": "xxx"},
        {"code": 1005, "message": "xxx"},
    ]

    print(sorted(s, key=lambda x: x.get("code")))
