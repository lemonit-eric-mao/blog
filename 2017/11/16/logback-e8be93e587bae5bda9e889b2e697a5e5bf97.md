---
title: 'logback 输出彩色日志'
date: '2017-11-16T13:19:28+00:00'
status: publish
permalink: /2017/11/16/logback-%e8%be%93%e5%87%ba%e5%bd%a9%e8%89%b2%e6%97%a5%e5%bf%97
author: 毛巳煜
excerpt: ''
type: post
id: 272
category:
    - Java
tag: []
post_format: []
wb_sst_seo:
    - 'a:3:{i:0;s:0:"";i:1;s:0:"";i:2;s:0:"";}'
hestia_layout_select:
    - sidebar-right
---
**开发工具: IDEA**

**项目类型: maven**

### pom.xml

```
<pre data-language="XML">```markup
<?xml version="1.0" encoding="UTF-8"??>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemalocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelversion>4.0.0</modelversion>

    <groupid>cn.com.plugins</groupid>
    <artifactid>ExtendFlinkPlugins</artifactid>
    <version>1.0-SNAPSHOT</version>

    <properties>
        <maven.compiler.source>8</maven.compiler.source>
        <maven.compiler.target>8</maven.compiler.target>
    </properties>

    <dependencies>

        
        <dependency>
            <groupid>org.slf4j</groupid>
            <artifactid>slf4j-api</artifactid>
            <version>1.7.25</version>
        </dependency>

        <dependency>
            <groupid>ch.qos.logback</groupid>
            <artifactid>logback-classic</artifactid>
            <version>1.2.3</version>
        </dependency>
        

    </dependencies>

</project>

```
```

### logback.xml

```
<pre data-language="XML">```markup
<?xml version="1.0"??>
<configuration>
    
    <appender class="ch.qos.logback.core.ConsoleAppender" name="console">
        <encoder>
            <pattern>%d{yyyy-MM-dd HH:mm:ss.SSS} %highlight(%5p [%15.15t]) %cyan(%-40.40c{1.}) : %highlight(%m%n)</pattern>
        </encoder>
    </appender>
    
    <root>
        
        <level value="ERROR"></level>
        <appender-ref ref="console"></appender-ref>
    </root>
    
    <logger level="DEBUG" name="cn.com.source"></logger>
</configuration>


```
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