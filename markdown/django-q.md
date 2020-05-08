title:  django-q 异步调度框架的全新选择
date: 2020-05-08 03:04:55
---

![by unsplash](/uploads/images/django-q.jpeg "cover")

在使用 Django q 之前我用过很多异步框架， 包括 Celery， Django Channels 等调度框架， 但如果您用过前面两个你会发现他是一个很全面并且很重的框架， 所以我写个能够异步发邮件的框架， 必须要用到 Redis 或者 MQ 服务， 这让我的部署过程变得异常的繁琐。 所以无论我的项目功能多么简单， 只要我用到异步任务， 那么我必须面对这两个看起来像庞然大物的东西。

由于我的工作几乎全是运维平台的开发或者其他支撑平台， 这样的应用几乎无须关联 redis 来提高性能。 所有在不追求高性能高并发的的前提下， 我只需要需求轻量的框架， 来完成我的相关调度。

在我的工作过程中， 比较频繁用到的功能点有

- 异步任务 (CI/CD过程经常需要)
- 定时任务

django-q 都能完美的支持， 而且最重要的是在性能要求不高的情况下可以拜托其他后端应用(Redis, MQ)的依赖， 这一点对快速开发和快速部署的运维平台（支撑平台）非常重要.

## django-q

[django-q 文档介绍]

功能点

- 基于 Multiprocessing worker pools
- 异步任务
- 定时任务和重复任务
- 加密和压缩参数
- 状态回写数据库或缓存
- 结果钩子， 组和链式调用
- Django Admin 集成
- Paas 式， 能与多个应用实例兼容.
- 多集群监控
- 支持 Redis, Disque, IronMQ, SQS, MongoDB or ORM
- 支持 Rollbar 和 Sentry

Django Q 是一个用于处理任务队列， 调度任务和辅助功能的 Python multiprocessing Django 应用包。 目前为止它仅支持相对比较新的技术栈， Python 3.7 Django 2.2 3.0 以上.

```shell
$ pip install django-q
```

```python
INSTALLED_APPS = (
    # other apps
    'django_q',
)
```

```python
# example ORM broker connection

Q_CLUSTER = {
    'name': 'DjangORM',
    'workers': 4,
    'timeout': 90,
    'retry': 120,
    'queue_limit': 50,
    'bulk': 10,
    'orm': 'default'
}
```

**启动集群**

除了启动 web 实例， 异步任务处理需启动 qcluster.

```shell
$ python manage.py qcluster 
```

## 执行任务

异步的， 不会阻塞请求。

```python
from django_q.tasks import async_task

# views.py
# user requests a report.
def create_report(request):
    async_task('tasks.create_html_report',
            request.user,
            hook='tasks.email_report')
```

## 定时任务

支持定时一次性任务及周期任务, 和 Django 高度集成， 直接操作 Model 就可以对定时任务进行修改。

```python
 # Use the schedule wrapper
from django_q.tasks import schedule

schedule('math.copysign',
         2, -2,
         hook='hooks.print_result',
         schedule_type='D')

# Or create the object directly
from django_q.models import Schedule

Schedule.objects.create(func='math.copysign',
                        hook='hooks.print_result',
                        args='2,-2',
                        schedule_type=Schedule.DAILY
                        )

# In case you want to use q_options
schedule('math.sqrt',
         9,
         hook='hooks.print_result',
         q_options={'timeout': 30},
         schedule_type=Schedule.HOURLY)

# Run a schedule every 5 minutes, starting at 6 today
# for 2 hours
import arrow

schedule('math.hypot',
         3, 4,
         schedule_type=Schedule.MINUTES,
         minutes=5,
         repeats=24,
         next_run=arrow.utcnow().replace(hour=18, minute=0))
```

关于 `tasks.create_html_report`， 是你函数的引用路径。 当然如果 import 进当前作用域， 直接写函数也是可以的。 具体可以参考 django-q 文档.

更多例子请参考 [Django-q Examples]

[django-q 文档介绍]: https://django-q.readthedocs.io/en/latest/index.html "django-q 文档介绍"
[Django-q Examples]: https://django-q.readthedocs.io/en/latest/examples.html "Django-q Examples"

