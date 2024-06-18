---
title: "Gossip是什么"
date: "2021-07-06"
categories: 
  - "consul"
---

###### Gossip是什么

   Gossip协议是一个通信协议，**一种`传播`消息的方式**，灵感来自于：瘟疫、社交网络等。使用Gossip协议的有：Redis Cluster、Consul、Apache Cassandra等。

* * *

###### 原理

   Gossip协议基本思想就是：一个节点想要分享一些信息给网络中的其他的一些节点。于是，它周期性的随机选择一些节点，并把信息传递给这些节点。这些收到信息的节点接下来会做同样的事情，即把这些信息传递给其他一些随机选择的节点。一般而言，信息会周期性的传递给N个目标节点，而不只是一个。这个N被称为fanout（这个单词的本意是扇出）。

* * *

###### 用途

   Gossip协议的主要用途就是信息传播和扩散：即把一些发生的事件传播到全世界。它们也被用于数据库复制，信息扩散，集群成员身份确认，故障探测等。

* * *

   基于Gossip协议的一些有名的系统：Apache Cassandra，Redis（Cluster模式），Consul等。

* * *

* * *

###### [参考资料](https://zhuanlan.zhihu.com/p/41228196 "参考资料")

###### [参考资料](https://www.jianshu.com/p/54eab117e6ae "参考资料")

* * *

* * *

* * *
