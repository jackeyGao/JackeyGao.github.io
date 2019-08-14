title: Python 可变参数的坑
date: 2017-07-04 12:19:43
---

Python 的可变参数有`*args`的位置可变参数和`**kwargs`参数可变两种. 今天在DEBUG的时候发现了一个非常棘手的`**kwargs`的坑.


具体代码为:

```python
cls(__auto_convert=False, _created=created, __only_fields=only_fields, **data)
```

正常情况, data为以下内容时此语句没有问题.

```python
data = {
    "user": "JG",
    "age": 18
}
```

但由于最近mongodb恢复数据的时候， 有重复数据。 mongodb会加上`_created`和`_modified`两个字段. 这样data的内容就成了下面这样.

```python
data = {
    "user": "JG",
    "age": 18,
    "_created": datetime.datetime(2017, 7, 1, 8, 11, 6, 699976),
    "_modified": datetime.datetime(2017, 7, 3, 13, 10, 6, 699976)
}
```

会产生什么BUG？ `_created`重复赋值问题.

```text
    obj = cls(__auto_convert=False, _created=created, __only_fields=only_fields, **data)
TypeError: TopLevelDocumentMetaclass object got multiple values for keyword argument '_created'
```

我的解决办法是删除了这两个无效字段.
