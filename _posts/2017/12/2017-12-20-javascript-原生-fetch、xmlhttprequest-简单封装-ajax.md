---
title: "JavaScript 原生 fetch、XMLHttpRequest 简单封装 Ajax"
date: "2017-12-20"
categories: 
  - "javascript"
---

## 新版

```javascript
class ajax {
    // 基础URL
    static baseURL = '';

    /**
     * 发起请求
     * @param url
     * @param options
     * @returns {Promise<any>}
     */
    static async request(url, options) {
        return await fetch(`${ajax.baseURL}${url}`, options); // 返回原始响应
    }

    /**
     * GET 请求
     * @param url
     * @param params
     * @param useBody
     * @returns {Promise<*>}
     */
    static async get(url, params, useBody = false) {

        let options = {
            method: 'GET',
        };

        if (useBody) {
            // 如果通过请求体传递参数
            options.headers = {'Content-Type': 'application/json'};
            options.body = JSON.stringify(params);
        } else {
            // 否则通过查询字符串传递参数（标准 HTTP 规范）
            let queryString = new URLSearchParams(params).toString();
            url = queryString ? `${url}?${queryString}` : url;
        }

        let response = await ajax.request(url, options);
        return response.json();
    }

    /**
     * POST 请求
     * @param url
     * @param data
     * @returns {Promise<*>}
     */
    static async post(url, data) {
        let options = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        };
        let response = await ajax.request(url, options);
        return response.json();
    }

    /**
     * PUT 请求
     * @param url
     * @param data
     * @returns {Promise<*>}
     */
    static async put(url, data) {
        let options = {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        };
        let response = await ajax.request(url, options);
        return response.json();
    }

    /**
     * DELETE 请求
     * @param url
     * @param params
     * @param useBody
     * @returns {Promise<*>}
     */
    static async delete(url, params, useBody = false) {
        let options = {
            method: 'DELETE',
        };

        // 通过请求体传递参数（兼容服务端不规范的实现）
        if (useBody) {
            options.headers = {'Content-Type': 'application/json'};
            options.body = JSON.stringify(params);
        } else {
            // 否则通过查询字符串传递参数（标准 HTTP 规范）
            let queryString = new URLSearchParams(params).toString();
            url = queryString ? `${url}?${queryString}` : url;
        }

        let response = await ajax.request(url, options);
        return response.json();
    }

    /**
     * 流式 POST 请求
     * @param url
     * @param data
     * @returns {Promise<*>}
     */
    static async postStream(url, data) {
        let options = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        };
        let response = await ajax.request(url, options);
        return response.body; // 返回流，交给业务代码处理
    }
}

```

#### **使用：**

> ```javascript
> ajax.baseURL = 'http://localhost:8080';
> 
> // 服务端为了方便直接返回了 JSON字符串
> let queryParams = new URLSearchParams();
> queryParams.append('year', 2023);
> queryParams.append('name', 'xxx');
> 
> let resultData = await ajax.get(`/server/task/list?${queryParams.toString()}`);
> ```

* * *

#### 案例

```javascript
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>

        #popupForm {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.5);
            z-index: 9999;
        }

        .popup-content {
            background-color: #fff;
            width: 300px;
            padding: 20px;
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            border-radius: 5px;
            box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.2);
        }

        .popup-close {
            position: absolute;
            top: 10px;
            right: 10px;
            cursor: pointer;
            font-size: 20px;
        }

        .popup-form {
            display: flex;
            flex-direction: column;
        }

        .popup-label {
            margin-top: 10px;
        }

        .popup-input {
            padding: 5px;
            margin-top: 5px;
        }

        .popup-button {
            margin-top: 10px;
            padding: 5px 10px;
            background-color: #007bff;
            color: #fff;
            border: none;
            cursor: pointer;
        }

        .popup-button:hover {
            background-color: #0056b3;
        }
    </style>
    <title>Create Task</title>
</head>
<body>
<div class="container">
    <button id="openFormBtn">Create Task</button>
</div>

<!--创建任务弹窗-->
<div id="popupForm" class="popup">
    <div class="popup-content">
        <span id="closeBtn" class="popup-close">×</span>
        <h2>创建任务</h2>
        <form id="taskForm" class="popup-form" onsubmit="return taskFormSubmit()">
            <label for="name" class="popup-label">Name:</label>
            <input type="text" class="popup-input" id="name" name="name" required>
            <label for="startTime" class="popup-label">Start Time:</label>
            <input type="date" class="popup-input" id="startTime" name="startTime" required>
            <label for="endTime" class="popup-label">End Time:</label>
            <input type="date" class="popup-input" id="endTime" name="endTime" required>
            <button type="submit" class="popup-button">Submit</button>
        </form>
    </div>
</div>

<script>
    let openFormBtn = document.getElementById('openFormBtn');

    // 窗体
    let popupForm = document.getElementById('popupForm');
    // 关闭窗体按钮
    let closeBtn = document.getElementById('closeBtn');
    // 窗体
    let taskForm = document.getElementById('taskForm');

    openFormBtn.addEventListener('click', () => {
        popupForm.style.display = 'block';
    });

    // 关闭窗体
    closeBtn.addEventListener('click', () => {
        popupForm.style.display = 'none';
        // 清空表单
        taskForm.reset();
    });

    /**
     * 提交表单
     */
    function taskFormSubmit() {

        // 获取表单数据
        let formData = new FormData(taskForm);
        // 表单数据转Json数据
        let jsonData = Object.fromEntries(formData);

        closeBtn.click();

        // 向服务端发起请求
        ajax.post('/server/task/add', jsonData);

        return false
    }
</script>
</body>
</html>

```

---

##### 流式调用

``` javascript
<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI 聊天对话</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/foundation-sites/dist/css/foundation.min.css">
    <script src="../ajax.js" defer></script>
    <style>
        #chatContainer {
            height: 80vh; /* 中间区域占 80% 高度 */
            overflow-y: auto;
            border: 1px solid #ccc;
            border-radius: 5px;
            margin-bottom: 20px;
            padding: 10px;
        }

        .user-message {
            display: flex;
            text-align: right;
            margin-bottom: 50px;
            flex-direction: column;
            align-items: flex-end;
        }

        .user-message-textarea {
            max-width: 60%; /* 最大宽度 60% */
            overflow-wrap: break-word; /* 超出时换行 */
            border: 0;
            border-radius: 10px;
            padding: 5px;
            margin-top: 10px;
            background-color: #f1f1f1;
        }

        .ai-message {
            display: flex;
            text-align: left;
            margin-bottom: 50px;
            flex-direction: column;
        }

        .ai-message-textarea {
            max-width: 100%; /* 最大宽度 100% */
            border: 0;
            border-radius: 5px;
            padding: 5px;
            overflow-wrap: break-word; /* 超出时换行 */
            margin-top: 10px;
        }

        .avatar {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            vertical-align: middle;
            margin-right: 10px;
        }

        #sendButton:disabled {
            background-color: #ccc;
        }
    </style>
</head>
<body>

<div class="grid-container">
    <div class="grid-x grid-margin-x">
        <div class="cell small-12">
            <div id="title">
                <h4>AI 聊天对话</h4>
            </div>
            <div id="chatContainer">
                <!-- 聊天内容将在这里动态插入 -->
            </div>
            <div class="grid-x grid-margin-x align-middle">
                <div class="cell small-9">
                    <input type="text" id="chatInput" class="form-control" placeholder="请输入您的消息">
                </div>
                <div class="cell small-1">
                    <button id="sendButton" class="button primary" disabled>发送</button>
                </div>
                <div class="cell small-2">
                    <select id="modelSelect" class="form-control">
                        <!-- 从 localStorage 中获取模型名称并填充 -->
                    </select>
                </div>
            </div>
        </div>
    </div>
</div>

<script>
    // 从 localStorage 中获取模型名称
    let modelSelect = document.getElementById('modelSelect');
    let models = JSON.parse(localStorage.getItem('modelList')) || [];

    models.forEach(modelName => {
        let option = document.createElement('option');
        option.value = modelName;
        option.textContent = modelName;
        modelSelect.appendChild(option);
    });

    // 发送按钮状态控制
    let chatInput = document.getElementById('chatInput');
    let sendButton = document.getElementById('sendButton');
    chatInput.addEventListener('input', () => {
        sendButton.disabled = chatInput.value.trim() === '';
    });

    async function sendMessage() {
        let message = chatInput.value.trim();
        if (message) {
            // 在聊天区域添加用户消息
            document.getElementById('chatContainer').innerHTML += `
                <div class="user-message">
                    <img class="avatar" src="user-avatar.png" alt="用户头像">
                    <span class="user-message-textarea">${message}</span>
                </div>
            `;
            chatInput.value = '';
            sendButton.disabled = true; // 发送后禁用按钮

            let response = await ajax.postStream('/api/chat/completions', {
                "question": message,
                "history": [],
                "stream": true,
                "model": modelSelect.value,
                "temperature": 0.5
            });

            // 处理流
            let reader = response.getReader();
            let decoder = new TextDecoder('utf-8');
            let readStream = async () => {
                let message = `
                    <img class="avatar" src="ai-avatar.png" alt="AI头像">
                    <span class="ai-message-textarea"></span>
                `

                // 必须要创建一个DOM元素，才能在下面使用appendChild()追加
                let wrapper = document.createElement('div');
                wrapper.classList.add('ai-message');
                // 将模板内容追加到DOM元素
                wrapper.innerHTML = message;
                // 将DOM元素追加到页面
                document.getElementById('chatContainer').appendChild(wrapper);

                while (true) {
                    let {done, value} = await reader.read();
                    if (done) break;

                    // 解码并处理每一行
                    let text = decoder.decode(value, {stream: true});
                    text.split('\n').forEach(line => {
                        if (line.trim()) { // 只处理非空行
                            let jsonObject = JSON.parse(line.replaceAll('data: {"text": ', '{"text": '));
                            wrapper.querySelector('.ai-message-textarea').innerHTML += jsonObject.text; // 将文本添加到页面
                        }
                    });
                }
            };
            await readStream(); // 等待流读取完成
        }
    }

    // 发送消息功能
    sendButton.onclick = () => {
        sendMessage();
    };

    // 回车事件
    chatInput.addEventListener('keydown', (event) => {
        if (event.key === 'Enter') {
            if (!event.shiftKey) {
                event.preventDefault(); // 阻止换行
                sendMessage();
            }
        }
    });
</script>

</body>
</html>

```

* * *

* * *

* * *

## 旧版

### ajax.html

```markup
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>ajax-example</title>
    <script src="ajax.js"></script>
    <script>
        $.ajax({
            method: 'GET',
            url: 'http://localhost:8060/',
            async: true,
            data: '',
            success: function (d) {
                console.log(d);
            },
            error: function (e) {
                console.info(e);
            }
        });
    </script>
</head>
<body>

</body>
</html>
```

### ajax.js

```javascript
/**
 * js原生 XMLHttpRequest 简单模拟 jquery Ajax
 * Created by mao_siyu on 2017/12/20.
 */
function $() {
}

$.ajax = function (option) {
    const xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            switch (xhr.status) {
                case 200:
                    option.success(xhr.response);
                    break;
                case 404:
                    option.error(xhr.statusText);
                    break;
                default:
                    option.error(xhr.statusText);
            }
        }
    }
    xhr.open(option.method, option.url, option.async || true);
    xhr.send({data: option.data});
}
```
