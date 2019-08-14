title: Django 一个模型不同Table的操作
date: 2018-12-11 12:58:53
---

![](/uploads/images/django-dynamic-tables.jpeg "cover")

教程代码托管在 <i class="github icon"></i>[JackeyGao](https://github.com/jackeyGao) / [django-dynamic-tables](https://github.com/jackeyGao/django-dynamic-tables)

用过 Django 框架的都知道， 模型定义是开发一个项目前面需要做的事情， 后面通过导入的方式在 View 中操作。 这样的流程是 Django 默认的流程， 但流程是一成不变的吗？ 大多数时候， 我们的设计的系统， Django 默认的框架都不能适用， Django 的确封装了很多功能组件，让MVT架构更有效率的开发， 您在设计的时候必须按照它们设计好的框架里面设计程序。 但今天要讲是一种比较干燥的方式

假设我有一个需求是一个日志表(log)，需要动态的根据每天生成结果表(log\_20181211, log\_20181212)。


默认情况下， 我们需要定义Model

**models.py**


```python
class Log(models.Model):
    level = models.IntegerField(choices=LOG_LEVELS)
    msg = models.TextField()
    time = models.DateTimeField(auto_now=True, auto_now_add=True)

    class Meta:
        db_table = "log"
```

然后通过 migrate 创建表， 这样的代码很属于 Django 风格，但实现不了我们的需求。 默认的 Django ORM 操作没有根据时间切割表. migrate 之后这张表就已经永久创建了。 后面操作这个 Model 一直在操作 log 这张表.

## 动态的创建表

动态的创建模型其实就是在运行时生成 Model 类， 这个可以通过函数实现， 通过传参(今天的日期, 如: 20181211)，然后生成新的模型类， Meta 中的 db\_table 为log\_20181211. 

```python
def get_log_model(prefix):
    table_name = 'log_%s' % str(prefix)

    LOG_LEVELS = (
        (0, 'DEBUG'),
        (10, 'INFO'),
        (20, 'WARNING'),
    )

    class LogMetaclass(models.base.ModelBase):
        def __new__(cls, name, bases, attrs):
            name += '_' + prefix  # 这是Model的name.
            return models.base.ModelBase.__new__(cls, name, bases, attrs)

    class Log(models.Model):
        __metaclass__ = LogMetaclass
        level = models.IntegerField(choices=LOG_LEVELS)
        msg = models.TextField()
        time = models.DateTimeField(auto_now=True, auto_now_add=True)

        @staticmethod
        def is_exists():
            return table_name in connection.introspection.table_names()

        class Meta:
            db_table = table_name

    return Log
```

可以看到， 通过函数生成不同的 Log Class. 注意LogMetaclass和\_\_metaclass\_\_  , 元类可以在运行时改变模型的名字，table 的名称我们可以通过db\_table定义, 类的名称可以通过覆盖元类的方法定义。

```python
print cls.__name__
Log_20181211
print cls._meta.db_table
log_20181211
```

## 使用

使用直接通过函数， 获取当前日期的 Log 模型， 然后通过is\_exists判读表是否创建， 没有创建则创建对应的表. 


```python
def index(request):
    today = date.today().strftime("%Y%m%d")

    # RuntimeWarning: Model '__main__.logclasslog_' was already registered.
    # Reloading models is not advised as it can lead to inconsistencies
    # most notably with related models.
    # 如上述警告所述, Django 不建议重复加载 Model 的定义.
    # 作为 demo 可以直接通过get_log_model获取，无视警告.
    # 所以这里先通过 all_models 获取已经注册的 Model,
    # 如果获取不到， 再生成新的模型.
    try:
        cls = apps.get_model('__main__', 'Log_%s' % today)
    except LookupError:
        cls = get_log_model(today)

    if not cls.is_exists():
        with connection.schema_editor() as schema_editor:
            schema_editor.create_model(cls)

    log = cls(level=10, msg="Hello")
    log.save()

    return HttpResponse('<h1>%s</h1>' % cls._meta.db_table)
```

上面获取 cls 部分， 这里的代码先通过apps的已经注册的 all\_models 获取, 否则一个模型的第二次执行定义代码就会抛出RuntimeWarning警告, 在模型的初始化函数都会注册此模型, 最好不要重复注册. 先通过 **apps.get\_model** 获取这个模型， 如果没有获取到则通过**get\_log\_model**初始化新的模型. 这样做更加稳妥一点.

代码托管在 <i class="github icon"></i>[JackeyGao](https://github.com/jackeyGao) / [django-dynamic-tables](https://github.com/jackeyGao/django-dynamic-tables)

