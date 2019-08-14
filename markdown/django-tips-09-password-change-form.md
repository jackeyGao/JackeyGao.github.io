title: Django小技巧09: 创建修改密码视图
date: 2018-10-26 12:50:51
set: Django小技巧
---

![](/uploads/images/password-change-form.jpg "cover")


> 翻译整理自: [simpleisbetterthancomplex.com](https://simpleisbetterthancomplex.com/tips/2016/08/04/django-tip-9-password-change-form.html)

本篇讲述如何使用内置的`PasswordChangeForm`快速创建更改密码视图.


就此而言， 使用函数式视图更容易实现。 因为`PasswordChangeForm`不从`ModelForm`继承。并且其构造函数使用`user`参数.

以下实例，用于更改经过认证过后的用户密码的功能代码:

- **views.py**

```python
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {
        'form': form
    })
```

`message.success()`和`message.error`是可选的， 但最好让用户知道应用程序中他们应该知道的状态。

需要注意一点是, 保存表单后要调用`update_session_auth_hash()`， 否则身份验证会话将会失效，用户必须重新登录.


- **urls.py**

```python
from django.conf.urls import url
from myproject.accounts import views

urlpatterns = [
    url(r'^password/$', views.change_password, name='change_password'),
]
```

- **change_password.html**

```django
<form method="post">
  {% csrf_token %}
  {{ form }}
  <button type="submit">Save changes</button>
</form>
```
