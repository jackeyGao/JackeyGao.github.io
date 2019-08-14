title: Django小技巧17: QuerySets的latest和earliest方法
date: 2018-11-05 14:58:39
set: Django小技巧
---

![](/uploads/images/earliest-latest.jpeg "cover")


> 翻译整理自: [simpleisbetterthancomplex.com](https://simpleisbetterthancomplex.com/tips/2016/10/06/django-tip-17-earliest-and-latest.html)

就像QuerySets的first和last方法一样, Django 还提供了`earliest`和`latest`方法. 用于获取最早和最新的数据，增强代码的可读性.


最好在模型的Meta类中先定义`get_latest_by`属性

```python
class Post(models.Model):
    headline = models.CharField(max_length=150)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    publication_date = models.DateTimeField(blank=True, null=True)
    change_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        get_latest_by = 'publication_date'
```

然后使用起来非常简单

```python
latest_post = Post.objects.latest()
earliest_post = Post.objects.earliest()
```

如果没有指定`get_latest_by`字段， 也可以通过参数来指定

```python
latest_change = Post.objects.latest('change_date')
```

如果以上两种方式都没有提供`get_latest_by`参数, 将会触发`DoesNotExist`错误. 它于 first 和 last 不同， 因为first和 last 在没有匹配到结果的情况下将会返回 None.


另外一个需要注意的点是， 和日期作为排序参数的时候， 可能会遇到日期为空的情况， 这时候工作的结果和我们想象的不一致。 所以我们可以过滤下日期为 Null 的结果，再做`earliest`和`latest`检索.

```python
Post.objects.filter(change_date__isnull=False).latest('change_date')
```

这两种方法， 通常与`DateField`、`DateTimeField`或`IntegerField`一起使用。应该避免和其他字段一起使用， 因为语义上是错误的。这两种方法主要是提供代码的方便性和可读性， 如果和非时间字段一起使用，会带来新的混淆.

