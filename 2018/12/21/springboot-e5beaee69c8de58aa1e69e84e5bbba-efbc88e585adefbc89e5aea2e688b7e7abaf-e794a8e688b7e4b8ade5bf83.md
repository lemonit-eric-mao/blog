---
title: 'SpringBoot 微服务构建 （六）客户端  用户中心'
date: '2018-12-21T03:07:47+00:00'
status: publish
permalink: /2018/12/21/springboot-%e5%be%ae%e6%9c%8d%e5%8a%a1%e6%9e%84%e5%bb%ba-%ef%bc%88%e5%85%ad%ef%bc%89%e5%ae%a2%e6%88%b7%e7%ab%af-%e7%94%a8%e6%88%b7%e4%b8%ad%e5%bf%83
author: 毛巳煜
excerpt: ''
type: post
id: 3378
category:
    - spring-boot
tag: []
post_format: []
---
##### user-center

- 操作系统: ubuntu 16.04
- 开发工具: idea
- jdk: 1.8
- spring-boot: 1.5.17
- 项目: user-center

###### user-center 项目作用是 正式开始业务开发

##### 项目结构

```
user-center
.
│ pom.xml
└─src
    └─main
       ├─java
       │  └─user
       │      └─center
       │          │  UserCenterApplication.java
       │          │
       │          └─common
       │              └─config
       │                      MybatisConfig.java
       │                      MysqlConfig.java
       │                      Swagger2.java
       │
       └─resources
           │  bootstrap.yml
           │
           └─config
                   logback-config.xml
                   mybatis-config.xml

```

##### 程序入口 UserCenterApplication.java

```java
package user.center;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.netflix.eureka.EnableEurekaClient;

@SpringBootApplication
@EnableEurekaClient
public class UserCenterApplication {

    public static void main(String[] args) {
        SpringApplication.run(UserCenterApplication.class, args);
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
    
    <logger level="DEBUG" name="user.center"></logger>
</configuration>

```
```

##### mybatis-config.xml

```
<pre data-language="XML">```markup
<?xml version="1.0" encoding="UTF-8" ??>

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
```

##### bootstrap.yml

```yml
# 必须使用 bootstrap.yml 要不然加载配置文件会失败
spring:
  application:
    name: user-center
#  # 调用本地文件
#  profiles:
#    active: dev
    # 调用配置中心的文件配置
  cloud:
    config:
      # 对应的是 framework-config-center 配置服务中的 {profile}
#      profile: dev
      profile: test
#      profile: prod
      # 对应的分支
      label: master
      # 测试服-配置中心URL地址; 当服务器分布式部署时，必须是使用地址的
      uri: http://172.20.60.14:8762
      # 本地-配置中心URL地址;
#      uri: http://127.0.0.1:8762
      # 当regist-center 与 gateway-zuul 在同一个系统时可用
#      discovery:
#        enabled: true
#        serviceId: framework-config-center


########################################################
#### 引入 logback 配置文件
########################################################
logging:
  config: classpath:config/logback-config.xml

########################################################
#### 引入 Mybatis 配置文件
########################################################
mybatis:
    mapperLocations: classpath:mappings/*.xml
    configLocation: classpath:config/mybatis-config.xml

```

##### pom.xml

```
<pre data-language="XML">```markup
<?xml version="1.0" encoding="UTF-8"??>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemalocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelversion>4.0.0</modelversion>

    <groupid>user.center</groupid>
    <artifactid>user-center</artifactid>
    <version>0.0.1-RELEASE</version>
    
    <packaging>jar</packaging>

    <name>user-center</name>
    <description>Demo project for Spring Boot</description>

    <parent>
        <groupid>framework.parent</groupid>
        <artifactid>framework-parent</artifactid>
        <version>0.0.1-RELEASE</version>
        <relativepath></relativepath> 
    </parent>

    <dependencies>

        
        <dependency>
            <groupid>org.springframework.boot</groupid>
            <artifactid>spring-boot-starter-web</artifactid>
        </dependency>

        
        <dependency>
            <groupid>com.google.guava</groupid>
            <artifactid>guava</artifactid>
        </dependency>

        
        <dependency>
            <groupid>org.springframework.boot</groupid>
            <artifactid>spring-boot-starter-actuator</artifactid>
        </dependency>

        
        <dependency>
            <groupid>org.mybatis.spring.boot</groupid>
            <artifactid>mybatis-spring-boot-starter</artifactid>
        </dependency>

        
        <dependency>
            <groupid>mysql</groupid>
            <artifactid>mysql-connector-java</artifactid>
            <scope>runtime</scope>
        </dependency>

        
        <dependency>
            <groupid>com.zaxxer</groupid>
            <artifactid>HikariCP</artifactid>
        </dependency>

        
        <dependency>
            <groupid>org.projectlombok</groupid>
            <artifactid>lombok</artifactid>
            <optional>true</optional>
        </dependency>

        
        <dependency>
            <groupid>io.springfox</groupid>
            <artifactid>springfox-swagger2</artifactid>
        </dependency>

        
        <dependency>
            <groupid>io.springfox</groupid>
            <artifactid>springfox-swagger-ui</artifactid>
        </dependency>

        
        <dependency>
            <groupid>org.springframework.cloud</groupid>
            <artifactid>spring-cloud-starter-config</artifactid>
        </dependency>

    </dependencies>

</project>

```
```

##### MybatisConfig.java

```java
package user.center.common.config;

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

/**
 * mybatis 配置
 * Created by mao-siyu on 17-8-17.
 */
@Configuration
@AutoConfigureAfter(MysqlConfig.class)
@MapperScan(basePackages = "user.center.mapper")
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
        // 扫描所有 mappings/*Mapping.xml文件
        sqlSessionFactoryBean.setMapperLocations(new PathMatchingResourcePatternResolver().getResources(environment.getProperty("mybatis.mapperLocations")));
        // 扫描 mybatis-config.xml文件
        sqlSessionFactoryBean.setConfigLocation(new DefaultResourceLoader().getResource(environment.getProperty("mybatis.configLocation")));
        return sqlSessionFactoryBean.getObject();
    }

}

```

##### MysqlConfig.java

```java
package user.center.common.config;

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

import javax.sql.DataSource;
import java.util.HashMap;
import java.util.Map;

/**
 * mysql 数据源配置
 * Created by mao-siyu on 17-8-17.
 */
@Configuration
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
        hikariDataSource.setJdbcUrl(environment.getProperty(PREFIX + "master.jdbcUrl"));
        hikariDataSource.setUsername(environment.getProperty(PREFIX + "master.username"));
        hikariDataSource.setPassword(environment.getProperty(PREFIX + "master.password"));
        hikariDataSource.setDriverClassName(environment.getProperty(PREFIX + "master.driverClassName"));
        hikariDataSource.setMaximumPoolSize(Integer.valueOf(environment.getProperty(PREFIX + "master.maximumPoolSize")));
        hikariDataSource.setAutoCommit(Boolean.valueOf(environment.getProperty(PREFIX + "master.autoCommit")));
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
        hikariDataSource.setJdbcUrl(environment.getProperty(PREFIX + "slave.jdbcUrl"));
        hikariDataSource.setUsername(environment.getProperty(PREFIX + "slave.username"));
        hikariDataSource.setPassword(environment.getProperty(PREFIX + "slave.password"));
        hikariDataSource.setDriverClassName(environment.getProperty(PREFIX + "slave.driverClassName"));
        hikariDataSource.setMaximumPoolSize(Integer.valueOf(environment.getProperty(PREFIX + "slave.maximumPoolSize")));
        hikariDataSource.setAutoCommit(Boolean.valueOf(environment.getProperty(PREFIX + "slave.autoCommit")));
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

##### Swagger2.java

```java
package user.center.common.config;

import io.swagger.annotations.ApiOperation;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import springfox.documentation.builders.ApiInfoBuilder;
import springfox.documentation.builders.PathSelectors;
import springfox.documentation.builders.RequestHandlerSelectors;
import springfox.documentation.service.ApiInfo;
import springfox.documentation.spi.DocumentationType;
import springfox.documentation.spring.web.plugins.Docket;
import springfox.documentation.swagger2.annotations.EnableSwagger2;

/**
 * Created by mao_siyu on 2018/11/27.
 */
@Configuration
@EnableSwagger2
public class Swagger2 {
    @Bean
    public Docket restApi() {
        return new Docket(DocumentationType.SWAGGER_2)
                .apiInfo(apiInfo())
                .select()
                .paths(PathSelectors.any())
                .apis(RequestHandlerSelectors.withMethodAnnotation(ApiOperation.class))
                .build();
    }

    private ApiInfo apiInfo() {
        return new ApiInfoBuilder()
                .title("Springcloud API")
                .version("2.0")
                .build();
    }
}

```

###### http://127.0.0.1:8080/user/swagger-ui.html