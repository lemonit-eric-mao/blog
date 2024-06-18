---
title: "Java 数据库数据 加解密实现思路"
date: "2018-04-13"
categories: 
  - "java"
---

#### 数据库数据 加解密

```java
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

        List<Integer> list = new ArrayList<>();

        char[] charArray = str.toCharArray();
        for (int i = 0; i < charArray.length; i++) {
            // 将 char 转成 16进制uncoide
            String uncoide16 = Integer.toHexString(charArray[i]);
            // 将 uncoide16 转成 10进制uncoide
            int uncoide10 = Integer.parseInt(uncoide16, 16);
            // 加密处理（串改数值）
            list.add(uncoide10 + 666);
        }
        return list.toString().replaceAll("(\\[)|(])|\\s", "");
    }

    /**
     * unicode 转 字符串
     * 必须要知道数值是如何串改的, 不然无法解密
     *
     * @param unicode
     * @return
     */
    public static String unicodeToString(String unicode) {

        String[] unicodeArray = unicode.split(",");
        StringBuilder sBuilder = new StringBuilder();
        for (int i = 1; i < unicodeArray.length; i++) {
            // 解密处理（串改数值）
            int temp = Integer.parseInt(unicodeArray[i]) - 666;
            sBuilder.append((char) Integer.parseInt(String.valueOf(temp), 10));
        }
        return sBuilder.toString();
    }

}
```
