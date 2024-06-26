---
title: "Docker 学习笔记(六) 下载/安装/运行 Node.js"
date: "2017-11-16"
categories: 
  - "docker"
---

##### 查看Docker Hub官网node.js 镜像 https://hub.docker.com/r/library/node/tags/

##### 服务器地址: 10.32.156.51

##### 从Docker 中国官方镜像加速官网, 下载node.js镜像文件

##### **docker pull registry.docker-cn.com/library/node:8.9.1**

```ruby
[root@localhost ~]# docker pull registry.docker-cn.com/library/node:8.9.1
8.9.1: Pulling from library/node
85b1f47fba49: Already exists
ba6bd283713a: Pull complete
817c8cd48a09: Pull complete
47cc0ed96dc3: Pull complete
8888adcbd08b: Pull complete
6f2de60646b9: Pull complete
51fa8867e10f: Pull complete
3de546fb9d8f: Pull complete
Digest: sha256:552348163f074034ae75643c01e0ba301af936a898d778bb4fc16062917d0430
Status: Downloaded newer image for registry.docker-cn.com/library/node:8.9.1
[root@localhost ~]#
[root@localhost ~]# docker images
REPOSITORY                             TAG                 IMAGE ID            CREATED             SIZE
registry.docker-cn.com/library/node    8.9.1               1934b0b038d1        6 days ago          676MB
[root@localhost ~]#
```

##### 运行镜像系统

##### **新版的Docker运行镜像文件以后会直接进入到镜像系统当中**

```ruby
[root@localhost ~]# docker run -ti 1934b0b038d1
```
