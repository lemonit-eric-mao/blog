---
title: "CentOS 7 安装 ElasticHD"
date: "2019-10-15"
categories: 
  - "elasticsearch"
---

##### 环境

- IP: 172.160.180.46
- 系统： CentOS 7.6

| 服务器 | IP | hostname |
| --- | --- | --- |
| ES-Master | 172.160.180.46 | test1 |
| ES-Node | 172.160.180.47 | test2 |
| ES-Node | 172.160.180.48 | test3 |
| ES-Node | 172.160.181.18 | test4 |

下载地址：https://github.com/360EntSecGroup-Skylar/ElasticHD/releases/

##### 下载/解压

```ruby
[elasticsearch@test1 deploy]$ wget https://github.com/360EntSecGroup-Skylar/ElasticHD/releases/download/1.4/elasticHD_linux_amd64.zip
[elasticsearch@test1 deploy]$
[elasticsearch@test1 deploy]$ unzip -o elasticHD_linux_amd64.zip
[elasticsearch@test1 deploy]$
```

##### 启动

```ruby
[elasticsearch@test1 deploy]$ ./ElasticHD -p 0.0.0.0:9800
```

##### webURL: 172.160.180.46:9800
