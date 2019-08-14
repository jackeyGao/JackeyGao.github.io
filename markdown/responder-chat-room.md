title: 使用 responder 实现多人在线聊天室
date: 2019-07-05 09:28:19
---
![2019-07-05](/uploads/images/2019-07-05.jpeg "cover")

我在之前的文章中提到 [responder] 是个新的 Web 框架， 它的介绍是『*A familiar HTTP Service Framework for Python.*』

他是基于 [ASGI] 接口做的支持异步的 Web 框架. [ASGI] 的出现让 Python 生态实现 Websockets 技术提高了便利性。 而 responder 框架更是以便捷的 API 让开发者更快的实现 websockets 需求.

下面我做了一个基于 websockets 的聊天室， 在 responder 上开发.


```python
import responder
from collections import defaultdict
from jinja2 import Template
from starlette.websockets import WebSocketState
from starlette.websockets import WebSocketDisconnect


api = responder.API()

__version__ = 'v0.0.1'

sessions = defaultdict(list)

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>{{ room }}</title>
    </head>
    <body>
        <h1>Chat Room ({{ room }})</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://"+location.host+"/ws?room=default");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


async def broadcast_message(room_sessions, msg):
    for s in room_sessions:
        if s.client_state == WebSocketState.CONNECTED:
            await s.send_json(msg)
        elif s.client_state == WebSocketState.DISCONNECTED:
            room_sessions.remove(s)


@api.route("/")
async def room(req, resp):
    room = req.params.get('room', 'default')
    resp.html = Template(html).render(**locals())


@api.route('/ws', websocket=True)
async def websocket(ws):
    await ws.accept()

    room = ws.query_params["room"]

    sessions[room].append(ws)

    await broadcast_message(sessions[room], "Has new user join room")

    while True:
        try:
            msg = await ws.receive_text()
        except WebSocketDisconnect as e:
            break

        # Broadcast
        await broadcast_message(sessions[room], msg)

    sessions[room].remove(ws)
    await ws.close()


if __name__ == '__main__':
    api.run(address='0.0.0.0')
```

比起 [Django Channels] 大量的封装， responder 仅提供 websockets 基础功能， 所以我们要维护各个链接的 session ，这比较像 Django 维护的 Group。 每次有新的消息，我们需要对所有链接的 session 进行广播发送。 



[responder]: https://python-responder.org/ "responder 文档"
[ASGI]: https://asgi.readthedocs.io/en/latest/ "ASGI 介绍"
[Django Channels]: https://channels.readthedocs.io/en/latest/ "Django 实现 ASGI 网关的框架"

