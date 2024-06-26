---
title: "docker-compose 安装 RabbitMQ"
date: "2020-02-09"
categories: 
  - "mq"
---

###### 前置条件

服务器： hostname:test1 IP: 172.108.180.46

* * *

###### docker-compose.yml

```ruby
cat > docker-compose.yml << ERIC
version: '3.1'
services:

  rabbitmq:
    container_name: rabbitmq
    image: rabbitmq:3.10.7-management-alpine
    ports:
      - 15672:15672
      - 5672:5672
    restart: always
    # 这个hostname必须写，因为RabbitMQ的数据持久化目录，是根据容器的hostname动态生成的
    hostname: rabbitmq
    volumes:
      - ./data:/var/lib/rabbitmq
    environment:
      TZ: Asia/Shanghai
      RABBITMQ_DEFAULT_USER: admin
      RABBITMQ_DEFAULT_PASS: 123456
      RABBITMQ_DEFAULT_VHOST: default_admin_vhost
ERIC

```

* * *

###### 启/停

```ruby
docker-compose up -d
docker-compose down
```

* * *

###### 测试连接

http://172.108.180.46:15672
