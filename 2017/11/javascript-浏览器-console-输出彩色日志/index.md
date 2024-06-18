---
title: "JavaScript 浏览器 Console 输出彩色日志"
date: "2017-11-16"
categories: 
  - "javascript"
---

### Logger.js

```javascript
/**
 * Created by mao_siyu on 2017/9/10.
 */
var Logger = {
    level: 1,
    debug: function (message) {
        if (this.level <= 1)
            console.log('%c ' + message, 'font-size:12px;color:rgba(65,105,225,255)');
    },
    info: function (message) {
        if (this.level <= 2)
            console.log('%c ' + message, 'font-size:12px;color:rgba(60,179,113,255)');
    },
    warn: function (message) {
        if (this.level <= 3)
            console.log('%c ' + message, 'font-size:12px;color:rgba(218,165,32,255)');
    },
    error: function (message) {
        if (this.level <= 4)
            console.log('%c ' + message, 'font-size:12px;color:rgba(255,0,0,255)');
    },
};
```
