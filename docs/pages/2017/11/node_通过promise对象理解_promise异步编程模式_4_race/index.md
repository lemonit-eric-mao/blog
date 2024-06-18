---
title: "Node_通过Promise对象理解_Promise异步编程模式_4_race"
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
 * Promise.race
 * race 赛跑 故名思义,看谁跑的快
 * then只返回第一个执行完成的任务, 其它的任务会继续执行,但不会返回给then
 */
Promise.race([pms1(), pms2(), pms3(), pms4()]).then(function (dataArray) {
    console.log(dataArray);
    // 输出data的数据类型
    console.log('dataArray的数据类型是: ' + {}.toString.call(dataArray));
})
```
