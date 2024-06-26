---
title: "Node_EventEmitter_理解"
date: "2017-11-16"
categories: 
  - "node-js"
---

```javascript
/**
 * Created by mao-siyu on 16-10-26.
 *
 * Node.js EventEmitter
 * Node.js 所有的异步 I/O 操作在完成时都会发送一个事件到事件队列。
 * Node.js 里面的许多对象都会分发事件：一个net.Server对象会在每次有新连接时分发一个事件， 一个fs.readStream对象会在文件被打开的时候发出一个事件。 所有这些产生事件的对象都是 events.EventEmitter 的实例。
 *
 * EventEmitter 类
 * events 模块只提供了一个对象： events.EventEmitter。EventEmitter 的核心就是事件触发与事件监听器功能的封装。
 * 你可以通过require("events");来访问该模块。
 *
 * EventEmitter 对象如果在实例化时发生错误，会触发 'error' 事件。当添加新的监听器时，'newListener' 事件会触发，当监听器被移除时，'removeListener' 事件被触发。
 * 下面我们用一个简单的例子说明 EventEmitter 的用法：
 */
```

```javascript
var EventEmitter = require('events').EventEmitter;
var emitter1 = new EventEmitter();
/**
 * on方法 注册一个监听器
 */
emitter1.on('some_event', function () {
    console.log('emitter1: ====== some_event 事件触发');
});
/**
 * 循环触发
 */
var stop = setInterval(function () {
    // emit方法 执行监听器
    emitter1.emit('some_event');
}, 1000);
clearInterval(stop);
```

```javascript
/**
 * EventEmitter 的每个事件由一个事件名和若干个参数组成，事件名是一个字符串，通常表达一定的语义。
 * 对于每个事件，EventEmitter 支持 若干个事件监听器。
 * 当事件触发时，注册到这个事件的事件监听器被依次调用，事件参数作为回调函数参数传递。
 * 让我们以下面的例子解释这个过程：
 * 以下例子中，emitter 为事件 someEvent 注册了两个事件监听器，然后触发了 someEvent 事件。
 * 运行结果中可以看到两个事件监听器回调函数被先后调用。 这就是EventEmitter最简单的用法。
 */
var events = require('events');
var emitter2 = new events.EventEmitter();
// emitter2.setMaxListeners(100);
/**
 * on方法也可以理解成是 订阅someEvent事件
 */
// for (var i = 0; i < 10; i++) {
emitter2.once('someEvent', function (arg1, arg2) {
    console.log('listener1', arg1, arg2);
});
emitter2.on('someEvent', function (arg1, arg2) {
    console.log('listener2', arg1, arg2);
});
emitter2.on('someEvent', function (arg1, arg2) {
    console.log('listener3', arg1, arg2);
});
// }
/**
 * emit方法也可以理解成 广播someEvent事件
 */
emitter2.emit('someEvent', 'arg1 参数', 'arg2 参数');

/**
 * 循环触发
 */
var stop = setInterval(function () {
    // emit方法 执行监听器
    emitter2.emit('someEvent', 'for arg1 参数', 'for arg2 参数');
}, 1000);
clearInterval(stop);
```

```javascript
// 1    addListener(event, listener)
// 为指定事件添加一个监听器到监听器数组的尾部。
// 2    on(event, listener)
// 为指定事件注册一个监听器，接受一个字符串 event 和一个回调函数。
//
// server.on('connection', function (stream) {
//     console.log('someone connected!');
// });
//
// 3    once(event, listener)
// 为指定事件注册一个单次监听器，即 监听器最多只会触发一次，触发后立刻解除该监听器。
//
// server.once('connection', function (stream) {
//     console.log('Ah, we have our first user!');
// });
//
// 4    removeListener(event, listener)
// 移除指定事件的某个监听器，监听器 必须是该事件已经注册过的监听器。
//
// var callback = function(stream) {
//     console.log('someone connected!');
// };
// server.on('connection', callback);
// // ...
// server.removeListener('connection', callback);
//
// 5    removeAllListeners([event])
// 移除所有事件的所有监听器， 如果指定事件，则移除指定事件的所有监听器。
// 6    setMaxListeners(n)
// 默认情况下， EventEmitters 如果你添加的监听器超过 10 个就会输出警告信息。 setMaxListeners 函数用于提高监听器的默认限制的数量。
// 7    listeners(event)
// 返回指定事件的监听器数组。
// 8    emit(event, [arg1], [arg2], [...])
// 按参数的顺序执行每个监听器，如果事件有注册监听返回 true，否则返回 false。
```
