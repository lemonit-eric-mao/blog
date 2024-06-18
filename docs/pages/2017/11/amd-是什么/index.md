---
title: "AMD 是什么"
date: "2017-11-16"
categories: 
  - "node-js"
---

##### **什么是AMD, 与它的由来**

##### 这里需要引用 阮一峰 的一段话

**CommonJS规范`加载模块是同步`的，也就是说，只有加载完成，才能执行后面的操作。 由于Node.js主要用于服务器编程，模块文件一般都已经存在于本地硬盘，所以加载起来比较快，可以同步加载完成，等待时间就是硬盘的读取时间。**

**但是，对于浏览器，这却是一个大问题，因为模块都放在服务器端，等待时间取决于网速的快慢，可能要等很长时间，浏览器处于"假死"状态。 因此，浏览器端的模块，不能采用"同步加载"（synchronous），只能采用"异步加载"（asynchronous）。这就是AMD规范诞生的背景。**

**AMD是"Asynchronous Module Definition"的缩写，意思就是"异步模块定义"。 它采用`异步方式加载模块`，模块的加载不影响它后面语句的运行。 所有依赖这个模块的语句，都定义在一个回调函数中，等到加载完成之后，这个回调函数才会运行。**

[原文链接](http://www.ruanyifeng.com/blog/2012/10/asynchronous_module_definition.html "原文链接")

##### AMD 与 CommonJS 区别

假定有一个数学模块 math.js

```javascript
/**
 * Created by mao_siyu on 2017/9/10.
 * 测试类
 * @constructor
 */
// 此模块在程序启动时就会执行引用
// 缺点： 浏览器打开时加载模块会产生延迟等待，降低渲染速度，浏览器容易发生假死
const math = require('math');
math.add(2, 3); // 5
```

**AMD 写法**

```javascript
// 模块加载成功之后在执行回调函数，模块加载不是同步的，因此浏览器不会发生假死
require(['math'], function (math) {
    math.add(2, 3);
});
```
