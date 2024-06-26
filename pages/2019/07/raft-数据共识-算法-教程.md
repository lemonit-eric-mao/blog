---
title: "Raft 数据共识 算法 数据生命的秘密"
date: "2019-07-05"
categories: 
  - "k8s"
---

#### [数据生命的秘密](http://thesecretlivesofdata.com/raft/ "数据生命的秘密")

1. 组成一个Raft集群至少需要三台机器。
    
2. Raft限制每一时刻最多只能有一个节点可以发起提案，这个限制极大的简化了一致性的实现，这个可以发起提案的节点称为 **`Leader`**。
    
3. 例如TiDB中就使用了 raft 共识算法： 其中 `PD、TiKV中的Region` 的选举都使用了 `raft算法`， 所以 `PD的Leader` 就是 `Raft Leader` `Region的Leader` 也是 `Raft Leader`
