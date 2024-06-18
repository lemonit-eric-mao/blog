---
title: "docker构建Node.js镜像"
date: "2022-07-19"
categories: 
  - "node-js"
---

###### Dockerfile 写法

```shell
FROM node:18.6.0-alpine

# 设置该dockerfile的作者和联系邮箱
MAINTAINER 85785053@qq.com

# RUN mkdir -p 用于在Image里创建一个文件夹，将来用于保存我们的代码
RUN mkdir -p /app

# WORKDIR 是将我们创建的文件夹做为工作目录
WORKDIR /app

# COPY是把本机当前目录下的所有文件拷贝到Image的工作目录下
COPY . /app

# 配置服务器端口
EXPOSE 3000

# 初始化项目
RUN npm install -g cnpm --registry=https://registry.npmmirror.com \
    && cnpm i

# 最后 配置启动项目的命令
CMD ["npm", "start"]

```

* * *

###### 构建Docker镜像

```ruby
## 下载项目
git clone https://gitee.com/eric-mao/koa2-server.git

## 进入目录
cd koa2-server/

## 构建镜像
docker build -t koa2-server:0.1.0 .

## docker测试
docker run --rm -it -p 8080:3000 koa2-server:0.1.0
```

* * *

###### 创建docker-compose.yaml

```yaml
version: '3.1'
services:
  koa2-server:
    image: koa2-server:0.1.0
    container_name: koa2-server
    restart: always
    ports:
      - 8080:3000
    hostname: eric_koa2_server

    volumes:
      # 容器与宿主机时间同步
      - /etc/localtime:/etc/localtime
    environment:
      DB_HOST: '192.168.2.10'
      DB_PORT: '3306'
      DATABASE: 'oidc_auth'
      DB_USER: 'root'
      DB_PASSWORD: 'yourpasswd'

```

* * *

```ruby
## 访问服务端渲染页面
http://192.168.2.10:8080/test/info/1

```

* * *

* * *

* * *

* * *

* * *

* * *

## 另一种构建方式

> 基于操作系统构建自己的`Node.js`环境，通常用于给`Nocalhost`制作开发环境

```shell
cat > Dockerfile << ERIC
FROM centos:centos7.9.2009

RUN curl -sL https://rpm.nodesource.com/setup_16.x | bash - && \\
        yum install -y nodejs zsh

ERIC




## 构建
docker build -t centos-node:centos7.9.2009-16.19.0 .


## 测试
docker run --rm -it centos-node:centos7.9.2009-16.19.0
[root@53e772479770 /]# node -v
v16.19.0
[root@53e772479770 /]# npm -v
8.19.3

```

* * *

* * *

* * *
