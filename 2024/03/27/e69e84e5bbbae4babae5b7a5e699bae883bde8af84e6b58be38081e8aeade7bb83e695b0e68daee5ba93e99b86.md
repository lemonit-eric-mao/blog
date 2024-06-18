---
title: 构建RAG评测、训练数据库集
date: '2024-03-27T12:07:35+00:00'
status: publish
permalink: /2024/03/27/%e6%9e%84%e5%bb%ba%e4%ba%ba%e5%b7%a5%e6%99%ba%e8%83%bd%e8%af%84%e6%b5%8b%e3%80%81%e8%ae%ad%e7%bb%83%e6%95%b0%e6%8d%ae%e5%ba%93%e9%9b%86
author: 毛巳煜
excerpt: ''
type: post
id: 10732
category:
    - 人工智能
    - 开发工具
tag: []
post_format: []
wb_sst_seo:
    - 'a:3:{i:0;s:0:"";i:1;s:0:"";i:2;s:0:"";}'
hestia_layout_select:
    - sidebar-right
---
构建RAG评测、训练数据库集
==============

介绍
--

> 该小工具旨在简化创建数据集的复杂性。  
>  对于初学者在测试 RAG 系统时存在很多不明之处，使用此工具可以通过简单的字符串拼接来生成 RAGAS 的测试数据集。  
>  同时，也可以将后台代码修改为自动收集 RAG 系统的评估数据。

安装教程
----

```bash
conda create -n ragas python==3.10.12 -c http://172.16.21.146:8081/repository/anaconda-proxy/main --override-channels

pip install -i http://172.16.21.146:8081/repository/pypi/simple  --trusted-host 172.16.21.146 --timeout 0 -r ./requirements.txt

```

使用说明
----

> 使用该工具非常简单。通过一个`静态页面`和一个 `FastAPI 服务端`将简化的数据格式转换为 `RAGAS 数据集`，你可以直接通过浏览器将数据集下载到本地。  
>  运行服务端的 `python main.py` 后，双击打开静态页，即可输入你要转换为数据集的数据。格式如下：

```text
question:法国的首都是什么？,
groundTruths:巴黎,
answer:巴黎,
contexts:巴黎是法国的首都。,

question:《哈利波特》的作者是谁？,
groundTruths:J.K.罗琳,
answer:J.K.罗琳,
contexts:J.K.罗琳写了《哈利波特》。,

question:水的沸点是多少？,
groundTruths:100度摄氏度,
answer:100度摄氏度,
contexts:水在海平面下沸腾的温度是100摄氏度。,

```

#### 点击`提交`进行数据集格式转换

[![](http://qiniu.dev-share.top/image/create_dataset.png)](http://qiniu.dev-share.top/image/create_dataset.png)

#### 点击`导出`会下载生成的数据集.zip

[![](http://qiniu.dev-share.top/image/export.png)](http://qiniu.dev-share.top/image/export.png)

- - - - - -

前端代码
====

<div style="overflow:hidden; clear:both; width: 100%; height: 40px; position: relative;">- - - - - -

 <span style="position: absolute;top: 50%;left: 50%; transform: translate(-50%, -50%); background-color: white;">以下为隐藏内容</span> </div> ### index.html

```javascript



    <meta charset="UTF-8"></meta>
    <meta content="width=device-width, initial-scale=1.0" name="viewport"></meta>
    <title>表单管理</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f0f0f0;
            color: #333;
        }

        h1, h2 {
            margin-bottom: 10px;
            padding-left: 20px;
        }

        h1 {
            font-size: 24px;
        }

        h2 {
            font-size: 20px;
        }

        form {
            margin-bottom: 20px;
            padding: 0 20px;
        }

        label {
            display: block;
            margin-bottom: 5px;
        }

        textarea {
            width: calc(100% - 40px);
            padding: 10px;
            font-size: 16px;
        }

        input[type="submit"], button {
            padding: 10px 15px;
            font-size: 16px;
            cursor: pointer;
            background-color: #007bff;
            color: #fff;
            border: none;
            border-radius: 5px;
        }

        input[type="submit"]:hover, button:hover {
            background-color: #0056b3;
        }

        ul {
            list-style-type: none;
            padding: 0;
            padding-left: 20px;
        }

        li {
            margin-bottom: 10px;
            padding: 10px;
            background-color: #fff;
            border: 1px solid #ddd;
            border-radius: 5px;
        }

        li:last-child {
            margin-bottom: 0;
        }

        section {
            margin: 20px;
        }

        /* &#26679;&#24335;&#25353;&#38062; */
        .export-button {
            font-size: 12px; /* &#26356;&#25913;&#25353;&#38062;&#22823;&#23567; */
        }

        .delete-button {
            color: red; /* &#23558;&#21024;&#38500;&#25353;&#38062;&#39068;&#33394;&#26356;&#25913;&#20026;&#32418;&#33394; */
            font-size: 12px; /* &#23558;&#21024;&#38500;&#25353;&#38062;&#22823;&#23567;&#26356;&#25913;&#20026;&#19982;&#23548;&#20986;&#25353;&#38062;&#30456;&#21516; */
        }

        pre {
            background-color: #f3f0f0;
        }
    </style>



<header>
    <h1>构建数据集</h1>
</header>

<section>
    <h2>批量创建数据集</h2>
    <form id="createDataSet">
        <textarea cols="50" id="formData" name="formData" placeholder="question:法国的首都是什么？,
groundTruths:巴黎,
answer:巴黎,
contexts:巴黎是法国的首都。,

question:《哈利波特》的作者是谁？,
groundTruths:J.K.罗琳,
answer:J.K.罗琳,
contexts:J.K.罗琳写了《哈利波特》。,

question:水的沸点是多少？,
groundTruths:100度摄氏度,
answer:100度摄氏度,
contexts:水在海平面下沸腾的温度是100摄氏度。,
" rows="15"></textarea>
        <input type="submit" value="提交"></input>
    </form>
</section>

<section>
    <h2>表单列表</h2>
    <ul id="formsList"></ul>
</section>

<script>

    class ajax {
        static baseURL = '';

        /**
         * &#21457;&#36215;&#35831;&#27714;
         * @param url
         * @param options
         * @returns {Promise<any>}
         */
        static async request(url, options) {
            let response = await fetch(`<span class="katex math inline">{ajax.baseURL}{url}`, options);
            return response.json();
        }

        /**
         *
         * @param url
         * @returns {Promise<*>}
         */
        static async get(url) {
            return ajax.request(url, {});
        }

        /**
         *
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
            return ajax.request(url, options);
        }

        /**
         *
         * @param url
         * @returns {Promise<*>}
         */
        static async delete(url) {
            let options = {
                method: 'DELETE',
            };
            return ajax.request(url, options);
        }
    }
</script>
<script>

    ajax.baseURL = 'http://localhost:8000'


    /**
     * &#26174;&#31034;&#34920;&#21333;&#21015;&#34920;
     * @returns {Promise<void>}
     */
    async function displayForms() {
        let formsList = document.getElementById('formsList');
        formsList.innerHTML = '';
        let result = await ajax.get('/dataset/');
        result.forEach(r => {
            let listItem = `
            <li>
                <label>${r.pid}
                <button class="export-button" onclick="exportDataset(${r.pid})">&#23548;&#20986;
                <button class="delete-button" onclick="deleteDataset(${r.pid})">X
                ${JSON.stringify(r.data, null, 4)}</script>
```

 `;

 formsList.insertAdjacentHTML('beforeend', listItem)  
 });  
 }

 /\*\*  
 \* 创建数据集  
 \*/  
 document.getElementById('createDataSet').addEventListener('submit', async (event) =&gt; {  
 event.preventDefault();  
 let formData = document.getElementById('formData').value.trim();  
 if (!formData) return  
 // 向服务端发起请求  
 await ajax.post('/dataset/ragas', {data: formData});  
 // // 向服务端发起请求  
 // await ajax.post('/dataset/chatglm', {data: formData});  
 // 刷新表单列表  
 await displayForms();  
 });

 /\*\*  
 \* 导出数据集  
 \* @param pid  
 \* @returns {Promise<void>}  
 \*/  
 async function exportDataset(pid) {</void>

 try {  
 // 通过 AJAX 请求获取数据压缩包  
 let response = await fetch(`<span class="katex math inline">{ajax.baseURL}/export-dataset/</span>{pid}`);

 // 检查响应状态码  
 if (!response.ok) {  
 throw new Error('导出数据失败');  
 }

 // 读取响应的数据流  
 let blob = await response.blob();

 // 创建一个链接元素以下载文件  
 let url = URL.createObjectURL(blob);  
 let a = document.createElement('a');  
 a.href = url;  
 // 设置下载的文件名为 data.zip  
 a.download = `data\_${pid}.zip`;  
 // 模拟点击链接以触发下载  
 a.click();  
 } catch (error) {  
 // 如果出现错误，则显示导出数据失败的警告  
 alert(error.message);  
 }  
 }

 /\*\*  
 \* 删除数据集  
 \* @param pid  
 \* @returns {Promise<void>}  
 \*/  
 async function deleteDataset(pid) {  
 try {  
 await fetch(`<span class="katex math inline">{ajax.baseURL}/dataset/</span>{pid}/`, {method: 'DELETE'});  
 await ajax.delete(`/dataset/${pid}/`);  
 await displayForms(); // 删除成功后刷新表单列表  
 } catch (error) {  
 alert('删除数据集失败：' + error.message);  
 }  
 }</void>

 // 初始化页面  
 displayForms();

后端代码
====

<div style="overflow:hidden; clear:both; width: 100%; height: 40px; position: relative;">- - - - - -

 <span style="position: absolute;top: 50%;left: 50%; transform: translate(-50%, -50%); background-color: white;">以下为隐藏内容</span> </div> ### index.html

```javascript



    <meta charset="UTF-8"></meta>
    <meta content="width=device-width, initial-scale=1.0" name="viewport"></meta>
    <title>表单管理</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f0f0f0;
            color: #333;
        }

        h1, h2 {
            margin-bottom: 10px;
            padding-left: 20px;
        }

        h1 {
            font-size: 24px;
        }

        h2 {
            font-size: 20px;
        }

        form {
            margin-bottom: 20px;
            padding: 0 20px;
        }

        label {
            display: block;
            margin-bottom: 5px;
        }

        textarea {
            width: calc(100% - 40px);
            padding: 10px;
            font-size: 16px;
        }

        input[type="submit"], button {
            padding: 10px 15px;
            font-size: 16px;
            cursor: pointer;
            background-color: #007bff;
            color: #fff;
            border: none;
            border-radius: 5px;
        }

        input[type="submit"]:hover, button:hover {
            background-color: #0056b3;
        }

        ul {
            list-style-type: none;
            padding: 0;
            padding-left: 20px;
        }

        li {
            margin-bottom: 10px;
            padding: 10px;
            background-color: #fff;
            border: 1px solid #ddd;
            border-radius: 5px;
        }

        li:last-child {
            margin-bottom: 0;
        }

        section {
            margin: 20px;
        }

        /* &#26679;&#24335;&#25353;&#38062; */
        .export-button {
            font-size: 12px; /* &#26356;&#25913;&#25353;&#38062;&#22823;&#23567; */
        }

        .delete-button {
            color: red; /* &#23558;&#21024;&#38500;&#25353;&#38062;&#39068;&#33394;&#26356;&#25913;&#20026;&#32418;&#33394; */
            font-size: 12px; /* &#23558;&#21024;&#38500;&#25353;&#38062;&#22823;&#23567;&#26356;&#25913;&#20026;&#19982;&#23548;&#20986;&#25353;&#38062;&#30456;&#21516; */
        }

        pre {
            background-color: #f3f0f0;
        }
    </style>



<header>
    <h1>构建数据集</h1>
</header>

<section>
    <h2>批量创建数据集</h2>
    <form id="createDataSet">
        <textarea cols="50" id="formData" name="formData" placeholder="question:法国的首都是什么？,
groundTruths:巴黎,
answer:巴黎,
contexts:巴黎是法国的首都。,

question:《哈利波特》的作者是谁？,
groundTruths:J.K.罗琳,
answer:J.K.罗琳,
contexts:J.K.罗琳写了《哈利波特》。,

question:水的沸点是多少？,
groundTruths:100度摄氏度,
answer:100度摄氏度,
contexts:水在海平面下沸腾的温度是100摄氏度。,
" rows="15"></textarea>
        <input type="submit" value="提交"></input>
    </form>
</section>

<section>
    <h2>表单列表</h2>
    <ul id="formsList"></ul>
</section>

<script>

    class ajax {
        static baseURL = '';

        /**
         * &#21457;&#36215;&#35831;&#27714;
         * @param url
         * @param options
         * @returns {Promise<any>}
         */
        static async request(url, options) {
            let response = await fetch(`<span class="katex math inline">{ajax.baseURL}{url}`, options);
            return response.json();
        }

        /**
         *
         * @param url
         * @returns {Promise<*>}
         */
        static async get(url) {
            return ajax.request(url, {});
        }

        /**
         *
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
            return ajax.request(url, options);
        }

        /**
         *
         * @param url
         * @returns {Promise<*>}
         */
        static async delete(url) {
            let options = {
                method: 'DELETE',
            };
            return ajax.request(url, options);
        }
    }
</script>
<script>

    ajax.baseURL = 'http://localhost:8000'


    /**
     * &#26174;&#31034;&#34920;&#21333;&#21015;&#34920;
     * @returns {Promise<void>}
     */
    async function displayForms() {
        let formsList = document.getElementById('formsList');
        formsList.innerHTML = '';
        let result = await ajax.get('/dataset/');
        result.forEach(r => {
            let listItem = `
            <li>
                <label>${r.pid}
                <button class="export-button" onclick="exportDataset(${r.pid})">&#23548;&#20986;
                <button class="delete-button" onclick="deleteDataset(${r.pid})">X
                ${JSON.stringify(r.data, null, 4)}</script>
```

 `;

 formsList.insertAdjacentHTML('beforeend', listItem)  
 });  
 }

 /\*\*  
 \* 创建数据集  
 \*/  
 document.getElementById('createDataSet').addEventListener('submit', async (event) =&gt; {  
 event.preventDefault();  
 let formData = document.getElementById('formData').value.trim();  
 if (!formData) return  
 // 向服务端发起请求  
 await ajax.post('/dataset/ragas', {data: formData});  
 // // 向服务端发起请求  
 // await ajax.post('/dataset/chatglm', {data: formData});  
 // 刷新表单列表  
 await displayForms();  
 });

 /\*\*  
 \* 导出数据集  
 \* @param pid  
 \* @returns {Promise<void>}  
 \*/  
 async function exportDataset(pid) {</void>

 try {  
 // 通过 AJAX 请求获取数据压缩包  
 let response = await fetch(`<span class="katex math inline">{ajax.baseURL}/export-dataset/</span>{pid}`);

 // 检查响应状态码  
 if (!response.ok) {  
 throw new Error('导出数据失败');  
 }

 // 读取响应的数据流  
 let blob = await response.blob();

 // 创建一个链接元素以下载文件  
 let url = URL.createObjectURL(blob);  
 let a = document.createElement('a');  
 a.href = url;  
 // 设置下载的文件名为 data.zip  
 a.download = `data\_${pid}.zip`;  
 // 模拟点击链接以触发下载  
 a.click();  
 } catch (error) {  
 // 如果出现错误，则显示导出数据失败的警告  
 alert(error.message);  
 }  
 }

 /\*\*  
 \* 删除数据集  
 \* @param pid  
 \* @returns {Promise<void>}  
 \*/  
 async function deleteDataset(pid) {  
 try {  
 await fetch(`<span class="katex math inline">{ajax.baseURL}/dataset/</span>{pid}/`, {method: 'DELETE'});  
 await ajax.delete(`/dataset/${pid}/`);  
 await displayForms(); // 删除成功后刷新表单列表  
 } catch (error) {  
 alert('删除数据集失败：' + error.message);  
 }  
 }</void>

 // 初始化页面  
 displayForms();

依赖
--

### requirements.txt

```txt
aiohttp==3.9.3
aiosignal==1.3.1
annotated-types==0.6.0
anyio==4.3.0
async-timeout==4.0.3
attrs==23.2.0
certifi==2024.2.2
charset-normalizer==3.3.2
click==8.1.7
colorama==0.4.6
datasets==2.18.0
dill==0.3.8
exceptiongroup==1.2.0
fastapi==0.110.0
filelock==3.13.3
frozenlist==1.4.1
fsspec==2024.2.0
h11==0.14.0
huggingface-hub==0.22.1
idna==3.6
multidict==6.0.5
multiprocess==0.70.16
numpy==1.26.4
packaging==24.0
pandas==2.2.1
pyarrow==15.0.2
pyarrow-hotfix==0.6
pydantic==2.6.4
pydantic_core==2.16.3
python-dateutil==2.9.0.post0
pytz==2024.1
PyYAML==6.0.1
requests==2.31.0
six==1.16.0
sniffio==1.3.1
starlette==0.36.3
tqdm==4.66.2
typing_extensions==4.10.0
tzdata==2024.1
urllib3==2.2.1
uvicorn==0.29.0
xxhash==3.4.1
yarl==1.9.4

```