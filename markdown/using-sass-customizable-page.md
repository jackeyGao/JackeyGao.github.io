title: 使用SASS做个可自定义主题的网页
date: 2018-11-28 16:41:11
---

本篇的代码已托管在 <i class="github icon"></i>[jackeyGao](https://github.com/jackeyGao) / [sass-theme](https://github.com/jackeyGao/sass-theme)

<hr/>

Sass 是对 CSS 的扩展，让 CSS 语言更强大、优雅。 它允许你使用变量、嵌套规则、 mixins、导入等众多功能， 并且完全兼容 CSS 语法。 Sass 有助于保持大型样式表结构良好， 同时也让你能够快速开始小型项目， 特别是在搭配 Compass 样式库一同使用时。

具体的 Sass 语法教学这里并不准备讲， 请参考官方教程， 本篇只举一个自定义主题的例子， 让你对 sass 的功能更加深刻， 理解 sass 在这个场景的优越性.

CSS 比较新的标准中增加 `var()` 变量功能， 这个可以非常方便的让我们切换 css 属性值， 从而达到切换主题的功能。 但只有只写现代化webkit内核浏览器才支持， IE 不支持。关于`var()`请参考"[var() | MDN](https://developer.mozilla.org/zh-CN/docs/Web/CSS/var)".

我们开始本篇的东西

## 准备

首先安装 Sass ， 这是一个 ruby 的工具， 使用 gem 可以快速安装.

```shell
$ gem install sass
```

安装完毕后， 通过查看 sass 版本来检查是否安装成功.

```shell
$ sass --version
Sass 3.4.23 (Selective Steve)
```

今天是2018年11月28日， **3.4.23**应该是最新的稳定版。

## 介绍

切换主题我们仅举例最简单的例子， 通过点击相应的主题， 来改变一个区域(div)的背景颜色和文字颜色.

需要更改的 div:

```html
<body class="sk-theme"> <!-- 主题 css 切换 -->
    <div class="main">
         <p>时间就像海绵里的水，只要愿挤，总还是有的。</p>
         <p class="meta">鲁迅</p>
    </div>
</body>
```

这是一个很简单的 div 展示，下面我们通过 sass 生成一些 css. 在上面的 html 例子中，假设我们有六个主题分别是sk-default, sk-mo, sk-green, sk-orange, sk-yellow, sk-pink. 那么我们至少要定义六个样式. 分别是:

- .sk-default .main
- .sk-mo .main
- .sk-green .main
- .sk-orange .main
- .sk-yellow .main
- .sk-pink .main


看着不太多, 手写还能接受? 但现实情况比这个复杂的多， 一个大的项目所需要切换的主题元素远比这一个区域多， 而且如果体验比较好的主题切换还要更加复杂。 往往分散在多个文件中， 当增加主题的时候需要更改的就很多。而 sass 就能很好的解决这个需求.

这里我们用到了 sass 的这些功能:

- sass 命令行 (把 scss build 为 css 功能)
- each (类似于 for 循环, 对 map 进行循环)
- map声明 

map 类似于 js 中的 object 和 python 中的 dict . 是一组 key: value  的集合. 这里我们主要存储我们的主题的配置.


```sass
$themes: (
    sk-default: (
        bg: #2c3e50,
        color: #fff
    ),
    sk-green: (
        bg: #80ac7b,
        color: #fff
    ),
    sk-mo: (
        bg: #585756,
        color: #fff
    ),
    sk-orange: (
        bg : #ff8364,
        color: #FFF
    ),
    sk-pink: (
        bg : #e7759a,
        color : #f6ec66
    ),
    sk-yellow: (
        bg : #f7de1c,
        color : #333
    )
);
```

可以看到我们定义了六个主题， 每个主题我们都选择了一个背景颜色(bg)和适配于背景颜色的文字颜色(color). 然后我们通过`each`生成六个样式.


```sass
@each $theme, $config in $themes {
    .#{$theme} .main
    {
        background: map-get($config, 'bg');
        color: map-get($config, 'color');
    }
}
```

通过 build sass可以自动生成六个样式表.

```shell
sass global.scss global.css
```

然后在页面引用这个 global.css 就可以了.


## 完成图

![](/uploads/images/using-sass-customizable-page.png "cover:border")

## 项目地址

<i class="github icon"></i>[jackeyGao](https://github.com/jackeyGao) / [sass-theme](https://github.com/jackeyGao/sass-theme)

## DEMO

[sass-theme](/sass-theme/)
