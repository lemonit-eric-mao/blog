---
title: "JavaScript ES6 合并对象"
date: "2017-11-16"
categories: 
  - "javascript"
---

```javascript
/**
 * ES6 新语法Object.assign(...); 合并对象
 * Created by mao-siyu on 17-6-8.
 */

// 合并两个或多个对象
var obj1 = {name: 'mao_siyu', age: 30};
var obj2 = {height: 178, sex: '男'};
Object.assign(obj1, obj2);
// 输出: Object {name: "mao_siyu", age: 30, height: 178, sex: "男"}

// 如果有相同的值, 后边的会替换前面的值
var obj1 = {name: 'mao_siyu', age: 30};
var obj2 = {height: 178, sex: '男'};
var obj3 = {age: 16, name: 'maomao'};
Object.assign(obj2, obj1, obj3);
// 输出: Object {height: 178, sex: "男", name: "maomao", age: 16}
```
