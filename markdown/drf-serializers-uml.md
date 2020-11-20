title: DRF Serializer UML
date: 2020-11-20 14:53:11
---

上周要求对当前项目产出数据结构 UML 图及流程图， 为了完成流程图我花了一天的时间， 几近抓狂。 做完准备画数据结构关系图时， 心态炸裂。 于是上网搜索 Django 自动生成 Models UML  图的项目。

没想到还真有， 那就是著名的 [django-extensions]。

具体的生成 Models Graph 的方式， 请参考 [Graph Models](https://django-extensions.readthedocs.io/en/latest/graph_models.html).

由于项目 Models 不能完全提现项目的全部数据结构， 要求对 Django rest framework 的 Serializer 也通过图描述出来。 我在网上并没有找到对 Serializer 进行构图的工具。

于是查看 [django-extensions] graph_models 源码, 做了一个关于生成 Serializer UML 构图的工具。 

思路基本上是通过 Serializer 入口， 解析每一个字段类型， 然后通过模板生成 [dot] 文件。 然后通过 [Graphviz] 工具提供的 dot 命令进行生成 png 图形。

## 解析代码

```python
import os
from django.core.management.base import BaseCommand, CommandError
from django.template import Template, Context, loader
from rest_framework.serializers import Serializer, Field, ListField, ListSerializer, ChoiceField
from xxxxx.xxxxx.describe import DescribeSerializer  # Serializer 入口文件


serializers = {}

def name(serializer):
    try:
        return str(serializer.__name__)
    except:
        return str(serializer.__class__.__name__)

def render(serializer, label=None):
    if not label:
        label = getattr(serializer, '__doc__', '')

    if isinstance(serializer, ChoiceField):
        data = { 'name': label, 'label': 'Enum' }
        fields = []
        for k, v in serializer.choices.items():
            fields.append({'key': k, 'ref': 'field', 'type': type(v).__name__, 'label': v})
        
        data["fields"] = fields

        serializers[label] = data
        return 

    data = { 'name': name(serializer), 'label': label }
    fields = []

    ref_fields = []

    if hasattr(serializer, 'Meta'):
        ref_fields  = getattr(serializer.Meta, 'ref_fields', [])
        
    for k, field in serializer._declared_fields.items():
        ref_fields.append({
            'key': k, 'field': field
        })

    for item in ref_fields:
        k, field = item["key"], item["field"]
        if isinstance(field, Serializer):
            render(field)
            fields.append({'key': k, 'ref': 'ref', 'type': name(field), 'label': field.label})
            continue
        if isinstance(field, ListField):
            render(field.child)
            fields.append({'key': k, 'ref': 'ref-[]', 'type': name(field.child), 'list': name(field), 'label': field.label})
            continue
        if isinstance(field, ListSerializer):
            render(field.child)
            fields.append({'key': k, 'ref': 'ref-[]', 'type': name(field.child), 'list': name(field), 'label': field.label})
            continue
        if isinstance(field, ChoiceField):
            label = f'{k.title()}Choices'
            render(field, label)
            fields.append({'key': k, 'ref': 'ref', 'type': label, 'label': name(field)})
            continue
        else:
            fields.append({'key': k, 'ref': 'field', 'type': name(field), 'label': field.label})

    data["fields"] = fields

    serializers[name(serializer)] = data
```

## 渲染 dot 文件

模板文件 (dot/serializers.dot), 可以放到 templates ， 通过 loader.get_template 获取, 也可以读取单独的文件内容， 然后通过 Template 类实例化.

```
// filename: myapp/tempaltes/dot/serializers.dot
digraph model_graph {
  // Dotfile by Django-Extensions graph_models
  // Created: 2020-11-17 13:03
  // Cli Options: --dot -o myapp_models.dot console

  fontname = "Helvetica"
  fontsize = 8
  splines  = true

  node [
    fontname = "Helvetica"
    fontsize = 8
    shape = "plaintext"
  ]

  edge [
    fontname = "Helvetica"
    fontsize = 8
  ]

  // Labels
  {% for serializer_name, serializer in serializers.items %}
  console_serializer_{{ serializer_name }} [label=<
    <TABLE BGCOLOR="white" BORDER="1" CELLBORDER="0" CELLSPACING="0">
    <TR><TD COLSPAN="3" CELLPADDING="5" ALIGN="CENTER" BGCOLOR="#1b563f">
    <FONT FACE="Helvetica Bold" COLOR="white" POINT-SIZE="10"><B>
    {{ serializer_name }} {{ serializer.label }}
    </B></FONT></TD></TR>
    {% for field in serializer.fields %}
    <TR><TD ALIGN="LEFT" BORDER="0">
    <FONT FACE="Helvetica" COLOR="#7B7B7B"><B>{{ field.key }}</B></FONT>
    </TD><TD ALIGN="LEFT">
    <FONT FACE="Helvetica" COLOR="#7B7B7B">{{ field.type }}</FONT>
    </TD><TD ALIGN="LEFT">
    <FONT FACE="Helvetica" COLOR="#7B7B7B">{{ field.label }}</FONT>
    </TD></TR>
    {% endfor %}
    </TABLE>
    >]
  {% endfor %}
  // Relations
  {% for serializer_name, serializer in serializers.items %}
  {% for field in serializer.fields %}
  {% if field.ref == 'ref' %}
  console_serializer_{{ serializer_name }} -> console_serializer_{{ field.type }}
  [label=" {{ field.key }} ({{ serializer_name }})"] [arrowhead=none, arrowtail=dot, dir=both];
  {% endif %}
  {% if field.ref == 'ref-[]' %}
  console_serializer_{{ serializer_name }} -> console_serializer_{{ field.type }}
  [label=" {{ field.key }} ({{ serializer_name }} [])"] [arrowhead=none, arrowtail=dot, dir=both];
  {% endif %}
  {% endfor %}
  {% endfor %}

}
```

```python
import os

if __name__ == '__main__':
    render(DescribeSerializer) # 传入入口文件， 您可以指定您的入口文件， 当然您也可以改造上面的脚本让它支持多个入口.

    t = loader.get_template('dot/serializers.dot')

    output_file = './doc/dot/serializers.dot'  # 输出文件.

    if not os.path.exists(os.path.dirname(output_file)):
        raise CommandError('./doc/dot 不存在， 请创建.')

    with open(output_file, 'w') as f:
        f.write(t.render({'serializers': serializers}))
```

## 生成图形

#### 通过 Graphviz 提供的 dot 命令.

首先您要[安装 Graphviz 软件](https://graphviz.org/download/)。然后执行

```
dot ./doc/dot/serializers.dot -T png -o ./doc/dot/serializers.png 
```

#### 通过在线转换网站

如果您不想安装这个过于重量级的应用程序， 幸运的是我发现一个良心的转换网站。它免费！

请点击这里进入在线转换页面 [dot-to-png](https://onlineconvertfree.com/zh/convert-format/dot-to-png/)

上传文件就可以生成 png 图形了。

![UML](/uploads/images/graph-serializers.jpg "cover:border")


[django-extensions]: https://github.com/django-extensions/django-extensions "Django框架的全局自定义管理扩展"
[dot]: https://www.graphviz.org/pdf/dotguide.pdf "图表描述语言"
[Graphviz]: https://www.graphviz.org/ " 一个图形可视化软件"
