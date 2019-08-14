title: 终端操作(SHELL)技巧
date: 2018-11-29 11:34:27
---

![](/uploads/images/shell-tips.jpeg "cover")


本篇是一些小但是有用的终端操作技巧和一些快捷方式，可以让你在 linux 命令行有出奇的效率。一方面这些技巧可以让你的效率有所提高， 但有时候也会有隐患， 所以终端操作一定要注意高风险的行为， 每一步也都要小心的执行。

当然我相信你也有祖传的小技巧， 自己偷偷的使用， 希望你也能通过留言评论， 分享给大家。


## 0.使用 Tab 键补齐.

如果一个命令， 或者命令参数很长， 并且命令支持补全操作， 那么通过 Tab 键可以很方便的自动补全后面的参数。 当你在命令行键入内容的时候，可以按 Tab 键来显示可能的后面需要补齐的选项, 你可以根据这些选项来进一步操作。

一般执行一个命令， 命令可以补齐， 参数也可以补齐，一个命令操作一般连续按下多次 Tab 键才能完成输入， 最后确保没有问题的时候回车执行。 

这个技巧可以让我们不需要死记硬背所有的命令和参数， 你只需要知道命令大概的名字和作用即可。

```shell
$ cd m[按下Tab]
my-test-directory-00001    my-test-directory-00002    my-test-directory-00003
my-test-directory-00004    main.py

$ cd my[按下Tab]
$ cd my-test-direction-0000[按下Tab]
my-test-directory-00001    my-test-directory-00002    my-test-directory-00003
my-test-directory-00004
```


## 1.回到上一个工作目录

假设你要在一个目录中工作， 但是你需要到其他的目录处理一个小的问题， 处理完后你可以快速的回到工作目录中. 这是一个非常常用的技巧.

```shell
$ pwd
/Users/jackeygao/Coding
$ cd ~/Downloads
$ pwd
/Users/jackeygao/Downloads
$ cd -
~/Coding
$ pwd
/Users/jackeygao/Coding
```

## 2.回到主目录

无论你在任何位置， 你可以通过下面命令快速回到用户目录.

```shell
cd ~
```

or 

```shell
cd 
```

## 3.一行执行多个命令

多个语句可以通过';'分割

```shell
$ echo Hello; echo World; echo '.';
Hello
World
.
```

## 4.一行执行多个命令 (只有上一句执行成功才执行)

比较类似于链式操作， 但需要保证上一句的结果. SHELL 语言没有好的异常停止机制， 所以你必须显式的控制语句.  和上面有区别的是， 可以通过&&串联多个语句， 来保证所有语句必须在上一次执行成功才能这执行. 下面例子中如果 python-devel 已经安装， echo "no"不会执行. 

```shell
$ rpm -qa | grep python-devel &> /dev/null && echo "ok" || echo "no"
ok
```

在 shell 中， 执行成功或者成功的完成了某个命令(比如grep的匹配)返回码用0表示, 失败或者没有完成某个命令的逻辑则用非0表示. 

- && 表示上一句返回码0才会执行
- || 表示上一句返回码非0才会执行
- ; 无论如何都执行

关于返回码, 你可以需要进一步的了解[https://www.shellscript.sh/exitcodes.html](https://www.shellscript.sh/exitcodes.html).


## 5.搜索并执行历史命令

通过搜索历史命令， 可以很轻松的对历史命令进行复用。 一般很多 SHELL 程序都支持历史命令搜索.

```shell
Ctrl + R   然后 键入关键字
```

```shell
$ docker run --rm -i -p 8001:8001 -t nova python manage.py runserver 0.0.0.0:8001
bck-i-search: docker run       < 在这个提示符输入关键字(通过 Ctrl + R快捷键调出)
```

## 6.解锁你的终端

如果你不小心按到了 Ctrl + S , 那么你会得到一个『冻僵』(只是暂停(Stop)了)的终端 ， 好像和死了一样。 而 Ctrl + S 是一般保存文档的快捷键， 这在和 vim 命令编辑文件的时候经常遇到的事情， 不要慌可以通过Ctrl + Q快捷键解冻. 


## 7. 移动到行首或行尾

如下图， 如果我输入一个长的命令， 输入到最后在执行前我发现了问题， 需要在行首增加 sudo 。 这时我可以使用 Ctrl  + A移动光标到行首.

![](/uploads/images/move-to-first-and-move-to-end.jpeg)

## 8. 删除一个单词

默认通过 退格键 可以删除一个字符, 但如果我的命令很长， 删除操作就会很慢。 可以通过 Esc + 退格键(Backspace) 来删除一个单词(以空格, 符号分割区分).


## 9. 使用上个命令的最后参数

这个是很常见的场景， 比如我们创建一个目录， 一般紧接着就进到这个空目录操作了. 虽然可以补全操作， 但有一种更简单的方法，你也应该知道， 这会让你显得很酷。 就是组合快捷键[ESC + .], .号就是英文状态下的句号. 也可以通过`!$`.

```shell
$ mkdir my-test-directory-00001
mkdir: test: File exists
$ cd [按下EST + .] my-test-directory-00001

方法二:

$ cd !$
$ cd  my-test-directory-00001
```


## 10. 使用上一个命令

和上面不同的是， 这个操作是直接使用上一个命令， 而不是最后一个参数.

假如我需要安装一个包, 执行完毕后发现需要 root用户才可以安装， 这时我需要在前面加sudo。 请谨慎使用这个.

```shell
$ yum -y install nginx
permission denied

$ sudo !!
sudo yum -y install nginx
Loaded plugins: fastestmirror
....
```

## 11.xargs 

这是一个魔法命令， 希望你去研究并学会它.

[main xargs](http://man7.org/linux/man-pages/man1/xargs.1.html)


## 12.使用 Python 替代你的 Shell.

前面已经说到， SHELL 没有严谨的异常处理. 如果有自动脚本， 这让服务器运维增加风险属性。 小的脚本还好， 一旦脚本迭代了几个需求，臃肿复杂而且维护性极差， 甚至会非常不安全。 我推荐你使用高级语言来替代 SHELL。 推荐 Python， Ruby 等解释性语言. 大多数系统都自带了 Python, 这对我们对脚本打包提供便利.


以上 : )

