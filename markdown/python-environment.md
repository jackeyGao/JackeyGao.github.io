title: Python生态圈
categories:
  - Python
date: 2015-11-26 14:33:53
tags:
  - Python
  - virtualenv
  - pip
---

## 版本

* python2.6(不推荐)
* python2.7
* python3.0(强力推荐)

## PYTHONPATH变量

`PYTHONPATH`是一个可以用来增强默认包检索路径的环境变量

```bash
export PYTHONPATH=/path/to/some/directory:/path/to/another/directory:/path/to/yet/another/directory
```

在某些情况下，你不用覆盖已有的PYTHONPATH，只需要在开头或结尾加上新的路径即可。

```bash
export PYTHONPATH=$PYTHONPATH:/path/to/some/directory    # 追加
export PYTHONPATH=/path/to/some/directory:$PYTHONPATH    # 覆盖
```

同时在python代码里面也可以使用`sys.path.insert`来动态添加搜索路径. 无论是通过环境变量`PYTHONPATH`还是通过`sys.path.insert`都不建议你这样做. 按照python规范好的路径来开发不然维护性要加大.

## 第三方包

在Linux系统上，至少有3种安装第三方包的方法。

* 使用系统本身自带的包管理器（deb, rpm等）
* 通过社区开发的类似pip, easy_install等多种工具
* 从源文件安装

三种方法都会安装所需的依赖包, 并处理好依赖程序, 同时遵守python的搜索路径.

### 如果找到合适的包

* 你使用的系统自带的包管理器
* [Python包索引（也被称为PyPI）](http://pypi.python.org/pypi)
* 源码托管服务，如Launchpad， Github， Bitbucket等。
* 必要时候进行搜索

### 非root pip安装权限问题

当没有root权限是不能在系统层面安装python包的, 这时候可以采取**虚拟环境的方式**或者加入`--user`参数。

默认python的搜索路径里有宿主目录下的`~/.local/lib/python2.7/site-packages`目录, `--user`参数的作用也就是安装到这个路径里面.

```python
>>> import sys
>>> print(sys.path)
['', '/home/monitor/.local/lib/python2.7/site-packages', ...略..]
```

当然也可以在root环境下安装`virtualenv` 下节讲

## virtualenv 虚拟环境

Python社区中设置开发环境的最受欢迎的方法，是通过virtualenv。Virtualenv是一个用于创建孤立Python环境的工具。那么现在问题来了：为什么我们需要孤立的Python环境？要回答这个问题，请允许我引用virtualenv的官方文档。

> 我们要解决的问题之一，就是依赖包和版本的管理问题，以及间接地解决权限问题。假设你有一个应用需要使用LibFoo V1，但是另一个应用需要V2。那么你如何使用两个应用呢？如果你把需要的包都安装在/usr/lib/python2.7/site-packages（或是你的系统默认路径），很容易就出现你不小心更新了不应该更新的应用。

简单来说，你的每一个项目都可以拥有一个单独的、孤立的Python环境；你可以把所需的包安装到各自孤立的环境中。

```bash
sudo pip install virtualenv
```

```bash
$ mkdir my_env
$ cd my_env/
$ virtualenv .
New python executable in ./bin/python
Installing setuptools, pip...done.
$ ls -al
总用量 20
drwxrwxr-x  5 monitor monitor 4096 11月 26 13:56 .
drwx------ 10 monitor monitor 4096 11月 26 13:56 ..
drwxrwxr-x  2 monitor monitor 4096 11月 26 13:56 bin
drwxrwxr-x  2 monitor monitor 4096 11月 26 13:56 include
drwxrwxr-x  3 monitor monitor 4096 11月 26 13:56 lib
lrwxrwxrwx  1 monitor monitor    3 11月 26 13:56 lib64 -> lib
```

### 进入虚拟环境

进入环境后终端的提示符, 会有关于所在虚拟环境的标示, 这里我的标示就是`my_env`

```bash
[monitor@localhost]$ source bin/activate
(my_env)[monitor@localhost]$ 
```

到了这里， 使用pip安装都会安装到`./lib/python2.7/site-packages/`里面， 可以看下我们使用的pip命令和python命令位置, 已经完全和系统的python环境分离. 甚至可以看到python的搜索路径.

```bash
(my_env)[monitor@localhost]$ which pip
~/my_env/bin/pip 
(my_env)[monitor@localhost]$ which python
~/my_env/bin/python
```

```python
>>> import sys
>>> sys.path
['', '/home/monitor/my_env/lib64/python27.zip', '/home/monitor/my_env/lib64/python2.7', '/home/monitor/my_env/lib64/python2.7/plat-linux2', '/home/monitor/my_env/lib64/python2.7/lib-tk', '/home/monitor/my_env/lib64/python2.7/lib-old', '/home/monitor/my_env/lib64/python2.7/lib-dynload', '/usr/lib64/python2.7', '/usr/lib/python2.7', '/home/monitor/my_env/lib/python2.7/site-packages']
>>>
```

### 退出虚拟环境

如果需要回到系统环境

```bash
(my_env)[monitor@localhost]$ deactivate
[monitor@localhost]$ 
```

### 默认虚拟环境里面可以使用系统环境的包

**注意:**系统Python环境中安装的所有包，默认是可以在虚拟环境中调用的。这意味着，如果你在系统环境中安装了simplejson包，那么所有的虚拟环境将自动获得这个包的地址。你可以在创建虚拟环境时，通过添加`--no-site-packages`选项，取消这个行为，就像这样：

```bash
[monitor@localhost]$ virtualenv . --no-site-packages
```

### virtualenvwrapper 

`virtualenvwrapper`是virtualenv 封装后的工具集

**安装**

```bash
[monitor@localhost]$ sudo pip install virtualenvwrapper
```

安装后此工具提供这个bash 方法文件

```text
virtualenvwrapper                            virtualenvwrapper_setup_tab_completion
virtualenvwrapper_absolutepath               virtualenvwrapper.sh
virtualenvwrapper_cd                         virtualenvwrapper_show_workon_options
virtualenvwrapper_derive_workon_home         virtualenvwrapper_tempfile
virtualenvwrapper_expandpath                 virtualenvwrapper_verify_active_environment
virtualenvwrapper_get_python_version         virtualenvwrapper_verify_project_home
virtualenvwrapper_get_site_packages_dir      virtualenvwrapper_verify_resource
virtualenvwrapper_initialize                 virtualenvwrapper_verify_virtualenv
virtualenvwrapper_lazy.sh                    virtualenvwrapper_verify_virtualenv_clone
virtualenvwrapper_mkproject_help             virtualenvwrapper_verify_workon_environment
virtualenvwrapper_mktemp                     virtualenvwrapper_verify_workon_home
virtualenvwrapper_mkvirtualenv_help          virtualenvwrapper_workon_help
virtualenvwrapper_run_hook
```

其实需要用到的就一个`virtualenvwrapper.sh`，  所有封装好的工具都是此bash脚本里面的函数, 所以我们要使用必须要`source`加载一下,找到它的位置, 加到` ~/.bashrc` 里面每次进入系统自动加载. 

```bash
echo -e "\n# 加载虚拟环境工具集\nsource $(which virtualenvwrapper.sh)\n\n" >> ~/.bashrc
```

这样只要每次登陆系统就可以使用里面的工具集了, 这里说下`virtualenvwrapper`提供了哪些方法.

```bash
# 创建虚拟环境
mkvirtualenv my_env

# 进入虚拟环境
workon my_env

# 退出虚拟环境
deactivate

# 删除虚拟环境
rmvirtualenv my_env
```

**注意:**`mkvirtualenv`同时支持`virtualenv`参数， 所以前面讲的`--user`和`--no-site-packages`参数同时也会支持, 看到这里相信你知道这个工具只是对`virtualenv`做了封装了吧, 所以最好每次只需要安装`virtualenvwrapper`就行了， 依赖包`virtualenv`会自动安装.

## 通过pip和virtualenv进行基本的依赖包管理

virtualenv虚拟环境的确是开发环境的好东西， 但是不只是仅仅开发环境， 线上部署多应用的时候同样需要多虚拟环境同时存在. 如果我们在虚拟环境开发完了， 可以直接把依赖的包提取出来， 也就是打包的范畴了.   Python项目里都存在一个`requirements.txt`文件， 好像成了标准规范. 幸运的是`pip freeze`命令支持直接生成.

```bash
(my_env)[monitor@localhost]$ pip freeze > requirements.txt
```

## 编辑器推荐

个人比较倾向vim， 还有支持自动补全的 PyCharm， 你应该选择最合适的编辑器.


