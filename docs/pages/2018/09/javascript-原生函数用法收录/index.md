---
title: "Javascript  String.prototype.concat()"
date: "2018-09-06"
categories: 
  - "javascript"
---

### String.prototype.concat()

#### concat()方法将字符串参数连接到调用字符串, 并返回一个新字符串。

```javascript
var str1 = 'Hello';
var str2 = 'World';

console.log(str1.concat(...[' ', 'mao', '_', 'si', 'yu']));
// expected output: "Hello mao_siyu"

console.log(str1.concat([' ', 'mao', '_', 'si', 'yu']));
// expected output: "Hello ,mao,_,si,yu"

console.log(str2.concat(' ', str1));
// expected output: "World Hello"
```
