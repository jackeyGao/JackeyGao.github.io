title: WebSocket 404
date: 2019-07-18 17:54:30
---

今天遇到一个关于 WebSocket 路径 404 的错误， 经过排查这个错误是 nginx 转发 WebSoeckt 协议导致的， 因为没有处理 ws 路径的 WebSocket 协议，所以 ws 路径就走了 HTTP 协议. 这显然是不可行的，所以 Web 服务就出现了 404 错误.

解决方法也很简单， 在 Django Channels [部署页面](https://channels.readthedocs.io/en/latest/deploying.html#http-and-websocket "Django Channels 上线部署")中看到相关的解决方法.

在 nginx 上配置

```nginx
upstream channels-backend {
    server localhost:8000;
}
...
server {
    ...
    location / {
        try_files $uri @proxy_to_app;
    }
    ...
    location @proxy_to_app {
        proxy_pass http://channels-backend;

        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";

        proxy_redirect off;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Host $server_name;
    }
    ...
}
```

不要忘记 reload.

![夏天](/uploads/images/summer.jpg "cover")




