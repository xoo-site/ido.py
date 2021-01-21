#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
#=============================================================================
# FileName: handler.py
# Desc:
# Author: Jeyrce.Lu
# Email: jianxin.lu@woqutech.com
# HomePage: www.woqutech.com
# Version: 0.0.1
# LastChange:  2021/1/21 下午4:53
# History:
#=============================================================================
"""

import time

from django.http.response import JsonResponse


async def index(request):
    return JsonResponse({"code": 0, "message": "realtime"})


async def wait(request, s: int):
    time.sleep(int(s))
    return JsonResponse({"code": 0, "message": f"slept for {s} seconds"})
