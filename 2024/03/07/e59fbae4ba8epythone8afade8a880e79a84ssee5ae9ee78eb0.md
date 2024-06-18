---
title: 基于Python语言的SSE实现
date: '2024-03-07T08:44:50+00:00'
status: private
permalink: /2024/03/07/%e5%9f%ba%e4%ba%8epython%e8%af%ad%e8%a8%80%e7%9a%84sse%e5%ae%9e%e7%8e%b0
author: 毛巳煜
excerpt: ''
type: post
id: 10703
category:
    - Python
    - 人工智能
tag: []
post_format: []
wb_sst_seo:
    - 'a:3:{i:0;s:0:"";i:1;s:0:"";i:2;s:0:"";}'
hestia_layout_select:
    - sidebar-right
---
Python 前端 index.html
--------------------

```python



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

- - - - - -

Python 服务端 main.py
------------------

```python
# 引入 FastAPI 框架，用于构建 Web 应用程序
from fastapi import FastAPI, Request, Response, HTTPException
# 引入 CORS 中间件，用于处理跨域请求
from fastapi.middleware.cors import CORSMiddleware
# 引入 Pydantic 库，用于数据验证和序列化
from pydantic import BaseModel
# 引入 List 类型，用于指定列表类型的参数或返回值
from typing import List
# 引入 StreamingResponse 类，用于实现流式响应
from sse_starlette import EventSourceResponse
from starlette.responses import StreamingResponse
# 引入 asyncio 库，用于异步编程
import asyncio
# 引入 json 库，用于 JSON 数据处理
import json

# 创建 FastAPI 应用程序实例
app = FastAPI()

# 添加跨域资源共享中间件，允许跨域请求
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源
    allow_credentials=True,  # 允许凭证
    allow_methods=["*"],  # 允许所有 HTTP 方法
    allow_headers=["*"],  # 允许所有 HTTP 头部
)

# 用于保存消息的列表
messages = []


# 用于接收和处理前端发送的消息
@app.post("/server/send")
async def receive_message(request: Request):
    # 接收请求的 JSON 数据
    data = await request.json()
    print(data)

    # 从 JSON 数据中获取消息
    m = data.get("messages")
    if m:
        # 如果存在消息，则将其添加到消息列表中
        messages.append(m)
        return {"status": "Message received successfully"}  # 返回成功状态
    else:
        # 如果未提供消息，则返回错误状态
        raise HTTPException(status_code=422, detail="传输的实体不正确")  # 返回错误状态码和详细信息


# 用于订阅事件消息的端点
@app.get("/server/events")
def subscribe_to_events():
    # 用于向前端推送事件消息
    async def event_generator():
        while True:
            if messages:  # 如果消息列表非空
                message = messages.pop(0)  # 弹出第一个消息
                yield f"data: {json.dumps(message)}"  # 以 Server-Sent Events 格式发送消息
            await asyncio.sleep(1)  # 设置消息推送的间隔时间为 1 秒

    return EventSourceResponse(event_generator(), media_type="text/event-stream")  # 返回流式响应


if __name__ == "__main__":
    # 当脚本作为主程序运行时，启动 FastAPI 应用程序
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)  # 在本地主机的 8000 端口上运行应用程序


```