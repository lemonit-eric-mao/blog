---
title: "Milvus 术语表"
date: "2023-12-13"
categories: 
  - "milvus"
---

# 术语表

### Databases

> 一个 Milvus 集群最多支持 64 个数据库。 https://milvus.io/docs/manage\_databases.md#Manage-Databases

#### Schema

> 模式是定义数据类型和数据属性的元信息。每个集合都有自己的集合模式，定义集合的所有字段、启用自动ID（主键）分配以及集合描述。集合模式还包括定义字段模式的字段，该字段定义字段的名称、数据类型和其他属性。

#### **`Collection`**

> 在Milvus中，`集合`相当于关系数据库管理系统（RDBMS）中的表。在Milvus中，`集合`用于存储和管理实体。 Milvus的`集合`（Collection）`类似MYSQL的表`，用于组织数据，由一个或多个分区组成 一个Collection由一个或多个分区组成。在创建新`Collection`时，Milvus 会创建一个默认分区`_default` https://milvus.io/docs/create\_collection.md#Create-a-Collection

#### **`Partition`**

> `分区`是集合的一个分割。Milvus支持将集合数据`在物理存储上分为多个部分`，这个过程称为`分区`，每个分区可以包含多个`段`。 Milvus允许将向量数据划分为少数几个`分区`。搜索和其他操作可以限定在一个`分区`中，以提高性能。 https://milvus.io/docs/create\_partition.md#Create-a-Partition

#### **`Segment`**

> `段`是**Milvus`自动创建`的**用于保存插入数据的数据文件。一个集合可以有多个`段`，一个`段`可以包含多个`实体`。 在向量相似性搜索期间，Milvus扫描每个段并返回搜索结果。一个段可以是增长的或封闭的。增长的段持续接收新插入的数据直到被封闭。封闭的段不再接收任何新数据，并将刷新到对象存储，新数据将插入到新创建的增长段中。

#### **`Entity`**

> 实体由代表现实世界对象的一组字段组成。Milvus中的每个实体都由唯一的主键表示。您可以自定义主键，如果不手动配置，Milvus会自动为实体分配主键。

#### **Vector Index**

> 向量索引是从原始数据派生出的重新组织的数据结构，可以大大加速向量相似性搜索的过程。Milvus支持多种向量索引类型。 向量索引是用于加速向量相似度搜索的元数据组织单位。**`如果没有`在向量上构建索引，Milvus将执行一次暴力搜索。** https://milvus.io/docs/build\_index.md#Build-an-Index-on-Vectors

#### Sharding

> 分片是将写操作分布到不同节点的过程，以充分利用Milvus集群的并行计算潜力。默认情况下，一个集合包含两个分片。Milvus采用基于主键哈希的分片方法。Milvus的开发路线图包括支持更灵活的分片方法，如随机和自定义分片。

#### Bitset

> 在Milvus中，Bitset是由0和1组成的位数数组，可用于紧凑高效地表示特定数据，与`int`、`float`或`char`相比。位数默认为0，只有在满足特定要求时才设置为1。

#### Channel

> Milvus中有两种不同的通道：PChannel和VChannel。每个PChannel对应于日志存储的主题，而每个VChannel对应于集合中的一个分片。

#### Dependency

> 依赖是另一个程序依赖于其正常工作的程序。Milvus的依赖包括`etcd`（存储元数据）、`MinIO`或`S3`（对象存储）和`Pulsar`（管理快照日志）。

#### Field

> 字段是构成实体的单元。字段可以是结构化数据（例如数字、字符串）或向量。从Milvus 2.0开始，支持标量字段过滤。

#### Log Broker

> 日志代理是支持回放的发布-订阅系统，负责流数据持久化、可靠异步查询执行、事件通知以及查询结果返回。它还确保在工作节点从系统故障中恢复时增量数据的完整性。

#### Log Sequence

> 日志序列记录Milvus中更改集合状态的所有操作。

#### Log Snapshot

> 日志快照是二进制日志，是记录和处理Milvus向量数据库中数据更新和更改的较小单元。Milvus中有三种类型的二进制日志：InsertBinlog、DeleteBinlog和DDLBinlog。

#### Log Subscriber

> 日志订阅者订阅日志序列以更新本地数据，并以只读副本的形式提供服务。

#### Message Storage

> 消息存储是Milvus的日志存储引擎。

#### Milvus Cluster

> 在Milvus的集群部署中，一组节点提供服务，实现高可用性和易扩展性。

#### Milvus Standalone

> 在Milvus的独立部署中，包括数据插入、索引构建和向量相似性搜索在内的所有操作都在单个进程中完成。

#### Normalization

> 归一化是将嵌入（向量）转换为其范数等于一的过程。如果使用内积（IP）计算嵌入相似性，所有嵌入都必须经过归一化。归一化后，内积等于余弦相似性。

#### PChannel

> PChannel代表物理通道，每个PChannel对应于日志存储的主题。默认情况下，Milvus集群启动时将分配一组256个PChannel来存储记录数据插入、删除和更新的日志。

#### Unstructured Data

> 非结构化数据包括图像、视频、音频和自然语言等不遵循预定义模型或组织方式的信息。这种数据类型占据了世界数据的约80%，可以使用各种人工智能（AI）和机器学习（ML）模型转换为向量。

#### VChannel

> VChannel代表逻辑通道，每个VChannel表示集合中的一个分片。每个集合将被分配一组VChannel，用于记录数据的插入、删除和更新。VChannels在逻辑上是分离的，但在物理上共享资源。

#### Embedding Vector

> 嵌入向量是非结构化数据（如电子邮件、物联网传感器数据、Instagram照片、蛋白质结构等）的特征抽象。从数学角度来说，嵌入向量是浮点数或二进制数组。现代嵌入技术用于将非结构化数据转换为嵌入向量。

#### Vector Similarity Search

> 向量相似性搜索是将向量与数据库进行比较，以找到与目标搜索向量最相似的向量的过程。使用近似最近邻（ANN）搜索算法计算向量之间的相似性。
