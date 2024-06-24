---
title: "SpringBoot 微服务构建 （四）客户端  配置文件中心"
date: "2018-03-30"
categories: 
  - "spring-boot"
---

##### framework-config-center

- 操作系统: ubuntu 16.04
- 开发工具: idea
- jdk: 1.8
- spring-boot: 1.5.17
- 项目: framework-config-center

###### framework-config-center 项目作用是 读取gitlab中 framework-file-center 项目中的配置文件

##### 项目结构

```
framework-config-center
.
│ pom.xml
└─src
    └─main
       ├─java
       │  └─framework
       │      └─config
       │          └─center
       │                  FrameworkConfigCenterApplication.java
       │
       └─resources
           │  application-dev.yml
           │  application-prod.yml
           │  application-test.yml
           │  application.yml
           │
           └─config
                   logback-config.xml
```

##### 程序入口 FrameworkConfigCenterApplication.java

```java
package framework.config.center;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.config.server.EnableConfigServer;
import org.springframework.cloud.netflix.eureka.EnableEurekaClient;

@SpringBootApplication
@EnableEurekaClient
@EnableConfigServer
public class FrameworkConfigCenterApplication {

    public static void main(String[] args) {
        SpringApplication.run(FrameworkConfigCenterApplication.class, args);
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
    <!-- 指定 framework.config.center 路径下的日志级别为 DEBUG -->
    <logger name="framework.config.center" level="DEBUG"></logger>
</configuration>
```

##### application.yml

```yml
spring:
  application:
    name: framework-config-center
  profiles:
    active: dev

########################################################
#### 引入 logback 配置文件
########################################################
logging:
  config: classpath:config/logback-config.xml
```

##### application-dev.yml

```yml
# 网关端口
server:
  port: 8762
#
spring:
  cloud:
    config:
      server:
        git:
          # 文件中心git仓库
          uri: http://git.dev-share.top/Java/framework-file-center.git
          username: zhangsu
          password: zhangsu123
          default-label: master
          force-pull: true
          # 对应的是 framework-file-center.git仓库中的文件夹
          search-paths: '{profile}'

# 注册到 Eureka Server
eureka:

  # Eureka 服务器端 配置
  instance:
    # 开启自定义，在服务器列表上显示的，客户端的名称
    preferIpAddress: true
    # 在服务器列表上显示的，客户端的名称
    instanceId: ${spring.cloud.client.ipAddress}:${server.port}
    # 在服务器列表上点击，客户端的名称后，跳转的地址
    hostname: ${spring.cloud.client.ipAddress}
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
      defaultZone: http://${eureka.instance.eurekaServerHostname}:${eureka.instance.eurekaServerPort}/eureka/
```

##### application-prod.yml

```yml
# 网关端口
server:
  port: 8762
#
spring:
  cloud:
    config:
      server:
        git:
          # 文件中心git仓库
          uri: http://172.20.60.17:8080/Framework/framework-file-center.git
          username: zhangsu
          password: zhangsu123
          default-label: master
          force-pull: true
          # 对应的是 framework-file-center.git仓库中的文件夹
          search-paths: '{profile}'

# 注册到 Eureka Server
eureka:

  # Eureka 服务器端 配置
  instance:
    # 开启自定义，在服务器列表上显示的，客户端的名称
    preferIpAddress: true
    # 在服务器列表上显示的，客户端的名称
    instanceId: ${spring.cloud.client.ipAddress}:${server.port}
    # 在服务器列表上点击，客户端的名称后，跳转的地址
    hostname: ${spring.cloud.client.ipAddress}
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
      defaultZone: http://${eureka.instance.eurekaServerHostname}:${eureka.instance.eurekaServerPort}/eureka/
```

##### application-test.yml

```yml
# 网关端口
server:
  port: 8762
#
spring:
  cloud:
    config:
      server:
        git:
          # 文件中心git仓库
          uri: http://172.20.60.17:8080/Framework/framework-file-center.git
          username: zhangsu
          password: zhangsu123
          default-label: master
          force-pull: true
          # 对应的是 framework-file-center.git仓库中的文件夹
          search-paths: '{profile}'

# 注册到 Eureka Server
eureka:

  # Eureka 服务器端 配置
  instance:
    # 开启自定义，在服务器列表上显示的，客户端的名称
    preferIpAddress: true
    # 在服务器列表上显示的，客户端的名称
    instanceId: ${spring.cloud.client.ipAddress}:${server.port}
    # 在服务器列表上点击，客户端的名称后，跳转的地址
    hostname: ${spring.cloud.client.ipAddress}
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
      defaultZone: http://${eureka.instance.eurekaServerHostname}:${eureka.instance.eurekaServerPort}/eureka/
```

##### pom.xml

```markup
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>framework.config.center</groupId>
    <artifactId>framework-config-center</artifactId>
    <version>0.0.1-RELEASE</version>
    <packaging>jar</packaging>

    <name>framework-config-center</name>
    <description>Demo project for Spring Boot</description>

    <parent>
        <groupId>framework.parent</groupId>
        <artifactId>framework-parent</artifactId>
        <version>0.0.1-RELEASE</version>
        <!--<version>0.0.1-SNAPSHOT</version>-->
        <relativePath/> <!-- lookup parent from repository -->
    </parent>

    <!-- config server -->
    <dependencies>
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-config-server</artifactId>
        </dependency>
    </dependencies>

</project>
```
