---
title: "Node_通过Promise对象理解_Promise异步编程模式_5_catch"
date: "2017-11-16"
categories: 
  - "node-js"
---

```javascript
var promise1 = function () {
    return new Promise(function (resolve, reject) {
        setTimeout(function () {
            resolve('promise1----成功');
        }, 2000);
    });
};

var promise2 = function () {
    return new Promise(function (resolve, reject) {
        setTimeout(function () {
            // resolve('promise2----成功');
            reject('promise2----失败');
        }, 1000);
    });
};

// 执行任务
promise1().then(function (data) {
    console.info(data);
    return promise2();
}).then(function (data) {
    console.info(data);
}).catch(function (err) {
    console.error('出现异常 =:|=====> ' + err);
});
```
