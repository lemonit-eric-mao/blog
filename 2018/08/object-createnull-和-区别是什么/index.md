---
title: "Object.create(null) 和 {} 区别是什么"
date: "2018-08-14"
categories: 
  - "javascript"
---

```javascript
// 在Object的原型链上添加一个新的对象
console.log(Object.create({}));
VM104:1 {}__proto__: Object

// 没有继承任何原型方法, 可以理解为顶级对象
console.log(Object.create(null));
VM104:2 {}No properties

```
