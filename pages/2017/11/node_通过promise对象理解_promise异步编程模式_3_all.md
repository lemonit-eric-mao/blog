---
title: "Node_通过Promise对象理解_Promise异步编程模式_3_all"
date: "2017-11-16"
categories: 
  - "node-js"
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
