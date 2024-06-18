---
title: 'SpringBoot 微服务构建 （一） 注册中心 Eureka Server'
date: '2017-12-25T14:20:28+00:00'
status: publish
permalink: /2017/12/25/springboot-%e9%85%8d%e7%bd%ae-eureka-%e7%ac%ac1%e8%8a%82-%e5%88%9b%e5%bb%ba%e6%9c%8d%e5%8a%a1%e7%ab%af
author: 毛巳煜
excerpt: ''
type: post
id: 1800
category:
    - spring-boot
tag: []
post_format: []
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
    
    <logger level="DEBUG" name="framework.register.center"></logger>
</configuration>

```
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
      defaultZone: http://<span class="katex math inline">{eureka.instance.hostname}:</span>{server.port}/eureka/

```

##### pom.xml

```
<pre data-language="XML">```markup
<?xml version="1.0" encoding="UTF-8"??>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemalocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelversion>4.0.0</modelversion>

    <groupid>framework.register.center</groupid>
    <artifactid>framework-register-center</artifactid>
    <version>0.0.1-RELEASE</version>
    
    <packaging>jar</packaging>

    <name>framework-eureka-server</name>
    <description>Demo project for Spring Boot</description>

    <parent>
        <groupid>org.springframework.boot</groupid>
        <artifactid>spring-boot-starter-parent</artifactid>
        <version>1.5.17.RELEASE</version>
        <relativepath></relativepath> 
    </parent>

    <properties>
        <project.build.sourceencoding>UTF-8</project.build.sourceencoding>
        <project.reporting.outputencoding>UTF-8</project.reporting.outputencoding>
        <java.version>1.8</java.version>
        <spring-cloud.version>Dalston.SR5</spring-cloud.version>
    </properties>

    <dependencies>
        
        <dependency>
            <groupid>org.springframework.boot</groupid>
            <artifactid>spring-boot-starter</artifactid>
        </dependency>

        
        <dependency>
            <groupid>org.springframework.boot</groupid>
            <artifactid>spring-boot-starter-test</artifactid>
            <scope>test</scope>
        </dependency>

        
        <dependency>
            <groupid>org.springframework.cloud</groupid>
            <artifactid>spring-cloud-starter-eureka-server</artifactid>
        </dependency>
    </dependencies>

    
    <dependencymanagement>
        <dependencies>
            <dependency>
                <groupid>org.springframework.cloud</groupid>
                <artifactid>spring-cloud-dependencies</artifactid>
                <version>${spring-cloud.version}</version>
                <type>pom</type>
                <scope>import</scope>
            </dependency>
        </dependencies>
    </dependencymanagement>

    
    <build>
        <finalname>${project.artifactId}</finalname>
        <plugins>
            <plugin>
                <groupid>org.springframework.boot</groupid>
                <artifactid>spring-boot-maven-plugin</artifactid>
                <configuration>
                    <fork>true</fork>
                    <executable>true</executable>
                </configuration>
            </plugin>
        </plugins>
    </build>

</project>

```
```

##### 访问地址 http://localhost:8761/