---
title: '图解 java 多线程 工作流程'
date: '2017-11-16T13:26:00+00:00'
status: publish
permalink: /2017/11/16/%e5%9b%be%e8%a7%a3-java-%e5%a4%9a%e7%ba%bf%e7%a8%8b-%e5%b7%a5%e4%bd%9c%e6%b5%81%e7%a8%8b
author: 毛巳煜
excerpt: ''
type: post
id: 276
category:
    - Java
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
### **单线程**

![](http://qiniu.dev-share.top/image/danxiancheng.png)

### **多线程**

![](http://qiniu.dev-share.top/image/multread.png)

**示例代码如下:**

```
<pre class="line-numbers prism-highlight" data-start="1">```java
package itfactor;

public class Test {

    static int index = 0;

    public static void main(String[] args) {
        // 上图以 3个线程为例, 这里为了测试效果明显, 启用 1000个线程.
        for (int i = 0; i 
```
```

**第二种写法**

```
<pre class="line-numbers prism-highlight" data-start="1">```java
package itfactor;

public class Test {

    public static void main(String[] args) {

        int index = 0;

        for (int i = 0; i 
```
```

**便于理解 提个问: 如下代码 结果是什么?, 根据下面的注释说出两个结果**

```
<pre class="line-numbers prism-highlight" data-start="1">```java
package itfactor;

public class Test {

    public static void main(String[] args) {

        final StringBuffer stringBuffer = new StringBuffer();

        for (int i = 0; i 
```
```

### **synchronized**

![](http://qiniu.dev-share.top/image/synchronized.png)

答案: (1) length等于1000; (2) length等于3000;