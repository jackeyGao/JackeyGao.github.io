title: Django小技巧19: 保护敏感信息
date: 2018-11-05 16:11:09
set: Django小技巧
---

![](/uploads/images/protecting-sensitive-information.jpg "cover")

> 翻译整理自: [simpleisbetterthancomplex.com](https://simpleisbetterthancomplex.com/tips/2016/10/17/django-tip-18-translations.html)


互联网是一片荒地， 在互联网上部署 Web 服务的时候， 安全是首要考虑的。Django 在提供可靠和安全的API方面做的非常出色.但是前提是你要正确的使用它们。


**永远不应该在部署 WEB 服务的时候开启 DEBUG=True**


DEBUG = True 一个很大的功能是发生异常的时候从你的环境中转储大量元数据， 并且暴露在页面中。包括整个 settings.py 的配置.

即使你永远不会使用DEBUG = True, 在 settings.py 中命名配置时也需要格外的小心， 确保你的所有敏感配置的字段都包含下面关键字之一：

- API
- KEY
- PASS
- SECRET
- SIGNATURE
- TOKEN

这样 Django 就不好转储哪些包含敏感信息的配置变量.

```python:good#Do
S3_BUCKET_KEY = 'xxxxxxxxxxxxxxxx'
```

```python:error#Don't
S3_BUCKET = 'xxxxxxxxxxxxxxxx'
JENKINS_MIMA = 'xxxxxxxxxxxxxxxx'  # 使用中文命名 jenkins_token
```

即便你关闭的 DEBUG， 如果 Django 配置了电子邮件发送错误报告，也会有可能在公网环境中泄露错误报告从而泄露 settings 配置, 特别是没有加密的电子邮件传输协议。

> **特别注意的一点：** 永远不要把敏感信息提交到公共代码仓库！换句话说，就说不要把敏感信息添加到 settings.py 中， 最好的方式是使用环境变量或者python-decouple. 后续会写一篇将配置上下线分离的文章

说到过滤错误报告，你应该使用两个过滤器:

### sensitive\_variables

可以定义一组局部敏感变量， 这些变量不好显示在错误报告中，从而达到保护它们的作用。

```python
from django.views.decorators.debug import sensitive_variables

@sensitive_variables('user', 'pw', 'cc')
def process_info(user):
    pw = user.pass_word
    cc = user.credit_card_number
    name = user.name
    ...
```

或者 ，如果想保护函数里的所有变量

```python
@sensitive_variables()
def my_function():
    ...
```

PS: 使用多个装饰器的时候， 确保`@sensitive_variables()`装饰器在第一个位置.

### sensitive\_post\_parameters

与前面的例子类似， 但这个处理 post 参数.

```python
from django.views.decorators.debug import sensitive_post_parameters

@sensitive_post_parameters('pass_word', 'credit_card_number')
def record_user_profile(request):
    UserProfile.create(
        user=request.user,
        password=request.POST['pass_word'],
        credit_card=request.POST['credit_card_number'],
        name=request.POST['name'],
    )
    ...
```

隐藏 post 所有参数

```python
@sensitive_post_parameters()
def my_view(request):
    ...
```


> 阅读更多关于过滤敏感信息的文档. [Django Documentation](https://docs.djangoproject.com/en/dev/howto/error-reporting/#filtering-sensitive-information)
