---
title: 'JavaScript 滚动条 自动运行'
date: '2018-01-29T15:40:25+00:00'
status: publish
permalink: /2018/01/29/javascript-%e6%bb%9a%e5%8a%a8%e6%9d%a1-%e8%87%aa%e5%8a%a8%e8%bf%90%e8%a1%8c
author: 毛巳煜
excerpt: ''
type: post
id: 1903
category:
    - JavaScript
tag: []
post_format: []
hestia_layout_select:
    - default
---
### 写爬虫时经常遇到懒加载的网站, 所以需要先加载完所有页面数据.

```
<pre class="line-numbers prism-highlight" data-start="1">```javascript
var intervalId = setInterval(() => {
    let scrollTop = document.documentElement.scrollTop += 1000;
    let scrollHeight = document.documentElement.scrollHeight;

    if(scrollTop >= scrollHeight) {
        window.clearInterval(intervalId);
        console.log('======到底了!======');
    }
}, 1000);

```
```