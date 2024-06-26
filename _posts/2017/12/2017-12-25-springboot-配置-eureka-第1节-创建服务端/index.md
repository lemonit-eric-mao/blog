---
title: "SpringBoot 微服务构建 （一） 注册中心 Eureka Server"
date: "2017-12-25"
categories: 
  - "spring-boot"
---

##### spring-boot 注册中心

- 操作系统: ubuntu 16.04
- 开发工具: idea
- jdk: 1.8
- spring-boot: 1.5.17
- 项目: framework-register-center

##### 项目结构

```
framework-register-center
.
│ pom.xml
└─src
    └─main
        ├─java
        │  └─framework
        │      └─register
        │          └─center
        │                  FrameworkRegisterCenterApplication.java
        │
        └─resources
            │  application-dev.yml
            │  application.yml
            │
            └─config
                    logback-config.xml
```

##### 程序入口

FrameworkRegisterCenterApplication.java

```java
package framework.register.center;

import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.builder.SpringApplicationBuilder;
import org.springframework.cloud.netflix.eureka.server.EnableEurekaServer;

@SpringBootApplication
@EnableEurekaServer
public class FrameworkRegisterCenterApplication {

    public static void main(String[] args) {
        new SpringApplicationBuilder(FrameworkRegisterCenterApplication.class).web(true).run(args);
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
    <!-- 指定 framework.register.center 路径下的日志级别为 DEBUG -->
    <logger name="framework.register.center" level="DEBUG"></logger>
</configuration>
```

##### application.yml

```yml
#
spring:
  application:
    name: framework-register-center
  # 调用本地文件
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
server:
  port: 8761

eureka:
  instance:
    hostname: 127.0.0.1
  server:
    # 关闭自我保护模式（缺省为打开）
    enable-self-preservation: false
    # 续期时间，即扫描失效服务的间隔时间（缺省为60*1000ms）
    eviction-interval-timer-in-ms: 1000
  client:
    # 设置是否将自己作为客户端注册到注册中心（缺省true）
    # 这里为不需要（查看@EnableEurekaServer注解的源码，会发现它间接用到了@EnableDiscoveryClient）
    registerWithEureka: false
    # 设置是否从注册中心获取注册信息（缺省true）
    # 因为这是一个单点的EurekaServer，不需要同步其它EurekaServer节点的数据，故设为false
    fetchRegistry: false
    # 服务注册中心的地址
    serviceUrl:
      defaultZone: http://${eureka.instance.hostname}:${server.port}/eureka/
```

##### pom.xml

```markup
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>framework.register.center</groupId>
    <artifactId>framework-register-center</artifactId>
    <version>0.0.1-RELEASE</version>
    <!--<version>0.0.1-SNAPSHOT</version>-->
    <packaging>jar</packaging>

    <name>framework-eureka-server</name>
    <description>Demo project for Spring Boot</description>

    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>1.5.17.RELEASE</version>
        <relativePath/> <!-- lookup parent from repository -->
    </parent>

    <properties>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
        <project.reporting.outputEncoding>UTF-8</project.reporting.outputEncoding>
        <java.version>1.8</java.version>
        <spring-cloud.version>Dalston.SR5</spring-cloud.version>
    </properties>

    <dependencies>
        <!-- Spring Boot的核心启动器，包含了自动配置、日志和YAML。-->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter</artifactId>
        </dependency>

        <!-- 支持常规的测试依赖，包括JUnit、Hamcrest、Mockito以及spring-test模块。-->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>

        <!-- Eureka 服务器端 -->
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-eureka-server</artifactId>
        </dependency>
    </dependencies>

    <!-- 只是对版本进行管理，不会实际引入jar -->
    <dependencyManagement>
        <dependencies>
            <dependency>
                <groupId>org.springframework.cloud</groupId>
                <artifactId>spring-cloud-dependencies</artifactId>
                <version>${spring-cloud.version}</version>
                <type>pom</type>
                <scope>import</scope>
            </dependency>
        </dependencies>
    </dependencyManagement>

    <!--项目打包配置-必须-->
    <build>
        <finalName>${project.artifactId}</finalName>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
                <configuration>
                    <fork>true</fork>
                    <executable>true</executable>
                </configuration>
            </plugin>
        </plugins>
    </build>

</project>
```

##### 访问地址 http://localhost:8761/
