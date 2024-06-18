---
title: "Node.js_Redis集群调用"
date: "2017-11-16"
categories: 
  - "node-js"
---

```javascript
/* =-=-=-=-=-=-=-=-=-= 此文件是链接 redis 的配置文件 =-=-=-=-=-=-=-=-=-=-= */
// 使用 ioredis 进行Redi集群节点调用
var Redis = require('ioredis');
var cluster = new Redis.Cluster([
    {host: '10.32.156.123', port: 6380},
    {host: '10.32.156.123', port: 7380},
    {host: '10.32.156.167', port: 6380},
    {host: '10.32.156.167', port: 7380},
    {host: '10.32.156.168', port: 6380},
    {host: '10.32.156.168', port: 7380}
]);

cluster.on("connect", function () {
    console.info('redis 集群链接 SUCCESS!');
});

cluster.on("error", function (err) {
    if (err) throw 'Error =:|=====> ' + err;
});

```

```javascript
// 以下是: 测试获取多个节点中的key
cluster.get('dlfc:sys_code:marr_status', function (err, res) {
    if (err)
        console.error(err);
    console.info(res);
});
cluster.get('dlfc:sys_code:depositagr_status', function (err, res) {
    if (err)
        console.error(err);
    console.info(res);
});
cluster.get('dlfc:sys_code:deposit_gain_reason', function (err, res) {
    if (err)
        console.error(err);
    console.info(res);
});
```

```javascript
 // 查询单个节点的所有key
 cluster.keys('*', function (err, res) {
     if (err)
         console.error(err);
    console.info(res);
 });

// cluster.set('foo', 'bar');
```
