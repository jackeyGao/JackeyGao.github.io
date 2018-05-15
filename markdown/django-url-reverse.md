title: Django url 反解析
date: 2015-09-30 14:07:20
categories: 
- Python
- Django
tags:
- Python
- Django
---

Django 是个python中web-framework
MTV框架能够快速的开发网站, 刚开始学习django时候， 对于模版里面经常根据自己项目的`urls`来手写链接. 
虽然这种方法是可行的， 但是不是规范的。 
为什么呢？
最近公司要做一个django改造， 由于改造需求的原因， 项目urls统一加上`项目名字`
urls.py 中很简单， 在url前面加上就行. 但是很多的模版中的url都要改掉. 这就增加了改造的复杂度。
通过此次改造我发现
其实django中有一种很好的机制, 来通过urls中的viewname 来反解析url生成url.

他们分别是: `django.core.urlresolvers.reverse` 和 `templatetags.url`


## django.core.urlresolvers.reverse

这个函数主要用在于python代码中， 详情请看下面案例

`urls.py`这里是一个对象详细页面, 需要两个参数.
`models.py`中要通过`viewname` detail 来生成url.

### urls.py

```python
urlpatterns = [
    ...
    url(r'^step/(?P<label>.*)/(?P<name>.*)$', step, name="detail"),
    ...
]
```

### models.py

```python
class Step(models.Model):
    ......
    ......

    def get_absolute_url(self):
        return reverse('detail', kwargs={
            'label': self.label,
            'name': self.name}
        )

    def label_name(self):
        return self.label.name

    def __unicode__(self):
        return unicode(self.name)

    def __str__(self):
        return self.name

```


## templatetags.url

这里还使用上面的urls.py 中的detail举例, 在模版中生成url

### base.html

```html
{% url "detail" step.label.name step.name %}
```


