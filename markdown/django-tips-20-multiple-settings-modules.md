title: Django小技巧20: 使用多个settings模块
date: 2018-11-09 13:22:43
set: Django小技巧
---

![](/uploads/images/multiple-settings-modules.jpeg "cover")

> 翻译整理自: [simpleisbetterthancomplex.com](https://simpleisbetterthancomplex.com/tips/2017/07/03/django-tip-20-working-with-multiple-settings-modules.html)

通常来说， 为了保持项目的配置简单，我们会避免使用多个配置文件。但理想很丰满， 现实是随着项目越来越大， **settings.py**可能也会变得相当复杂. 在那种情况下， 你必须使用大量的`if`语句，类似于: if not DEBUG: # do something... .为了将**development**配置和**production**严格的分离，你可以将**settings**模块分解成多个文件. 这样对我们的配置可能更加清楚.

## 默认的基本结构

一个全新的 Django 项目结构默认情况下如下所示


```text
mysite/
 |-- mysite/
 |    |-- __init__.py
 |    |-- settings.py
 |    |-- urls.py
 |    +-- wsgi.py
 +-- manage.py
```

我们在mysite目录中创建一个叫做**settings**的目录, 然后将原有的**settings.py**移动到 settings 目录中， 并更改名字为**base.py**. 如果使用 Python 2.x 增加`__init__.py``文件.

```text
mysite/
 |-- mysite/
 |    |-- __init__.py
 |    |-- settings/         <--
 |    |    |-- __init__.py  <--
 |    |    +-- base.py      <--
 |    |-- urls.py
 |    +-- wsgi.py
 +-- manage.py
```

顾名思义, base.py 将提供适用于所有环境(development, production, staging, 等)配置.

然后为每个环境创建一个**settings**模块. 常见的用例有


- ci.py
- development.py
- production.py
- staging.py

然后文件结构应该和下面类似:


```text
mysite/
 |-- mysite/
 |    |-- __init__.py
 |    |-- settings/
 |    |    |-- __init__.py
 |    |    |-- base.py
 |    |    |-- ci.py
 |    |    |-- development.py
 |    |    |-- production.py
 |    |    +-- staging.py
 |    |-- urls.py
 |    +-- wsgi.py
 +-- manage.py
```

## 配置新的settings.py

依下面的base.py为例:


**settings/base.py**

```python
from decouple import config

SECRET_KEY = config('SECRET_KEY')

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'mysite.core',
    'mysite.blog',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mysite.urls'

WSGI_APPLICATION = 'mysite.wsgi.application'
```

为了保证实例简单， 我删除其他无效的代码


然后创建**development.py**配置文件， 我可以直接通过 base 来扩展.


**settings/development.py**

```python
from .base import *

DEBUG = True

INSTALLED_APPS += [
    'debug_toolbar',
]

MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware', ]

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DEBUG_TOOLBAR_CONFIG = {
    'JQUERY_URL': '',
}
```

然后， 你可以这样定义**production.py**模块

```python
from .base import *

DEBUG = False

ALLOWED_HOSTS = ['mysite.com', ]

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.mailgun.org'
EMAIL_PORT = 587
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = True
```

**注意:** 应该避免使用`import *`导入，`*`导入可能会在命名空间作用域中导入一些不必要的东西. 在某些情况下可能会产生冲突, 造成奇怪的问题. 另外一个问题是即使使用多个配置文件， 你依然要注意敏感数据的问题. 强烈推荐使用**Python-Decouple ** 这样的库来保护配置, 或者通过环境变量的形式使用密码或密钥配置.


## 如何使用多个配置文件


因为我们代码库中已经没有`settings.py`文件， 所以不能直接使用`python manage.py runserver`.相反你必须在命令参数中指定settings模块.


```shell
python manage.py runserver --settings=mysite.settings.development
```

Or

```shell
python manage.py migrate --settings=mysite.settings.production
```

由于我们在开发中经常使用 manage.py, 因此你可以在**manage.py**中， 硬编码写死配置模块.

**manage.py**

```python
#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings.development")  # <-- Change here!
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise
    execute_from_command_line(sys.argv)
```

所以， 我们只改动了一行

```python
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
```

改为

```python
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings.development")
```

## 也许可以更稳妥


现在我们有了多个配置模块， 这样你可以将**AUTH_PASSWORD_VALIDATORS**配置从**base.py**中移动到**production.py**中. 这样, 你可以在开发环境中使用简单密码(如: "123"). 但在生产环境中必须要通过密码验证才能使用.

在你测试环境中的配置文件中(settings/ci.py or settings/tests.py), 覆盖以下配置, 以便加快你的测试用例速度:


```python
DATABASES['default'] = {
    'ENGINE': 'django.db.backends.sqlite3'
}

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
)
```

## 结论

多个配置文件虽然提供了便利， 但你还是需要小心使用. 任何情况下都要考虑安全. 如果有疑问， 通过下面评论讨论.
