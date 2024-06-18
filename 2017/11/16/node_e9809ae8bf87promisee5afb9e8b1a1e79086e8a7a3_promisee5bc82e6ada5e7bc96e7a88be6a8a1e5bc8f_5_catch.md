---
title: Node_通过Promise对象理解_Promise异步编程模式_5_catch
date: '2017-11-16T11:01:10+00:00'
status: publish
permalink: /2017/11/16/node_%e9%80%9a%e8%bf%87promise%e5%af%b9%e8%b1%a1%e7%90%86%e8%a7%a3_promise%e5%bc%82%e6%ad%a5%e7%bc%96%e7%a8%8b%e6%a8%a1%e5%bc%8f_5_catch
author: 毛巳煜
excerpt: ''
type: post
id: 107
category:
    - node.js
tag: []
post_format: []
hestia_layout_select:
    - default
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