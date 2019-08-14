title: 使用CSP代替X-frame-options
date: 2018-12-18 14:04:49
---

![Content Security Policy](/uploads/images/Content-Security-Policy.jpg "cover")

内容安全策略（Content-Security-Policy）是W3C的一项重要标准，旨在防止广泛的内容注入攻击，如跨站点脚本（XSS）等。 CSP 有着灵活的白名单控制.

CSP 目前支持的浏览器有


- Chrome 25+
- Edge 14+
- Firefox 23+
- IE 10+
- Opera 15+


不支持 CSP 的浏览器只会忽略它，如常运行，默认为网页内容使用标准的同源策略。如果网站不提供 CSP 头部，浏览器也使用标准的同源策略(Same origin policy)a 比如: x-frame-options 控制嵌入白名单源, 大多数都是 sameorigin ， 表示仅当前主机域名可以嵌入(显然这没必要， 一般嵌入都是外面嵌入)。

CSP 通过指令进行各个安全项控制, 不只是可以对嵌入做控制.  可以参考下面两个文档阅读更多

- [CSP 介绍 | MDN](https://developer.mozilla.org/zh-CN/docs/Web/HTTP/CSP);
- [CSP 指令列表 | MDN](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy#Directives);
- [CSP 浏览器支持 | MDN](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy#Browser_compatibility)

## 背景

我最近做的项目是把所有的运维项目合并到一个项目里面， 当然最简单的方式是嵌入, 但在嵌入项目的时候发现了Chrome 控制台这样的错误.

```
(index):1 Refused to display 'http://xxx.com/' in a frame because it set 'X-Frame-Options' to 'sameorigin'.
```

显然这是因为sameorigin导致的.


## X-FRAME-Options 写法

如果我要允许被嵌入， 就要更新 X-Frame-Options 的值. 我们先看看此 Header 支持的写法.

- sameorigin

表示该页面可以在相同域名页面的 frame 中展示。

- deny

表示该页面不允许在 frame 中展示，即便是在相同域名的页面中嵌套也不允许。

- ALLOW-FROM uri

表示该页面可以在指定来源的 frame 中展示。 


Django 默认是 SameOrigin. 如果其他项目需要嵌入页面， 必须在被嵌入的项目为每个 endpoint 增加 @xframe\_options\_exempt 装饰器. 此装饰器是移除`X-Frame-Options` Response header, 表示此 View 可以嵌入任何页面， 这不符合 [OWASP Clickjacking](https://www.owasp.org/index.php/Clickjacking) 的建议. 所以我们可以通过ALLOW-FROM uri来指定单个项目来嵌入, 这也是我选择的方案. 或者我可以直接指定 ALLOW\_From uri 白名单的形式.

## 现实的问题.

但 Django 没有任何控制项， 可以完成`ALLOW-FROM uri`的控制, 虽然可以通过自定义中间件的形式， 或者通过[django-xframeoptions](https://github.com/paulosman/django-xframeoptions)第三方项目来设置, 但是我需要嵌入的项目太多， 而且我也不想一个一个的去更新， 这是我想要了在 nginx 上面设置这个header.


于是我在 nginx 配置里面加入.

```nginx
add_header X-Frame-Options ALLOW-FROM <my uri>;
```
但事实是增加这个 header 就出现了两个 X-Frame-Options header.

```
X-Frame-Options: sameorigin;
X-Frame-Options: ALLOW-FROM <my uri>;
```

浏览器对于多个值， 是直接不处理， 并直接拒绝通过此次同源策略的检查.

```
(index):1 Refused to display 'http://xxx.com' in a frame because it set multiple 'X-Frame-Options' headers with conflicting values ('SAMEORIGIN, ALLOW-FROM <my uri>'). Falling back to 'deny'.
```

所以 add\_header X-Frame-Options 并不是覆盖， 而且追加到两个 header， 显然这样不行。当然 nginx 上也有其他方式， 去除 SameOrigin 这个值，或者直接更新这个 header. 但我准备采取 CSP, 并移除 X-Frame-Options。


## 使用 CSP.

前面提到可以使用 `@xframe_options_exempt` 装饰器， 移除X-Frame-Options。 但是我要移除所有的视图， 就特别麻烦了。 但可以通过移除django.middleware.clickjacking.XFrameOptionsMiddleware中间件来移除当前项目所有视图的x-Frame-Options。

> %warning 为什么移除X-Frame-Options?
> 经过 Chrome71 测试, 当 X-Frame-Options 和 Content-Security-Policy 同时设置， 前者依然作用。

*settings.py*

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # remove this middleware 'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```

然后在 nginx 增加， CSP 相关的 Header. 依然是 add\_header .


```nginx
add_header Content-Security-Policy frame-ancestors <my uri>;
```

以上, 目前 CSP 正在逐渐取代 X-Frame-Options 。 而 X-Frame-Options 将被弃用. 相信在以后的迭代里， Django 将会默认支持 CSP 的控制. 但在目前(2018-12-18)的时间里， 上面的方法可能对你有帮助.
