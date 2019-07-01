title: Django小技巧18: ugettext和ugettext_lazy的区别
date: 2018-11-05 15:20:39
set: Django小技巧
---

![redirect](/uploads/images/translations.jpg "cover")

> 翻译整理自: [simpleisbetterthancomplex.com](https://simpleisbetterthancomplex.com/tips/2016/10/17/django-tip-18-translations.html)

Django API 提供了几个有用的模块来帮助你翻译你的应用程序. 它们都在`django.utils.translation`中使用，大多数情况下， 我们会使用到ugettext()和ugettext\_lazy().

「u」前缀代表「unicode」, 因为大多数情况下，我们经常使用 Unicode,  所以使用ugettext()代替gettext(), 使用ugettext\_lazy()代替gettext\_lazy().

顾名思义, "lazy"该函数是对翻译字符串的引用， 而不是实际翻译的文本. 因此在访问值的时候会进行转换， 而不是调用的时候.

注意这个特性，Django 启动的时候一些特定的代码只执行一次， 比如在**models**, **forms**和**model forms**.

那么， 我们假设在模型定义的时候使用ugettext(), 而不是ugettext\_lazy()会怎么样?


- 1. Django 启动, 默认语言是英文.
- 2. Django 选择了英文版的field labels
- 3. 用户将网站语言改为简体中文.
- 4. **field labels**依然是英文显示. 


> %warning 因为models的字段定义仅仅被执行一次，并且在执行定义代码的时候语言不是简体中文(一般是英文).

要避免这种行为，要必须正确的使用ugettext()和ugettext\_lazy()

下面总结了， 在合适的地方使用合适的函数:


- **ugettext_lazy():**
    - models.py (fields, verbose\_name, help\_text, methods short\_description);
    - forms.py (labels, help\_text, empty\_label);
    - apps.py (verbose\_name).
- **ugettext():**
    - views.py
    - 其他类似于在请求过程中调用的代码

