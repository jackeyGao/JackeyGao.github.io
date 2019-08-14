title: Django小技巧12: 禁用单元测试的Migrations
date: 2018-10-29 18:12:42
set: Django小技巧
---

![](/uploads/images/disabling-migrations.jpeg "cover")


> 翻译整理自: [simpleisbetterthancomplex.com](https://simpleisbetterthancomplex.com/tips/2016/08/19/django-tip-12-disabling-migrations-to-speed-up-unit-tests.html)

Migrations 无疑是 Django 的一大特色功能，当它在单元测试的时候， 却会加长整个单元测试的时间。特别是你的migrations history特别的大.本篇是加快单元测试的小技巧:


为单元测试单独创建一个 settings

**tests_settings.py**

```python
from settings import *

# Custom settings goes here
```

然后在执行测试的时候，这样做:

```shell
python manage.py test --settings=myproject.tests_settings --verbosity=1
```


## Django >= 1.9

使用`MIGRATION_MODULES`设置项, 用于定义migration模块的自定义名称， 如果为`None`则是忽略此模块.


```python
from settings import *

MIGRATION_MODULES = {
    'auth': None,
    'contenttypes': None,
    'default': None,
    'sessions': None,

    'core': None,
    'profiles': None,
    'snippets': None,
    'scaffold_templates': None,
}
```

## Django < 1.9

如果是1.9之前的版本，可以用下面的方法。实际上， 我现在依然在使用它， 因为这种方法不需要指定各个模块.

```python
from settings import *

class DisableMigrations(object):
    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return 'notmigrations'

MIGRATION_MODULES = DisableMigrations()
```

## 更旧的版本 (使用: South)

```
SOUTH_TESTS_MIGRATE = False
```

这个可以写在生产的**settings.py**中.

