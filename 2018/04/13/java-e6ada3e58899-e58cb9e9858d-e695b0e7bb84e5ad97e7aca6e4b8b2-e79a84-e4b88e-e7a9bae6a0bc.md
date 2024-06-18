---
title: 'Java 正则 匹配 数组字符串 的 [ ] 与 空格'
date: '2018-04-13T14:31:24+00:00'
status: publish
permalink: /2018/04/13/java-%e6%ad%a3%e5%88%99-%e5%8c%b9%e9%85%8d-%e6%95%b0%e7%bb%84%e5%ad%97%e7%ac%a6%e4%b8%b2-%e7%9a%84-%e4%b8%8e-%e7%a9%ba%e6%a0%bc
author: 毛巳煜
excerpt: ''
type: post
id: 2084
category:
    - Java
tag: []
post_format: []
hestia_layout_select:
    - default
---
##### 将 \[50, 51, 52, 53, 24353, 19978, 54, 55, 66, 70, 88, 56, 57, 58, 116, 99, 26447, 26032\] 的 \[ \] 空格去掉

```
<pre class="line-numbers prism-highlight" data-start="1">```java
    public static void main(String[] args) throws Base64DecodingException {
        String str = "[50, 51, 52, 53, 24353, 19978, 54, 55, 66, 70, 88, 56, 57, 58, 116, 99, 26447, 26032]";
        str = str.replaceAll("(\\[)|(])|\\s", "");
        System.out.println(str);
    }

```
```