---
title: "docker-compose 部署 kafka"
date: "2020-03-11"
categories: 
  - "kafka"
---

###### [kafka 官网](https://kafka.apache.org/ "kafka 官网")

###### [kafka github](https://github.com/apache/kafka/releases "kafka github")

###### [kafka 下载](https://github.com/apache/kafka/releases "kafka 下载")

**[kafka-docker github参考](https://github.com/wurstmeister/kafka-docker)**

* * *

* * *

* * *

###### 准备

```ruby
mkdir -p /home/deploy/kafka/logs/
mkdir -p /home/deploy/kafka/data/
```

* * *

##### 安装kafka

```ruby
cat > /home/deploy/kafka/docker-compose.yaml << ERIC

version: '3.6'
services:

  zookeeper:
    image: bitnami/zookeeper:3.6.3
    container_name: zookeeper
    restart: always
    hostname: zookeeper
    ports:
      - 2181:2181
#    volumes:
#      - ./config/zookeeper/data:/bitnami/zookeeper
#      - ./config/zookeeper/log:/opt/bitnami/zookeeper/logs
    environment:
      - ZOO_SERVER_ID=1
      - ZOO_SERVERS=zookeeper:2888:3888
      - ALLOW_ANONYMOUS_LOGIN=yes

  kafka-server:
    depends_on:
      - zookeeper
    image: bitnami/kafka:3.2.3
    privileged: true
    user: root
    hostname: kafka-server
    container_name: kafka-server
    restart: always
    extra_hosts:
      - 'kafka-server-external:192.168.101.30'
    ports:
      - 9094:9094
#    volumes:
#      - ./config/kafka-server:/bitnami/kafka
    environment:
      - KAFKA_BROKER_ID=1
      - KAFKA_CFG_ZOOKEEPER_CONNECT=zookeeper:2181
      - ALLOW_PLAINTEXT_LISTENER=yes
      - KAFKA_CFG_LISTENER_SECURITY_PROTOCOL_MAP=CLIENT:PLAINTEXT,EXTERNAL:PLAINTEXT
      - KAFKA_CFG_LISTENERS=CLIENT://kafka-server:9092,EXTERNAL://kafka-server:9094
      - KAFKA_CFG_ADVERTISED_LISTENERS=CLIENT://kafka-server:9092,EXTERNAL://kafka-server-external:9094
      - KAFKA_INTER_BROKER_LISTENER_NAME=CLIENT
      - KAFKA_CFG_AUTO_CREATE_TOPICS_ENABLE=true

  kafdrop:
    depends_on:
      - kafka-server
    image: obsidiandynamics/kafdrop:3.30.0
    container_name: kafdrop
    restart: always
    ports:
      - 9000:9000
    environment:
      - KAFKA_BROKERCONNECT=kafka-server:9092

ERIC

```

**启动集群**：

```ruby
# 添加多副本：
docker-compose up -d
# 销毁集群：
docker-compose down
```

* * *

###### **打开web界面**：`http://192.168.180.46:9000`
