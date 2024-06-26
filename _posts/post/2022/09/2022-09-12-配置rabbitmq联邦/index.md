---
title: "配置RabbitMQ联邦"
date: "2022-09-12"
categories: 
  - "mq"
---

##### 1\. 创建交换机

> [![](images/rabbitmq-federation-03.png)](http://qiniu.dev-share.top/image/rabbitmq-federation-03.png)

##### 2\. 创建队列

> [![](images/rabbitmq-federation-04.png)](http://qiniu.dev-share.top/image/rabbitmq-federation-04.png)

##### 3\. 交换机绑定队列

> [![](images/rabbitmq-federation-05.png)](http://qiniu.dev-share.top/image/rabbitmq-federation-05.png)

##### 4\. 添加联邦上游服务

> [![](images/rabbitmq-federation-06.png)](http://qiniu.dev-share.top/image/rabbitmq-federation-06.png)

##### 5\. 添加策略

> [![](images/rabbitmq-federation-07.png)](http://qiniu.dev-share.top/image/rabbitmq-federation-07.png)

##### 6\. 查看联邦状态

> [![](images/rabbitmq-federation-08.png)](http://qiniu.dev-share.top/image/rabbitmq-federation-08.png)

##### 7\. 登录另一台RabbitMQ 查看上游服务信息

> [![](images/rabbitmq-federation-09.png)](http://qiniu.dev-share.top/image/rabbitmq-federation-09.png)

##### 8\. 登录另一台RabbitMQ 查看上游服务交换机信息

> [![](images/rabbitmq-federation-10.png)](http://qiniu.dev-share.top/image/rabbitmq-federation-10.png)

##### 9\. 上游服务，创建队列，并绑定到上游交换机

> [![](images/rabbitmq-federation-12.png)](http://qiniu.dev-share.top/image/rabbitmq-federation-12.png)

* * *

##### 查看交换机联邦效果

###### 下游服务同步效果

> [![](images/rabbitmq-federation-11.png)](http://qiniu.dev-share.top/image/rabbitmq-federation-11.png)

* * *

###### 上游服务同步效果

> [![](images/rabbitmq-federation-13.png)](http://qiniu.dev-share.top/image/rabbitmq-federation-13.png)
