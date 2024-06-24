---
title: "Kafka深入浅出-故障处理-工作原理"
date: "2022-10-08"
categories: 
  - "kafka"
---

## Follower 故障处理-工作原理

#### 名词解释

**LEO** (Log End Offset)

- **LEO**其实就是每个副本当中最后一个**offset + 1**

**HW** (High Watermark) 高水位线

- **HW**其实就是所有副本中最小的**LEO**

[![](http://qiniu.dev-share.top/image/kafka/Follower%20%E6%95%85%E9%9A%9C%E5%A4%84%E7%90%86-%E5%B7%A5%E4%BD%9C%E5%8E%9F%E7%90%86.gif)](http://qiniu.dev-share.top/image/kafka/Follower%20%E6%95%85%E9%9A%9C%E5%A4%84%E7%90%86-%E5%B7%A5%E4%BD%9C%E5%8E%9F%E7%90%86.gif)

## Leader 故障处理-工作原理

[![](http://qiniu.dev-share.top/image/kafka/Leader%20%E6%95%85%E9%9A%9C%E5%A4%84%E7%90%86-%E5%B7%A5%E4%BD%9C%E5%8E%9F%E7%90%86.gif)](http://qiniu.dev-share.top/image/kafka/Leader%20%E6%95%85%E9%9A%9C%E5%A4%84%E7%90%86-%E5%B7%A5%E4%BD%9C%E5%8E%9F%E7%90%86.gif)
