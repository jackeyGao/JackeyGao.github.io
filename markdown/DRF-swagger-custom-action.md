title: DRF Swagger自定义的action文档参数实现
date: 2018-07-04 16:22:11
---

![Swagger](/uploads/images/swagger-logo-horizontal.jpeg "cover")


这里不讲 [DRF(django rest framework)](https://github.com/encode/django-rest-framework) 和 [DRS(django rest swagger)](https://github.com/marcgibbons/django-rest-swagger) 如何结合使用, 在以上两个项目文档中都有相关文档。

在安装完毕后， Swagger 可以自动通过我们锁定一的 serializer 来自动生成各个方法(GET, POST, PUT, DELETE)的`coreapi.link`(是一套 REST Docuemnt 描述工具)， 这样后在Swagger上就可以根据相关的 Link 识别出所需的参数(Query或者Form)了。

但大多数我们往往需要根据特定的需求， 做一些自定义的接口， 比如使用的 `api_view` 装饰器定义的函数式视图， 或者使用DRF 中的 `action` 装饰器定义的自定义接口（在一些较早的DRF版本中为`list_route`和`detail_route`）。 那么这种情况下， 一些query和定义的 Form 不能直接在 swagger 中很好的展示出来，所以文档性描述接口语言， 在这个时候很是需要。

下面我们对一个接口进行改造， 改造前

**form**

```python
from django import forms


class RegisterForm(forms.Form):
    name = forms.CharField(label="name", required=True)
```


**API VIEW**

```python
@api_view(["GET", "POST"])
def register(request):
    if request.method == 'GET':
        form = RegisterForm(request.GET)
    else:
        form = RegisterForm(request.data)
    
    if not form.is_valid():
        raise_as_form(form)

    ip = request.META["REMOTE_HOST"]
    REGISTER_NODE_CACHE[ip] = form.data["name"]
    node = Node.objects.filter(ip=ip).first()

    if not node:
        raise ParseError("%s 没有创建节点" % ip)
    
    jobs = Job.objects.filter(src=node)

    serializer = JobSerializer(jobs, many=True)

    return Response(serializer.data)
```


默认情况下， swagger 不是显示出来这个接口会接受 `name` 字段.

DRF 的 schema 是控制接口参数架构的组件， 我们基于默认的 AutoSchema 重写一个新的 Schama.

主要逻辑为， 当为函数式视图或者为view 的 action的 endpoint 则通过 yaml 格式的文档描述，其他则通过默认的行为获取接口 link。 


```python
# -*- coding: utf-8 -*-
import six, yaml

if six.PY3:
    from urllib.parse import urljoin
else:
    from urlparse import urljoin

from rest_framework.compat import coreapi
from rest_framework.schemas import SchemaGenerator
from rest_framework_swagger import renderers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import exceptions
from rest_framework.permissions import AllowAny
from rest_framework.schemas.generators import is_custom_action
from rest_framework.schemas.inspectors import AutoSchema


class CustomViewSchema(AutoSchema):

    def get_link(self, path, method, base_url):
        """
        __doc__ in yaml format, eg:
        desc: the desc of this api.
        parameters:
        - name: mobile
          desc: the mobile number
          type: string
          required: true
          location: query
        - name: promotion
          desc: the activity id
          type: int
          required: true
          location: form
        """
        if hasattr(self.view, 'action'):
            # Viewsets have explicitly named actions.
            action = self.view.action
        else:
            action = ''

        if not is_custom_action(action):
            # print(path, 'is api view')
            return super(CustomViewSchema, self).get_link(path, method, base_url)
            
        fields = self.get_path_fields(path, method)

        yaml_doc = None
        if self.view and self.view.__doc__:
            try:
                yaml_doc = yaml.load(self.view.__doc__)
            except:
                yaml_doc = None
        
        # print yaml_doc
        if yaml_doc and 'desc' in yaml_doc:
            desc = yaml_doc.get('desc', '')
            _method_desc = desc
            params = yaml_doc.get('parameters', [])
            for i in params:
                _name = i.get('name')
                _desc = i.get('desc')
                _required = i.get('required', True)
                _type = i.get('type', 'string')
                _location = i.get('location', 'query')
                f = coreapi.Field(
                    name=_name,
                    location=_location,
                    required=_required,
                    description=_desc,
                    type=_type
                )
                fields.append(f)
        else:
            _method_desc = self.view.__doc__ if self.view and self.view.__doc__ else ''
            fields += self.get_serializer_fields(path, method)
        fields += self.get_pagination_fields(path, method)
        fields += self.get_filter_fields(path, method)

        if fields and any([field.location in ('form', 'body') for field in fields]):
            encoding = self.get_encoding(path, method)
        else:
            encoding = None

        if base_url and path.startswith('/'):
            path = path[1:]

        return coreapi.Link(
            url=urljoin(base_url, path),
            action=method.lower(),
            encoding=encoding,
            fields=fields,
            description=_method_desc
        )
```


然后通过 schama 装饰器对 register 视图覆盖自定义的 AutoSchema 为 CustomViewSchema .

并加上 yaml 描述.


```python
@api_view(["GET", "POST"])
@schema(CustomViewSchema())
def register(request):
    """
    desc: 注册 agent 接口
    parameters:
    - name: name
      desc: The agent host name
      type: string
      required: true
      location: form
    """
    if request.method == 'GET':
        form = RegisterForm(request.GET)
    else:
        form = RegisterForm(request.data)
    
    if not form.is_valid():
        raise_as_form(form)

    ip = request.META["REMOTE_HOST"]
    REGISTER_NODE_CACHE[ip] = form.data["name"]
    node = Node.objects.filter(ip=ip).first()

    if not node:
        raise ParseError("%s 没有创建节点" % ip)
    
    jobs = Job.objects.filter(src=node)

    serializer = JobSerializer(jobs, many=True)

    return Response(serializer.data)
```



如果是基于 view 的 action 需要在 view 上定义 schema 属性.

```python
class XXXXXXViewSet(viewsets.ModelViewSet):
    schema = CustomViewSchema()

    @action(methods=['post'], detail=True, url_path='set-xy')
    def set_xy(self, request, pk=None):
        """
        desc: Set Node x y position.
        parameters:
        - name: x
          desc: The position of x.
          type: float
          required: true
          location: form
        - name: y
          desc: The position of y.
          type: float
          required: true
          location: form
        """
        obj = self.get_object()
        form = SetXYForm(request.data)

        if not form.is_valid():
            raise_as_form(form)

        ...
```

这时候， swagger UI 上执行的时候， 就可以显示出来参数的表单了.
