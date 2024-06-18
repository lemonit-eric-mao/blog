---
title: 'H5 WebSocket 客户端  与 node.js WebSocket 服务端'
date: '2018-08-25T15:22:44+00:00'
status: publish
permalink: /2018/08/25/h5-websocket-%e5%ae%a2%e6%88%b7%e7%ab%af-%e4%b8%8e-node-js-websocket-%e6%9c%8d%e5%8a%a1%e7%ab%af
author: 毛巳煜
excerpt: ''
type: post
id: 2288
category:
    - node.js
tag: []
post_format: []
hestia_layout_select:
    - default
---
#### H5 WebSocket 客户端

```
<pre data-language="HTML">```markup



    <meta content="text/html; charset=UTF-8" http-equiv="Content-Type"></meta>
    <title>WebSocket测试</title>
    <script type="text/javascript">
        function startWebSocket() {

            const wsuri = 'ws://192.168.1.16:10086';
            const ws = new WebSocket(wsuri);

            ws.onopen = () => {
                console.log('&#19982;&#26381;&#21153;&#22120;&#38142;&#25509;&#25104;&#21151;!');
            }

            ws.onmessage = (evt) => {
                console.log(`&#25509;&#25910;&#26381;&#21153;&#31471;&#28040;&#24687;:    ${evt.data}`);
            }

            ws.onclose = () => {
                console.log('&#19982;&#26381;&#21153;&#22120;&#26029;&#24320;&#38142;&#25509;!');
            }

            // &#24322;&#24120;
            ws.onerror = (evt) => {
                console.log(evt);
            };

            setInterval(() => {
                ws.send('WebSocketServer &#20320;&#22909;!');
            }, 2000);
        }

    </script>





```
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

console.log(`ws://<span class="katex math inline">{ip}:</span>{PORT}`);


```