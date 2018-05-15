title: Python eval安全案例
date: 2017-06-13 12:15:12
---

关于Python的eval函数， 大家一致的避免使用。 但有时候必须使用， 怎么保证安全呢？ 下面我用一个案例来避免eval潜在的风险。 当然这只是其中的一种。

我的使用场景是这样的， 要把mongodb中的输出bson类型转换成JSON。 我需要转换的JSON是这样的, 看样子是个map类型， 但不是JSON类型， 确切的说他是bson类型。

```bson
{
  "_id" : ObjectId("58e4506f0b14fcb6cb4ecf76"),
  "database" : "test",
  "collection" : "users",
  "command" : "count",
  "params" : {
    "count" : "users"
  },
  "start_time" : ISODate("2017-04-05T10:03:27.777Z"),
  "end_time" : ISODate("2017-04-05T10:03:27.780Z")
}
```

以上我们需要在作用域中有ObjectId对象， 和ISODate对象, 来分别做两个类型的实例化。 实例化后再通过json.dumps转换为JSON字符串. 所以我想到了eval， 把ObjectId和ISODate分别创建对应的函数.

为了安全考虑，对eval的**globals**参数中的`__builtins__`设置为空， 避免掉使用所有内置函数， 然后通过eval第三个参数**locals**进行实现白名单的机制(safe_map安全映射)。 

```python
#! -*- coding: utf-8 -*-
import arrow, re
from bson.son import SON
from bson.binary import Binary, UUIDLegacy, STANDARD
from bson import ObjectId as objectid

ReplaceStrings = (
    ('new.*.Date', 'Date'),
    ('new.*.String', 'String'),
    ('new.*.ObjectId', 'ObjectId')
)


def ObjectId(_id):
    return objectid(_id)


def Date(string=''):
    if string:
        return arrow.get(string).datetime
    else:
        return arrow.get().datetime

def ISODate(string=''):
    return Date(string)


null = None
true = True
false = False


# 定义安全函数列表
SAFES = ('ObjectId', 'Date', 'null', 'true', 'false', 'SON', 'True', 'False', 'ISODate')
SAFE_MAPS = dict(
    [ (k, locals().get(k, None)) for k in SAFES ]
)


def to_python(string):
    """
    把Python代码转换为BSON代码

    目前支持的BSON类型有
        - ObjectId
        - Date
    """
    _string = '''x = %s''' % string

    # 批量替换区
    for _from, _to in ReplaceStrings:
        _string = re.sub(_from, _to, _string)

    x = {
        "error": "E10051",
        "message": "转换BSON失败"
    }

    # 开始转换
    try:
        exec(
            _string,
            {'__builtins__': None},
           SAFE_MAPS
        )

        x = SAFE_MAPS.get('x', x)
    except NameError as e:
        return {
            "error": "E10050",
            "message": str(e)
        }
    except Exception as e:
        return {
            "error": "E10055",
            "message": str(e)
        }

    return x

```

通过以上的`to_python`函数转换字符串到python实例. 在通过`json.dumps`转换json字符串, 然后就可以得到以下结果.

```json
{
  "_id": "58e4506f0b14fcb6cb4ecf76",
  "collection": "users",
  "command": "count",
  "database": "test",
  "end_time": "2017-04-05T10:03:27.777Z",
  "params": {
    "count": "users"
  },
  "start_time": "2017-04-05T10:03:27.780Z"
}
```
