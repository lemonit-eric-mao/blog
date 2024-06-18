---
title: "深入 Javascript 逻辑运行"
date: "2019-11-06"
categories: 
  - "javascript"
---

##### 一个对象 == 多个结果

```javascript
var obj = {
    value: 1,
    valueOf() {
        console.info(`执行了valueOf() ${this.value}`)
        console.log('\n')
        return this.value++;
    },
    // 或
    toString() {
        console.warn(`执行了toString() ${this.value}`)
        console.log('\n')
        return this.value++;
    }
}

if (obj == 1 && obj == 2 && obj == 3) {
    console.log(true)
}
```

* * *

##### 一个对象 === 多个结果

##### [Object.defineProperty()](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/Object/defineProperty "Object.defineProperty()")

```javascript
Object.defineProperty(this, 'obj', {
    get() {
        this.m = this.m ? this.m + 1 : 1;
        console.info(`执行了defineProperty的get() ${this.m} 次`)
        return this.m;
    }
});

if (obj === 1 && obj == 2 && obj === 3) {
    console.log(true)
}
```
