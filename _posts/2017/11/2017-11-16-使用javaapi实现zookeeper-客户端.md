---
title: "使用JavaAPI实现Zookeeper 客户端"
date: "2017-11-16"
categories: 
  - "大数据"
---

- 开发工具: IDEA
- 系统: Ubuntu 16.04
- JDK: jdk 1.8
- 项目工程类型: maven
- 项目名称: Zookeeper
- 服务端地址: 10.32.156.68:2181 基于上一篇文章 [CentOS 7 安装运行 Zookeeper 服务端](centos-7-%e5%ae%89%e8%a3%85%e8%bf%90%e8%a1%8c-zookeeper-%e6%9c%8d%e5%8a%a1%e7%ab%af "CentOS 7 安装运行 Zookeeper 服务端")

###### pom.xml

```markup
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>Zookeeper</groupId>
    <artifactId>Zookeeper</artifactId>
    <version>1.0-SNAPSHOT</version>

    <dependencies>
        <!-- https://mvnrepository.com/artifact/org.apache.hadoop/zookeeper -->
        <dependency>
            <groupId>org.apache.hadoop</groupId>
            <artifactId>zookeeper</artifactId>
            <version>3.3.1</version>
        </dependency>
        <!-- https://mvnrepository.com/artifact/log4j/log4j -->
        <dependency>
            <groupId>log4j</groupId>
            <artifactId>log4j</artifactId>
            <version>1.2.17</version>
        </dependency>

    </dependencies>
</project>

```

###### log4j 配置文件 log4j.properties

```yaml
log4j.rootLogger=INFO, Console
#Console
log4j.appender.Console=org.apache.log4j.ConsoleAppender
log4j.appender.Console.layout=org.apache.log4j.PatternLayout
log4j.appender.Console.layout.ConversionPattern=%-5p: %c - %m%n
```

###### Zookeeper 实现类 BaseWatcher.java

```java
import org.apache.zookeeper.WatchedEvent;
import org.apache.zookeeper.Watcher;

import java.util.concurrent.CountDownLatch;

/**
 * Created by mao-siyu on 17-8-15.
 */
public class BaseWatcher implements Watcher {

    public static CountDownLatch countDownLatch = new CountDownLatch(1);

    @Override
    public void process(WatchedEvent watchedEvent) {
        if (Event.KeeperState.SyncConnected == watchedEvent.getState()) {
            countDownLatch.countDown();
        }
    }
}
```

###### 添加测试类 TestZookeeper.java

```java
import org.apache.log4j.Logger;
import org.apache.zookeeper.CreateMode;
import org.apache.zookeeper.ZooDefs;
import org.apache.zookeeper.ZooKeeper;


/**
 * Created by mao-siyu on 17-8-15.
 */
public class TestZookeeper {

    private static final Logger LOGGER = Logger.getLogger(TestZookeeper.class);
    private static final String CONNECT_STRING = "10.32.156.68:2181";
    private static final int SESSION_TIMEOUT = 5000;

    public static void main(String[] args) throws Exception {

        ZooKeeper zooKeeper = new ZooKeeper(CONNECT_STRING, SESSION_TIMEOUT, new BaseWatcher());
        LOGGER.info("================    " + zooKeeper.getState());
        BaseWatcher.countDownLatch.await();
    }
}
```
