title: Django小技巧14: messages 框架
date: 2018-10-30 14:04:39
set: Django小技巧
---

![](/uploads/images/messages-framework.jpg "cover")


> 翻译整理自: [simpleisbetterthancomplex.com](https://simpleisbetterthancomplex.com/tips/2016/09/06/django-tip-14-messages-framework.html)

让用户知道应用程序发生了什么， 是个极好的用户体验。让应用程序和用户之间能够有个很好的『交流』是个不错的选择。


设想一下下面场景:

- 用户: 点击保存按钮
- 应用程序： 什么都没有发生
- 所以是否保存了数据？ 用户并不知道
- 这时一些急性子就疯狂的点击，点击，点击...

所以， 要让用户不要慌...

## 配置

默认情况下，Django 项目内置了messages框架, 如果你没有更改这些配置， 只需要跳到下一节。 如果有改动， 按照下面这样设置：

- **INSTALLED_APPS**
    - django.contrib.messages
- **MIDDLEWARE** 或者 **MIDDLEWARE_CLASSES**(老版本)
    - django.contrib.sessions.middleware.SessionMiddleware
    - django.contrib.messages.middleware.MessageMiddleware
- **TEMPLATES**
    - **context_processors**
        - django.contrib.messages.context_processors.messages

## 消息级别和标签


| Constant | Level | Tag     | Purpose |
| -------- | ----- | ------- | ------- |
| DEBUG    | 10    | debug   | 开发相关的消息 |
| INFO     | 20    | info    | 用户级别消息   |
| SUCCESS  | 25    | success | 一个操作的成功消息 |
| WARNING  | 30    | warning | 失败但非迫在眉睫的消息 |
| ERROR    | 40    | errror  | 操作未成功或发生错误 |

默认情况下， Django 只会显示 `level >= 20` (INFO)的消息， 如果显示`DEBUG`消息， 可以在设置中:

**settings.py**

```python
from django.contrib.messages import constants as message_constants
MESSAGE_LEVEL = message_constants.DEBUG
```

为了避免遇到导入循环， 可以直接设置 level.

```python
MESSAGE_LEVEL = 10  # DEBUG
```

## 使用

在视图里面必要的地方添加， 触发消息的逻辑， 在模板里面添加显示的代码， 就可以使用消息啦

**views.py**

```python
from django.contrib import messages

@login_required
def password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password was updated successfully!')  # <-
            return redirect('settings:password')
        else:
            messages.warning(request, 'Please correct the error below.')  # <-
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'profiles/change_password.html', {'form': form})
```

**然后template中**

```django
{% if messages %}
  <ul class="messages">
    {% for message in messages %}
      <li class="{{ message.tags }}">{{ message }}</li>
    {% endfor %}
  </ul>
{% endif %}
```

如果添加成功了， 则输出的 html 应该是这样呢, 可以看到实际上标签应该和你的用户美化messsage的 css 对应。


```html
<ul class="messages">
  <li class="success">Your password was updated successfully!</li>
</ul>
```

你可以对 message， 添加额外的标签:


```python
messages.success(request, 'Your password was updated successfully!', extra_tags='alert')
```

输出html 为:

```html
<ul class="messages">
  <li class="success alert">Your password was updated successfully!</li>
</ul>
```


内置方法介绍:

```python
messages.debug(request, 'Total records updated {0}'.format(count))
messages.info(request, 'Improve your profile today!')
messages.success(request, 'Your password was updated successfully!')
messages.warning(request, 'Please correct the error below.')
messages.error(request, 'An unexpected error occured.')

# Or...

messages.add_message(request, messages.DEBUG, 'Total records updated {0}'.format(count))
messages.add_message(request, messages.INFO, 'Improve your profile today!')

# Useful to define custom levels:
CRITICAL = 50
messages.add_message(request, CRITICAL, 'A very serious error ocurred.')
```


## 和Bootstrap结合代码片段


- **messages.html**

```django
{% for message in messages %}
  <div class="alert {{ message.tags }} alert-dismissible" role="alert">
    <button type="button" class="close" data-dismiss="alert" aria-label="Close">
      <span aria-hidden="true">&times;</span>
    </button>
    {{ message }}
  </div>
{% endfor %}
```

- **settings.py**

Bootstrap 中定义了如`alert-info`或者`alert-success`等`alert-*`的组件css. 所以我们需要更改下默认的 tags.

```python
from django.contrib.messages import constants as messages

MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}
```

- **base.html**

然后把`messages.html`添加到需要显示的地方:


```django
<!doctype html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Simple is Better Than Complex</title>
  </head>
  <body>
    {% include 'partials/header.html' %}
    <main>
      <div class="container">
        {% include 'partials/messages.html' %}
        {% block content %}
        {% endblock %}
      </div>
    </main>
    {% include 'partials/footer.html' %}
  </body>
</html>
```


> 阅读更多关于messages框架的文档. [Django Documentation](https://docs.djangoproject.com/en/dev/ref/contrib/messages/)
