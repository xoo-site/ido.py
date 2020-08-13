# coding=utf-8
"""
__purpose__ = ...
__author__  = JeeysheLu [Jeeyshe@gmail.com] [https://www.lujianxin.com/] [2020/8/12 16:26]

    Copyright (c) 2020 JeeysheLu

This software is licensed to you under the MIT License. Looking forward to making it better.
"""

import paramiko


def read():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect("10.10.90.154", 22, "root", "cljslrl0620")
    _, stdout, stderr = client.exec_command("cd /root && ls -al")
    for line in stdout.readlines():
        yield line


if __name__ == '__main__':
    lines = read()
    for line in lines:
        print(line)
