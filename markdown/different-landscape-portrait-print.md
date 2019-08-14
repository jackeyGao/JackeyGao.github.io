title: 定义横向和纵向不同的print样式
date: 2018-11-25 16:11:14
---


最近优化了 [中文诗歌](http://shici.store) 的打印样式， 由于 Chrome 在打印的时候可以选择横向或者纵向的布局， 所以想同时支持两种布局。


横向布局是这样的, 图文为左右结构, 开启 overflow ，如果有溢出到文章范围则不显示(比如长恨歌), 则全部打印一页：


![横向效果图](/uploads/images/landscape.png "cover:border")


纵向布局则是这样, 图文为上下结构， 并且文章的overflow关闭:

![纵向效果图](/uploads/images/portrait.png "border")


## 怎么设置?


**@media print** 可以设置打印样式， 配合特定的条件， 我们可以针对不同的布局做样式处理。 布局的特定的条件就是`orientation`控制项.


即：

**横向**

```css
@media print and (orientation:landscape) {
    #main .grid .column {
        width: 50%;
    }
    /* ... */
    /* 为了举例简单， 我省略了下面部分代码. */
}
```

**纵向**


```css
@media print and (orientation:portrait) {
    #main .grid .column {
        width: 100%;
    }
    /* ... */
    /* 为了举例简单， 我省略了下面部分代码. */
}
```


当然你也可以通过定义不同的stylesheets文件， 然后通过 link 的media参数各自声明引用. 此例中假设我已经定义了portrait.css和landscape.css样式表文件.


```html
<link rel="stylesheet" media="print and (orientation:portrait)" href="portrait.css">

<link rel="stylesheet" media="print and (orientation:landscape)" href="landscape.css">
```

如果配置没有问题的话， 通过Chrome的打印功能可以看到以下结果图:


![横向打印效果图](/uploads/images/portrait-print.png "border")

![纵向打印效果图](/uploads/images/landscape-print.png "border")


