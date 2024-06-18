---
title: Node_通过Promise对象理解_Promise异步编程模式_1
date: '2017-11-16T10:58:21+00:00'
status: publish
permalink: /2017/11/16/node_%e9%80%9a%e8%bf%87promise%e5%af%b9%e8%b1%a1%e7%90%86%e8%a7%a3_promise%e5%bc%82%e6%ad%a5%e7%bc%96%e7%a8%8b%e6%a8%a1%e5%bc%8f_1
author: 毛巳煜
excerpt: ''
type: post
id: 99
category:
    - node.js
tag: []
post_format: []
hestia_layout_select:
    - default
---
```javascript
// 目标想要多个异步程序, 按照流程化执行
//
// setTimeout(function () {
//     console.log('添加任务1');
//     resolve('执行任务1成功');
//     // reject('执行任务1失败');
// }, 3000);
// setTimeout(function () {
//     console.log('添加任务2');
//     resolve('执行任务2成功');
// }, 2000);
// setTimeout(function () {
//     console.log('添加任务3');
//     resolve('执行任务3成功');
// }, 1000);


/*=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= ES6原生提供了 Promise 对象 =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=*/
/*=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= 通过Promise对象理解 Promise异步编程模式 =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=*/
/*=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=*/


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

// 执行任务
pms1().then(function (data) {
    console.log('第1个回调：' + data);
    return pms2();
}).then(function (data) {
    console.log('第2个回调：' + data);
    return pms3();
}).then(function (data) {
    console.log('第3个回调：' + data);
    return pms4();
}).then(function (data) {
    console.log(data);
});

```