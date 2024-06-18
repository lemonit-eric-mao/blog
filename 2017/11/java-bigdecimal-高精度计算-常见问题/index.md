---
title: "Java BigDecimal  高精度计算 常见问题"
date: "2017-11-16"
categories: 
  - "java"
---

```java
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
