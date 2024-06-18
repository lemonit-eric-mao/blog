---
title: 'JavaScript 计算不重复随机数 192~45'
date: '2017-12-05T16:42:06+00:00'
status: publish
permalink: /2017/12/05/javascript-%e8%ae%a1%e7%ae%97%e4%b8%8d%e9%87%8d%e5%a4%8d%e9%9a%8f%e6%9c%ba%e6%95%b0-19245
author: 毛巳煜
excerpt: ''
type: post
id: 1711
category:
    - JavaScript
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
##### 需求: 有192条数据, 随机从里面取出45条不重复的数据, 保存到另一个数组当中

##### 请写出最优的算法.

```
<pre class="line-numbers prism-highlight" data-start="1">```javascript
/**
 * 需求: 有192条数据, 随机从里面取出45条不重复的数据, 保存到另一个数组当中
 * 解答: 请写出最优的算法.
 * Created by mao-siyu on 17-12-5.
 */

// 先将192条数据平均分
// step 1 取余(结果是 12)
let s1 = 192 % 45;

// step 2 均分 并获取每段长度(结果是 4)
let s2 = (192 - s1) / 45;

// step 3 循环45次 从192条数据中随机获取数据(也就是在192这个范围内, 循环出45个不重复的随机数.)
// 但这样只能取得 范围是 180 的平均结果(还差 12)
for (let i = 0; i 
```
```