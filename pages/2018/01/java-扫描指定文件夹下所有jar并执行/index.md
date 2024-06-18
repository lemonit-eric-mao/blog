---
title: "Java 扫描指定文件夹下所有jar并执行"
date: "2018-01-18"
categories: 
  - "java"
---

#### 运行环境: jdk 1.8

#### 开发工具: idea 2017.2

#### 构建方式: maven

* * *

* * *

* * *

##### 需求分析:

###### 新一个项目, 在不同的包下创建两个类用来测试, 分别为 DemoA.java 与 DemoB.java

##### DemoA.java

```java
package com.lemonsoft;

public class DemoA {
    public String show() {
        return "DemoA-show-456456";
    }
}
```

##### DemoB.java

```java
package com.abcd;

public class DemoB {
    public String show() {
        return "DemoB-show-abcd";
    }
}
```

##### 将项目用 maven打成jar包, 分别为 DemoA.jar, DemoB.jar 备用

##### jar包项目结构

```null
DemoA.jar
.
├── Demo.iml
├── pom.xml
└── src
    └── main
        ├── java
        │   └── com
        │       └── lemonsoft
        │           └── DemoA.java
        └── resources
```

```null
DemoB.jar
.
├── Demo.iml
├── pom.xml
└── src
    └── main
        ├── java
        │   └── com
        │       └── abcd
        │           └── DemoB.java
        └── resources

```

* * *

* * *

* * *

## 新创建一个测试的项目

### 处理文件工具类 FileUtil.java

```java
package cn.lemonit.robot.runner.core.util;

import java.io.File;

/**
 * 处理文件工具类 单例: 懒汉式
 *
 * @author mao-siyu
 */
public class FileUtil {

    private FileUtil() {
    }

    /**
     * 提供公有访问函数
     *
     * @return Example
     */
    public static FileUtil getInstance() {
        return FileUtilChild.NEW_INSTANCE;
    }

    /**
     * 获取当前包含文件名的全路径
     *
     * @return
     */
    public String getCurrentFullPath() {

        // 获取jar 运行时所在路径
        String filePath = FileUtil.class.getProtectionDomain().getCodeSource().getLocation().getPath();
        return filePath;
    }

    /**
     * 获取当前不包含文件名的全路径
     *
     * @return
     */
    public String getCurrentPath() {

        // 获取jar 运行时所在路径
        String filePath = new File(getCurrentFullPath()).getParent();
        return filePath;
    }

    /**
     * 创建路径 (注: 文件路径中不能有中文出现)
     *
     * @param newPath 文件路径
     * @return 返回路径
     */
    public String mkdir(String newPath) {

        // 生成新路径
        File file = new File(newPath);
        // 创建路径
        boolean mkdir = file.mkdir();
        // 创建路径 成功
        if (mkdir) {
            // 直接返回路径
            return newPath;
        } else {
            return null;
        }
    }

    /**
     * 获取路径 (注: 文件路径中不能有中文出现)
     *
     * @param filePath 文件路径
     * @param dirName  文件夹名
     * @return newPath
     */
    public String getDIR(String filePath, String dirName) {

        // 拼接新路径
        String newPath = filePath + File.separator + dirName;
        // 生成新路径
        File file = new File(newPath);
        // 如果文件路径已经存在
        if (file.exists()) {
            // 直接返回路径
            return newPath;
        }

        // 如果文件路径不存在 则创建路径
        return mkdir(newPath);
    }

    /**
     * 创建内部类
     */
    private static class FileUtilChild {
        private static final FileUtil NEW_INSTANCE = new FileUtil();
    }
}
```

### PluginsManagerImpl.java

```java
package cn.lemonit.robot.runner.core.interfaces.impl;

import cn.lemonit.robot.runner.core.interfaces.PluginsManager;
import cn.lemonit.robot.runner.core.util.FileUtil;

import java.io.File;
import java.net.MalformedURLException;
import java.net.URL;
import java.net.URLClassLoader;
import java.util.ArrayList;
import java.util.List;

/**
 * 插件管理器实现类
 *
 * @author mao-siyu
 */
public class PluginsManagerImpl {

    /**
     * 获取工具类
     */
    private FileUtil fileUtil = FileUtil.getInstance();

    /**
     * 插件文件夹名称
     */
    private final String DIR_NAME = "plugins";

    /**
     * 文件路径前缀
     */
    private final String PROTOCOL = "file:";

    /**
     * 承载所有插件
     */
    private URLClassLoader urlLoader;


    public PluginsManagerImpl() throws MalformedURLException {
        scanPlugins();
    }

    /**
     * 扫描 plugins 文件下所有插件
     *
     * @return
     * @throws MalformedURLException
     */
    public void scanPlugins() throws MalformedURLException {

        List<URL> urls = new ArrayList<URL>();

        // 获取当前路径
        String currentPath = fileUtil.getCurrentPath();
        // 创建plugins文件夹
        String newPath = fileUtil.getDIR(currentPath, DIR_NAME);

        File file = new File(newPath);
        // 获取所有文件和文件夹
        File[] fileList = file.listFiles();

        // 获取所有插件路径
        for (int i = 0; null != fileList && i < fileList.length; i++) {
            urls.add(new URL(PROTOCOL + fileList[i].getPath()));
        }

        // 将所有插件加载到 URLClassLoader
        urlLoader = new URLClassLoader(urls.toArray(new URL[urls.size()]));
    }

    /**
     * 获取插件对象
     *
     * @param className
     * @return
     * @throws MalformedURLException
     * @throws ClassNotFoundException
     */
    public Class<?> getPluginClass(String className) throws MalformedURLException, ClassNotFoundException {

        // 动态获取类对象
        Class<?> clazz = urlLoader.loadClass(className);
        return clazz;
    }
}
```

### 运行时项目结构 lemon-robot-runner-core.java

```null
target
    ├── classes
    │   └── cn
    │       └── lemonit
    │           └── robot
    │               └── runner
    │                   └── core
    │                       ├── InitProject.class
    │                       ├── interfaces
    │                       │   ├── impl
    │                       │   │   └── PluginsManagerImpl.class
    │                       │   └── PluginsManager.class
    │                       └── util
    │                           ├── FileUtil$1.class
    │                           ├── FileUtil.class
    │                           └── FileUtil$FileUtilChild.class
    ├── generated-sources
    │   └── annotations
    └── plugins
        ├── DemoA.jar
        └── DemoB.jar
```

###### 执行这个类 将会找到项目运行时 根目录下的 plugins文件夹, 如果没有它会自己创建一个, 然后将 DomeA.jar, DemoB.jar 分别放到这个文件夹下.

###### 运行 main方法测试

```java
    public static void main(String[] args) throws MalformedURLException, ClassNotFoundException, NoSuchMethodException, IllegalAccessException, InstantiationException, InvocationTargetException {
        PluginsManager pm = new PluginsManagerImpl();
        Class<?> clazz = pm.getPluginClass("com.lemonsoft.DemoA");
        // Class<?> clazz = pm.getPluginClass("com.abcd.DemoB");
        // 动态获取方法
        Method show = clazz.getDeclaredMethod("show");
        // 执行方法
        Object result = show.invoke(clazz.newInstance());
        // output
        System.out.println(result);
    }
```
