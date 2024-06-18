---
title: "Node_通过Promise对象理解_Promise异步编程模式_2"
date: "2017-11-16"
categories: 
  - "node-js"
---

#### 理解 resolve, reject

```javascript
var pms1 = function () {
    return new Promise(function (resolve, reject) {
        setTimeout(function () {
            // 生成1-10的随机数
            var num = Math.ceil(Math.random() * 10);
            if (num <= 5) {
                resolve(num);
            } else {
                reject('数字太大了吧！');
            }
        }, 2000);
    });
}

// 持续执行
setInterval(function () {
    pms1().then(function (data) {
        // resolve 函数回调
        console.log(data);
    }, function (data) {
        // reject 函数回调
        console.log(data);
    })
}, 1000);
```
