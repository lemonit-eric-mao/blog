---
title: Node_通过Promise对象理解_Promise异步编程模式_3_all
date: '2017-11-16T11:00:25+00:00'
status: publish
permalink: /2017/11/16/node_%e9%80%9a%e8%bf%87promise%e5%af%b9%e8%b1%a1%e7%90%86%e8%a7%a3_promise%e5%bc%82%e6%ad%a5%e7%bc%96%e7%a8%8b%e6%a8%a1%e5%bc%8f_3_all
author: 毛巳煜
excerpt: ''
type: post
id: 103
category:
    - node.js
tag: []
post_format: []
hestia_layout_select:
    - default
---
```javascript
// 声明任务
var pms1 = function () {
    return new Promise(function (resolve, reject) {
        setTimeout(function () {
            console.log('执行任务1');
            resolve('执行任务1成功');
        }, 3000);
    });
}
var pms2 = function () {
    return new Promise(function (resolve, reject) {
        setTimeout(function () {
            console.log('执行任务2');
            resolve('执行任务2成功');
        }, 2000);
    });
}
var pms3 = function () {
    return new Promise(function (resolve, reject) {
        setTimeout(function () {
            console.log('执行任务3');
            resolve('执行任务3成功');
        }, 1000);
    });
}
var pms4 = function () {
    return new Promise(function (resolve, reject) {
        setTimeout(function () {
            console.log('执行任务4');
            resolve('执行任务4成功');
        }, 2000);
    });
}

/**
 * Promise.all
 * 并发执行所有任务, 直到最后一个任务执行完成, 才会进到then里面,
 * 会把 所有异步操作的结果 放进一个数组中传给then
 */
Promise.all([pms1(), pms2(), pms3(), pms4()]).then(function (dataArray) {
    console.log(dataArray);
    // 得到一个对象的更精确的类型时, 不是用的typeof, 而是 Object.prototype.toString.call({})
    // 输出data的数据类型
    console.log('dataArray的数据类型是: ' + {}.toString.call(dataArray));
})

```