---
title: "Java 读取文件夹下所有文件"
date: "2019-03-05"
categories: 
  - "java"
---

```java
    /**
     * 读取文件夹下所有文件
     *
     * @param file
     * @return
     */
    protected void readFolderAndFile(File file) {
        if (!file.exists()) {
            return;
        }
        // 是文件夹
        if (file.isDirectory()) {
            File[] files = file.listFiles();
            for (File f : files) {
                readFolderAndFile(f);
            }
            return;
        }
        System.out.println(file.getPath());
    }
```
