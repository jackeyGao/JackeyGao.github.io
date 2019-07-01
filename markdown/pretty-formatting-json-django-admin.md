title: Django Admin输出JSON
date: 2017-03-15 12:41:12
---


Django 自带Admin后台这是Django的优势所在, 这样的话我们可以开箱即用后台功能。 有人说Django重， 可能设计就是这样， 过度的封装就是让开发者更简单的实现。 比起flask、tornado等轻量级的框架。 Django更适合做支撑系统的开发。 


当然本文不讲述Django和其他轻量级框架的优劣， 主要说一个修改Admin后台的例子。 虽然Admin可以对定义的模型表做一些基本的增删改查， 但是有时候我们需要加一些功能。 比如： 我想在change页面加入一个字段， 可以完整的显示整个实例的所有字段， 并以JSON的格式显示出来。 这样对于我在开发API的时候能更加直观， 而且我想显示的JSON是格式化之后的， 最好是加上语法高亮.


所以我用了以下代码去完成了这个需求:

```python
from django.contrib import admin
import json
import copy
from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import HtmlFormatter

from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import APIData


class APIDataAdmin(admin.ModelAdmin):
    readonly_fields = ('data_prettified',)

    def data_prettified(self, instance):
        """Function to display pretty version of our data"""
        # Convert the data to sorted, indented JSON
        data = copy.deepcopy(instance.__dict__)
        data.pop('_state')
        response = json.dumps(data, sort_keys=True, indent=2)

        # Truncate the data. Alter as needed
        response = response[:5000]

        # Get the Pygments formatter
        formatter = HtmlFormatter(style='colorful')

        # Highlight the data
        response = highlight(response, JsonLexer(), formatter)

        # Get the stylesheet
        style = "<style>" + formatter.get_style_defs() + "</style><br>"

        # Safe the output
        return mark_safe(style + response)

    data_prettified.short_description = 'data prettified'

admin.site.register(APIData, APIDataAdmin)
```

完成后的效果图
![](/uploads/images/pretty-formatting-json-django-admin.png)


