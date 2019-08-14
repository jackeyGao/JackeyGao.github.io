title: Django小技巧21: 使用重定向
date: 2018-11-09 15:14:28
set: Django小技巧
---

![](/uploads/images/redirects.jpeg "cover")

> 翻译整理自: [simpleisbetterthancomplex.com](https://simpleisbetterthancomplex.com/tips/2017/08/11/django-tip-21-redirects-app.html)


Django 附带了一组可以轻松安装的可选模块, 其中一个模块就是重定向的模块, 它在您想要更新某些现有URL而不损害您的网站SEO或在任何情况下避免404错误的情况下特别有用。

比如我现有的 URL 是

```url
/tips/2017/08/11/django-tip-21.html
```

在某一次更新之后 URL 有变动变成了:

```url
/tips/redirects-app/
```

而且我原有 URL， 已经被搜索引擎收录. 我不想在用户通过搜索引擎点过来是404页面。 这时候就需要做重定向到新的地址


redirects 模块是通过在数据库中创建一张表, 包含两个字段(old\_path和new\_path)来实现的.每当你的项目出现404错误的时候，redirects 组件将会拦截404响应， 并检索特定的 table 进行匹配, 如果在特定的 table 中匹配到old\_path ,将会重定向到所绑定的new\_path. 不会返回404, 而返回一个301响应(Moved Permanently).

OK, 让我看看redirects在实践中如何执行

## 安装

Django redirects 组件需要安装**sites**框架. 通过**settings.py**的**INSTALLED_APPS**来添加到项目中。


**settings.py**


```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django.contrib.sites',
    'django.contrib.redirects',
]
```

设置`SITE_ID`让**sites**框架能够工作.

**settings.py**

```python
SITE_ID = 1
```

现在将redirects的中间件添加到**MIDDLEWARE**

**settings.py**

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
]
```

通过**migrate**创建所需要的表：

```shell
python manage.py migrate
```

## 使用

最简单的方式通过 Django Admin 来对这个表添加记录. 如果你没有 Django Admin, 并且此操作是一次性的事情, 你可以通过redirects的 Python API 或者创建一个**fixture**. 如果你不使用Django Admin 但这个不是一次性的事情， 需要后面维护更新这个表， 那么你需要创建一个自己的视图管理页面.

### 通过DjangoAdmin管理redirects

默认情况下， 安装后会自动加到 Django Admin 界面

![Django Admin 管理 redirects](/uploads/images/redirects-admin.png)

只需添加对应的路径， redirects组件将会自动完成这个重定向工作

![redirects table](/uploads/images/redirects-admin-create.png)

你可以通过浏览器来访问旧的路径， 看看他是否能够正常的重定向. 另一种方法是检测响应的body, 可以通过`curl`来完成:

```shell
curl --head 127.0.0.1:8000/tips/2017/08/11/django-tip-21.html

HTTP/1.0 301 Moved Permanently
Date: Fri, 11 Aug 2017 15:42:27 GMT
Server: WSGIServer/0.2 CPython/3.6.1
Content-Type: text/html; charset=utf-8
Location: /tips/redirects-app/
X-Frame-Options: SAMEORIGIN
Content-Length: 0
```

### 通过Python API管理redirects

你可以通过 Django ORM 来对 redirects 的 Model 进行操作管理. 它位于[django/contrib/redirects/models.py](https://github.com/django/django/blob/master/django/contrib/redirects/models.py).

以下是创建redirects 条目的示例代码:


```python
from django.contrib.redirects.models import Redirect
from django.contrib.sites.models import Site
from django.conf import settings

site = Site.objects.get(pk=settings.SITE_ID)

Redirect.objects.create(site=site, old_path='/index.html', new_path='/')
Redirect.objects.create(site=site, old_path='/tips/2017/08/11/django-tip-21.html', new_path='/tips/redirects-app/')
```

### 通过Fixtures导入redirects

关于Fixtures, 是 Django 提供的一个功能， 可以到这里[查看文档了解更多](https://code.djangoproject.com/wiki/Fixtures).

首先按照以下示例的模板创建 JSON 文件

**redirects-fixture.json**

```json
[
   {
      "model":"redirects.redirect",
      "fields":{
         "site":1,
         "old_path":"/tips/2017/08/11/django-tip-21.html",
         "new_path":"/tips/redirects-app/"
      }
   },
   {
      "model":"redirects.redirect",
      "fields":{
         "site":1,
         "old_path":"/index.html",
         "new_path":"/"
      }
   }
]
```

然后通过命令将其加载到数据库


```shell
python manage.py loaddata redirects-fixtures.json
Installed 2 object(s) from 1 fixture(s)
```

就是这样~
