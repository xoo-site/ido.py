# coding=utf-8
"""
__purpose__ = ...
__author__  = JeeysheLu [Jeeyshe@gmail.com] [https://www.lujianxin.com/] [2020/10/14 09:46]

    Copyright (c) 2020 JeeysheLu

This software is licensed to you under the MIT License. Looking forward to making it better.
"""

if __name__ == '__main__':
    for i in range(10):
        try:
            ok = True
            b = 1 / 0
        except Exception as e:
            pass
        else:
            break
    if not ok:
        print("xx")
