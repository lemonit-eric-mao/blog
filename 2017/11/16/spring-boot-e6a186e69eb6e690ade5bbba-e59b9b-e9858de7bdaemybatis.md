---
title: 'spring-boot 框架搭建 四 (配置Mybatis)'
date: '2017-11-16T13:44:37+00:00'
status: publish
permalink: /2017/11/16/spring-boot-%e6%a1%86%e6%9e%b6%e6%90%ad%e5%bb%ba-%e5%9b%9b-%e9%85%8d%e7%bd%aemybatis
author: 毛巳煜
excerpt: ''
type: post
id: 319
category:
    - spring-boot
tag: []
post_format: []
---
### 添加配置文件 com.my.springboot.common.dbconfig.MybatisConfig.java

```
<pre class="line-numbers prism-highlight" data-start="1">```java
package com.my.springboot.common.dbconfig;

import org.apache.ibatis.session.SqlSessionFactory;
import org.mybatis.spring.SqlSessionFactoryBean;
import org.mybatis.spring.annotation.MapperScan;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.autoconfigure.AutoConfigureAfter;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.core.env.Environment;
import org.springframework.core.io.DefaultResourceLoader;
import org.springframework.core.io.support.PathMatchingResourcePatternResolver;
import org.springframework.jdbc.datasource.DataSourceTransactionManager;
import org.springframework.jdbc.datasource.lookup.AbstractRoutingDataSource;
import org.springframework.transaction.annotation.EnableTransactionManagement;

/**
 * mybatis 配置
 * Created by mao-siyu on 17-8-17.
 */
@Configuration
@EnableTransactionManagement
@AutoConfigureAfter(MysqlConfig.class)
@MapperScan(basePackages = "com.my.springboot.mapper")
public class MybatisConfig {

    private static Logger logger = LoggerFactory.getLogger(MybatisConfig.class);
    /**
     * 通过前缀获取application.properties文件中的属性列表值.
     */
    @Autowired
    private Environment environment;


    /**
     * 根据数据源创建SqlSessionFactory
     */
    @Bean
    public SqlSessionFactory sqlSessionFactory(AbstractRoutingDataSource abstractRoutingDataSource) throws Exception {

        logger.info("=:|======>    根据数据源创建 SqlSessionFactory!");
        SqlSessionFactoryBean sqlSessionFactoryBean = new SqlSessionFactoryBean();
        // 多数据源注入
        sqlSessionFactoryBean.setDataSource(abstractRoutingDataSource);
        // 扫描所有 mapping/*Mapping.xml文件
        sqlSessionFactoryBean.setMapperLocations(new PathMatchingResourcePatternResolver().getResources(environment.getProperty("mybatis.mapper-locations")));
        // 扫描 mybatis-config.xml文件
        sqlSessionFactoryBean.setConfigLocation(new DefaultResourceLoader().getResource(environment.getProperty("mybatis.config-location")));
        return sqlSessionFactoryBean.getObject();
    }

    /**
     * 配置事务管理器
     */
    @Bean
    public DataSourceTransactionManager transactionManager(AbstractRoutingDataSource dataSource) throws Exception {
        logger.info("=:|======>    配置事务管理器!");
        return new DataSourceTransactionManager(dataSource);
    }

}

```
```