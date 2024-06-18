---
title: 'SpringBoot 微服务构建 （二） 客户端 Parent'
date: '2017-12-25T14:25:52+00:00'
status: publish
permalink: /2017/12/25/springboot-%e5%be%ae%e6%9c%8d%e5%8a%a1%e6%9e%84%e5%bb%ba-%ef%bc%88%e4%ba%8c%ef%bc%89-%e5%ae%a2%e6%88%b7%e7%ab%af-parent
author: 毛巳煜
excerpt: ''
type: post
id: 1803
category:
    - spring-boot
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
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

```
<pre data-language="XML">```markup
<?xml version="1.0" encoding="UTF-8"??>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemalocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelversion>4.0.0</modelversion>

    <groupid>framework.parent</groupid>
    <artifactid>framework-parent</artifactid>
    <version>0.0.1-RELEASE</version>
    
    
    <packaging>pom</packaging>

    <name>framework-parent</name>
    <description>Demo project for Spring Boot</description>

    <parent>
        <groupid>org.springframework.boot</groupid>
        <artifactid>spring-boot-starter-parent</artifactid>
        <version>1.5.17.RELEASE</version>
        <relativepath></relativepath> 
    </parent>

    <properties>
        <project.build.sourceencoding>UTF-8</project.build.sourceencoding>
        <project.reporting.outputencoding>UTF-8</project.reporting.outputencoding>
        <java.version>1.8</java.version>
        <spring-cloud.version>Dalston.SR5</spring-cloud.version>
        <swagger2.version>2.9.2</swagger2.version>
        <mybatis.version>1.3.2</mybatis.version>
        <hikaricp.version>3.2.0</hikaricp.version>
        <guava.version>20.0</guava.version>
    </properties>

    
    <dependencies>

        
        <dependency>
            <groupid>org.springframework.boot</groupid>
            <artifactid>spring-boot-starter</artifactid>
        </dependency>

        
        <dependency>
            <groupid>org.springframework.boot</groupid>
            <artifactid>spring-boot-starter-test</artifactid>
            <scope>test</scope>
        </dependency>

        
        <dependency>
            <groupid>org.springframework.cloud</groupid>
            <artifactid>spring-cloud-starter-eureka</artifactid>
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

            
            <dependency>
                <groupid>org.mybatis.spring.boot</groupid>
                <artifactid>mybatis-spring-boot-starter</artifactid>
                <version>${mybatis.version}</version>
                
                <exclusions>
                    <exclusion>
                        <groupid>org.apache.tomcat</groupid>
                        <artifactid>tomcat-jdbc</artifactid>
                    </exclusion>
                </exclusions>
            </dependency>

            
            <dependency>
                <groupid>com.zaxxer</groupid>
                <artifactid>HikariCP</artifactid>
                <version>${HikariCP.version}</version>
            </dependency>

            
            <dependency>
                <groupid>io.springfox</groupid>
                <artifactid>springfox-swagger2</artifactid>
                <version>${swagger2.version}</version>
            </dependency>

            
            <dependency>
                <groupid>io.springfox</groupid>
                <artifactid>springfox-swagger-ui</artifactid>
                <version>${swagger2.version}</version>
            </dependency>

            
            <dependency>
                <groupid>com.google.guava</groupid>
                <artifactid>guava</artifactid>
                <version>${guava.version}</version>
            </dependency>

        </dependencies>
    </dependencymanagement>

    
    <distributionmanagement>
        <repository>
            <id>framework-parent-releases</id>
            <url>http://nexus.dev-share.top/repository/framework-parent-releases/</url>
        </repository>
        <snapshotrepository>
            <id>framework-parent-snapshots</id>
            <url>http://nexus.dev-share.top/repository/framework-parent-snapshots/</url>
        </snapshotrepository>
    </distributionmanagement>

    
    <build>
        <finalname>${project.artifactId}</finalname>
        <plugins>
            <plugin>
                <groupid>org.springframework.boot</groupid>
                <artifactid>spring-boot-maven-plugin</artifactid>
                <configuration>
                    <fork>true</fork>
                    <executable>true</executable>
                </configuration>
            </plugin>
        </plugins>
    </build>
</project>

```
```