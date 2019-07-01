title: Paramiko实时输出stdout,stderr
date: 2018-09-04 17:01:11
---

![SSH](/uploads/images/ssh.png "cover")

Python 执行远程主机可以使用 paramiko 框架，但 paramiko 框架的 `exec_command` 方法， 默认是没有开启 bufsize 的， 也就是说必须等到一个命令执行完， 我们才可以打印到命令的输出信息， 但为了体验更接近在终端执行的感觉， 实时输出就很有必要了。我这里的需求是 websockets 实时输出远程命令的日志信息，所以我只需要定义 command 和下面的 callback 函数就可以了。

Paramiko 的 `exec_command` 方法提供了 `bufsize` 参数， 我们可以调小缓冲区， 然后使程序更快的打满缓冲区生成缓冲块的方式， 来实现实时输出。我们对`SSHClient` 简单封装一下， 增加一个 run 的方法。

```python
from gevent.socket import wait_read
from paramiko import SSHClient
from paramiko import AutoAddPolicy


class MySSHClient(SSHClient):


    def _forward_bound(self, channel, callback, *args):
        try:
            while True:
                wait_read(channel.fileno())
                data = channel.recv(1024)
                if not len(data):
                    return
                callback(data, *args)
        finally:
            self.close()


    def run(self, command, callback, *args):
        stdin, stdout, stderr = self.exec_command(
            command, get_pty=True
        )
        self._forward_bound(stdout.channel, callback, *args)

        return stdin, stdout, stderr
```


使用方式和原生的 `SSHClient` 一样， 只不过不去调用 `exec_command` 方法了， 改为调用 `run` 方法.


```python
def console(text):
    print(text)

ssh = MySSHClient()
ssh.set_missing_host_key_policy(AutoAddPolicy())
ssh.connect("IPADDRESS", 22, "USER", "PASSWORD")
stdin, stdout, stderr = ssh.run("python -u test.py", console)

print stderr.channel.recv_exit_status()
```


Python 执行本地命令， 也可以做到实时输出， 不用等到命令执行完毕后才得到输出信息。


```python
import subprocess
import shlex

def run_command(command):
    process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE)
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            print("writing websockets")
            print output.strip()
    rc = process.poll()
    return rc


if __name__ == '__main__':
    command = """sh run.sh"""
    run_command(command)
```


