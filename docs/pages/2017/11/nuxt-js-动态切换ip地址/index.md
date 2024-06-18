---
title: "nuxt.js 动态切换IP地址"
date: "2017-11-16"
categories: 
  - "vue"
---

##### **问题： 在使用nuxt.js框架开发时，如果不明确指定 HOST 那么项目运行时，是以 Localhost 做为连接地址，如果这样除了本机以外，其它的机器是无法访问的，所以我使用了动态获取本机IP地址的方式来解决这个问题。**

##### **注意：Linux 系统获取时`os.hostname()`时， 在终端控制台上显示的是 自定义的hostname，你有可能看到的不是 IP地址，但在浏览器中显示的肯定是当前的本机地址所以不用担心取不到IP地址，这一点请注意。**

##### **baseURL.js**

```javascript
// Node.js内置操作系统模块
const os = require('os');
let baseURL = ''
// 服务端接口
const javaServerUrl = 'http://10.32.156.54:8080';
// // 测试服IP地址
// const testServerIP = 'http://10.32.156.54';
// // 生产服IP地址
// const prodServerIP = 'http://10.32.156.53';

// 本地开发
if (process.env.NODE_ENV === 'development') {
  baseURL = `http://${os.hostname()}:3000`;
} else if (process.env.NODE_ENV === 'production') {
  // 获取本机IP地址
  baseURL = `http://${os.hostname()}`;
}

module.exports = {javaServerUrl: javaServerUrl, baseURL: baseURL}
```

##### **package.json**

```json
"scripts": {
    "dev": "nuxt",
    "build": "nuxt build",
    "start": "HOST=10.32.156.54 PORT=80 nuxt start",
    "generate": "nuxt generate",
    "lint": "eslint --ext .js,.vue --ignore-path .gitignore .",
    "precommit": "npm run lint"
  }
```

##### **.vue文件**

```javascript
export default {
    mounted() {

      // 获取服务端数据
      axios.get(javaServerUrl + '/user/query').then((response) => {
        $nuxt.$emit('initDLMap', response.data);
      });

      // 获取本地 json数据
      axios.get(baseURL + '/user.json').then((response) => {
        $nuxt.$emit('initDLMap', response.data);
      });
}
```
