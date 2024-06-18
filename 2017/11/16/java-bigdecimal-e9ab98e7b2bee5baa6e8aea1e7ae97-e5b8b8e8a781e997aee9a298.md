---
title: 'Java BigDecimal  高精度计算 常见问题'
date: '2017-11-16T13:05:32+00:00'
status: publish
permalink: /2017/11/16/java-bigdecimal-%e9%ab%98%e7%b2%be%e5%ba%a6%e8%ae%a1%e7%ae%97-%e5%b8%b8%e8%a7%81%e9%97%ae%e9%a2%98
author: 毛巳煜
excerpt: ''
type: post
id: 250
category:
    - Java
tag: []
post_format: []
---
```
<pre class="line-numbers prism-highlight" data-start="1">```java
public static void main(String[] args) {

    // 输入 double 0.4
    // new BigDecimal(0.40) = 0.40000000000000002220446049250313080847263336181640625
    BigDecimal a_decimal = new BigDecimal(0.40).setScale(1, RoundingMode.CEILING);

    // 输入 double 0.5
    // new BigDecimal(0.50) = 0.5
    BigDecimal a_decimal1 = new BigDecimal(0.50).setScale(1, RoundingMode.CEILING);

    // 输入 double 0.6
    //new BigDecimal(0.60) = 0.59999999999999997779553950749686919152736663818359375
    BigDecimal a_decimal2 = new BigDecimal(0.60).setScale(1, RoundingMode.CEILING);

    // 打印结果
    System.out.println("format 第一种：\n" + a_decimal +"\n"+ a_decimal1 +"\n"+ a_decimal2);


    // 输入 字符串 0.4
    // new BigDecimal("0.40") = 0.40
    BigDecimal b_decimal = new BigDecimal("0.40").setScale(1, RoundingMode.CEILING);

    // 输入 字符串 0.5
    // new BigDecimal("0.50") = 0.50
    BigDecimal b_decimal1 = new BigDecimal("0.50").setScale(1, RoundingMode.CEILING);

    // 输入 字符串 0.6
    // new BigDecimal("0.60") = 0.60
    BigDecimal b_decimal2 = new BigDecimal("0.60").setScale(1, RoundingMode.CEILING);

    // 打印结果
    System.out.println("format 第二种：\n" + b_decimal +"\n"+ b_decimal1 +"\n"+ b_decimal2);
}

```
```