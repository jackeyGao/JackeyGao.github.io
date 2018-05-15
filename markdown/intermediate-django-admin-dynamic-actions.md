title: Django 进阶学习 - 动态actions
date: 2016-05-03 16:09:06
tags:
- Django
- Python
---

Django后台默认只有一个动作`Delete selected xxxxs`, 那么如果自定义动作该怎么办， 也很容易， 直接写个类似于这种的函数

```python
def make_published(modeladmin, request, queryset):
    queryset.update(status='p')
```

然后绑定到ModelAdmin的actions属性

`admin.py`

```python
class TriggerAdmin(admin.ModelAdmin):
    empty_value_display = u'无规则'
    list_display = ('__str__', 'id')
    search_fields = ('description',)
    list_filter = (IpFilter, 't_type')
    actions = (make_published,) #指定自定义actions
```

action在程序启动后就会正常工作， 现在我有个项目需要根据一张表（role表）来动态扩展动作， 所以这种方法没有办法扩展。 总不能在role表加一个数据就要重启django把？ 显然不能这样做， 当然django有动态生成action的方法, 那就是`admin.ModelAdmin`的`get_actions()`方法

**首先写个闭包**

根据role生成`action function`

`actions.py`

```python
from django.utils.translation import ugettext as _, ugettext_lazy
from controller.models import SwitchRole
from controller.models import ConvergeRole

def _with_role(role, switch=True):
    """闭包实现， 设置role, switch为通用变量,  返回一个action函数"""

    # 根据role类型判断字段类型
    if isinstance(role, SwitchRole):
        field_name = "switch_role"
    elif isinstance(role, ConvergeRole):
        field_name = "converge_role"
    else:
        return None

    def set_selected(modeladmin, request, queryset):
        """
        规则动作
        """
        # 根据开关选项， 来判断字段value
        kwargs = {}
        if switch:
            field_value = role.pk
        else:
            field_value = None

        kwargs[field_name] = field_value
        return queryset.update(**kwargs)

    set_selected.short_description = ugettext_lazy(u"设置规则为: %s" % role)
    set_selected.__name__ = "set_role_%s_%s" % (field_name, role.pk)
    return set_selected
```

**注意:** `set_selected.short_description`为后台管理界面actions下拉菜单显示的文本， `set_selected.__name__` 是函数的名称， 由于我们是多个，所以函数的名称一定要唯一.

**下面重写get_actions()**

`admin.py`

```python
class TriggerAdmin(admin.ModelAdmin):
    empty_value_display = u'无规则'
    list_display = ('__str__', 'id', 'ip', 't_type',
            'get_converge', 'get_switch', 'level')
    search_fields = ('description',)
    list_filter = (IpFilter, 't_type', 'converge_role', 'switch_role', 'level')

    def get_actions(self, request):
        # 设置Role动作
        fns = [ _with_role(i) for i in SwitchRole.objects.all() ]
        fns += [_with_role(i) for i in ConvergeRole.objects.all()]

        # 清空Role动作
        if SwitchRole.objects.all():
            role = _with_role(SwitchRole.objects.all()[0], switch=False)
            role.__name__ = 'remove_switch_role'
            role.short_description = ugettext_lazy(u"清空开关规则")
            fns.append(role)

        if ConvergeRole.objects.all():
            role = _with_role(ConvergeRole.objects.all()[0], switch=False)
            role.__name__ = 'remove_converge_role'
            role.short_description = ugettext_lazy(u"清空聚合规则")
            fns.append(role)

        actions = [ self.get_action(fn) for fn in fns ]
        actions = OrderedDict(
            (name, (func, name, desc))
            for func, name, desc in actions
        )
        return actions
```

这样每次刷新页面`get_actions`都会执行一遍， 做到动态actions.

!["截屏图片"](/uploads/images/intermediate-django-admin-dynamic-actions.png)


