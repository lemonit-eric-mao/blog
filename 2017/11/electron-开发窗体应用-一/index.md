---
title: "electron 开发窗体应用 (一)"
date: "2017-11-16"
categories: 
  - "electron"
---

- 开发环境: ubuntu 16
- 开发工具: webstorm
- ECMAScript: 6

* * *

###### package.json

```json
{
  "name": "electron-exercise",
  "version": "1.0.0",
  "description": "",
  "main": "main.js",
  "scripts": {
    "start": "electron .",
    "debug": "electron --debug=5858 .",
    "sandbox": "electron . --enable-sandbox"
  },
  "author": "",
  "license": "ISC",
  "dependencies": {
    "electron-prebuilt": "^1.4.13"
  }
}
```

* * *

###### **以下代码执行就可以打开一个窗体** main.js

```javascript
'use strict';
const path = require('path');
const electron = require('electron');
// 控制应用生命周期的模块。
const app = electron.app;
// 创建原生浏览器窗口的模块
const BrowserWindow = electron.BrowserWindow;

// 保持一个对于 window 对象的全局引用，不然，当 JavaScript 被 GC，
// window 会被自动地关闭
var mainWindow = null;
/**
 * 当所有窗口被关闭了，退出。
 */
app.on('window-all-closed', () => {
    // 在 OS X 上，通常用户在明确地按下 Cmd + Q 之前
    // 应用会保持活动状态
    if (process.platform != 'darwin') {
        app.quit();
        console.info('所有窗口关闭');
    }
});

// 当 Electron 完成了初始化并且准备创建浏览器窗口的时候
// 这个方法就被调用
app.on('ready', () => {
    mainWindow = new BrowserWindow({
        width: 1024,
        height: 712,
        center: true,
        resizable: true
    });

    // 加载应用的 webview.html
    var url = path.join('file://', __dirname, '/html/index.html');
    // 可以是本地的html 也可以是 http://www.baidu.com
    mainWindow.loadURL('http://www.baidu.com');

    // 打开开发工具
    mainWindow.openDevTools();

    /**
     * 当前 window 被关闭，这个事件会被发出
     */
    mainWindow.on('closed', () => {
        // 取消引用 window 对象，如果你的应用支持多窗口的话，
        // 通常会把多个 window 对象存放在一个数组里面，
        // 但这次不是。
        mainWindow = null;
        console.info('窗口关闭');
    });

});
```
