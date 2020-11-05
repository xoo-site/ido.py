# coding=utf-8
"""
__purpose__ = 批量生成 名字
__author__  = JeeysheLu [Jeeyshe@gmail.com] [https://www.lujianxin.com/] [2020/11/5 10:55]

    Copyright (c) 2020 JeeysheLu

This software is licensed to you under the MIT License. Looking forward to making it better.
"""

prefix = [
    "Jey",
    "Jay",
    "Jee",
    "Jan",
]


expect_letters = "aechikorsuxyz"

def gen():
    names = []
    for first in expect_letters:
        for second in expect_letters:
            for third in expect_letters:
                names.append(f"{first}{second}{third}")
    return names


if __name__ == '__main__':
    content = gen()
    for p in prefix:
        ft = open(f"{p}.txt", "wt", encoding="utf-8")
        line = []
        for n in content:
            name = f"{p}{n}"
            print(name)
            line.append(name)
            if len(line) == 7:
                ft.write("\t".join(line))
                ft.write("\n")
                line = []
        if len(line) > 0:
            ft.write("\t".join(line))
            ft.write("\n")
        ft.close()

