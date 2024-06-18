---
title: Node_Cluster_理解
date: '2017-11-16T12:21:21+00:00'
status: publish
permalink: /2017/11/16/node_cluster_%e7%90%86%e8%a7%a3
author: 毛巳煜
excerpt: ''
type: post
id: 155
category:
    - node.js
tag: []
post_format: []
hestia_layout_select:
    - default
---
```javascript
var cluster = require('cluster');
var http = require('http');
var numCPUs = require('os').cpus().length;

// cluster.isMaster 判断是不是master节点
if (cluster.isMaster) {
    console.log('[master] ' + "start master...");

    for (var i = 0; i 
```