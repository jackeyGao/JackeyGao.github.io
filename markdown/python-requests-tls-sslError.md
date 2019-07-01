title: requests 的Certificate did not match错误
date: 2019-01-22 10:19:31
---

![Security](/uploads/images/requests-ca-did-not-match.jpeg "cover")

最近在 Django 后端对接其他系统时遇到一个 SSL 的错误， 是 HTTPS 协议的接口， 我使用的是 Python 的 requests 库， 进行 HTTP 数据交换. 以下是错误的详细:

```
connection [ERROR] Certificate did not match expected hostname: 10.0.0.6. Certificate: {'crlDistributionPoints': (u'http://crl.comodoca.com/COMODORSADomainValidationSecureServerCA.crl',), 'subjectAltName': (('DNS', '*.example.com'), ('DNS', 'example.com')), 'notBefore': u'Aug  9 00:00:00 2017 GMT', 'caIssuers': (u'http://crt.comodoca.com/COMODORSADomainValidationSecureServerCA.crt',), 'OCSP': (u'http://ocsp.comodoca.com',), 'serialNumber': u'EF82BAF0A699ACFBC0E5E149E34566EB', 'notAfter': 'Aug  8 23:59:59 2020 GMT', 'version': 3L, 'subject': ((('organizationalUnitName', u'Domain Control Validated'),), (('organizationalUnitName', u'EssentialSSL Wildcard'),), (('commonName', u'*.example.com'),)), 'issuer': ((('countryName', u'GB'),), (('stateOrProvinceName', u'Greater Manchester'),), (('localityName', u'Salford'),), (('organizationName', u'COMODO CA Limited'),), (('commonName', u'COMODO RSA Domain Validation Secure Server CA'),))}
```

## "hostname doesn't match" 错误是怎么回事？

当 SSL certificate verification 发现服务器响应的认证和它认为自己连接的主机名不匹配时，就会发生这样的错误。如果你确定服务器的 SSL 设置是正确的（例如你可以用浏览器访问页面），而且你使用的是 Python 2.6 或者 2.7，那么一个可能的解释就是你需要 Server-Name-Indication。

Server-Name-Indication 简称 SNI，是一个 SSL 的官方扩展，其中客户端会告诉服务器它连接了哪个主机名。当服务器使用虚拟主机（ Virtual Hosting）时这点很重要。这样的服务器会服务多个 SSL 网站，所以它们需要能够针对客户端连接的主机名返回正确的证书。

Python 3 和 Python 2.7.9+ 的 SSL 模块包含了原生的 SNI 支持。

## requests 为什么会发生这个错误?

一般来说， 服务器端使用的可能是私有证书， 才会导致这种情况。Requests 默认附带了一套它信任的根证书，来自于 Mozilla trust store。然而它们在每次 Requests 更新时才会更新。这意味着如果你固定使用某一版本的 Requests，你的证书有可能已经 太旧了。 

所以当私有证书， 或者证书太久了， 都会导致证书验证失败。

Requests 可以为 HTTPS 请求验证 SSL 证书，就像 web 浏览器一样。SSL 验证默认是开启的，如果证书验证失败，Requests 会抛出 SSLError:

```python
>>> requests.get('https://requestb.in')
requests.exceptions.SSLError: hostname 'requestb.in' doesn't match either of '*.herokuapp.com', 'herokuapp.com'
```

在该域名上我没有设置 SSL，所以失败了。但 Github 设置了 SSL:

```python
>>> requests.get('https://github.com', verify=True)
<Response [200]>
```

## 怎么避免？

### 指定 CA 证书方式.

你可以为 verify 传入 CA\_BUNDLE 文件的路径，或者包含可信任 CA 证书文件的文件夹路径：

```python
>>> requests.get('https://github.com', verify='/path/to/certfile')
```

在 Session 中可以设置verify 属性.

```python
s = requests.Session()
s.verify = '/path/to/certfile'
```

>%warning 你还可以通过 REQUESTS\_CA\_BUNDLE 环境变量定义可信任 CA 列表。


### 忽略对 SSL 证书的验证

如果你将 verify 设置为 False，Requests 也能忽略对 SSL 证书的验证。

```
>>> requests.get('https://kennethreitz.org', verify=False)
<Response [200]>
```

默认情况下， verify 是设置为 True 的。选项 verify 仅应用于主机证书。

对于私有证书，你也可以传递一个 CA\_BUNDLE 文件的路径给 verify。你也可以设置 REQUEST\_CA\_BUNDLE 环境变量。

## 其他

从 Requests 2.4.0 版之后，如果系统中装了 certifi 包，Requests 会试图使用它里边的 证书。这样用户就可以在不修改代码的情况下更新他们的可信任证书。为了安全起见，我们建议你经常更新 certifi！


