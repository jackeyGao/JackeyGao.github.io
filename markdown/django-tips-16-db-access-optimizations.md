title: Django小技巧16: 数据库访问优化
date: 2018-11-05 13:04:39
set: Django小技巧
---

![错综复杂](/uploads/images/db-access-optimizations.jpeg "cover")


> 翻译整理自: [simpleisbetterthancomplex.com](https://simpleisbetterthancomplex.com/tips/2016/10/05/django-tip-16-simple-database-access-optimizations.html)

本篇分享数据库访问优化相关， 读完这些并不是让你立即去优化代码， 更多的时候对于现有代码的优化， 需要借助[Django Debug Toolbar](https://github.com/jazzband/django-debug-toolbar)来分析后， 再去相应的优化代码， 但今天要说的是一些简单的技巧， 用于你在编写代码的时候就所有规避不好用法， 使用推荐的用法.


## 访问外键值

如果你只需外键的ID


```python:Do
post.author_id
```

```python:Don't
post.author.id
```

如果你的博文中有一个 author 的外键，Django 会自动将主键存储在属性author\_id中, 而在author属性则是一个惰性的数据库引用。如果你如果使用author来访问 ID, 数据则会多出一个额外的查询，就会产生开销。


## 批量插入Many to Many字段

```python:Do
user.groups.add(administrators, managers)
```

```python:Don't
user.groups.add(administrators)
user.groups.add(managers)
```

## Count QuerySets

如果你只需获取 QuerySet count

```python:Do
users = User.objects.all()
users.count()

# Or in template...
{{ users.count }}
```

```python:Don't
users = User.objects.all()
len(users)

# Or in template...
{{ users|length }}
```

## Empty QuerySets

如果你只想知道 QuerySets 是否为空.

```python:Do
groups = Group.objects.all()
if groups.exists():
    # Do something...
```

```python:Don't
groups = Group.objects.all()
if groups:
    # Do something...
```

## 减少不必要的查询次数

就是之前讲过的 select\_related 

```python:Do
review = Review.objects.select_related('author').first()  # Select the Review and the Author in a single query
name = review.author.first_name
```

```python:Don't
review = Review.objects.first()  # Select the Review
name = review.author.first_name  # Additional query to select the Author
```

## 只检索需要的字段

假设模型**Invoice**有50个字段，你想要创建一个表格只显示摘要信息，包含**number**、**date**和**value**.

```python:Do
# views.py
# If you don't need the model instance, go for:
invoices = Invoice.objects.values('number', 'date', 'value')  # Returns a dict

# If you still need to access some instance methods, go for:
invoices = Invoice.objects.only('number', 'date', 'value')  # Returns a queryset

# invoices.html
<table>
  {% for invoice in invoices %}
    <tr>
      <td>{{ invoice.number }}</td>
      <td>{{ invoice.date }}</td>
      <td>{{ invoice.value }}</td>
    </tr>
  {% endfor %}
</table>
```

```python:Don't
# views.py
invoices = Invoice.objects.all()

# invoices.html
<table>
  {% for invoice in invoices %}
    <tr>
      <td>{{ invoice.number }}</td>
      <td>{{ invoice.date }}</td>
      <td>{{ invoice.value }}</td>
    </tr>
  {% endfor %}
</table>
```

## 批量更新

使用 `F()` 批量更新.

```python:Do
from django.db.models import F

Product.objects.update(price=F('price') * 1.2)
```

```python:Don't
products = Product.objects.all()
for product in products:
    product.price *= 1.2
    product.save()
```
