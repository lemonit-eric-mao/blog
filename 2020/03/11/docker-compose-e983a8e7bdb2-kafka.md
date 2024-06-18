---
title: 'docker-compose 部署 kafka'
date: '2020-03-11T10:05:09+00:00'
status: publish
permalink: /2020/03/11/docker-compose-%e9%83%a8%e7%bd%b2-kafka
author: 毛巳煜
excerpt: ''
type: post
id: 5285
category:
    - Kafka
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
wb_sst_seo:
    - 'a:3:{i:0;s:0:"";i:1;s:0:"";i:2;s:0:"";}'
---
###### [kafka 官网](https://kafka.apache.org/ "kafka 官网")

###### [kafka github](https://github.com/apache/kafka/releases "kafka github")

###### [kafka 下载](https://github.com/apache/kafka/releases "kafka 下载")

**[kafka-docker github参考](https://github.com/wurstmeister/kafka-docker)**

- - - - - -

- - - - - -

- - - - - -

###### 准备

```ruby
mkdir -p /home/deploy/kafka/logs/
mkdir -p /home/deploy/kafka/data/

```

- - - - - -

##### 安装kafka

```ruby
cat > /home/deploy/kafka/docker-compose.yaml 
```

**启动集群**：

```ruby
# 添加多副本：
docker-compose up -d
# 销毁集群：
docker-compose down

```

- - - - - -

###### **打开web界面**：`http://192.168.180.46:9000`