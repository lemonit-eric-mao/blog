---
title: 'ES6 编程风格-数组'
date: '2017-11-16T10:06:01+00:00'
status: publish
permalink: /2017/11/16/es6-%e7%bc%96%e7%a8%8b%e9%a3%8e%e6%a0%bc-%e6%95%b0%e7%bb%84
author: 毛巳煜
excerpt: ''
type: post
id: 54
category:
    - JavaScript
tag: []
post_format: []
hestia_layout_select:
    - default
---
转载: [ECMAScript 6 入门](http://es6.ruanyifeng.com/)

### 数组

使用扩展运算符（...）拷贝数组。

```javascript
// bad
const len = items.length;
const itemsCopy = [];
let i;

for (i = 0; i 
```

使用Array.from方法，将类似数组的对象转为数组。

```javascript
const foo = document.querySelectorAll('.foo');
const nodes = Array.from(foo);

```