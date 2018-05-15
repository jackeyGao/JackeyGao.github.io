title: 使用 python-jenkins 执行脚本返回为空
date: 2018-05-10 11:01:11
---


最近在做一个发布系统的整合， 使用到 Jenkins API的 Python 的 python-jenkins 的包.

但是在调用 `server.run_script` 死活不工作， 最终在源码中找到问题所在.

修改下 POST 的数据格式可以通过， 具体问题暂时不清楚， 可以由于版本升级导致.

原有的 `run_script` 方法


```python

class Jenkins:
   def run_script(self, script):
        '''Execute a groovy script on the jenkins master.

        :param script: The groovy script, ``string``
        :returns: The result of the script run.

        Example::
            >>> info = server.run_script("println(Jenkins.instance.pluginManager.plugins)")
            >>> print(info)
            u'[Plugin:windows-slaves, Plugin:ssh-slaves, Plugin:translation,
            Plugin:cvs, Plugin:nodelabelparameter, Plugin:external-monitor-job,
            Plugin:mailer, Plugin:jquery, Plugin:antisamy-markup-formatter,
            Plugin:maven-plugin, Plugin:pam-auth]'
        '''
        return self.jenkins_open(
            requests.Request(
                'POST', self._build_url(SCRIPT_TEXT),
                data="script=".encode('utf-8') + quote(script).encode('utf-8')))

```

修改后的方法

```python
from jenkins import Jenkins, requests, quote, SCRIPT_TEXT

class TeambitionJenkins(Jenkins):

    def console(self, script):
        return self.jenkins_open(requests.Request(
                'POST', self._build_url(SCRIPT_TEXT),
                data={'script': script}))

```
