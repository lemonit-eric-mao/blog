---
title: "Java8 常用日期种类封装"
date: "2018-09-12"
categories: 
  - "java"
---

#### 常用日期种类

```java
/**
     * 获取本月第一天
     *
     * @return
     */
    public static LocalDate getFirstDayOfMonth() {

        LocalDate firstDayOfMonth = LocalDate.now().with(TemporalAdjusters.firstDayOfMonth());
        return firstDayOfMonth;
    }

    /**
     * 获取上个月第一天
     *
     * @return
     */
    public static LocalDate getFirstDayOfLastMonth() {

        LocalDate firstDayOfMonth = LocalDate.now().with(TemporalAdjusters.firstDayOfMonth());
        return firstDayOfMonth.minusMonths(1);
    }

    /**
     * 获取上个月的今天
     *
     * @return
     */
    public static LocalDate getLastMonthToday() {

        return LocalDate.now().minusMonths(1);
    }

    /**
     * 获取当前年月
     *
     * @return
     */
    public static String getYearMonth() {

        return DateTimeFormatter.ofPattern("YYYY-MM").format(LocalDate.now());
    }

    /**
     * 获取今天
     *
     * @return
     */
    public static LocalDate getToday() {

        return LocalDate.now();
    }
```
