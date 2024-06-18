---
title: 'JavaScript 将表单元素转成JSON'
date: '2017-11-16T10:12:49+00:00'
status: publish
permalink: /2017/11/16/javascript-%e5%b0%86%e8%a1%a8%e5%8d%95%e5%85%83%e7%b4%a0%e8%bd%ac%e6%88%90json
author: 毛巳煜
excerpt: ''
type: post
id: 76
category:
    - JavaScript
tag: []
post_format: []
hestia_layout_select:
    - default
---
```javascript
// 获取所有表单数据
var formElement = document.querySelectorAll('div>input');
// 将表单元素添加到JSON
var param = {};

for (var i = 0; i 
```