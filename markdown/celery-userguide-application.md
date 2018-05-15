title: Celery用户手册 - Application
date: 2016-04-18 14:51:56
tags:
- Python
- Celery
- 翻译
---

## Application

必须使用一个Application实例来创建celery 任务.

该Application线程是安全(thread-safe)的，以便你可以使用多个不同的Application 配置.  组件和任务能共存于相同的进程空间。

创建一个Application实例:

```python
>>> from celery import Celery
>>> app = Celery()
>>> app
<Celery __main__:0x100469fd0>
```

最后一行显示的是此Application实例的文本描述，其中包括celery类的名称，此实例存在于`__main__` 主模块中和此实例的内存地址.

### Main Name

`Main Name` 是个很重要的概念， 以下会介绍为什么重要.

当你使用Celery 推送一个任务消息， 这个消息不携带任何的源代码，但是需要指定一个此消息需要执行的任务名称。这种工作方式类似于hostname工作方式， 在网络上: 每个worker维护着任务名和他们所能执行的实际函数. 这就是所谓的`task registry`(任务注册表).

每当你定义一个任务,  该任务也将要添加到本地的`task registry`

```python
>>> @app.task
... def add(x, y):
...     return x + y
>>> add
<@task: __main__.add>
>>> add.name
__main__.add
>>> app.tasks['__main__.add'] # 根据task name取出实际函数(function)
<@task: __main__.add>
```

这里你会在此看到`__main__` ，每当Celery无法检索到function属于哪个模块, 它会使用主模块名称生成任务模块， 即`__main__.add`.

这种现象只会出现在下面情况中：

1. 定义的task所属的application 在一个主模块中
2. 此application实例创建在Python 交互式环境中

第一种:
`tasks.py`

```python
from celery import Celery
app = Celery()

@app.task
def add(x, y): return x + y

if __name__ == '__main__':
    app.worker_main()
```

当这个`tasks.py` 作为一个主模块执行的时候(`__main__`成立)任务名称以`__main__`开头， 即`__main__.add`. 但是当此模块被另外一个模块引用的时候，它的任务名称将以`tasks`开头, 即`tasks.add`.

```python
>>> from tasks import add
>>> add.name
tasks.add
```

可以在创建的Application的时候指定一个名称.

```python
>>> app = Celery('tasks')
>>> app.main
'tasks'

>>> @app.task
... def add(x, y):
...     return x + y

>>> add.name
tasks.add
```

> 参考: [Names](http://docs.jinkan.org/docs/celery/userguide/tasks.html#task-names)


### Configuration

你可以设置Celery的其他选项，这些选项作用于application 实例. 但你最好单独定义一个配置模块。 

查看一个配置

```python
>>> app.conf.CELERY_TIMEZONE
'Europe/London'
```

你也可以直接设置配置项

```python
>>> app.conf.CELERY_ENABLE_UTC = True
```

使用`update`方法更新多个键值.

```python
>>> app.conf.update(
...     CELERY_ENABLE_UTC=True,
...     CELERY_TIMEZONE='Europe/London',
...)
```

配置对象可以通过多种方法去修改操作, 他们的优先级是:

1. 运行时修改
2. 配置模块(如果有的话)
3. 默认配置模块(**celery.app.defaults**)

你甚至可以使用celery.add_defaults()方法来添加新的默认源.

> 参见: [Configuration reference](http://docs.jinkan.org/docs/celery/configuration.html#configuration) 查看支持的通用选项参数列表.

#### config_from_object

` Celery.config_from_object()` 可以从一个配置对象加载配置， 可以是一个配置模块， 或者其他配置属性的对象.


需要注意的是， 使用此方法后默认参数将会被重置， 如果配置对象的键值和默认对象有冲突的话。 如果你想设置额外的配置你应该在之后在此方法之后去设置.


**Example 1: 使用name作为module**

```python
from celery import Celery

app = Celery()
app.config_from_object('celeryconfig')
```

`celeryconfig` 作为字符串对象传入， `celeryconfig`内容如下

`celeryconfig.py`:
```
CELERY_ENABLE_UTC = True
CELERY_TIMEZONE = 'Europe/London'
```

**Example 2: 使用configtion module**

```python
from celery import Celery

app = Celery()
import celeryconfig
app.config_from_object(celeryconfig)
```

**Example 3: 使用configtion class/object**

```python
from celery import Celery

app = Celery()

class Config:
    CELERY_ENABLE_UTC = True
    CELERY_TIMEZONE = 'Europe/London'

app.config_from_object(Config)
# or using the fully qualified name of the object:
#   app.config_from_object('module:Config')
```

#### config_from_envvar

使用`Celery.config_from_envvar()`方法可以从环境变量来设置选项.

从环境变量名为**CELERY_CONFIG_MODULE**加载配置:

```python
import os
from celery import Celery

#: Set default configuration module name
os.environ.setdefault('CELERY_CONFIG_MODULE', 'celeryconfig')

app = Celery()
app.config_from_envvar('CELERY_CONFIG_MODULE')
```

然后你可以指定配置模块，通过设置环境变量的方法:

```bash
$ CELERY_CONFIG_MODULE="celeryconfig.prod" celery worker -l info
```

### Censored configuration

如果你想打印出配置， 但是你不想打印一些敏感的数据， 就像密码和API 密钥类似的敏感信息。

Celery 支持用于展示配置相关逻辑， 一个就是`humanize()`:

```python
>>> app.conf.humanize(with_defaults=False, censored=True)
```

此方法将会隐藏敏感信息， 如果`with_defaults`为true的话， 可以显示为默认的值。

默认情况下Celery认为配置KEY中包含`API`, `TOKEN`, `KEY`, `SECRET`, `PASS`, `SIGNATURE`, `DATABASE`这些字符的都为敏感信息。


### Breaking the chain

并没有看懂这段 , 貌似讲的是一种规范.

### Abstract Tasks

以上所有的tasks创建的时候都使用了task() 装饰器，task会继承Task class.

当然可以指定成其他的Task基类， 比如下面代码中`base=OtherTask`, 那么此task的基类为`OtherTask`.

```python
@app.task(base=OtherTask):
def add(x, y):
    return x + y
```

如果你想创建一个自定义的Task 类， 你必须继承自`celery.Task`

```python
from celery import Task

class DebugTask(Task):
    abstract = True

    def __call__(self, *args, **kwargs):
        print('TASK STARTING: {0.name}[{0.request.id}]'.format(self))
        return super(DebugTask, self).__call__(*args, **kwargs)
```




