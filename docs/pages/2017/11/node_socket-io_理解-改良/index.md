---
title: "Node_Socket.IO_理解 (改良)"
date: "2017-11-16"
categories: 
  - "node-js"
---

```javascript
/**
 * Created by mao_siyu on 2016/11/30.
 * socket.io服务
 */
var EventEmitter = require('events').EventEmitter;
var emitter = new EventEmitter();
// 创建http服务器并监听 10086 端口
var http = require('http');
var server = http.createServer().listen(10086);
// 长连接监听http服务器(如果有向服务器发送的长连接事件请求，将会被捕获)
var sio = require('socket.io');
var sc = sio.listen(server);
// 绑定一个事件 每次调用的时候进行连接,这样做是为了保证每次的调用都不会受到异步的影响而获取不到已经连接的socket
emitter.on('getSocket', function (callback) {
    sc.on('connection', function (socket) {
        console.log('客户端已经连接');
        callback(socket);
        // 监听是否断开事件
        socket.on('disconnect', function () {
            console.log('客户端断开连接');
        });
    });
});
//
var socket = function (callback) {
    emitter.emit('getSocket', callback);
};
module.exports = socket;

// 在其它模块中的用法
var socket = require('../public/config/socketIO');
socket(function (sc) {
});
```
