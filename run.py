#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
#=============================================================================
# FileName: run.py
# Desc:
# Author: Jeyrce.Lu
# Email: jianxin.lu@woqutech.com
# HomePage: www.woqutech.com
# Version: 0.0.1
# LastChange:  2020/12/1 下午3:32
# History:
#=============================================================================
"""
import importlib
from exceptions import load_all_errors

load_all_errors()

from exceptions.base import BaseError

if __name__ == '__main__':
    # es = BaseError.__subclasses__()
    # print(es)
    importlib.import_module("code", "exceptions")
