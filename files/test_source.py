# coding=utf-8
"""
__purpose__ = 测试命令行source家目录用户环境
__author__  = JeeysheLu [Jeeyshe@gmail.com] [https://www.lujianxin.com/] [2020/9/18 14:10]

    Copyright (c) 2020 JeeysheLu

This software is licensed to you under the MIT License. Looking forward to making it better.
"""

import os

path = "/home/jeeyshe/.bashrc"
cmd = """echo "alias xecho=\'echo Jeeyshe\'" >> %s""" % path

if __name__ == '__main__':
    os.system(cmd)
    os.system(". %s" % path)
