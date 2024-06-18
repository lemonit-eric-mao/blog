---
title: 'Javascript 获取彩票号码'
date: '2019-11-13T13:55:54+00:00'
status: private
permalink: /2019/11/13/javascript-%e8%8e%b7%e5%8f%96%e5%bd%a9%e7%a5%a8%e5%8f%b7%e7%a0%81
author: 毛巳煜
excerpt: ''
type: post
id: 5125
category:
    - JavaScript
tag: []
post_format: []
---
[双色球走势图](http://zst.aicai.com/ssq/ "双色球走势图")  
这个网址的走势图比较简单，因为它没有分页好抓取

```javascript
var trs = document.querySelectorAll('#tdata > tr');
var rows = [];
for (let i = 0, len = trs.length; i 
```