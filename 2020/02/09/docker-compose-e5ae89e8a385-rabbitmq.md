---
title: 'docker-compose 安装 RabbitMQ'
date: '2020-02-09T05:31:54+00:00'
status: publish
permalink: /2020/02/09/docker-compose-%e5%ae%89%e8%a3%85-rabbitmq
author: 毛巳煜
excerpt: ''
type: post
id: 5249
category:
    - MQ
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
wb_sst_seo:
    - 'a:3:{i:0;s:0:"";i:1;s:0:"";i:2;s:0:"";}'
---
###### 前置条件

服务器：  
hostname:test1  
IP: 172.108.180.46

- - - - - -

###### docker-compose.yml

```ruby
cat > docker-compose.yml 
```

- - - - - -

###### 启/停

```ruby
docker-compose up -d
docker-compose down

```

- - - - - -

###### 测试连接

http://172.108.180.46:15672