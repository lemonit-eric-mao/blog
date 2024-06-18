---
title: 'ES6 编程风格-Map结构'
date: '2017-11-16T10:06:50+00:00'
status: publish
permalink: /2017/11/16/es6-%e7%bc%96%e7%a8%8b%e9%a3%8e%e6%a0%bc-map%e7%bb%93%e6%9e%84
author: 毛巳煜
excerpt: ''
type: post
id: 58
category:
    - JavaScript
tag: []
post_format: []
hestia_layout_select:
    - default
---
转载: [ECMAScript 6 入门](http://es6.ruanyifeng.com/)

### Map结构

注意区分Object和Map，只有模拟现实世界的实体对象时，才使用Object。如果只是需要key: value的数据结构，使用Map结构。因为Map有内建的遍历机制。

```javascript
let map = new Map(arr);

for (let key of map.keys()) {
  console.log(key);
}

for (let value of map.values()) {
  console.log(value);
}

for (let item of map.entries()) {
  console.log(item[0], item[1]);
}

```