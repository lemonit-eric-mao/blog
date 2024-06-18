---
title: "Node_Socket_理解"
date: "2017-11-16"
categories: 
  - "node-js"
---

```javascript
// 构建 TCP 服务
var net = require('net');
/**
 * 创建TCP服务器
 * 解释:TCP的请求方式是 点对点方式,需要先建立三次握手成功以后,才能实现连接.
 * 以www.housecenter.cn 网址为例:Linux系统下使用 curl -v 命令来解释TCP的三次握手
 *
 *    mao-siyu@mao-siyu-PC:~$ curl -v www.housecenter.cn
 *
 *    // 第一部分内容为经典的TCP的三次握手请求报文；如下所示:
 *    * Rebuilt URL to: www.housecenter.cn/
 *    *   Trying 42.56.70.236...
 *    * Connected to www.housecenter.cn (42.56.70.236) port 80 (#0)
 *    // 第二部分 在握手完成之后,客户端向服务端发送请求；如下所示:
 *    > GET / HTTP/1.1
 *    > Host: www.housecenter.cn
 *    > User-Agent: curl/7.47.0
 *    > Accept: *\/*
 *    >
 *    // 第三部分是服务端完成处理后,向客户端发送响应内容,包括响应头和响应体；如下所示:
 *    < HTTP/1.1 301 Moved Permanently
 *    < Server: openresty/1.9.7.5
 *    < Date: Fri, 11 Nov 2016 03:58:15 GMT
 *    < Content-Type: text/html
 *    < Content-Length: 190
 *    < Connection: keep-alive
 *    < Location: https://www.housecenter.cn/
 *    <
 *    <html>
 *    <head><title>301 Moved Permanently</title></head>
 *    <body bgcolor="white">
 *    <center><h1>301 Moved Permanently</h1></center>
 *    <hr><center>openresty/1.9.7.5</center>
 *    </body>
 *    </html>
 *    // 最后部分是结束会话的信息；如下所示:
 *    * Connection #0 to host www.housecenter.cn left intact
 *    mao-siyu@mao-siyu-PC:~$
 */
```

```javascript
var server = net.createServer(function (socket) {
    // 新的连接
    socket.on('data', function (paramData) {
        socket.write('你好!');
    });

    socket.on('end', function (paramData) {
        socket.write('连接断开!');
    });

    socket.write('<<深入浅出Node.js>>示例: \n');
});
```

```javascript
/**
 * 监听接口
 */
server.listen(6666, function () {
    console.log('TCP server bound success! Please use command $> telnet ip port');
});

```

```javascript
// 构建 UDP 服务
var dgram = require('dgram');
/**
 * 创建UDP服务
 * 解释:UDP是以数据报的形式传输,无论是否有链接,都会向本地的指定的ip地址和端口,发送数据.
 */
var dServer = dgram.createSocket('udp4');

dServer.on('message', function (msg, rinfo) {
    console.log('server got: ' + msg + ' form ' + rinfo.address + ':' + rinfo.port);
});

dServer.on('listening', function () {
    var address = dServer.address();
    console.log('\n');
    console.log('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=');
    console.log('\n');
    console.log(address.address + ':' + address.port);
});

dServer.bind(8888);
```

```javascript
var dgram = require('dgram');
// 创建UDP客户端
var client = dgram.createSocket('udp4');
var message = new Buffer('深入浅出Node.js');
/**
 * 发送信息
 */
client.send(message, 0, message.length, '8888', 'localhost', function (err, bytes) {
    client.close();
});
```
