---
title: 'Electron 中，为什么不能用 jQuery、RequireJS、Meteor、AngularJS？'
date: '2017-11-16T12:45:32+00:00'
status: publish
permalink: /2017/11/16/electron-%e4%b8%ad%ef%bc%8c%e4%b8%ba%e4%bb%80%e4%b9%88%e4%b8%8d%e8%83%bd%e7%94%a8-jquery%e3%80%81requirejs%e3%80%81meteor%e3%80%81angularjs%ef%bc%9f
author: 毛巳煜
excerpt: ''
type: post
id: 205
category:
    - Electron
tag: []
post_format: []
---
###### 因为 Electron 在运行环境中引入了 Node.js，所以在 DOM 中有一些额外的变量，比如 module、exports和 require。这导致 了许多库不能正常运行，因为它们也需要将同名的变量加入运行环境中。

###### **我们可以通过禁用 Node.js 来解决这个问题，用如下的方式：**

```javascript
// 在主进程中
var mainWindow = new BrowserWindow({
  webPreferences: {
    nodeIntegration: false
  }
});

```

[w3cschool中有详细说明](http://www.w3cschool.cn/electronmanual/electronmanual-electron-faq.html "w3cschool中有详细说明")