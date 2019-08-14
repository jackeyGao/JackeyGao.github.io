title: ANSIBLE模块 - shell和command区别
date: 2017-11-13 12:08:12
---

Ansible 提供了大量的模块([All Modules](https://docs.ansible.com/ansible/latest/list_of_all_modules.html))供执行 AD-Hoc 和撰写 playbook。 有些模块有很多通用性， 但设计为多个还是有部分区别的。

## shell vs. command

一个典型的例子就是 [shell](https://docs.ansible.com/ansible/latest/shell_module.html) 和 [command](https://docs.ansible.com/ansible/latest/command_module.html) 模块. 这两个模块在很多情况下都能完成同样的工作， 以下是两个模块之前的区别：

- command 模块命令将不会使用 shell 执行. 因此, 像 `$HOME` 这样的变量是不可用的。还有像`<`, `>`, `|`, ';', '&'都将不可用。
- shell 模块通过shell程序执行， 默认是`/bin/sh`, `<`, `>`, `|`, ';', '&' 可用。但这样有潜在的 shell 注入风险， 后面会谈.
- command 模块更安全，因为他不受用户环境的影响。 也很大的避免了潜在的 shell 注入风险.

## 结论

结论是两个模块都要避免使用， 你应该优先考虑更具体的 ansible 模块。 比如用 command 或者 shell 执行 yum 命令前， 应该先了解到直接的 yum 模块。使用具体模块比执行命令要优雅很多， 因为这些模块设计都是具有幂等性的, 并满足其他标准, 如异常处理等.

如果没有更具体的模块， 相对来说 command 更安全点。

如果您需要用户环境和流式操作，则只能使用 shell 模块，但您要小心。 请记住 ansible 官方给出的提示, 如果将 shell 模块和变量一起使用：

>%warning To sanitize any variables passed to the shell module, you should use “{{ var | quote }}” instead of just “{{ var }}” to make sure they don’t include evil things like semicolons.)

> 即: 如果你需要安全的使用带有变量的 shell 模块， 使用`{{ var | quote }}`` 代替`{{ var }}` , 确保输入不包含分号或者流式操作.

