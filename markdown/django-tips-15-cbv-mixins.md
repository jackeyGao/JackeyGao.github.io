title: Django小技巧15: 使用基于类视图的Mixins
date: 2018-11-05 11:04:39
set: Django小技巧
---

![](/uploads/images/cbv-mixins.jpg "cover")


> 翻译整理自: [simpleisbetterthancomplex.com](https://simpleisbetterthancomplex.com/tips/2016/09/27/django-tip-15-cbv-mixins.html)

今天讲述三点关于 Mixins 使用的一些规范:


- Django 提供的View 保持在继承的最右边.
- Mixins 在基本视图的左侧
- Mixins 应该继承Python的内置对象类型(object).

下面举例说明规则

```python
class FormMessageMixin(object):
    @property
    def form_valid_message(self):
        return NotImplemented

    form_invalid_message = 'Please correct the errors below.'

    def form_valid(self, form):
        messages.success(self.request, self.form_valid_message)
        return super(FormMessageMixin, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, self.form_invalid_message)
        return super(FormMessageMixin, self).form_invalid(form)


class DocumentCreateView(FormMessageMixin, CreateView):
    model = Document
    fields = ('name', 'file')
    success_url = reverse_lazy('documents')
    form_valid_message = 'The document was successfully created!'
```


依类似的方式， 你可以在UpdateView中， 重用相同的FormMessageMixin, 并覆盖默认的`form_invalid_message`方法.

```python
class DocumentUpdateView(FormMessageMixin, UpdateView):
    model = Document
    fields = ('name', )
    success_url = reverse_lazy('documents')
    form_valid_message = 'The document was successfully updated!'
    form_invalid_message = 'There are some errors in the form below.'
```


Django 1.9开始， 内置的LoginRequiredMixin和UserPassesTestMixin. 如果你要在视图中使用它们， 它们始终位于最左侧:


```python:Mixins在左,View在后
class DocumentUpdateView(LoginRequiredMixin, FormMessageMixin, UpdateView):
    model = Document
    fields = ('name', )
    success_url = reverse_lazy('documents')
    form_valid_message = 'The document was successfully updated!'
```


