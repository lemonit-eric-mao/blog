---
title: 'CentOS 7 安装 ElasticHD'
date: '2019-10-15T07:34:03+00:00'
status: publish
permalink: /2019/10/15/centos-7-%e5%ae%89%e8%a3%85-elastichd
author: 毛巳煜
excerpt: ''
type: post
id: 5075
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

下载地址：https://github.com/360EntSecGroup-Skylar/ElasticHD/releases/

##### 下载/解压

```ruby
[elasticsearch@test1 deploy]<span class="katex math inline">wget https://github.com/360EntSecGroup-Skylar/ElasticHD/releases/download/1.4/elasticHD_linux_amd64.zip
[elasticsearch@test1 deploy]</span>
[elasticsearch@test1 deploy]<span class="katex math inline">unzip -o elasticHD_linux_amd64.zip
[elasticsearch@test1 deploy]</span>

```

##### 启动

```ruby
[elasticsearch@test1 deploy]$ ./ElasticHD -p 0.0.0.0:9800

```

##### webURL: 172.160.180.46:9800