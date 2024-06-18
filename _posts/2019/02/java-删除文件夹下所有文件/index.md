---
title: "Java 删除文件夹下所有文件"
date: "2019-02-25"
categories: 
  - "java"
---

```java
    /**
     * 删除文件夹下所有文件
     *
     * @param file
     * @return
     */
    public boolean deleleFolderAndFile(File file) {
        if (!file.exists()) {
            return false;
        }

        if (file.isDirectory()) {
            File[] files = file.listFiles();
            for (File f : files) {
                deleleFolderAndFile(f);
            }
        }
        return file.delete();
    }
```
