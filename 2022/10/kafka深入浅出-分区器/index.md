---
title: "Kafka深入浅出-分区器"
date: "2022-10-08"
categories: 
  - "kafka"
---

## Kafka中所谓的分区器，到底是什么？

- 消息在通过 **send()** 方法发往 **broker** 的过程中，有可能需要经**过拦截（Interceptor）、序列化器（Serializer和分区器（Partitioner）** 的一系列作用之后才能被真正地发往 **broker**。
- **拦截器一般不是必需的**，而**序列化器是必需的**。
- 消息经过序列化之后就需要确定它发往的分区，如果消息 **ProducerRecord** 中指定了 **partition** 字段，那么就不需要分区器的作用，因为 **partition** 代表的就是所要发往的分区号。
- 如果消息 **ProducerRecord** 中没有指定 **partition** 字段，那么就需要依赖分区器，根据 **key** 这个字段来计算 **partition** 的值。
- **分区器的作用就是为消息分配分区**。
- **Kafka** 中提供的**默认分区器**是 **org.apache.kafka.clients.producer.internals.DefaultPartitioner**，它实现了 **org.apache.kafka.clients.producer.Partitioner** 接口

> 代码片段如下：[源码地址](https://github.com/apache/kafka/blob/trunk/clients/src/main/java/org/apache/kafka/clients/producer/internals/DefaultPartitioner.java)

```java
    /**
     * Compute the partition for the given record.
     *
     * @param topic The topic name
     * @param numPartitions The number of partitions of the given {@code topic}
     * @param key The key to partition on (or null if no key)
     * @param keyBytes serialized key to partition on (or null if no key)
     * @param value The value to partition on or null
     * @param valueBytes serialized value to partition on or null
     * @param cluster The current cluster metadata
     */
    public int partition(String topic, Object key, byte[] keyBytes, Object value, byte[] valueBytes, Cluster cluster,
                         int numPartitions) {
        if (keyBytes == null) {
            return stickyPartitionCache.partition(topic, cluster);
        }
        return BuiltInPartitioner.partitionForKey(keyBytes, numPartitions);
    }
```

#### 分区是如何计算的？

[源码地址](https://github.com/apache/kafka/blob/trunk/clients/src/main/java/org/apache/kafka/clients/producer/ProducerRecord.java)

```java
public class ProducerRecord<K, V> {

    private final String topic;
    private final Integer partition;
    private final Headers headers;
    private final K key;
    private final V value;
    private final Long timestamp;

    /**
     * 指明 partition 的情况下，直接将指明的值作为 partition 值；
     * 例如：partition=0，所有数据写入 分区0
     * 
     * 参数key 通常是传入有意义的值，例如：数据库的表名
     * 
     */
    public ProducerRecord(String topic, Integer partition, Long timestamp, K key, V value, Iterable<Header> headers) {
        // 省略具体代码
    }

    public ProducerRecord(String topic, Integer partition, Long timestamp, K key, V value) {
        this(topic, partition, timestamp, key, value, null);
    }

    public ProducerRecord(String topic, Integer partition, K key, V value, Iterable<Header> headers) {
        this(topic, partition, null, key, value, headers);
    }

    public ProducerRecord(String topic, Integer partition, K key, V value) {
        this(topic, partition, null, key, value, null);
    }

    /**
     * 没有指明 partition 值，但是有 key 的情况下，将【key的hash值】与【topic的partition数】进行【取余】得到partition值；
     * 例如：
     *   key1的hash值=5
     *   key2的hash值=6
     *   topic的partition数=2， 
     *     那么(5 % 2)=1，key1对应的【value1写入1号分区】
     *        (6 % 2)=0，key2对应的【value2写入0号分区】
     */
    public ProducerRecord(String topic, K key, V value) {
        this(topic, null, null, key, value, null);
    }

    /**
     * 既没有 partition 值以没有key值的情况下， Kafka采用【粘性分区】，第一次会随机选择一个分区，并尽可能一直使用该分区，
     * 待该分区的batch 已满 或者 已完成， Kafka再随机一个分区进行使用【和上一次的分区不同】。
     */
    public ProducerRecord(String topic, V value) {
        this(topic, null, null, null, value, null);
    }

}
```
