title: Django + MySQL 查询不区分大小写问题
date: 2018-05-29 15:40:00
---

最近发现一个现象是测试环境的 sqlite 是可以区分大小写的。

就是说

```Python
# sqlite 环境
>>> Company.objects.filter(name='Teambition')
<QuerySet [<Company: Teambition>]>


>>> Company.objects.filter(name='teambition')
<QuerySet [<Company: teambition>]>
```

而到了线上的 MySQL 就不区分大小写了。

```python
# MySQL 环境
>>> Company.objects.filter(name='teambition')
[<QuerySet [<Company: Teambition>]>, <QuerySet [<Company: teambition>]>]
```

获得到两个实例。 但这样不是我预想的。


起初我查询了官方文档， 得到指引使用`__exact`方法. 即:


```python
Company.objects.filter(name__exact='teambition') 
```

但是无效！！！


由于测试环境的 sqlite 没有问题， 所以怀疑在 mysql 的配置上面。 原来是字符集校对规则的问题， `utf8_general_ci` 不区分大小写, 可以改成`utf8_bin`(将字符串中的每一个字符用二进制数据存储，区分大小写。) 或者 `utf8_general_cs`(cs为case sensitive的缩写，即大小写敏感).

但是, 由于我程序段没有操作数据库的权限， 所以没有去 alter 已经有的 TABLE。 我找到另外的一种解决方式


通过 DJANGO ORM 的`extra`, 在匹配语句上面加上BINARY来区分大小写.


```python
if settings.ENV == 'prod':
    # 线上的 MySQL 数据库加上 binary
    app = Company.objects.extra(where=['binary name=%s'], params=[options['app'],]).first()
else:
    # Sqlite 不做处理
    app = Company.objects.filter(name=options['app']).first()

```



**参考:**

- 1. [https://www.v2ex.com/t/138452](https://www.v2ex.com/t/138452)
- 2. [https://stackoverflow.com/questions/10929836/utf8-bin-vs-utf-unicode-ci](https://stackoverflow.com/questions/10929836/utf8-bin-vs-utf-unicode-ci)
- 3. [https://docs.djangoproject.com/en/dev/ref/models/querysets/#extra](https://docs.djangoproject.com/en/dev/ref/models/querysets/#extra)
