---
title: "ES6 编程风格-字符串"
date: "2017-11-16"
categories: 
  - "javascript"
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
