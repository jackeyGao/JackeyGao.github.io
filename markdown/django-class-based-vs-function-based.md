title: 类视图 vs. 函数视图
date: 2018-12-12 10:31:32
---

![Coding](/uploads/images/fbv-vs-cbv.jpeg "cover")


基于类的视图(CBV)和基于函数的视图(FBV)到底有什么区别？ 有什么优缺点？ 本篇将会去探讨。 在阅读本篇之前，请记住一点「*基于类的视图不会替代基于函数的视图*」.


## 介绍 

无论是类视图还是基于函数的视图， 最终绑定到 URL Conf 的都是函数. 为什么这么说？ 函数绑定到 URL 上面很显式的证明了绑定的是函数， 这一点毋庸置疑。 但类是怎么被绑定成为函数的， 我们可以看下类的`as_view`方法.

*View.as_view()*

```python
class View:
    @classonlymethod
    def as_view(cls, **initkwargs):
        """Main entry point for a request-response process."""
        for key in initkwargs:
            # Code omitted for clarity
            # ...

        def view(request, *args, **kwargs):
            self = cls(**initkwargs)
            if hasattr(self, 'get') and not hasattr(self, 'head'):
                self.head = self.get
            self.request = request
            self.args = args
            self.kwargs = kwargs
            return self.dispatch(request, *args, **kwargs)

        # Code omitted for clarity
        # ...

        return view
```

为了方便举例， 我简短了一些代码。 你可以到 [Github](https://github.com/django/django/blob/1.10.6/django/views/generic/base.py#L46) 上阅读全部代码.

如上面代码所示， 当我们把视图绑定到 url conf 时使用的 as\_view 挂载其实返回的是一个函数.

如果我在代码里面， 显式的调用类视图必须这样做:

```python
return MyView.as_view()(request)
```

为了让代码显示更加自然， 有可读性，你可以这个函数分配给一个变量.

```python
view_function = MyView.as_view()
return view_function(request)
```

是不是很熟悉？ 这样就太像基于函数的视图了， 当然view\_function其实就是函数.

as\_view 方法是基于类的外部接口， 他返回一个视图函数. 调用后, 视图将请求传递给dispatch() 方法，该方法将根据请求的类型(**GET**, **POST**, **PUT**, etc)执行响应的方法(详情参考*django/views/generic/base.py*, dispatch 方法.) 这个是类的一大优点.

### 基于类视图例子

举例创建一个基于类的视图，分别处理不同的 HTTP Method . 如果方法为 GET 则执行 get() 方法， 如果为 POST 则执行 post() ;

*views.py*

```python
from django.views import View

class ContactView(View):
    def get(self, request):
        # Code block for GET request

    def post(self, request):
        # Code block for POST request
```


*urls.py*

```python
urlpatterns = [
    url(r'contact/$', views.ContactView.as_view(), name='contact'),
]
```

### 基于函数视图例子

实现上面的需求， 这次基于函数， 我们需要用 if 语句控制.

*views.py*

```python
def contact(request):
    if request.method == 'POST':
        # Code block for POST request
    else:
        # Code block for GET request (will also match PUT, HEAD, DELETE, etc)
```

*urls.py*

```python
urlpatterns = [
    url(r'contact/$', views.contact, name='contact'),
]
```

这些是两者的最显要的区别. 你也可以感受到基于类视图的优势. 下面， 将会介绍**基于类的通用视图(GV)**, 它又是一个不同的形式.


## 基于类的通用视图(GV)

Django 引入了基于类的通用视图， 来处理 web 常见的用例需求， 比如创建新对象，表单处理，列表视图，分页，归档视图等.

你可以在`django.views.generic`引用它们.

你可以直接使用它们来加快开发的过程，以下是可用视图的概述:


### 基础视图

- View (最基本的View)
- TemplateView
- RedirectView

### 通用展示视图

- ListView
- DetailView

### 通用编辑视图

- FormView
- CreateView
- UpdateView
- DeleteView

### 基于日期的视图

- ArchiveIndexView
- YearArchiveView
- MonthArchiveView
- WeekArchiveView
- DayArchiveView
- TodayArchiveView
- DateDetailView

你可以在Django Doc上查看[基于类的通用视图](https://docs.djangoproject.com/en/dev/ref/class-based-views/)一篇阅读更多的详细信息, 还有更多的mixins.

通用视图的实现， 使用大量的 mixins. 这一点， 仁者见仁智者见智.

可以查看[基于类的通用视图-扁平索引](https://docs.djangoproject.com/en/dev/ref/class-based-views/flattened-index/) , 来查看所有的视图的方法. 它非常实用，建议把 这个页面放到浏览器书签栏里.



## 各种观点


### #1

> 观点 「**使用所有的通用视图(GV)**」
> 此观点认为，Django 提供这些通用视图就是让减少开发的效率， 为什么不用呢？

### #2

> 观点 「**仅使用django.views.generic.View, 不用GV**」
> 此观点认为, View 就足够了， 并且 View 是真正的CBV, 而通用视图则不是真正的 CBV. View 的确没有通用视图封装那么全， 但也说明了它比通用视图灵活。 在函数视图和通用视图中间位置.


### #3

> 观点 「**除非必要， 否则避免适用视图**」
> 一般建议是从功能视图开始，这样更容易阅读和理解。并且在你需要的地方使用 CBV。一般在哪里需要用到 CBV？ 任务需要在多个视图中重用代码的地方， 这个场景下 CBV 是最好的选择。


我建议是选择第三种，正如那句话『从需求场景选择最佳的实现』 最佳的做法取决你自己, .

## 优点和缺点

有关 CBV 和 FBV 的优缺点, 仅供参考.


## Function-Based Views

<span class="green text">优点</span>

- 易于构建
- 可读性佳
- 显示代码流
- 直接用装饰器

<span class="red text">缺点</span>

- 难以扩展及复用代码
- 通过 if 条件处理HTTP方法


## Class-Based Views

<span class="green text">优点</span>

- 轻松扩展及复用代码
- 可以面向对象如mixins(多重继承)
- 单独的类方法处理 HTTP 方法
- 内置的基于类通用视图

<span class="red text">缺点</span>

- 可读性差
- 隐式代码流
- 隐式mixins及父类代码
- 装饰器的使用需要额外的导入或方法覆盖

选择哪一种都没有对错， 这一切取决于你的项目背景和需求以及对以后代码扩展性的考虑.正如我开头提到的， 基于类的视图不会取代基于函数的视图, 有些情况下基于函数视图更容易实现， 有些时候繁琐的需求变更及代码复用你选择基于类视图更好.

例如我想实现一个博客， 对首页展示博客的列表， 我只需要适用一个通用视图ListView并覆盖其 queryset 属性即可大功告成.

又假如你要实现一个复杂的请求， 如一次处理多个表单，基于函数的视图的灵活性将更好为你服务.

## 结论

我觉得如果是初学者在做线上项目，在不了解面向对象时适用函数式编程是个好的选择，无论是对于以后维护还是开发阶段，都能 hold 住。 但也别放弃学习 OOP， 并使用 CBV 的方式实现非重要项目练手。 对于没有面向对象经验的同学，函数式编程不会觉得代码很低级， 相反一些大佬依然坚持函数式编程。 FBV代码是显式的， CBV代码大多数都是隐式的。所以FBV 容易阅读， CBV 难于阅读。 

通用视图(GV)虽然封装更加具体， 但无法处理更宽泛的情况. Django 官方的建议是: 如果你难以将自己的视图实现为通用视图(重点是generic views)的子类, 那么你直接使用基于 View 的视图或功能视图， 只编写你所需的代码更更加有效.  
