---
title: "JavaScript 高阶函数"
date: "2017-11-16"
categories: 
  - "javascript"
---

##### 什么是高阶函数

**`可以返回其它函数的函数，和接受其它函数作为参数的函数`，均被称之为高阶函数，是函数式语言的特点。**

```javascript
/**
 * Created by mao_siyu on 2018/11/14.
 * 高阶函数则是可以把函数作为参数，或是把函数作为返回值的函数
 */
function show(param) {
    console.log('---------------show------------')
    console.log(param)
}

/**
 * 把函数作为参数
 * @param callback
 */
function main(callback) {
    // 判断参数是否是 一个函数
    let bol = Object.prototype.toString.call(callback) === '[object Function]';
    // 如果不是函数 就抛出异常
    if (!bol) {
        throw '要求参数必须是一个函数！';
    }
    // 如果是函数 就执行这个函数
    callback('############--main--############');
}

main(show);

// ---------------show------------
// ############--main--############

// ==========================================================================

/**
 * 把函数作为返回值
 * @returns {Function}
 */
function main() {
    // 返回一个可以计算加法的匿名函数
    return function (a, b) {
        return a + b;
    }
}
// 把 计算加法的匿名函数， 赋给 add变量
let add = main();
// 执行计算加法的匿名函数
add(1, 2);
// 3
```
