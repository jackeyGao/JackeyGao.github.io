title: Django小技巧07: 在模板中获取当前URL
date: 2018-10-26 11:55:23
set: Django小技巧
---

![](/uploads/images/get-url-in-template.jpg "cover")


> 翻译整理自: [simpleisbetterthancomplex.com](https://simpleisbetterthancomplex.com/tips/2016/07/20/django-tip-7-how-to-get-the-current-url-within-a-django-template.html)


确保项目配置里的`context_processors`包含`django.template.context_processors.request`.


从 Django 1.9 开始， 默认是已经配置的。

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

获取当前位置:

```django
{{ request.path }}
```

获取带有querystring的URL:

```django
{{ request.get_full_path }}
```

获取完全的绝对路径:

```django
{{ request.build_absolute_uri }}
```

## 示例表

假设， 我们的URL是: `https://jackeygao.io/search/?keyword=django`


| Method | Output |
| -------------  |:------------- |
| request.path | /search/ |
| `request.get_full_path` | search/?keyword=django |
| `request.build_absolute_uri` | https://jackeygao.io/search/?keyword=django |


## Django 1.7 或者更早的版本


### settings.py

```
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP

TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    'django.core.context_processors.request',
)
```



> 阅读更多关于Automatic DateTime Fields的文档. [Django Documentation](https://docs.djangoproject.com/en/dev/ref/models/fields/#datefield)
