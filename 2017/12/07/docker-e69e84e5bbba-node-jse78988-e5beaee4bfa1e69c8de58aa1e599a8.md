---
title: 'Docker 构建 Node.js版 微信服务器'
date: '2017-12-07T18:01:00+00:00'
status: publish
permalink: /2017/12/07/docker-%e6%9e%84%e5%bb%ba-node-js%e7%89%88-%e5%be%ae%e4%bf%a1%e6%9c%8d%e5%8a%a1%e5%99%a8
author: 毛巳煜
excerpt: ''
type: post
id: 1715
category:
    - Docker
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
##### 系统环境

```ruby
[root@localhost ~]# docker -v
Docker version 20.10.8, build 3967b7d

[root@localhost ~]# cat /etc/redhat-release
CentOS Linux release 7.9.2009 (Core)


```

- - - - - -

##### 项目目录树

```ruby
[root@localhost wx-server]# tree
.
├── app.js
├── bin
│   └── www
├── Dockerfile
├── exception-log
│   └── exception-log.js
├── package.json
└── routes
    ├── get_WX_JS_SDK_INFO.js
    ├── get_WX_JS_SDK.js
    ├── get_WX_JS_SDK_SIGN.js
    ├── get_WX_JS_SDK_USER_LIST_DETAIL.js
    └── get_WX_JS_SDK_USER_LIST.js

3 directories, 10 files
[root@localhost wx-server]#

```

- - - - - -

##### 配置Dockerfile文件

```ruby
# mao_siyu Docker
#
# VERSION 1.0.0

# 应用哪个仓库 承载自己的应用程序
# 在打包时相当于执行了 docker pull node:lts-alpine
FROM node:lts-alpine

# 设置该dockerfile的作者和联系邮箱
MAINTAINER mao_siyu@sina.com

# RUN mkdir -p 用于在Image里创建一个文件夹，将来用于保存我们的代码
RUN mkdir -p /app/wx/server

# WORKDIR 是将我们创建的文件夹做为工作目录
WORKDIR /app/wx/server

# COPY是把本机当前目录下的所有文件拷贝到Image的/wx/server文件夹下
COPY  .  /app/wx/server

# 设置npm私服地址
RUN npm config set registry http://172.16.15.205:8081/repository/npm-public/ \
    && npm install

# 从外部可以访问的接口
EXPOSE 8006

# 最后启动项目
CMD ["npm", "start"]

```

- - - - - -

##### 使用 Dockerfile 将自己的项目构建成 docker 镜像

`docker build -t wx-server:1.0 .`

```ruby
[root@localhost wx-server]# docker build -t wx-server:1.0 .
Sending build context to Docker daemon  3.584kB
Step 1/8 : FROM node:lts-alpine
 ---> 44e24535dfbf
Step 2/8 : MAINTAINER mao_siyu@sina.com
 ---> Using cache
 ---> 6a752a6b31ad
Step 3/8 : RUN mkdir -p /app/wx/server
 ---> Using cache
 ---> 38227079a76f
Step 4/8 : WORKDIR /app/wx/server
 ---> Using cache
 ---> 3f979a928bb6
Step 5/8 : COPY  .  /app/wx/server
 ---> 0b50059984b8
Step 6/8 : RUN npm config set registry http://172.16.15.205:8081/repository/npm-public/     && npm install
 ---> Running in 6ce16fd50282

up to date, audited 1 package in 333ms

found 0 vulnerabilities
Removing intermediate container 6ce16fd50282
 ---> ab359401df6e
Step 7/8 : EXPOSE 8006
 ---> Running in e31521382918
Removing intermediate container e31521382918
 ---> 977ceb9885d3
Step 8/8 : CMD ["npm", "start"]
 ---> Running in 7d6a09abeeee
Removing intermediate container 7d6a09abeeee
 ---> 273988913792
Successfully built 273988913792
Successfully tagged wx-server:1.0


```

- - - - - -

##### 查看结果

```ruby
[root@localhost wx-server]# docker images
REPOSITORY                      TAG           IMAGE ID       CREATED          SIZE
wx-server                       1.0           273988913792   50 seconds ago   110MB
node                            lts-alpine    44e24535dfbf   9 days ago       110MB


```

- - - - - -

##### 测试运行

```ruby
[root@localhost wx-server]# docker run -d -p 8006:8006 --name wxServer ddbe99e9a2b5
c2ee848d5807e9486d19d78a3d8e3b4181fc9ed853277dd24f2c12a19e28ccf2
[root@localhost wx-server]# docker ps -a
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS                    NAMES
c2ee848d5807        ddbe99e9a2b5        "npm start"         4 seconds ago       Up 3 seconds        0.0.0.0:8006->8006/tcp   wxServer
[root@localhost wx-server]# netstat -antp | grep 8006
tcp6       0      0 :::8006                 :::*                    LISTEN      32065/docker-proxy
[root@localhost wx-server]#

```

- - - - - -

- - - - - -

- - - - - -