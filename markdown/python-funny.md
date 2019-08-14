title: 用Python不务正业 - 第一弹
date: 2016-04-16 18:31:40
tags: 
- Python
- Python不务正业
- 终端乱弹
---

从这篇开始会做一个`用Python不务正业`专题， 记录Python一些一无是用但是很好玩的脚本.本期是一个`终端乱弹`的脚本.

效果图:
![效果图](/uploads/images/xiaoguo.gif)

记得刚学shell的时候做过终端随机的点生成随机颜色的字符， 只为好玩和增强脚本开发技能， 下午闲来无事用python实现了， 正好学习了python的`curses`标准库. python `curses`标准库可以用来对终端定制开发， 做一些友好的终端命令。

本脚本不需要安装其他的库， 只依赖标准库， 在Python2.7 测试通过， 以下为代码:

```python
# -*- coding: utf-8 -*-
'''
File Name: mt2.py
Author: JackeyGao
mail: gaojunqi@outlook.com
Created Time: Fri Apr 15 15:52:31 2016
'''
import os, sys
import locale
import signal
import random
import curses
import time
import traceback

locale.setlocale(locale.LC_ALL, '')
code = locale.getpreferredencoding()

stdscr = curses.initscr()
size = lambda: os.popen('stty size', 'r').read().split()

def show_point(str, x, y, colorpair=2):
    global stdscr
    try:
        stdscr.addstr(y, x, str, curses.color_pair(colorpair))
    except Exception as e:
        pass
    stdscr.refresh()

def set_window():
    '''''控制台设置'''
    global stdscr
    curses.start_color()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(7, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.noecho()
    curses.cbreak()
    stdscr.nodelay(1)

def unset_window():
    '''控制台重置'''
    global stdstr
    curses.nocbreak()
    stdscr.keypad(0)
    curses.echo()
    curses.endwin()

def signal_handler(signal, frame):
    sys.exit(0)

if __name__=='__main__':
    signal.signal(signal.SIGINT, signal_handler)
    try:
        set_window()
        while True:
            height, weight = size()
            y = random.randrange(0, int(height), 1)
            x = random.randrange(0, int(weight), 1)
            color = random.randrange(1, 8, 1)
            show_point('Ooo0oOo', x, y, colorpair=color)
            time.sleep(0.01)
    except Exception as e:
        pass
    finally:
        unset_window()
```

