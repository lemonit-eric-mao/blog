---
title: 'JavaScript 原生 fetch、XMLHttpRequest 简单封装 Ajax'
date: '2017-12-20T22:51:57+00:00'
status: publish
permalink: /2017/12/20/javascript-%e5%8e%9f%e7%94%9f-fetch%e3%80%81xmlhttprequest-%e7%ae%80%e5%8d%95%e5%b0%81%e8%a3%85-ajax
author: 毛巳煜
excerpt: ''
type: post
id: 1783
category:
    - JavaScript
tag: []
post_format: []
wb_sst_seo:
    - 'a:3:{i:0;s:0:"";i:1;s:0:"";i:2;s:0:"";}'
hestia_layout_select:
    - sidebar-right
---
新版
--

```javascript
class ajax {
    static baseURL = '';

    /**
     * 发起请求
     * @param url
     * @param options
     * @returns {Promise<any>}
     */
    static async request(url, options) {
        let response = await fetch(`<span class="katex math inline">{ajax.baseURL}</span>{url}`, options);
        return response.json();
    }

    /**
     *
     * @param url
     * @returns {Promise}
     */
    static async get(url) {
        return ajax.request(url, {});
    }

    /**
     *
     * @param url
     * @param data
     * @returns {Promise}
     */
    static async post(url, data) {
        let options = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        };
        return ajax.request(url, options);
    }

    /**
     *
     * @param url
     * @param data
     * @returns {Promise}
     */
    static async put(url, data) {
        let options = {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        };
        return ajax.request(url, options);
    }

    /**
     *
     * @param url
     * @returns {Promise}
     */
    static async delete(url) {
        let options = {
            method: 'DELETE',
        };
        return ajax.request(url, options);
    }
}

</any>
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
> 
> ```

- - - - - -

#### 案例

```javascript



    <meta charset="UTF-8"></meta>
    <meta content="width=device-width, initial-scale=1.0" name="viewport"></meta>
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


<div class="container">
    <button id="openFormBtn">Create Task</button>
</div>


<div class="popup" id="popupForm">
    <div class="popup-content">
        <span class="popup-close" id="closeBtn">×</span>
        <h2>创建任务</h2>
        <form class="popup-form" id="taskForm" onsubmit="return taskFormSubmit()">
            <label class="popup-label" for="name">Name:</label>
            <input class="popup-input" id="name" name="name" required="" type="text"></input>
            <label class="popup-label" for="startTime">Start Time:</label>
            <input class="popup-input" id="startTime" name="startTime" required="" type="date"></input>
            <label class="popup-label" for="endTime">End Time:</label>
            <input class="popup-input" id="endTime" name="endTime" required="" type="date"></input>
            <button class="popup-button" type="submit">Submit</button>
        </form>
    </div>
</div>

<script>
    let openFormBtn = document.getElementById('openFormBtn');

    // &#31383;&#20307;
    let popupForm = document.getElementById('popupForm');
    // &#20851;&#38381;&#31383;&#20307;&#25353;&#38062;
    let closeBtn = document.getElementById('closeBtn');
    // &#31383;&#20307;
    let taskForm = document.getElementById('taskForm');

    openFormBtn.addEventListener('click', () => {
        popupForm.style.display = 'block';
    });

    // &#20851;&#38381;&#31383;&#20307;
    closeBtn.addEventListener('click', () => {
        popupForm.style.display = 'none';
        // &#28165;&#31354;&#34920;&#21333;
        taskForm.reset();
    });

    /**
     * &#25552;&#20132;&#34920;&#21333;
     */
    function taskFormSubmit() {

        // &#33719;&#21462;&#34920;&#21333;&#25968;&#25454;
        let formData = new FormData(taskForm);
        // &#34920;&#21333;&#25968;&#25454;&#36716;Json&#25968;&#25454;
        let jsonData = Object.fromEntries(formData);

        closeBtn.click();

        // &#21521;&#26381;&#21153;&#31471;&#21457;&#36215;&#35831;&#27714;
        ajax.post('/server/task/add', jsonData);

        return false
    }
</script>




```

- - - - - -

- - - - - -

- - - - - -

旧版
--

### ajax.html

```
<pre data-language="HTML">```markup



    <meta charset="UTF-8"></meta>
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






```
```

### ajax.js

```javascript
/**
 * js原生 XMLHttpRequest 简单模拟 jquery Ajax
 * Created by mao_siyu on 2017/12/20.
 */
function <span class="katex math inline">() {
}</span>.ajax = function (option) {
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