#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
#=============================================================================
# FileName: server.py
# Desc:
# Author: Jeyrce.Lu
# Email: jianxin.lu@woqutech.com
# HomePage: www.woqutech.com
# Version: 0.0.1
# LastChange:  2021/1/21 下午4:25
# History:
#=============================================================================
"""

import time
import uvicorn
import asyncio
from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def index():
    return {"code": 0, 'message': 'OK'}


@app.get('/wait/{seconds}')
def wait(seconds: int):
    print(f"slept for {seconds} seconds")
    time.sleep(seconds)
    return {"code": 0, 'message': 'OK'}


if __name__ == '__main__':
    uvicorn.run(app="fast_api.server:app", host='0.0.0.0', port=8080, workers=10)
