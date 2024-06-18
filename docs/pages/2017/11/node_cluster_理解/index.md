---
title: "Node_Cluster_理解"
date: "2017-11-16"
categories: 
  - "node-js"
---

```javascript
var cluster = require('cluster');
var http = require('http');
var numCPUs = require('os').cpus().length;

// cluster.isMaster 判断是不是master节点
if (cluster.isMaster) {
    console.log('[master] ' + "start master...");

    for (var i = 0; i < numCPUs; i++) {
        cluster.fork();
    }

    cluster.on('listening', function (worker, address) {
        console.log('[master] ' + 'listening: worker' + worker.id + ',pid:' + worker.process.pid + ', Address:' + address.address + ":" + address.port);
    });

    // cluster.isWorker 判断是不是worker节点
} else if (cluster.isWorker) {
    console.log('[worker] ' + "start worker ..." + cluster.worker.id);
    http.createServer(function (req, res) {
        console.log('worker' + cluster.worker.id);
        res.end('worker' + cluster.worker.id + ',PID:' + process.pid);
    }).listen(8080);
}
```
