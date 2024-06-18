---
title: "计算运行时间"
date: "2017-11-16"
categories: 
  - "node-js"
---

```javascript
var process = require('process');
var testRuntime = function (_function) {
    var startTime = process.hrtime();
    _function();
    var endTime = process.hrtime(startTime);
    // [秒, 纳秒]
    console.info('[秒, 纳秒]');
    console.info(endTime);
};
```
