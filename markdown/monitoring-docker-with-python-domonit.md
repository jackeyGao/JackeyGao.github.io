title: 使用DoMonit监控Docker
date: 2016-08-17 09:30:01
tags: 
- Python
- 运维
- Monitoring
- Docker
---

本篇的目的是介绍Python包[Domonit](https://github.com/eon01/DoMonit), 一个基于Python语言开发的API封装的轻量监控程序.

监控可以让你可视化服务的基础架构, 生产环境不进行监控是不推荐的. 同样生产环境的Docker也需要监控, 特别是很多容器运行了关键的服务.

管理生产环境下的linux系统超过十年, 我有部署测试了很多基础架构和生产监控系统。从我经验来看, 采取云基础架构管理, 改变了我们使用管理基础架构的方式. 我想说即使问题的性质正在改变, 产品的质量变的更加重要，关键的监控也变的更积极主动,监控并不仅仅是收集和可视化哪些指标而意识到发生了什么. 在大多情况下, 监控是基于某个特别的用例和环境下(比如: 基于业务逻辑)。 这就是在某些情况下我实用脚本来编写监控程序, 我几乎都是使用Python， 有时使用Bash.

> 译者注: 大概意思就是云的出现， 一些基础的监控收集指标数据并且可视化的事情云服务提供商已经做了, 之后更多可能就是基于特定的场景进行监控, 这个时候没有通用的模版来监控, 只能自己写脚本来监控, 这个感触我太了解了， 因为我曾经写过两年的监控脚本


在我关于Docker的实验工作中, [Docker Swarm](https://docs.docker.com/swarm/) 和 Micro Services运行在Docker上. 我需要一个可以让我在自己编写的脚本使用获取监控指标的监控工具, 我通过此工具自定义一些监控指标和监控逻辑。 这就是我为什么要使用[Domonit](https://github.com/eon01/DoMonit)。 先看一下DoMonit是什么?

此工具用Python 封装了Docker API, 提供了更优雅的Python接口供您脚本调用获取Docker相关的数据. 基于Docker API 1.24版本封装, 兼容监控Docker版本1.12.x及以上的docker版本.


![码头鸟瞰图](/uploads/images/ashdod-port-aerial-view.jpeg "cover")


## DoMonit 目的

其目的是让你很容易的通过python编写方便监控Docker 所有容器的脚本， 搜集所有需要的指标数据,  

> The Github repository of Domonit is : https://github.com/eon01/DoMonit

## 封装信息

```bash
api/
├── changes.py
├── containers.py
├── errors.py
├── ids.py
├── inspect.py
├── logs.py
├── process.py
└── stats.py
```

api|说明
---|---
**containers**| 容器列表
**inspect**|返回指定id容器的基础信息
**ids**|返回容器id列表
**logs**|返回指定id容器的stdout和stderr日志
**process**|列出此容器中运行的进程信息, 在unix系统中通过ps命令完成的, 所以此功能不支持windows
**stats**|返回关于此容器的使用统计的实时数据

## 使用样例

创建虚拟环境 克隆项目

```bash
virtualenv domonit
cd domonit 
. bin/activate
git clone https://github.com/eon01/DoMonit.git
cd DoMonit
pip install -r requirements.txt
python examples.py
```

`examples.py`

```python
from api.containers import Containers
from api.ids import Ids
from api.inspect import Inspect
from api.logs import Logs
from api.process import Process
from api.changes import Changes
from api.stats import Stats

import json

c = Containers()
i = Ids()
print ("Number of containers is : %s " % (sum(1 for i in i.ids())))
if __name__ == "__main__":
    for c_id in i.ids():
        ins = Inspect(c_id)
        sta = Stats(c_id)
        proc = Process(c_id, ps_args = "aux")
        # Container name
        print ("\n#Container name")
        print ins.name()
        # Container id
        print ("\n#Container id")
        print ins.id()
        # Memory usage
        mem_u = sta.usage()
        # Memory limit
        mem_l = sta.limit()
        # Memory usage %
        print ("\n#Memory usage %")
        print  int(mem_u)*100/int(mem_l)

        # The number of times that a process of the cgroup triggered a "major fault"
        print ("\n#The number of times that a process of the cgroup triggered a major fault")
        print sta.pgmajfault()

        # Same output as ps aux in *nix
        print("\n#Same output as ps aux in *nix")
        print proc.ps()
```

我有五个容器， 出于简单， 我省略了其他的，保留1个输出信息.


```text
Number of containers is : 5 
#Container name
/vote_webapp_1
#Container id
1a29e9652822447a440799306f4edb65003bca9cdea4c56e1e0ba349d5112d3e
#Memory usage %
0.697797903077
#The number of times that a process of the cgroup triggered a major fault
15
#Same output as ps aux in *nix
{u'Processes': [[u'root', u'26636', u'0.0', u'0.2', u'76808', u'16228', u'?', u'Ss', u'15:43', u'0:00', u'/usr/local/bin/python2 /usr/local/bin/gunicorn app:app -b 0.0.0.0:80 --log-file - --access-logfile - --workers 4 --keep-alive 0'], [u'root', u'26773', u'0.0', u'0.2', u'88776', u'19976', u'?', u'S', u'15:43', u'0:00', u'/usr/local/bin/python2 /usr/local/bin/gunicorn app:app -b 0.0.0.0:80 --log-file - --access-logfile - --workers 4 --keep-alive 0'], [u'root', u'26784', u'0.0', u'0.2', u'88572', u'19800', u'?', u'S', u'15:43', u'0:00', u'/usr/local/bin/python2 /usr/local/bin/gunicorn app:app -b 0.0.0.0:80 --log-file - --access-logfile - --workers 4 --keep-alive 0'], [u'root', u'26787', u'0.0', u'0.2', u'88568', u'19816', u'?', u'S', u'15:43', u'0:00', u'/usr/local/bin/python2 /usr/local/bin/gunicorn app:app -b 0.0.0.0:80 --log-file - --access-logfile - --workers 4 --keep-alive 0'], [u'root', u'26793', u'0.0', u'0.2', u'88572', u'19828', u'?', u'S', u'15:43', u'0:00', u'/usr/local/bin/python2 /usr/local/bin/gunicorn app:app -b 0.0.0.0:80 --log-file - --access-logfile - --workers 4 --keep-alive 0']], u'Titles': [u'USER', u'PID', u'%CPU', u'%MEM', u'VSZ', u'RSS', u'TTY', u'STAT', u'START', u'TIME', u'COMMAND']}
[..etc..]
```

