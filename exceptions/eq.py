#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
#=============================================================================
# FileName: eq.py
# Desc:
# Author: Jeyrce.Lu
# Email: jianxin.lu@woqutech.com
# HomePage: www.woqutech.com
# Version: 0.0.1
# LastChange:  2020/12/2 下午7:44
# History:
#=============================================================================
"""
from typing import Union


class ErrorCode(list):
    def __eq__(self, error_code: Union["ErrorCode", str, bytes]) -> bool:  # type: ignore
        """
        可在项目中使用  e == "ORA-12545"
        """
        if isinstance(error_code, str):
            return error_code in self

        if isinstance(error_code, bytes):
            return error_code.decode() in self

        return error_code == self


if __name__ == '__main__':
    e = ErrorCode(["ORA-12545", "ORA-12066"])
    print(e == "ORA-12535")
