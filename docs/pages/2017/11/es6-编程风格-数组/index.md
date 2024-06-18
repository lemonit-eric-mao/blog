---
title: "ES6 编程风格-数组"
date: "2017-11-16"
categories: 
  - "javascript"
---

转载: [ECMAScript 6 入门](http://es6.ruanyifeng.com/)

### 数组

使用扩展运算符（...）拷贝数组。

```javascript
// bad
const len = items.length;
const itemsCopy = [];
let i;

for (i = 0; i < len; i++) {
  itemsCopy[i] = items[i];
}

// good
const itemsCopy = [...items];
```

使用Array.from方法，将类似数组的对象转为数组。

```javascript
const foo = document.querySelectorAll('.foo');
const nodes = Array.from(foo);
```
