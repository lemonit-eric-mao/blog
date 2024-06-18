---
title: 基于Go语言的SSE实现
date: '2023-09-07T09:08:31+00:00'
status: private
permalink: /2023/09/07/%e5%9f%ba%e4%ba%8ego%e8%af%ad%e8%a8%80%e7%9a%84sse%e5%ae%9e%e7%8e%b0
author: 毛巳煜
excerpt: ''
type: post
id: 10279
category:
    - Go
    - JavaScript
tag: []
post_format: []
wb_sst_seo:
    - 'a:3:{i:0;s:0:"";i:1;s:0:"";i:2;s:0:"";}'
hestia_layout_select:
    - sidebar-right
---
SSE（Server-Sent Events）
=======================

概述
--

> SSE是一种用于实现`服务器向客户端实时推送`数据的Web技术。
> 
>  它基于HTTP协议，允许服务器将数据以事件流的形式发送给客户端，从而实现实时通信。

#### SSE的关键特点包括：

1. **简单易用**: SSE采用文本格式（如纯文本或JSON），使数据的发送和解析变得简单。
2. **单向通信**: SSE支持服务器向客户端的单向通信，服务器可以主动推送数据给客户端，而客户端只需接收数据。
3. **实时性**: SSE建立长时间的连接，使服务器可以实时地将数据推送给客户端，无需客户端频繁地发起请求。

#### `SSE`与`WebSocket`相比

> `SSE`适用于需要`服务器向客户端实时推送`数据的场景，如股票价格更新、新闻实时推送等。
> 
>  `WebSocket`则更适合需要`实时双向通信`的应用，如聊天应用或多人协同编辑工具。

- - - - - -

### 前端代码（index.html）：

```javascript



    <title>Chat Tool</title>


<div id="chat"></div>
<input id="message" placeholder="Type a message..." type="text"></input>
<button onclick="sendMessage()">Send</button>

<script>
    // &#33719;&#21462;DOM&#20803;&#32032;
    let chat = document.getElementById('chat');
    let messageInput = document.getElementById('message');

    let baseUrl = "http://127.0.0.1:8000"

    // &#21019;&#24314;EventSource&#23545;&#35937;&#20197;&#25509;&#25910;&#26381;&#21153;&#22120;&#21457;&#36865;&#30340;&#20107;&#20214;
    let eventSource = new EventSource(`<span class="katex math inline">{baseUrl}/server/events`);

    // &#24403;&#25509;&#25910;&#21040;&#20107;&#20214;&#28040;&#24687;&#26102;&#30340;&#22788;&#29702;&#31243;&#24207;
    eventSource.onmessage = (event) => {
        appendMessage(event.data);
    };

    // &#21457;&#36865;&#28040;&#24687;&#32473;&#26381;&#21153;&#22120;
    function sendMessage() {
        let message = messageInput.value;
        if (!message) {
            return
        }

        // &#26500;&#24314;&#28040;&#24687;&#21442;&#25968;
        let param = {
            "messages": [
                {
                    "role": "user",
                    "content": message
                }
            ]
        }

        // &#35774;&#32622;HTTP&#35831;&#27714;&#36873;&#39033;
        let options = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(param),
        };

        // &#21457;&#36865;&#28040;&#24687;&#21040;&#26381;&#21153;&#22120;
        fetch(`{baseUrl}/server/send`, options);
        messageInput.value = '';
    }

    // &#22312;&#32842;&#22825;&#30028;&#38754;&#20013;&#26174;&#31034;&#28040;&#24687;
    function appendMessage(message) {
        let messageElement = document.createElement('p');
        messageElement.innerText = message;
        chat.appendChild(messageElement);
    }
</script>




```

### 后端代码（main.go）：

```go
package server

import (
    "fmt"
    "github.com/lemonit-eric-mao/commons/logger"
    "io"
    "net/http"
)

// Router 定义服务端路由
func Router() {
    http.HandleFunc("/server/send", handleSend)
    http.HandleFunc("/server/events", handleEvents)
}

var EventChan chan []byte

// handleSend 处理添加请求
func handleSend(writer http.ResponseWriter, request *http.Request) {
    if request.Method != http.MethodPost {
        http.Error(writer, "只允许POST请求", http.StatusMethodNotAllowed)
        return
    }

    // 从请求体中读取数据
    body, err := io.ReadAll(request.Body)
    if err != nil {
        http.Error(writer, "无法读取请求体", http.StatusInternalServerError)
        return
    }

    // 将信息转发给大模型
    result, err := ErnieBotTurbo(string(body))
    if err != nil {
        logger.Error(err)
        http.Error(writer, err.Error(), http.StatusBadRequest)
        return
    }

    // 将查询结果推送给SSE事件
    EventChan 
```