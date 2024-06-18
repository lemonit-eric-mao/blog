---
title: "Node_EventProxy_理解"
date: "2017-11-16"
categories: 
  - "node-js"
---

```javascript
/**
 * Created by mao-siyu on 16-10-28.
 * 通过事件实现异步协作是 EventProxy 的主要亮点
 * EventProxy 相关事件 API
 * on/addListener; // 绑定事件监听器
 * removeListener; // 移除事件的监听器
 * removeAllListeners; // 移除单个事件或者所有事件的监听器
 * emit; // 触发事件
 * once; // 绑定只执行一次的事件监听器
 * immediate/别名asap; // 绑定事件,并立即触发它
 * all/别名assign; // 绑定一些事件,当所有事件执行后,将执行回调方法
 * fail; // error事件处理
 * tail/别名assignAll/assignAlways; // 与all方法比较类似,都是注册到事件组合上。不同在于,指定事件都触发之后,如果事件依旧持续触发,将会在每次触发时调用handler
 * after; // 事件执行N次后,在执行回调函数
 * any; // 事件执行完成后,只执行一次回调函数
 * not; // 当事件名称与绑定的绑定事件名称不符时,才执行回调函数
 * done; // error事件处理
 * create; // 创建EventProxy
 *
 */
```

```javascript
var EventProxy = require('eventproxy');
var proxy = new EventProxy();

proxy.on('step1', function () {
    console.info('=-=-=-=- in step1 -=-=-=-=');
    proxy.emit('step2');
}).on('step2', function () {
    console.info('=-=-=-=- in step2 -=-=-=-=');
    // 重点 这里是不会执行step3的因为,它的事件在asap事件执行前还没有添加进来
    proxy.emit('step3');
    // asap 绑定事件,并立即触发它
}).asap('step1', function () {
    console.info('=-=-=-=- in step4 asap -=-=-=-=');
    // 重点 这里是不会执行step5的因为,它的事件在asap事件执行前还没有添加进来
    proxy.emit('step5');
}).on('step3', function () {
    console.info('=-=-=-=- in step3 -=-=-=-=');
    proxy.emit('step5');
}).on('step5', function () {
    console.info('=-=-=-=- in step5 -=-=-=-=');
    proxy.emit('step_success');
}).fail(function (err) {
    console.error(err);
}).all('step1', function () {
    console.info('=-=-=-=- in all -=-=-=-=');
});
```
