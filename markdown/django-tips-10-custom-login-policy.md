title: Django小技巧10: 自定义认证策略
date: 2018-10-26 13:30:12
set: Django小技巧
---

![](/uploads/images/authentication-form-custom-login-policy.jpeg "cover")


> 翻译整理自: [simpleisbetterthancomplex.com](https://simpleisbetterthancomplex.com/tips/2016/08/12/django-tip-10-authentication-form-custom-login-policy.html)

Django 内置了一套功能极全的认证系统，而且可以很容易的进行自定义， 本章的内容就是自定义认证策略。


对于内置的login视图，Django 使用`django.contrib.auth.forms.AuthenticationForm`来处理身份验证过程。 这个认证检查了基本的`username`, `password`和`is_active`标识.

Django 可以通过`AuthenticationForm`的`confirm_login_allowed(user)`方法， 轻松添加自定义认证.

假设你想通过双重的电子邮件认证， 只有用户点击确认邮件后才可以登录，那么你可以这样做:

- **forms.py**

```python
from django import forms
from django.contrib.auth.forms import AuthenticationForm

class CustomAuthenticationForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        if not user.is_active or not user.is_validated:
            raise forms.ValidationError('There was a problem with your login.', code='invalid_login')
```

- **urls.py**

```python
from django.conf.urls import url
from django.contrib.auth import views as auth_views

from .forms import CustomAuthenticationForm

urlpatterns = [
    url(r'^login/$', auth_views.login, {'template_name': 'core/login.html',
        'authentication_form': CustomAuthenticationForm}, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    ...
]
```

很简单， 只需覆盖`confirm_login_allowed`方法,并在 urlconf 替换新的表单`CustomAuthenticationForm`即可。你可以在`confirm_login_allowed`添加任何的代码策略， 需要注意的是， 如果认证失败仅能抛出`ValidationError`才可以正常工作.


