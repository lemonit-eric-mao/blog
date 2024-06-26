---
title: "通过代码来理解事件驱动思想"
date: "2022-03-03"
categories: 
  - "javascript"
---

###### 理解事件驱动思想

```javascript
// 首先做一个能存放"待执行事件"的数组队列
let queue = [];

// 然后做一个"执行数组队列中事件"的功能函数
function execEevent() {
    // 取出数组队列中的事件
    let fun = queue.shift();
    // 按顺序执行队列中的事件
    //console.log(fun)
    eval(fun);
    // 判断队列中是否还有"待执行事件"
    if(queue.length) {
        // 继续执行
        execEevent();
    }
}


// ---------------------------- 测试向队列中添加事件 ----------------------------
function start() {
    for(let i = 0; i < 5; i++) {
        queue.push(`console.log(${i})`)
    }
}
function start1() {
    for(let i = 5; i < 10; i++) {
        queue.push(`console.log(${i})`)
    }
}


// ---------------------------- 在JS中使用setTimeout()执行函数时，不同的是哪个setTimeout()先执行，而内部执行的方法仍然是按顺序执行的 ----------------------------
setTimeout(() => {
    start();
    // 触发执行事件
    execEevent();
    //console.log('start')
}, 100)
setTimeout(() => {
    start1();
    // 触发执行事件
    execEevent();
    //console.log('start1')
}, 100)

```
