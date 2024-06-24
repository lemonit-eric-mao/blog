---
title: "Java 正则 匹配 数组字符串 的 [ ] 与 空格"
date: "2018-04-13"
categories: 
  - "java"
---

##### 将 \[50, 51, 52, 53, 24353, 19978, 54, 55, 66, 70, 88, 56, 57, 58, 116, 99, 26447, 26032\] 的 \[ \] 空格去掉

```java
    public static void main(String[] args) throws Base64DecodingException {
        String str = "[50, 51, 52, 53, 24353, 19978, 54, 55, 66, 70, 88, 56, 57, 58, 116, 99, 26447, 26032]";
        str = str.replaceAll("(\\[)|(])|\\s", "");
        System.out.println(str);
    }
```
