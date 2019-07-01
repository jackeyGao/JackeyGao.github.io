title: Django小技巧13: 使用F()表达式
date: 2018-10-29 18:49:08
set: Django小技巧
---

![](/uploads/images/f-expression.jpg "cover")


> 翻译整理自: [simpleisbetterthancomplex.com](https://simpleisbetterthancomplex.com/tips/2016/08/23/django-tip-13-f-expressions.html)

在 Django QuerySets API 中， F() 用于直接在数据库中引用模型的值。假设你有一个带有`price`的 Product 模型， 你希望为所有的Product的价格上涨20%.

一个可以实现在解决方案:

```python
products = Product.objects.all()
for product in products:
    product.price *= 1.2
    product.save()
```


相反， 你可以在单个查询中更新price.

```python
from django.db.models import F

Product.objects.update(price=F('price') * 1.2)
```

你也可以对单个对象执行这个操作:

```python
product = Product.objects.get(pk=5009)
product.price = F('price') * 1.2
product.save()
```

> %warning 要注意， 保存模型后， `F()`对象依然存在.

```python
product.price                   # price = Decimal('10.00')
product.price = F('price') + 1
product.save()                  # price = Decimal('11.00')
product.name = 'What the F()'
product.save()                  # price = Decimal('12.00')
```

所以， 在更新这样的字段后, `product.price`实际上保存的是`django.db.models.expressions.CombinedExpression`实例， 而不是实际结果。

如果要立即访问结果:

```python
product.price = F('price') + 1
product.save()
print(product.price)            # <CombinedExpression: F(price) + Value(1)>
product.refresh_from_db()
print(product.price)            # Decimal('13.00')
```

你可以使用`F()`实现annotate功能:


```python
from django.db.models import ExpressionWrapper, DecimalField

Product.objects.all().annotate(
    value_in_stock=ExpressionWrapper(
        F('price') * F('stock'), output_field=DecimalField()
    )
)

```

由于price是DecimalField, 而stock是IntegerField，我们需要将表达式包装在`ExpressionWrapper`中.

也可以用来过滤数据:

```python
Product.objects.filter(stock__gte=F('ordered'))
```

