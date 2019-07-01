title: Cable : 基于Ansible运维Web管理平台
date: 2018-12-14 15:10:08
---

![Cable](/uploads/images/cable-logo.png "cover")

> %error **注意:** 代码质量不高， 稳定性极差。 目前没有时间做此项目开源， 暂无开源计划.

Cable 在设计之初是 Ansible Tower 的替代品.基于WEB的ANSIBLE管理中心，使ANSIBLE更易于用于各种 IT 团队(需要有强烈的需求前提下， 默认避免线上操作). 可直接在 web 中使用 AD-HOC或者 PLAYBOOK 批量管理线上主机， 它支持短命令(AD-HOC)和 Playbook 的执行, 也可以对任务保存成模板供l以后方便复用。并可以对任务模板进行授权给其他任何成员， 做到最小化的能力交付（一个命令或者一个过程）.

CABLE 可以分配用户属于哪个组织， 可以访问组织哪些权限。甚至共享凭证，而不需要危险的传输 SSH 凭证.  Inventory 可以图形化管理或者通过规范化接口管理。CABLE 会记录用户的所有操作，并且有一个很友好的 REST API.

## 功能

- 多组织

可根据不同项目或产品甚至物理空间来创建不同的组织， 用于区分。

![多组织](/uploads/images/cable-1-choice-organization.png)

- 批量AD-HOC

支持对多台主机批量执行命令

![执行一个 ADHOC](/uploads/images/cable-6-run-adhoc.jpeg)

![ADHOC执行页, 实时的进度](/uploads/images/cable-6-run-adhoc-running.jpeg)

- 批量执行 PLAYBOOK

支持对多台主机批量执行 PLAYBOOK, 支持二次自定义主机。

![执行一个 Playbook](/uploads/images/cable-run-playbook.png)

![执行 Playbook 确认页](/uploads/images/cable-run-playbook-choice-hosts.jpeg)

![任务详情和进度页面](/uploads/images/cable-run-playbook-detail.png)

- Inventory 管理

在线管理 Inventory 主机, 包括增加，修改， 更新， 删除. 变量管理

![](/uploads/images/cable-2-host-edit.png)

- Group 管理

在线管理 Group 主机, 包括增加，修改， 更新， 删除. 变量管理

![](/uploads/images/cable-3-group.png)

- Project 管理

通过 Git 方式更新 Playbook， Template， FILE。

![](/uploads/images/cable-4-projects.png)

- 活动审计, 任务重试， 增量执行（仅执行上次失败执行）

所有操作做历史纪录

![](/uploads/images/cable-5-activity.png)

可以查看一个任务的详细， 包括执行的成功主机列表和失败主机列表。 也可以重新执行这个任务， 或者删除这个活动.

也可以查看详细的步骤信息, 比如一个任务有多个 playbook 或者 多个模块组成， 那么可以查看单个模块的执行情况.

![](/uploads/images/cable-5-activity-detail.png)

查看单个模块的执行详细

![](/uploads/images/cable-5-job-view.png)

可以通过 JSON 查看， 也可以通过 Table 查看， 更可以下载 JSON 文件， 本地编辑器查看.

- 结果视图， TABLE 视图， 实时进度

可视化执行结果， 支持实时展示结果.

![](/uploads/images/cable-table-view.jpeg)


- 权限管理

不同用户拥有不同组织的不同权限， 可供灵活分配

- 任务模板

可以对常用任务创建任务模板， 并支持参数.

![](/uploads/images/cable-templates.png)

支持执行模板的时候 可选参数， 使template更加灵活.

![](/uploads/images/cable-templates-prompt.png)


## 名词解释

- ORGANIZATION

组织，一组资源（INVENTORY）的集合。  可根据不同产品或项目划分. 组织是 CABLE 最高级的划分， 不同组织的 INVENTORY(INSTANCE, GROUP, KEY, PROJECT, TEMPLATE)不可跨组织使用.

- INVENTORY

资源, 资源代表了组织内(INSTANCE, GROUP, KEY， PROJECT)的统称。 他是执行 AD-HOC 和 PLAYBOOK 的引用资源。 一个组织必须有资源才能运作下来.

- INSTANCE

主机hosts, 组织内管理的所有远程机器。

- GROUP

组标签, ansible 支持灵活的 pattern 匹配， 加入组标签的划分可以很方便的进行 pattern 搜索.

- KEY

密钥 KEY， 用于 SSH 连接到远程机器。 可以通过绑定到 INSTANCE 使用， 也可以绑定到 GROUP 使用。 另外一个重要的功能就是， 通过 GIT 同步 PROJECT 的时候使用。

- PROJECT

PROJECT 用于同步PLAYBOOK 和一些执行素材。PLAYBOOK 和 GIT 结合能够最大方便的管理版本变更和回滚。  PROJECT 分为 PLAYBOOK、 TEMPLATE、 FILES 分别使用于不同场景。

- 
    - Playbook： 执行 PLAYBOOK 的列表。
    - Template： 配置模板（AD-HOC 模块参数按需使用）
    - Files： 文件（AD-HOC 模块参数按需使用）

- AD-HOC [>](https://docs.ansible.com/ansible/latest/intro_adhoc.html)

短命令，在 ansble中为临时命令, 在 ansible 中通过/usr/bin/ansible命令调起。在 CABLE 中，是一个很方便的在线编辑任务的功能 ， 并可以保存为任务模板。他支持 ansible 所有模块(允许的情况)。并可以使用 ansible 所有 ad-hoc 参数和模块参数。ansible 拥有1378个模块， 如: command, shell, yum, service, copy, file, template等


- PLAYBOOK [>](https://docs.ansible.com/ansible/latest/playbooks.html)

PLAYBOOK 是 ansible 配置、部署和编排语言。CABLE 支持在线执行 PLAYBOOK 功能。PLAYBOOK 比 AD-HOC 具有更好的逻辑性、模块化和工程性。 它非常适合部署复杂的应用程序。


- TEMPLATE (任务模板)

CABLE 支持把常用的 AD-HOC 或 PLAYBOOK 保存， 方便下次复用。 并至此增加 CABLE 变量， 让执行者启动任务的时候填写。 TEMPLATE默认仅管理员拥有权限，但可以通过管理员授权给{ 任务执行者 }。 可以跨域组织授权.

- Prompt on launch

CABLE 支持 CABLE 级别参数（非 ansible 变量）， 当任务启动的时候再指定这个变量的值。使任务更灵活. 可以设置描述和一组可选值列表.

## 技术依赖

### 平台

- Python 2.7
- MySQL
- Redis
- Docker

### 库

```
incremental==17.5.0
ansible==2.3.1.0
asgi-redis==1.4.2
asgiref==1.1.2
asn1crypto==0.22.0
attrs==17.2.0
autobahn==17.7.1
Automat==0.6.0
bcrypt==3.1.3
certifi==2017.7.27.1
cffi==1.10.0
channels==1.1.6
chardet==3.0.4
constantly==15.1.0
coreapi==2.3.1
coreschema==0.0.4
cryptography==2.0.2
daphne==1.3.0
Django==1.11.4
django-cors-headers==2.1.0
django-filter==1.0.4
django-rest-swagger==2.1.2
djangorestframework==3.6.3
djangorestframework-jwt==1.11.0
enum34==1.1.6
giturlparse.py==0.0.5
hyperlink==17.3.0
idna==2.5
ipaddress==1.0.18
itypes==1.1.0
Jinja2==2.9.6
jinja2schema==0.1.4
jsonfield==2.0.2
MarkupSafe==1.0
msgpack-python==0.4.8
openapi-codec==1.3.2
paramiko==2.2.1
pyasn1==0.3.1
pycparser==2.18
pycrypto==2.6.1
PyJWT==1.5.2
PyNaCl==1.1.2
pytz==2017.2
PyYAML==3.12
redis==2.10.6
requests==2.18.2
simplejson==3.11.1
six==1.10.0
Twisted==17.5.0
txaio==2.8.1
uritemplate==3.0.0
urllib3==1.22
zope.interface==4.4.2
MySQL-python==1.2.5
```

## 架构图

![架构图](/uploads/images/cable-design.png "border")

## 任务执行逻辑

![任务执行逻辑图](/uploads/images/cable-task-design.png "border")

## 安全考虑


**KEY 安全考虑**

为了管理方便， CABLE推荐使用KEY认证连接方式，KEY 在系统生成的时候，仅当前 CABLE 运行用户对私有 KEY有访问权限。 所以需要保护好 CABLE 运行账户.

KEY文件权限600 后续加入passphrase.

**SHELL 注入**

避免使用shell模块, 必须要用的话， 可以在使用变量时加入单引号或quote过滤器。当不得不使用 SHELL 模块，并且需要配合变量在 free\_from中使用时，创建者必须严格使用下列方法.

```shell:error#Bad
echo {{ var }}
```

```shell:good#Good
echo {{ var | quote }}
```

> **Ansible 官方建议**: To sanitize any variables passed to the shell module, you should use “{{ var | quote }}” instead of just “{{ var }}” to make sure they don’t include evil things like semicolons.)

**rm命令屏蔽**

CABLE 简单的对`rm`命令进行屏蔽， 但仅检测free\_form参数.

## 权限

- 超级用户(管理者在组织之上， 管理所有组织)
    - 增加组织
    - 删除组织
    - 查看所有用户的执行记录
    - **{ 组织管理者 }**
- 组织管理者 (组织内管理权限.) 
    - 管理组织内资产
    - 加入移除组织成员
    - 授权组织内template
    - 同步 PROJECT
    - 查看当前组织的所有用户的执行记录
    - **{ 组织成员 }**
- 组织成员 (组织之下的成员, 可属于多个组织)
    - 创建和执行组织内 AD-Hoc
    - 创建和执行组织内 Playbook
    - 创建修改删除组织内 Template
    - **{ 任务执行者 }**
- 任务执行者 (拥有Template 执行权限的成员)
    - 执行已授权的 template
    - 查看自己的 Activity
    - 查看自己的 任务结果

## API

![Cable Swagger](/uploads/images/cable-swagger.png)


