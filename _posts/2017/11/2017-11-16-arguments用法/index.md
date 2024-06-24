---
title: "JavaScript arguments用法"
date: "2017-11-16"
categories: 
  - "javascript"
---

[JavaScript 指南](https://developer.mozilla.org/zh-CN/docs/Web/Javascript/Guide "JavaScript 指南")

```javascript
/**
 * 讲解 arguments 用法
 * arguments 是指当前这个函数的参数
 * arguments.length 是指当前这个函数的参数的个数
 * arguments.callee 是指当前这个函数
 * arguments.Symbol 不知道是干什么的
 *
 * Created by mao_siyu on 2017/1/9.
 */
var fun = function () {
    // 输出结果 ["mao", "siyu", 1987, callee: function, Symbol(Symbol.iterator): function]
    console.log(arguments);
    // 输出结果 3
    console.log(arguments.length);
    // 输出结果 是当前这个函数
    console.log(arguments.callee);
}

// 执行上面的函数
fun('mao', 'siyu', 1987);
```
