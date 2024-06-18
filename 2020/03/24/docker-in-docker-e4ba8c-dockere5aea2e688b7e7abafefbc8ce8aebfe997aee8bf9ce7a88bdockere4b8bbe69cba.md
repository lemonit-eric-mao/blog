---
title: 'Docker In Docker (二) Docker客户端，访问远程Docker主机'
date: '2020-03-24T03:30:46+00:00'
status: publish
permalink: /2020/03/24/docker-in-docker-%e4%ba%8c-docker%e5%ae%a2%e6%88%b7%e7%ab%af%ef%bc%8c%e8%ae%bf%e9%97%ae%e8%bf%9c%e7%a8%8bdocker%e4%b8%bb%e6%9c%ba
author: 毛巳煜
excerpt: ''
type: post
id: 5299
category:
    - Docker
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
##### 前置条件

CentOS 7  
Docker version 18.06.1-ce

test1 192.168.180.46  
test2 192.168.180.47

###### [官方文档](https://docs.docker.com/install/linux/linux-postinstall/#control-where-the-docker-daemon-listens-for-connections#configuring-remote-access-with-systemd-unit-file#configuring-remote-access-with-systemd-unit-file "官方文档")

- - - - - -

- - - - - -

- - - - - -

###### test2 开启docker远程访问模式

```ruby
# 编辑 docker.service 文件加入如下代码
[root@test2 ~]# systemctl edit docker.service

[Service]
ExecStart=
ExecStart=/usr/bin/dockerd -H tcp://0.0.0.0:2375 -H unix://var/run/docker.sock

# 重启docker
[root@test2 ~]# systemctl daemon-reload && systemctl restart docker.service

```

- - - - - -

###### test1 docker -H 远程访问测试

```ruby
[root@test1 ~]# docker -H 192.168.180.47:2375 info | grep Version
# 或者
[root@test1 ~]# docker -H 192.168.180.47 info | grep Version
Server Version: 18.06.1-ce
Kernel Version: 5.4.6-1.el7.elrepo.x86_64
[root@test1 ~]#

```

- - - - - -

###### test1 curl -X GET 远程访问测试

```ruby
[root@test1 ~]# curl -X GET http://192.168.180.47:2375/info | jq | grep Version
  "KernelVersion": "5.4.6-1.el7.elrepo.x86_64",
  "ServerVersion": "18.06.1-ce",
[root@test1 ~]#

```

- - - - - -

- - - - - -

- - - - - -