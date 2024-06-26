---
title: "Java 集成 无界面浏览器 在 无界面系统中 实现截图"
date: "2018-01-24"
categories: 
  - "java"
---

- **测试运行环境**
- 运行环境： jdk 1.8
- 操作系统： centOS 7
- 执行脚本命令测试： java -jar JBrowserDriverExample-v0.1.jar

### Example.java

```java
package com.lemonsoft;

import com.machinepublishers.jbrowserdriver.JBrowserDriver;
import com.machinepublishers.jbrowserdriver.Settings;
import org.apache.commons.io.FileUtils;
import org.openqa.selenium.OutputType;

import java.io.File;
import java.io.IOException;

/**
 * Java 集成 无界面浏览器(JBrowserDriver) 在 无界面系统中 实现截图功能
 *
 * Created by mao_siyu on 2018/1/23.
 */
public class Example {

    public static void main(String[] args) throws IOException {

        Settings.Builder builder = Settings.builder();
        // 这一行很关键，如果不加，在无界面系统中是不能运行的，
        // 会提示 Error: JavaFX detected no fonts! Please refer to release notes for proper font configuration
        builder.javaOptions("-Dprism.useFontConfig=false");
        //        builder.headless(true);
        //        builder.javascript(true);
        //        builder.quickRender(true);
        //        builder.timezone(Timezone.ASIA_CALCUTTA);
        //        builder.userAgent(UserAgent.CHROME);

        JBrowserDriver driver = new JBrowserDriver(builder.build());

        // You can optionally pass a Settings object here,
        // constructed using Settings.Builder
        //        JBrowserDriver driver = new JBrowserDriver(Settings.builder().timezone(Timezone.AMERICA_NEWYORK).build());

        // This will block for the page load and any
        // associated AJAX requests
        driver.get("https://www.baidu.com/");

        // You can get status code unlike other Selenium drivers.
        // It blocks for AJAX requests and page loads after clicks
        // and keyboard events.
        //        System.out.println(driver.getStatusCode());

        // Returns the page source in its current state, including
        // any DOM updates that occurred after page load
        //        System.out.println(driver.getPageSource());

        File screenShot = driver.getScreenshotAs(OutputType.FILE);
        // 将图片写到 jar包执行时所在的目录
        FileUtils.copyFile(screenShot, new File("." + File.separator + "screenShot.jpg"));

        // Close the browser. Allows this thread to terminate.
        driver.quit();
    }


}
```

### pom.xml 配置maven打jar包， 并执行main方法测试

```markup
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>headless</groupId>
    <artifactId>headless-artifact</artifactId>
    <version>1.0-SNAPSHOT</version>

    <dependencies>

        <!-- https://mvnrepository.com/artifact/com.machinepublishers/jbrowserdriver -->
        <dependency>
            <groupId>com.machinepublishers</groupId>
            <artifactId>jbrowserdriver</artifactId>
            <version>0.17.11</version>
        </dependency>

        <!-- https://mvnrepository.com/artifact/commons-io/commons-io -->
        <dependency>
            <groupId>commons-io</groupId>
            <artifactId>commons-io</artifactId>
            <version>2.6</version>
        </dependency>

    </dependencies>

    <build>
        <plugins>
            <plugin>
                <artifactId>maven-assembly-plugin</artifactId>
                <configuration>
                    <appendAssemblyId>false</appendAssemblyId>
                    <descriptorRefs>
                        <descriptorRef>jar-with-dependencies</descriptorRef>
                    </descriptorRefs>
                    <archive>
                        <manifest>
                            <!-- 主函数的入口 -->
                            <mainClass>com.lemonsoft.Example</mainClass>
                        </manifest>
                    </archive>
                    <!--自定义jar包名称-->
                    <finalName>JBrowserDriverExample-v0.1</finalName>
                </configuration>
                <executions>
                    <execution>
                        <id>make-assembly</id>
                        <phase>package</phase>
                        <goals>
                            <goal>assembly</goal>
                        </goals>
                    </execution>
                </executions>
            </plugin>
        </plugins>
    </build>

</project>
```

[下载地址](http://qiniu.dev-share.top/file/headless-example%28%E6%97%A0%E7%95%8C%E9%9D%A2%E6%B5%8F%E8%A7%88%E5%99%A8%20%E5%9C%A8%20%E6%97%A0%E7%95%8C%E9%9D%A2%E7%B3%BB%E7%BB%9F%E4%B8%AD%20%E5%AE%9E%E7%8E%B0%E6%88%AA%E5%9B%BE%29.zip "下载地址")
