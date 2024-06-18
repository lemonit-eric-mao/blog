---
title: 'spring-boot 框架搭建 三  (配置多数据源)'
date: '2017-11-16T13:44:13+00:00'
status: publish
permalink: /2017/11/16/spring-boot-%e6%a1%86%e6%9e%b6%e6%90%ad%e5%bb%ba-%e4%b8%89-%e9%85%8d%e7%bd%ae%e5%a4%9a%e6%95%b0%e6%8d%ae%e6%ba%90
author: 毛巳煜
excerpt: ''
type: post
id: 317
category:
    - spring-boot
tag: []
post_format: []
hestia_layout_select:
    - default
---
### 添加数据库连接池 配置多数据源

### 数据库连接池选择 HikariCP

```
<pre data-language="XML">```markup

<dependency>
    <groupid>com.zaxxer</groupid>
    <artifactid>HikariCP</artifactid>
    <version>2.6.3</version>
</dependency>

```
```

### 添加配置文件 com.my.springboot.common.dbconfig.MysqlConfig.java

```java
package com.my.springboot.common.dbconfig;

import com.zaxxer.hikari.HikariDataSource;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Primary;
import org.springframework.core.env.Environment;
import org.springframework.jdbc.datasource.lookup.AbstractRoutingDataSource;
import org.springframework.transaction.annotation.EnableTransactionManagement;

import javax.sql.DataSource;
import java.util.HashMap;
import java.util.Map;

/**
 * mysql 数据源配置
 * Created by mao-siyu on 17-8-17.
 */
@Configuration
@EnableTransactionManagement
public class MysqlConfig {

    private static final String PREFIX = "spring.datasource.hikari.";

    private static Logger logger = LoggerFactory.getLogger(MysqlConfig.class);

    /**
     * 通过前缀获取application.properties文件中的属性列表值.
     */
    @Autowired
    private Environment environment;


    /**
     * 初始化注入 Hikari 主数据源
     *
     * @return
     */
    @Primary
    @Bean(name = "masterDataSource")
    public DataSource masterDataSource() {
        logger.info("=:|======>    初始化注入 Hikari 主数据源!");
        HikariDataSource hikariDataSource = new HikariDataSource();
        hikariDataSource.setJdbcUrl(environment.getProperty(PREFIX + "master.jdbc-url"));
        hikariDataSource.setUsername(environment.getProperty(PREFIX + "master.username"));
        hikariDataSource.setPassword(environment.getProperty(PREFIX + "master.password"));
        hikariDataSource.setDriverClassName(environment.getProperty(PREFIX + "master.driver-class-name"));
        hikariDataSource.setMaximumPoolSize(Integer.valueOf(environment.getProperty(PREFIX + "master.maximum-pool-size")));
        hikariDataSource.setAutoCommit(Boolean.valueOf(environment.getProperty(PREFIX + "master.auto-commit")));
        return hikariDataSource;
    }

    /**
     * 初始化注入 Hikari 从数据源
     *
     * @return
     */
    @Bean(name = "slaveDataSource")
    public DataSource slaveDataSource() {
        logger.info("=:|======>    初始化注入 Hikari 从数据源!");
        HikariDataSource hikariDataSource = new HikariDataSource();
        hikariDataSource.setJdbcUrl(environment.getProperty(PREFIX + "slave.jdbc-url"));
        hikariDataSource.setUsername(environment.getProperty(PREFIX + "slave.username"));
        hikariDataSource.setPassword(environment.getProperty(PREFIX + "slave.password"));
        hikariDataSource.setDriverClassName(environment.getProperty(PREFIX + "slave.driver-class-name"));
        hikariDataSource.setMaximumPoolSize(Integer.valueOf(environment.getProperty(PREFIX + "slave.maximum-pool-size")));
        hikariDataSource.setAutoCommit(Boolean.valueOf(environment.getProperty(PREFIX + "slave.auto-commit")));
        return hikariDataSource;
    }

    /**
     * @Primary 该注解表示在同一个接口有多个实现类可以注入的时候，默认选择哪一个，而不是让@autowire注解报错
     * @Qualifier 根据名称进行注入，通常是在具有相同的多个类型的实例的一个注入（例如有多个DataSource类型的实例）
     */
    @Bean(name = "abstractRoutingDataSource")
    public AbstractRoutingDataSource abstractRoutingDataSource(@Qualifier("masterDataSource") DataSource masterDataSource, @Qualifier("slaveDataSource") DataSource slaveDataSource1) {

        logger.info("=:|======>    初始化注入 mysql 动态数据源!");
        Map<object object=""> targetDataSources = new HashMap();
        targetDataSources.put(DatabaseType.MASTER, masterDataSource);
        targetDataSources.put(DatabaseType.SLAVE1, slaveDataSource1);

        // 动态数据源（需要继承AbstractRoutingDataSource）
        AbstractRoutingDataSource dataSource = new AbstractRoutingDataSource() {
            @Override
            protected Object determineCurrentLookupKey() {
                return DatabaseContextHolder.getDatabaseType();
            }
        };

        // 该方法是AbstractRoutingDataSource的方法
        dataSource.setTargetDataSources(targetDataSources);
        // 默认的datasource设置为 masterDataSource
        dataSource.setDefaultTargetDataSource(masterDataSource);

        return dataSource;
    }

    /**
     * 作用：
     * 1、保存一个线程安全的DatabaseType容器
     */
    public static class DatabaseContextHolder {
        private static final ThreadLocal<databasetype> contextHolder = new ThreadLocal();

        public static void setDatabaseType(DatabaseType type) {
            contextHolder.set(type);
        }

        public static DatabaseType getDatabaseType() {
            return contextHolder.get();
        }
    }

    /**
     * 列出所有的数据源key（常用数据库名称来命名）
     * 注意：
     * 1）这里数据源与数据库是一对一的
     * 2）DatabaseType中的变量名称就是数据库的名称
     */
    public enum DatabaseType {
        MASTER, SLAVE1
    }
}
</databasetype></object>
```