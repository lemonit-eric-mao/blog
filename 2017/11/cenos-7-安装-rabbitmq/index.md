---
title: "Cenos 7 安装 RabbitMQ"
date: "2017-11-16"
categories: 
  - "centos"
---

**erlang下载地址: https://packagecloud.io/rabbitmq/erlang/packages/el/7/erlang-20.1.1-1.el7.centos.x86\_64.rpm**

### **先安装 erlang**

```ruby
[root@zhujiwu download]# wget --content-disposition https://packagecloud.io/rabbitmq/erlang/packages/el/7/erlang-20.1.1-1.el7.centos.x86_64.rpm/download.rpm
[root@zhujiwu download]#
[root@zhujiwu download]# rpm -ivh erlang-20.1.1-1.el7.centos.x86_64.rpm
[root@zhujiwu download]#
[root@zhujiwu download]# yum install erlang
[root@zhujiwu download]#
```

**rabbitmq下载地址: https://packagecloud.io/rabbitmq/rabbitmq-server/packages/el/7/rabbitmq-server-3.6.12-1.el7.noarch.rpm**

### **安装 RabbitMQ**

```ruby
[root@zhujiwu download]# wget --content-disposition https://packagecloud.io/rabbitmq/rabbitmq-server/packages/el/7/rabbitmq-server-3.6.12-1.el7.noarch.rpm/download.rpm
[root@zhujiwu download]#
[root@zhujiwu download]# rpm -ivh rabbitmq-server-3.6.12-1.el7.noarch.rpm
[root@zhujiwu download]#
[root@zhujiwu download]# yum install rabbitmq-server
[root@zhujiwu download]#
```

### **启动**

```ruby
[root@zhujiwu download]# systemctl start rabbitmq-server
Job for rabbitmq-server.service failed. See 'systemctl status rabbitmq-server.service' and 'journalctl -xn' for details.
[root@zhujiwu download]#
```

### **启动失败 Failed to start RabbitMQ broker.**

```ruby
[root@zhujiwu download]# systemctl status rabbitmq-server
rabbitmq-server.service - RabbitMQ broker
   Loaded: loaded (/usr/lib/systemd/system/rabbitmq-server.service; disabled)
   Active: failed (Result: exit-code) since 三 2017-10-11 23:23:10 CST; 3s ago
  Process: 11914 ExecStop=/bin/sh -c while ps -p $MAINPID >/dev/null 2>&1; do sleep 1; done (code=exited, status=0/SUCCESS)
  Process: 11778 ExecStop=/usr/sbin/rabbitmqctl stop (code=exited, status=0/SUCCESS)
  Process: 11606 ExecStart=/usr/sbin/rabbitmq-server (code=exited, status=1/FAILURE)
 Main PID: 11606 (code=exited, status=1/FAILURE)

10月 11 23:23:10 vdevops rabbitmqctl[11778]: * connected to epmd (port 4369) on vdevops
10月 11 23:23:10 vdevops rabbitmqctl[11778]: * epmd reports: node 'rabbit' not running at all
10月 11 23:23:10 vdevops rabbitmqctl[11778]: no other nodes on vdevops
10月 11 23:23:10 vdevops rabbitmqctl[11778]: * suggestion: start the node
10月 11 23:23:10 vdevops rabbitmqctl[11778]: current node details:
10月 11 23:23:10 vdevops rabbitmqctl[11778]: - node name: 'rabbitmq-cli-61@vdevops'
10月 11 23:23:10 vdevops rabbitmqctl[11778]: - home dir: .
10月 11 23:23:10 vdevops rabbitmqctl[11778]: - cookie hash: kMXEA9T9/LYIxrGXsavTgw==
10月 11 23:23:10 vdevops systemd[1]: Failed to start RabbitMQ broker.
10月 11 23:23:10 vdevops systemd[1]: Unit rabbitmq-server.service entered failed state.
[root@zhujiwu download]#
```

### **解决方案 直接输入 rabbitmq-server 进行服务器启动**

```ruby
[root@zhujiwu ~]# rabbitmq-server

              RabbitMQ 3.6.12. Copyright (C) 2007-2017 Pivotal Software, Inc.
  ##  ##      Licensed under the MPL.  See http://www.rabbitmq.com/
  ##  ##
  ##########  Logs: /var/log/rabbitmq/root@zhujiwu.log
  ######  ##        /var/log/rabbitmq/root@zhujiwu-sasl.log
  ##########
              Starting broker...
 completed with 6 plugins.

```

### **测试服务器是否启动成功**

```ruby
[root@zhujiwu ~]# curl 127.0.0.1:15672
```
