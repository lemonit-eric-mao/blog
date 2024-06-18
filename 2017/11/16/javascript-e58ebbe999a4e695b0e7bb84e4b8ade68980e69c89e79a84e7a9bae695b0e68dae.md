---
title: 'JavaScript 去除数组中所有的空数据'
date: '2017-11-16T10:01:07+00:00'
status: publish
permalink: /2017/11/16/javascript-%e5%8e%bb%e9%99%a4%e6%95%b0%e7%bb%84%e4%b8%ad%e6%89%80%e6%9c%89%e7%9a%84%e7%a9%ba%e6%95%b0%e6%8d%ae
author: 毛巳煜
excerpt: ''
type: post
id: 35
category:
    - JavaScript
tag: []
post_format: []
hestia_layout_select:
    - default
---
### 错误的写法

```javascript
var arr = [1, 23, 4, 5, "", 345, 34, "", 5, 4, "", "", "", "", 32, "", "", "", 666];
for (var i = 0; i 
```

### 正确的写法

```javascript
var arr = [1, 23, 4, 5, "", 345, 34, "", 5, 4, "", "", "", "", 32, "", "", "", 666];
var length = arr.length;
while (length > 0) {
    var temp = arr.shift();
    if (temp)
        arr.push(temp);
    length--;
}
arr; // (10) [1, 23, 4, 5, 345, 34, 5, 4, 32, 666]

```

### 原因

`使用splice(i, 1)方法删除数组元素时, 数组长度会改变, 导致for循环时, 索引与数组的元素位置错乱.`