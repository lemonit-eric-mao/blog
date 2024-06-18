---
title: 'JavaScript 偏函数'
date: '2017-11-16T09:56:15+00:00'
status: publish
permalink: /2017/11/16/javascript-%e9%ab%98%e9%98%b6%e5%87%bd%e6%95%b0
author: 毛巳煜
excerpt: ''
type: post
id: 25
category:
    - JavaScript
tag: []
post_format: []
---
```javascript
/**
 * Created by mao_siyu on 2018/11/13.
 */

// 需求： 封装判断类型的工具方法
var toString = Object.prototype.toString;

var isNumber = function (obj) {
    return toString.call(obj) == '[object Number]';
}
var isString = function (obj) {
    return toString.call(obj) == '[object String]';
}
var isFunction = function (obj) {
    return toString.call(obj) == '[object Function]';
}

// =====================================================================

// 使用Object.prototype上的原生toString()方法判断数据类型
// Object.prototype.toString.call(value)
// 判断基本类型
var toString = Object.prototype.toString;

// 精简代码， 含义是通过一个函数，又构建了多个函数对象
// 当使用者调用这个 isType函数的时候，返回的是一个匿名函数，这个匿名函数并没有执行
var isType = function (type) {
    // 返回一个 匿名function
    return function (obj) {
        return toString.call(obj) == '[object ' + type + ']';
    };
};

// 当执行 isType 函数的时候，是把 匿名function 赋给了 isString变量
var isString = isType('String');
var isFunction = isType('Function');

var param = 666;
// 在这里才执行了 匿名function
console.log(isString(param));
console.log(isFunction(param));
console.log(toString.call(param));

```