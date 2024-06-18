---
title: '构建 Docker 极小镜像'
date: '2020-03-25T08:09:52+00:00'
status: publish
permalink: /2020/03/25/%e6%9e%84%e5%bb%ba-docker-%e6%9e%81%e5%b0%8f%e9%95%9c%e5%83%8f
author: 毛巳煜
excerpt: ''
type: post
id: 5301
category:
    - Docker
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
wb_sst_seo:
    - 'a:3:{i:0;s:0:"";i:1;s:0:"";i:2;s:0:"";}'
---
##### 创建脚本

```ruby
cat > start.sh 
```

- - - - - -

##### Dockerfile 构建镜像

```ruby
cat > Dockerfile 
```

- - - - - -

##### 构建

```ruby
## 构建
docker build -t tools:1.0.0 .

## 查看
docker images tools
REPOSITORY   TAG       IMAGE ID       CREATED          SIZE
tools        1.0.0     2f3c597df221   56 seconds ago   5.54MB


```

- - - - - -

##### 运行以后会自动删除容器(--rm)

```ruby
## 容器内脚本
docker run --rm -it -e TEMP=world! tools:1.0.0 /bin/sh
/app # ./start.sh
hello_world!


## 在容器外直接执行脚本
docker run --rm -it -e TEMP=world! tools:1.0.0 /bin/sh ./start.sh
hello_world!


```