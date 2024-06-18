---
title: node_querystring
date: '2017-11-16T12:15:27+00:00'
status: publish
permalink: /2017/11/16/node_querystring
author: 毛巳煜
excerpt: ''
type: post
id: 141
category:
    - node.js
tag: []
post_format: []
hestia_layout_select:
    - default
---
```
<pre data-language="">```javascript
//////////////////////////===================序列化和反序列化==================////////////////////////////////
// 字符串转换 Query String模块的基本介绍
// Query String模块用于实现URL参数字符串与参数对象之间的互相转换，提供了"stringify"、"parse"等一些实用函数来针对字符串进行处理
// ，通过序列化和反序列化，来更好的应对实际开发中的条件需求，对于逻辑的处理也提供了很好的帮助，下面就让我们一起来了解学习它吧！

```
```

```
<pre data-language="">```javascript
// stringify函数的基本用法
// stringify函数的作用就是序列化对象，也就是说将对象类型转换成一个字符串类型（默认的分割符（"&"）和分配符（"="））
// ，本节先介绍它的基本用法，在下一节里我们将学习如何替换默认分配符，下面我们就通过以下例子来清楚的认识一下吧！
// 例1：querystring.stringify("对象")
// 练习 "get=fire&get=ice&want=go"，用stringify序列化怎么实现呢？
var querystring = require('querystring');
var result = querystring.stringify({
    get: ['fire', 'ice'],
    want: 'go'
});
console.log(result);

```
```

```
<pre data-language="">```javascript
// stringify函数的多参数用法
// 这节我们来学习stringify函数的多参数用法，上节我们知道了对象被序列化为字符串之后默认是通过分割符（"&"）和分配符（"="）组成的
// ，那可不可以改变呢，这节我们就来了解一下，是否可以自己去定义组合结果，看下面的小例子
// 例1：querystring.stringify("对象"，"分隔符"，"分配符")
// 练习 "spr#sum@spr#aut@aut#win" 练一练！
var result = querystring.stringify({
    spr: ['sum', 'aut'],
    aut: 'win'
}, '@', '#');
console.log(result);

```
```

```
<pre data-language="">```javascript
// parse函数的基本用法
// 刚刚我们已经学习了stringify函数的作用，接下来就来学习反序列化函数——parse函数
// ，parse函数的作用就是反序列化字符串（默认是由"="、"&"拼接而成），转换得到一个对象类型。如下示例：
// 例1：querystring.parse("字符串")
var result = querystring.parse('get=fire&get=ice&want=go');
console.log(result);

```
```

```
<pre data-language="">```javascript
// parse函数的多参数用法
// 现在我们学习parse函数的扩展用法，和上节stringify函数的多参数用法不同的是
// ，parse函数可以根据用户所自定义的分割符、分配符来反序列化字符串，从而得到相应的对象结果.如下示例：
// 例1：querystring.parse("字符串"，"分隔符"，"分配符")
var result = querystring.parse('spr#sum@spr#aut@aut#win', '@', '#');
console.log(result);

```
```