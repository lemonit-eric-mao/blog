---
title: 'Docker 学习笔记(三) 构建简单系统，并安装常用工具'
date: '2017-11-16T14:42:21+00:00'
status: publish
permalink: /2017/11/16/docker-%e5%ad%a6%e4%b9%a0%e7%ac%94%e8%ae%b0%e5%9b%9b-%e5%ae%89%e8%a3%85-vim-node-js-java-git
author: 毛巳煜
excerpt: ''
type: post
id: 400
category:
    - Docker
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
###### 配置 Dockerfile

```ruby
[root@test1 build]# cat > Dockerfile 
```

###### 构建

```ruby
[root@test1 build]# docker build -t tools-os:v1.0.0 .
[root@test1 build]#
[root@test1 build]# docker images
REPOSITORY                           TAG                 IMAGE ID            CREATED             SIZE
tools-os                             v1.0.0              7b3d382fc9ae        16 seconds ago      354 MB
[root@test1 build]#
# 测试
[root@test1 build]# docker run -dti --name tools-os -p 80:80 tools-os:v1.0.0

```