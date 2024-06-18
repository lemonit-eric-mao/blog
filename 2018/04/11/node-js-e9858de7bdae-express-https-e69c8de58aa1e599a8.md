---
title: 'Node.js 配置 express HTTPS 服务器'
date: '2018-04-11T10:23:56+00:00'
status: publish
permalink: /2018/04/11/node-js-%e9%85%8d%e7%bd%ae-express-https-%e6%9c%8d%e5%8a%a1%e5%99%a8
author: 毛巳煜
excerpt: ''
type: post
id: 2074
category:
    - node.js
tag: []
post_format: []
hestia_layout_select:
    - default
---
### 修改 Express 的 www 文件

```
<pre class="line-numbers prism-highlight" data-start="1">```javascript
<br></br>/**
 * Module dependencies.
 */
const app = require('../app');
const debug = require('debug')('server-encryption:server');
const http = require('http');
// 添加
const https = require('https');
const fs = require('fs');

/** ============================== HTTP 服务 ==================================== */

/**
 * 创建 HTTP 服务.
 */
const httpServer = http.createServer(app);
/**
 * 监听 HTTP 80端口.
 */
const httpPort = normalizePort(process.env.PORT || '80');
httpServer.listen(httpPort);
httpServer.on('error', onError);
httpServer.on('listening', onListening);

/** ============================== HTTPS 服务 ==================================== */

/**
 * HTTPS 服务 私钥与证书.
 */
const options = {
    // 私钥
    key: fs.readFileSync('ssl/privatekey.pem'),
    // 证书
    cert: fs.readFileSync('ssl/cert.pem')
};
/**
 * 创建 HTTPS 服务.
 */
const httpsServer = https.createServer(options, app);
/**
 * 监听 HTTPS 443端口.
 */
const httpsPort = normalizePort(process.env.PORT || '443');
httpsServer.listen(httpsPort);
httpsServer.on('error', onError);
httpsServer.on('listening', onListening);

/** ============================== END ==================================== */

/**
 * Normalize a port into a number, string, or false.
 */
function normalizePort(val) {
    let port = parseInt(val, 10);

    if (isNaN(port)) {
        // named pipe
        return val;
    }

    if (port >= 0) {
        // port number
        return port;
    }

    return false;
}

/**
 * Event listener for HTTP server "error" event.
 */
function onError(error) {
    if (error.syscall !== 'listen') {
        throw error;
    }

    let bind = typeof httpPort === 'string'
        ? 'Pipe ' + httpPort
        : 'Port ' + httpPort;

    // handle specific listen errors with friendly messages
    switch (error.code) {
        case 'EACCES':
            console.error(bind + ' requires elevated privileges');
            process.exit(1);
            break;
        case 'EADDRINUSE':
            console.error(bind + ' is already in use');
            process.exit(1);
            break;
        default:
            throw error;
    }
}

/**
 * Event listener for HTTP server "listening" event.
 */
function onListening() {
    let addr = httpServer.address();
    let bind = typeof addr === 'string'
        ? 'pipe ' + addr
        : 'port ' + addr.port;
    debug('Listening on ' + bind);
}

```
```