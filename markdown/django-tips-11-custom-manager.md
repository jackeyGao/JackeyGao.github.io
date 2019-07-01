title: Django小技巧11: 自定义链式Queryset Manager
date: 2018-10-26 17:12:42
set: Django小技巧
---

![](/uploads/images/custom-manager.jpeg "cover")


> 翻译整理自: [simpleisbetterthancomplex.com](https://simpleisbetterthancomplex.com/tips/2016/08/16/django-tip-11-custom-manager-with-chainable-querysets.html)

在 Django Model 中，Manager是与数据库交互的接口。默认情况下Manager可通过`Model.objects`属性使用。默认情况下， 每个 Model 的默认 Manager 是`django.db.models.Manager`。扩展和重写默认Manager非常简单.


```python
from django.db import models

class DocumentManager(models.Manager):
    def pdfs(self):
        return self.filter(file_type='pdf')

    def smaller_than(self, size):
        return self.filter(size__lt=size)

class Document(models.Model):
    name = models.CharField(max_length=30)
    size = models.PositiveIntegerField(default=0)
    file_type = models.CharField(max_length=10, blank=True)

    objects = DocumentManager()
```


设置后， 你可以通过`pdfs`方法快速的过滤属于 PDF 的文档.


```python
Document.objects.pdfs()
```


当然，返回的结果是链式的， 依然拥有 queryset 的一些操作方法(`order_by` 或 `filter`等..).

```python
Document.objects.pdfs().order_by('name')
```

> %warning 但是， 如果你试图在使用自定义的一些方法， 链式将会中止:

```python
Document.objects.pdfs().smaller_than(1000)

AttributeError: 'QuerySet' object has no attribute 'smaller_than'
```

要使上述代码能够工作， 你必须创建自定义的`get_queryset`方法.


```python
class DocumentQuerySet(models.QuerySet):
    def pdfs(self):
        return self.filter(file_type='pdf')

    def smaller_than(self, size):
        return self.filter(size__lt=size)

class DocumentManager(models.Manager):
    def get_queryset(self):
        return DocumentQuerySet(self.model, using=self._db)  # Important!

    def pdfs(self):
        return self.get_queryset().pdfs()

    def smaller_than(self, size):
        return self.get_queryset().smaller_than(size)

class Document(models.Model):
    name = models.CharField(max_length=30)
    size = models.PositiveIntegerField(default=0)
    file_type = models.CharField(max_length=10, blank=True)

    objects = DocumentManager()
```

现在可以像任何的 QuerySet 方法一样使用他。 并且是链式的！


```python
Document.objects.pdfs().smaller_than(1000).exclude(name='Article').order_by('name')
```


> Manager 除了自定义 QuerySet 还可以做其他的工作， 如果你只在 Manager 中自定义 QuerySet ，推荐扩展下`models.QuerySet`, 并在模型中定义`objects = DocumentQuerySet.as_manager()`.

```python
class DocumentQuerySet(models.QuerySet):
    def pdfs(self):
        return self.filter(file_type='pdf')

    def smaller_than(self, size):
        return self.filter(size__lt=size)

class Document(models.Model):
    name = models.CharField(max_length=30)
    size = models.PositiveIntegerField(default=0)
    file_type = models.CharField(max_length=10, blank=True)

    objects = DocumentQuerySet.as_manager()
```


> 自定义的 Manager 代码， 你可以写在**models.py**， 但随着代码库的增长， 我更加推荐你将定义的` QuerySets` 和`Managers`保存名为**managers.py**文件中.

