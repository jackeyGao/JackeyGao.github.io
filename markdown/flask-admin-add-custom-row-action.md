title: Flask-Admin 增加自定义Action
date: 2017-05-12 12:50:22
---

默认情况下, Flask Admin提供了两个Row Action, 即delete和edit. 但是大多数情况下, 这些并不能满足有其他快捷操作需求, 好在Flask Admin提供增加这种按钮的接口.

## `UserView.py`

这是我原本的Admin ModelView实现, 很明显我没有对row actions做任务的定制.

```python
class UserView(ModelView):
    column_default_sort = ('active', False)
    column_list = ('name', 'email', 'active', 'roles')
    column_filters = ('name', 'active')
    form_create_rules = ('name', 'avatar', 'email', 'active', 'roles')
```

## 增加row action按钮

我们可以通过[`column_extra_row_actions`](https://flask-admin.readthedocs.io/en/latest/api/mod_model/#flask_admin.model.BaseModelView.column_extra_row_actions)属性增加row action. 

```python
from flask_admin.model.template import EndpointLinkRowAction

class UserView(ModelView):
    column_default_sort = ('active', False)
    column_list = ('name', 'email', 'active', 'roles')
    column_filters = ('name', 'active')
    form_create_rules = ('name', 'avatar', 'email', 'active', 'roles')

    column_extra_row_actions = [
        EndpointLinkRowAction(
            'off glyphicon glyphicon-off',
            'user.activate_user_view',
        )
    ]
```

> Flask-admin提供了row action的模版, 其中上面使用的`EndpointLinkRowAction`, 传入的是一个view(`user.activate_user_view`). 它是定义在UserView上的一个view方法(请看下面代码). 同时row action也有`LinkRowAction`类型, 它接受icon class和一个url. 另外它支持更多的类型, 请看[这里:Github](https://github.com/flask-admin/flask-admin/blob/master/flask_admin/model/template.py#L66)


## 增加对应的endpoint

在上面我们增加了一个`EndpointLinkRowAction`, 但是我们还没有定义动作具体的逻辑. 下面我们定义`user.activate_user_view`来接收这个动作的参数, 并实现相应的功能.

```python
class UserView(ModelView):
    column_default_sort = ('active', False)
    column_list = ('name', 'email', 'active', 'roles')
    column_filters = ('name', 'active')
    form_create_rules = ('name', 'avatar', 'email', 'active', 'roles')

    column_extra_row_actions = [
        EndpointLinkRowAction(
            'off glyphicon glyphicon-off',
            'user.activate_user_view',
        )
    ]

    @expose('/activate/', methods=('GET',))
    def activate_user_view(self):
        """
            Activate user model view. Only GET method is allowed.
        """
        return_url = get_redirect_target() or self.get_url('.index_view')

        id = request.args["id"]
        model = self.get_one(id)

        if model is None:
            flash(gettext('用户不存在'), 'error')
            return redirect(return_url)

        if model.active:
            flash(gettext('已经激活， 无需重复激活.'), 'warning')
            return redirect(return_url)

        model.active = True
        model.save()

        flash(gettext('已激活'), 'success')
        return redirect(return_url)
```

到此我们增加一个`快速激活用户`的方法就完成了.

![增加后的动作列表](/uploads/images/flask-admin-add-custom-row-action.jpeg)


