# coding=utf-8
"""
__purpose__ = ...
__author__  = JeeysheLu [Jeeyshe@gmail.com] [https://www.lujianxin.com/] [2020/8/18 19:36]

    Copyright (c) 2020 JeeysheLu

This software is licensed to you under the MIT License. Looking forward to making it better.
"""

from celery.schedules import crontab

from celery_test import app



@app.task
def send():
    pass


if __name__ == '__main__':
    crontab()

