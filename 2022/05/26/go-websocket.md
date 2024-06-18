---
title: 'Go WebSocket'
date: '2022-05-26T13:52:46+00:00'
status: publish
permalink: /2022/05/26/go-websocket
author: 毛巳煜
excerpt: ''
type: post
id: 8700
category:
    - Go
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
##### WebSocket 长链接

目前为止基本上现有的所有**http服务器**，使用 **`同一个端口`** 都能够同时支持 **`长链接`和`短链接`**

- - - - - -

###### **[项目地址](https://gitee.com/eric-mao/iris-server/repository/archive/0.2.0-websocket.zip "项目地址")**

###### Websocket相关文件

```ruby
    index-ws.html
    irisws-goroutine.go
    irisws.go
    README.md

```

> - index-ws.html 文件是使用 **HTML5** 写的长链接客户端，静态页面双击打开即可向服务端自动发起链接

```javascript



    <meta content="text/html; charset=UTF-8" http-equiv="Content-Type"></meta>
    <title>WebSocket测试</title>
    <script type="text/javascript">
        class WS {

            constructor() {
                // &#23450;&#26102;&#22120;ID&#29992;&#26469;&#25191;&#34892;&#32593;&#32476;&#37325;&#26032;&#38142;&#25509;
                this.intervalId = null;
                this.initConnect();
            }

            /**
             * &#21021;&#22987;&#21270;&#38142;&#25509;&#37197;&#32622;
             */
            initConnect() {

                // &#21021;&#22987;&#21270; WebSocket &#23545;&#35937;
                this.webSocket = new WebSocket(`ws://localhost:8080/websocket`);

                // &#30417;&#21548; WebSocket &#36830;&#25509;&#24322;&#24120;&#30340;&#22238;&#35843;&#20449;&#24687;
                this.webSocket.onerror = (evt) => {
                    console.log('%c%s', 'color:red;', '=============&#36830;&#25509;&#24322;&#24120;=============');
                };

                // &#30417;&#21548; WebSocket &#26381;&#21153;&#31471;&#26410;&#36830;&#25509;&#30340;&#22238;&#35843;&#20449;&#24687;
                this.webSocket.onclose = (evt) => {
                    console.log('%c%s', 'color:blue;', '=============&#32593;&#32476;&#36830;&#25509;&#24050;&#26029;&#24320;=============');
                    if (!this.intervalId) {
                        // &#23581;&#35797;&#37325;&#26032;&#38142;&#25509;
                        this.intervalId = setInterval(() => {
                            console.log('%c%s', 'color:blue;', '=============&#27491;&#22312;&#23581;&#35797;&#37325;&#26032;&#36830;&#25509;=============');
                            this.initConnect();
                        }, 3000);
                    }
                }

                // &#30417;&#21548; WebSocket &#36830;&#25509;&#25104;&#21151;&#30340;&#22238;&#35843;&#20449;&#24687;
                this.webSocket.onopen = (evt) => {
                    console.log('%c%s', 'color:purple;', '=============&#26381;&#21153;&#22120;&#24050;&#36830;&#25509;=============');
                    if (this.intervalId) {
                        // &#26381;&#21153;&#22120;&#38142;&#25509;&#25104;&#21151;&#65292;&#28165;&#38500;&#37325;&#38142;&#23450;&#26102;&#22120;
                        window.clearInterval(this.intervalId);
                        this.intervalId = null;
                    }
                }

                // &#30417;&#21548; WebSocket &#25509;&#25910;&#28040;&#24687;
                this.webSocket.onmessage = (evt) => {
                    this.onmessage(evt.data);
                }

            }

            /**
             * WebSocket &#25509;&#25910;&#28040;&#24687;&#22238;&#35843;&#26041;&#27861;
             * @param msg
             */
            onmessage(msg) {
                document.body.innerText = msg
                console.log('%c%s', 'color:green;', msg);
                this.send(`&#20320;&#22909;&#25105;&#26159; Client ${new Date().toLocaleString()}`);
            }

            /**
             * WebSocket &#21457;&#36865;&#28040;&#24687;&#26041;&#27861;
             * @param callback
             */
            send(info) {
                this.webSocket.send(info);
            }

        }
    </script>






```

> - irisws.go 文件是使用 **go** 语言编写的基于**Iris服务器的**长链接服务端，使用 **`gobwas/ws`** 模块实现WebSocket 
>   - 基于回调函数的设计编写

```go
package ws

import (
    "github.com/kataras/iris/v12"
    "github.com/kataras/iris/v12/websocket"
    "github.com/kataras/neffos"
    "log"
)

type IrisWebSocket struct {
    ws *neffos.Server
}

// NewWebSocket 初始化 WebSocket
func NewWebSocket(app *iris.Application) *IrisWebSocket {

    i := &IrisWebSocket{}

    // 使用gobwas/ws模块实现WebSocket
    i.ws = websocket.New(websocket.DefaultGobwasUpgrader, websocket.Events{
        // 将回调函数暴露给使用者
        websocket.OnNativeMessage: i.ReceiveMessage,
    })

    // 监听服务是否链接
    i.ws.OnConnect = func(c *websocket.Conn) error {
        log.Printf("[%s] 服务已连接!", c.ID())
        return nil
    }

    // 监听链接是否断开
    i.ws.OnDisconnect = func(c *websocket.Conn) {
        log.Printf("[%s] 链接已断开!", c.ID())
    }

    // 设置WebSocket链接地址
    app.Any("/websocket", websocket.Handler(i.ws))

    return i
}

// SendMessage 发送消息
func (i *IrisWebSocket) SendMessage(message string) {

    i.ws.Broadcast(nil, websocket.Message{
        Body:     []byte(message), // 消息体
        IsNative: true,            // 使用自己的格式传递数据
    })
}

// ReceiveMessage 接收客户消息
func (i *IrisWebSocket) ReceiveMessage(nsConn *websocket.NSConn, msg websocket.Message) error {
    log.Printf("接收到客户端消息: %s from [%s]", msg.Body, nsConn.Conn.ID())
    return nil
}


```

> - irisws-goroutine.go 文件是使用 **go** 语言编写的基于**Iris服务器的**长链接服务端，使用 **`gorilla/websocket`** 模块实现WebSocket 
>   - 基于Go协程的设计编写

```go
package ws

import (
    gorilla "github.com/gorilla/websocket"
    "github.com/kataras/iris/v12"
    "github.com/kataras/iris/v12/websocket"
    "github.com/kataras/neffos"
    irisgorilla "github.com/kataras/neffos/gorilla"
    "log"
    "net/http"
)

type IrisWebSocketGoroutine struct {
    ws             *neffos.Server
    ReceiveMessage chan []byte // 接收消息的通道
    SendMessage    chan string // 推送消息的通道
}

// NewWebSocketGoroutine 初始化 WebSocket
func NewWebSocketGoroutine(app *iris.Application) *IrisWebSocketGoroutine {

    i := &IrisWebSocketGoroutine{
        ReceiveMessage: make(chan []byte),
        SendMessage:    make(chan string),
    }

    // 使用gorilla/websocket模块实现WebSocket
    u := irisgorilla.Upgrader(gorilla.Upgrader{
        // 允许跨域
        CheckOrigin: func(r *http.Request) bool {
            return true
        },
    })

    i.ws = websocket.New(u, websocket.Events{
        websocket.OnNativeMessage: func(nsConn *websocket.NSConn, msg websocket.Message) error {
            // 将接收到的消息发送到通道中
            i.ReceiveMessage 
```

- - - - - -

- - - - - -

- - - - - -

##### 测试使用 main\_test.go

```go
package main

import (
    "github.com/kataras/iris/v12"
    "iris-server/commons/tools"
    "iris-server/commons/ws"
    "testing"
    "time"
)

// 测试WebSocket
func TestWebSocket(t *testing.T) {
    app := iris.Default()

    // 初始化 WebSocket
    i := ws.NewWebSocket(app)
    // 定时推送消息
    go tools.SetInterval(1e9, func() {
        i.SendMessage(time.Now().Format("2006-01-02 15:04:05"))
    })

    // 启动服务
    app.Listen(":8080")
}

// 测试WebSocket
func TestGoroutineWebSocket(t *testing.T) {
    app := iris.Default()

    // 初始化 WebSocket
    i := ws.NewWebSocketGoroutine(app)
    // 定时推送消息
    go tools.SetInterval(1e9, func() {
        i.SendMessage 
```

> **`go服务端`程序启动后，打开`index-ws.html`文件会自动与`go服务端`建立长链接，之后查看控制台，`go服务端`程序会不断的向`index-ws.html`端发送信息。**