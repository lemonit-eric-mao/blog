---
title: "Node.js 获取当前主机IP地址"
date: "2020-09-23"
categories: 
  - "node-js"
---

###### 兼容不同操作系统，获取IP

```javascript
const os = require('os')

/**
 * 控制台输出ip地址
 */
const network = os.networkInterfaces();

let hostname;

switch (os.type()) {
    case 'Windows_NT':
        hostname = network[Object.keys(network)[0]][1].address;
        break;
    case 'Linux':
        hostname = network[Object.keys(network)[1]][0].address;
        break;
    default:
        hostname = 'localhost'
}

console.log('\033[32;1m%s\033[0m', '================ Server Start SUCCESS ================');
console.log('\033[32;1m访问地址:\033[0m \033[34;1m%s\033[0m', `http://${hostname}`);
```
