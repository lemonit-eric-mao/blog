---
title: "微信返回的时间戳 在JAVA8 中进行转换"
date: "2017-12-01"
categories: 
  - "移动端"
---

```java
    /**
     * 微信时间戳 转 yyyy-MM-dd HH:mm:ss
     *
     * @param param
     * @return
     */
    public static String getWXTimestamp(String param) {
        Instant timestamp = Instant.ofEpochMilli(new Long(param) * 1000);
        LocalDateTime localDateTime = LocalDateTime.ofInstant(timestamp, ZoneId.systemDefault());
        String format = localDateTime.format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss"));
        return format;
    }

    public static void main(String[] args) {
        String str = LocalDateUtil.getWXTimestamp("1511524000");
        System.out.println(str);
    }
```
