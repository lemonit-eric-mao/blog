---
title: 'DIV滚动条在底部; 将DIV变为可输入框'
date: '2017-11-16T16:41:35+00:00'
status: publish
permalink: /2017/11/16/div%e6%bb%9a%e5%8a%a8%e6%9d%a1%e5%9c%a8%e5%ba%95%e9%83%a8-%e5%b0%86div%e5%8f%98%e4%b8%ba%e5%8f%af%e8%be%93%e5%85%a5%e6%a1%86
author: 毛巳煜
excerpt: ''
type: post
id: 561
category:
    - 前端开发
tag: []
post_format: []
hestia_layout_select:
    - default
---
#### 在div中加入 **contenteditable** 属性，DIV将变为可输入框。

#### 在Body中的任意位置填写 **messageId.scrollTop = messageId.scrollHeight;** DIV的滚动条会一直保持在底部。

```
<pre data-language="HTML">```markup



    <meta charset="UTF-8"></meta>
    <title>Title</title>
    <style>
        .message {
            border: 1px solid #000;
            width: 30%;
            height: 60%;
            position: fixed;
            top: 16%;
            left: 65%;
            background-color: rgb(186, 216, 186);
            overflow: hidden;
            overflow-y: scroll;
        }
    </style>


<div class="message" contenteditable="" id="messageId"></div>
messageId.scrollTop = messageId.scrollHeight;



```
```