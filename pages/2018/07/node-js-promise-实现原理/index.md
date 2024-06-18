---
title: "Node.js 学习实现 Promise 第一阶段 实现思路"
date: "2018-07-05"
categories: 
  - "node-js"
---

### 学习实现 Promise 第一阶段 实现思路

```javascript
/**
 * 学习实现 Promise 第一阶段 实现思路
 * @param resolver
 * @constructor
 */
class CustomPromise {

    constructor(callback) {
        // pending 等待时 默认
        // fulfilled 被允许时 执行
        // rejected 被拒绝时 执行
        this.states = 'pending';
        // 返回值 表明Promise被允许时的返回值
        this.value = null;
        // 原因 表明Promise被拒绝的原因
        this.reason = null;
        // 后期使用
        this.defferd = [];
        //
        callback(this.resolve.bind(this), this.reject.bind(this));
    }

    /**
     * 被允许时触发
     * @param result
     */
    resolve(result) {
        this.states = 'fulfilled';
        this.value = result;
    }

    /**
     * 被拒绝时触发
     * @param error
     */
    reject(error) {
        this.states = 'rejected';
        this.reason = error;
    }

    then(callback) {
        if (this.states === 'fulfilled') {
            // 被允许时 执行
            callback(this.value);
        } else if (this.states === 'rejected') {
            // 被拒绝时 执行
            callback(this.reason);
        }
    }

    /**
     * 判断参数是否是一个函数
     * @param fun
     * @returns {boolean}
     */
    isFunction(fun) {
        return typeof fun === 'function';
    }
}

/**
 * 测试
 */
new CustomPromise((resolve, reject) => {

    if (Math.round(Math.random())) {
        resolve('666');
    } else {
        reject('777');
    }

}).then((result) => {
    console.log(result)
});
```
