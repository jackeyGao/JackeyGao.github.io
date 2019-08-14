title: Django小技巧04: 自动日期时间字段
date: 2018-10-25 11:55:23
set: Django小技巧
---

![Time](/uploads/images/time.jpeg "cover")


> 翻译整理自: [simpleisbetterthancomplex.com](https://simpleisbetterthancomplex.com/tips/2016/05/23/django-tip-4-automatic-datetime-fields.html)

Django 的`DateTimeField`和`DateField`有两个非常有用的参数，用于自动管理时间。如果你需要跟踪保存纪录的创建时间和更改时间，则无须手动执行，只需要加上`auto_now`和`auto_now_add`参数并设置为`True`即可。 如下面例子所示:

```python
class Invoice(models.Model):
    description = models.CharField(max_length=255)
    status = models.CharField(max_length=10)
    vendor = models.ForeignKey(Vendor)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

- `auto_now_add`在创建的时候设置字段为`timezone.now()`
- `auto_now` 在每次调用`save`方法都会更新字段


需要注意的是， 两个参数都将使用`timezone.now()`更新字段值，这意味着纪录创建的时候两个字段都将会填充。

这是一个非常简单的技巧， 让你的代码变得非常清晰。




> 阅读更多关于Automatic DateTime Fields的文档. [Django Documentation](https://docs.djangoproject.com/en/dev/ref/models/fields/#datefield)
