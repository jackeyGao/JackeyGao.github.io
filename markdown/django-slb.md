title: SLB和django runserver结合报错问题
date: 2018-04-24 11:27:11
---


SLB 检测流量会使服务器报`[Errno 104] Connection reset by peer`

```
web_1       | ----------------------------------------
web_1       | Traceback (most recent call last):
web_1       |   File "/usr/local/lib/python2.7/SocketServer.py", line 596, in process_request_thread
web_1       |     self.finish_request(request, client_address)
web_1       |   File "/usr/local/lib/python2.7/SocketServer.py", line 331, in finish_request
web_1       |     self.RequestHandlerClass(request, client_address, self)
web_1       |   File "/usr/local/lib/python2.7/SocketServer.py", line 652, in __init__
web_1       |     self.handle()
web_1       |   File "/usr/local/lib/python2.7/site-packages/django/core/servers/basehttp.py", line 140, in handle
web_1       |     self.raw_requestline = self.rfile.readline(65537)
web_1       |   File "/usr/local/lib/python2.7/socket.py", line 480, in readline
web_1       |     data = self._sock.recv(self._rbufsize)
web_1       | error: [Errno 104] Connection reset by peer
web_1       | ----------------------------------------
web_1       | Exception happened during processing of request from ('100.116.165.131', 21753)
web_1       |
```


由于问题比较紧急， 具体原因没有查。 我直接用 gunicorn 模块启动项目， 完美解决. 试试上跑线上环境不能使用 runserver. 推荐: gunicorn uwsgi.


```bash
pip install gunicorn

gunicorn xxxxxx.wsgi 0.0.0.0:8000
```

静态文件可以通过 urls.py 生成静态文件 patterns。


```python
from django.contrib.staticfiles.urls import staticfiles_urlpattern

...

urlpatterns += staticfiles_urlpatterns()
```
