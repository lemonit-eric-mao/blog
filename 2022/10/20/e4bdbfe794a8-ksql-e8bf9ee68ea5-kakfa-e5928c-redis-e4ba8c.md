---
title: '使用 KSQL 连接 kakfa 和 redis 二'
date: '2022-10-20T05:32:16+00:00'
status: private
permalink: /2022/10/20/%e4%bd%bf%e7%94%a8-ksql-%e8%bf%9e%e6%8e%a5-kakfa-%e5%92%8c-redis-%e4%ba%8c
author: 毛巳煜
excerpt: ''
type: post
id: 9473
category:
    - KSQL
tag: []
post_format: []
wb_sst_seo:
    - 'a:3:{i:0;s:0:"";i:1;s:0:"";i:2;s:0:"";}'
hestia_layout_select:
    - sidebar-right
---
POC验证
=====

此方案使用 `jcustenborder/kafka-connect-redis` 插件来实现kafka数据同步到Redis

部署 Kafka服务端
-----------

- **创建工作目录**```shell
  mkdir -p kafka-server/config schema-registry/config ksql/config redis/config
  
  ```
- **kafka单节点部署**```shell
  cat > kafka-server/docker-compose.yaml 
  ```

部署 Redis
--------

```shell
cat > redis/docker-compose.yaml 
```

部署 schema-registry
------------------

```shell
cat > schema-registry/docker-compose.yaml 
```

部署 ksql
-------

目前confluent KSQL支持两种方式，一种是ksql-cli，一种是rest

```yaml
cat > ksql/docker-compose.yaml 
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

- - - - - -

**使用 ksql 建立 connector**
========================

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
                  =      |   

## 输入SQL命令，测试连接成功
ksql> show streams;

 Stream Name         | Kafka Topic                 | Key Format | Value Format | Windowed
------------------------------------------------------------------------------------------
 KSQL_PROCESSING_LOG | default_ksql_processing_log | KAFKA      | JSON         | false
------------------------------------------------------------------------------------------


```

**创建Redis-Sink-Connector**
--------------------------

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

相关资料
====

[ksqlDB Documentation](https://docs.ksqldb.io/en/latest/how-to-guides/use-connector-management/)

[ksqlDB Quickstart](https://ksqldb.io/quickstart.html?_ga=2.60114468.842746710.1665991169-1677490446.1663818586&_gac=1.149635524.1664180174.CjwKCAjwm8WZBhBUEiwA178UnOhRFxCj0xLDYF4HFarzIwngEoMy26V5u6OfSucnYawoPWkpDgwZSBoCDeoQAvD_BwE)

[Confluent Hub](https://www.confluent.io/hub/)