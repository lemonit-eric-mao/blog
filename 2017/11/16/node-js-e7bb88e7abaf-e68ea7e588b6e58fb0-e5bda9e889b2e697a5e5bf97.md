---
title: 'Node.js 终端 控制台 彩色日志'
date: '2017-11-16T12:33:55+00:00'
status: publish
permalink: /2017/11/16/node-js-%e7%bb%88%e7%ab%af-%e6%8e%a7%e5%88%b6%e5%8f%b0-%e5%bd%a9%e8%89%b2%e6%97%a5%e5%bf%97
author: 毛巳煜
excerpt: ''
type: post
id: 180
category:
    - node.js
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
###### 创建工具类

```javascript
const ColorLog = () => {
};

ColorLog.red = (msg) => {
    console.log('\033[31;1m  %s  \033[0m', msg);
}
ColorLog.green = (msg) => {
    console.log('\033[32;1m  %s  \033[0m', msg);
}
ColorLog.yellow = (msg) => {
    console.log('\033[33;1m  %s  \033[0m', msg);
}
ColorLog.blue = (msg) => {
    console.log('\033[34;1m  %s  \033[0m', msg);
}
ColorLog.purple = (msg) => {
    console.log('\033[35;1m  %s  \033[0m', msg);
}
ColorLog.young = (msg) => {
    console.log('\033[36;1m  %s  \033[0m', msg);
}

exports.ColorLog = ColorLog;


```

- - - - - -

###### 测试

```javascript
ColorLog.red('颜色！');
ColorLog.green('颜色！');
ColorLog.yellow('颜色！');
ColorLog.blue('颜色！');
ColorLog.purple('颜色！');
ColorLog.young('颜色！');

```

![](http://qiniu.dev-share.top/color.png)
-----------------------------------------

- - - - - -

- - - - - -