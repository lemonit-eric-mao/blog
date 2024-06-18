---
title: 'JavaScript 浏览器 Console 输出彩色日志'
date: '2017-11-16T10:13:55+00:00'
status: publish
permalink: /2017/11/16/javascript-%e6%b5%8f%e8%a7%88%e5%99%a8-console-%e8%be%93%e5%87%ba%e5%bd%a9%e8%89%b2%e6%97%a5%e5%bf%97
author: 毛巳煜
excerpt: ''
type: post
id: 80
category:
    - JavaScript
tag: []
post_format: []
hestia_layout_select:
    - default
---
### Logger.js

```
<pre class="line-numbers prism-highlight" data-start="1">```javascript
/**
 * Created by mao_siyu on 2017/9/10.
 */
var Logger = {
    level: 1,
    debug: function (message) {
        if (this.level 
```
```