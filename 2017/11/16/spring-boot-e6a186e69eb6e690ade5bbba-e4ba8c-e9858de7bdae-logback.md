---
title: 'spring-boot 框架搭建 二 (配置 logback )'
date: '2017-11-16T13:43:47+00:00'
status: publish
permalink: /2017/11/16/spring-boot-%e6%a1%86%e6%9e%b6%e6%90%ad%e5%bb%ba-%e4%ba%8c-%e9%85%8d%e7%bd%ae-logback
author: 毛巳煜
excerpt: ''
type: post
id: 314
category:
    - spring-boot
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
创建基础目录与基础文件  
common/dbconfig/ `多数据源配置目录`  
controller/  
entity/  
service/  
mapper/  
mapping/  
`application.properties`  
`application-dev.properties`  
`application-prod.properties`  
`logback.xml`  
`mybatis-config.xml`

### 自定义logger 输入格式 添加 logback.xml 文件

```
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
    
    <logger level="DEBUG" name="com.my.springboot"></logger>
</configuration>

```

### 配置 application.properties

```
spring.profiles.active=dev

```

### 配置 application-dev.properties application-prod.properties

```
########################################################
#### logback
########################################################
logging.config=classpath:logback.xml

########################################################
#### mysql-datasource-master
########################################################
spring.datasource.hikari.master.jdbc-url=jdbc:mysql://10.32.156.52:3306/masterTest?useUnicode=true&characterEncoding=utf8&useSSL=true&autoReconnect=true&failOverReadOnly=false&maxReconnects=10
spring.datasource.hikari.master.username=dlfc
spring.datasource.hikari.master.password=dlfc#123
spring.datasource.hikari.master.driver-class-name=com.mysql.jdbc.Driver
spring.datasource.hikari.master.maximum-pool-size=15
spring.datasource.hikari.master.auto-commit=true

########################################################
#### mysql-datasource-slave
########################################################

spring.datasource.hikari.slave.jdbc-url=jdbc:mysql://10.32.156.52:3306/slave1Test?useUnicode=true&characterEncoding=utf8&useSSL=true&autoReconnect=true&failOverReadOnly=false&maxReconnects=10
spring.datasource.hikari.slave.username=dlfc
spring.datasource.hikari.slave.password=dlfc#123
spring.datasource.hikari.slave.driver-class-name=com.mysql.jdbc.Driver
spring.datasource.hikari.slave.maximum-pool-size=15
spring.datasource.hikari.slave.auto-commit=true

########################################################
#### redis-datasource
########################################################
datasource.redis.url=jdbc:redis://localhost:3306/test?useUnicode=true&characterEncoding=utf8&useSSL=true&autoReconnect=true&failOverReadOnly=false&maxReconnects=10
datasource.redis.username=root
datasource.redis.password=root
datasource.redis.driverClassName=com.mysql.jdbc.Driver
datasource.redis.max-active=20
datasource.redis.max-idle=8
datasource.redis.min-idle=8
datasource.redis.initial-size=10

########################################################
#### mongo-datasource
########################################################
datasource.mongo.url=jdbc:mongo://localhost:3306/test?useUnicode=true&characterEncoding=utf8&useSSL=true&autoReconnect=true&failOverReadOnly=false&maxReconnects=10
datasource.mongo.username=root
datasource.mongo.password=root
datasource.mongo.driverClassName=com.mysql.jdbc.Driver
datasource.mongo.max-active=20
datasource.mongo.max-idle=8
datasource.mongo.min-idle=8
datasource.mongo.initial-size=10

########################################################
#### mybatis
########################################################
mybatis.config-location=classpath:mybatis-config.xml
mybatis.mapper-locations=classpath:mapping/*Mapping.xml

```

### 配置 mybatis-config.xml

```

<configuration>
    
    <settings>
        
        <setting name="cacheEnabled" value="true"></setting>

        
        <setting name="lazyLoadingEnabled" value="true"></setting>

        
        <setting name="aggressiveLazyLoading" value="true"></setting>

        
        <setting name="multipleResultSetsEnabled" value="true"></setting>

        
        <setting name="useColumnLabel" value="true"></setting>

        
        <setting name="useGeneratedKeys" value="false"></setting>

        
        <setting name="autoMappingBehavior" value="PARTIAL"></setting>

        
        <setting name="defaultExecutorType" value="SIMPLE"></setting>

        
        <setting name="mapUnderscoreToCamelCase" value="true"></setting>

        
        <setting name="localCacheScope" value="SESSION"></setting>

        
        <setting name="jdbcTypeForNull" value="NULL"></setting>
    </settings>
</configuration>

```

![](http://qiniu.dev-share.top/image/spring-boot-2.png)