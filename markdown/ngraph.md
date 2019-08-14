title: 数据可视化系统NGraph
date: 2017-03-13 17:30:01
set: 个人项目
---


去年重写了报表系统并为之取名为NGraph, 目的是做一套可以通过API提交数据来生成可视化数据的系统。

此系统第一版本只有报表项目， NGraph加入了监控报表的概念， 来区分报表项目， 并且优先级大于报表项目。 同时还有数据导出的工具. 报表目前支持table和pie.


# 相关功能截图

![](/uploads/images/ngraph/ngraph-dashboard.png "仪表盘")

![](/uploads/images/ngraph/ngraph-monitor.png "报表项目")

![](/uploads/images/ngraph/ngraph-database.png "数据导出")

![](/uploads/images/ngraph/ngraph-pie.png "饼图支持")


其实很想把此项目完善下并开源， 但是觉得功能有点少， 而且目前有Grafana这样的开源系统， 开源的计划也就停止了.
