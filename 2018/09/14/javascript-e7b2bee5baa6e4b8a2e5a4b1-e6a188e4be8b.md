---
title: 'Javascript 精度丢失 案例'
date: '2018-09-14T10:20:22+00:00'
status: publish
permalink: /2018/09/14/javascript-%e7%b2%be%e5%ba%a6%e4%b8%a2%e5%a4%b1-%e6%a1%88%e4%be%8b
author: 毛巳煜
excerpt: ''
type: post
id: 2364
category:
    - JavaScript
tag: []
post_format: []
---
#### 精度丢失经典案例

```javascript
mao-siyu@pc:~$ node
> 0.1 + 0.2
0.30000000000000004
>

```

```javascript
> (0.1+0.2).toFixed(1)
'0.3'
>

```