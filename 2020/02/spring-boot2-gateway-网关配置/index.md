---
title: "Spring-boot2 gateway 网关配置"
date: "2020-02-12"
categories: 
  - "spring-boot"
---

###### 1 项目结构

```
pom.xml
.
src
 └─main
    ├─java
    │  └─com
    │      └─cloud
    │          │  GatewayApplication.java
    │          │
    │          └─common
    │                  RouteConfiguration.java
    │
    └─resources
        │  bootstrap.yml
        │
        └─config
                logback-config.xml
```

* * *

###### 2 pom.xml

```markup
......
<!-- gateway 网关   -->
<!-- https://mvnrepository.com/artifact/org.springframework.cloud/spring-cloud-starter-gateway -->
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-gateway</artifactId>
    <version>2.2.1.RELEASE</version>
</dependency>

<!-- nacos 注册中心-发现，依赖包 mao_siyu add -->
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-alibaba-nacos-discovery</artifactId>
    <version>0.9.0.RELEASE</version>
</dependency>
......
```

* * *

###### 3 入口文件 GatewayApplication.java

```java
package com.cloud;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.client.discovery.EnableDiscoveryClient;


@EnableDiscoveryClient
@SpringBootApplication
public class GatewayApplication {

    public static void main(String[] args) {
        SpringApplication.run(GatewayApplication.class, args);
    }

}

```

* * *

###### 4 允许跨域 RouteConfiguration.java

```java
package com.cloud.common;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.HttpHeaders;
import org.springframework.http.server.reactive.ServerHttpRequest;
import org.springframework.http.server.reactive.ServerHttpResponse;
import org.springframework.web.cors.reactive.CorsUtils;
import org.springframework.web.server.ServerWebExchange;
import org.springframework.web.server.WebFilter;
import org.springframework.web.server.WebFilterChain;

/**
 * SpringApiGateway Cors
 */
@Configuration
public class RouteConfiguration {
    private static final String ALLOWED_HEADERS = "x-requested-with, authorization, Content-Type, Authorization, credential, X-XSRF-TOKEN,token,username,client";
    private static final String ALLOWED_METHODS = "POST, GET, PUT, DELETE, OPTIONS";
    private static final String ALLOWED_EXPOSE = "x-requested-with, authorization, Content-Type, Authorization, credential, X-XSRF-TOKEN,token,username,client";
    private static final String MAX_AGE = "18000L";

    /**
     * 允许跨域
     * @return
     */
    @Bean
    public WebFilter corsFilter() {
        return (ServerWebExchange ctx, WebFilterChain chain) -> {
            ServerHttpRequest request = ctx.getRequest();
            if (CorsUtils.isCorsRequest(request)) {
                ServerHttpResponse response = ctx.getResponse();
                HttpHeaders headers = response.getHeaders();
                headers.add("Access-Control-Allow-Origin", request.getHeaders().getOrigin());
                headers.add("Access-Control-Allow-Methods", ALLOWED_METHODS);
                headers.add("Access-Control-Max-Age", MAX_AGE);
                headers.add("Access-Control-Allow-Headers", ALLOWED_HEADERS);
                headers.add("Access-Control-Expose-Headers", ALLOWED_EXPOSE);
                headers.add("Access-Control-Allow-Credentials", "true");
            }
            return chain.filter(ctx);
        };
    }

}
```

* * *

###### 5 logback-config.xml

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
    <!-- 指定 com.cloud 路径下的日志级别为 DEBUG -->
    <logger name="com.cloud" level="DEBUG"></logger>
</configuration>

```

* * *

###### 6 bootstrap.yml

```yml
server:
  port: 8001

spring:
  application:
    name: cloud-gateway
  cloud:

    nacos:
      discovery:
        # nacos注册中心地址
        server-addr: 127.0.0.1:8848
    #         namespace: a30c71d4-945d-44f9-8b7e-f73fb1a0d7c1

  # 设置上传文件大小限制
  servlet:
    multipart:
      # 最大文件大小。值可以使用后缀“MB”或“KB”分别表示兆字节或千字节。
      max-file-size: 100MB
      # 最大请求大小。值可以使用后缀“MB”或“KB”分别表示兆字节或千字节。
      max-request-size: 100MB

    gateway:
      # 路由转换
      routes:
        # 这个路由的唯一id，不定义的话为一个uuid
        - id: gw-demo
          # 转发的服务器地址;
          # http请求为 lb://前缀 + 服务id
          # ws请求为 lb:ws://前缀 + 服务id
          uri: lb://demo
          predicates:
            # 拦截的URL路径
            - Path=/demo_v1/**
          filters:
            # 删除前缀
            - StripPrefix=1

        - id: gw-test
          uri: lb://test
          predicates:
            - Path=/test_v1/**
          filters:
            - StripPrefix=1

      discovery:
        locator:
          enabled: true
          lower-case-service-id: true
      # 支持跨域
      globalcors:
        corsConfigurations:
          '[/**]':
            allowedOrigins: "*"
            allowedMethods: "*"
            allowedHeaders: "*"
            exposedHeaders: cte

# 添加饥饿加载
ribbon:
  eager-load:
    enabled: true
    # 指定需要饥饿加载的客户端名称、服务名(spring.application.name: 名称是啥就写啥)
    clients: demo, test

feign:
  hystrix:
    enabled: true

# 配置日志级别
logging:
  level:
    # 指定哪些路径下的 java文件，可以输入日志
    com.yihui: debug
```

* * *

###### 7 测试路径

http://localhost:8001/demo\_v1/swagger-ui.html
