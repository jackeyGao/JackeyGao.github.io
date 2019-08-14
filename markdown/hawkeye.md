title: 多监控平台统一 | Hawkeye
date: 2018-03-27 10:01:11
set: 个人项目
---


近年来出现越来越多的监控平台， 每一个监控平台都是其擅长的地方， 比方说 zabbix 监控收集， 并监控基础服务。 grafana 监控平台可以很好的展示数据， kibana 又是日志相关的监控， 可以很出色的自定义很多业务监控。 总而言之基本上大多数有一定技术规模的公司， 运维都有很多监控平台。

多监控平台虽然好， 但暴露一个问题, 那就是关注度低， 因为有时候祸绝不单行， 一个问题的爆发， 往往在底层或者高层就已经暴露出来, 而我们需要来回的切换各个平台的监控图表， 这样排查起来非常慢。 如果我们能够更立体的看全部的监控报表， 那么暴露的问题也就一目了然了。

我进入 teambition 刚开始就是在做多监控平台统一的事情， 当时想的是把所有的数据全部写到一个平台， 而后通过结构化数据统一生成图表。 但构思太大， 实现起来艰难。 于是此项目难产了。

现在用的是嵌入的方式，幸运的是 zabbix、grafana、kibana 都支持嵌入， 而且每个图表的嵌入都支持start_time和 end_time, 这使得一个页面大盘看多个平台的监控就非常直观。

## 各个平台的嵌入 URL 组成部分.


### Zabbix

```
http://HOST:PORT/chart2.php?graphid=1911&period=1800&stime=20190309095657&updateProfile=1&profileIdx=web.screens&profileIdx2=1911&width=1302
```

### Grafana

```
https://grafana.teambition.net/dashboard-solo/db/cpu-overview?orgId=1&panelId=5&from=1520540867986&to=1520562467987
```

### Kibana

```
https://elk.teambition.net/app/kibana#/visualize/edit/API-response-time-(avg)?embed=true&_g=()&_a=(filters:!(),linked:!f,query:(query_string:(analyze_wildcard:!t,query:'*')),uiState:(),vis:(aggs:!((enabled:!t,id:'1',params:(field:req_time),schema:metric,type:avg),(enabled:!t,id:'2',params:(customInterval:'2h',extended_bounds:(),field:timestamp,interval:auto,min_doc_count:1),schema:segment,type:date_histogram)),listeners:(),params:(addLegend:!t,addTimeMarker:!f,addTooltip:!t,categoryAxes:!((id:CategoryAxis-1,labels:(show:!t,truncate:100),position:bottom,scale:(type:linear),show:!t,style:(),title:(),type:category)),defaultYExtents:!f,grid:(categoryLines:!f,style:(color:%23eee)),interpolate:linear,legendPosition:right,mode:stacked,scale:linear,seriesParams:!((data:(id:'1',label:Count),drawLinesBetweenPoints:!t,interpolate:linear,mode:stacked,show:true,showCircles:!t,type:area,valueAxis:ValueAxis-1)),setYExtents:!f,shareYAxis:!t,smoothLines:!f,times:!(),valueAxes:!((id:ValueAxis-1,labels:(filter:!f,rotate:0,show:!t,truncate:100),name:LeftAxis-1,position:left,scale:(mode:normal,type:linear),show:!t,style:(),title:(text:Count),type:value)),yAxis:()),title:'API+response+time+(avg)',type:area))
```

可以看到三个平台支持开始时间和结束时间， 这方便了我们 hawkeye 平台的时间选择控制。


## 核心处理URL代码

根据所指定的开始时间和结束时间， 对各个平台的 url 进行处理。 最后生成 url。

```python
def reload_url(s, e, items):
    s_cst = s + 28800000
    e_cst = e + 28800000
    zabbix = {
        "stime": datetime.fromtimestamp(s_cst/1000.0).strftime("%Y%m%d%H%M%S"),
        "period": (e - s) / 1000,
        "width": "600"
    }

    grafana = { "from": s, "to": e }

    kibana = {
        "from": datetime.fromtimestamp(s/1000.0).strftime("%Y-%m-%dT%H:%M:%S.%sZ"),
        "to": datetime.fromtimestamp(e/1000.0).strftime("%Y-%m-%dT%H:%M:%S.%sZ"),
    }

    kibana = {
        "_g": "(refreshInterval:(display:On,pause:!f,value:0)," + \
        "time:(from:'%s',mode:absolute,to:'%s'))" % (kibana["from"], kibana["to"])
    }

    for item in items:
        r = urlsplit(item.url)
        root = "%s://%s%s" % (r.scheme, r.netloc, r.path)

        if item.type == 'KB':
            r = urlsplit(r.fragment)

        query_dict = { k: v[0] for k, v in parse_qs(r.query).items() }

        if item.type == 'ZB':
            query_dict.update(zabbix)
        elif item.type == 'GF':
            query_dict.update(grafana)
        elif item.type == 'KB':
            query_dict.update(kibana)

        query_string = urlencode(query_dict)

        if item.type == 'KB':
            full_url = root + '#' + r.path + '?' + query_string
        else:
            full_url = root + '?' + query_string

        item.url = full_url
    return items
```

## 项目效果图


![大盘](/uploads/images/hawkeye-overview.png "大盘")
![控制](/uploads/images/hawkeye-control.png "可控制")
