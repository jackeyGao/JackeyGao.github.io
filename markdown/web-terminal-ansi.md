title: 在网页中显示ansi终端颜色
date: 2018-11-21 15:59:11
---

![](/uploads/images/ansi.png "cover:border")

终端命令为了可以友好的显示大多数都支持了颜色显示。 在终端中良好的颜色显示， 能够让我们处理问题更加高效，但是在运维开发中， 难免要在 web 网页中操作服务器, 难免要执行这些命令并且要显示在终端中.

除了友好的显示为等宽字体外， 显示这些颜色也是有必要的， 因为终端的颜色代码如果直接显示会很奇怪， 更加会干扰我们的信息.


默认情况下终端的显示颜色代码是这样的:


```text
Restarting mongod (via systemctl):  [60G[[0;32m  OK  [0;39m]
```

可以看到ansi 的颜色代码就好像乱码一样，而且在网页中， 我更希望颜色代码为 html 的样式。类似于这样:

```html
Restarting mongod (via systemctl):  [<span style="color:rgb(0,187,0)">  OK  </span>]
```

## ansi\_up


> 项目地址: [https://github.com/drudru/ansi\_up](https://github.com/drudru/ansi_up)

**ansi\_up** 库可以把终端颜色代码自动转换成 html 格式颜色样式， 让 web 显示终端颜色更加方便。

**浏览器示例**

```html
<script src="ansi_up.js" type="text/javascript"></script>
<script type="text/javascript">

  var txt  = "\n\n\033[1;33;40m 33;40  \033[1;33;41m 33;41  \033[1;33;42m 33;42  \033[1;33;43m 33;43  \033[1;33;44m 33;44  \033[1;33;45m 33;45  \033[1;33;46m 33;46  \033[1m\033[0\n\n\033[1;33;42m >> Tests OK\n\n"

  var ansi_up = new AnsiUp;

  var html = ansi_up.ansi_to_html(txt);

  var cdiv = document.getElementById("console");

  cdiv.innerHTML = html;

</script>
```

**Node示例**


```node
var AU = require('ansi_up');
var ansi_up = new AU.default;

var txt  = "\n\n\033[1;33;40m 33;40  \033[1;33;41m 33;41  \033[1;33;42m 33;42  \033[1;33;43m 33;43  \033[1;33;44m 33;44  \033[1;33;45m 33;45  \033[1;33;46m 33;46  \033[1m\033[0\n\n\033[1;33;42m >> Tests OK\n\n"

var html = ansi_up.ansi_to_html(txt);
```

**TypeScript示例**

```typescript
import {
    default as AnsiUp
} from 'ansi_up';

const ansi_up = new AnsiUp();

const txt  = "\n\n\x1B[1;33;40m 33;40  \x1B[1;33;41m 33;41  \x1B[1;33;42m 33;42  \x1B[1;33;43m 33;43  \x1B[1;33;44m 33;44  \x1B[1;33;45m 33;45  \x1B[1;33;46m 33;46  \x1B[1m\x1B[0\n\n\x1B[1;33;42m >> Tests OK\n\n"

let html = ansi_up.ansi_to_html(txt);
```

**安装**

```shell
$ npm install ansi_up
```

## Python 版本类似项目

- [https://github.com/Kronuz/ansi2html](https://github.com/Kronuz/ansi2html)
- [https://pythonhosted.org/ansiconv/](https://pythonhosted.org/ansiconv/)
