---
title: 'Maven 系列三 搭建父子工程'
date: '2020-09-05T01:40:49+00:00'
status: publish
permalink: /2020/09/05/maven-%e7%b3%bb%e5%88%97%e4%b8%89-%e6%90%ad%e5%bb%ba%e7%88%b6%e5%ad%90%e5%b7%a5%e7%a8%8b
author: 毛巳煜
excerpt: ''
type: post
id: 6098
category:
    - Maven
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
###### 父子工程列表

```ruby
.
│
├─001-webapp                    # 子工程
│  │  pom.xml
│  │
│  └─src
│      └─main
│          ├─java
│          │  └─com
│          │      └─app
│          │          └─cloud
│          │              └─webapp
│          │                      WebappServerApplication.java
│          │
│          └─resources
│                  application.yml
│
│
└─app-parent                    # 父工程
        pom.xml


```

- - - - - -

###### 父工程 pom.xml

**父工程就一个`pom.xml`文件啥也没有， 将所有`子pom.xml`中共同的配置，都写在这里**

```
<pre data-language="XML">```markup
<?xml version="1.0" encoding="UTF-8"??>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemalocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">

    <modelversion>4.0.0</modelversion>

    
    <groupid>com.app.cloud</groupid>
    <artifactid>app-parent</artifactid>
    
    <version>1.0.0</version>
    
    <packaging>pom</packaging>

    <parent>
        <groupid>org.springframework.boot</groupid>
        <artifactid>spring-boot-starter-parent</artifactid>
        <version>1.4.4.RELEASE</version>
    </parent>

    <properties>
        <project.build.sourceencoding>UTF-8</project.build.sourceencoding>
        <project.reporting.outputencoding>UTF-8</project.reporting.outputencoding>
        <java.version>1.8</java.version>
    </properties>

    <dependencymanagement>
        <dependencies>
            <dependency>
                <groupid>org.springframework.cloud</groupid>
                <artifactid>spring-cloud-dependencies</artifactid>
                <version>Camden.SR5</version>
                <type>pom</type>
                <scope>import</scope>
            </dependency>
        </dependencies>
    </dependencymanagement>

    
    <distributionmanagement>
        <repository>
            
            <id>local-nexus-userid</id>
            <url>http://192.168.20.91:8081/repository/maven-releases/</url>
        </repository>
    </distributionmanagement>

    
    
        
    

</project>


```
```

- - - - - -

###### 子工程 pom.xml

```
<pre data-language="XML">```markup
<?xml version="1.0" encoding="UTF-8"??>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemalocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelversion>4.0.0</modelversion>

    
    <name>001-webapp</name>
    
    <groupid>com.app.cloud</groupid>
    <artifactid>001-webapp</artifactid>
    
    <version>0.0.1</version>
    <packaging>jar</packaging>

    
    <parent>
        
        <groupid>com.app.cloud</groupid>
        <artifactid>app-parent</artifactid>
        <version>1.0.0</version>
        
        <relativepath></relativepath>
    </parent>

    <dependencies>
        <dependency>
            <groupid>org.springframework.cloud</groupid>
            <artifactid>spring-cloud-starter-gateway-server</artifactid>
        </dependency>
    </dependencies>

    <build>
        
        <finalname>${project.name}</finalname>
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

- - - - - -

- - - - - -

- - - - - -