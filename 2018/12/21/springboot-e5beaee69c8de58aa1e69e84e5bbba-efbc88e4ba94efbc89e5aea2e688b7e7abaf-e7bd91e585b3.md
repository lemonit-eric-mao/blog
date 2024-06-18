---
title: 'SpringBoot 微服务构建 （五）客户端  网关'
date: '2018-12-21T02:54:35+00:00'
status: publish
permalink: /2018/12/21/springboot-%e5%be%ae%e6%9c%8d%e5%8a%a1%e6%9e%84%e5%bb%ba-%ef%bc%88%e4%ba%94%ef%bc%89%e5%ae%a2%e6%88%b7%e7%ab%af-%e7%bd%91%e5%85%b3
author: 毛巳煜
excerpt: ''
type: post
id: 3376
category:
    - spring-boot
tag: []
post_format: []
---
##### framework-gateway-zuul

- 操作系统: ubuntu 16.04
- 开发工具: idea
- jdk: 1.8
- spring-boot: 1.5.17
- 项目: framework-gateway-zuul

###### framework-gateway-zuul 项目作用是 微服务客户端统一入口

##### 项目结构

```
framework-gateway-zuul
.
│ pom.xml
└─src
    └─main
       ├─java
       │  └─framework
       │      └─gateway
       │          └─zuul
       │              │  FrameworkGatewayZuulApplication.java
       │              │
       │              └─common
       │                  └─config
       │                          ApplicationConfiguration.java
       │                          CorsConfig.java
       │
       └─resources
           │  bootstrap.yml
           │
           └─config
                   logback-config.xml

```

##### 程序入口 FrameworkGatewayZuulApplication.java

```java
package framework.gateway.zuul;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.netflix.zuul.EnableZuulProxy;

@SpringBootApplication
@EnableZuulProxy
public class FrameworkGatewayZuulApplication {

    public static void main(String[] args) {
        SpringApplication.run(FrameworkGatewayZuulApplication.class, args);
    }
}

```

##### logback-config.xml

```
<pre data-language="XML">```markup
<?xml version="1.0"??>
<configuration>
    
    <appender class="ch.qos.logback.core.ConsoleAppender" name="console">
        <encoder>
            <pattern>%d{yyyy-MM-dd HH:mm:ss.SSS} %highlight(%5p [%15.15t]) %cyan(%-50.40c{1.}) : %highlight(%m%n)
            </pattern>
        </encoder>
    </appender>
    
    <root>
        
        <level value="ERROR"></level>
        <appender-ref ref="console"></appender-ref>
    </root>
    
    <logger level="DEBUG" name="framework.gateway.zuul"></logger>
</configuration>

```
```

##### bootstrap.yml

```yml
# 必须使用 bootstrap.yml 要不然加载配置文件会失败
spring:
  application:
    name: framework-gateway-zuul
#  # 调用本地文件
#  profiles:
#    active: dev
  # 调用配置中心的文件配置
  cloud:
    config:
      # 对应的是 framework-config-center 配置服务中的 {profile}
#      profile: dev
      profile: test
#      profile: prod
      # 对应的分支
      label: master
      # 测试服-配置中心URL地址; 当服务器分布式部署时，必须是使用地址的
      uri: http://172.20.60.14:8762
      # 本地-配置中心URL地址;
#      uri: http://127.0.0.1:8762
      # 当regist-center 与 gateway-zuul 在同一个系统时可用
#      discovery:
#        enabled: true
#        serviceId: framework-config-center

########################################################
#### 引入 logback 配置文件
########################################################
logging:
  config: classpath:config/logback-config.xml

```

##### pom.xml

```
<pre data-language="XML">```markup
<?xml version="1.0" encoding="UTF-8"??>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemalocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelversion>4.0.0</modelversion>

    <groupid>framework.gateway.zuul</groupid>
    <artifactid>framework-gateway-zuul</artifactid>
    <version>0.0.1-RELEASE</version>
    
    <packaging>jar</packaging>

    <name>framework-gateway-zuul</name>
    <description>Demo project for Spring Boot</description>

    <parent>
        <groupid>framework.parent</groupid>
        <artifactid>framework-parent</artifactid>
        <version>0.0.1-RELEASE</version>
        <relativepath></relativepath> 
    </parent>

    <dependencies>
        <dependency>
            <groupid>org.springframework.cloud</groupid>
            <artifactid>spring-cloud-starter-zuul</artifactid>
        </dependency>

        
        <dependency>
            <groupid>org.springframework.cloud</groupid>
            <artifactid>spring-cloud-starter-config</artifactid>
        </dependency>
    </dependencies>

</project>

```
```