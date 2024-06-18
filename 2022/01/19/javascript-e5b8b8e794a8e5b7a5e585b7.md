---
title: 'JavaScript 常用工具'
date: '2022-01-19T01:36:42+00:00'
status: private
permalink: /2022/01/19/javascript-%e5%b8%b8%e7%94%a8%e5%b7%a5%e5%85%b7
author: 毛巳煜
excerpt: ''
type: post
id: 8252
category:
    - JavaScript
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
wb_sst_seo:
    - 'a:3:{i:0;s:0:"";i:1;s:0:"";i:2;s:0:"";}'
---
### 打字机效果

```javascript



    <meta charset="UTF-8"></meta>
    <meta content="width=device-width, initial-scale=1.0" name="viewport"></meta>
    <title>Typewriter Effect</title>
    <style>
        #output {
            overflow: hidden;
            white-space: nowrap;
            border-right: 1px solid #000;
        }
    </style>


<div id="output"></div>

<script>
    // &#33719;&#21462;&#35201;&#36755;&#20986;&#30340;&#20803;&#32032;
    let outputElement = document.getElementById("output");
    async function typeText() {
        // &#35774;&#32622;&#35201;&#25171;&#21360;&#30340;&#25991;&#26412;&#20869;&#23481;
        let message = `<div style="color: green">&#36825;&#26159;&#19968;&#20010;&#25171;&#23383;&#26426;&#25928;&#26524;&#30340;&#31034;&#20363;<div style="color: red">, &#35753;&#25991;&#26412;&#19968;&#20010;&#23383;&#31526;&#19968;&#20010;&#23383;&#31526;&#22320;&#26174;&#31034;&#12290;`;
        // &#23558;&#25991;&#26412;&#23383;&#31526;&#20018;&#36716;&#20026;&#21333;&#20010;&#23383;&#31526;&#25968;&#32452;
        let chars = message.split('');

        while (chars.length) {
            // &#23558;&#24403;&#21069;&#23383;&#31526;&#28155;&#21152;&#21040;&#36755;&#20986;&#20803;&#32032;(&#36755;&#20986;&#30340;&#20803;&#32032;&#20026;&#23383;&#31526;&#20018;)
            outputElement.textContent += chars.shift();
            // &#20351;&#29992;Promise&#21644;setTimeout&#31561;&#24453;&#19968;&#27573;&#26102;&#38388;; 10&#27627;&#31186;&#24310;&#36831;
            await new Promise(resolve => setTimeout(resolve, 10));
        }
        // &#23558;&#23383;&#31526;&#20018;&#20803;&#32032;&#20174;&#26032;&#28210;&#26579;&#20026; Dom
        outputElement.innerHTML = outputElement.textContent;
    }

    // &#39029;&#38754;&#21152;&#36733;&#21518;&#24320;&#22987;&#25171;&#23383;&#25928;&#26524;
    window.onload = typeText;
</script>




```

- - - - - -

#### 打字机输出 DOM

```
<pre data-language="HTML">```markup



    <meta charset="UTF-8"></meta>
    <meta content="width=device-width, initial-scale=1.0" name="viewport"></meta>
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

    
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>

    
    <link href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.3.1/styles/default.min.css" rel="stylesheet"></link>
    
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.3.1/highlight.min.js"></script>



<div id="output"></div>

<script>
    // &#33719;&#21462;&#35201;&#36755;&#20986;&#30340;&#20803;&#32032;
    let outputElement = document.getElementById("output");

    async function Render() {
        // &#35774;&#32622;&#35201;&#25171;&#21360;&#30340;&#20195;&#30721;&#22359;&#20869;&#23481;
        let code = "### &#25105;&#21487;&#20197;&#24110;&#24744;&#20889;&#19968;&#20010;&#31616;&#21333;&#30340;HTML&#39029;&#38754;&#12290;&#20197;&#19979;&#26159;&#19968;&#20010;&#31034;&#20363;&#65306;\n\n\n```html\n\u003c!DOCTYPE html\u003e\n\u003chtml\u003e\n  \u003chead\u003e\n    \u003ctitle\u003e&#25105;&#30340;&#32593;&#39029;\u003c/title\u003e\n    \u003cmeta charset=\"UTF-8\"\u003e\n    \u003cmeta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\"\u003e\n  \u003c/head\u003e\n  \u003cbody\u003e\n    \u003ch1\u003e&#27426;&#36814;&#26469;&#21040;&#25105;&#30340;&#32593;&#39029;&#65281;\u003c/h1\u003e\n    \u003cp\u003e&#36825;&#26159;&#19968;&#20010;&#31616;&#21333;&#30340;HTML&#39029;&#38754;&#65292;&#29992;&#20110;&#23637;&#31034;&#19968;&#20123;&#22522;&#26412;&#30340;HTML&#20803;&#32032;&#12290;\u003c/p\u003e\n    \u003cimg src=\"example.jpg\" alt=\"&#31034;&#20363;&#22270;&#29255;\"\u003e\n  \u003c/body\u003e\n\u003c/html\u003e\n```\n&#36825;&#20010;&#31034;&#20363;&#21253;&#25324;&#19968;&#20010;&#26631;&#39064;&#12289;&#19968;&#27573;&#25991;&#23383;&#21644;&#19968;&#20010;&#22270;&#29255;&#12290;&#24744;&#21487;&#20197;&#23558;&#36825;&#20123;&#20803;&#32032;&#22797;&#21046;&#21040;&#20219;&#20309;&#25991;&#26412;&#32534;&#36753;&#22120;&#20013;&#65292;&#28982;&#21518;&#23558;&#25991;&#20214;&#20445;&#23384;&#20026;.html&#25991;&#20214;&#65292;&#28982;&#21518;&#29992;&#20219;&#20309;&#25903;&#25345;HTML&#30340;&#27983;&#35272;&#22120;&#25171;&#24320;&#23427;&#12290;";
        //
        let codeChars = code.split('');
        // &#24490;&#29615;&#21462;&#20986;&#23383;&#31526;
        while (codeChars.length) {
            // &#21462;&#20986;&#23383;&#31526;
            let char = codeChars.shift();

            // &#23558;&#23383;&#31526;&#28155;&#21152;&#21040;&#36755;&#20986;&#20803;&#32032;
            outputElement.textContent += char;

            // &#20351;&#29992;Promise&#21644;setTimeout&#31561;&#24453;&#19968;&#27573;&#26102;&#38388;; 10&#27627;&#31186;&#24310;&#36831;
            await new Promise(resolve => setTimeout(resolve, 10));
        }

        // &#36716;&#25442;Markdown
        outputElement.innerHTML = marked.parse(outputElement.textContent);

        // &#20351;&#29992;Highlight.js&#23545;&#36755;&#20986;&#20803;&#32032;&#36827;&#34892;&#39640;&#20142;&#22788;&#29702;
        let codes = outputElement.getElementsByTagName('code');
        for (let code of codes) {
            hljs.highlightElement(code);
        }
    }

    // &#39029;&#38754;&#21152;&#36733;&#21518;&#24320;&#22987;&#25171;&#23383;&#25928;&#26524;
    window.onload = Render;

</script>




```
```

- - - - - -

- - - - - -

- - - - - -

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

- - - - - -

### insertAdjacentHTML

> **insertAdjacentHTML** 是 JavaScript 中用于在指定的位置插入 HTML 内容的方法。  
>  它可以用于修改 DOM（文档对象模型）中的元素结构，动态地添加、修改或删除 HTML 内容。  
>  insertAdjacentHTML 方法可以在元素的四个位置进行插入操作：
> 
> - **beforebegin**: 在元素前插入 HTML 内容。
> - **afterbegin**: 在元素内部的开头插入 HTML 内容。
> - **beforeend**: 在元素内部的末尾插入 HTML 内容。
> - **afterend**: 在元素后插入 HTML 内容。

```javascript



    <title>薄荷</title>
    <meta charset="UTF-8"></meta>



<div class="panel"></div>


<script>

    /**
     * 1. &#21019;&#24314;Item
     * @returns {HTMLDivElement}
     */
    function createItem() {
        // 1. &#33719;&#21462;DOM&#20803;&#32032;
        let panel = document.querySelector('.panel');
        // 2. &#32534;&#20889;&#26032;&#30340;&#23436;&#25972;DOM
        let container = `
            <div class="container">
                <div class="items">&#34180;&#33655;&#12289;&#34180;&#33655;
            
        `;
        // 3. &#23558;&#26032;DOM&#25554;&#20837;&#21040;panel
        //    &#36825;&#26679;&#20570;&#30340;&#22909;&#22788;&#23601;&#26159;&#19981;&#38656;&#35201;&#20351;&#29992; document.createElement() &#20877;&#21019;&#24314;&#19968;&#20010;&#26032;DOM
        panel.insertAdjacentHTML('beforeend',container)
    }
    createItem()
</script>




```

- - - - - -