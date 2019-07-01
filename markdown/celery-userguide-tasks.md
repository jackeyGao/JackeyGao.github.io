title: Celery用户手册 - Tasks 
date: 2016-04-19 14:39:27
tags: 
- Python
- Celery
- 翻译
---

`Tasks`是Celery 应用的构建块。事实上Celery应用是由一个或多个Task拼装组成的。

一个Task即是一个对象， Task被创建后可以被所有调用， 它是双重角色， 当Task被调用可以通过Task可以发送消息， 同时当作为一个worker的时候可以接收消息，并消费。

每个Task name 都是唯一的， 这样可以通过这个名字，找到合适的function去执行消费。

当发送一个任务消息在worker确认(acknowledged)前不会消失，一个worker可以提前存储很多消息，如果worker进程崩溃或killed，消息也不会消失， 消息会通过在投递的方式给其他存活worker。

理想的Task函数必须是幂等的，这意味着相同的参数调用多次不会出现不同的结果。但是worker并不知道函数是幂等的， woker默认是提前确认消息， 在执行完成之前这个task永远不会被重复执行。 这个就是上锁(LOCK)意思。这一段和上一段还是有区别的， 这一段强调的是**开始执行之前确认**。

当然确认如果任务是幂等的，你可以设置`acks_late`选项来控制worker 在函数返回之后去确认消息`acknowledge`. 请参考: [Should I use retry or acks_late?](http://docs.celeryproject.org/en/latest/faq.html#faq-acks-late-vs-retry%20%22%22)


在这一章节， 你将学习所有关于任务的定义，以下为目录:

> - [Basics](#basics)
> - [Names](#names)
> - [Context](#context)
> - [Logging](#logging)
> - [Retrying](#retrying)
> - [List of Options](#listofoptions)
> - [States](#states)
> - [Semipredicates](#semipredicates)
> - [Custom task classes](#customtaskclasses)
> - [How it works](#howitworks)
> - [Tips and Best Practices](#tips)
> - [Performance and Strategies](#performance)
> - [Example](#example)

## Basics <span id="basics"></span>

你可以很容易的创建任务在任何的可调用函数上使用`task()`装饰器.

```python
from .models import User

@app.task
def create_user(username, password):
    User.objects.create(username=username, password=password)
```

可以在装饰器上指定参数， 来设置`Task`

```python
@app.task(serializer='json')
def create_user(username, password):
    User.objects.create(username=username, password=password)
```

**Multiple decorators**

当使用多个装饰器，需要确保任务装饰生效， 把`task decorator` 写在函数第一个装饰器.

```python
@app.task
@decorator2
@decorator1
def add(x, y):
    return x + y
```

**如何引入task装饰器？**

`task decorator` 存在于你的Celery应用的实例上， 上一节我们已经讲过如何声明Application和使用它. 

如果你使用的是Django 或者仍然适用老的版本， 你可能导入`task decorator`的方式是下面这样.

```python
from celery import task

@task
def add(x, y):
    return x + y
```

## Names <span id="names"></span>

每个任务都有一个唯一的名称， 一个任务创建时如果不提供一个自定义的名字， 将会去生成一个任务.

```python
>>> @app.task(name='sum-of-two-numbers')
>>> def add(x, y):
...     return x + y

>>> add.name
'sum-of-two-numbers'
```

最好的方式是适用模块名称作为一个名称空间，如果一个任务另外一个模块中也有这样的名称如user模块中有`add`, group 模块中也有`add`, 那么这样就会冲突. 最好的方式如下:

```python
>>> @app.task(name='tasks.add')
>>> def add(x, y):
...     return x + y
```

你可以通过调用task的属性来获取task name.

```python
>>> add.name
'tasks.add'
```

如果不指定， 默认也会通过模块名和函数名拼装生成name

`tasks.py`:

```python
@app.task
def add(x, y):
    return x + y

>>> from tasks import add
>>> add.name
'tasks.add'
```

**自动命名和相对import**

相对import和自动命名不能一起工作， 所以如果适用相对引入你必须精确的设置name.

如果一个客户端(创建消息的时候) 导入这个`myapp.tasks` 通过`.tasks`导入，另外一个worker导入模块通过`myapp.tasks`， 生成的名称不匹配导致worker会抛出`NotRegistered` 从而不能工作.

Django INSTALLED_APPS的`project.myapp`风格.

```python
INSTALLED_APPS = ['project.myapp']
```

如果你安装app使用`project.myapp`, 那么task导入的时候也要通过`project.myapp.tasks`导入， 所以你要确保总是使用相同的名称导入任务.

```python
>>> from project.myapp.tasks import mytask   # << GOOD

>>> from myapp.tasks import mytask    # << BAD!!!
```

上面第二个例子将导致任务以不同的方式命名， 进而导致客户端和worker不用的任务名称。

```python
>>> from project.myapp.tasks import mytask
>>> mytask.name
'project.myapp.tasks.mytask'

>>> from myapp.tasks import mytask
>>> mytask.name
'myapp.tasks.mytask'
```

因而你导入必须一致， 这也是python推荐的方式。

同样的你不应该使用旧风格进行相对引入.

```python
from module import foo   # BAD!

from proj.module import foo  # GOOD!
```

以下新的风格相对引入也是可以推荐的

```python
from .module import foo  # GOOD!
```

如果你的程序已经做了错的引入， 并且你没有时间去重构， 建议通过显式的指定名称去覆盖自动命名.

```python
@task(name='proj.tasks.add')
def add(x, y):
    return x + y
```

## Context <span id="context"></span>

执行任务`request` 包含的信息和状态.

`request`定义了以下属性

key|value
---|---
**id:**|执行任务的唯一ID
**group:**|组id如果属于组
**chord:**|The unique id of the chord this task belongs to (if the task is part of the header).
**args:** |位置参数
**kwargs:** | 键值参数
**retries:** |重拾次数
**is_eager:** |如果不是工人是本地客户端，设置为True
**eta:** |预计任务时间
**expires:** |任务的过期时
**logfile:**|worker 的日志文件, See: [logging](#logging)
**loglevel:**|当前使用的日志级别
**hostname:**|worker实例的hostname
**delivery_info:**|额外的传递信息
**called_directly:**|This flag is set to true if the task was not executed by the worker.
**callbacks:**|回调函数
**errback:**|异常回调函数
**utc:**|如果为True说明调用者启动了utc

3.1 新属性
key|value
---|---
**headers:**|映射消息头
**reply_to:**|发送replay到哪个队列
**correlation_id:**|通常与任务id通用， 常用语amqp的跟踪回复


一个从context获取获取信息的例子:

```python
@app.task(bind=True)
def dump_context(self, x, y):
    print('Executing task id {0.id}, args: {0.args!r} kwargs: {0.kwargs!r}'.format(
            self.request))
```

## Logging <span id="logging"></span>

worker 将会自动配置logging， 也可以手动配置定制logging 日志输出.

Celery 提供一个名为`celery.task`的logger供使用, 你可以通过这个logger 自动的生成一个名称和唯一id作为日志的一部分.

推荐在每个模块中都声明一个logger， 每个模块使用单独的logger.

```python
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

@app.task
def add(x, y):
    logger.info('Adding {0} + {1}'.format(x, y))
    return x + y
```

Celery 使用Python标准库的logging模块， 文档支持可以在[logging](http://docs.python.org/dev/library/logging.html#module-logging) 模块中看到

你也可以使用`print()`, 任何写入标准输出和标准错误都会转到日志系统。 所以print的字符也会作为日志记录， 记录等级为**WARN**.


## Retrying <span id="retrying"></span>

`retry()` 可以重试任务， 当任务出现可恢复的错误.

当调用`retry()`时将会发送一个新的消息， 使用相同的task-id,  确保消息和原始任务属于相同的队列.

当一个消息重试后， 任务也会记录一个状态。这样你可以使用结果实例跟踪任务状态记录(see [States](#states))

一个使用`retry()` 的例子:

```python
@app.task(bind=True)
def send_twitter_status(self, oauth, tweet):
    try:
        twitter = Twitter(oauth)
        twitter.update_status(tweet)
    except (Twitter.FailWhaleError, Twitter.LoginError) as exc:
        raise self.retry(exc=exc)
```

`bind` 参数告诉装饰器将会给一个可以访问的self实例.

当存储任务结果，exc 是用于传递异常信息用户日志输出。 内容有异常信息和traceback信息都存在于exc.

如果此任务有`max_retries`值， 并且重试次数超过了这个值， 那么这个exc异常将会重新raise.  如果是下列情况将不会这样:

- exc 没有指定

这种情况下将会raise `MaxRetriesExceeded`异常, 这个是默认异常

- 没有异常

当重试没有异常发生(也就是上面except没有发生)， 重试次数达到了， 但task还没有正确返回， 可以指定给exc一个异常， 用于代理默认的`MaxRetriesExceeded`.

```python
self.retry(exc=Twitter.LoginError())
```

将会触发提供的异常信息。 

**自定义重试间隔**

当一个任务要去重试， 可以指定一个时间之后再去重试. 使用`default_retry_delay`属性来设置默认延迟.默认是三分钟,  注意: 延迟的单位是秒.

你可以使用 `retry(..., countdown=60s)`来覆盖task级别的`default_retry_delay`时间. 两种方法灵活使用 

```python
@app.task(bind=True, default_retry_delay=30 * 60)  # retry in 30 minutes.
def add(self, x, y):
    try:
        …
    except Exception as exc:
        raise self.retry(exc=exc, countdown=60)  # override the default and                                                 # retry in 1 minute                        
```

## List of Options <span id="listofoptions"></span>

Task.**name**

task 注册名

可以手动设置，也可以生成此name. See: [Names](#names)

未完待续>>>





