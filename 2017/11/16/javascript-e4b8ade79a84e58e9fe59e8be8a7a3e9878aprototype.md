---
title: 'JavaScript 中的原型(prototype) 用法'
date: '2017-11-16T09:58:37+00:00'
status: publish
permalink: /2017/11/16/javascript-%e4%b8%ad%e7%9a%84%e5%8e%9f%e5%9e%8b%e8%a7%a3%e9%87%8aprototype
author: 毛巳煜
excerpt: ''
type: post
id: 28
category:
    - JavaScript
tag: []
post_format: []
---
```javascript
/**
 * Created by mao_siyu on 2018/11/14.
 * JS 基于原型实现扩展
 */
String.prototype.go = function () {
    console.log('我是自定义的Go函数')
}

"".go()
// 我是自定义的Go函数

// ===================================================

/**
 * Created by mao_siyu on 2018/11/14.
 * JS 基于原型实现继承
 */
var E = function () {

    this.name = 'eName';
}

var F = function () {

    this.age = '18';
    this.sex = '女';
}

var G = function () {
    this.name = 'gName';
}

var e = new E();
var f = new F();
var g = new G();

// f对象 继承 e对象
Object.setPrototypeOf(f, e);
// g对象 继承 f对象
Object.setPrototypeOf(g, f);

console.log(f.name);
console.log(g.name);
// eName
// gName

```