---
title: 'JVM 内存益出-实践'
date: '2020-03-10T06:54:12+00:00'
status: publish
permalink: /2020/03/10/jvm-%e5%86%85%e5%ad%98%e7%9b%8a%e5%87%ba-%e5%ae%9e%e8%b7%b5
author: 毛巳煜
excerpt: ''
type: post
id: 5280
category:
    - Java
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
##### 内存泄漏 与 内存溢出的区别

- 早上公司上班突然想上个厕所，厕所一共就`6个位置`(内存总大小)， 一下子进来了`10个人`， 溢出了`4个人`，这就是 **`内存溢出`**
- 早上公司上班突然想上个厕所，厕所一共就`6个位置`(内存总大小)， 先来了`4个人`， 垃完出去以后把门给反锁了，本来可以`6个人`一起用， 现在占着`4个`茅坑不拉屎， 导致厕所爆满， 这就是 **`内存溢出`**

- - - - - -

##### GC overhead limit exceeded **`俗称内存泄露`**

`Caused by: java.lang.OutOfMemoryError: GC overhead limit exceeded`  
**引发原因**：  
jvm gc行为中`超过98%`以上的时间去释`放小于2%`的堆空间时会报这个错误。  
 由于JVM参数`-XX:+/-UseGCOverheadLimit` 可以关闭这个异常监控，网上大部分解决方案是关闭这个功能，不过我个人是非常的不建议关闭它，因为要解决问题的根本，而不是表面

**[具体查看参数作用](http://www.dev-share.top/2020/03/10/jvm-%E5%8F%82%E6%95%B0/ "具体查看参数作用")**

**[知呼解释](https://zhuanlan.zhihu.com/p/88956975 "知呼解释")**

- - - - - -

- - - - - -

- - - - - -