---
title: 'ES6 yield'
date: '2017-11-16T10:03:24+00:00'
status: publish
permalink: /2017/11/16/es6-yield
author: 毛巳煜
excerpt: ''
type: post
id: 42
category:
    - JavaScript
tag: []
post_format: []
wb_sst_seo:
    - 'a:3:{i:0;s:0:"";i:1;s:0:"";i:2;s:0:"";}'
hestia_layout_select:
    - sidebar-right
---
### 生成器（Generator）的工作原理可以总结如下：

1. **内部暂停和恢复**： 
  - 生成器内部被 `yield` 标记的部分只执行一次，然后在该位置暂停执行。这个部分的执行结果会被返回。
2. **手动推进**： 
  - 通过显式调用生成器的 `.next()` 方法，可以从上一次暂停的位置继续执行，逐个生成值。这一过程需要手动控制。
3. **`.next().done`**： 
  - 使用 `.next().done` 可以判断生成器是否已经生成完所有值。当生成完最后一个值后，`.done` 变为 `true`。

> 这个机制允许你逐个生成值，保持控制流的状态，以及实现懒加载和分段生成值，这对于处理大数据集或无限序列非常有用，并且可以节省内存和计算资源。

```javascript
function* myGenerator() {
    yield 1;
    yield 2;
    yield 3;
}

const gen = myGenerator();

console.log(gen.next().value); // 输出 1
// 此时生成器函数在第一个 yield 处暂停

console.log(gen.next().value); // 输出 2
// 此时生成器函数在第二个 yield 处暂停

console.log(gen.next().value); // 输出 3
// 此时生成器函数在第三个 yield 处暂停

console.log(gen.next().done); // 输出 true，表示生成器生成完所有值

```

> 生成器函数`function*`与常规函数`function`不同之处在于，他不像常规函数`function`会一次性的把函数中的逻辑全部执行完，而是使用`yield`关键字，进行了暂停处理，这样做可有效的阻止函数中处理的业务逻辑过于庞大而导致内存溢出

- - - - - -

### 写一个带有延迟或能的生成器

```javascript
function* myGenerator() {
    yield 1;
    yield delay(3000); // 使用带有3秒延时的函数
    yield 3;
}

function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

const gen = myGenerator();

async function runGenerator() {
    console.log(gen.next().value); // 输出 1
    await gen.next().value; // 等待3秒后继续执行
    console.log(gen.next().value); // 输出 3
    console.log(gen.next().done); // 输出 true
}

runGenerator();


```