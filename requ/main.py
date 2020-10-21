# coding=utf-8
"""
__purpose__ = ...
__author__  = JeeysheLu [Jeeyshe@gmail.com] [https://www.lujianxin.com/] [2020/9/18 21:40]

    Copyright (c) 2020 JeeysheLu

This software is licensed to you under the MIT License. Looking forward to making it better.
"""
import json
import urllib2

if __name__ == '__main__':
    headers = {"Content-Type": "application/json"}
    data = {
        "msgtype": "text",
        "text": {
            "mentioned_list": ["@all", ],
            "content": "测试消息",
        }
    }
    request = urllib2.Request(
        "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=d46dd427-f8c1-4b96-92da-xxxx7cd08d1f",
        json.dumps(data),
        headers,
    )
    response = urllib2.urlopen(request)
    print response.read()
