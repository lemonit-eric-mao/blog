---
title: "使用 KSQL 连接 kakfa connector"
date: "2022-10-20"
categories: 
  - "ksql"
---

## 前置资料

##### [Kafka Connecotr 官方概念](https://docs.confluent.io/platform/current/connect/concepts.html#connectors)

##### [什么是 Kafka Connect？](https://docs.taosdata.com/third-party/kafka/#%E4%BB%80%E4%B9%88%E6%98%AF-kafka-connect "什么是 Kafka Connect？")

> Kafka Connect 是 Apache Kafka 的一个组件，用于使其它系统，比如数据库、云服务、文件系统等能方便地连接到 Kafka。 数据既可以通过 Kafka Connect 从其它系统流向 Kafka, 也可以通过 Kafka Connect 从 Kafka 流向其它系统。 从其它系统读数据的插件称为 Source Connector, 写数据到其它系统的插件称为 Sink Connector。 Source Connector 和 Sink Connector 都不会直接连接 Kafka Broker，Source Connector 把数据转交给 Kafka Connect。Sink Connector 从 Kafka Connect 接收数据。

![](images/KafkaConnect.png)

* * *

# KSQL概念

## 1\. KSQL是什么？

- KSQL是Apache Kafka的流式SQL引擎，让你可以SQL语方式句执行流处理任务。
    
- KSQL降低了数据流处理这个领域的准入门槛，为使用Kafka处理数据提供了一种简单的、完全交互的SQL界面。你不再需要用Java或Python之类的编程语言编写代码了！
    
- KSQL具有这些特点：开源（采用Apache 2.0许可证）、分布式、可扩展、可靠、实时。它支持众多功能强大的数据流处理操作，包括**聚合、连接、加窗（windowing）和sessionization**（捕获单一访问者的网站会话时间范围内所有的点击流事件）等等。
    

## 2\. KSQL能解决什么问题？

- **流式ETL**
    
    Apache Kafka是为数据管道的流行选择。 KSQL使得在管道中转换数据变得简单，准备好消息以便在另一个系统中干净地着陆。
    
- **实时监控和分析**
    
    通过快速构建实时仪表板，生成指标以及创建自定义警报和消息，跟踪，了解和管理基础架构，应用程序和数据源。
    
- **数据探索和发现**
    
    在Kafka中导航并浏览您的数据。
    
- **异常检测**
    
    通过毫秒级延迟识别模式并发现实时数据中的异常，使您能够正确地表现出异常事件并分别处理欺诈活动。
    
- **个性化**
    
    为用户创建数据驱动的实时体验和洞察力。
    
- **传感器数据和物联网**
    
    理解并提供传感器数据的方式和位置。
    
- **客户360视图**
    
    通过各种渠道全面了解客户的每一次互动，实时不断地整合新信息。
    

## 3.KSQL组件

- **KSQL服务器**
    
    KSQL服务器运行执行KSQL查询的引擎。这包括处理，读取和写入目标Kafka集群的数据。 KSQL服务器构成KSQL集群，可以在容器，虚拟机和裸机中运行。您可以在实时操作期间向/从同一KSQL群集添加和删除服务器，以根据需要弹性扩展KSQL的处理能力。您可以部署不同的KSQL集群以实现工作负载隔离。
    
- **KSQL CLI**
    
    你可以使用KSQL命令行界面（CLI）以交互方式编写KSQL查询。 KSQL CLI充当KSQL服务器的客户端。对于生产方案，您还可以将KSQL服务器配置为以非交互式“无头”配置运行，从而阻止KSQL CLI访问。
    

KSQL服务器，客户端，查询和应用程序在Kafka brokers之外，在单独的JVM实例中运行，或者在完全独立的集群中运行。

* * *

# POC验证

## 部署 Kafka服务端

- **创建工作目录**
    
    ```shell
    mkdir -p kafka-server/config/  schema-registry/config/  ksql/config/plugins/  redis/config/
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
      KSQL_CONNECT_KEY_CONVERTER: "io.confluent.connect.avro.AvroConverter"
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

**按顺序启动所有服务**

```shell
docker-compose -f kafka-server/docker-compose.yaml up -d
docker-compose -f redis/docker-compose.yaml up -d

docker-compose -f schema-registry/docker-compose.yaml up -d
docker-compose -f ksql/docker-compose.yaml up -d

```

* * *

# 应用 Connector 插件

## 集成 connect-redis 插件

**注意 `ksqldb-server:0.28.2` 对应 `jaredpetersen/kafka-connect-redis-1.2.0.jar` 不能高于此版本**

```shell
wget -P ksql/config/plugins/connect-redis/ https://repo1.maven.org/maven2/io/github/jaredpetersen/kafka-connect-redis/1.2.0/kafka-connect-redis-1.2.0.jar --no-check-certificate

## 或者 二选一
wget -P ksql/config/plugins/connect-redis/ https://github.com/jaredpetersen/kafka-connect-redis/releases/download/1.2.0/kafka-connect-redis-1.2.0.jar --no-check-certificate

```

**重新部署 ksqldb-server**

```shell
docker-compose -f ksql/docker-compose.yaml down
docker-compose -f ksql/docker-compose.yaml up -d

```

**查看内置 connector 是否启动成功**

```shell
## 需要多等待一会儿

## 验证 Connector 是否启动成功
docker-compose -f ksql/docker-compose.yaml exec ksqldb-server curl localhost:8083

{"version":"7.3.0-cc-docker-ksql.119-33-ccs","commit":"8798a7293c174267","kafka_cluster_id":"1bgVxWdoTAyg4CC_j5FpKA"}


## 验证 Connector Java线程是否运行
docker-compose -f ksql/docker-compose.yaml exec ksqldb-server jstack KsqlServerMain | grep DistributedHerder-connect

"DistributedHerder-connect-1-1" #96 prio=5 os_prio=0 cpu=5721.00ms elapsed=4020.77s tid=0x00007fc56ea47000 nid=0x97 runnable  [0x00007fc5005a6000]

```

### **使用 ksql 建立 connector-redis**

```shell
[root@centos siyu.mao]# docker-compose -f ksql/docker-compose.yaml exec ksqldb-cli ksql http://ksqldb-server:8088

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

**创建Redis-Sink-Connector**

```shell
## 创建Redis-Sink-Connector
ksql> CREATE SINK CONNECTOR redis_sink_connector_ja WITH (
  "connector.class" = 'io.github.jaredpetersen.kafkaconnectredis.sink.RedisSinkConnector',
  "tasks.max" = '1',
  "topics" = 'private_topic.redis-events',

  -- Redis配置
  "redis.uri" = 'redis://redis-uri:6379',
  "redis.cluster.enabled" = false,

  "key.converter" = 'io.confluent.connect.avro.AvroConverter',
  "key.converter.schema.registry.url" = 'http://schema-registry:8081',

  "value.converter" = 'io.confluent.connect.avro.AvroConverter',
  "value.converter.schema.registry.url" = 'http://schema-registry:8081'
);

 Message
-------------------------------------------
 Created connector REDIS_SINK_CONNECTOR_JA
-------------------------------------------

```

**查看**

```shell
## 查看Connector列表
ksql> show connectors;

 Connector Name          | Type | Class                                                             | Status
----------------------------------------------------------------------------------------------------------------------------------
 REDIS_SINK_CONNECTOR_JA | SINK | io.github.jaredpetersen.kafkaconnectredis.sink.RedisSinkConnector | RUNNING (1/1 tasks RUNNING)
----------------------------------------------------------------------------------------------------------------------------------




## 查看某个connector详情
ksql> DESCRIBE CONNECTOR REDIS_SINK_CONNECTOR_JA;

Name                 : REDIS_SINK_CONNECTOR_JA
Class                : io.github.jaredpetersen.kafkaconnectredis.sink.RedisSinkConnector
Type                 : sink
State                : RUNNING
WorkerId             : 192.168.48.2:8083

 Task ID | State   | Error Trace
---------------------------------
 0       | RUNNING |
---------------------------------




## 删除connector
ksql> DROP CONNECTOR redis_sink_connector_ja;

```

* * *

## 集成 connect-mm2 插件

**从`confluentinc/cp-kafka-connect-base`镜像中提取所需的jar包**

```shell
cat > ksql/docker-compose-mm2.yaml<< ERIC
version: '3.6'
services:
  cp-mm2:
    image:  confluentinc/cp-kafka-connect-base:6.1.0
    container_name: cp-mm2
    privileged: true
    user: root
    volumes:
      - ./config/plugins/connect-mm2:/plugins
    entrypoint: |
      cp /usr/share/java/kafka/connect-mirror-6.1.0-ccs.jar /plugins &&
      cp /usr/share/java/kafka/connect-mirror-client-6.1.0-ccs.jar /plugins

ERIC

docker-compose -f ksql/docker-compose-mm2.yaml up -d

```

**重新部署 ksqldb-server**

```shell
docker-compose -f ksql/docker-compose.yaml down
docker-compose -f ksql/docker-compose.yaml up -d

```

**查看内置 connector 是否启动成功**

```shell
## 需要多等待一会儿

## 验证 Connector 是否启动成功
docker-compose -f ksql/docker-compose.yaml exec ksqldb-server curl localhost:8083

{"version":"7.3.0-cc-docker-ksql.119-33-ccs","commit":"8798a7293c174267","kafka_cluster_id":"1bgVxWdoTAyg4CC_j5FpKA"}


## 验证 Connector Java线程是否运行
docker-compose -f ksql/docker-compose.yaml exec ksqldb-server jstack KsqlServerMain | grep DistributedHerder-connect

"DistributedHerder-connect-1-1" #96 prio=5 os_prio=0 cpu=5721.00ms elapsed=4020.77s tid=0x00007fc56ea47000 nid=0x97 runnable  [0x00007fc5005a6000]

```

### **使用 ksql 建立 connector-mm2**

```shell
[root@centos siyu.mao]# docker-compose -f ksql/docker-compose.yaml exec ksqldb-cli ksql http://ksqldb-server:8088

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

**创建MM2-Connector**

```shell
## 创建 MM2-Connector
ksql> CREATE SOURCE CONNECTOR mm2_connector WITH (
  'connector.class' = 'org.apache.kafka.connect.mirror.MirrorSourceConnector',
  'tasks.max' = '3',
  -- 私有云kafka上需要有能够与它匹配上的Topic
  'topics' = 'private_topic.*',

  -- 私有云配置
  'source.cluster.alias' = 'Private_Cloud_DC',
  'source.cluster.bootstrap.servers' = '192.168.101.31:9094',

  -- 公有云
  'target.cluster.alias' = 'Public_Cloud_DC',
  'target.cluster.bootstrap.servers' = '192.168.101.30:9094',

  'key.converter' = 'org.apache.kafka.connect.converters.ByteArrayConverter',
  'value.converter' = 'org.apache.kafka.connect.converters.ByteArrayConverter'
);

 Message
---------------------------------
 Created connector MM2_CONNECTOR
---------------------------------

```

**查看**

```shell
## 查看Connector列表
ksql> show connectors;

 Connector Name | Type   | Class                                                 | Status
---------------------------------------------------------------------------------------------------------------
 MM2_CONNECTOR  | SOURCE | org.apache.kafka.connect.mirror.MirrorSourceConnector | RUNNING (1/1 tasks RUNNING)
---------------------------------------------------------------------------------------------------------------




## 查看某个connector详情
ksql> DESCRIBE CONNECTOR MM2_CONNECTOR;

Name                 : MM2_CONNECTOR
Class                : org.apache.kafka.connect.mirror.MirrorSourceConnector
Type                 : source
State                : RUNNING
WorkerId             : 172.31.0.2:8083

 Task ID | State   | Error Trace
---------------------------------
 0       | RUNNING |
---------------------------------





## 删除connector
ksql> DROP CONNECTOR mm2_connector;

```

## 相关资料

[ksqlDB Documentation](https://docs.ksqldb.io/en/latest/how-to-guides/use-connector-management/)

[ksqlDB Quickstart](https://ksqldb.io/quickstart.html?_ga=2.60114468.842746710.1665991169-1677490446.1663818586&_gac=1.149635524.1664180174.CjwKCAjwm8WZBhBUEiwA178UnOhRFxCj0xLDYF4HFarzIwngEoMy26V5u6OfSucnYawoPWkpDgwZSBoCDeoQAvD_BwE)
