---
title: 'SpringBoot 微服务构建 （三） 统一文件管理中心'
date: '2017-12-26T17:21:51+00:00'
status: publish
permalink: /2017/12/26/springboot-%e9%85%8d%e7%bd%ae-eureka-%e7%ac%ac3%e8%8a%82-%e7%bd%91%e5%85%b3-zuul
author: 毛巳煜
excerpt: ''
type: post
id: 1817
category:
    - spring-boot
tag: []
post_format: []
---
##### framework-file-center

- 操作系统: ubuntu 16.04
- 开发工具: idea
- jdk: 1.8
- spring-boot: 1.5.17
- 项目: framework-file-center

`file-center 项目作用是 将所有客户端子项目的配置文件统一管理，其好处是 当微服务做负载时，所有的服务器都会使用同一配置文件，方便维护; 它不是微服务器，它只是一个放在gitlab中存放配置文件的项目。`

##### 项目结构

```
framework-file-center
├─dev
│      framework-gateway-zuul.yml
│      user-center.yml
│
├─prod
│      framework-gateway-zuul.yml
│      user-center.yml
│
└─test
        framework-gateway-zuul.yml
        user-center.yml

```

##### dev/ framework-gateway-zuul.yml

```yml
# 网关端口
server:
  port: 8080
#
zuul:
  # 这意味着对 "/user" 的http调用将转发到 "user-center" 服务。
  # 路径必须有一个 "路径"，可以指定为蚂蚁风格的模式，
  # 因此 "/user/*" 只匹配一个级别，但 "/user/**" 按层次匹配。
  routes:
    # 访问用户中心
    users:
      path: /user/**
      serviceId: USER-CENTER
    # 访问框架级别
    framework:
      # 转发到认证中心
      path: /oauth/**
      serviceId: framework-oauth-center

# 注册到 Eureka Server
eureka:

  # Eureka 服务器端 配置
  instance:
    # 开启自定义，在服务器列表上显示的，客户端的名称
    preferIpAddress: true
    # 在服务器列表上显示的，客户端的名称
    instanceId: <span class="katex math inline">{spring.cloud.client.ipAddress}:</span>{server.port}
    # 在服务器列表上点击，客户端的名称后，跳转的地址
    hostname: <span class="katex math inline">{spring.cloud.client.ipAddress}
    # eureka 服务器地址
    eurekaServerHostname: 127.0.0.1
    # eureka 服务器地端口
    eurekaServerPort: 8761

  # Eureka 客户端 配置
  client:
    # 是否注册自身到eureka服务器
    registerWithEureka: true
    # 是否从eureka服务器获取注册信息
    fetchRegistry: true
    # 开启健康检查（依赖spring-boot-starter-actuator）
    healthcheck:
      enabled: true
    # 指定服务注册中心的地址
    serviceUrl:
      defaultZone: http://</span>{eureka.instance.eurekaServerHostname}:${eureka.instance.eurekaServerPort}/eureka/

```

##### dev/ user-center.yml

```yml
# 当前文件名需要与 服务器的 spring.application.name=user-center.yml 相同

# 用户中心
server:
  port: 8082

# 注册到 Eureka Server
eureka:

  # Eureka 服务器端 配置
  instance:
    # 开启自定义，在服务器列表上显示的，客户端的名称
    preferIpAddress: true
    # 在服务器列表上显示的，客户端的名称
    instanceId: <span class="katex math inline">{spring.cloud.client.ipAddress}:</span>{server.port}
    # 在服务器列表上点击，客户端的名称后，跳转的地址
    hostname: <span class="katex math inline">{spring.cloud.client.ipAddress}
    # eureka 服务器地址
    eurekaServerHostname: 127.0.0.1
    # eureka 服务器地端口
    eurekaServerPort: 8761

  # Eureka 客户端 配置
  client:
    # 是否注册自身到eureka服务器
    registerWithEureka: true
    # 是否从eureka服务器获取注册信息
    fetchRegistry: true
    # 开启健康检查（依赖spring-boot-starter-actuator）
    healthcheck:
      enabled: true
    # 指定服务注册中心的地址
    serviceUrl:
      defaultZone: http://</span>{eureka.instance.eurekaServerHostname}:${eureka.instance.eurekaServerPort}/eureka/

########################################################
#### mysql-datasource
########################################################
spring:
  datasource:
    hikari:
      master:
        jdbcUrl: jdbc:mysql://mysql.dev-share.top/db_common?characterEncoding=utf8&useSSL=false&serverTimezone=UTC&rewriteBatchedStatements=true
        username: root
        password: Maosiyu1987!
        driverClassName: com.mysql.jdbc.Driver
        maximumPoolSize: 15
        autoCommit: true
      slave:
        jdbcUrl: jdbc:mysql://mysql.dev-share.top/db_common?characterEncoding=utf8&useSSL=false&serverTimezone=UTC&rewriteBatchedStatements=true
        username: root
        password: Maosiyu1987!
        driverClassName: com.mysql.jdbc.Driver
        maximumPoolSize: 15
        autoCommit: true

```

- - - - - -

- - - - - -

##### prod/ framework-gateway-zuul.yml

```yml
# 网关端口
server:
  port: 80
#
zuul:
  # 这意味着对 "/user" 的http调用将转发到 "user-center" 服务。
  # 路径必须有一个 "路径"，可以指定为蚂蚁风格的模式，
  # 因此 "/user/*" 只匹配一个级别，但 "/user/**" 按层次匹配。
  routes:
    # 访问用户中心
    users:
      path: /user/**
      serviceId: USER-CENTER
    # 访问框架级别
    framework:
      # 转发到认证中心
      path: /oauth/**
      serviceId: framework-oauth-center

# 注册到 Eureka Server
eureka:

  # Eureka 服务器端 配置
  instance:
    # 开启自定义，在服务器列表上显示的，客户端的名称
    preferIpAddress: true
    # 在服务器列表上显示的，客户端的名称
    instanceId: <span class="katex math inline">{spring.cloud.client.ipAddress}:</span>{server.port}
    # 在服务器列表上点击，客户端的名称后，跳转的地址
    hostname: <span class="katex math inline">{spring.cloud.client.ipAddress}
    # eureka 服务器地址
    eurekaServerHostname: 172.20.60.14
    # eureka 服务器地端口
    eurekaServerPort: 8761

  # Eureka 客户端 配置
  client:
    # 是否注册自身到eureka服务器
    registerWithEureka: true
    # 是否从eureka服务器获取注册信息
    fetchRegistry: true
    # 开启健康检查（依赖spring-boot-starter-actuator）
    healthcheck:
      enabled: true
    # 指定服务注册中心的地址
    serviceUrl:
      defaultZone: http://</span>{eureka.instance.eurekaServerHostname}:${eureka.instance.eurekaServerPort}/eureka/

```

##### prod/ user-center.yml

```yml
# 当前文件名需要与 服务器的 spring.application.name=user-center.yml 相同

# 用户中心
server:
  port: 8082

# 注册到 Eureka Server
eureka:

  # Eureka 服务器端 配置
  instance:
    # 开启自定义，在服务器列表上显示的，客户端的名称
    preferIpAddress: true
    # 在服务器列表上显示的，客户端的名称
    instanceId: <span class="katex math inline">{spring.cloud.client.ipAddress}:</span>{server.port}
    # 在服务器列表上点击，客户端的名称后，跳转的地址
    hostname: <span class="katex math inline">{spring.cloud.client.ipAddress}
    # eureka 服务器地址
    eurekaServerHostname: 172.20.60.14
    # eureka 服务器地端口
    eurekaServerPort: 8761

  # Eureka 客户端 配置
  client:
    # 是否注册自身到eureka服务器
    registerWithEureka: true
    # 是否从eureka服务器获取注册信息
    fetchRegistry: true
    # 开启健康检查（依赖spring-boot-starter-actuator）
    healthcheck:
      enabled: true
    # 指定服务注册中心的地址
    serviceUrl:
      defaultZone: http://</span>{eureka.instance.eurekaServerHostname}:${eureka.instance.eurekaServerPort}/eureka/

########################################################
#### mysql-datasource
########################################################
spring:
  datasource:
    hikari:
      master:
        jdbcUrl: jdbc:mysql://172.20.60.20:3306/db_common?characterEncoding=utf8&useSSL=false&serverTimezone=UTC&rewriteBatchedStatements=true
        username: maosiyu
        password: Maosiyu1987!
        driverClassName: com.mysql.jdbc.Driver
        maximumPoolSize: 15
        autoCommit: true
      slave:
        jdbcUrl: jdbc:mysql://172.20.60.21:3306/db_common?characterEncoding=utf8&useSSL=false&serverTimezone=UTC&rewriteBatchedStatements=true
        username: maosiyu
        password: Maosiyu1987!
        driverClassName: com.mysql.jdbc.Driver
        maximumPoolSize: 15
        autoCommit: true

```

- - - - - -

- - - - - -

##### test/ framework-gateway-zuul.yml

```yml
# 网关端口
server:
  port: 8080
#
zuul:
  # 这意味着对 "/user" 的http调用将转发到 "user-center" 服务。
  # 路径必须有一个 "路径"，可以指定为蚂蚁风格的模式，
  # 因此 "/user/*" 只匹配一个级别，但 "/user/**" 按层次匹配。
  routes:
    # 访问用户中心
    users:
      path: /user/**
      serviceId: USER-CENTER
    # 访问框架级别
    framework:
      # 转发到认证中心
      path: /oauth/**
      serviceId: framework-oauth-center

# 注册到 Eureka Server
eureka:

  # Eureka 服务器端 配置
  instance:
    # 开启自定义，在服务器列表上显示的，客户端的名称
    preferIpAddress: true
    # 在服务器列表上显示的，客户端的名称
    instanceId: <span class="katex math inline">{spring.cloud.client.ipAddress}:</span>{server.port}
    # 在服务器列表上点击，客户端的名称后，跳转的地址
    hostname: <span class="katex math inline">{spring.cloud.client.ipAddress}
    # eureka 服务器地址
    eurekaServerHostname: 172.20.60.14
    # eureka 服务器地端口
    eurekaServerPort: 8761

  # Eureka 客户端 配置
  client:
    # 是否注册自身到eureka服务器
    registerWithEureka: true
    # 是否从eureka服务器获取注册信息
    fetchRegistry: true
    # 开启健康检查（依赖spring-boot-starter-actuator）
    healthcheck:
      enabled: true
    # 指定服务注册中心的地址
    serviceUrl:
      defaultZone: http://</span>{eureka.instance.eurekaServerHostname}:${eureka.instance.eurekaServerPort}/eureka/

```

##### test/ user-center.yml

```yml
# 当前文件名需要与 服务器的 spring.application.name=user-center.yml 相同

# 用户中心
server:
  port: 8082

# 注册到 Eureka Server
eureka:

  # Eureka 服务器端 配置
  instance:
    # 开启自定义，在服务器列表上显示的，客户端的名称
    preferIpAddress: true
    # 在服务器列表上显示的，客户端的名称
    instanceId: <span class="katex math inline">{spring.cloud.client.ipAddress}:</span>{server.port}
    # 在服务器列表上点击，客户端的名称后，跳转的地址
    hostname: <span class="katex math inline">{spring.cloud.client.ipAddress}
    # eureka 服务器地址
    eurekaServerHostname: 172.20.60.14
    # eureka 服务器地端口
    eurekaServerPort: 8761

  # Eureka 客户端 配置
  client:
    # 是否注册自身到eureka服务器
    registerWithEureka: true
    # 是否从eureka服务器获取注册信息
    fetchRegistry: true
    # 开启健康检查（依赖spring-boot-starter-actuator）
    healthcheck:
      enabled: true
    # 指定服务注册中心的地址
    serviceUrl:
      defaultZone: http://</span>{eureka.instance.eurekaServerHostname}:${eureka.instance.eurekaServerPort}/eureka/

########################################################
#### mysql-datasource
########################################################
spring:
  datasource:
    hikari:
      master:
        jdbcUrl: jdbc:mysql://172.20.60.20:3306/db_common?characterEncoding=utf8&useSSL=false&serverTimezone=UTC&rewriteBatchedStatements=true
        username: maosiyu
        password: Maosiyu1987!
        driverClassName: com.mysql.jdbc.Driver
        maximumPoolSize: 15
        autoCommit: true
      slave:
        jdbcUrl: jdbc:mysql://172.20.60.21:3306/db_common?characterEncoding=utf8&useSSL=false&serverTimezone=UTC&rewriteBatchedStatements=true
        username: maosiyu
        password: Maosiyu1987!
        driverClassName: com.mysql.jdbc.Driver
        maximumPoolSize: 15
        autoCommit: true

```