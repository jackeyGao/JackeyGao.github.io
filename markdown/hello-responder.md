title: responder初体验
date: 2018-12-05 14:03:52
---

![responder](/uploads/images/responder.png "cover:radius")

[responder](https://github.com/kennethreitz/responder) 是 [@kennethreitz](https://github.com/kennethreitz) 新开发的一个项目， 是一个基于 Python 的 HTTP 服务框架. 底层用了 Starlette 的框架, Starlette 是一款轻量级的 ASGI 框架/工具包， 可以用 Starlette 构建高性能的异步 IO 服务. 

写到这里， 你可能想知道 ASGI 是什么， ASGI(异步服务网关接口) 由 Django 团队提出，为了解决在一个网络框架里（如 Django）同时处理 HTTP、HTTP2、WebSocket 协议。为此，Django 团队开发了 Django Channels 插件，为 Django 带来了 ASGI 能力。 通俗一点就是 Django Channels 中使用的 websockets 其实就是 ASGI 网关协议的支持.

作为运维开发， 当需要可视化操作服务器的时候， 可能就需要异步进行操作。 传统的同步操作， 会加长等待时间， 造成不好的应用体验. 而 ASGI技术 就能解决这一点, 上面提到的 Django 框架可以使用 Django Channels来支持 websocket 完成这个需求.  但今天我发现一个更合适的框架responder。

相对于 Starlette , responder 对开发者更加友好一点。 kennethreitz写了 requests 号称"HTTP for Humans" 更加清楚这一点. 事实上比较下来， responder 也比Starlette 优雅很多.

## 安装

依赖:

- Python 3.6 +

```python
pip install responder
```

可能是新项目， 打包还不太完善. 在安装过程和启动的时候遇到了两个错误, 在github上均有处理方法.

- [#255](https://github.com/kennethreitz/responder/issues/255) ModuleNotFoundError: No module named 'starlette.lifespan'  
- [#187](https://github.com/kennethreitz/responder/issues/187) AttributeError: module 'typing' has no attribute 'AsyncGenerator'


## 让我们写个例子

*main.py*

```python
import responder


api = responder.API()


@api.route("/")
def hello_world(req, resp):
    resp.text = "hello, world!"


if __name__ == '__main__':
    api.run()
```

可以看到， 比较类似于微框架 Flask，定义比较清晰.

启动

```shell
python main.py
INFO: Started server process [29036]
INFO: Waiting for application startup.
INFO: Uvicorn running on http://127.0.0.1:5042 (Press CTRL+C to quit)
```

默认端口5402， 当访问http://127.0.0.1:5042时， 会显示出来 Hello world.  这只是一个 Hello world 例子， 它真正强大的地方在于异步处理, 这个在后面的例子中.


## 接受路由参数

即动态 URL， 在路由中使用f-string语法就可以添加动态参数.

*main.py*

```python
@api.route("/hello/{who}")
def hello_to(req, resp, *, who):
    resp.text = f"hello, {who}!"
```

```shell
$ curl http://127.0.0.1:5042/hello/JackeyGao
hello, JackeyGao!%
```

## 渲染模板

模板引擎使用的 jinja2.

*templates/hello.html*

```jinja
<div style="padding: 1em; background: #000; color: #fff;">
Hello, {{ who }}!
</div>
```

*main.py*

```python
@api.route("/hello/{who}/html")
def hello_html(req, resp, *, who):
    resp.content = api.template('hello.html', who=who)
```

效果

```shell
$ curl http://127.0.0.1:5042/hello/JackeyGao/html
<div style="padding: 1em; background: #000; color: #fff;">
Hello, JackeyGao!
</div>
```

## 返回 JSON / YAML

如果你想做一个 JSON API， 只需要把 resp.media 属性设置为可被 JSON 序列化的 Python 对象即可.

*main.py*

```python
@api.route("/hello/{who}/json")
def hello_to(req, resp, *, who):
    resp.media = {"hello": who}
```

效果

```shell
$ curl http://127.0.0.1:5042/hello/JackeyGao/json
{"hello": "JackeyGao"}
```

如果客户端请求 YAML，需要设置 header 的 Accept: application/x-yaml 参数.

## 设置返回码

返回 HTTP 状态吗

*main.py*

```python
@api.route("/416")
def teapot(req, resp):
    resp.status_code = api.status_codes.HTTP_416
```


```shell
$ curl -i http://127.0.0.1:5042/416
HTTP/1.1 416 Requested Range Not Satisfiable
server: uvicorn
date: Wed, 05 Dec 2018 06:59:43 GMT
content-type: application/json
transfer-encoding: chunked

null
```

## 设置响应 Header

*main.py*

```python
@api.route("/pizza")
def pizza_pizza(req, resp):
    resp.headers['X-Pizza'] = '42'
```


```shell
$ curl -i http://127.0.0.1:5042/pizza
HTTP/1.1 200 OK
server: uvicorn
date: Wed, 05 Dec 2018 07:00:58 GMT
content-type: application/json
x-pizza: 42
transfer-encoding: chunked

null
```

## 接受数据和后台任务.

这个才是 responder 的闪光点， 可以快速的创建一个异步的任务.

*main.py*

```python
import time

@api.route("/incoming")
async def receive_incoming(req, resp):

    @api.background.task
    def process_data(data):
        """Just sleeps for three seconds, as a demo."""
        time.sleep(3)
        print("Done")


    # Parse the incoming data as form-encoded.
    # Note: 'json' and 'yaml' formats are also automatically supported.
    data = await req.media()

    # Process the data (in the background).
    process_data(data)

    # Immediately respond that upload was successful.
    resp.media = {'success': True}
```

此请求会立即响应，会在后台执行**process\_data**. 这方便了我们处理数据， 比如发邮件等耗时操作.

## Websockets

简单的不可思议(就 Django Channels 来说, Django websockets 请参考我的这个聊天室项目 [django-vuejs](https://github.com/jackeygao/djang-vuejs/).).

<del>就目前(2018.12.05)版本(responder: 1.1.2)而言, 下面代码还不能正常工作. 但接口形式已经定义完毕, 期待后面版本会加上去, 如果下面代码可用， 请留言通知.</del>

讨论PR: [responder#114](https://github.com/kennethreitz/responder/pull/114)

讨论Issue: [responder#190](https://github.com/kennethreitz/responder/issues/190)

> **更新!** 2018-12-13 websockets代码已经更新， 可以工作了！！


```python
@api.route("/ws", websocket=True)
async def websocket(ws):
    await ws.accept()
    await ws.send_text("Hello via websocket!")
    await ws.close()


@api.route('/{greeting}', websocket=True)
async def greeting(ws, greeting):
    await ws.accept()
    while True:
        name = await ws.text()
        await ws.send_text(f"{greeting} {name} via ws!")
    await ws.close()
```


## 进阶

后续会写一篇进阶的学习. 除了这些， responder 还支持以下特行

- 基于类的视图
- 后台任务
- GraphQL 
- OpenAPI Schema
- 安装 WSGi 程序
- 单页的 Web 应用的支持
- Cookie Sesssion
- before\_request 中间件
- 测试 Client
- 强制 HTTPS 功能
- 安全的可信主机功能

请[进一步阅读官方文档](https://python-responder.org/en/latest/tour.html). 


## 总结

responder 是新开发的一个支持 ASGI 的框架， 优点是接口清晰对开发者友好。 能够能方便的构建异步服务或 WebSockets 服务, 同时可以安装 WSGI 协议的服务. 是一个很有潜力的一个框架，但就目前来说最好不要上生产环境。 好在社区比较活跃， 保持关注吧. 
