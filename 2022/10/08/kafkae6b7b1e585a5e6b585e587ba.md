---
title: Kafka深入浅出
date: '2022-10-08T16:02:29+00:00'
status: private
permalink: /2022/10/08/kafka%e6%b7%b1%e5%85%a5%e6%b5%85%e5%87%ba
author: 毛巳煜
excerpt: ''
type: post
id: 9404
category:
    - Kafka
tag: []
post_format: []
wb_sst_seo:
    - 'a:3:{i:0;s:0:"";i:1;s:0:"";i:2;s:0:"";}'
hestia_layout_select:
    - sidebar-right
---
**什么是Kafka?**
-------------

**Apache Kafka®** 是一个**分布式事件流处理平台**。

**Kafka** 结合了三个关键功能:

1. **消息系统**(发布/订阅) **Kafka** 和传统的消息中间件都具备**系统解耦**、**冗余存储**、**流量削峰**、**缓冲**、**异步通信**、**扩展性**、**可恢复性**等功能。
  
  **Kafka** 还提供了大多数消息系统难以实现的**消息顺序性保障**及**回溯消费**的功能。
2. **存储系统**(存储事件流)
  
  **Kafka** `把消息持久化到磁盘`，相比于其它基于内存存储的中间件而言，有效的`降低了数据丢失的风险`。
  
  也正是得益于 **Kafka** 的`消息持久化`功能和`多副本`机制，我们可以把 **Kafka** 作为长期的数据存储系统来使用，只需要把对应的`数据保留策略`设置为 **永久** 或 启用 **Topic** 的`日志压缩`功能即可。
3. **流式处理平台**(处理事件流)
  
  **Kafka** 不仅为每个流行的流式处理框架提供了可靠的数据来源，还提供了一个**完整的流式处理类库**，比如**窗口**、**连接**、**变换**和**聚合**等种类操作。

- - - - - -

### **消息队列的两种模式**

- **点对点模式**
  
  
  - 只有一个主题【Topic】
  - 消费者主动拉取数据，消息收到后消息数据  
      [  
      <image src="http://qiniu.dev-share.top/image/kafka/kafka-message-queue-01.gif" width="500px"></image>  ](http://qiniu.dev-share.top/image/kafka/kafka-message-queue-01.gif)
- **发布/订阅模式**
  - 可以有多个主题【Topic】（浏览、点赞、收藏、评论等）
  - 消费者消费数据之后，不删除消息数据
  - 可以有多个消费者，每个消费者相互独立，都可以消费到数据
  
  [  
  <image src="http://qiniu.dev-share.top/image/kafka/kafka-message-queue-02.png" width="500px"></image>  ](http://qiniu.dev-share.top/image/kafka/kafka-message-queue-02.png)

- - - - - -

- - - - - -

- - - - - -

**Kafka 基本概念**
--------------

- **Producer**：生产者 
  - 将数据发送到 **Broker**
- **Broker**：服务代理节点 
  - 负责将收到的消息存储到**磁盘**中
- **Consumer**：消费者
  
  
  - 负责从 **Broker** 订阅并消费消息
  
  [  
  <image src="http://qiniu.dev-share.top/image/kafka/Kafka%E5%B7%A5%E4%BD%9C%E5%8E%9F%E7%90%86.png" width="500px"></image>  ](http://qiniu.dev-share.top/image/kafka/Kafka%E5%B7%A5%E4%BD%9C%E5%8E%9F%E7%90%86.png)

> 生产者、消费者的概念基本所有人都知道，那么这里主要讲一下 **Broker**

- - - - - -

### **Broker** 服务代理节点

- 对于 **Kafka** 而言， **Broker** 可以简单地看作一个独立的 【**Kafka** 服务节点】或 【**Kafka** 服务实例】 。
- 大多数情况下也可以将 **Broker** 看作一台 **Kafka** 服务器，前提是这台服务器上只部署了一个 **Kafka** 实例。
- 一个或多个 **Broker** 组成了一个 **Kafka** 集群

> **Kafka** 中还有两个特别重要的概念 **主题**(Topic) 与 **分区**(Partition)

- - - - - -

### **主题(Topic)**

- **Kafka** 中的消息以 **主题** 为单位进行归类，**生产者负责将消息发送到特定的主题** ，发送到 **Kafka** 集群中的每一条消息都要指定一个 **主题** ，而 **消费者负责订阅主题** 并进行消费
- **主题** 是一个**逻辑上的概念**，它可以被细分为多个 **分区**

- - - - - -

### **分区(Partition)**

- **分区** 很多时候也会把分区称为 **主题分区(Topic-Partition)** 即基于主题的 **物理分区**。
- **同一个主题**的**不同分区**包含的消息是不同的，**分区在存储层面**可以看作是一个**可追加的日志文件(Append Log**)，消息在被追加到分区日志文件的时候都会分配一个特定的 **偏移量(offset)**。
- 一个分区一个队列

- - - - - -

### **偏移量(Offset)**

- **offset** 是消息在分区中的唯一标识，**Kafka** 通过 **Offset** 来保证**消息在分区内的顺序性**，不过 **Offset** 并不跨越分区，也就是说，**Kafka** 保证的是**分区有序**而**不是主题有序**

- - - - - -

- - - - - -

- - - - - -

**基础架构图-主题与分区结构-分区单副本**
-----------------------

[  
 <image src="http://qiniu.dev-share.top/image/kafka/Kafka%E5%B7%A5%E4%BD%9C%E5%8E%9F%E7%90%86-%E4%B8%BB%E9%A2%98%E4%B8%8E%E5%88%86%E5%8C%BA%E7%BB%93%E6%9E%84.png" width="500px"></image>  
 ](http://qiniu.dev-share.top/image/kafka/Kafka%E5%B7%A5%E4%BD%9C%E5%8E%9F%E7%90%86-%E4%B8%BB%E9%A2%98%E4%B8%8E%E5%88%86%E5%8C%BA%E7%BB%93%E6%9E%84.png)

- 每条消息被发送到 **broker** 之前，会根据分区规则选择存储到哪个具体的分区。
- 如果分区规则设定的合理，所有的消息都可以均匀地分配到不同的分区中。
- **如果一个主题只对应一个文件，那么这个文件所在的机器 I/O 将会成为这个主题的性能瓶颈，而分区解决了这个问题**。

- - - - - -

- - - - - -

- - - - - -

**基础架构图-分区多副本(Replica)**
------------------------

- **Kafka** 为分区引入了多副本机制，通过增加副本数量来提升容灾能力。
- 同一分区的不同副本中保存的是相同的消息（在同一时刻，副本之间并非完全一样）
- 副本之间是 **一主多从** 的关系，其中 【**leader** 副本负责处理读写请求】，**follower** 副本只负责与 **leader** 副本的消息同步。
- 副本处于不同的 **broker** 中，当 **leader** 副本出现故障时，从 **follower** 副本中重新选举新的 **leader** 副本对外提供服务。
- **Kafka** 通过副本机制实现了故障的自动转移。

[  
 <image src="http://qiniu.dev-share.top/image/kafka/Kafka%E5%B7%A5%E4%BD%9C%E5%8E%9F%E7%90%86-%E5%88%86%E5%8C%BA%E5%A4%9A%E5%89%AF%E6%9C%AC.png" width="500px"></image>  ](http://qiniu.dev-share.top/image/kafka/Kafka%E5%B7%A5%E4%BD%9C%E5%8E%9F%E7%90%86-%E5%88%86%E5%8C%BA%E5%A4%9A%E5%89%AF%E6%9C%AC.png)

- - - - - -

- - - - - -

- - - - - -

生产者工作原理
-------

将外部接收过来的数据，传送到 **kafka** 集群

[  
 <image src="http://qiniu.dev-share.top/image/kafka/Kafka%E5%B7%A5%E4%BD%9C%E5%8E%9F%E7%90%86-%E7%94%9F%E4%BA%A7%E8%80%85-%E5%8E%9F%E7%90%86.png" width="500px"></image>  ](http://qiniu.dev-share.top/image/kafka/Kafka%E5%B7%A5%E4%BD%9C%E5%8E%9F%E7%90%86-%E7%94%9F%E4%BA%A7%E8%80%85-%E5%8E%9F%E7%90%86.png)

### **说明**

**RecordAccumulator**  
 分区器-缓冲区内存总大小 【默认 **32M**】

**ProducerBatch**  
 一个分区一个队列，每个队列中的每一批次消息数据的大小【 默认 **16k**】

**batch.size:**  
 只有队列中的数据积累到**batch.size**之后，**sender**才会发送数据。【默认**16K**】

**linger.ms:**  
 如果数据迟迟未达到**batch.size**，**sender**等待**linger.ms**设置时间到了之后就会发送数据。单位**ms**，默认值是 **0ms**，表示没有延迟。

**compression.type:**  
 压缩snappy

- - - - - -

### **ACKS应答**

- 0 生产者发送过来的数据，不需要等数据落盘应答。
- **1** 生产者发送过来的数据，**Leader**收到数据后应答。
- **-1 (all)** 生产者发送过来的数据，**Leader** 和 **ISR** 队列里面所有的节点收齐数据后应答。**-1** 和 **all** 等价。**kafka的acks默认值**

- - - - - -

### **ACK应答原理**

- **ACK应答**是指在leader分区接收到生产者的数据后，何时对生产者做出应答的策略。 
  - ACK可选的值有【0，1，-1】三个，可以在生产者的配置项 **acks** 中设置，**ACK**设置不同，对生产者做出应答的时机也不同。
- **ACK=0**
  - 可靠性 **差**，效率高。
  - leader收到生产者数据后不需要等数据落盘，立即对生产者做出应答。
  - 生产者收到应答后认为leader已成功接收数据，因此不需要再发当前数据了。
  - 但是，如果leader在将内存中的数据落盘时突然出现故障，那么这条数据因为没有保存到磁盘中而导致**数据的丢失**。
- **ACK=1**
  - 可靠性 **中等**，效率中等。
  - leader收到生产者的数据并将数据落盘后，对生产者做出应答。
  - 生产者收到应答后继续发送其他数据。
  - 如果leader做出应答并且follower未同步到该数据时，leader出现故障。
  - kafka会重新在follower中选出新的leader，而新的leader心有同步到数据，生产者也不会再发该数据，因此导致该**数据的丢失**。
- **ACK=-1（all）**
  - 可靠性 **高**，效率低。
  - **kafka的acks默认值**。
  - leader收到数据并落盘，并且确认所有follower收到数据后再给生产者应答。
  - 此时，所有分区副本都有该数据了，即使任意分区出现故障数据仍然是完整的。

- - - - - -

### **ISR**

- 就像追女孩子一样，我们把所有有机会追到的对象都放在同一个列表里，经常同她们发消息，其中不免会有对你爱答不理的，那还要继续追吗？肯定是要及时止损的啦，只留下成功率大的岂不美哉。
- kafka也一样，它的 **Leader** 维护了一个动态的 **in-sync replica set，简称ISR**，意为和 **Leader** 保持同步的**Follower 和 Leader** 的集合。 
  - ISR里面存放的是正常工作的**Follower 和 Leader** 的集合。数据结构如：**(leader: 0, isr: 0,1,2)**。
  - 如果**Follower**长时间未向**Leader**同步数据 ，则该**Follower**将被踢出**ISR**。被踢出的**Follower**将会放在**OSR**中。
  - 该时间阈值由配置文件中**replica.lag.time.max.ms**参数设定，【默认 **30秒**】。例如**Follower 2**超时：**(leader: 0, isr: 0,1)**。
  - Leader发生故障之后，就会从ISR中选举新的leader。

- - - - - -

### **数据可靠性**

- **保证数据完全可靠条件**
  - ACK级别设置为**-1**
  - 分区副本大于等于**2**
  - ISR里应答的最小副本数量大于等于**2** (**min.insync.replicas = 2**)
- **数据去重**
  
  
  - **幂等性**
  - 幂等性，就是指**Producer**不论向**Broker**发送多少次重复数据，**Broker**端都只会持久化一条，保证不重复
  - 【**至少一次 (At Least Once)**】
  - ACK级别设置为-1 + 分区副本大于等于2 + ISR里应答的最小副本数量大于等于2
  - 可以保证数据不丢失，但是不能保证数据不重复
  - 【**最多一次 (At Most Once)**】
  - ACK级别设置为0
  - 可以保证数据不重复，但是不能保证数据不丢失
  - 【**精确一次 (Exactly Once)**】
  - 幂等性 + 至少一次 (ack=-1 + 分区副本数&gt;=2 + ISR最小副本数量&gt;= 2)
- **Kafka幂等性原理**
  - 具有**<pid partition="" seqnumber=""></pid>**相同主键的消息提交时， **Broker** 只会持久化一条。其中**PID是生产者ID，Kafka每次重启都会分配一个新的；Partition表示分区号；SequenceNumber是单调自增的**
  - 所以幂等性【只能保证的是在单分区单会话内不重复】
- **生产者事务**
  - 开启事务必须开启幂等性，因为事务依赖幂等性。
  - 开启事务，会在Kafka集群中每一个broker中开启一个事务协调器
  - 事务的划分是根据 【**transactional.id的hashcode值 % 分区数**】，计算出该事务属于哪个分区。
  
  [  
   <image src="http://qiniu.dev-share.top/image/kafka/producer-transactional.png" width="500px"></image>  ](http://qiniu.dev-share.top/image/kafka/producer-transactional.png)

- - - - - -

- - - - - -

- - - - - -

**生产者-数据乱序**
------------

[  
 <image src="http://qiniu.dev-share.top/image/kafka/producer-disorder.png" width="500px"></image>  ](http://qiniu.dev-share.top/image/kafka/producer-disorder.png)

- - - - - -

- - - - - -

- - - - - -

**消费者工作原理**
-----------

[  
 <image src="http://qiniu.dev-share.top/image/kafka/image-20220928103144242.png" width="500px"></image>  ](http://qiniu.dev-share.top/image/kafka/image-20220928103144242.png)

- 消费者和消费者之间**相互独立**
- 消费者为了提高消费能力，诞生了**消费者组** （某个分区 只能由一个消费者消费）
- 如果不明确指定消费者组ID，每个消费者都有一个**默认分配的组ID**
- 当多个消费者，明确指定为**同一个组ID**时，就会诞生**消费者组**
- **一个生产者** --&gt; **多个主题分区(Topic-Partition-`*`)** --&gt; **一组消费者(Consumer Group)**
  - [  
      <image src="http://qiniu.dev-share.top/image/kafka/Kafka%E5%B7%A5%E4%BD%9C%E5%8E%9F%E7%90%86-%E7%94%9F%E4%BA%A7%E8%80%85-%E6%B6%88%E8%B4%B9%E8%80%85-%E5%B7%A5%E4%BD%9C%E5%8E%9F%E7%90%86.png" width="500px"></image>  ](http://qiniu.dev-share.top/image/kafka/Kafka%E5%B7%A5%E4%BD%9C%E5%8E%9F%E7%90%86-%E7%94%9F%E4%BA%A7%E8%80%85-%E6%B6%88%E8%B4%B9%E8%80%85-%E5%B7%A5%E4%BD%9C%E5%8E%9F%E7%90%86.png)
- 建议： 
  - 通常情况下一个**消费者组(Consumer Group)** 对应一个**主题分区(Topic)**
  - 一个**主题分区(Topic)**对应一类数据，一类数据由同一类**生产者**产出

### 消费者默认的分区分配策略

> **消费者组**，**不会重复消费同一个分区**，更确切的说，是消费者组内的所有成员都不会做重复消费分区的事

### 再均衡(Rebalance)

> - 再均衡是指分区的所属权**从一个消费者转移到另一个消费者**的行为，它为消费组具备高可用性和伸缩性提供保障 
>   - 使我们可以既方便又安全地**删除消费组内的消费者**或往**消费组内添加消费者**
> - 不过在再均衡发生期间，消费组内的消费者是无法读取消息的 
>   - 也就是说，在再均衡发生期间的这一小段时间内，消费组会变得不可用
> - 另外，当一个分区被重新分配给另一个消费者时，消费者当前的状态也会丢失 
>   - 比如消费者消费完某个分区中的一部分消息时**还没有来得及提交消费位移**就发生了**再均衡**操作，之后这个分区又被分配给了消费组内的另一个消费者，原来被消费完的那部分消息又被重新消费一遍，也就是发生了**重复消费**。
> - 所以**一般情况下**，应**尽量避免**不必要的**再均衡**的发生。

- - - - - -

- - - - - -

- - - - - -

### 什么是死信队列？

> 将正常情况下无法被消费的消息称为 **死信消息**（**Dead-Letter Message**）  
>  将存储死信消息的特殊队列称为 **死信队列** （**Dead-Letter Queue**）

- - - - - -

- - - - - -

- - - - - -

### [故障处理-工作原理](http://www.dev-share.top/2022/10/08/kafka%e6%b7%b1%e5%85%a5%e6%b5%85%e5%87%ba-%e6%95%85%e9%9a%9c%e5%a4%84%e7%90%86-%e5%b7%a5%e4%bd%9c%e5%8e%9f%e7%90%86/ "故障处理-工作原理")

- - - - - -

- - - - - -

- - - - - -

### [kafka为什么那么快](http://www.dev-share.top/2022/10/08/kafka%e6%b7%b1%e5%85%a5%e6%b5%85%e5%87%ba-kafka%e4%b8%ba%e4%bb%80%e4%b9%88%e9%82%a3%e4%b9%88%e5%bf%ab/ "kafka为什么那么快")