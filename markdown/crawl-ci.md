title: 全宋词爬取过程及数据分析
date: 2017-03-07 14:11:01
set: 个人项目
---

<script src="/static/3rd/tagul.min.js" async defer></script>

<style>

.block {
    padding-bottom: 0 !important;
}

</style>
![hidden](/uploads/images/WX20180516-101305@2x.png "cover")
由于某个公众号对我仓库[chinese-poetry](https://github.com/jackeyGao/chinese-poetry)的推广， 短时间大量涨粉， 有人想要宋词的数据。 于是最近利用零散时间对全宋词进行爬取分析， 并做了简单的分析， 发现了一些不得了的事情。

分析仅仅对全宋词的内容进行了关键字排名分析、 宋词作者产量分析、 最受欢迎的词牌名排名分析

## 关键字排名分析

宋人喜欢用东风， 东风作为现代也会微妙， 人间、何处从唐诗就开始蝉联前三. 即使到了现代， 这两个词依存古风.

<div class="block" style="height: 400px;" data-tagul-src="/static/data/uifp9qxzt4ea" data-tagul-show-attribution></div>


## 宋词作者产量分析

辛弃疾果不其然的成为两宋现存词最多的作家, 还有一些虽然产量丰富但未必是我们熟知的。

<div class="block" style="height: 400px;" data-tagul-src="/static/data/hs8hgxlpmo29" data-tagul-show-attribution></div>

## 最受欢迎的词牌名排名分析

浣溪沙作为婉约 豪放两派所常用的词牌， 在两宋时期作为最受欢迎也是理所应当. 

<div class="block" style="height: 400px;" data-tagul-src="/static/data/xb019pkh27dn" data-tagul-show-attribution></div>


爬取逻辑没有做相应的系统化处理， 只是简单的脚本， 配置交互式界面做的操作。采用的相关技术: Python + parsel + peewee + requests + jieba

附上爬取解析脚本的逻辑:


<div class="gist">
<script src="https://gist.github.com/jackeyGao/d73381087b1278177aab60636f635119.js"></script>
</div>

<div class="gist">
<script src="https://gist.github.com/jackeyGao/6a68100a0298895c6ef92869669a12c2.js"></script>
</div>

## 运行

分别保存上面两个脚本为**parse.py**和**db.py**, 然后执行以下命令

```bash
$ pip install peewee parsel requests
$ python db.py # 初始化数据库
$ python parse.py
```
