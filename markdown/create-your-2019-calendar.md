title: 如何做一个实体日历
date: 2018-12-24 10:11:15
---

![2019](/uploads/images/calendar-2019.jpg "cover")

诗词周历实体版大部分已经送出， 剩余部分也会酌情送出。

本篇唠下做一本实体日历用到了哪些东西， 虽然工作量大部分是技术编码方面， 但剩余联系打印社及了解打印纸张和打印的质量等东西对我来说比编码难多了。 甚至和打印店讨价还价也让我心力憔悴， 甚至失眠了几天. 但整个过程还是比较快乐的.


# 技术方面

诗词周历目前仅提供 Web ，以下技术栈用到的是最多的， 占代码工作量的70%. 

- HTML5 
- JavaScript
- CSS3

诗词和配图作为主要内容， 整理这些也花费了很多时间.  这些会有一些简单的文本处理和配图爬虫的爬取. 因为时间的缘故配图和诗词都比较草率, 而且诗词和配图选取比较有个人倾向.

- chinese-poetry
- 泼辣有图

以上技术可以做一个 web 版本， 但做实体版为了印刷的方便, 还需要生成 PDF 或者其他格式的电子版. 这里主要是通过PyQt5生成55个PDF单页面， 然后 merge 成一个 PDF. 

- PyQt5
- PyPDF2

# 印刷方面

一开始我对质量要求挺严格的， 后面我觉得能看就行. 纸张的规格第一版为 B5， 而且是铁圈装订， 拿到手后太像一本书了。 完全没有日历的样子. 后来改为 A5， 并且调整为竖版. 装订方式为书圈装订看起来更加简约, 可以挂着也可以配合支架摆放. 

关于打印质量， 最后的版本是157g的铜版纸, 而且成品出来的厚度适中， 用最小的书圈翻页也比较灵活. 但这个纸折叠会掉颜料， 翻着翻着就会产生纸屑. 

我一点都不会谈价钱， 这个还是别提了.

- 纸张规格
- 打印质量
- 谈价钱


## 生成PDF脚本介绍

脚本通过 PyQt5 的 webView 引擎， 它是一个 Chrome 内核的浏览器， 我们用到pyQt 的打印功能， 生成每个页面(一周一个页面)的 PDF. 然后通过 PyPDF2 的 Merger 合并50+单页面 PDF.


```python
import sys, os
from datetime import date, timedelta
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets
from PyQt5.QtCore import QMarginsF
from PyQt5.QtPrintSupport import QPrinter
from PyQt5.QtGui import QPageLayout, QPageSize
from PyPDF2 import PdfFileMerger


root = "https://shici.store/poetry-calendar"

def log(msg):
    print("+ " + msg);


def printPDF(url, margins):
    app = QtWidgets.QApplication(sys.argv)
    loader = QtWebEngineWidgets.QWebEngineView()
    loader.setZoomFactor(1)
    loader.load(QtCore.QUrl(url))
    
    layout = QPageLayout(
        QPageSize(QPageSize.A4),
        QPageLayout.Portrait, QMarginsF(margins[0], margins[1], margins[2], margins[3])
    )
    
    def printFinished():
        page = loader.page()
        page.profile().clearHttpCache()
        log("%s Printing Finished!" % page.title())
        app.exit()
    
    def printToPDF(finished):
        loader.show()
        page = loader.page()
        page.printToPdf("./pdfs/%s.pdf" % page.title(), layout)
    
    
    loader.page().pdfPrintingFinished.connect(printFinished)
    loader.loadFinished.connect(printToPDF)

    app.exec_()


if __name__ == '__main__':
    year = 2019

    d = date(year, 01, 01)

    if not os.path.exists('./pdfs'):
        os.makedirs('./pdfs')
        log("+ Created directory './pdfs';")


    # cover page and end page.
    margins = [0, 0, 0, 0]
    printPDF(root + '/first.html', margins)
    printPDF(root + '/end.html', margins)

    margins = [16, 32, 16, 32]
    while True:
        if d.year > year:
            break    

        url = root + '/?d=' + str(d)
        printPDF(url, margins)
        
        d = d + timedelta(days=7)



    log("+ Merging PDF files;")

    pdfs = [ os.path.join('./pdfs', x) for x in os.listdir('./pdfs') if x.endswith(".pdf") ]

    merger = PdfFileMerger()

    for pdf in pdfs:
        print pdf
        merger.append(open(pdf, 'rb'))

    with open("%s.pdf" % year, "wb") as fout:
        merger.write(fout)

    log("+ Merged! Save as '%s.pdf'" % year)
```

## PDF 直接下载

> 链接: [https://pan.baidu.com/s/1aoL6VflUsFTeD0Vzbo3LSg](https://pan.baidu.com/s/1aoL6VflUsFTeD0Vzbo3LSg) 提取码: tni4



