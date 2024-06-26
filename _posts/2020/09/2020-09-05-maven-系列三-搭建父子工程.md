---
title: "Maven 系列三 搭建父子工程"
date: "2020-09-05"
categories: 
  - "maven"
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

* * *

###### 父工程 pom.xml

**父工程就一个`pom.xml`文件啥也没有， 将所有`子pom.xml`中共同的配置，都写在这里**

```markup
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">

    <modelVersion>4.0.0</modelVersion>

    <!-- 组名称， 当前工程所属的组 -->
    <groupId>com.app.cloud</groupId>
    <artifactId>app-parent</artifactId>
    <!-- 版本号不要写 SNAPSHOT -->
    <version>1.0.0</version>
    <!-- 父工程必须是 pom -->
    <packaging>pom</packaging>

    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>1.4.4.RELEASE</version>
    </parent>

    <properties>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
        <project.reporting.outputEncoding>UTF-8</project.reporting.outputEncoding>
        <java.version>1.8</java.version>
    </properties>

    <dependencyManagement>
        <dependencies>
            <dependency>
                <groupId>org.springframework.cloud</groupId>
                <artifactId>spring-cloud-dependencies</artifactId>
                <version>Camden.SR5</version>
                <type>pom</type>
                <scope>import</scope>
            </dependency>
        </dependencies>
    </dependencyManagement>

    <!-- 告诉Maven 往哪个仓库中 deploy项目 -->
    <distributionManagement>
        <repository>
            <!-- 这是 settings.xml中写好的用户/密码的ID -->
            <id>local-nexus-userid</id>
            <url>http://192.168.20.91:8081/repository/maven-releases/</url>
        </repository>
    </distributionManagement>

    <!-- 引入子工程， 如果需要批量打包，就引入modules, 如果使用自动化部署，这个就不需要了 -->
    <!-- <modules> -->
        <!-- <module>../001-webapp</module> -->
    <!-- </modules> -->

</project>

```

* * *

###### 子工程 pom.xml

```markup
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://maven.apache.org/POM/4.0.0"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <!-- 这是 module 的名称， 父工程引入modules时使用 -->
    <name>001-webapp</name>
    <!-- 组名称， 当前工程所属的组 -->
    <groupId>com.app.cloud</groupId>
    <artifactId>001-webapp</artifactId>
    <!-- 版本号不要写 0.0.1-SNAPSHOT -->
    <version>0.0.1</version>
    <packaging>jar</packaging>

    <!-- 指定父工程 -->
    <parent>
        <!-- 指定父工程所在的组 -->
        <groupId>com.app.cloud</groupId>
        <artifactId>app-parent</artifactId>
        <version>1.0.0</version>
        <!-- 告诉Maven 打包时从仓库中拉取父pom.xml -->
        <relativePath/>
    </parent>

    <dependencies>
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-gateway-server</artifactId>
        </dependency>
    </dependencies>

    <build>
        <!-- 使用 module名称， 做为打包后的文件名  -->
        <finalName>${project.name}</finalName>
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

* * *

* * *

* * *
