title: JPG2ASCII开发上线记录
date: 2015-11-18 14:17:10
categories:
- Python
tags:
  - Python
  - Flask
  - JPG2ASCII
  - Heroku

---

## 介绍

刚开始做运维的时候喜欢在登录服务器的时候自动打印一些ASCII图像， 于是大量搜寻这种图片以做到自己的欢迎页独一无二。 想想有点不误正业， 现在虽说找到合适的ASCII图形， 相对于以前不喜这个东西了， 但至少是一段时间的情怀. 最近研究flask， 碰巧又遇到jp2a这个开源软件, 所以想把图片转ASCII图像做成一个在线服务, 顺便入门flask.
[JPG2ASCII](jpg2ascii.herokuapp.com)

### 用到的开源
**jp2a**

进行转换的工具
项目地址:  [https://csl.name/jp2a/](https://csl.name/jp2a/)
> jp2a is a small utility that converts JPG images to ASCII. It's written in C and released under the GPL.

**flask**

一个Python web框架
项目地址: [https://github.com/mitsuhiko/flask](https://github.com/mitsuhiko/flask)

> A microframework based on Werkzeug, Jinja2 and good intentions http://flask.pocoo.org/

**semantic-UI**

一个前端开发框架
项目地址: [https://github.com/semantic-org/semantic-ui/](https://github.com/semantic-org/semantic-ui/)

> Semantic is a development framework that helps create beautiful, responsive layouts using human-friendly HTML.

## 主要思路
前端网页UI将图片和参数传递到后端flask, 然后保存图片生成ASCII最后返回生成结果.项目已经开源， 这里不贴代码了， 有兴趣移步到[https://github.com/jackeyGao/Flask-JPG2ASCII](https://github.com/jackeyGao/Flask-JPG2ASCII)

## 最后部署heroku
`Heroku`是一个支持多种编程语言的云平台即服务

Python 的web程序指定好`Procfile` 和 `requirements.txt` 就可以正常工作了， 但是由于此次项目用到了jp2a这个需要编译的工具, 现在就有个问题. 现在本地的jp2a可执行文件是不能在heroku机器上运行成功的, 所以我怎么在heroku上编译这个工具。 幸运的是heroku支持的， 官方的`快速开始`文档没有关于这个的介绍, 我在国外的一个博客看到有个伙计成功了. 下面介绍

首先需要获得一个shell命令行交互环境.其次需要把包放到heroku APP机器上, 这个可以scp, 或者wget, curl. 
获得shell(其实相当于ssh操作这台机器)， 使用heroku的run命令

```bash
heroku run /bin/bash
```

然后就会有一个shell环境来操作app机器, 这时候

```bash
curl -O http://sourceforge.net/projects/jp2a/files/latest/download

tar zxvf download
cd jp2a-xxxxx/
./configure --prefix=/app/.heroku/vendor/jp2a
make && make install
```
编译完成后需要把这个jp2a可执行命令打进包里面, heroku app机器上不太方便git操作, 我这边是在heroku app机器scp到我的服务器上. 然后add commit.


