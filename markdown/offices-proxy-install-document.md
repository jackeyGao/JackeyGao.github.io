title: 企业级翻墙服务部署文档
date: 2016-04-13 10:35:45
tags: 
- Squid
- Stunnel
- vps
- 翻墙
---

写在前面, 翻墙后仅资料查询或学术研究. 之前有说过翻墙方案： [企业级翻墙方案](/2015/11/06/offices-proxy/)

## 思考工作

翻墙主要的技术有VPN和代理， 但是VPN在去年政策出了后正常使用需要备案， 所以VPN肯定是不推荐。 其次是代理， 个人代理最多用的是shadowsocks, shadowsocks不支持集中认证， 所以不考虑. squid支持ldap集中认证， 但是要考虑加密工作, 随着墙的升级, 越来越多的手段都被禁止或者被干扰. 所以加密一定要做的， 这里采用了Stunnel进行加密.其次是网站过滤, 一些视频网站控制住. 这里用PAC文件来控制， 有些人懂一些网络基础直接连接端口进行全局proxy也不是不可能的。 这个地方可以通过squid的ACL来控制.关于ACL本文不会描述 ， 请自行查阅squid文档.

## 环境

**硬件环境**

- 墙外VPS 若干(国外需要网络自由)
- 墙内VPS (Stunnel分流机器, 带宽要足够)

**软件环境**

- `Squid` 是一种用来缓冲Internet数据的软件。在这里仅仅使用它的代理功能.
- `Stunnel` 是一个自由的跨平台软件，用于提供全局的`TLS/SSL`服务。针对本身无法进行TLS或SSL通信的客户端及服务器，Stunnel可提供安全的加密连接。这里我们在墙内VPS和墙外VPS中间通信中间加个加密通道， 所以需要双向安装， 墙外的为服务端墙内分流为客户端.
- `LDAP Server`（这里没有安装介绍）

## 安装

### 墙外VPS

**墙外VPS**需要安装Stunnel 服务端和Squid服务端.

```bash
$ yum -y install stunnel 
$ yum -y install squid
```

####  配置stunnel - 生成pem  

**pem可以生成一份， 所有机器通用**

```bash
$ cd /etc/stunnel/;
$ openssl req -new -x509 -days 365 -nodes -out stunnel.pem -keyout stunnel.pem

# 接着给它生成Diffie-Hellman部分
$ openssl gendh 512>> stunnel.pem
```

#### 配置stunnel -  配置Stunnel.conf

配置文件: `/etc/stunnel/stunnel.conf`

```text
cert = /etc/stunnel/stunnel.pem
CAfile = /etc/stunnel/stunnel.pem
socket = l:TCP_NODELAY=1
socket = r:TCP_NODELAY=1

pid = /tmp/stunnel.pid
verify = 3


setuid = stunnel
setgid = stunnel

compression = zlib
delay = no
sslVersion = TLSv1
fips=no

debug = 7
syslog = no
output = stunnel.log

[sproxy]
accept = 34567
connect = 127.0.0.1:10801
```

以上这是stunnel 服务端的配置， cert、CAfile指定刚刚生成的pem， 后面的[sproxy] 可以指定一组对应，sproxy可以多个， 单服务端不需要一台机器只有一个squid所以只写一组. accept 表示转发的端口， connect表示映射端口， 也就是squid的端口这里是10801， 默认为3128.

#### 启动

```bash
$ service squid start
$ stunnel
```


### 配置squid - 配置squid.conf

```text
... 以下为修改， 也可以不修改， 选择默认， 上面的connect需要写成3128
http_port 10801

... 以下为添加
auth_param basic program /usr/lib64/squid/squid_ldap_auth -u -cn -f "uid=%s" -b "ou=people,dc=shuyun,dc=com" -D "cn=proxy proxy,ou=people,dc=shuyun,dc=com" -w "Shuyun123456"  -H ldap://ldap.shuyun.com   # ldap 配置
auth_param basic realm Please enter the wiki user and password ＃ 认证提示
auth_param basic credentialsttl 8 hours ＃ 认证过期时间
auth_param basic casesensitive off   
acl ldapauth proxy_auth REQUIRED
http_access allow ldapauth ＃ 默认允许ldap认证过的
http_access deny all ＃ 拒绝其他所有
acl rejectfile  urlpath_regex -i \.avi$ \.rmvb$ \.wmv$ \.rm$ \.mpg$ \.mpeg$ \.mp4$ \.mov$ \.asf$ \.mkv$ \.dat$ \.flv$ \.3gp$ \.mp3$
http_access deny rejectfile ＃ 拒绝视频文件
```

**注意:**  http_access 语句配置完成后应该只有上面的三个， 安装**Squid默认的配置文件里面的http_access 语句需要注视掉**， 否则ldapauth 会不生效， 因为默认是没有认证的。`http_access allow all` 这一句就允许所有了...

**注意:**  如果有多台墙外VPS的话重复上面的步骤, pem 可以直接复制到备份机器. 下面stunnel client可以复制这个pem.

到这里服务端的配置就完成了， 下面开始分流机器的配置

### 墙内分流VPS

**墙内分流VPS**需要安装Stunnel 软件作为客户端.


```bash
$ yum -y install stunnel
```

### 配置Stunnel - 复制pem

复制刚刚生成pem那台服务器的pem文件

```bash
$ scp root@$墙外VPS:/etc/stunnel/stunnel.pem /etc/stunnel/stunnel.pem
```

### 配置Stunnel - 配置stunnel.conf

配置文件: `/etc/stunnel/stunnel.conf`

```
cert = /etc/stunnel/stunnel.pem
CAfile = /etc/stunnel/stunnel.pem
socket = l:TCP_NODELAY=1
socket = r:TCP_NODELAY=1
verify = 2
client=yes  # 这里指明当前服务为客户端， 默认是服务端(no).
compression = zlib
ciphers = AES256-SHA
delay = no
failover = prio
sslVersion = TLSv1
fips = no
debug = debug

[sproxy2]
accept  = 0.0.0.0:7072
connect = $墙内vps1:34567

[sproxy2]
accept  = 0.0.0.0:7073
connect = $墙内vps2:34567
```

#### 启动

```bash
$ stunnel
```

这里所有的配置均已完成， 测试的话，可以在浏览器设置里面设置

Windows: windows键+R键输入inetcpl.cpl > 连接 > 局域网设置 > 代理服务器
MAC: 系统设置 > 网络 > <选择所用网络> > 高级 > 代理 > WEB 代理(HTTP) > 输入地址端口用户名密码.
