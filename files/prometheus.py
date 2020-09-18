# coding=utf-8
"""
__purpose__ = ...
__author__  = JeeysheLu [Jeeyshe@gmail.com] [https://www.lujianxin.com/] [2020/9/16 09:48]

    Copyright (c) 2020 JeeysheLu

This software is licensed to you under the MIT License. Looking forward to making it better.
"""

import json

import yaml

path = "prometheus.yml"

if __name__ == '__main__':
    with open(path, "rt") as ft:
        yml = yaml.safe_load(ft)
        with open("prometheus.json", "w") as j:
            j.write(json.dumps(yml))
