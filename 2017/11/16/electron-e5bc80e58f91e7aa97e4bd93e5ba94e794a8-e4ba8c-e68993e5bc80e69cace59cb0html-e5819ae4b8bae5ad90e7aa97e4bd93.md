---
title: 'electron 开发窗体应用 (二) 打开本地html 做为子窗体'
date: '2017-11-16T12:44:13+00:00'
status: publish
permalink: /2017/11/16/electron-%e5%bc%80%e5%8f%91%e7%aa%97%e4%bd%93%e5%ba%94%e7%94%a8-%e4%ba%8c-%e6%89%93%e5%bc%80%e6%9c%ac%e5%9c%b0html-%e5%81%9a%e4%b8%ba%e5%ad%90%e7%aa%97%e4%bd%93
author: 毛巳煜
excerpt: ''
type: post
id: 201
category:
    - Electron
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
##### main.js

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
    var url = path.join('file://', __dirname, '/index.html');
    // 可以是本地的html 也可以是 http://www.baidu.com
    mainWindow.loadURL(url);

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

##### index.html

```javascript



    <meta charset="UTF-8"></meta>
    <title>Electron DOM webview 标签</title>
    <style>
        .foo {
            width: 100%;
            line-height: 100%;
            height: 712px;
        }

        .indicator {
            position: fixed;
            top: 50%;
            width: 100%;
            height: 100%;
            text-align: center;
            font-size: 60px;
        }
    </style>


<webview class="foo" id="foo" src="https://www.baidu.com/"></webview>
<div class="indicator"></div>
<script>
    onload = function () {
        var webview = document.getElementById('foo');
        var indicator = document.querySelector('.indicator');

        webview.addEventListener("did-start-loading", () => {
            indicator.innerText = "Loading...";
        });
        webview.addEventListener("did-stop-loading", () => {
            indicator.innerText = "";
        });
    }
</script>



```