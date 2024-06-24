---
title: "logback 输出彩色日志"
date: "2017-11-16"
categories: 
  - "java"
---

**开发工具: IDEA**

**项目类型: maven**

### pom.xml

```markup
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>cn.com.plugins</groupId>
    <artifactId>ExtendFlinkPlugins</artifactId>
    <version>1.0-SNAPSHOT</version>

    <properties>
        <maven.compiler.source>8</maven.compiler.source>
        <maven.compiler.target>8</maven.compiler.target>
    </properties>

    <dependencies>

        <!-- 日志输出 START -->
        <dependency>
            <groupId>org.slf4j</groupId>
            <artifactId>slf4j-api</artifactId>
            <version>1.7.25</version>
        </dependency>

        <dependency>
            <groupId>ch.qos.logback</groupId>
            <artifactId>logback-classic</artifactId>
            <version>1.2.3</version>
        </dependency>
        <!-- 日志输出 END -->

    </dependencies>

</project>
```

### logback.xml

```markup
<?xml version="1.0"?>
<configuration>
    <!-- ch.qos.logback.core.ConsoleAppender 控制台输出 -->
    <appender name="console" class="ch.qos.logback.core.ConsoleAppender">
        <encoder>
            <pattern>%d{yyyy-MM-dd HH:mm:ss.SSS} %highlight(%5p [%15.15t]) %cyan(%-40.40c{1.}) : %highlight(%m%n)</pattern>
        </encoder>
    </appender>
    <!-- 日志级别 -->
    <root>
        <!-- 默认日志级别 -->
        <level value="ERROR"/>
        <appender-ref ref="console"/>
    </root>
    <!-- 指定 cn.com.source 路径下的日志级别为 DEBUG -->
    <logger name="cn.com.source" level="DEBUG"></logger>
</configuration>

```

### Test.java

```java
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Created by mao-siyu on 17-8-15.
 */
public class Test {

    private static final Logger LOGGER = LoggerFactory.getLogger(Test.class);

    public static void main(String[] args) throws Exception {
        LOGGER.debug(" This is debug!!!");
        LOGGER.info(" This is info!!!");
        LOGGER.warn(" This is warn!!!");
        LOGGER.error(" This is error!!!");
    }
}

```
