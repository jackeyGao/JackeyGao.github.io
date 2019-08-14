title: Python 高级并发2
date: 2015-09-30 11:15:40
categories: 
- Python
- Python高级并发
tags:
- Python
- Concurrent

---


一般程序并发分为`多线程`和`多进程`并发.

那么什么时候选择两种并发手段， 该如何选择呢， 应用场景是什么？

根据编程逻辑一般需要计算密集和I/O操作密集的时候选择并发提高程序效率， Python 由于GIL的限制，密集性运算需要使用多核心CPU时候， 这时候多线程显得力不从心， 甚至会变得更慢。而当需要I/O操作， 比如HTTP长连接的时候， 耗费的时间只是TCP建立链接的等待时间， 这时候当然优先使用多线程。

所以一般情况下， 我们开发程序耗费比较慢的是`计算密集`和`I/O密集`两种情况下的逻辑， 那么我可以采取：

* 计算密集:多进程
* I/O密集:多线程

推荐使用库：

concurrent.futures 是python3新增加的一个库，用于并发处理，类似于其他语言里的线程池（也有一个进程池），他属于上层的封装，对于用户来说，不用在考虑那么多东西了, 现已加入python 3.2标准库， python 2.7需要安装一下。

`pip install futures`

Executor:两个子`ThreadPoolExecutor`和`ProcessPoolExecutor`分别是产生进程池和线程池

Future：有Executor.submit产生多任务

ThreadPoolExecutor 和 ProcessPoolExecutor直接python的with as 控制流语句， 让你非常简单的就套入了程序里面。


