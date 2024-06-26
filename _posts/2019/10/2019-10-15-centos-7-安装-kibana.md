---
title: "CentOS 7 安装 kibana"
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

##### 下载/解压

**`需要注意:`**`kibana的版本最好与ES的版本相同`

```ruby
[elasticsearch@test1 deploy]$ pwd
/home/elasticsearch/deploy
[elasticsearch@test1 deploy]$ curl -L -O https://artifacts.elastic.co/downloads/kibana/kibana-7.4.0-linux-x86_64.tar.gz
[elasticsearch@test1 deploy]$
[elasticsearch@test1 deploy]$ tar -zxvf kibana-7.4.0-linux-x86_64.tar.gz
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
