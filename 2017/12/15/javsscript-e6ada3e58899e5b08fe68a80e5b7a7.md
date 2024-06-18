---
title: 'JavsScript 正则小技巧'
date: '2017-12-15T16:47:36+00:00'
status: publish
permalink: /2017/12/15/javsscript-%e6%ad%a3%e5%88%99%e5%b0%8f%e6%8a%80%e5%b7%a7
author: 毛巳煜
excerpt: ''
type: post
id: 1758
category:
    - JavaScript
tag: []
post_format: []
---
### 在每一位字符后面添加一个回车

```
<pre class="line-numbers prism-highlight" data-start="1">```javascript
var str = '甘井子区';
str.replace(/(.{1})/g,'$1\n');
"甘
井
子
区
"

```
```