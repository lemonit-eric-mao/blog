---
title: 'ES6 编程风格-字符串'
date: '2017-11-16T10:04:45+00:00'
status: publish
permalink: /2017/11/16/es6-%e7%bc%96%e7%a8%8b%e9%a3%8e%e6%a0%bc-%e5%ad%97%e7%ac%a6%e4%b8%b2
author: 毛巳煜
excerpt: ''
type: post
id: 48
category:
    - JavaScript
tag: []
post_format: []
hestia_layout_select:
    - default
---
转载: [ECMAScript 6 入门](http://es6.ruanyifeng.com/)

### 字符串

静态字符串一律使用单引号或反引号，不使用双引号。动态字符串使用反引号。

```javascript
// bad
const a = "foobar";
const b = 'foo' + a + 'bar';

// acceptable
const c = `foobar`;

// good
const a = 'foobar';
const b = `foo${a}bar`;
const c = 'foobar';

```