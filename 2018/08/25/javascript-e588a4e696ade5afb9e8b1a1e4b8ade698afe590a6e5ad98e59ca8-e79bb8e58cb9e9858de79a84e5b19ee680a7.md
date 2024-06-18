---
title: 'JavaScript 判断对象中是否存在 相匹配的属性'
date: '2018-08-25T10:16:48+00:00'
status: publish
permalink: /2018/08/25/javascript-%e5%88%a4%e6%96%ad%e5%af%b9%e8%b1%a1%e4%b8%ad%e6%98%af%e5%90%a6%e5%ad%98%e5%9c%a8-%e7%9b%b8%e5%8c%b9%e9%85%8d%e7%9a%84%e5%b1%9e%e6%80%a7
author: 毛巳煜
excerpt: ''
type: post
id: 2286
category:
    - JavaScript
tag: []
post_format: []
hestia_layout_select:
    - default
---
#### 判断对象中是否存在 相匹配的属性

```javascript
var errorMsg =  {
    '400': '用户名或密码不存在!',
    '401': '用户名或密码不存在!'
}

errorMsg.hasOwnProperty(401);
true
errorMsg.hasOwnProperty(402);
false

401 in errorMsg
true
402 in errorMsg
false

```