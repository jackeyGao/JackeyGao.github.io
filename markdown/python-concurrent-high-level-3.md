title: Python 高级并发3
date: 2015-09-30 11:22:40
categories: 
- Python
- Python高级并发
tags:
- Python
- Concurrent

---



本篇主要讲案例, 两个使用Concurrent.futures实现的并发， 一个是多线程， 一个是多进程。

**多进程**

用在计算密集的确定Long Number是否为`质数`的例子

```python
import concurrent.futures
import math

PRIMES = [
    112272535095293,
    112582705942171,
    112272535095293,
    115280095190773,
    115797848077099,
    1099726899285419]

def is_prime(n):
    if n % 2 == 0:
        return False

    sqrt_n = int(math.floor(math.sqrt(n)))
    for i in range(3, sqrt_n + 1, 2):
        if n % i == 0:
            return False
    return True

def main():
    with concurrent.futures.ProcessPoolExecutor() as executor:
        for number, prime in zip(PRIMES, executor.map(is_prime, PRIMES)):
            print('%d is prime: %s' % (number, prime))

if __name__ == '__main__':
    main()
```

**多线程**

用在多线程访问HTTP链接， I/O密集的时候

```python
import concurrent.futures
import requests

URLS = ['http://jackeygao.com/',
        'http://pythoner.party/',
        'http://www.baidu.com/',
        'http://12306.cn/',
        'http://china.com/']

# Retrieve a single page and report the url and contents
def load_url(url, timeout):
    res = requests.get(url, timeout=timeout)
    return res.text

# We can use a with statement to ensure threads are cleaned up promptly
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    # Start the load operations and mark each future with its URL
    future_to_url = {executor.submit(load_url, url, 60): url for url in URLS}
    for future in concurrent.futures.as_completed(future_to_url):
        url = future_to_url[future]
        try:
            data = future.result()
        except Exception as exc:
            print('%r generated an exception: %s' % (url, exc))
        else:
            print('%r page is %d bytes' % (url, len(data)))
```

以上内容修改自[docs.python.org](https://docs.python.org/3/library/concurrent.futures.html)

`ThreadPoolExecutor` 和 `ProcessPoolExecutor` 都是`concurrent.futures.Executor`的子类。 那么他们都有`submit`、`map`、`shutdown`方法

**submit(fn, *args, **kwargs)**

异步执行函数

**参数:**

**fn**      为需要异步执行的函数

**args**    kwargs  函数的参数

**map(func, *iterables, timeout=None)¶**

此map函数和python自带的map函数功能类似，只不过concurrent模块的map函数从迭代器获得参数后异步执行。并且，每一个异步操作，能用timeout参数来设置超时时间，timeout的值可以是int或float型，如果操作timeout的话，会raisesTimeoutError。如果timeout参数不指定的话，则不设置超时间。

**func** 为需要异步执行的函数

**\*iterables**  可以是一个能迭代的对象，例如列表等。每一次func执行，会从iterables中取参数。

**timeout** 每个异步操作的超时时间

**shutdown(wait=True)**

此函数用于释放异步执行操作后的系统资源。



