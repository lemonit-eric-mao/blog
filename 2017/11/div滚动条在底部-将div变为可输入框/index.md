---
title: "DIV滚动条在底部; 将DIV变为可输入框"
date: "2017-11-16"
categories: 
  - "前端开发"
---

#### 在div中加入 **contenteditable** 属性，DIV将变为可输入框。

#### 在Body中的任意位置填写 **messageId.scrollTop = messageId.scrollHeight;** DIV的滚动条会一直保持在底部。

```markup
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
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
</head>
<body>
<div class="message" id="messageId" contenteditable></div>
messageId.scrollTop = messageId.scrollHeight;
</body>
</html>
```
