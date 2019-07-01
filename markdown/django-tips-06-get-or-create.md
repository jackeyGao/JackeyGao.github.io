title: Django小技巧06: get_or_create
date: 2018-10-26 11:08:23
set: Django小技巧
---

![](/uploads/images/get-or-create.jpg "cover")


> 翻译整理自: [simpleisbetterthancomplex.com](https://simpleisbetterthancomplex.com/tips/2016/07/14/django-tip-6-get-or-create.html)

`get_or_create` 是查找对象的一种便捷方法， 其最大的功能点是在目标对象不存在的时候， 可以根据参数创建对象。

它实际上返回一个`(object, created)`元祖，第一个元素是您要检索 get 的模型的实例，第二个元素是个是否创建的布尔值，用户判断实例是否是创建的。

如果实例已经存在数据库中， 并且通过参数可以找到， 那么 created 为 False， 反之则会创建， created 为 True。

定义个名为`AppSettings`的模型， 你可以在此存储配置：

```python
obj, created = AppSettings.objects.get_or_create(name='DEFAULT_LANG')
obj.value = request.POST.get('DEFAULT_LANG')
obj.save()
```

如上面代码所示， 如果这是我第一次运行这段代码保存名为`DEFAULT_LANG`的配置，`get_or_create`将创建一个实例并在数据库中保留。 如果这是我第二次或者第三次调用此段代码， 它只会更新现有实例, 而原有的实例ID和name不会改变.

