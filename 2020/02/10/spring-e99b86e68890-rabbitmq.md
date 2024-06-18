---
title: 'Spring 集成 RabbitMQ'
date: '2020-02-10T05:52:13+00:00'
status: publish
permalink: /2020/02/10/spring-%e9%9b%86%e6%88%90-rabbitmq
author: 毛巳煜
excerpt: ''
type: post
id: 5251
category:
    - spring-boot
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
##### spring-cloud 集成 RabbitMQ

- - - - - -

###### pom.xml

```
<pre data-language="XML">```markup
<?xml version="1.0" encoding="UTF-8"??>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemalocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelversion>4.0.0</modelversion>
    <parent>
        <groupid>org.springframework.boot</groupid>
        <artifactid>spring-boot-starter-parent</artifactid>
        <version>2.2.4.RELEASE</version>
        <relativepath></relativepath> 
    </parent>
    <groupid>top.devshare.mq</groupid>
    <artifactid>rabbit</artifactid>
    <version>0.0.1-SNAPSHOT</version>
    <name>rabbit</name>
    <description>Demo project for Spring Boot</description>

    <properties>
        <java.version>1.8</java.version>
        <spring-cloud.version>Hoxton.SR1</spring-cloud.version>
    </properties>

    <dependencies>
        <dependency>
            <groupid>org.springframework.cloud</groupid>
            <artifactid>spring-cloud-starter</artifactid>
        </dependency>

        <dependency>
            <groupid>org.springframework.boot</groupid>
            <artifactid>spring-boot-starter-test</artifactid>
            <scope>test</scope>
            <exclusions>
                <exclusion>
                    <groupid>org.junit.vintage</groupid>
                    <artifactid>junit-vintage-engine</artifactid>
                </exclusion>
            </exclusions>
        </dependency>

        <dependency>
            <groupid>org.springframework.boot</groupid>
            <artifactid>spring-boot-starter-web</artifactid>
            <scope>provided</scope>
        </dependency>

        
        <dependency>
            <groupid>org.springframework.boot</groupid>
            <artifactid>spring-boot-starter-amqp</artifactid>
            <version>2.2.4.RELEASE</version>
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
        <plugins>
            <plugin>
                <groupid>org.springframework.boot</groupid>
                <artifactid>spring-boot-maven-plugin</artifactid>
            </plugin>
        </plugins>
    </build>

</project>


```
```

- - - - - -

###### application.yml

```yml
spring:
  application:
    name: rabbitmq-test
  # 以下都是MQ配置
  rabbitmq:
    host: 172.160.180.46
    port: 5672
    username: admin
    password: 123456
    virtual-host: /vhost_eric
    listener:
      simple:
        retry:
          enabled: true # 是否开启消费者重试（为false时关闭消费者重试，这时消费端代码异常会一直重复收到消息）
          max-attempts: 1 # 最大重试次数； 该数值必须大于0
          initial-interval: 5000 # 重试间隔时间（单位毫秒）
          max-interval: 1200000 # 重试最大时间间隔（单位毫秒）

```

- - - - - -

###### 创建 消费者(监听者) ConsumerTopicListener.java

```java
package top.devshare.mq.rabbit;

import org.springframework.amqp.core.ExchangeTypes;
import org.springframework.amqp.rabbit.annotation.*;
import org.springframework.stereotype.Component;

/**
 * 消费者
 */
@Component
public class ConsumerTopicListener {

    /**
     * 小米消费者
     * @param msg
     */
    @RabbitListener(bindings = @QueueBinding(
            // 提供一个消息队列名为：queue_xiaomi
            value = @Queue("queue_xiaomi"),
            // 将消息队列绑定到名为：topic_name_eric 的 Topic 上
            exchange = @Exchange(value = "topic_name_eric", type = ExchangeTypes.TOPIC),
            // 凡是 routingkey 以 "test" 开头的消息，都被路由到 queue_xiaomi 这个消息队列上
            key = "test.#"))
    @RabbitHandler
    public void xiaomiConsumer(String msg) {

        System.out.printf("|  小米有新的消息，请注意查收:|    %s\n", msg);
        System.out.println("+----------------------------------------------+");
    }

    /**
     * 华为消费者
     * @param msg
     */
    @RabbitListener(bindings = @QueueBinding(
            // 提供一个消息队列名为：queue_huawei
            value = @Queue("queue_huawei"),
            // 将消息队列绑定到名为：topic_name_eric 的 Topic 上
            exchange = @Exchange(value = "topic_name_eric", type = ExchangeTypes.TOPIC),
            // routingkey 为 "test.huawei" 的消息，都被路由到 queue_huawei 这个消息队列上
            key = "test.huawei"))
    @RabbitHandler
    public void huaweiConsumer(String msg) {

        System.out.printf("|  华为有新的消息，请注意查收:|    %s\n", msg);
        System.out.println("+----------------------------------------------+");
    }

}

```

- - - - - -

###### 创建 生产者 ProducerController.java

```java
package top.devshare.mq.rabbit;

import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

/**
 * 生产者
 */
@RestController
public class ProducerController {

    @Autowired
    private RabbitTemplate rabbitTemplate;

    @GetMapping("/send")
    public void sendMessage() {

        // 向Topic名称为 topic_name_eric 中的队列发送消息， routingKey为test.huawei
        rabbitTemplate.convertAndSend("topic_name_eric", "test.huawei", "Hello RabbitMQ");
    }

}

```

- - - - - -

###### 启动程序 RabbitApplication.java

```java
package top.devshare.mq.rabbit;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.ComponentScan;

@SpringBootApplication
public class RabbitApplication {

    public static void main(String[] args) {
        SpringApplication.run(RabbitApplication.class, args);

        System.out.println("测试URL: http://localhost:8080/send");
        System.out.println("+----------------------------------------------+");
        System.out.println("|               持续等待接收消息                  |");
        System.out.println("+----------------------------------------------+");
    }

}

```

- - - - - -

- - - - - -

###### [下载项目](https://share.weiyun.com/5mB27Pq "下载项目")