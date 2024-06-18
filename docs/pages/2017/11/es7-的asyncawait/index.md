---
title: "ES7 的Async/Await"
date: "2017-11-16"
categories: 
  - "javascript"
---

## **ES7 的Async/Await**

```javascript
// 定义一个 Promise 对象
var sleep = function (time) {
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            console.log('sleep');
            resolve();
        }, time);
    })
};

// 定义一个异步函数
var test = async function () {
    console.log('test');
    // 在异步函数中执行 Promise对象
    await sleep(6000);
    console.log('end');
};

test();
```

async 表示这是一个async函数，await只能用在这个函数里面。 await 表示在这里等待promise返回结果了，再继续执行。 await 后面跟着的应该是一个promise对象（当然，其他返回值也没关系，只是会立即执行，不过那样就没有意义了…）

[节选自: 体验异步的终极解决方案-ES7的Async/Await](https://cnodejs.org/topic/5640b80d3a6aa72c5e0030b6)
