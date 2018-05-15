title: 用户Python3解析超大的csv文件
date: 2016-08-15 12:11:01
tags: 
- Python
- 翻译
- BigData
- Unicode
- Generators
---


我在日前获得一个任务，为了做分析, 从一个超大的csv文件中解析email地址和对应的日期时间戳然后插入到数据库中. 我知道有其他工具可以方便的完成我的工作(比如pandas),对于本文的目的, 我只打算用python的方式来处理这些数据.

这个csv文件超过了2G, 200万条的数据. 起初, 我尝试用excel打开这个文件， 来查看数据 。不幸的是, 我的excel程序开始假死最后我不得不杀掉excel进程.


## 使用Generators

> A generator function is mainly a more convenient way of writing an iterator. You don’t have to worry about the iterator protocol (.next, .__iter__, etc.). It just works. — David Beazley, [Generator Tricks for Systems Programmers](http://www.dabeaz.com/generators/)

Generators 可以让你很容易的从一个很大的数据集惰性遍历获取单条数据, 而不是全部读入内存.

```python
def get_email_data(csv_fname):
	with open(csv_fname, "r", encoding="latin-1") as email_records:
    	for email_record in csv.reader(email_records):
      		yield email_record


if __name__ == '__main__':
  	filename = "./emailData.csv"
  	iter_email = iter(get_email_data(filename))
  	next(iter_email)  # Skipping the column names

  	for row in iter_email:
    	print(row)
```

但这样报了一个错...

```python
UnicodeDecodeError: 'ascii' codec can't decode byte 0xe8 in position 1: ordinal not in range(128).
```

## 关于Unicode

> The best practice for handling text is the “Unicode sandwich” . This means that bytes should be decoded to str as early as possible on input (e.g., when opening a file for reading). The “meat” of the sandwich is the business logic of your program, where text handling is done exclusively on str objects. You should never be encoding or decoding in the middle of other processing. On output, the str are encoded to bytes as late as possible. — Luciano Ramalho, Fluent Python

因为我调试的时候打印在windows终端上, 因为windows默认不支持unicode, 所以出现了此错误. 然后我修改了`get_email_data`

```python
def get_email_data():
	with open(csv_fname, "r", encoding="latin-1") as email_records:
    	for email_record in csv.reader(email_records):
      		ascii_record = (x.encode('ascii', errors='replace').decode() 
                   	for x in email_record)
      		yield ascii_record
```

注意: `erros='replace'` 参数, 该方案不能完美的解决问题, 当编码一个字符串出现问题, Python 提供了三种方法:

- 1. strict - 抛出一个致命的错误
- 2. ignore - 删除这个字符
- 3. replace - 用?替换字符

replace 虽然不理想, 但他适合我的需要. 使用它能让我的程序完整的跑过去, 而没有unicode错误. 


## 更锦上添花

我不太想用索引来获取数据, 就像下面一样， 一点都不pythonic

```python
# Example: email_row[0], email_row[1], email_row[2], etc...
```

当然这样才是更人性化， 我也将要优化成这样

```python
# Example: email_row.date, email_row.from, email_row.to, etc...
```

`NamedTuples` 正合我意, 这里同样修改`get_email_data`函数 

```python
def get_email_data(csv_fname):
    """
    A generator for the data in the csv. This is because the csv files can often contain millions of records and shouldn't be stored in memory all at once.

    :param csv_fname:
        filename/location of the csv.

    :return:
        yields each row as a namedtuple.
    """
    EmailRecord = namedtuple('EmailRecord', 'date size from_addr  to_addr subject excerpt')
    with open(csv_fname, "r", encoding="latin-1") as email_records:
        for email_record in csv.reader(email_records):
            if len(email_record) == 6: # a valid row
                ascii_email_record = (x.encode('ascii', errors='replace').decode() for x in email_record)
                yield EmailRecord(*ascii_email_record)
```

关于NamedTuples， 它属于标准库里面的, 可以访问这里查看文档 [NamedTuples](https://docs.python.org/3/library/collections.html#collections.namedtuple)

## 总结

我们只是学习怎么让自己的电脑不死机, 然后友好的处理大的文件. 同时我们还学习了更加多的实用的技巧:

- Generators
- 字符编码问题
- NamedTuples





