# coding=utf-8
"""
__purpose__ = ...
__author__  = JeeysheLu [Jeeyshe@gmail.com] [https://www.lujianxin.com/] [2020/10/14 16:29]

    Copyright (c) 2020 JeeysheLu

This software is licensed to you under the MIT License. Looking forward to making it better.
"""
from schema import *

UTF8 = And(Or(Use(str)), len)

schema = Schema({
    "name": And(UTF8, Use(lambda x: "manager" if x == "cloud" else x)),
})

if __name__ == '__main__':
    print(schema.validate({"name": "cloud"}))
