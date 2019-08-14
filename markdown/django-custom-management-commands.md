title: Django 自定义管理命令
date: 2018-11-27 16:16:43
---

![](/uploads/images/custom-management-command-cover.jpeg "cover")

Django 提供了一组非常实用的命令， 可以通过**django-admin.py**和**pytohn manage.py**脚本调用. 关于这个Management Command的一个优点是你可以创建自定义的command来扩展它.当你需要通过终端命令来对程序进行操作的时候， 通过这个管理命令就非常方便了。 在本篇中， 你将学习到如何编写自己的命令并通过manage.py 来调用.


- [介绍](#introduction)
- [基本示例](#basic)
- [处理参数](#handling-arguments)
    - [位置参数](#positional-arguments)
    - [可选参数](#optional-arguments)
    - [Flag参数](#flag-arguments)
    - [任意长度列表参数](#list-arguments)
- [Ansi颜色字体](#styling)
- [定时任务](#cronjob)
- [进阶阅读](#read-more)


<h2 id="introduction">介绍</h2>

开始之前我们先熟悉下， Management Command(manage.py)命令行. 可以看到有我们熟悉的**startproject**, **runserver**, **collectstatic**等命令. 通过help命令可以查看完整的命令列表.

```shell
python manage.py help
```

```text:output
Type 'manage.py help <subcommand>' for help on a specific subcommand.

Available subcommands:

[auth]
    changepassword
    createsuperuser

[contenttypes]
    remove_stale_contenttypes

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

[sessions]
    clearsessions

[staticfiles]
    collectstatic
    findstatic
    runserver
```

现在， 我们开始创建我们自己的自定义命令了， 首先你要在你的APP目录创建**management/commands**目录. 如下:


```text
mysite/                                   <-- 项目目录
 |-- core/                                <-- APP目录
 |    |-- management/
 |    |    +-- commands/                  <-- 创建的目录
 |    |         +-- my_custom_command.py  <-- 命令将要生效的模块, 默认情况下此模块的名字将是 command 名字.
 |    |-- migrations/
 |    |    +-- __init__.py
 |    |-- __init__.py
 |    |-- admin.py
 |    |-- apps.py
 |    |-- models.py
 |    |-- tests.py
 |    +-- views.py
 |-- mysite/
 |    |-- __init__.py
 |    |-- settings.py
 |    |-- urls.py
 |    |-- wsgi.py
 +-- manage.py
```

调用命令的方式


```shell
python manage.py my_custom_command
```

<h2 id="basic">基本示例</h2>

下面一个自定义命令的例子, 获取当前时间的例子.

**management/commands/what\_time\_is\_it.py**


```python
from django.core.management.base import BaseCommand
from django.utils import timezone

class Command(BaseCommand):
    help = 'Displays current time'

    def handle(self, *args, **kwargs):
        time = timezone.now().strftime('%X')
        self.stdout.write("It's now %s" % time)
```

Django 管理命令由一个 Command 类组成， 这个类继承自 BaseCommand. 命令的处理代码应该在handle() 方法中定义.


然后我们执行测试一下

```shell
$ python manage.py what_time_is_it
It's now 18:35:31
```

你可以会问和普通的脚本有什么不同. 其实是这个例子不具有代表性， Django Management 命令的主要优点是handle()方法中， Django 所有的模块都已经加载并准备完毕.这意味着你可以Django的 ORM 模型, 对数据库进行查询, 并与你项目的所有模块或者函数进行交互. 而这些单独的普通脚本是非常麻烦的， 而且通过这种方式会让代码组织更加紧凑.


<h2 id="handling-arguments">处理参数</h2>


参数处理部分使用了[argparse](https://docs.python.org/3/library/argparse.html), 属于标准库里面的包，我们应该定义一个名为**add\_arguments**的方法.


<h3 id="positional-arguments">位置参数</h3>

下面举例创建随机用户实例的命令， 他接受一个total参数, 作用定义该命令创建的随机用户数.

**management/commands/create\_users.py**

```python
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string

class Command(BaseCommand):
    help = 'Create random users'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='Indicates the number of users to be created')

    def handle(self, *args, **kwargs):
        total = kwargs['total']
        for i in range(total):
            User.objects.create_user(username=get_random_string(), email='', password='123')
```

怎么使用?

```shell
python manage.py create_users 10
```

<h3 id="optional-arguments">可选参数</h3>


可选参数可以按照任何顺序传递，下面举例对随机创建的用户加上前缀.

**management/commands/create\_users.py**


```python
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string

class Command(BaseCommand):
    help = 'Create random users'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='Indicates the number of users to be created')

        # Optional argument
        parser.add_argument('-p', '--prefix', type=str, help='Define a username prefix', )

    def handle(self, *args, **kwargs):
        total = kwargs['total']
        prefix = kwargs['prefix']

        for i in range(total):
            if prefix:
                username = '{prefix}_{random_string}'.format(prefix=prefix, random_string=get_random_string())
            else:
                username = get_random_string()
            User.objects.create_user(username=username, email='', password='123')
```

使用?

```shell
python manage.py create_users 10 --prefix custom_user
```

or 

```shell
python manage.py create_users 10 -p custom_user
```

如果使用**--prefix**用户名会创建为**custom\_user\_oYwoxtt4vNHR** 如果不使用前缀则创建为oYwoxtt4vNHR.


<h3 id="flag-arguments">Flag 参数</h3>


另一种参数是 flag 参数， 用于处理布尔值， 当使用的时候则为 True. 下面具体添加**--admin** flag , 用于创建随机的管理员用户实例. 如果不指定这个 flag， 则创建普通的用户实例.

**management/commands/create\_users.py**

```python
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string

class Command(BaseCommand):
    help = 'Create random users'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='Indicates the number of users to be created')
        parser.add_argument('-p', '--prefix', type=str, help='Define a username prefix')
        parser.add_argument('-a', '--admin', action='store_true', help='Create an admin account')

    def handle(self, *args, **kwargs):
        total = kwargs['total']
        prefix = kwargs['prefix']
        admin = kwargs['admin']

        for i in range(total):
            if prefix:
                username = '{prefix}_{random_string}'.format(prefix=prefix, random_string=get_random_string())
            else:
                username = get_random_string()

            if admin:
                User.objects.create_superuser(username=username, email='', password='123')
            else:
                User.objects.create_user(username=username, email='', password='123')
```

使用?

```shell
python manage.py create_users 2 --admin
```

or 

```shell
python manage.py create_users 2 -a
```


<h3 id="list-arguments">任意长度列表参数</h3>


下面举例创建一个新命令**delete\_users**, 它接受一个 ID 列表， 用户删除指定用户.


**management/commands/delete\_users.py**


```shell
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Delete users'

    def add_arguments(self, parser):
        parser.add_argument('user_id', nargs='+', type=int, help='User ID')

    def handle(self, *args, **kwargs):
        users_ids = kwargs['user_id']

        for user_id in users_ids:
            try:
                user = User.objects.get(pk=user_id)
                user.delete()
                self.stdout.write('User "%s (%s)" deleted with success!' % (user.username, user_id))
            except User.DoesNotExist:
                self.stdout.write('User with id "%s" does not exist.' % user_id)
```

使用?

```shell
$ python manage.py delete_users 1

User "SMl5ISqAsIS8 (1)" deleted with success!
```

我们也可以通过空格分割， 传递 ID 列表. 删除多个用户

```shell
$ python manage.py delete_users 1 2 3 4

User with id "1" does not exist.
User "9teHR4Y7Bz4q (2)" deleted with success!
User "ABdSgmBtfO2t (3)" deleted with success!
User "BsDxOO8Uxgvo (4)" deleted with success!
```

<h2 id="styling">Ansi颜色字体</h2>


可以输出带有颜色的消息， 让输出更加直观.


**management/commands/delete\_users.py**


```python
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Delete users'

    def add_arguments(self, parser):
        parser.add_argument('user_id', nargs='+', type=int, help='User ID')

    def handle(self, *args, **kwargs):
        users_ids = kwargs['user_id']

        for user_id in users_ids:
            try:
                user = User.objects.get(pk=user_id)
                user.delete()
                self.stdout.write(self.style.SUCCESS('User "%s (%s)" deleted with success!' % (user.username, user_id)))
            except User.DoesNotExist:
                self.stdout.write(self.style.WARNING('User with id "%s" does not exist.' % user_id))
```

用法和以前一样， 区别在于输出的信息.

```shell
$ python manage.py delete_users 3 4 5 6
```
输出

![](/uploads/images/custom-management-command-style1.png)

下面是所有样式的列表, 请挑选使用


```python
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Show all available styles'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.ERROR('error - A major error.'))
        self.stdout.write(self.style.NOTICE('notice - A minor error.'))
        self.stdout.write(self.style.SUCCESS('success - A success.'))
        self.stdout.write(self.style.WARNING('warning - A warning.'))
        self.stdout.write(self.style.SQL_FIELD('sql_field - The name of a model field in SQL.'))
        self.stdout.write(self.style.SQL_COLTYPE('sql_coltype - The type of a model field in SQL.'))
        self.stdout.write(self.style.SQL_KEYWORD('sql_keyword - An SQL keyword.'))
        self.stdout.write(self.style.SQL_TABLE('sql_table - The name of a model in SQL.'))
        self.stdout.write(self.style.HTTP_INFO('http_info - A 1XX HTTP Informational server response.'))
        self.stdout.write(self.style.HTTP_SUCCESS('http_success - A 2XX HTTP Success server response.'))
        self.stdout.write(self.style.HTTP_NOT_MODIFIED('http_not_modified - A 304 HTTP Not Modified server response.'))
        self.stdout.write(self.style.HTTP_REDIRECT('http_redirect - A 3XX HTTP Redirect server response other than 304.'))
        self.stdout.write(self.style.HTTP_NOT_FOUND('http_not_found - A 404 HTTP Not Found server response.'))
        self.stdout.write(self.style.HTTP_BAD_REQUEST('http_bad_request - A 4XX HTTP Bad Request server response other than 404.'))
        self.stdout.write(self.style.HTTP_SERVER_ERROR('http_server_error - A 5XX HTTP Server Error response.'))
        self.stdout.write(self.style.MIGRATE_HEADING('migrate_heading - A heading in a migrations management command.'))
        self.stdout.write(self.style.MIGRATE_LABEL('migrate_label - A migration name.'))
```

![](/uploads/images/custom-management-command-style2.png)


<h2 id="cronjob">定时任务</h2>

```crontab
# m h  dom mon dow   command
0 4 * * * /home/mysite/venv/bin/python /home/mysite/mysite/manage.py my_custom_command
```

<h2 id="read-more">阅读更多</h2>

> 阅读更多关于自定义命令的文档， [Django Documentation](https://docs.djangoproject.com/en/dev/howto/custom-management-commands/#command-objects)

