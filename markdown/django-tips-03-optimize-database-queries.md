title: Django小技巧03: 优化数据库查询
date: 2018-10-25 11:54:23
set: Django小技巧
---

![Fast](/uploads/images/odq.jpeg "cover")


> 翻译整理自: [simpleisbetterthancomplex.com](https://simpleisbetterthancomplex.com/tips/2016/05/16/django-tip-3-optimize-database-queries.html)


本文介绍一个非常简单的技巧， 能够帮助你在使用 `Django ORM` 时优化数据库查询.

需要注意的是， Django QuerySets 是惰性查询的， 如果使用得当非常适用。

例如， 我们有一个叫做Invoice模型，并执行以下代码:

```python
invoices = Invoice.objects.all()
unpaid_invoices = invoices.filter(status='UNPAID')
```

此时， `Django ORM` 还没有触及到数据库，也就是说没有执行操作。当我们调用这个 queryset(unpaid_invoices) 才会真正的执行到数据库查询。通常情况下， 当我们去遍历这个 Queryset 就会发生这种情况， 即 queryset 开始执行。如下面代码所示:

```django
<table>
  <tbody>
  {% for invoice in unpaid_invoices %}
    <tr>
      <td>{{ invoice.id }}</td>
      <td>{{ invoice.description }}</td>
      <td>{{ invoice.status }}</td>
    </tr>
  {% endfor %}
  </tbody>
</table>
```

上面的代码， 看起来没有什么问题。只会执行一个数据库查询。 但是当您的模型有关系数据字段时， 比如`ForeignKey`, `OneToOneField` 或 `ManyToManyField`. 上面的查询就会发生变化了。 

假设`Invoice`模型有一个vendor字段是个`ForeignKey`:

```python
class Invoice(models.Model):
    description = models.CharField(max_length=255)
    status = models.CharField(max_length=10)
    vendor = models.ForeignKey(Vendor)
```


现在和上面的模板中一样去迭代这个 queyset， 但这次显示了供应商名称，`Django ORM`将对`unpaid_invoices`数据集每一条记录执行一次额外的查询.

```django
<table>
  <tbody>
  {% for invoice in unpaid_invoices %}
    <tr>
      <td>{{ invoice.id }}</td>
      <td>{{ invoice.description }}</td>
      <td>{{ invoice.status }}</td>
      <td>{{ invoice.vendor.name }}</td>
    </tr>
  {% endfor %}
  </tbody>
</table>
```

如果`unpaid_invoices`数据集有100条记录， 那么将会有101条查询生成。检索invoices所有对象的一条查询， 和每个invoice供应商的一次查询， 共计101条。

当然， 可以使用`select_related`方法， 来减轻这种不期望的影响，以便在单次数据查询中，检索所有必要的信息。

所以，不要像上面那样过滤未付款的发票，可以这样做:

```python
invoices = Invoice.objects.all()
unpaid_invoices = invoices.select_related('vendor').filter(status='UNPAID')
```

这样， `Django ORM` 将会在同一查询中为每个发票检索供应商数据.因此这种情况不需要额外的查询，这样可以为您的应用程序出色的性能提升。

推荐一个可以跟踪数据库查询的调试工具[Django Debug Toolbar](https://django-debug-toolbar.readthedocs.io/)


> 阅读更多关于Django QuerySet API的文档. [Django Documentation](https://docs.djangoproject.com/en/dev/ref/models/querysets/#select-related)
