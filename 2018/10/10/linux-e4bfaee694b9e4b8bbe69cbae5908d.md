---
title: 'Linux 修改主机名'
date: '2018-10-10T06:45:13+00:00'
status: publish
permalink: /2018/10/10/linux-%e4%bf%ae%e6%94%b9%e4%b8%bb%e6%9c%ba%e5%90%8d
author: 毛巳煜
excerpt: ''
type: post
id: 3197
category:
    - Linux服务器
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
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