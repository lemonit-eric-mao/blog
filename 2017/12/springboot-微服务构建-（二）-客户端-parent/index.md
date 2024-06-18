---
title: "SpringBoot 微服务构建 （二） 客户端 Parent"
date: "2017-12-25"
categories: 
  - "spring-boot"
---

##### framework-parent

- 操作系统: ubuntu 16.04
- 开发工具: idea
- jdk: 1.8
- spring-boot: 1.5.17
- 项目: framework-parent

###### parent项目主要是为了统一管理 maven项目的版本、与共通插件的引用

##### 项目结构

```
framework-parent
.
└─pom.xml
```

##### pom.xml

```markup
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>framework.parent</groupId>
    <artifactId>framework-parent</artifactId>
    <version>0.0.1-RELEASE</version>
    <!--<version>0.0.1-SNAPSHOT</version>-->
    <!--父项目必须是 <packaging>pom</packaging> 就是不会把项目发布成jar包-->
    <packaging>pom</packaging>

    <name>framework-parent</name>
    <description>Demo project for Spring Boot</description>

    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>1.5.17.RELEASE</version>
        <relativePath/> <!-- lookup parent from repository -->
    </parent>

    <properties>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
        <project.reporting.outputEncoding>UTF-8</project.reporting.outputEncoding>
        <java.version>1.8</java.version>
        <spring-cloud.version>Dalston.SR5</spring-cloud.version>
        <swagger2.version>2.9.2</swagger2.version>
        <mybatis.version>1.3.2</mybatis.version>
        <HikariCP.version>3.2.0</HikariCP.version>
        <guava.version>20.0</guava.version>
    </properties>

    <!-- 会实际下载jar包 -->
    <dependencies>

        <!-- Spring Boot的核心启动器，包含了自动配置、日志和YAML。-->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter</artifactId>
        </dependency>

        <!-- 支持常规的测试依赖，包括JUnit、Hamcrest、Mockito以及spring-test模块。-->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>

        <!-- Eureka客户端 -->
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-eureka</artifactId>
        </dependency>

    </dependencies>

    <!-- 只是对版本进行管理，不会实际引入jar -->
    <dependencyManagement>
        <dependencies>

            <dependency>
                <groupId>org.springframework.cloud</groupId>
                <artifactId>spring-cloud-dependencies</artifactId>
                <version>${spring-cloud.version}</version>
                <type>pom</type>
                <scope>import</scope>
                <!--排除这个slf4j-log4j12-->
                <!--<exclusions>-->
                    <!--<exclusion>-->
                        <!--<groupId>org.slf4j</groupId>-->
                        <!--<artifactId>slf4j-log4j12</artifactId>-->
                    <!--</exclusion>-->
                <!--</exclusions>-->
            </dependency>

            <!-- mybatis -->
            <dependency>
                <groupId>org.mybatis.spring.boot</groupId>
                <artifactId>mybatis-spring-boot-starter</artifactId>
                <version>${mybatis.version}</version>
                <!-- 排除tomcat jdbc -->
                <exclusions>
                    <exclusion>
                        <groupId>org.apache.tomcat</groupId>
                        <artifactId>tomcat-jdbc</artifactId>
                    </exclusion>
                </exclusions>
            </dependency>

            <!-- HikariCP -->
            <dependency>
                <groupId>com.zaxxer</groupId>
                <artifactId>HikariCP</artifactId>
                <version>${HikariCP.version}</version>
            </dependency>

            <!-- swagger2 -->
            <dependency>
                <groupId>io.springfox</groupId>
                <artifactId>springfox-swagger2</artifactId>
                <version>${swagger2.version}</version>
            </dependency>

            <!-- swagger-ui -->
            <dependency>
                <groupId>io.springfox</groupId>
                <artifactId>springfox-swagger-ui</artifactId>
                <version>${swagger2.version}</version>
            </dependency>

            <!-- guava -->
            <dependency>
                <groupId>com.google.guava</groupId>
                <artifactId>guava</artifactId>
                <version>${guava.version}</version>
            </dependency>

        </dependencies>
    </dependencyManagement>

    <!--发布管理 deploy 配置-->
    <distributionManagement>
        <repository>
            <id>framework-parent-releases</id>
            <url>http://nexus.dev-share.top/repository/framework-parent-releases/</url>
        </repository>
        <snapshotRepository>
            <id>framework-parent-snapshots</id>
            <url>http://nexus.dev-share.top/repository/framework-parent-snapshots/</url>
        </snapshotRepository>
    </distributionManagement>

    <!--项目打包配置-必须 所有子项目共享-->
    <build>
        <finalName>${project.artifactId}</finalName>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
                <configuration>
                    <fork>true</fork>
                    <executable>true</executable>
                </configuration>
            </plugin>
        </plugins>
    </build>
</project>
```
