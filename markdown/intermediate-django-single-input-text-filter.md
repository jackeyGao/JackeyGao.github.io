title: Django 进阶学习 - 文本框过滤
date: 2016-05-03 15:46:46
tags:
- Python
- Django
---

默认情况下django可以对列进行过滤， 但大多数是对`Relationship `列通过`list_filter` 直接指定`field name`就可以方便的进行过滤了， 但是如果实现文本框输入过滤属性， 然后通过按钮触发事件后来过滤只能通过自定义Django filter来实现

**首先自定义一个filter类**

`filters.py` 默认情况下如果没有`filters.py`需要在app目录新建此模块, 推荐命名`filters.py`, 下面这个类是通用的， 所以我们要基于模型的某个字段来定义一个Filter类，继承`SingleTextInputFilter`(还是在`filters.py`)

```python
from django.contrib.admin import ListFilter
from django.utils.translation import ugettext_lazy as _

class SingleTextInputFilter(ListFilter):
    """
    renders filter form with text input and submit button
    """
    parameter_name = None
    template = "admin/textinput_filter.html"

    def __init__(self, request, params, model, model_admin):
        super(SingleTextInputFilter, self).__init__(
            request, params, model, model_admin)
        if self.parameter_name is None:
            raise ImproperlyConfigured(
                "The list filter '%s' does not specify "
                "a 'parameter_name'." % self.__class__.__name__)

        if self.parameter_name in params:
            value = params.pop(self.parameter_name)
            self.used_parameters[self.parameter_name] = value

    def value(self):
        """
        Returns the value (in string format) provided in the request's
        query string for this filter, if any. If the value wasn't provided then
        returns None.
        """
        return self.used_parameters.get(self.parameter_name, None)

    def has_output(self):
        return True

    def expected_parameters(self):
        """
        Returns the list of parameter names that are expected from the
        request's query string and that will be used by this filter.
        """
        return [self.parameter_name]


    def choices(self, cl):
        all_choice = {
            'selected': self.value() is None,
            'query_string': cl.get_query_string({}, [self.parameter_name]),
            'display': _('All'),
        }
        return ({
            'get_query': cl.params,
            'current_value': self.value(),
            'all_choice': all_choice,
            'parameter_name': self.parameter_name
        }, )

class IpFilter(SingleTextInputFilter):
    """基于IP过滤, 继承SigleTextInputFilter"""
    title = "IP"
    parameter_name = 'ip'  #作用model的字段名
    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(ip__iexact=self.value()) ＃ 这里自定义过滤条件. self.value() 是文本框输入的值.
```


**自定义filter template**

`admin/textinput_filter.html`, 直接放到本项目的template目录即可， 千万不要放到`django`包目录下的admin template目录， 如果你了解django 模版检索的过程优先级， 你应该知道我说的意思. 这里我放到`$MYAPP/templates/admin/textinput_filter.html`位置

```html
<h3>{% blocktrans with filter_title=title %} By {{ filter_title }} {% endblocktrans %}</h3>

{#i for item, to be short in names#}
{% with choices.0 as i %}
<ul>
    <li>
        <form method="get">
            <input type="search" name="{{ i.parameter_name }}" value="{{ i.current_value|default_if_none:"" }}"/>

            {#create hidden inputs to preserve values from other filters and search field#}
            {% for k, v in i.get_query.items %}
                {% if not k == i.parameter_name %}
                    <input type="hidden" name="{{ k }}" value="{{ v }}">
                {% endif %}
            {% endfor %}
            <input type="submit" value="{% trans 'apply' %}">
        </form>
    </li>

    {#show "All" link to reset current filter#}
    <li{% if i.all_choice.selected %} class="selected"{% endif %}>
        <a href="{{ i.all_choice.query_string|iriencode }}">
            {{ i.all_choice.display }}
        </a>
    </li>
</ul>
{% endwith %}
```

**最后配置admin.py**

`admin.py`

```python
from controller.filters import IpFilter

class TriggerAdmin(admin.ModelAdmin):
    empty_value_display = u'无规则'
    list_display = ('__str__', 'id', 'ip', 't_type',
            'get_converge', 'get_switch', 'level')
    search_fields = ('description',)
    list_filter = (IpFilter, 't_type', 'converge_role', 'switch_role', 'level') # 直接把IpFilter类写进去
```

**配置完成**




