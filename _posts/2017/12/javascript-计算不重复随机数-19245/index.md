---
title: "JavaScript 计算不重复随机数 192~45"
date: "2017-12-05"
categories: 
  - "javascript"
---

##### 需求: 有192条数据, 随机从里面取出45条不重复的数据, 保存到另一个数组当中

##### 请写出最优的算法.

```javascript
/**
 * 需求: 有192条数据, 随机从里面取出45条不重复的数据, 保存到另一个数组当中
 * 解答: 请写出最优的算法.
 * Created by mao-siyu on 17-12-5.
 */

// 先将192条数据平均分
// step 1 取余(结果是 12)
let s1 = 192 % 45;

// step 2 均分 并获取每段长度(结果是 4)
let s2 = (192 - s1) / 45;

// step 3 循环45次 从192条数据中随机获取数据(也就是在192这个范围内, 循环出45个不重复的随机数.)
// 但这样只能取得 范围是 180 的平均结果(还差 12)
for (let i = 0; i < 45; i++) {
    let temp = Math.floor(Math.random() * s2) + i * s2; // s2 = 4
}

// step 4 解决上面的问题 还需要加上12个数才能满足是从192这个范围内随机选取, 所以在加上 12
// 但这样, 最小数又变成了12, 所以不能将 12写死.
for (let i = 0; i < 45; i++) {
    let temp = Math.floor(Math.random() * s2) + i * s2 + s1; // s2 = 4  s1 = 12
}

// step 5 解决上面的问题 将12也变成随机数
let s5 = Math.floor(Math.random() * s1); // s1 = 12
for (let i = 0; i < 45; i++) {
    let temp = Math.floor(Math.random() * s2) + i * s2 + s5; // s2 = 4 s5 = (0~12随机数)
    console.log(temp);
}

/**=============================最终实现代码=========================================*/
const p192 = [];
const p45 = [];
for (let i = 1; i <= 192; i++) {
    p192.push(i);
}

let step1 = p192.length % 45;
let step2 = (p192.length - step1) / 45;

let step5 = Math.floor(Math.random() * step1);
for (let i = 0; i < 45; i++) {
    let index = Math.floor(Math.random() * step2) + i * step2 + step5;
    p45.push(p192[index]);
}

for (let i = 0, len = p45.length; i < len; i++) {
    console.log(p45[i]);
}
```
