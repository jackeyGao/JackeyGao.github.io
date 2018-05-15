title: Hyper shadowsocks完全教程
date: 2016-08-15 14:11:01
tags: 
- Docker
- shadowsocks
- 翻墙
---

## 什么是Hyper?

>  Hyper是一个可以在hypervisor上，不安装完整操作系统，直接运行Docker Image的运行引擎。Hyper可以在hypervisor上运行一组相关的Docker Image，而不是一个，也正是Kubernetes所阐述的Pod的概念——不是一个虚机，不是一个胖容器，而是一组关联的容器。再进一步说，Hyper致力于成为一个平台中立、hypervisor中立的执行引擎，除了支持KVM/QEMU外，接下来Hyper还将会支持Xen。

## 三步获得一个翻墙应用

### 1. 注册

hyper现在正在推广优惠, 使用下面我的分享链接注册可以多获得$10, 加上原有的$20就是$30. 这些够用一段时间了.

> [推广链接](https://console.hyper.sh/register/invite/aMwQqQG655h2K7M2YwMxFywwyd8l96u2)

注册后绑定信用卡才会赠送$30, 之后可以生成API凭证(此步骤必须绑定一个可用的信用卡), 通过web端[Account-Credential](https://console.hyper.sh/account/credential)就可以生成, 生成后保存后面`cli`需要用到.

这里以shadowsocks服务为例，计算价格, 一个shadowsocks需要一个容器和一个ip.

![容器价格表](/uploads/images/hyper-container-pricing.png "容器价格表")
![Floating IP价格](/uploads/images/hyper-network-pricing.png "Floating IP价格")

shadowsocks 可以使用最小规格的容器, 也就是**$1.03/month**, ip为**$1/month**， 所有一个月最少需要$2左右(但可以用).


### 2. 安装cli

```bash
$ curl -O https://hyper-install.s3.amazonaws.com/hyper-mac.bin.zip
$ unzip hyper-mac.bin.zip 
$ chmod +x hyper
$ ./hyper --help
```

### 3. 配置ss

要使用hyper cli首先要指定凭证通过认证. Access Key和Secret Key在注册过程中获取, 上面已经提过. 

```bash
./hyper config
Enter Access Key: xxxxxxxxxxxxxxx
Enter Secret Key: xxxxxxxxxxxxxxxxxxxxxxxxxx
```

然后后面的类似与Docker启动一个应用来开启shadowsocks服务

```bash
$ ./hyper pull oddrationale/docker-shadowsocks
Using default tag: latest
latest: Pulling from oddrationale/docker-shadowsocks
012a7829fd3f: Pull complete
41158247dd50: Pull complete
916b974d99af: Pull complete
a3ed95caeb02: Pull complete
95b198eff4ae: Pull complete
001c5b5b7517: Pull complete
Digest: sha256:221070b8688f049fa791528e1e9c5fc0c027f12a858d22b540170c2cca1dec69
Status: Image is up to date for oddrationale/docker-shadowsocks:latest

$ ./hyper run -d --name shadowsocks -p 1989 oddrationale/docker-shadowsocks -s 0.0.0.0 -p 1989 -k MyPassWord -m aes-256-cfb
b6cae93b056ddb123dcb754e785c557bee9b080e4a3a4731f3e1cd97798fe058

$ ./hyper ps
CONTAINER ID        IMAGE                             COMMAND                  CREATED             STATUS              PORTS               NAMES               PUBLIC IP
b6cae93b056d        oddrationale/docker-shadowsocks   "/usr/local/bin/ssser"   23 seconds ago      Up 18 seconds                           shadowsocks         

$ ./hyper fip allocate 1
162.221.195.201

$ hyper fip attach 162.221.195.201 shadowsocks # 指定上面命令输出的ip

```

到此结束,然后shadowsocks 客户端通过服务端配置指定

