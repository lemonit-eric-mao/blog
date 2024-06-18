---
title: "Java 常用工具类"
date: "2020-02-22"
categories: 
  - "java"
---

##### 计算程序耗时

```java
/**
 * 计算程序耗时
 */
public static void timeConsum(Instant start, String message) {

    Duration timeElapsed = Duration.between(start, Instant.now());
    // 获取毫秒
    long ms = timeElapsed.toMillis();
    // 毫秒转为 时-分-秒-毫秒
    // 时
    long hour = ms / 1000 / 60 / 60;
    // 分
    long min = ms / 1000 / 60 % 60;
    // 秒
    long sec = ms / 1000 % 60;
    // 毫秒
    long mi = ms % 1000;

    log.info("{}耗时: \n ---< {}小时 {}分 {}秒 {}毫秒 >---\n", message, hour, min, sec, mi);
}

```

* * *

* * *

* * *
