title: 探索Django utils
date: 2018-11-16 14:36:42
set: 好玩的Django
---

Django utils 提供了很多实用的功能.


![](/uploads/images/exploring-utils.jpeg "cover")


## Crypto

> Module: **django.utils.crypto**

**get\_random\_string**

获取随机字符串函数， 默认是返回长度为12的随机字符串。 可以通过参数传递长度.


```python
from django.utils.crypto import get_random_string

get_random_string()
```

```python:output
'5QxAxqyhsyJM'
```


你可以传递参数， 获取指定长度的字符串


```python
get_random_string(50)
```

```python:output
'lrWYnyxhnXpwmjHDzmdgTFaIi1j73cKD5fPDOPwuVBmmKxITYF'
```

也可以指定字符串的选值范围

```python
get_random_string(12, '0123456789')
```

```python:output
'805379737758'
```

## Dates

> Module: **django.utils.dates**

常用日期的集合， 日期的人性化显示.


**WEEKDAYS**

```python
from django.utils.dates import WEEKDAYS
```

```python
WEEKDAYS = {
    0: _('Monday'), 1: _('Tuesday'), 2: _('Wednesday'), 3: _('Thursday'), 4: _('Friday'),
    5: _('Saturday'), 6: _('Sunday')
}
```

**WEEKDAYS\_ABBR**

```python
from django.utils.dates import WEEKDAYS_ABBR
```

```python
WEEKDAYS_ABBR = {
    0: _('Mon'), 1: _('Tue'), 2: _('Wed'), 3: _('Thu'), 4: _('Fri'),
    5: _('Sat'), 6: _('Sun')
}
```

**MONTHS**

```python
from django.utils.dates import MONTHS
```

```python
MONTHS = {
    1: _('January'), 2: _('February'), 3: _('March'), 4: _('April'), 5: _('May'), 6: _('June'),
    7: _('July'), 8: _('August'), 9: _('September'), 10: _('October'), 11: _('November'),
    12: _('December')
}
```

## DateFormat

> Module: **django.utils.dateformat**

一个很棒的日期格式化模块


**format**

```python
from django.utils.dateformat import format
from django.utils import timezone

now = timezone.now()    # datetime.datetime(2018, 11, 16, 6, 48, 41, 351928, tzinfo=<UTC>)
format(now, 'd M Y')
```

```python:output
u'16 Nov 2018'
```

**日期和时间一起**

```python
format(now, 'd/m/Y H:i')
```

```python:output
u'16/11/2018 06:48'
```

## DateParse

> Module: **django.utils.dateparse**

将格式化后的字符串转为 date/time/datetime 对象. 如果字符串格式正确， 但表示无效时间将会返回 **None**.


**parse\_date**


```python
from django.utils.dateparse import parse_date

parse_date('2018-11-16')
```

```python:output
datetime.date(2018, 11, 16)
```

**parse\_time**

```python
from django.utils.dateparse import parse_time

parse_time('14:54:02')
```

```python:output
datetime.time(14, 54, 2)
```

**parse\_datetime**


```python
from django.utils.dateparse import parse_datetime

parse_datetime('2018-11-16 14:54:02')
```

```python:output
datetime.datetime(2018, 11, 16, 14, 54, 2)
```

## HTML

> Module: **django.utils.html**


**urlize**

将文本中的网址转换为\<a\>标签

```python
from django.utils.html import urlize

urlize('You guys should visit this website www.google.com')
print urlize('Please visit:  https://jackeygao.io')
```

```python:output
'You guys should visit this website <a href="http://www.google.com">www.google.com</a>'
Please visit:  <a href="https://jackeygao.io">https://jackeygao.io</a>
```

他也适用于email地址

```python
urlize('Send me a message to gaojunqi@outlook.com')
```

```python:output
'Send me a message to <a href="mailto:gaojunqi@outlook.com">gaojunqi@outlook.com</a>'
```

你也可以修剪链接显示部分长度, 不足处以'...'替代

```python
urlize('Please visit https://jackeygao.io/words/django-exploring-utils.html', 24)
```

```python:output
Please visit <a href="https://jackeygao.io/words/django-exploring-utils.html">https://jackeygao.io/...</a>
```

**escape**

对html 特殊字符编码

```python
from django.utils.html import escape

escape("<strong style='font-size: 12px'>escaped html</strong>")
```

```python:output
'&lt;strong style=&#39;font-size: 12px&#39;&gt;escaped html&lt;/strong&gt;'
```

这将导致已转义的字符串再次被转义

```python
escaped_html = escape("<strong>escaped html</strong>")
# '&lt;strong&gt;escaped html&lt;/strong&gt;'

escape(escaped_html)
# '&amp;lt;strong&amp;gt;escaped html&amp;lt;/strong&amp;gt;'
```

如果不想这样, 请改用**conditional\_escape()**

**conditional_escape**

```python
escaped_html = conditional_escape("<strong>escaped html</strong>")
# '&lt;strong&gt;escaped html&lt;/strong&gt;'

conditional_escape(escaped_html)
# '&lt;strong&gt;escaped html&lt;/strong&gt;'
```

**format\_html**

此函数类似格式化字符串(str.format()), 因为安全的原因推荐使用**format\_html**.


```python
from django.utils.html import format_html

format_html('<div class="alert {}">{}</>', 'warning', 'Watch out!')
```

```python:output
'<div class="alert warning">Watch out!</>'
```

安全的格式化 HTML 代码.

```python
format_html('<div class="alert {}">{}</>', '<script>alert(1);</script>', 'Watch out!')
```

```python:output
'<div class="alert &lt;script&gt;alert(1);&lt;/script&gt;">Watch out!</>'
```

**format\_html\_join**

适用于快速用相同的方式格式化一组列表

```python
format_html_join('\n', '<p>{}</p>', ['a', 'b', 'c'])
```

```python:output
<p>a</p>\n<p>b</p>\n<p>c</p>
```

另外一个例子

```python
data = [
    ['success', 'Success message'],
    ['warning', 'Watch out!'],
    ['danger', 'Danger!!'],
]

format_html_join('\n', '<div class="alert {0}">{1}</div>', data)
```

```python:output
<div class="alert success">Success message</div>\n
<div class="alert warning">Watch out!</div>\n
<div class="alert danger">Danger!!</div>
```

和表格一起使用, 当然也可以和ul li一起使用.

```python
format_html_join('\n', '<tr><td>{0}</td><td>{1}</td></tr>', ((u.first_name, u.last_name)
                                                            for u in users))
```

```python:output
<tr><td>Vitor</td><td>Freitas</td></tr>\n
<tr><td>John</td><td>Duo</td></tr>\n
<tr><td>Peter</td><td>Croke</td></tr>\n
<tr><td>Elektra</td><td>Moore</td></tr>
```

**linebreaks**

快速将**\n**转换为\<br /\>


```python
from django.utils.html import linebreaks

linebreaks('convert\ninto html paragraphs\ntest')
```

```python:output
<p>convert<br />into html paragraphs<br />test</p>
```

就是这样， 我希望你也能找到一些有趣的函数， 欢迎通过留言推荐.


