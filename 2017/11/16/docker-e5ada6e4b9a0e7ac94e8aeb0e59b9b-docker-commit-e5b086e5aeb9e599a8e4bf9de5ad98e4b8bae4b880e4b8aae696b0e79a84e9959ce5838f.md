---
title: 'Docker 学习笔记(四) Docker commit 将容器保存为一个新的镜像'
date: '2017-11-16T14:43:48+00:00'
status: publish
permalink: /2017/11/16/docker-%e5%ad%a6%e4%b9%a0%e7%ac%94%e8%ae%b0%e5%9b%9b-docker-commit-%e5%b0%86%e5%ae%b9%e5%99%a8%e4%bf%9d%e5%ad%98%e4%b8%ba%e4%b8%80%e4%b8%aa%e6%96%b0%e7%9a%84%e9%95%9c%e5%83%8f
author: 毛巳煜
excerpt: ''
type: post
id: 405
category:
    - Docker
tag: []
post_format: []
---
### **docker commit -m `'注释'` `容器CONTAINER ID` `镜像名称`:`镜像版本`**

### 退出容器

```
<pre class="line-numbers prism-highlight" data-start="1">```ruby
[root@23c18d958279 ~]# exit
exit
[root@localhost dockerImage]#
[root@localhost dockerImage]# docker ps -a
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS                       PORTS                    NAMES
23c18d958279        4a5932cd5a14        "/bin/bash"              17 minutes ago      Exited (130) 9 minutes ago                            determined_sammet
[root@localhost dockerImage]#

```
```

### 将容器保存为一个新的镜像

```
<pre class="line-numbers prism-highlight" data-start="1">```ruby
[root@localhost dockerImage]# docker commit 23c18d958279 bigdata:v0.2
[root@localhost dockerImage]#
[root@localhost dockerImage]# docker images
REPOSITORY                              TAG                 IMAGE ID            CREATED             SIZE
bigdata                                 v0.2                715bc4108155        8 minutes ago       1.64GB
bigdata                                 v0.1                4a5932cd5a14        4 hours ago         1.64GB
registry.docker-cn.com/library/centos   7                   d123f4e55e12        4 days ago          197MB
[root@localhost dockerImage]#

```
```

### 运行测试

```
<pre class="line-numbers prism-highlight" data-start="1">```ruby
[root@localhost dockerImage]# docker run -d -p 3000:3000 715bc4108155 /home/bigdata/start.sh
[root@localhost dockerImage]#
[root@localhost dockerImage]# docker ps -a
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS                       PORTS                    NAMES
60ebba65b023        715bc4108155        "/home/bigdata/sta..."   7 minutes ago       Up 7 minutes                 0.0.0.0:3000->3000/tcp   naughty_shannon
23c18d958279        4a5932cd5a14        "/bin/bash"              17 minutes ago      Exited (130) 9 minutes ago                            determined_sammet
[root@localhost dockerImage]#

```
```

#### **例如: 本机的IP地址是 10.32.156.51**

#### **测试地址为: http://10.32.156.51:3000**