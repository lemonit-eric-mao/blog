---
title: "Java 原生 定时器"
date: "2018-08-13"
categories: 
  - "java"
---

```java
/**
 * 测试 java 原生 定时器
 *
 * @author: mao-siyu
 * @date: 18-8-13 10:13
 * @description:
 */
public class TestTimer {
    public static void main(String[] args) {
        int corePoolSize = 1000;
        // 创建时间线程池
        ScheduledExecutorService executorService = new ScheduledThreadPoolExecutor(corePoolSize);
        // 每隔1秒触发一次
        executorService.scheduleAtFixedRate(() -> System.out.println("hello world!"), 0, 1, TimeUnit.SECONDS);
    }
}
```
