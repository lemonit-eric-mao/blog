---
title: "Node_Socket.IO_理解"
date: "2017-11-16"
categories: 
  - "node-js"
---

```javascript
/**
 * Created by mao_siyu on 2016/11/30.
 *  socket.io服务
 */
// 创建http服务器并监听1337端口
var http = require('http');
var server = http.createServer().listen(1337);
// 长连接监听http服务器(如果有向服务器发送的长连接事件请求，将会被捕获)
var sio = require('socket.io');
var socket = sio.listen(server);
socket.on('connection', function (socket) {
    console.log('客户端建立连接');
    // 监听是否断开事件
    socket.on('disconnect', function () {
        console.log('客户端断开连接');
    });
    // 接收客户端的请求事件
    socket.on('client_connection', function (message) {
        console.log(message);
    });
    // 定时向客户端发送信息
    setInterval(function () {
        socket.emit('news', '你好');
    }, 1000);
});
```
