---
title: "Java 首字母转大/小写"
date: "2019-02-13"
categories: 
  - "java"
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
    if (ch[0] >= 'a' && ch[0] <= 'z') {
        ch[0] = (char) (ch[0] - 32);
    }
    return new String(ch);
}
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
    if (ch[0] >= 'A' && ch[0] <= 'Z') {
        ch[0] = (char) (ch[0] + 32);
    }
    return new String(ch);
}
```
