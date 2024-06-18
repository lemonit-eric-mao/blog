---
title: 'Docker 学习笔记(二) 下载/安装/运行 CentOS 7'
date: '2017-11-16T14:34:50+00:00'
status: publish
permalink: /2017/11/16/docker-%e5%ad%a6%e4%b9%a0%e7%ac%94%e8%ae%b0%e4%ba%8c-%e4%b8%8b%e8%bd%bd%e5%ae%89%e8%a3%85%e8%bf%90%e8%a1%8c-centos-7
author: 毛巳煜
excerpt: ''
type: post
id: 388
category:
    - Docker
tag: []
post_format: []
---
### 查看Docker Hub官网centos7 镜像

https://hub.docker.com/r/library/centos/tags/

### 服务器地址: 10.32.156.51

### 从Docker 中国官方镜像加速官网, 下载centos7镜像文件

docker pull registry.docker-cn.com/library/centos:7

```
<pre class="line-numbers prism-highlight" data-start="1">```ruby
[root@localhost dockerImage]# docker pull registry.docker-cn.com/library/centos:7
7: Pulling from library/centos
d9aaf4d82f24: Pull complete
Digest: sha256:4565fe2dd7f4770e825d4bd9c761a81b26e49cc9e3c9631c58cfc3188be9505a
Status: Downloaded newer image for registry.docker-cn.com/library/centos:7
[root@localhost dockerImage]#
[root@localhost dockerImage]# docker images
REPOSITORY                              TAG                 IMAGE ID            CREATED             SIZE
registry.docker-cn.com/library/centos   7                   d123f4e55e12        3 days ago          197MB
[root@localhost dockerImage]#

```
```

运行镜像系统
------

#### **新版的Docker运行镜像文件以后会直接进入到镜像系统当中**

```
<pre class="line-numbers prism-highlight" data-start="1">```ruby
[root@localhost dockerImage]# docker run -ti d123f4e55e12
[root@8f564c36b28c /]#

```
```