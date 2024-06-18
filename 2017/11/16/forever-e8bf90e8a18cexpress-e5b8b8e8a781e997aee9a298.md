---
title: 'forever 运行express 常见问题'
date: '2017-11-16T12:29:01+00:00'
status: publish
permalink: /2017/11/16/forever-%e8%bf%90%e8%a1%8cexpress-%e5%b8%b8%e8%a7%81%e9%97%ae%e9%a2%98
author: 毛巳煜
excerpt: ''
type: post
id: 170
category:
    - node.js
tag: []
post_format: []
---
### **问题**：

使用 express 搭建的项目 为什么执行 forever start app.js 后查看进程列表，显示程序已经运行，但是怎么也访问不到？

### **原因**

首先要注意 express 项目的启动方式 node ./bin/www 而不是 node app.js，所以 forever start app.js 执行的是app.js文件， 相当于执行 node app.js，所以会访问不到。

### **解决**

改为 forever start ./bin/www 启动结果执行成功后可以正常访问。