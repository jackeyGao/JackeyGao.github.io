title: Django XSS
date: 2019-08-02 10:57:30
---

[XSS]攻击通常指的是通过利用网页开发时留下的漏洞，通过巧妙的方法注入恶意指令代码到网页，使用户加载并执行攻击者恶意制造的网页程序。

在 Django 框架开发中， 我们很容易禁止这个攻击。 我们可以在数据接受层面和数据展示层面来避免 XSS 。

## 接收数据

接收数据时， 我们对表单的数据落地前escape转义.

escape 的作用是转移字符串中的 HTML , 具体的是替换字符串中的特殊符号， 比如:

- `<` to `&lt;`
- `>` to `&gt;`
- `'` to `&#39;`
- `"` to `&quot;`
- `&` to `&amp;`


比如某个用户在表单中的 notes 字段输入了以下内容;

```
今天天气很好

&lt;script&gt;alert(&quot;XSS&quot;);&lt;/script&gt;
```

如果我们没有 escape 转移操作， 那么存入数据库中就是原封不动的存入。 看起来相安无事， 如果这个值是富文本， 我们需要通过标签渲染到HTML 页面中？ 会发生什么？

![XSS Alert](/uploads/images/xss-alert.png "border:padding")

试想一下， 如果你是这个产品的用户， 如果访问到这个日记页面， 没有看到优美的日记之前， 先被这个弹窗打扰了， 你心情如何？ 当然弹窗只是干扰， 最可怕的是我可以在 notes 字段输入任何的代码， 每一个访问这个日记的用户都会执行恶意代码。 可以说后果非常的严重.

我们在 Django 获取数据的时候转移用户输入的字段.

```python
notes = escape(request.POST.get('notes', ''))
```

然后我们得到的 notes 内容， 应该是下面这样的, 可以看到下面的字符串是不能被执行的.

```
今天天气很好

&amp;lt;script&amp;gt;alert(&amp;quot;XSS&amp;quot;);&amp;lt;/script&amp;gt;
```

我们可以把这个内容安全的转换成 markdown. 然后通过 `safe` 展示带有格式的日记内容,而且内容是安全的.


## 再次编辑

再次编辑的时候， 输入框渲染的内容也要 `safe` 过滤一下， 否则从数据库拉出来的内容是 escape 转义过后的， 用户并不知道这是怎么回事。 所以在编辑器中应该这样做

```html
<textarea class="editor">{{ notes|safe }}</textarea>
```


![樱花 by 「Meriç Dağlı」](/uploads/images/summer-flower.jpeg "overflow:cover")


[XSS]: https://en.wikipedia.org/wiki/Cross-site_scripting "Cross-site scripting (XSS)"
