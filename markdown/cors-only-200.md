title: 非 200 返回 CORS Error 问题排查
date: 2021-09-22 17:45:20
---

![](/uploads/images/cors-error-cover.jpeg "cover:border")

## 问题表现

大家都知道如果出现CORS ERROR此类跨域问题，可以通过指定跨域的Headers来开放跨域。

大多数情况下，我们可以在nginx上来增加这些header

比如在nginx的location中增加以下控制项， 来达到swagger应用中能够跨域调试调用的结果:

```nginx
add_header 'Access-Control-Allow-Origin' 'http://swagger.example.net';
add_header 'Access-Control-Allow-Methods' 'GET, POST, DELETE, PUT, OPTIONS';
add_header 'Access-Control-Allow-Headers' 'DNT,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range';
add_header 'Access-Control-Expose-Headers' 'Content-Length,Content-Range';
```

但以上配置在我的环境中， 无法对某些错误的返回码生效， 具体表现就是400+，500+错误无法正常显示， 浏览器依然提示Cors Error错误。

## 问题排查

经过排查发现是 add_headers 配置项问题，需要add_header 第二参数增加always， 来显示的表示覆盖所有返回类型。

```nginx
add_header 'Access-Control-Allow-Origin' 'http://swagger.example.net' always;
add_header 'Access-Control-Allow-Methods' 'GET, POST, DELETE, PUT, OPTIONS' always;
add_header 'Access-Control-Allow-Headers' 'DNT,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range' always;
add_header 'Access-Control-Expose-Headers' 'Content-Length,Content-Range' always;
```

## 升级Nginx

如果您的nginx版本小于 < 1.7.5 , 是不支持 always 参数的。 所以你还需要升级下 nginx.




