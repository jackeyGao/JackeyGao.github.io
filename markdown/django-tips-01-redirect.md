title: Django小技巧01: redirect
date: 2018-10-25 11:52:23
set: Django小技巧
---

![redirect](/uploads/images/redirect.jpeg "cover")


> 翻译整理自: [simpleisbetterthancomplex.com](https://simpleisbetterthancomplex.com/tips/2016/05/05/django-tip-1-redirect.html)

```python
from django.shortcuts import redirect
```

`redirect`函数会返回一个`HttpResponseRedirect`类，比起`HttpResponseRedirect`类我更喜欢使用更简洁的`redirect`. 它会使我的代码保持一致。


推荐使用 redirect 的理由是， 您可以指定不同类型的参数(model, url, endpoint)，指定 endpoint 的时候还可以直接指定URL， 不用再用`django.urlresolvers.reverse`来解析一遍了， 简洁了作用域环境.


下面我们来看看实例:

- 一个模型实例, 这将自动调用模型的`get_absolute_url()`方法;

```python
from django.shortcuts import redirect
from simple_blog.models import Post

def post_view(request, post_id):
    post = Post.objects.get(pk=post_id)
    return redirect(post)
    # equivalent to: return HttpResponseRedirect(post.get_absolute_url())
```

- 反解析endpoint URL 名称(接受视图 endpoint 参数)

```python
from django.shortcuts import redirect
from simple_blog.models import Post

def post_view(request, post_id):
    return redirect('post_details', id=post_id)
    # equivalent to: return HttpResponseRedirect(reverse('post_details', args=(post_id, )))
```

- 原始URL (aboluste 或者 relative)

```python
from django.shortcuts import redirect

def relative_url_view(request):
    return redirect('/posts/archive/')
    # equivalent to: return HttpResponseRedirect('/posts/archive/')

def absolute_url_view(request):
    return redirect('https://simpleblog.com/posts/archive/')
    # equivalent to: return HttpResponseRedirect('https://simpleblog.com/posts/archive/')
```


> 阅读更多关于redirect的文档. [Django Documentation](https://docs.djangoproject.com/en/dev/topics/http/shortcuts/#redirect)
