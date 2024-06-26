---
title: "JavaScript 获得对象更精确的类型"
date: "2017-11-16"
categories: 
  - "javascript"
---

```javascript
// 得到一个对象的更精确的类型时, 不是用的typeof, 而是
Object.prototype.toString.call(value)
```

### 使用typeof 出现的弊端

```javascript
typeof {} === 'object' // 对的
true
typeof [] === 'object' // 对的
true
typeof null === 'object' // 这个就不对了
true
```

### 精确的使用方式

```javascript
Object.prototype.toString.call({});
"[object Object]"

Object.prototype.toString.call('');
"[object String]"

Object.prototype.toString.call(null);
"[object Null]"
```
