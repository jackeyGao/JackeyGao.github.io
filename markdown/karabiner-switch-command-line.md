title: Karabiner profile 命令行切换方式
date: 2016-04-14 11:35:05
tags:
- Karabiner
---

Karabiner 提供了一个命令行工具来方便脚本编程， 一般这个命令行工具在安装包的bin目录下， 具体地址为: `/Applications/Karabiner.app/Contents/Library/bin/karabiner` 

## 帮助文档

```bash
Usage:
  Profile operations:
    $ karabiner list
    $ karabiner select INDEX (INDEX starts at 0)
    $ karabiner select_by_name NAME
    $ karabiner selected
    $ karabiner append NAME
    $ karabiner rename INDEX NEWNAME (INDEX starts at 0)
    $ karabiner delete INDEX (INDEX starts at 0)
  Settings:
    $ karabiner set IDENTIFIER VALUE
    $ karabiner enable IDENTIFIER (alias of set IDENTIFIER 1)
    $ karabiner disable IDENTIFIER (alias of set IDENTIFIER 0)
    $ karabiner toggle IDENTIFIER
    $ karabiner changed
  Others:
    $ karabiner export
    $ karabiner reloadxml
    $ karabiner relaunch
    $ karabiner be_careful_to_use__clear_all_values_by_name PROFILE_NAME

Examples:
  $ karabiner list
  $ karabiner select 1
  $ karabiner select_by_name NewItem
  $ karabiner selected
  $ karabiner append "For external keyboard"
  $ karabiner rename 1 "Empty Setting"
  $ karabiner delete 1

  $ karabiner set repeat.wait 30
  $ karabiner enable remap.shiftL2commandL
  $ karabiner disable remap.shiftL2commandL
  $ karabiner toggle remap.shiftL2commandL
  $ karabiner changed

  $ karabiner export
  $ karabiner reloadxml
  $ karabiner relaunch
  $ karabiner be_careful_to_use__clear_all_values_by_name NewItem

```

### 简单介绍

**查看已定义的profile**

```bash
$ karabiner list
0: Default
1: Poker2
```

**切换到指定profile 通过index**

```bash
$ karabiner select 1
```

**切换到指定profile 通过item name**

```bash
$ karabiner select_by_name $NAME
```

**当前选择的profile**

```bash
$ karabiner selected
1
```

**当前选择的profile name**

```bash
$ karabiner list | grep "^$(karabiner selected)"
```

同时此命令行工具还支持 `export`, `reloadxml`, `relaunch`, `删除profile`, `rename profile`, 等..


### 通过karabiner 设置热键来切换

以下为定义, 写入到private.xml的root标签中. 之后reload xml. 可以通过preferences界面也可以通过命令行`karabiner reloadxml`

```xml
<vkopenurldef>
    <name>KeyCode::VK_OPEN_URL_SHELL_switchprofile_newitem</name>
    <url type="shell">
        <![CDATA[    /Applications/Karabiner.app/Contents/Library/bin/karabiner select_by_name Poker2    ]]>
    </url>
</vkopenurldef>
<item>
    <name>Switch Profile to NewItem with F4</name>
    <identifier>private.switch1</identifier>
    <autogen>
        __KeyToKey__
        KeyCode::SHIFT_L,
        KeyCode::SHIFT_L,
        KeyCode::VK_OPEN_URL_SHELL_switchprofile_newitem
    </autogen>
</item>
```

