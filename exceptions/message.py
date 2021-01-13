#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
#=============================================================================
# FileName: message.py
# Desc:
# Author: Jeyrce.Lu
# Email: jianxin.lu@woqutech.com
# HomePage: www.woqutech.com
# Version: 0.0.1
# LastChange:  2020/12/29 下午4:41
# History:
#=============================================================================
"""


class CustomError(Exception):
    """
    自定义异常
    """
    pass


if __name__ == '__main__':
    try:
        raise CustomError
    except Exception as e:
        print()
