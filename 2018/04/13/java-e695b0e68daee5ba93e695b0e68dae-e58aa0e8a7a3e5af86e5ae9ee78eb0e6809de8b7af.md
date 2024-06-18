---
title: 'Java 数据库数据 加解密实现思路'
date: '2018-04-13T15:05:51+00:00'
status: publish
permalink: /2018/04/13/java-%e6%95%b0%e6%8d%ae%e5%ba%93%e6%95%b0%e6%8d%ae-%e5%8a%a0%e8%a7%a3%e5%af%86%e5%ae%9e%e7%8e%b0%e6%80%9d%e8%b7%af
author: 毛巳煜
excerpt: ''
type: post
id: 2086
category:
    - Java
tag: []
post_format: []
hestia_layout_select:
    - default
---
#### 数据库数据 加解密

```
<pre class="line-numbers prism-highlight" data-start="1">```java
package com.my.springboot.common.crypto;

import java.util.ArrayList;
import java.util.List;

/**
 * 数据库数据 加解密
 *
 * @author mao-siyu
 * @date 2018-04-13
 */
public class DataBaseEncrypAndDecryp {

    /**
     * 写下思路
     *
     * @param args
     */
    public static void main(String[] args) {

        // 数据明文
        String str = "1234张三56AEW789sb李斯";
        // 数据加密： 将明文转为10进制uncoide 然后修改每一位的数值
        String unicode = stringToUnicode(str);
        System.out.println(unicode);
        // 数据解密
        String strs = unicodeToString(unicode);
        System.out.println(strs);
        // 以这种方式处理的进行加密的数据，还可以支持模糊查询
        // 模糊查询 用法 最后在将查询的结果进行对应的解密
        StringBuilder sql = new StringBuilder();
        sql.append("SELECT                  ");
        sql.append("  *                     ");
        sql.append("FROM                    ");
        sql.append("  users                 ");
        sql.append("WHERE                   ");
        sql.append("  users.u_backup LIKE   ");
        sql.append("'%" + stringToUnicode("张三") + "%';");
        System.out.println(sql);
    }

    /**
     * 字符串 转 unicode
     * 将串改后的数值保存到数据库中
     *
     * @param str
     * @return
     */
    public static String stringToUnicode(String str) {

        List<integer> list = new ArrayList();

        char[] charArray = str.toCharArray();
        for (int i = 0; i </integer>
```
```