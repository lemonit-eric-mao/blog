---
title: "SpringBoot 微服务构建 （五）客户端  网关"
date: "2018-12-21"
categories: 
  - "spring-boot"
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

```markup
<?xml version="1.0"?>
<configuration>
    <!-- ch.qos.logback.core.ConsoleAppender 控制台输出 -->
    <appender name="console" class="ch.qos.logback.core.ConsoleAppender">
        <encoder>
            <pattern>%d{yyyy-MM-dd HH:mm:ss.SSS} %highlight(%5p [%15.15t]) %cyan(%-50.40c{1.}) : %highlight(%m%n)
            </pattern>
        </encoder>
    </appender>
    <!-- 日志级别 -->
    <root>
        <!-- 默认日志级别 -->
        <level value="ERROR"/>
        <appender-ref ref="console"/>
    </root>
    <!-- 指定 framework.gateway.zuul 路径下的日志级别为 DEBUG -->
    <logger name="framework.gateway.zuul" level="DEBUG"></logger>
</configuration>
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

```markup
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>framework.gateway.zuul</groupId>
    <artifactId>framework-gateway-zuul</artifactId>
    <version>0.0.1-RELEASE</version>
    <!--<version>0.0.1-SNAPSHOT</version>-->
    <packaging>jar</packaging>

    <name>framework-gateway-zuul</name>
    <description>Demo project for Spring Boot</description>

    <parent>
        <groupId>framework.parent</groupId>
        <artifactId>framework-parent</artifactId>
        <version>0.0.1-RELEASE</version>
        <relativePath/> <!-- lookup parent from repository -->
    </parent>

    <dependencies>
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-zuul</artifactId>
        </dependency>

        <!-- 文件配置中心客户端，必须 -->
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-config</artifactId>
        </dependency>
    </dependencies>

</project>
```
