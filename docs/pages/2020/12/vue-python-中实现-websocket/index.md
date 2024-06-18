---
title: "Vue + Python 中实现 WebSocket"
date: "2020-12-03"
categories: 
  - "vue"
---

###### Vue 做为客户端

```javascript
import Vue from 'vue';

/**
 * Created by mao-siyu on 17-12-21.
 */
class WS {

    constructor() {
        // 定时器ID用来执行网络重新链接
        this.intervalId = null;
        this.initConnect();
    }

    /**
     * 初始化链接配置
     */
    initConnect() {

        // 初始化 WebSocket 对象
        this.webSocket = new WebSocket(`ws://localhost:10086/websocket`);

        // 监听 WebSocket 连接异常的回调信息
        this.webSocket.onerror = (evt) => {
            console.log('%c%s', 'color:red;', '=============连接异常=============');
        };

        // 监听 WebSocket 服务端未连接的回调信息
        this.webSocket.onclose = (evt) => {
            console.log('%c%s', 'color:blue;', '=============网络连接已断开=============');
            if (!this.intervalId) {
                // 尝试重新链接
                this.intervalId = setInterval(() => {
                    console.log('%c%s', 'color:blue;', '=============正在尝试重新连接=============');
                    this.initConnect();
                }, 3000);
            }
        }

        // 监听 WebSocket 连接成功的回调信息
        this.webSocket.onopen = (evt) => {
            console.log('%c%s', 'color:purple;', '=============服务器已连接=============');
            if (this.intervalId) {
                // 服务器链接成功，清除重链定时器
                window.clearInterval(this.intervalId);
                this.intervalId = null;
            }
        }

        // 监听 WebSocket 接收消息
        this.webSocket.onmessage = (evt) => {
            // console.log('%c%s', 'color:green;', evt.data);
            this.onmessage(evt.data);
        }

    }

    /**
     * WebSocket 接收消息回调方法
     * @param msg
     */
    onmessage(msg) {
        console.log(msg)
        this.send(`你好我是 Client ${new Date()}`);
    }

    /**
     * WebSocket 发送消息方法
     * @param callback
     */
    send(info) {
        this.webSocket.send(info);
    }

}

// 添加到 Vue原型链
Vue.prototype.$WebSocket = new WS();

```

* * *

* * *

* * *

###### python 做为服务端

**安装： `pip3 install websockets`**

```python
#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2020/12/03 11:28
# @Author  : Eric.Mao
# @FileName: ws.py
# @Software: PyCharm
# @Blog    : http://www.dev-share.top/

import asyncio
import websockets


# 接收客户端消息， 使用 (无限循环 + 线程阻塞) 技术来实践会话监听
async def recv_msg(websocket, path):
    # 无限循环
    while True:
        # 线程阻塞， 等待接收客户端信息
        recv_text = await websocket.recv()
        print(f'{recv_text}')

        # 向客户端发送信息
        response_text = f"your submit context: {recv_text}"
        await websocket.send(response_text)


if __name__ == '__main__':
    server = websockets.serve(recv_msg, 'localhost', 10086)
    asyncio.get_event_loop().run_until_complete(server)
    asyncio.get_event_loop().run_forever()

```
