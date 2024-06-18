---
title: Node_Bagpipe_理解
date: '2017-11-16T12:22:29+00:00'
status: publish
permalink: /2017/11/16/node_bagpipe_%e7%90%86%e8%a7%a3
author: 毛巳煜
excerpt: ''
type: post
id: 159
category:
    - node.js
tag: []
post_format: []
hestia_layout_select:
    - default
---
```javascript
/**
 * Created by mao-siyu on 16-10-30.
 */
 /**
  * 随便自定义函数
  */
 var async = function (callback) {
         callback(null, 'success!');
 }
var Bagpipe = require('bagpipe');
//  最大并发数为10
 var bagpipe = new Bagpipe(10);
//  监听如果超出最大并发数 (按照当前的限制,就会有30个并发请求被挡在了外面)
 bagpipe.on('full', function (length) {
     console.warn('底层系统处理不能及时完成,队列拥堵,目前队列长度为: ' + length);
 });

 for (var i = 0; i 
```

```javascript
// 在拒绝模式下,如果等待的调用队列也満他之后,新来的调用就直接反给它一个队列太忙的拒绝异常;
// 最大并发数为20 + 拒绝模式
 var bagpipe = new Bagpipe(20, {
     refuse: true
 });
 for (var i = 0; i 
```

```javascript
/**
 * 随便自定义函数
 */
var async = function (param1, param2, callback) {
    callback(null, param1 + param2);
}

// 最大并发数为20 + 超时控制
var bagpipe = new Bagpipe(20, {
    timeout: 1000
});
for (var i = 0; i ' + err);
        else
            console.info('callback:=====>' + callback);
    });
}

```