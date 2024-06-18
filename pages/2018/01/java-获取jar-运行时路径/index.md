---
title: "Java 获取jar 运行时路径"
date: "2018-01-18"
categories: 
  - "java"
---

```java
package cn.lemonit.robot.runner.core.util;

import java.io.File;

/**
 * 处理文件工具类
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
    public String getCurrentPath() {

        // 获取jar 运行时路径
        String filePath = FileUtil.class.getProtectionDomain().getCodeSource().getLocation().getPath();
        return filePath;
    }

    /**
     * 创建路径 (注: 文件路径中不能有中文出现)
     *
     * @param filePath 包含文件名的全路径
     */
    public void mkdir(String filePath) {

        // 获取不包含文件名的全路径
        String parentFilePath = new File(filePath).getParent();
        // 生成新路径
        File pluginsPath = new File(parentFilePath + File.separator + "plugins");
        //
        if (!pluginsPath.exists()) {
            // 创建路径
            boolean mkdir = pluginsPath.mkdir();
            System.out.println(mkdir);
        }
    }

    /**
     * 创建内部类
     */
    private static class FileUtilChild {
        private static final FileUtil NEW_INSTANCE = new FileUtil();
    }
}
```
