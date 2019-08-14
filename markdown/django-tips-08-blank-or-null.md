title: Django小技巧08: Blank or Null
date: 2018-10-26 12:12:51
set: Django小技巧
---

![](/uploads/images/blank-or-null.jpg "cover")


> 翻译整理自: [simpleisbetterthancomplex.com](https://simpleisbetterthancomplex.com/tips/2016/07/25/django-tip-8-blank-or-null.html)

Django Model API 中提供了`blank`和`null`两个参数， 非常容易混淆。当我第一次使用 Django 的时候， 总是不能恰当的使用这两个参数。

看起来两者都做了几乎相同的事情， 但是这两者还是有区别的：

- **null**: 数据库相关； 定义数据库字段的值是否接受空值。
- **blank**: 验证相关， 当调用`form.is_valid()`时， 将会判断值是否为空.

虽然两者的是有区别的， 但一个拥有`null=True`和`blank=False`的字段是完全没有问题的。 在数据库级别上， 该字段可以为 NULL， 但在应用程序级别上， 它是必填字段(前提你通过 Django 标准的 Form 进行判断)。

大多数开发人员都对基于字符串的字段(`CharField`和`TextField`)定义`null=True`, 这其实是没有必要的, 应该避免这样做，因为 Django约定使用空字符串设置空值， 而非**Null**.

所以， 如果你想设置一个基于字符的字段可以为空，那么你应该这样做:


```python
class Person(models.Model):
    name = models.CharField(max_length=255)  # 强制填写
    bio = models.TextField(max_length=500, blank=True)  # 可选填写 (不要设置null=True)
    birth_date = models.DateField(null=True, blank=True) # 可选填写 (这里你应该设置null=True)
```

## 默认值

- **null**: False
- **blank**: False

## NullBooleanField

当您需要为`BooleanField`字段设置允许为空时， 您应该使用`NullBooleanField`代替，**而非通过参数**.

