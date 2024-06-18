---
title: "使用 KSQL 连接 kakfa 和 redis 二"
date: "2022-10-20"
categories: 
  - "ksql"
---

# POC验证

此方案使用 `jcustenborder/kafka-connect-redis` 插件来实现kafka数据同步到Redis

## 部署 Kafka服务端

- **创建工作目录**
    
    ```shell
    mkdir -p kafka-server/config schema-registry/config ksql/config redis/config
    ```
    
- **kafka单节点部署**
    
    ```shell
    cat > kafka-server/docker-compose.yaml << ERIC
    
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
    

## 部署 Redis

```shell
cat > redis/docker-compose.yaml << ERIC

version: '3.6'

services:

  redis:
    image: redis:6.2
    hostname: redis
    container_name: redis
    restart: always
    ports:
      - 6379:6379
      - 16379:16379
    volumes:
      - ./config/redis/redis.conf:/usr/local/etc/redis/redis.conf
      - ./config/data:/data
    command: redis-server /usr/local/etc/redis/redis.conf

ERIC

```

## 部署 schema-registry

```shell
cat > schema-registry/docker-compose.yaml << ERIC

version: '3.6'
services:

  schema-registry:
    image: confluentinc/cp-schema-registry:6.1.0
    container_name: schema-registry
    restart: always
    extra_hosts:
      - 'schema-registry:192.168.101.30'
      - 'kafka-server-external:192.168.101.30'
    ports:
      - 8081:8081
    environment:
      SCHEMA_REGISTRY_HOST_NAME: schema-registry
      SCHEMA_REGISTRY_KAFKASTORE_BOOTSTRAP_SERVERS: 'kafka-server-external:9094'

ERIC

```

## 部署 ksql

目前confluent KSQL支持两种方式，一种是ksql-cli，一种是rest

```yaml
cat > ksql/docker-compose.yaml << ERIC

version: '3.6'

services:
  # 服务端
  ksqldb-server:
    image: confluentinc/ksqldb-server:0.28.2
    hostname: ksqldb-server
    container_name: ksqldb-server
    privileged: true
    user: root
    ports:
      - 8088:8088
    extra_hosts:
      - 'redis-uri:192.168.101.30'
      - 'schema-registry:192.168.101.30'
      - 'kafka-server-external:192.168.101.30'
    environment:
      KSQL_LISTENERS: http://0.0.0.0:8088
      # kafka 服务端IP地址
      KSQL_BOOTSTRAP_SERVERS: kafka-server-external:9094
      KSQL_KSQL_SCHEMA_REGISTRY_URL: "http://schema-registry:8081"
      KSQL_KSQL_LOGGING_PROCESSING_STREAM_AUTO_CREATE: "true"
      KSQL_KSQL_LOGGING_PROCESSING_TOPIC_AUTO_CREATE: "true"
      # kafka connect 配置.
      KSQL_CONNECT_GROUP_ID: "kafka-connect-redis"
      KSQL_CONNECT_BOOTSTRAP_SERVERS: "kafka-server-external:9094"
      KSQL_CONNECT_KEY_CONVERTER: "org.apache.kafka.connect.storage.StringConverter"
      KSQL_CONNECT_VALUE_CONVERTER: "io.confluent.connect.avro.AvroConverter"
      KSQL_CONNECT_KEY_CONVERTER_SCHEMA_REGISTRY_URL: "http://schema-registry:8081"
      KSQL_CONNECT_VALUE_CONVERTER_SCHEMA_REGISTRY_URL: "http://schema-registry:8081"
      KSQL_CONNECT_VALUE_CONVERTER_SCHEMAS_ENABLE: "false"
      KSQL_CONNECT_CONFIG_STORAGE_TOPIC: "ksql-connect.configs"
      KSQL_CONNECT_OFFSET_STORAGE_TOPIC: "ksql-connect.offsets"
      KSQL_CONNECT_STATUS_STORAGE_TOPIC: "ksql-connect.statuses"
      # 告诉 kafka-connect-redis 将要链接的 kafka服务端，是单节点部署的
      KSQL_CONNECT_CONFIG_STORAGE_REPLICATION_FACTOR: 1
      KSQL_CONNECT_OFFSET_STORAGE_REPLICATION_FACTOR: 1
      KSQL_CONNECT_STATUS_STORAGE_REPLICATION_FACTOR: 1
      KSQL_CONNECT_PLUGIN_PATH: "/usr/share/kafka/plugins"
    volumes:
      - ./config/plugins:/usr/share/kafka/plugins

  # 客户端
  ksqldb-cli:
    depends_on:
      - ksqldb-server
    image: confluentinc/ksqldb-cli:0.28.2
    container_name: ksqldb-cli
    entrypoint: /bin/sh
    tty: true

ERIC

```

**启动**

```shell
docker-compose -f kafka-server/docker-compose.yaml up -d
docker-compose -f redis/docker-compose.yaml up -d

docker-compose -f schema-registry/docker-compose.yaml up -d
docker-compose -f ksql/docker-compose.yaml up -d

```

**查看内置 connector 是否启动成功**

```shell
## 需要多等待一会儿
docker-compose exec ksqldb-server curl localhost:8083
{"version":"7.3.0-cc-docker-ksql.119-33-ccs","commit":"8798a7293c174267","kafka_cluster_id":"1bgVxWdoTAyg4CC_j5FpKA"}


docker-compose exec ksqldb-server jstack KsqlServerMain | grep DistributedHerder-connect
"DistributedHerder-connect-1-1" #96 prio=5 os_prio=0 cpu=5721.00ms elapsed=4020.77s tid=0x00007fc56ea47000 nid=0x97 runnable  [0x00007fc5005a6000]


```

* * *

# **使用 ksql 建立 connector**

**下载相关connector插件**

```shell
wget -P ksql/config/plugins https://d1i4a15mxbxib1.cloudfront.net/api/plugins/jcustenborder/kafka-connect-redis/versions/0.0.3/jcustenborder-kafka-connect-redis-0.0.3.zip

unzip jcustenborder-kafka-connect-redis-0.0.3.zip

# 查看下载
ls ksql/config/plugins/
jcustenborder-kafka-connect-redis-0.0.3

```

**重新部署 ksqldb-server**

```shell
docker-compose -f ksql/docker-compose.yaml down
docker-compose -f ksql/docker-compose.yaml up -d

```

**查看内置 connector 是否启动成功**

```shell
[root@centos siyu.mao]# docker-compose exec ksqldb-cli ksql http://ksqldb-server:8088

OpenJDK 64-Bit Server VM warning: Option UseConcMarkSweepGC was deprecated in version 9.0 and will likely be removed in a future release.

                  ===========================================
                  =       _              _ ____  ____       =
                  =      | | _____  __ _| |  _ \| __ )      =
                  =      | |/ / __|/ _` | | | | |  _ \      =
                  =      |   <\__ \ (_| | | |_| | |_) |     =
                  =      |_|\_\___/\__, |_|____/|____/      =
                  =                   |_|                   =
                  =        The Database purpose-built       =
                  =        for stream processing apps       =
                  ===========================================

Copyright 2017-2022 Confluent Inc.

CLI v0.28.2, Server v0.28.2 located at http://ksqldb-server:8088
Server Status: RUNNING

Having trouble? Type 'help' (case-insensitive) for a rundown of how things work!

ksql>

## 输入SQL命令，测试连接成功
ksql> show streams;

 Stream Name         | Kafka Topic                 | Key Format | Value Format | Windowed
------------------------------------------------------------------------------------------
 KSQL_PROCESSING_LOG | default_ksql_processing_log | KAFKA      | JSON         | false
------------------------------------------------------------------------------------------

```

## **创建Redis-Sink-Connector**

```shell
## 创建Redis-Sink-Connector
ksql> CREATE SINK CONNECTOR redis_sink_connector WITH (
  "connector.class" = 'com.github.jcustenborder.kafka.connect.redis.RedisSinkConnector',
  "tasks.max" = '1',
  "topics" = 'private_topic.redis-events',

  "redis.hosts" = 'redis-uri:6379',
  "redis.cluster.enabled" = false,

  "key.converter" = 'io.confluent.connect.avro.AvroConverter',
  "key.converter.schema.registry.url" = 'http://schema-registry:8081',

  "value.converter" = 'io.confluent.connect.avro.AvroConverter',
  "value.converter.schema.registry.url" = 'http://schema-registry:8081'
);

 Message
----------------------------------------
 Created connector REDIS_SINK_CONNECTOR
----------------------------------------

```

**查看**

```shell
## 查看Connector列表
ksql> show connectors;

 Connector Name       | Type | Class                                                           | Status
-----------------------------------------------------------------------------------------------------------------------------
 REDIS_SINK_CONNECTOR | SINK | com.github.jcustenborder.kafka.connect.redis.RedisSinkConnector | RUNNING (1/1 tasks RUNNING)
-----------------------------------------------------------------------------------------------------------------------------




## 查看某个connector详情
ksql> DESCRIBE CONNECTOR REDIS_SINK_CONNECTOR;

Name                 : REDIS_SINK_CONNECTOR
Class                : com.github.jcustenborder.kafka.connect.redis.RedisSinkConnector
Type                 : sink
State                : RUNNING
WorkerId             : 192.168.128.2:8083

 Task ID | State   | Error Trace
---------------------------------
 0       | RUNNING |
---------------------------------




## 删除connector
ksql> DROP CONNECTOR redis_sink_connector;

```

# 相关资料

[ksqlDB Documentation](https://docs.ksqldb.io/en/latest/how-to-guides/use-connector-management/)

[ksqlDB Quickstart](https://ksqldb.io/quickstart.html?_ga=2.60114468.842746710.1665991169-1677490446.1663818586&_gac=1.149635524.1664180174.CjwKCAjwm8WZBhBUEiwA178UnOhRFxCj0xLDYF4HFarzIwngEoMy26V5u6OfSucnYawoPWkpDgwZSBoCDeoQAvD_BwE)

[Confluent Hub](https://www.confluent.io/hub/)
