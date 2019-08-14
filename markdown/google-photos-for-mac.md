title: Google photos for MAC使用教程
date: 2016-04-12 11:41:17
tags: 
- 翻墙
- 病
- Google
---


Google photos 是谷歌推出了一个独立的无限相片 / 视频存放服务。使用者可以免费存放无限量相片和视频至云端，唯其大小限于最大 16MP 和 1080p。而且客户端可以设置是否对图片进行压缩， 所以大的图片也不会占用google drive的空间。

安卓手机上面使用shadowsocks 可以正常登陆和备份照片 ， 此处略。

但是mac 上使用shadowsocks是不行的， 貌似有一些连接不支持socks协议。就在刚刚折腾了VPN死活出错， 最后放弃。 于是又折腾了hosts， 这个比较好弄。

首先获取最新hosts文件， 向维护作者致敬

```bash
git clone https://github.com/racaljk/hosts
```

然后追加到/etc/hosts文件

```bash
# 需要root权限, 第一步请输入提权密码。 
sudo $SHELL
cat hosts/hosts >> /etc/hosts
exit
```


