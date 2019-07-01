title: 获取 zabbix 挂件数据(widget)
date: 2018-01-03 10:00:11
---

Zabbix 有非常丰富的 API ，但没有 widget 的 API。 所以获取 widget 的数据需要通过模拟登录爬取网页的形式来做。虽然我们可以用一定的 API 数据和相应的逻辑计算出此 TABLE 的数据， 但工作量非常大。
![zabbix widget](/uploads/images/zabbix-widget.png 'Zabbix Widget')

> 我用了两个模块来做， 一个逻辑控制 一个解析模块.

## main.py

```python
# -*- coding: utf-8 -*-

import sys
import json
import requests
from parse import HTMLTableParser

reload(sys)
sys.setdefaultencoding("utf-8")

HOST = "http://{{ HOST }}:8080/"


def parse(html):
    p = HTMLTableParser()
    p.feed(html)
    table = p.tables[0]
    c = [ {'prop': str(x), 'label': y} \
           for x,y in zip(range(len(table[0])), table[0]) ]
    return { "columns": c }, table[1:]


def login_session():
    s = requests.Session()
    payload = {
        "name": "{{ USER }}",
        "password": "{{ PASSWORD }}",
        "autologin": "1",
        "enter": "Sign in"
    }
    s = requests.Session()
    resp = s.post(HOST + 'index.php', payload)
    return s


def action(action_name):
    session = login_session()

    # 可以通过浏览器的开发者模式获取这里的参数, 一般需要更改 sid.
    params = {
        "action": action_name,
        "sid": "8c09585cdef21c27",  {{ SID }}
        "upd_counter": 0,
        "pmasterid": "dashboard"
    }
    payload = {"widgetRefresh": "syssum", '_': ""}

    resp = session.post(
        HOST + 'zabbix.php', params=params, data=payload)

    data = json.loads(resp.text)
    return data


def usage():
    raise Exception(
        """Arg error, Missing key
        Key choice in:
        \twidget.status.view
        \twidget.hosts.view
        \twidget.system.view
        \twidget.web.view
        \twidget.issues.view"""
    )


if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()

    data = action(sys.argv[1])
    config, data = parse(data["body"])
    sys.stdout.write(json.dumps(config, indent=2)+'\n')
    sys.stdout.write(json.dumps(data, indent=2)+'\n')
```


## parse.py

```python
from HTMLParser import HTMLParser


class HTMLTableParser(HTMLParser):
    """ This class serves as a html table parser. It is able to parse multiple
    tables which you feed in. You can access the result per .tables field.
    """
    def __init__(
        self,
        decode_html_entities=False,
        data_separator=' ',
    ):

        HTMLParser.__init__(self)

        self._parse_html_entities = decode_html_entities
        self._data_separator = data_separator

        self._in_td = False
        self._in_th = False
        self._in_span = 0
        self._current_table = []
        self._current_row = []
        self._current_cell = []
        self.tables = []

    def handle_starttag(self, tag, attrs):
        """ We need to remember the opening point for the content of interest.
        The other tags (<table>, <tr>) are only handled at the closing point.
        """
        if tag == 'span':
            self._in_span = self._in_span + 1
        if tag == 'td':
            self._in_td = True
        if tag == 'th':
            self._in_th = True

    def handle_data(self, data):
        """ This is where we save content to a cell """
        if self._in_td or self._in_th:
            if self._in_span in (0, 1):
                self._current_cell.append(data.strip())
            else:
                return

    def handle_charref(self, name):
        """ Handle HTML encoded characters """

        if self._parse_html_entities:
            self.handle_data(self.unescape('&#{};'.format(name)))

    def handle_endtag(self, tag):
        """ Here we exit the tags. If the closing tag is </tr>, we know that we
        can save our currently parsed cells to the current table as a row and
        prepare for a new row. If the closing tag is </table>, we save the
        current table and prepare for a new one.
        """
        if tag == 'td':
            self._in_td = False
        elif tag == 'th':
            self._in_th = False
        elif tag == 'span':
            self._in_span = self._in_span - 1

        if self._in_span < 2:
            if tag in ['td', 'th']:
                final_cell = self._data_separator.join(self._current_cell).strip()
                self._current_row.append(final_cell)
                self._current_cell = []
            elif tag == 'tr':
                self._current_table.append(self._current_row)
                self._current_row = []
            elif tag == 'table':
                self.tables.append(self._current_table)
                self._current_table = []
```


