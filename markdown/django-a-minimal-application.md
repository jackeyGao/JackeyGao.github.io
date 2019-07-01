title: 一个超级小的 Django 项目.
date: 2018-11-12 13:40:00
set: 好玩的Django
---

![](/uploads/images/a-minimal-application.jpeg "cover")

Django 可以支持类似于Flask 一样的单文件项目.


当用最简单的代码实现 Django 项目为最基本的要素的时候， 项目可以和微框架一样小.


但我建议， 最好不要这样做， 因为在选择使用 Django 的时候， 我比较看重的 Django 封装的一系列模块， 我更建议用 Django 官方提供的架构去开始我的工程。

## Introduction


首先我们知道， 在我们安装 Django 之后， Django 和其他 Python 包一样， 在**site-packages**里面, 这意味着 Django 和其他的 Python 包一样([Requests](http://www.python-requests.org/en/master/), [Pillow](https://python-pillow.org/), [NumPy](http://www.numpy.org/)).

验证 Django 是否安装最简单的方法是到交互式界面导入它

```python
>>> import django
>>> print(django.get_version())
1.11.4
```

但是我们使用 Django 和使用其他包不一样， 在官方推荐的例子下， 我们开始一个项目首先执行的是**startproject**


我们执行后， 会初始化创建默认的项目目录结构:


- manage.py
- settings.py
- urls.py
- wsgi.py

这就是常用的预配置

加入我们要做一个 web 项目， 你可能需要数据库， 处理用户的身份验证， 和会话等功能。 `startproject`会让我们对这些的处理和配置更加轻松. 而且 Django 默认就提供这些功能， 这让我们能够直接引用.

但这样不是开始项目的唯一方式， 这也是本章的目的。


## 最小的 Django 程序

**app.py**

```python
import sys

from django.conf import settings
from django.conf.urls import url
from django.core.management import execute_from_command_line
from django.http import HttpResponse

settings.configure(
    DEBUG=True,
    SECRET_KEY='A-random-secret-key!',
    ROOT_URLCONF=sys.modules[__name__],
)


def index(request):
    return HttpResponse('<h1>A minimal Django response!</h1>')

urlpatterns = [
    url(r'^$', index),
]

if __name__ == '__main__':
    execute_from_command_line(sys.argv)
```

**SECRET\_KEY**是我们必须要提供的一个参数, DEBUG默认是 False, 没有开启 DEBUG 的情况需要定义**ALLOWED\_HOSTS**配置, 所以我们直接覆盖 DEBUG 为 True.  **ROOT\_URLCONF** 是需要包含 URL 列表的特殊模块路径. 其实就是我们项目的urls.py文件.  在这里我们写到一个文件里面了， 所以我们直接定义`sys.modules[__name__]`表示当前模块, 并在当前文件下面定义**urlpatterns**列表, 定义的方式和urls.py一样和视图view对应起来.

然后通过`execute_from_command_line`快捷方式启动， 这个保留了 manage.py 命令的功能.


## 使用

由于没有其他的APP 在 **INSTALLED\_APPS**里面, 默认情况下只有 django 项目. 所以只有一些最基本的命令功能.

```shell
$ python app.py

Type 'app.py help <subcommand>' for help on a specific subcommand.

Available subcommands:

[django]
    check
    compilemessages
    createcachetable
    dbshell
    diffsettings
    dumpdata
    flush
    inspectdb
    loaddata
    makemessages
    makemigrations
    migrate
    runserver
    sendtestemail
    shell
    showmigrations
    sqlflush
    sqlmigrate
    sqlsequencereset
    squashmigrations
    startapp
    startproject
    test
    testserver
```

## 启动

我们使用 runserver 把程序启动

```shell
$ python app.py runserver
```
