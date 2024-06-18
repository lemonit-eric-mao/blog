---
title: "Java 获取所有jar包中的 config.json文件"
date: "2018-01-18"
categories: 
  - "java"
---

### Test.jar中的config.json

```json
{
  "mainClass": "cn.lemonit.robot.plugin.datasource.mysql.Main",
  "author": "LemonRobot官方"
}
```

### 获取jar包中的 config.json 为例

```java
package cn.lemonit.robot.runner.core.util;

import com.google.gson.Gson;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.jar.JarEntry;
import java.util.jar.JarFile;

public class Example {


    public Example() throws IOException {
        initGetJarConfigJson();
    }

    /**
     * 获取jar包中的 config.json文件
     *
     * @throws IOException
     */
    private void initGetJarConfigJson() throws IOException {

        // 使用 JarFile获取Jar包文件
        JarFile jarFile = new JarFile("/home/lemon-robot-runner-core/target/plugins/Test.jar");

        // 获取 jar包中的 config.json文件
        JarEntry entry = jarFile.getJarEntry("config.json");
        // 获取流文件
        InputStream inputStream = jarFile.getInputStream(entry);

        // 解析文件
        InputStreamReader isr = new InputStreamReader(inputStream);
        BufferedReader reader = new BufferedReader(isr);
        String line;
        StringBuilder sBuilder = new StringBuilder();
        while ((line = reader.readLine()) != null) {
            sBuilder.append(line);
        }

        System.out.println("config.json 文件内容    " + sBuilder.toString());

        reader.close();
        jarFile.close();
    }


    public static void main(String[] args) throws IOException {

        Example pm = new Example();
        pm.initGetJarConfigJson();
    }
}
```
