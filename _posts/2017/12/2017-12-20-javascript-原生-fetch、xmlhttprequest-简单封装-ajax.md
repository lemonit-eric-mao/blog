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
        let response = await fetch(`${ajax.baseURL}${url}`, options);
        return response; // 返回原始响应
    }

    /**
     * GET 请求
     * @param url
     * @returns {Promise<*>}
     */
    static async get(url) {
        let response = await ajax.request(url, {});
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
     * @returns {Promise<*>}
     */
    static async delete(url) {
        let options = {
            method: 'DELETE',
        };
        let response = await ajax.request(url, options);
        return response.json();
    }

    /**
     * 流式 POST 请求
     * @param url
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
        const response = await ajax.request(url, options);
        
        // 处理流
        const stream = response.body;
        const reader = stream.getReader();
        const decoder = new TextDecoder('utf-8');
        let result = '';

        const readStream = async () => {
            while (true) {
                const { done, value } = await reader.read();
                if (done) break;
                result += decoder.decode(value, { stream: true });
            }
            return result; // 返回完整的结果
        };

        return readStream(); // 返回读取流的 Promise
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
