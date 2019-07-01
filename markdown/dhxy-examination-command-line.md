title: 大话西游答题器 command line
date: 2016-01-15 09:55:15
tags:
- 病
- 游戏
---

科举，大理寺都适用。 唯独不支持的是殿试。

## 项目代吗

需要依赖[requests](http://docs.python-requests.org/en/latest/)

```bash
pip install requests
```

然后保存下列代码到一个python文件(如: `search.py`)

```python
# -*- coding: utf-8 -*-
'''
File Name: search.py
Author: JackeyGao
mail: junqi.gao@shuyun.com
Created Time: 三  1/13 11:12:32 2016
'''
import sys
import readline
import signal
import requests

readline.parse_and_bind('tab: complete')
readline.parse_and_bind('set editing-mode vi')

def _wrap_with_code(code):
    def inner(text, bold=False):
        c = code
        if bold:
            c = "1;%s" % c
        return "\033[%sm%s\033[0m" % (c, text)
    return inner

red = _wrap_with_code('31')
green = _wrap_with_code('32')
blue = _wrap_with_code('34')


categorys = (
        '',
        '乡试',
        '省试-地理',
        '省试-文学',
        '省试-常识',
        '省试-饮食',
        '省试-历史',
        '大话常识'
        )

try:
    category = sys.argv[1]
    if category not in categorys:
        raise Exception()
except IndexError as e:
    category = ''
except Exception as e:
    sys.stdout.write(red("CategoryError:\n无效的科目'%s',支持:(%s, ''(所有))\n" \
            % (category, ','.join(categorys))))
    exit()


def request(collect, query):
    url = "http://xy2-tiku.webapp.163.com/tiku/search"
    params = { "q": query }
    if collect:
        params["c"] = collect

    headers = {
            "Content-Type": "application/json",
            "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6",
            "Connection": "keep-alive",
            "Referer": "http://dhxy.163.com/"
            }
    response = requests.get(
            url,
            params=params,
            headers=headers
            )
    return response.json()


def show(data):
    for q in data["data"]:
        sys.stdout.write("- [%s] " % q["category"] + blue(q["question"]) + '\n')
        sys.stdout.write("> " + green(','.join(q["answers"])) + '\n')
        sys.stdout.write("\n")


def signal_handler(signal, frame):
    sys.stdout.write(red('\nYou pressed Ctrl+C! 答题终止.\n'))
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)
while True:
    collect = category or '所有'
    try:
        keyword = raw_input("[%s]输入关键字(终止Ctrl+C): " % red(collect))
        show(request(category, keyword))
    except EOFError:
        print(red("\n快捷键错误, 使用Ctrl+C 退出."))
```

## 使用方式

```bash
$ python search.py $CATEGORY

# CATEGORY 可以为空为空则为所有科目
# CATEGORY 支持(乡试,省试-地理,省试-文学,省试-常识,省试-饮食,省试-历史,大话常识, ''(所有))
```

![使用截图](/uploads/images/QQ20160115-1.png)
