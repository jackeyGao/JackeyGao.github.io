title: 我的 VSCode 配置
date: 2019-07-24 09:35:48
set: 个人项目
---

Python 程序员应该首要使用免费的 [VSCode](https://code.visualstudio.com/ "微软开发的开源代码编辑器.") 编辑器.

![VSCode](/uploads/images/vscode.png "cover")

我的开发主要语言 Python， 偶尔写一些页面， 包括 Vue.js 和 jQuery 页面.

以下为通用设置

```js
{
    "files.exclude": {
        "**/.git": true,
        "**/.svn": true,
        "**/.hg": true,
        "**/*.pyc": true,
        "**/.DS_Store": true,
        "**/__pycache__": true,
        "**/node_modules": true,
    },
    "window.zoomLevel": 1,
    "editor.letterSpacing": 0.5,
    "workbench.activityBar.visible": true,
    "workbench.colorTheme": "Solarized Dark",
    "editor.tabSize": 2,
    // Python
    "python.venvPath": "~/.virtualenvs",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.linting.pep8Enabled": false,
    "python.analysis.logLevel": "Warning",
    "python.dataScience.sendSelectionToInteractiveWindow": true,
    // Python
    "[python]": {
        "editor.rulers": [
            72,
            79
        ],
        "editor.tabSize": 4,
        "editor.insertSpaces": true
    },
    // JS
    "[javascript]": {
        "editor.tabSize": 2
    },
    "html.format.enable": false,
}
```

除了以上的通用设置， 我还会在每个项目中定义虚拟环境位置。 在项目的目录下在 `.vscode/settings.json`

一般通过 `Python: Select Interpreter` 选择虚拟环境解析器自动创建， 其他的关于此项目的配置也都在这个文件， 但通用环境的配置够用，一般也没有其他的配置.

```json
{
    "python.pythonPath": "/path/to/virtualenv/bin/python"
}
```
