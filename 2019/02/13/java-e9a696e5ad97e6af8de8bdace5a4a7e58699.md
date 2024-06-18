---
title: 'Java 首字母转大/小写'
date: '2019-02-13T07:34:37+00:00'
status: private
permalink: /2019/02/13/java-%e9%a6%96%e5%ad%97%e6%af%8d%e8%bd%ac%e5%a4%a7%e5%86%99
author: 毛巳煜
excerpt: ''
type: post
id: 3438
category:
    - Java
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
##### 使用反射时经常用到

```java
/**
 * 首字母转大写
 *
 * @param str
 * @return
 */
private String upperCase(String str) {
    char[] ch = str.toCharArray();
    if (ch[0] >= 'a' && ch[0] 
```

```java
/**
 * 首字母转小写
 *
 * @param str
 * @return
 */
protected static String lowerCase(String str) {
    char[] ch = str.toCharArray();
    if (ch[0] >= 'A' && ch[0] 
```