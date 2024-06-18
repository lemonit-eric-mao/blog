---
title: 'Spring-boot2 注册中心 nacos'
date: '2020-02-12T06:37:06+00:00'
status: publish
permalink: /2020/02/12/spring-boot2-%e6%b3%a8%e5%86%8c%e4%b8%ad%e5%bf%83-nacos
author: 毛巳煜
excerpt: ''
type: post
id: 5253
category:
    - spring-boot
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
###### [官网地址](https://nacos.io/zh-cn/ "官网地址")

###### [下载地址](https://github.com/alibaba/nacos/releases "下载地址")

- - - - - -

###### [安装部署教程](https://nacos.io/zh-cn/docs/quick-start-docker.html "安装部署教程")

```ruby
[root@dev2 nacos]# git clone https://github.com/nacos-group/nacos-docker.git && cd nacos-docker/

[root@dev2 nacos-docker]# docker-compose -f example/standalone-derby.yaml up -d

```

- - - - - -

###### 登录web界面管理

http://172.16.30.208:8848/nacos  
用户名/密码: nacos/nacos

- - - - - -

###### 项目使用

```yml
spring:

  #
  profiles:
    active: prod

  #
  application:
    name: devshare

  #
  cloud:
    nacos:
      discovery:
        # nacos 服务器地址
        server-addr: 172.16.30.208:8848
        # nacos 可以为不同环境配置不同的命名空间用它来隔离注册的服务, 不同namespace下的微服务，不会有影响
        namespace: 70dec7cd-11c8-4539-a7ea-447b5c3d2a59

  # 以下是rabbitmq配置
  rabbitmq:
    host: 172.16.30.220
    port: 5672
    username: admin
    password: 123456
    virtual-host: /vhost_devshare
    listener:
      simple:
        retry:
          enabled: true # 是否开启消费者重试（为false时关闭消费者重试，这时消费端代码异常会一直重复收到消息）
          max-attempts: 1 # 最大重试次数
          initial-interval: 5000 # 重试间隔时间（单位毫秒）
          max-interval: 1200000 # 重试最大时间间隔（单位毫秒）

#
server:
  port: 8080
  max-http-header-size: 1024000
  compression:
    enabled: true
    min-response-size:
      1024
    mime-types:
      - application/json

#
swagger:
  # 项目根目录
  base-package: top.devshare
  title: dev-share
  version: 2.0
  enabled: true

#
logging:
  level:
    top.devshare: error

```

- - - - - -