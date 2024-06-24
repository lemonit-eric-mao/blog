---
title: "spring-boot 框架搭建 二 (配置 logback )"
date: "2017-11-16"
categories: 
  - "spring-boot"
---

创建基础目录与基础文件 common/dbconfig/ `多数据源配置目录` controller/ entity/ service/ mapper/ mapping/ `application.properties` `application-dev.properties` `application-prod.properties` `logback.xml` `mybatis-config.xml`

### 自定义logger 输入格式 添加 logback.xml 文件

```
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
    <!-- 指定 com.my.springboot 路径下的日志级别为 DEBUG -->
    <logger name="com.my.springboot" level="DEBUG"></logger>
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
<!DOCTYPE configuration    PUBLIC "-//mybatis.org//DTD Config 3.0//EN"    "http://mybatis.org/dtd/mybatis-3-config.dtd">
<configuration>
    <!-- 全局参数 -->
    <settings>
        <!-- 使全局的映射器启用或禁用缓存。 -->
        <setting name="cacheEnabled" value="true"/>

        <!-- 全局启用或禁用延迟加载。当禁用时，所有关联对象都会即时加载。 -->
        <setting name="lazyLoadingEnabled" value="true"/>

        <!-- 当启用时，有延迟加载属性的对象在被调用时将会完全加载任意属性。否则，每种属性将会按需要加载。 -->
        <setting name="aggressiveLazyLoading" value="true"/>

        <!-- 是否允许单条sql 返回多个数据集  (取决于驱动的兼容性) default:true -->
        <setting name="multipleResultSetsEnabled" value="true"/>

        <!-- 是否可以使用列的别名 (取决于驱动的兼容性) default:true -->
        <setting name="useColumnLabel" value="true"/>

        <!-- 允许JDBC 生成主键。需要驱动器支持。如果设为了true，这个设置将强制使用被生成的主键，有一些驱动器不兼容不过仍然可以执行。  default:false  -->
        <setting name="useGeneratedKeys" value="false"/>

        <!-- 指定 MyBatis 如何自动映射 数据基表的列 NONE：不隐射　PARTIAL:部分  FULL:全部  -->
        <setting name="autoMappingBehavior" value="PARTIAL"/>

        <!-- 这是默认的执行类型  （SIMPLE: 简单； REUSE: 执行器可能重复使用prepared statements语句；BATCH: 执行器可以重复执行语句和批量更新）  -->
        <setting name="defaultExecutorType" value="SIMPLE"/>

        <!-- 使用驼峰命名法转换字段。 -->
        <setting name="mapUnderscoreToCamelCase" value="true"/>

        <!-- 设置本地缓存范围 session:就会有数据的共享  statement:语句范围 (这样就不会有数据的共享 ) defalut:session -->
        <setting name="localCacheScope" value="SESSION"/>

        <!-- 设置但JDBC类型为空时,某些驱动程序 要指定值,default:OTHER，插入空值时不需要指定类型 -->
        <setting name="jdbcTypeForNull" value="NULL"/>
    </settings>
</configuration>
```

![](http://qiniu.dev-share.top/image/spring-boot-2.png)
