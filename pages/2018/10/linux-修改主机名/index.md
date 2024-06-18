---
title: "Linux 修改主机名"
date: "2018-10-10"
categories: 
  - "linux服务器"
---

##### 永久修改主机名

```ruby
[root@k8s-master ~]# hostnamectl set-hostname k8s-master
# 重新连接即可 不需要重启
```

##### 修改欢迎语

```ruby
[root@k8s-master ~]# vim /etc/motd
**************************
*                        *
*         欢迎回家        *
*                        *
**************************
```
