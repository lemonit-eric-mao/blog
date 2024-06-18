---
title: "JavaScript 常用工具"
date: "2022-01-19"
categories: 
  - "javascript"
---

### 打字机效果

```javascript
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Typewriter Effect</title>
    <style>
        #output {
            overflow: hidden;
            white-space: nowrap;
            border-right: 1px solid #000;
        }
    </style>
</head>
<body>
<div id="output"></div>

<script>
    // 获取要输出的元素
    let outputElement = document.getElementById("output");
    async function typeText() {
        // 设置要打印的文本内容
        let message = `<div style="color: green">这是一个打字机效果的示例</div><div style="color: red">, 让文本一个字符一个字符地显示。</div>`;
        // 将文本字符串转为单个字符数组
        let chars = message.split('');

        while (chars.length) {
            // 将当前字符添加到输出元素(输出的元素为字符串)
            outputElement.textContent += chars.shift();
            // 使用Promise和setTimeout等待一段时间; 10毫秒延迟
            await new Promise(resolve => setTimeout(resolve, 10));
        }
        // 将字符串元素从新渲染为 Dom
        outputElement.innerHTML = outputElement.textContent;
    }

    // 页面加载后开始打字效果
    window.onload = typeText;
</script>
</body>
</html>

```

* * *

#### 打字机输出 DOM

```markup
<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Typewriter Effect with Code Highlighting</title>
    <style>
        #output {
            overflow: hidden;
            white-space: pre;
            font-family: "Courier New", monospace;
            background-color: #f4f4f4;
            padding: 10px;
            border: 1px solid #ccc;
            margin-top: 20px;
            font-size: 18px;
        }
    </style>

    <!-- 引入 marked.js 库 转换Markdown -->
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>

    <!-- 引入 Highlight.js 样式表 -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.3.1/styles/default.min.css">
    <!-- 引入 Highlight.js 库 -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.3.1/highlight.min.js"></script>

</head>
<body>
<div id="output"></div>

<script>
    // 获取要输出的元素
    let outputElement = document.getElementById("output");

    async function Render() {
        // 设置要打印的代码块内容
        let code = "### 我可以帮您写一个简单的HTML页面。以下是一个示例：\n\n\n```html\n\u003c!DOCTYPE html\u003e\n\u003chtml\u003e\n  \u003chead\u003e\n    \u003ctitle\u003e我的网页\u003c/title\u003e\n    \u003cmeta charset=\"UTF-8\"\u003e\n    \u003cmeta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\"\u003e\n  \u003c/head\u003e\n  \u003cbody\u003e\n    \u003ch1\u003e欢迎来到我的网页！\u003c/h1\u003e\n    \u003cp\u003e这是一个简单的HTML页面，用于展示一些基本的HTML元素。\u003c/p\u003e\n    \u003cimg src=\"example.jpg\" alt=\"示例图片\"\u003e\n  \u003c/body\u003e\n\u003c/html\u003e\n```\n这个示例包括一个标题、一段文字和一个图片。您可以将这些元素复制到任何文本编辑器中，然后将文件保存为.html文件，然后用任何支持HTML的浏览器打开它。";
        //
        let codeChars = code.split('');
        // 循环取出字符
        while (codeChars.length) {
            // 取出字符
            let char = codeChars.shift();

            // 将字符添加到输出元素
            outputElement.textContent += char;

            // 使用Promise和setTimeout等待一段时间; 10毫秒延迟
            await new Promise(resolve => setTimeout(resolve, 10));
        }

        // 转换Markdown
        outputElement.innerHTML = marked.parse(outputElement.textContent);

        // 使用Highlight.js对输出元素进行高亮处理
        let codes = outputElement.getElementsByTagName('code');
        for (let code of codes) {
            hljs.highlightElement(code);
        }
    }

    // 页面加载后开始打字效果
    window.onload = Render;

</script>

</body>
</html>
```

* * *

* * *

* * *

### 拦截浏览器按键

```javascript
/**
 * 拦截Ctrl + s 事件
 */
document.addEventListener('keydown', (event) => {
    // event.ctrlKey 的作用：判断是否按下组合键 Ctrl
    if (event.ctrlKey && event.key === 's') {
        // 阻止事件冒泡
        event.preventDefault()
        // 你的代码
        // save()
    }
});

```

* * *

### insertAdjacentHTML

> **insertAdjacentHTML** 是 JavaScript 中用于在指定的位置插入 HTML 内容的方法。 它可以用于修改 DOM（文档对象模型）中的元素结构，动态地添加、修改或删除 HTML 内容。 insertAdjacentHTML 方法可以在元素的四个位置进行插入操作：
> 
> - **beforebegin**: 在元素前插入 HTML 内容。
> - **afterbegin**: 在元素内部的开头插入 HTML 内容。
> - **beforeend**: 在元素内部的末尾插入 HTML 内容。
> - **afterend**: 在元素后插入 HTML 内容。

```javascript
<!DOCTYPE html>
<html lang="zh">
<head>
    <title>薄荷</title>
    <meta charset="UTF-8">
<body>

<!--面板页-->
<div class="panel"></div>

<!--1. 创建Item-->
<script>

    /**
     * 1. 创建Item
     * @returns {HTMLDivElement}
     */
    function createItem() {
        // 1. 获取DOM元素
        let panel = document.querySelector('.panel');
        // 2. 编写新的完整DOM
        let container = `
            <div class="container">
                <div class="items">薄荷、薄荷</div>
            </div>
        `;
        // 3. 将新DOM插入到panel
        //    这样做的好处就是不需要使用 document.createElement() 再创建一个新DOM
        panel.insertAdjacentHTML('beforeend',container)
    }
    createItem()
</script>

</body>
</html>
```

* * *
