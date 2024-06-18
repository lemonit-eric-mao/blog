---
title: 'Object.create(null) 和 {} 区别是什么'
date: '2018-08-14T10:03:11+00:00'
status: publish
permalink: /2018/08/14/object-createnull-%e5%92%8c-%e5%8c%ba%e5%88%ab%e6%98%af%e4%bb%80%e4%b9%88
author: 毛巳煜
excerpt: ''
type: post
id: 2271
category:
    - JavaScript
tag: []
post_format: []
hestia_layout_select:
    - default
---
```javascript
// 在Object的原型链上添加一个新的对象
console.log(Object.create({}));
VM104:1 {}__proto__: Object

// 没有继承任何原型方法, 可以理解为顶级对象
console.log(Object.create(null));
VM104:2 {}No properties


```