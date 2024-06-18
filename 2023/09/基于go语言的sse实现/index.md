---
title: "基于Go语言的SSE实现"
date: "2023-09-07"
categories: 
  - "go语言"
  - "javascript"
---

# SSE（Server-Sent Events）

## 概述

> SSE是一种用于实现`服务器向客户端实时推送`数据的Web技术。 它基于HTTP协议，允许服务器将数据以事件流的形式发送给客户端，从而实现实时通信。

#### SSE的关键特点包括：

1. **简单易用**: SSE采用文本格式（如纯文本或JSON），使数据的发送和解析变得简单。
2. **单向通信**: SSE支持服务器向客户端的单向通信，服务器可以主动推送数据给客户端，而客户端只需接收数据。
3. **实时性**: SSE建立长时间的连接，使服务器可以实时地将数据推送给客户端，无需客户端频繁地发起请求。

#### `SSE`与`WebSocket`相比

> `SSE`适用于需要`服务器向客户端实时推送`数据的场景，如股票价格更新、新闻实时推送等。 `WebSocket`则更适合需要`实时双向通信`的应用，如聊天应用或多人协同编辑工具。

* * *

### 前端代码（index.html）：

```javascript
<!DOCTYPE html>
<html lang="zh">
<head>
    <title>Chat Tool</title>
</head>
<body>
<div id="chat"></div>
<input type="text" id="message" placeholder="Type a message..."/>
<button onclick="sendMessage()">Send</button>

<script>
    // 获取DOM元素
    let chat = document.getElementById('chat');
    let messageInput = document.getElementById('message');

    let baseUrl = "http://127.0.0.1:8000"

    // 创建EventSource对象以接收服务器发送的事件
    let eventSource = new EventSource(`${baseUrl}/server/events`);

    // 当接收到事件消息时的处理程序
    eventSource.onmessage = (event) => {
        appendMessage(event.data);
    };

    // 发送消息给服务器
    function sendMessage() {
        let message = messageInput.value;
        if (!message) {
            return
        }

        // 构建消息参数
        let param = {
            "messages": [
                {
                    "role": "user",
                    "content": message
                }
            ]
        }

        // 设置HTTP请求选项
        let options = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(param),
        };

        // 发送消息到服务器
        fetch(`${baseUrl}/server/send`, options);
        messageInput.value = '';
    }

    // 在聊天界面中显示消息
    function appendMessage(message) {
        let messageElement = document.createElement('p');
        messageElement.innerText = message;
        chat.appendChild(messageElement);
    }
</script>
</body>
</html>

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
    EventChan <- result

    // 响应客户端
    writer.WriteHeader(http.StatusOK)
}

// handleEvents 处理推送事件
func handleEvents(writer http.ResponseWriter, request *http.Request) {
    // 设置响应头，指示服务器发送事件
    writer.Header().Set("Content-Type", "text/event-stream")
    writer.Header().Set("Cache-Control", "no-cache")
    writer.Header().Set("Connection", "keep-alive")

    // 初始化通道
    EventChan = make(chan []byte)

    for {
        message := <-EventChan
        // 这里必须这样写，尤其是【"data: %s\n\n"】除了%s其它的一个都不能少
        fmt.Fprintf(writer, "data: %s\n\n", message)
        writer.(http.Flusher).Flush() // 立即发送事件给客户端
    }
}

```
