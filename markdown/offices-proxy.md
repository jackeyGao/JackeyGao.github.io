title: 企业级翻墙方案
date: 2015-11-06 15:53:27
tags:
  - vps
  - 翻墙
  - Squid
  - Stunnel
---

为了公司内一些技术员工的要求访问google查资料, 公司准备采购国外vps来建设内部翻墙方案.利用公司内部的认证系统（Open LDAP）来进行账号授权。然后通过PAC文件进行网站过滤.


## 准备工作

**服务器**

* 自由网络的VPS若干, 以下简称VPS.
* LDAP 服务, 认证服务器
* 内部分流机器, 以下简称分流机器
* 提供PAC服务机器(HTTP服务), 可以和分流服务器共用

**开源软件**

* Squid
* Stunnel


## 思考工作

首先要考虑加密工作, 随着墙的升级, 越来越多的手段都被禁止或者被干扰. 所以加密一定要做的， 这里采用了Stunnel进行加密.其次是网站过滤,虽然一些技术人员不会关注政治黑暗， 但一些视频娱乐网站也是要控制的.这里用PAC文件来控制， 有些人懂一些网络基础直接连接端口进行全局proxy也不是不可能的。 这个地方可以通过squid的ACL来控制.关于ACL本文不会描述 ， 请自行查阅squid文档.

**所以**

* 加密 (保证在公网使用ssl加密)
* 控制 (这个看需求了, 最好控制youtube等无用的大流量网站)

**大概的路线**

**Client** <~localnetl~> **PAC** <~localnetl~> **分流Stunnel** <~internet~> **VPSStunnel** <~vps net~> **Squid** <~internet~> **目标服务器**


## 安装操作

参考这里: http://fuweiyi.com/others/2014/05/15/a-Centos-Squid-Stunnel-proxy.html

我说明下和ldap关联集中认证.首先调通 

```bash
$ /usr/lib64/squid/squid_ldap_auth -u -cn -f "uid=%s" -b "ou=people,dc=example,dc=com" -D "cn=squid,ou=people,dc=example,dc=com" -w "认证密码"  -H ldap://ldap.example.com
$username $password # 这里输入测试认证的用户名 空格 密码
OK #这里是ok才是正常
```

然后修改squid配置文件

```bash
vim /etc/squid/squid.conf

增加下面代码.

...
auth_param basic program /usr/lib64/squid/squid_ldap_auth -u -cn -f "uid=%s" -b "ou=people,dc=example,dc=com" -D "cn=squid,ou=people,dc=example,dc=com" -w "xxxxxx"  -H ldap://ldap.example.com
#auth_param basic realm Internet Proxy
auth_param basic credentialsttl 1 minute
acl ldapauth proxy_auth REQUIRED # 定义ldap认证后的acl，直接转发
http_access allow ldapauth # 允许ldapauth认证过的
http_access deny all # 其他拒绝

...
```

> squid_ldap_auth 这个工具是squid程序里面的， 地址可能不是我上面指定的 ， 因为我是yum安装的。 如果是编译安装应该是prefix里面找. 如果没有生效可以通过这个命令进行测试， 具体可以man squid_ldap_auth 查看EXAMPLE里面的介绍. 如果还不行可能是编译没有开启ldap. 这个需要开启， 网上有大量的文档说明开启ldap.



然后安装[文档](http://fuweiyi.com/others/2014/05/15/a-Centos-Squid-Stunnel-proxy.html)继续装剩下的。

## 关于PAC

PAC文件可以通过[Genpac](https://github.com/JinnLynn/GenPAC)生成. 然后使用**PAC服务机器**起个http服务， 让员工通过一个内网地址访问到就行。 这样只有上班实践可以使用翻墙.

## 关于拓展

多个vps 可以启动多个squid和stunnel服务, 客户端起多个stunnel端口即可.







