---
title: 'CentOS 7 安装 kibana'
date: '2019-10-15T06:31:36+00:00'
status: publish
permalink: /2019/10/15/centos-7-%e5%ae%89%e8%a3%85-kibana
author: 毛巳煜
excerpt: ''
type: post
id: 5074
category:
    - ElasticSearch
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
##### 环境

- IP: 172.160.180.46
- 系统： CentOS 7.6

<table><thead><tr><th>服务器</th><th>IP</th><th>hostname</th></tr></thead><tbody><tr><td>ES-Master</td><td>172.160.180.46</td><td>test1</td></tr><tr><td>ES-Node</td><td>172.160.180.47</td><td>test2</td></tr><tr><td>ES-Node</td><td>172.160.180.48</td><td>test3</td></tr><tr><td>ES-Node</td><td>172.160.181.18</td><td>test4</td></tr></tbody></table>

##### 下载/解压

**`需要注意:`**`kibana的版本最好与ES的版本相同`

```ruby
[elasticsearch@test1 deploy]<span class="katex math inline">pwd
/home/elasticsearch/deploy
[elasticsearch@test1 deploy]</span> curl -L -O https://artifacts.elastic.co/downloads/kibana/kibana-7.4.0-linux-x86_64.tar.gz
[elasticsearch@test1 deploy]<span class="katex math inline">[elasticsearch@test1 deploy]</span> tar -zxvf kibana-7.4.0-linux-x86_64.tar.gz

```

##### 替换配置文件中如下部分属性

```ruby
[elasticsearch@test1 deploy]$ vim kibana-7.4.0-linux-x86_64/config/kibana.yml

```

```yaml
#server.port: 5601
server.port: 5601

#server.host: "localhost"
server.host: "172.160.180.46"

#server.name: "your-hostname"
server.name: "sino-kibana"

# es 地址
#elasticsearch.hosts: ["http://localhost:9200"]
elasticsearch.hosts: ["http://172.160.180.46:9200"]

# 显示中文版
#i18n.locale: "en"
i18n.locale: "zh-CN"


```

##### 启动

```ruby
[elasticsearch@test1 deploy]$ ./kibana-7.4.0-linux-x86_64/bin/kibana

```

##### webURL: 172.160.180.46:5601