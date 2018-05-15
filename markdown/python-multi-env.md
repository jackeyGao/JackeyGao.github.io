title: Centos 6.x 共存安装Python 2.7 or 3.x
date: 2016-04-21 14:46:16
tags: 
- Centos
- Python
- virtualenvwrapper
- 折腾
- virtualenv
---

由于yum命令依赖系统的python2.6， 所以如果直接覆盖的话，会导致yum不能工作。 所以自带的python 2.6绝对不能动。 不过可以通过自定义安装来共存两套或多套python环境。 再配合virtualenv 隔离项目环境.


这里演示安装Python2.7 :

**首先安装系统依赖包**

```bash
yum install zlib-devel
yum install bzip2-devel
yum install openssl-devel
yum install ncurses-devel
yum install sqlite-devel
```

**下载Python2.7 源码编译安装**

```bash
cd /usr/local/src;
wget --no-check-certificate https://www.python.org/ftp/python/2.7.11/Python-2.7.11.tar.xz
tar xf Python-2.7.11.tar.xz
cd Python-2.7.11
./configure --prefix=/usr/local/python27
make && make install
```

**安装pip**

使用python27安装pip

```bash
 wget https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py
/usr/local/python27/bin/python ez_setup.py
/usr/local/python27/bin/easy_install pip
```

到这里python2.7.11 和 pip套件都安装了可以使用了。 下一步就是把`/usr/local/python27/bin/` 加入`$PATH`变量。


### 安装virtualenvwrapper 

这一步实在自带的python2.6 上执行的， 所以如果用python 2.7 需要再创建的虚拟环境的时候指定

```bash
pip install virtualenvwrapper
```

然后再`~/.bashrc`文件追加以下操作

`~/.bashrc` or `./zshrc`
```bash
source $(which virtualenvwrapper.sh)
```

然后`source ~/.bashrc` 这样就可以使用`workon`、 `mkvirtualenv`、 `rmvirtualenv`命令.具体的指南参考 [virtualenvwrapper](https://virtualenvwrapper.readthedocs.org/en/latest/command_ref.html)

创建基于Python 2.7 的虚拟环境

```bash
mkvirtualenv ansible -p /usr/local/python2.7.11/bin/python
```

### 错误处理

第一个错误,  `source $(which virtualenvwrapper.sh)`出现`logging no NullHandler`

```python
Traceback (most recent call last):
  File "/usr/lib64/python2.6/runpy.py", line 122, in _run_module_as_main
    "__main__", fname, loader, pkg_name)
  File "/usr/lib64/python2.6/runpy.py", line 34, in _run_code
    exec code in run_globals
  File "/usr/lib/python2.6/site-packages/virtualenvwrapper/hook_loader.py", line 16, in <module>
    from stevedore import ExtensionManager
  File "/usr/lib/python2.6/site-packages/stevedore/__init__.py", line 23, in <module>
    LOG.addHandler(logging.NullHandler())
AttributeError: 'module' object has no attribute 'NullHandler'
virtualenvwrapper.sh: There was a problem running the initialization hooks.

If Python could not import the module virtualenvwrapper.hook_loader,
check that virtualenvwrapper has been installed for
VIRTUALENVWRAPPER_PYTHON=/usr/bin/python and that PATH is
```

处理方法, 升级stevedore

```python
pip install stevedore
```
`python 2.6.6` 可以升级到1.3.0 就可以了.

