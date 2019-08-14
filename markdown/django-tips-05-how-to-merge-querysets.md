title: Django小技巧05: 合并QuerySets
date: 2018-10-25 11:56:23
set: Django小技巧
---

![train tracks](/uploads/images/merge-queryset.jpg "cover")

> 翻译整理自: [simpleisbetterthancomplex.com](https://simpleisbetterthancomplex.com/tips/2016/06/20/django-tip-5-how-to-merge-querysets.html)

当你想要让两个或者多个 queryset 合并为一个 queryset 的时候， 并且希望使用 list， 而且想要保留对象的`filter`, `count`, `distinct`等 queryset 方法。


查看以下模型：


```python
class Story(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    category = models.ForeignKey(Category, related_name='stories')
    author = models.ForeignKey(User, related_name='stories')

class Medium(models.Model):
    name = models.CharField(max_length=30, unique=True)
    stories = models.ManyToManyField(Story)
```

假设你想显示特定的 Medium 中发布的故事以及属于特定作者的所有故事。那么一般情况下， 你用以下方法获取了两个 queryset。


```python
medium = Medium.objects.get(name='Django Blog')
user = User.objects.get(username='vitor')

django_stories = medium.stories.all()
vitor_stories = user.stories.filter(category__name='django')
```


此时我们有两个查询集(QuerySets) ,我们可以通过`|` 运算符来合并这两个查询集。


```python
stories = django_stories | vitor_stories  # merge querysets
```


此时你依然可以使用 queryset 的一些操作方法.


```python
recent_stories = stories.distinct().order_by('-date')[:10]
```

> %warning **注意:** 合并运算符仅适用于同一类型的 queryset， 并且数据为切片前数据集.

