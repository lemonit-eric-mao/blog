---
title: 设计模式：单例
date: '2017-11-16T13:32:34+00:00'
status: publish
permalink: /2017/11/16/%e8%ae%be%e8%ae%a1%e6%a8%a1%e5%bc%8f%ef%bc%9a%e5%8d%95%e4%be%8b
author: 毛巳煜
excerpt: ''
type: post
id: 298
category:
    - Java
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
**懒汉式写法**
---------

### **不调用不初始化，一但调用就只初始化一次。**

```
<pre class="line-numbers prism-highlight" data-start="1">```java
package bigdata.common.utils;

/**
 * Created by mao_siyu on 2017/10/24.
 */
public class Example {

    /**
     * 私有构造方法
     */
    private Example() {
    }

    /**
     * 创建静态内部类
     */
    private static class ExampleChild {
        // 放心这里只初始化一次, 因为是静态的不会在次创建对象了
        private static final Example newInstance = new Example();
    }

    /**
     * 提供公有访问函数
     *
     * @return Example
     */
    public static Example getInstance() {
        // 调用内部类 进行初始化对象操作
        return ExampleChild.newInstance;
    }

    /**
     * 测试
     *
     * @param args
     */
    public static void main(String[] args) {
        // 循环测试对象内存地址
        for (int i = 0; i 
```
```

懒汉式 有参构造写法
----------

```
<pre class="line-numbers prism-highlight" data-start="1">```java
package bigdata.common.utils;

/**
 * Created by mao_siyu on 2017/10/24.
 */
public class Example {

    /**
     * 私有构造方法
     */
    private Example(String str) {
        System.out.println(str);
    }

    /**
     * 创建内部类
     */
    private static class ExampleChild {
        // 放心这里只初始化一次, 因为是静态的不会在次创建对象了
        private static final Example newInstance = new Example("testInfo");
    }

    /**
     * 提供公有访问函数
     *
     * @return Example
     */
    public static Example getInstance() {
        // 调用内部类 进行初始化对象操作
        return ExampleChild.newInstance;
    }

    /**
     * 测试
     *
     * @param args
     */
    public static void main(String[] args) {
        // 循环测试对象内存地址
        for (int i = 0; i 
```
```

饿汉式
---

### **不管调不调用都直接初始化！**

```
<pre class="line-numbers prism-highlight" data-start="1">```java
package bigdata.common.utils;

/**
 * Created by mao_siyu on 2017/10/24.
 */
public class Example {

    /**
     * 程序启动时就加载创建对象
     */
    private static final Example newInstance = new Example();

    /**
     * 私有构造方法
     */
    private Example() {
    }

    /**
     * 提供公有访问函数
     *
     * @return Example
     */
    public static Example getInstance() {
        return newInstance;
    }

    /**
     * 测试
     *
     * @param args
     */
    public static void main(String[] args) {
        // 循环测试对象内存地址
        for (int i = 0; i 
```
```