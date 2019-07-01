title: 使用PyQt5把网页打印成PDF
date: 2018-12-03 12:01:11
---


最近制作诗词日历的 PDF 版本， 准备打印一下做成实体日历。之前我写过一篇优化 print 样式的文章，在 Google 上搜索"page to pdf", 大多数都是把默认页面的样式打印， 而非使用 @media print 样式打印， 后面做了很多查询， 才发现 PyQt 可以使用 @media print 打印.

值得一提的是 PyQt 直接使用了Chrome 的内核, 而且在使用过程中我发现一些配置是可以共享的，比如 Chrome 的代理设置. 下面我通过打印日历的例子来介绍 PyQt 是怎么打印页面的。 而且 PyQt 基本上和 Chrome 的打印功能一致， 也可以通过QPageLayout控制打印的纸张大小， 以及边距的 margin 大小.

## 安装 pyQt5

在这里使用最新的PyQt5.

```shell
brew install PyQt5
```

其他系统的安装方法请请参考, 官方介绍: [https://pypi.org/project/PyQt5/](https://pypi.org/project/PyQt5/)

## 使用

PyQt5 是一个Python的GUI编程框架, 它提供了很多 GUI 编程的组件，我们这里主要用到 QtWebEngineWidgets 的组件.


```python
import sys, os
from datetime import date, timedelta
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets
from PyQt5.QtCore import QMarginsF
from PyQt5.QtPrintSupport import QPrinter
from PyQt5.QtGui import QPageLayout, QPageSize


app = QtWidgets.QApplication(sys.argv)
loader = QtWebEngineWidgets.QWebEngineView()
loader.load(QtCore.QUrl('http://shici.store/poetry-calendar/'))

layout = QPageLayout(
    QPageSize(QPageSize.B5),
    QPageLayout.Portrait, QMarginsF(0, 0, 0, 0)
)

def printFinished():
    page = loader.page()
    print("%s Printing Finished!" % page.title())
    app.exit()

def printToPDF(finished):
    loader.show()
    page = loader.page()
    page.printToPdf("%s.pdf" % page.title(), layout)


loader.page().pdfPrintingFinished.connect(printFinished)
loader.loadFinished.connect(printToPDF)

app.exec_()
```

可以看到上面代码中是打印了[http://shici.store/poetry-calendar/](http://shici.store/poetry-calendar/)页面， 并且以 B5 纸张进行打印， 当然你可以修改为 `QPageSize.A4`来打印 A4的纸张. 并且四边距均为0(也就是不留白).

需要注意上面的代码有一些是异步的操作， 这里使用信号挂载的形式来检查页面成功加载的时候和打印 PDF 完成的时候， 来分别完成部分任务。 这里比较类似于 JS 的事件。 

```python
loader.loadFinished.connect(printToPDF)
```

当页面加载完毕JS 执行完毕的时候再打印页面， 否则会出现打印空白页.

```python
loader.page().pdfPrintingFinished.connect(printFinished)
```

当 PDF 完成的时候， 调用printFinished逻辑， 打印相关的信息并退出此APP 实例。


由于是异步的，打印多个 URL 的时候可能会踩到一些坑。 我采用的方式是每一个页面都实例化一个 app， 当打印完后在printFinished退出此 APP。 下一个 URL 重新使用一个新的 URL 实例, 这是最简单的方式(理解PyQt5生命周期是个耗时的工作, 发量不够..).


执行多个 URL

```python
import sys, os
from datetime import date, timedelta
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets
from PyQt5.QtCore import QMarginsF
from PyQt5.QtPrintSupport import QPrinter
from PyQt5.QtGui import QPageLayout, QPageSize

def printPDF(t):
    app = QtWidgets.QApplication(sys.argv)
    loader = QtWebEngineWidgets.QWebEngineView()
    loader.setZoomFactor(1)
    loader.load(QtCore.QUrl('http://127.0.0.1:8090/?d=' + str(t)))

    layout = QPageLayout(
        QPageSize(QPageSize.B5),
        QPageLayout.Portrait, QMarginsF(0, 0, 0, 0)
    )

    def printFinished():
        page = loader.page()
        print("%s Printing Finished!" % page.title())
        app.exit()

    def printToPDF(finished):
        loader.show()
        page = loader.page()
        page.printToPdf("%s.pdf" % page.title(), layout)


    loader.page().pdfPrintingFinished.connect(printFinished)
    loader.loadFinished.connect(printToPDF)

    app.exec_()


if __name__ == '__main__':
    year = 2019

    d = date(year, 01, 01)

    while True:
        if d.year > year:
            break

        printPDF(d)

        d = d + timedelta(days=7)
```

## 诗词周历效果图

以下打印诗词周历效果图

![](/uploads/images/page-to-pdf.png "cover:border")


## 总结

这提供了一个思路， 我们可以用这个来用Python制作书籍， 也可以使用HTML配合 jinja2的渲染生成， 然后通过 PyQt 来制作 PDF， 然后通过PyPDF2的PdfFileMerger功能把每个pdf 合并成一个大的 PDF 文件。 总之， 可以无限想象.

