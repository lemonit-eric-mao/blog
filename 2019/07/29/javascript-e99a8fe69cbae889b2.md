---
title: 'Javascript 随机色'
date: '2019-07-29T07:29:40+00:00'
status: publish
permalink: /2019/07/29/javascript-%e9%9a%8f%e6%9c%ba%e8%89%b2
author: 毛巳煜
excerpt: ''
type: post
id: 4975
category:
    - JavaScript
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
##### 使用 js 生成随机色

```javascript
document.body.style.color = `#${Math.floor(Math.random() * 0xffffff).toString(16)}`;

```