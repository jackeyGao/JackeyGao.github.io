title: 查看你历史命令的使用率
date: 2015-09-30 13:46:55
categories:
- Python
tags:
- Python
- command
- Bash
- Zsh
---


一个查看历史命令的使用率工具， 因为看到`oh-my-zsh`项目中的`zsh_stats`function 后有感仿照开发了一个。 本项目不仅支持`zsh_history`而且支持`bash_history` 。 还有可扩展的趋势.

## oh-my-zsh 之 zsh_stats

如果你用`oh-my-zsh` ， 那么你就有了这个功能。 

```bash
$ zsh_stats
     1  3290  32.9033%   vim
     2  2204  22.0422%   python
     3  902   9.0209%    ls
     4  730   7.30073%   git
     5  449   4.49045%   cd
     6  194   1.94019%   curl
     7  170   1.70017%   pip
     8  168   1.68017%   ll
     9  157   1.57016%   scrapy
    10  142   1.42014%   rm
    11  96    0.960096%  cat
    12  78    0.780078%  hexo
    13  76    0.760076%  clear
    14  63    0.630063%  mkdir
    15  60    0.60006%   ping
    16  59    0.590059%  grep
    17  58    0.580058%  workon
    18  57    0.570057%  sudo
    19  57    0.570057%  docker
    20  55    0.550055%  mv
$ which zsh_stats # oh-my-zsh 封装的函数
zsh_stats () {
    fc -l 1 | awk '{CMD[$2]++;count++;}END { for (a in CMD)print CMD[a] " " CMD[a]/count*100 "% " a;}' | grep -v "./" | column -c3 -s " " -t | sort -nr | nl | head -n20
}
```

## cmdstats 项目

查看你终端命令使用频率列表, 原理是通过宿主目录下的 `.*history` 分析后得到历史命令使用频率状态， 并且进行排序输出.

目前支持 `~/.bash_history` 、 `~/.zsh_history`

### 安装

```bash
pip install git+https://github.com/jackeyGao/cmdstats.git
```

### 使用

```bash
$ cmdstats -h
usage: cmdstats [-h] [-l LIMIT]

optional arguments:
  -h, --help            show this help message and exit
  -l LIMIT, --limit LIMIT
                        显示条数[default: 20]
```

```bash
$ cmdstats
1   3612  33.13154%  vim
2   2473  22.68391%  python
3   1018  9.33774%   ls
4   692   6.34746%   git
5   487   4.46707%   cd
6   204   1.87122%   ll
7   194   1.77949%   curl
8   178   1.63273%   pip
9   157   1.4401%    scrapy
10  147   1.34838%   rm
11  98    0.89892%   cat
12  91    0.83471%   clear
13  86    0.78885%   ping
14  78    0.71547%   hexo
15  73    0.6696%    docker
16  71    0.65126%   mkdir
17  61    0.55953%   workon
18  60    0.55036%   grep
19  58    0.53201%   sudo
20  57    0.52284%   mv
$ which cmdstats
/usr/local/bin//cmdstats
```

### 项目地址

[jackeyGao/cmdstats](https://github.com/jackeyGao/cmdstats)
