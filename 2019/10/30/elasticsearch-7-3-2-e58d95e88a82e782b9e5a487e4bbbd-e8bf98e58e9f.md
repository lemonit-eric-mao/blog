---
title: 'ElasticSearch 7.3.2 单节点备份/还原'
date: '2019-10-30T03:48:44+00:00'
status: publish
permalink: /2019/10/30/elasticsearch-7-3-2-%e5%8d%95%e8%8a%82%e7%82%b9%e5%a4%87%e4%bb%bd-%e8%bf%98%e5%8e%9f
author: 毛巳煜
excerpt: ''
type: post
id: 5095
category:
    - ElasticSearch
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
##### 前置条件

- 版本：CentOS 7
- 软件版本：ElasticSearch 7.3.2

- - - - - -

- 在6.x中创建的索引快照可以恢复到7.x。
- 在5.x中创建的索引快照可以恢复到6.x。
- 在2.x中创建的索引快照可以恢复到5.x。
- 可以将在1.x中创建的索引快照恢复到2.x。
- 相反，  
  无法将在1.x中创建的索引快照还原到5.x或6.x，  
  无法将在2.x中创建的索引快照还原到6.x或7.x，  
  以及在5中创建的索引快照 x 无法还原到7.x。

###### [官网地址](https://www.elastic.co/guide/en/elasticsearch/reference/7.3/modules-snapshots.html "官网地址")

##### Elasticsearch提供了snapshot API 用作备份

###### 1、修改配置文件（开始）：

①修改Elasticsearch的配置文件 elasticsearch.yml 中增加设置：

```ruby
[elasticsearch@test1 ~]$ vim /elasticsearch-7.3.2/config/elasticsearch.yml

```

修改内容如下：

```ruby
path.repo: /home/elasticsearch/deploy/elasticsearch-7.3.2/snapshots

```

###### 2、创建备份仓库目录

- 调用API `_snapshot/仓库的路径名`
- `"location": "仓库的决对路径名/快照名称"`

```ruby
[elasticsearch@test1 ~]<span class="katex math inline">curl -X POST http://172.160.180.46:9200/_snapshot/snapshots/ -H "Content-Type: application/json" -d'{
    "type": "fs",
    "settings": {
        "location": "/home/elasticsearch/deploy/elasticsearch-7.3.2/snapshots/snapshot_20191106"
    }
}'

# 返回结果
{"acknowledged":true}
[elasticsearch@test1 ~]</span>

```

###### 3、备份

- 调用API `_snapshot`
- `wait_for_completion=true` 显示备份状态
- 快照名称：snapshot\_20191106

```ruby
[elasticsearch@test1 ~]$ curl -X PUT http://172.160.180.46:9200/_snapshot/snapshots/snapshot_20191106?wait_for_completion=true -H "Content-Type: application/json" 

```

###### 4、查看备份情况

- 调用API `_snapshot`

```ruby
[elasticsearch@test1 ~]$ curl -X GET "http://172.160.180.46:9200/_snapshot/snapshots/_all?pretty"
# 返回结果
{
  "snapshots" : [
    {
      "snapshot" : "snapshot_20191106",
      "uuid" : "ZpCaFwJZSC2maRR4iaeINQ",
      "version_id" : 7030299,
      "version" : "7.3.2",
      // 已经备份的索引列表
      "indices" : [
        "eric_test_schema"
      ],
      "include_global_state" : true,
      "state" : "SUCCESS",
      "start_time" : "2019-11-06T07:09:31.477Z",
      "start_time_in_millis" : 1573024171477,
      "end_time" : "2019-11-06T07:09:31.623Z",
      "end_time_in_millis" : 1573024171623,
      "duration_in_millis" : 146,
      "failures" : [ ],
      "shards" : {
        "total" : 3,
        "failed" : 0,
        "successful" : 3
      }
    }
  ]
}


```

###### 5、恢复数据

- 调用API `_restore`

```ruby
[elasticsearch@test1 ~]$ curl -X POST http://172.160.180.46:9200/_snapshot/snapshots/snapshot_20191106/_restore?wait_for_completion=true

```

###### 6、查看正在运行的索引列表

- 调用API `_cat`

```ruby
[elasticsearch@test1 ~]<span class="katex math inline">curl -X GET 'http://172.160.180.46:9200/_cat/indices?v'
health status index            uuid                   pri rep docs.count docs.deleted store.size pri.store.size
yellow open   eric_test_schema PeOw3lCmSx2kDjiVnPdmNw   3   2         10            0     34.2kb         34.2kb

[elasticsearch@test1 ~]</span>

```