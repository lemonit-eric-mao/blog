---
title: Node_通过Promise对象理解_Promise异步编程模式_2
date: '2017-11-16T10:58:46+00:00'
status: publish
permalink: /2017/11/16/node_%e9%80%9a%e8%bf%87promise%e5%af%b9%e8%b1%a1%e7%90%86%e8%a7%a3_promise%e5%bc%82%e6%ad%a5%e7%bc%96%e7%a8%8b%e6%a8%a1%e5%bc%8f_2
author: 毛巳煜
excerpt: ''
type: post
id: 101
category:
    - node.js
tag: []
post_format: []
hestia_layout_select:
    - default
---
#### 理解 resolve, reject

```javascript
var pms1 = function () {
    return new Promise(function (resolve, reject) {
        setTimeout(function () {
            // 生成1-10的随机数
            var num = Math.ceil(Math.random() * 10);
            if (num 
```