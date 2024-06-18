---
title: '什么是Flink?'
date: '2022-07-05T01:23:42+00:00'
status: private
permalink: /2022/07/05/%e4%bb%80%e4%b9%88%e6%98%afflink
author: 毛巳煜
excerpt: ''
type: post
id: 8868
category:
    - Flink
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
wb_sst_seo:
    - 'a:3:{i:0;s:0:"";i:1;s:0:"";i:2;s:0:"";}'
---
简述
--

> **计算引擎的发展历史**
> 
> - **第一代**，Hadoop承载的MapReduce
> - **第二代**，带有DAG（Directed Acyclic Graph 有向无环图）框架的计算引擎
> - **第三代**，以Spark为代表的内存计算引擎
> - **第四代**，Flink 把数据计算归为**有界**和**无界**的，**有界**的数据就是**批处理**，**无界**的数据就是**流式**，而且以**流批一体**为终极计算目标

### 什么是 Flink ？

> - **Apache Flink** 是一个在**【有界数据流】**和**【无界数据流】**上进行有状态计算分布式处理引擎和框架。
> - Flink 设计旨在**【所有常见的集群环境】**中运行，以**【任意规模】**和**【内存】**级速度执行计算。

### 什么是CDC ？

> - CDC 是 **Change Data Capture**（变更数据获取）的简称。
> - 核心思想是，**检测**并**捕获数据库**的变动（包括**数据**或**数据表**的插入、更新以及删除等），将这些变更**按发生的顺序**完整记录下来，**写入到消息中间件中**以供其他服务进行订阅及消费。
> - CDC 主要分为两种方式，**基于查询的CDC** 和 **基于Binlog的CDC**
>   
>   
>   - ![flink-cdc-01](http://qiniu.dev-share.top/image/flink-cdc-01.png)

### 什么是 [Debezium](https://debezium.io/) ？

> - **RedHat**开源的**Debezium**是一个**开源分布式平台，用于捕获数据库中的【变更数据】**，支持多种数据库。
> - 它是一种**CDC**工具，是通过抽取数据库日志来获取变更的。
> - 它可以把来自 **MySQL**、**PostgreSQL**、**Oracle**、**Microsoft SQL Server** 和许多其他数据库的更改实时流式传输到**【你期望的目标源】**中。
> - **Debezium** 为变更日志提供了统一的格式结构，并支持使用 **JSON** 和 **Apache Avro** 序列化消息。 
>   - [参考网址](https://nightlies.apache.org/flink/flink-docs-release-1.16/zh/docs/connectors/table/formats/debezium/)

### 什么是 [FlinkCDC](https://ververica.github.io/flink-cdc-connectors/master/content/about.html) ？

> - **Flink** 社区开发了 **flink-cdc-connectors** 组件 （阿里开发的）
> - **FlinkCDC 就是 【Debezium + Flink】**
>   
>   
>   1. 首先，我们使用 **Debezium** 监听数据库的变化，再拿到变化的数据
>   2. 然后，将 **Debezium** 拿到的数据，在传给 **Flink**
>   3. 最后，在使用 **Flink** 进行数据处理，把处理好的数据传给你想要的程序

Flink 能用来干什么？
-------------

> - **[DataStream](https://nightlies.apache.org/flink/flink-docs-release-1.16/docs/dev/datastream/overview/#flink-datastream-api-programming-guide) 用来处理流式计算的**
>   - **[Table API &amp; SQL](https://nightlies.apache.org/flink/flink-docs-release-1.16/docs/dev/table/overview/#table-api--sql) 是另一种用来处理流式计算的方法**
> - **[DataSet](https://nightlies.apache.org/flink/flink-docs-release-1.16/docs/dev/dataset/overview/#dataset-api) 用来做批处理**

当前Demo采用的就是 **【Table &amp; SQL】** 的这种方式

[基于FlinkCDC开发一个应用程序](https://gitee.com/eric-mao/test-flink-cdc/blob/master/README.md)
-------------------------------------------------------------------------------------

[在K8S中安装部署](http://www.dev-share.top/2022/12/13/k8s%e9%83%a8%e7%bd%b2flink-kubernetes-operator/)
------------------------------------------------------------------------------------------------

注意事项
----

> **注意**：虽然 Job 的所有任务都处于 **SCHEDULED** 状态，但整个 **Job** 的状态却显示为 **RUNNING**。
> 
>  此时，由于 **TaskManager** 提供的 **TaskSlots** 资源不够用，**Job** 的所有任务都不能成功转为 `RUNNING` 状态，直到有新的 **TaskManager** 可用。在此之前，该 **Job** 将经历一个取消和重新提交 不断循环的过程。
> 
>  与此同时，数据生成器 (data generator) 一直不断地往 *input* topic 中生成 `ClickEvent` 事件，**在【生产环境】中也经常出现这种 Job 挂掉但源头还在不断产生数据的情况**。

#### 重复的变更事件 [\#](https://nightlies.apache.org/flink/flink-docs-release-1.16/zh/docs/connectors/table/formats/debezium/#%E9%87%8D%E5%A4%8D%E7%9A%84%E5%8F%98%E6%9B%B4%E4%BA%8B%E4%BB%B6)

> 在正常的操作环境下，Debezium 应用能以 **exactly-once** 的语义投递每条变更事件。在这种情况下，Flink 消费 Debezium 产生的变更事件能够工作得很好。 然而，当有故障发生时，Debezium 应用只能保证 **at-least-once** 的投递语义。可以查看 [Debezium 官方文档](https://debezium.io/documentation/faq/#what_happens_when_an_application_stops_or_crashes) 了解更多关于 Debezium 的消息投递语义。 这也意味着，在非正常情况下，Debezium 可能会投递重复的变更事件到 Kafka 中，当 Flink 从 Kafka 中消费的时候就会得到重复的事件。 这可能会导致 Flink query 的运行得到错误的结果或者非预期的异常。因此，建议在这种情况下，将作业参数 [`table.exec.source.cdc-events-duplicate`](https://nightlies.apache.org/flink/flink-docs-release-1.16/zh/docs/dev/table/config/#table-exec-source-cdc-events-duplicate) 设置成 `true`，并在该 source 上定义 PRIMARY KEY。 框架会生成一个额外的有状态算子，使用该 primary key 来对变更事件去重并生成一个规范化的 changelog 流。

#### 消费 Debezium Postgres Connector 产生的数据 [\#](https://nightlies.apache.org/flink/flink-docs-release-1.16/zh/docs/connectors/table/formats/debezium/#%E6%B6%88%E8%B4%B9-debezium-postgres-connector-%E4%BA%A7%E7%94%9F%E7%9A%84%E6%95%B0%E6%8D%AE)

> 如果你正在使用 [Debezium PostgreSQL Connector](https://debezium.io/documentation/reference/1.2/connectors/postgresql.html) 捕获变更到 Kafka，请确保被监控表的 [REPLICA IDENTITY](https://www.postgresql.org/docs/current/sql-altertable.html#SQL-CREATETABLE-REPLICA-IDENTITY) 已经被配置成 `FULL` 了，默认值是 `DEFAULT`。 否则，Flink SQL 将无法正确解析 Debezium 数据。
> 
>  当配置为 `FULL` 时，更新和删除事件将完整包含所有列的之前的值。当为其他配置时，更新和删除事件的 “before” 字段将只包含 primary key 字段的值，或者为 null（没有 primary key）。 你可以通过运行 `ALTER TABLE <your-table-name> REPLICA IDENTITY FULL</your-table-name>` 来更改 `REPLICA IDENTITY` 的配置。 请阅读 [Debezium 关于 PostgreSQL REPLICA IDENTITY 的文档](https://debezium.io/documentation/reference/1.2/connectors/postgresql.html#postgresql-replica-identity) 了解更多。