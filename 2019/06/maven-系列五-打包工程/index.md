---
title: "Maven 系列五 打包工程"
date: "2019-06-28"
categories: 
  - "maven"
---

* * *

##### java 文件打jar包

###### 创建 SystemProperty.java 文件

```java
/**
 * eric.mao
 */
public class SystemProperty {

    public static void main(String[] args) {
        System.out.print("JVM Param: ");
        // 打印传入的JVM参数
        System.out.print(System.getProperty("test.prop"));
    }

}

```

* * *

###### 编译、打包、执行

```ruby
# 编译
[root@cloudserver ~]# javac SystemProperty.java

# 打包 jar    -cvfe    .jar文件    主类名全路径    .class文件
[root@cloudserver ~]# jar -cfe SystemProperty.jar SystemProperty SystemProperty.class

# 执行 java   -D属性名=属性值 -jar .jar文件
[root@cloudserver ~]# java -Dtest.prop=666 -jar SystemProperty.jar
JVM Param: 666

```

* * *

* * *

* * *

* * *

* * *

* * *

###### 项目目录

```ruuby
.
└─src
   └─main
      ├─java
      │  └─com
      │      └─TestDocker
      └─resources

```

* * *

### **`打Jar包，不包含依赖`**，普通 java项目 maven 打包 pom.xml 配置

```markup
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>Test</groupId>
    <artifactId>Test</artifactId>
    <version>1.0-SNAPSHOT</version>

    <build>
        <finalName>${project.artifactId}</finalName>
        <plugins>
            <!-- 打包普通的 java 程序 -->
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-jar-plugin</artifactId>
                <version>2.4</version>
                <configuration>
                    <archive>
                        <!-- 生成的jar中，不要包含pom.xml和pom.properties这两个文件-->
                        <addMavenDescriptor>false</addMavenDescriptor>
                        <manifest>
                            <!-- 是否要把第三方jar放到manifest的classpath中-->
                            <addClasspath>true</addClasspath>
                            <!-- 生成的manifest中classpath的前缀，因为要把第三方jar放到lib目录下，所以classpath的前缀是lib/-->
                            <classpathPrefix>lib/</classpathPrefix>
                            <!-- 应用的 main class-->
                            <mainClass>com.TestDocker</mainClass>
                        </manifest>
                    </archive>
                    <!-- 过滤掉不希望包含在jar中的文件-->
                    <excludes>
                        <exclude>${project.basedir}/xml/*</exclude>
                    </excludes>
                </configuration>
            </plugin>

            <!-- 打包SpringBoot的 java 程序时多加一个 -->
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

### **`将依赖打入Jar包中`**，普通 java项目 maven 打包 pom.xml 配置

```markup
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>org.jvm.metric</groupId>
    <artifactId>jvm-metric</artifactId>
    <version>1.0-SNAPSHOT</version>

    <properties>
        <maven.compiler.source>8</maven.compiler.source>
        <maven.compiler.target>8</maven.compiler.target>
    </properties>
    <dependencies>
        <dependency>
            <groupId>io.dropwizard.metrics</groupId>
            <artifactId>metrics-core</artifactId>
            <version>3.2.6</version>
        </dependency>
    </dependencies>

    <build>
        <finalName>${project.artifactId}</finalName>
        <plugins>
            <!-- 打包普通的 java 程序 -->
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-assembly-plugin</artifactId>
                <version>3.3.0</version>
                <configuration>
                    <!-- 获取所有项目依赖项（将依赖打入Jar包中） -->
                    <descriptorRefs>
                        <descriptorRef>jar-with-dependencies</descriptorRef>
                    </descriptorRefs>
                    <archive>
                        <!-- 生成的jar中，不要包含pom.xml和pom.properties这两个文件 -->
                        <addMavenDescriptor>false</addMavenDescriptor>
                        <manifest>
                            <!-- main 方法类 -->
                            <mainClass>cn.com.TestDocker</mainClass>
                            <!-- 是否要把第三方jar放到manifest的classpath中 -->
                            <addClasspath>true</addClasspath>
                        </manifest>
                        <manifestEntries>
                            <Premain-Class>agent.GaugeAgent</Premain-Class>
                            <Agent-Class>agent.GaugeAgent</Agent-Class>
                            <Can-Redefine-Classes>true</Can-Redefine-Classes>
                            <Can-Retransform-Classes>true</Can-Retransform-Classes>
                        </manifestEntries>
                    </archive>
                </configuration>
                <executions>
                    <!-- 配置执行器 -->
                    <execution>
                        <id>make-assembly</id>
                        <!-- 绑定到package命令的生命周期上 -->
                        <phase>package</phase>
                        <goals>
                            <!-- 只运行一次 -->
                            <goal>single</goal>
                        </goals>
                    </execution>
                </executions>
            </plugin>

        </plugins>
    </build>

</project>
```

* * *

* * *

* * *

* * *

* * *

* * *
