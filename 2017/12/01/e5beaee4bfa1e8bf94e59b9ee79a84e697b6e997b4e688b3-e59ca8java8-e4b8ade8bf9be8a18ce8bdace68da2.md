---
title: '微信返回的时间戳 在JAVA8 中进行转换'
date: '2017-12-01T13:07:57+00:00'
status: publish
permalink: /2017/12/01/%e5%be%ae%e4%bf%a1%e8%bf%94%e5%9b%9e%e7%9a%84%e6%97%b6%e9%97%b4%e6%88%b3-%e5%9c%a8java8-%e4%b8%ad%e8%bf%9b%e8%a1%8c%e8%bd%ac%e6%8d%a2
author: 毛巳煜
excerpt: ''
type: post
id: 1702
category:
    - 移动端
tag: []
post_format: []
---
```
<pre class="line-numbers prism-highlight" data-start="1">```java
<br></br>    /**
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
```