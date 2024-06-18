---
title: 'Java 常用工具类'
date: '2020-02-22T14:21:21+00:00'
status: publish
permalink: /2020/02/22/java-%e5%b8%b8%e7%94%a8%e5%b7%a5%e5%85%b7%e7%b1%bb
author: 毛巳煜
excerpt: ''
type: post
id: 5265
category:
    - Java
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
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

    log.info("{}耗时: \n ------\n", message, hour, min, sec, mi);
}


```

- - - - - -

- - - - - -

- - - - - -