---
title: 'Linux namespace和cgroup'
date: '2019-12-16T06:23:26+00:00'
status: publish
permalink: /2019/12/16/linux-namespace%e5%92%8ccgroup
author: 毛巳煜
excerpt: ''
type: post
id: 5195
category:
    - Linux服务器
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
##### `Cgroup`

 Cgroup是control group，又称为控制组，它主要是做资源控制。原理是将一组进程放在放在一个控制组里，通过给这个控制组分配指定的可用资源，达到控制这一组进程可用资源的目的。  
**cgroup 主要是用作资源的限制，常见的有cpu、内存、blkio等**

- - - - - -

##### `Namespace`

 Namespace又称为命名空间，它主要做访问隔离。其原理是针对一类资源进行抽象，并将其封装在一起提供给一个容器使用，对于这类资源，因为每个容器都有自己的抽象，而他们彼此之间是不可见的，所以就可以做到访问隔离。  
**namespace 主要用作环境的隔离，主要有以下namespace：**

- UTS: 主机名与域名
- IPC: 信号量、消息队列和共享内存
- PID: 进程编号
- Network:网络设备、网络栈、端口等等
- Mount: 挂载点
- User: 用户和用户组