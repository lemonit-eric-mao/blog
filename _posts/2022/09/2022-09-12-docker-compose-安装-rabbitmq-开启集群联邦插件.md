---
title: "docker-compose 安装 RabbitMQ 开启集群联邦插件"
date: "2022-09-12"
categories: 
  - "mq"
---

##### **[理解RabbitMQ工作原理](http://www.dev-share.top/2022/09/09/%e7%90%86%e8%a7%a3-rabbitmq-%e5%b7%a5%e4%bd%9c%e5%8e%9f%e7%90%86/ "理解RabbitMQ工作原理")**

* * *

##### 概述

###### **RabbitMQ Federation** 的类型

> - **RabbitMQ Federation**有两种类型可选，分别是 **Exchange Federation (交换器联邦)** 和 **Queue Federation (队列联邦)**。 **RabbitMQ的联邦**可以是**`单向`联邦**，也可以是**`双向`联邦**，这里的测试都是基于**双向联邦**场景下的实现。

* * *

###### 两种类型分别对应着两种不同的使用场景：

> - **Exchange Federation**
>     - `Exchange Federation` 它实现的是消息的**`复制`**功能，当消息进入到其中任意一个 **联邦 Exchange** 时， 两个 **联邦 Exchange** 之间的**消息是`复制`的**。
>     - 它更适用于**消息重复执行**的场景 ![](images/rabbitmq-exchange-federation.png)

* * *

> - **Queue Federation**
>     - `Queue Federation` 它实现的是消息的**`负载均衡`**功能，当消息进入到其中任意一个 **联邦 Queue** 时，**消息会`分发`**，它的负载策略会受到，**Prefetch count** 配置项的影响
>         - **Prefetch count**：定义Federation内部缓存的消息条数。 即当队列接收到的消息 **`超过`这个设定的阈值时** ，才会向下游联邦队列分发消息。（**此功能需要在代码中调整**）
>             
>             ```go
>             // CreateChannel 建立通道
>             func (mq *RabbitMQ) CreateChannel() {
>                 // 建立通道
>                 ch, err := mq.conn.Channel()
>                 // prefetchCount(预取消息数),
>                 // prefetchSize (预取消息大小),
>                 // global bool  (如果为true，对Channel可用；如果为false，则只对当前队列可用)
>                 ch.Qos(63, 0, false)
>                 tools.FailOnError(err, "操作失败，不能开启一个通道")
>                 mq.ch = ch
>             }
>             ```
>             
>     - 它类似主从的负载模式 ![](images/rabbitmq-queue-federation.png)

**[参考资料01](https://juejin.cn/post/7073669304603901983 "参考资料01")** **[参考资料02](https://www.modb.pro/db/138102 "参考资料02")**

* * *

* * *

* * *

##### 前置条件

- **操作系统**： CentOS 7.9 两台
- **操作系统IP**：`192.168.101.21`、`192.168.101.22`

##### 联邦服务部署

**在 `192.168.101.21`、`192.168.101.22` 两台主机，做如下相同的部署即可，具体联邦的操作是通过 Web页面进行手动配置的**

```ruby
cat > docker-compose.yml << ERIC
version: '3.1'
services:

  rabbitmq:
    container_name: rabbitmq
    image: rabbitmq:3.10.7-management-alpine
    ports:
      - 15672:15672
      - 5672:5672
    restart: always
    # 这个hostname必须写，因为RabbitMQ的数据持久化目录，是根据容器的hostname动态生成的
    hostname: rabbitmq
    volumes:
      - ./data:/var/lib/rabbitmq
      - ./config/enabled_plugins:/etc/rabbitmq/enabled_plugins
    environment:
      RABBITMQ_DEFAULT_USER: admin
      RABBITMQ_DEFAULT_PASS: 123456
      RABBITMQ_DEFAULT_VHOST: default_admin_vhost

ERIC

```

* * *

> - **添加配置文件，用来开启联邦插件**
>     
>     ```ruby
>     cat > ./config/enabled_plugins << ERIC
>     [rabbitmq_management,rabbitmq_prometheus,rabbitmq_federation,rabbitmq_federation_management].
>     ERIC
>     ```
>     

* * *

> - **启动**
>     
>     ```ruby
>     docker-compose up -d
>     ```
>     

* * *

> - **打开浏览器查看** ![](images/rabbitmq-federation-01.png)

* * *

> - **创建联邦** ![](images/rabbitmq-federation-02.png)

* * *

* * *

* * *

##### **[配置RabbitMQ联邦](http://www.dev-share.top/2022/09/12/%e9%85%8d%e7%bd%aerabbitmq%e8%81%94%e9%82%a6/ "配置RabbitMQ联邦")**
