title: 五个很实用的Django 项目推荐
date: 2016-08-16 13:24:11
---

很多Django的包都能很大的增加我们的开发效率或者增加我们项目的功能， 比如: [django-rest-framework](https://github.com/tomchristie/django-rest-framework/) 、[wagtail](https://github.com/torchbox/wagtail), 它们带来了很棒的功能. 但是今天我想推荐一些其他的包， 更有爱的包.

## [django-sql-explorer](https://github.com/groveco/django-sql-explorer)

有时候你的用户想通过执行SQL的方式来访问你数据库里面的数据， 但处于某些安全的原因，你不能给他们直接执行数据库的权限.但django-sql-explorer 可以让用户通过web端沙盒的方式执行SQL并可以下载执行结果(CSV), 排序数据和数据透视操作.

![A view of a query](/uploads/images/django-sql-explorer-1.png "A view of a query")
![Quick access to DB schema info](/uploads/images/django-sql-explorer-2.png "Quick access to DB schema info")
![Viewing all queries](/uploads/images/django-sql-explorer-3.png "Viewing all queries")

## [django-tables-2](https://github.com/bradleyayers/django-tables2)

很多数据在web中通过表格展示， 通过它能够很方便的操作HTML表格, 让你非常容易的在Django中操作表格. 它提供了`数据排列`、`数据排序`、`数据分页`.

可以通过[django-filter](https://github.com/carltongibson/django-filter)很容易的扩展搜索和过滤数据, 无论前端是bootstrap还是foundation或你自己开发的前端, 它可以完全兼容.

```python
import django_tables2 as tables
from .models import Address
class AddressTable(tables.Table):
    user = tables.Column(accessor='address.user')
    zip_code = tables.Column(verbose_name='Zip')
    city = tables.Column(verbose_name='Town')
    
    class Meta:
        model = Address
        order_by = '-zip_code'
        fields = sequence = ('user', 'zip_code', 'city',)
```

## [django-wiki](https://github.com/django-wiki/django-wiki)

有时, 你需要wiki功能, 可以使用django-wiki来扩展到自己的项目中.它也可以工作在某一个区域, 当然这需要你自己在模版中指定. 它支持markdown, 版本控制, 和开箱即用的Box UI.

![django-wiki](/uploads/images/django-wiki-demo.png "django-wiki")

## [django-reversion-compare](https://github.com/jedie/django-reversion-compare)

[django-reversion](https://github.com/etianen/django-reversion) 已经非常棒了, 然而对每一个变更都加入了比较功能, 你可以对变更做如下图一样直观的比较.

![django-reversion-compare](/uploads/images/django-reversion-compare.png)

## [django-rest-hooks](https://github.com/zapier/django-rest-hooks)

REST APIs 是很棒的接口设计, 而且[django-rest-framework](https://github.com/tomchristie/django-rest-framework/)能很好的提供这个功能. 但是如果你仅仅是基于事件来获取数据, 那么你需要一个webhook. 使用这个包可以非常容易的以REST框架装饰你的模型. 下面就是相应的代码.


```python
### settings.py ###

INSTALLED_APPS = (
    # other apps here...
    'rest_hooks',
)

HOOK_EVENTS = {
    'book.added':       'bookstore.Book.created',
    'book.changed':     'bookstore.Book.updated+',
    'book.removed':     'bookstore.Book.deleted',
    'book.read':        'bookstore.Book.read',
    'user.logged_in':    None
}

### bookstore/models.py ###

class Book(models.Model):
    user = models.ForeignKey('auth.User')
    title = models.CharField(max_length=128)
    pages = models.PositiveIntegerField()
    fiction = models.BooleanField()

    def serialize_hook(self, hook):
        return {
            'hook': hook.dict(),
            'data': {
                'id': self.id,
                'title': self.title,
                'pages': self.pages,
                'fiction': self.fiction,
            }
        }

    def mark_as_read(self):
        from rest_hooks.signals import hook_event
        hook_event.send(
            sender=self.__class__,
            action='read',
            instance=self # the Book object
        )
### USAGE ###
>>> from django.contrib.auth.models import User
>>> from rest_hooks.model import Hook
>>> jrrtolkien = User.objects.create(username='jrrtolkien')
>>> hook = Hook(user=jrrtolkien,
                event='book.added',
                target='http://example.com/target.php')
>>> hook.save()     # creates the hook and stores it for later...
>>> from bookstore.models import Book
>>> book = Book(user=jrrtolkien,
                title='The Two Towers',
                pages=327,
                fiction=True)
>>> book.save()     # fires off 'bookstore.Book.created' hook automatically
...
```


#### 原文地址: https://medium.com/@raiderrobert/5-django-packages-that-get-too-little-love-d55232c28640
