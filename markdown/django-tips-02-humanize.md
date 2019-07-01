title: Django小技巧02: humanize
date: 2018-10-25 11:53:23
set: Django小技巧
---

![humanize](/uploads/images/humanize.jpeg "cover")


> 翻译整理自: [simpleisbetterthancomplex.com](https://simpleisbetterthancomplex.com/tips/2016/05/09/django-tip-2-humanize.html)

Django 附带一组模板过滤器， 可为您的数据添加"人性化"选项。它用于将数字或者日期转化为人类友好可读的格式.


就我个人来说， 我使用模板过滤器`naturaltime`非常频繁。 比如我在`2018-10-25 11:33:24`定了个外卖， 在等待外卖的过程中， 订单页面的时间显示为`21 minutes ago`(考虑到目前是`2018-10-25 11:54:46`) 更好友好一点， 我能清楚的知道我等待了多长时间。 而不是`2018-10-25 11:54:46`这样的时间， 让我再计算一遍.

使用方法也非常简单:

在 `settings.py` `INSTALLED_APPS` 加入`django.contrib.humanize`.

```python
INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django.contrib.humanize',
]
```

然后在 template 中, 载入此 APP 下的标签。

```django
{% load humanize %}
```

使用过滤器也非常简单， 比如使用`naturaltime`过滤器.

```django
{% extends 'base.html' %}

{% load humanize %}

{% block content %}
  <ul>
    {% for notification in notifications %}
      <li>
        {{ notification }}
        <small>{{ notification.date|naturaltime }}</small>
      </li>
    {% empty %}
      <li>You have no unread notification.</li>
    {% endfor %}
  </ul>
{% endblock %}
```
- 功能表

| 过滤器        | 作用          | 举例  |
| :-----------: |:-------------:| :-----|
| apnumber      | 英文数字      | `1` => `one` |
| intcomma      | 三位逗号数字  | `4500000` => `4,500,000` |
| intword       | 文本数字      | `4500000` => `4.5 million` |
| naturalday    | 友好的日期    | `2018-10-24` => `yesterday` |
| naturaltime   | 友好的时间    | `2018-10-25 12:00:01` => `a minute ago.` |
| ordinal       | 序数字符串    | `3` => `3rd` |



> 阅读更多关于humanize的文档. [Django Documentation](https://docs.djangoproject.com/en/dev/ref/contrib/humanize/)
