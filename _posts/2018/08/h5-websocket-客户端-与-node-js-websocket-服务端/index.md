---
title: "H5 WebSocket 客户端  与 node.js WebSocket 服务端"
date: "2018-08-25"
categories: 
  - "node-js"
---

#### H5 WebSocket 客户端

```markup
<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <title>WebSocket测试</title>
    <script type="text/javascript">
        function startWebSocket() {

            const wsuri = 'ws://192.168.1.16:10086';
            const ws = new WebSocket(wsuri);

            ws.onopen = () => {
                console.log('与服务器链接成功!');
            }

            ws.onmessage = (evt) => {
                console.log(`接收服务端消息:    ${evt.data}`);
            }

            ws.onclose = () => {
                console.log('与服务器断开链接!');
            }

            // 异常
            ws.onerror = (evt) => {
                console.log(evt);
            };

            setInterval(() => {
                ws.send('WebSocketServer 你好!');
            }, 2000);
        }

    </script>
</head>
<body onload="startWebSocket();">
</body>
</html>
```

#### node.js WebSocket 服务端

```javascript
// 引入WebSocket模块
const ws = require('nodejs-websocket');
const PORT = 10086;

ws.createServer((conn) => {

    console.log('与客户端链接成功!');

    conn.on('text', (msg) => {
        console.log(msg)

        conn.sendText('WebSocketClient 你好!');
    })

    conn.on('close', () => {
        console.log('与客户端断开链接!');
    })

    conn.on('error', (err) => {
        console.log(err);
    })

}).listen(PORT);


const network = require('os').networkInterfaces();
const ip = network[Object.keys(network)[1]][0].address;

console.log(`ws://${ip}:${PORT}`);

```
