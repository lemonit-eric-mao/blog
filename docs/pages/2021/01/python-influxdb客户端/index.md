---
title: "Python InfluxDB客户端"
date: "2021-01-04"
categories: 
  - "influxdb"
  - "python"
---

###### 安装依赖

```ruby
pip3 install influxdb
```

* * *

###### python InfluxDB客户端

```python
#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2021/01/04 15:55
# @Author  : Eric.Mao
# @FileName: influxdb.py
# @Software: PyCharm
# @Blog    : http://www.dev-share.top/

from influxdb import InfluxDBClient


class GetInfluxDB(object):
    # 静态变量，初始化连接数据库
    db = InfluxDBClient(
        host='127.0.0.1',
        port=8086,
        username='root',
        password='123456789')

    @classmethod
    # 查询 _internal 数据库下的数据
    def query_internal(cls, sql: str):
        return cls.db.query(sql, database='_internal')

    @classmethod
    # 查询 graf_vcenter 数据库下的数据
    def query_graf_vcenter(cls, sql: str):
        return cls.db.query(sql, database='graf_vcenter')

```
