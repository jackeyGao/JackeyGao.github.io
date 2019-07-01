title: 动态切换代理 - PAC方法
date: 2015-11-24 15:50:19
categories:
  - 折腾
tags:
  - 翻墙
  - Squid
  - Stunnel
  - Python
  - Flask
---

最近协助搭建了企业级翻墙系统， 由于没有现成的公司提供这些， 也没有成套比较成熟的方案(国外人用不着, 国内人不敢用的东西). 所以就自己摸索搭建而且也搭建了， 而且相对来说能控制. 可以参考这里[企业级翻墙方案](https://jackeygao.io/words/offices-proxy.html). 随着很多用户的使用一台服务器显得力不从心, 所以又买了一台然后Squid ＋ Stunnel方案都配好正常启动了。 

## 搞定负载均衡

PAC文件支持故障转移(比较坑, 这种机制比较坑， 我们基本上是避免采取的),比较头疼的是负载均衡, 又两种方案

* 一种是通过负载均衡程序转发
* 通过随机PAC文件配置.

前者的故障转移不好做, 因为客户端代理用的stunnel端口转发到squid端口, 如果stunnel端口依然存活而squid端口还在的话， 这种是转移不了的。然后PAC的故障转移坑的点也在这里. 所以只能不做采取. 后者是我们采取的方案， 开发一个web服务提供pac文件, 然后response的逻辑改下, 随机选择代理服务器生成pac. 这种方法测试一段时间之后能达到我们预期的效果.

负载均衡基于flask服务代码

**server.py**

```python
# -*- coding: utf-8 -*-
'''
File Name: web.py
Author: JackeyGao
Created Time: 五 11/13 16:11:23 2015
'''
import random, os, json
from flask import Flask
from flask import make_response
from flask import render_template
from flask import request

app = Flask(__name__)

@app.route('/')
def home():
    with open('proxys.json', 'r') as f:
        proxy_policy = json.loads(f.read())
    return render_template("index.html", count=len(proxy_policy))


@app.route('/proxy.pac')
def proxy():
    with open('proxys.json', 'r') as f:
        proxy_policy = json.loads(f.read())
    proxys = [ proxy for proxy, pl in proxy_policy for n in range(pl) ]
    random.shuffle(proxys)
    master = random.sample(proxys, 1)[0]
    sleve  = [ proxy for proxy in proxys if proxy <> master ]
    if sleve:
        proxy_list = "PROXY %s;PROXY %s;" % (master, sleve[0])
    else:
        proxy_list = "PROXY %s;" % master

    response = make_response(render_template('proxy.pac',
        proxy_list=proxy_list))
    response.mimetype = "text/plain"
    return response


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
```

## 故障转移

前面已经提到PAC的故障转移是通过Stunnel端口的联通性作出判断的, 当stunnel端口存活而上游的squid端口不通的情况是不会自动转移的。 所以需要一个监控脚本去刷新整个过程的联通性然后把结果给上面的flask web pac服务使用. 这里使用一个reload.py 脚本搞定， 然后把reload.py 做成计划任务.

**reload.py**

```python
# -*- coding: utf-8 -*-
'''
File Name: reload.py
Author: JackeyGao
Created Time: 二 11/24 13:09:20 2015
'''
import requests
import json

proxy_configs = {
    '114.xxx.xx.xx:7072': {
        'user': 'xxxxxx',
        'passwd': 'xxxxxxx',
        'return': '127.0.0.1',
        'priority': 1,
        },
    '114.xxx.xx.xx:7071': {
        'user': 'xxxxxx',
        'passwd': 'xxxxxxxxx',
        'return': '127.0.0.1',
        'priority': 1,
        },
    }

def request_error_handler(func):
    def _deco(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except requests.exceptions.ConnectionError as e:
            if '407' in str(e):
                print("%s代理服务器认证失败" % (args,))
            else:
                print("%s链接的其他错误E:(%s)" % (args, str(e)))
        except Exception as e:
            print("%s发生未知错误E:(%s)" % (args, str(e)))
        return False
    return _deco


@request_error_handler
def test_proxy_connection(proxy, user, passwd, return_ip):
    proxies = {
        "https": "http://%s:%s@%s" % (user, passwd, proxy),
    }
    url = "https://httpbin.org/ip"
    r = requests.get(url, proxies=proxies, timeout=10)
    origin = r.json().get("origin", None)
    if return_ip == origin:
        return True
    else:
        return False


if __name__ == '__main__':
    proxys = []
    for proxy, config in proxy_configs.items():
        status = test_proxy_connection(proxy, config.get('user'),
                config.get('passwd'), config.get('return'))
        if status:
            proxys.append((proxy, config.get("priority")))

    with open('proxys.json', 'w') as f:
        f.write(json.dumps(proxys))
```

然后经过pac文件路径改成现在起的地址.需要说明一点有些系统支持的pac文件每隔一段时间会重载pac文件, 这个时间越快对于客户端的故障转移就越及时. pac服务端的故障转移取决于reload.py 的执行间隔, 可以在crontab里面设置为5分钟, 甚至更少的时间.
 
