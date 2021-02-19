#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
企业微信群消息推送
"""

import os
import json
import datetime
import urllib2
import logging
from logging.handlers import RotatingFileHandler

# 要推送的消息文件
MESSAGE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "message.txt")
# 日志文件
logfile = "/var/log/wechat.log"

# 推送的机器人地址
robot = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=2010f980-db21-4de3-ba4c-1ac026f26eb0"

# 日志位置以及格式
logging.basicConfig(
    filename=logfile,
    level=logging.INFO,
    format="[%(name)s %(levelname)s %(asctime)s %(module)s:%(lineno)d] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("wechat")
logger.addHandler(RotatingFileHandler(filename=logfile, maxBytes=5 * 1024, backupCount=5))

if __name__ == '__main__':
    logger.info("-" * 50)
    txt = open(MESSAGE, "rt")
    message = txt.read()
    message = message.format(datetime=datetime.datetime.now().strftime("%Y年%m月%d日"))
    logger.info("格式化消息结束")
    headers = {"Content-Type": "application/json"}
    data = {
        "msgtype": "text",
        "text": {
            "mentioned_list": ["@all", ],
            "content": message,
        }
    }
    request = urllib2.Request(robot, json.dumps(data), headers)
    response = urllib2.urlopen(request)
    logger.info(response.read())
    txt.close()
