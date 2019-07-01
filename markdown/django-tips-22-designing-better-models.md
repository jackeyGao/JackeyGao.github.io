title: Django小技巧22: 设计一个好的模型
date: 2018-11-09 16:14:28
set: Django小技巧
---

![](/uploads/images/designing-better-models.jpeg "cover")

> 翻译整理自: [simpleisbetterthancomplex.com](https://simpleisbetterthancomplex.com/tips/2018/02/10/django-tip-22-designing-better-models.html)

本篇将分享一些技巧，用户改进 Model 的设计。其中有很多与命名约定有关， 这可以大大的提高代码的可读性。

[PEP8](https://www.python.org/dev/peps/pep-0008/)规范， 广泛用于 Python 领域, 因此我建议你在项目中使用它.

除了 PEP8 ， 我更喜欢[Django编程风格](https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/coding-style/).


本篇目录:

- [命名你的Model](#naming-your-models)
- [Model定义顺序](#model-style-ordering)
- [反向关系](#reverse-relationships)
- [Blank 和 Null](#blank-and-null-fields)


<h2 id="naming-your-models">命名 Model</h2>

模型定义使用**CapWords**约定(没有下划线). 例如: `User`, `Permission`, `ContentType`.

模型的属性使用 [**snake\_case**](https://en.wikipedia.org/wiki/Snake_case). 例如: `first_name`, `last_name`.

如:

```python
from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=30)
    vat_identification_number = models.CharField(max_length=20)
```

**始终使用单数明明你的模型**, 用**Company**代替**Companies**. 模型的定义是对单个对象的表示， 而不是公司的集合.

这通常会导致混淆，因为我们倾向于通过数据库思考。模型最终被翻译成table.该表使用其复数形式命名的.

在 DJango 中，我们可以通过`Company.objects`来访问集合. 我可以通过定义**models.Manager**重命名**objects**属性.

```python
from django.db import models

class Company(models.Model):
    # ...
    companies = models.Manager()
```


而后， 可以通过下面语句来使用 Django ORM QuerySet 查询.


```python
Company.companies.filter(name='Google')
```


这样看起来代码就很有可读性了


<h2 id="model-style-ordering">Model 定义顺序</h2>

Django Coding Style 建议内部类，方法和属性的顺序为：



- 如果字段有`choices`参数, 则每个选项定义为元祖中元祖.并使用全大写的名称作为值属性。
- 所有数据库fields
- Custom manager attributes
- class Meta
- def \_\_str\_\_()
- def save()
- def get\_absolute\_url()
- 其他自定义方法

如:

```python
from django.db import models
from django.urls import reverse

class Company(models.Model):
    # CHOICES
    PUBLIC_LIMITED_COMPANY = 'PLC'
    PRIVATE_COMPANY_LIMITED = 'LTD'
    LIMITED_LIABILITY_PARTNERSHIP = 'LLP'
    COMPANY_TYPE_CHOICES = (
        (PUBLIC_LIMITED_COMPANY, 'Public limited company'),
        (PRIVATE_COMPANY_LIMITED, 'Private company limited by shares'),
        (LIMITED_LIABILITY_PARTNERSHIP, 'Limited liability partnership'),
    )

    # DATABASE FIELDS
    name = models.CharField('name', max_length=30)
    vat_identification_number = models.CharField('VAT', max_length=20)
    company_type = models.CharField('type', max_length=3, choices=COMPANY_TYPE_CHOICES)

    # MANAGERS
    objects = models.Manager()
    limited_companies = LimitedCompanyManager()

    # META CLASS
    class Meta:
        verbose_name = 'company'
        verbose_name_plural = 'companies'

    # TO STRING METHOD
    def __str__(self):
        return self.name

    # SAVE METHOD
    def save(self, *args, **kwargs):
        do_something()
        super().save(*args, **kwargs)  # Call the "real" save() method.
        do_something_else()

    # ABSOLUTE URL METHOD
    def get_absolute_url(self):
        return reverse('company_details', kwargs={'pk': self.id})

    # OTHER METHODS
    def process_invoices(self):
        do_something()
```


<h2 id="reverse-relationships">反向关系</h2>


### related\_name

ForeignKey 的 related\_name 可以为反向关系定义一个有意义的名称


经验法则: 如果你不确定`related_name`是什么， 请使用包含所定义ForeignKey的模型的复数形式.

```python
class Company:
    name = models.CharField(max_length=30)

class Employee:
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='employees')
```

上面代码意味着， Company 有一个`employees`特殊属性, 该属性将返回一个 QuerySet，其中包含与此公司相关的所有员工实例

```python
google = Company.objects.get(name='Google')
google.employees.all()
```

你也可以通过反向关系， 来更新Company的employees字段.

```python
vitor = Employee.objects.get(first_name='Vitor')
google = Company.objects.get(name='Google')
google.employees.add(vitor)
```

### related\_query\_name

这种关系也是用于查询过滤器， 比如我们要查询雇佣名为「Vitor」的所有公司:


```python
companies = Company.objects.filter(employee__first_name='Vitor')
```

如果你想自定义此关系的查询名称可以这样

```python
class Employee:
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='employees',
        related_query_name='person'
    )
```

然后这样查询

```python
companies = Company.objects.filter(person__first_name='Vitor')
```

代码要保持一致， **related\_name**是复数, **related\_query\_name**是单数.




<h2 id="blank-and-null-fields">Blank 和 Null</h2>

我在另一篇文章有讲过两者的区别 [Blank or Null](/words/django-tips-08-blank-or-null.html)，在这里我会总结一下.

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

## 进阶

模型定义是应用程序重要的一部分， 请务必使用合适的字段类型. 这里是 [Django 支持的所有字段类型](https://docs.djangoproject.com/en/dev/ref/models/fields/#field-types).

如果你对代码风格规范感兴趣， 可以读一读[Django Coding Style](https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/coding-style/). 当然也可以看一看[Flake8](http://flake8.pycqa.org/en/latest/).
