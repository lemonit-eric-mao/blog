---
title: "electron 数据抓取 控制管理软件 (一)"
date: "2017-11-16"
categories: 
  - "electron"
---

**数据抓取项目, 目前第一版主要以开发人员自己编写脚本, 自己开发定制任务流程, 编写好的脚本会保存在 localStorage 中, 以网站的hostname 做为key, 相同的网站页面渲染成功后会自动载入脚本.**

**项目的最终版理想状态是 可以通过界面 自由的配置任务 , 自由设置循环执行次数 , 自由配置多数据源, 配置任务只要鼠标在网页上点一点, 就可以自动生成任务脚本. 一键获取数据, 可以实时查看数据采集 任务状态, 随时暂停 | 终止 任务**

###### 工具类 RemoteBaseWindow.js

```javascript
/**
 * Created by mao_siyu on 2017/4/21.
 */
const electron = require('electron');
const BrowserWindow = electron.remote.BrowserWindow;

var BaseWindow = function () {
}

BaseWindow.open = function (options, callback) {
    options = options || {};
    // 新建一个窗体
    var manageWindow = new BrowserWindow({
        webPreferences: {
            // nodeIntegration: false 禁用子窗体使用 node.js功能
            nodeIntegration: options.nodeIntegration
        },
        show: false,
    });
    /**
     * 当窗口已经关闭的时候触发
     */
    manageWindow.on('closed', () => {
        // 删除对已经关闭的窗口的引用对象和避免再次使用它
        manageWindow = null;
    });
    manageWindow.loadURL(options.url);
    // manageWindow.openDevTools();
    manageWindow.maximize();
    if (options.winHide)
        manageWindow.hide();

    // 获取 webContents
    var webContents = manageWindow.webContents;
    /**
     * 渲染完成时触发
     */
    webContents.on('dom-ready', () => {
        // 脚本不为空时才能执行
        if (options.codeScript) {
            // 在 webContents 中执行脚本
            webContents.executeJavaScript(options.codeScript, false, (result) => {
                try {
                    callback(result, manageWindow);
                } catch (err) {
                    console.error('RemoteBaseWindow.js =:|======> ' + err);
                }
            });
        }
    });
}
```

###### 工具类 StorageTools.js

```javascript
/**
 * Created by mao-siyu on 17-2-9.
 */
var StorageTools = function () {
    // Check browser support
    if (typeof(Storage) === "undefined") {
        alert('抱歉！您的浏览器不支持 localStorage ...');
        return;
    }
}

StorageTools.setItem = function (key, value) {
    return localStorage.setItem(key, JSON.stringify(value));
}

StorageTools.getItem = function (key) {
    var result = '';
    try {
        result = JSON.parse(localStorage.getItem(key));
    } catch (e) {
    }
    return result;
}

StorageTools.removeItem = function (key) {
    return localStorage.removeItem(key);
}

StorageTools();
```

###### 输入 main.js

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
    var url = path.join('file://', __dirname, '/html/controller.html');
    // 可以是本地的html 也可以是 http://www.baidu.com
    mainWindow.loadURL(url);
    // 全屏显示
    mainWindow.maximize();
    // 打开开发工具
    // mainWindow.openDevTools();

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

###### 控制台界面 controller.html

```javascript
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Electron 控制管理界面</title>
    <style>
        /*左边窗体*/
        .webview-class {
            position: fixed;
            top: 3%;
            width: 66%;
            line-height: 100%;
            height: 90%;
            border: double 3px #000;
        }

        /*输入URL*/
        .url-input {
            position: fixed;
            top: 3%;
            right: 9%;
            width: 22%;
            height: 3%;
            border: double 3px blue;
        }

        /*渲染视图按钮*/
        .render-view {
            position: fixed;
            top: 3%;
            width: 7%;
            height: 36px;
            right: 1%;
            background-color: green;
            color: #FFF;
            border: double 4px fuchsia;
        }

        /*提示信息*/
        .info {
            position: fixed;
            top: 8%;
            right: 9%;
            width: 22%;
            height: 3%;
            border: dashed 3px fuchsia;
        }

        /*打开开发工具*/
        .open-dev-tools {
            position: fixed;
            top: 8%;
            width: 7%;
            height: 36px;
            right: 1%;
            background-color: green;
            color: #FFF;
            border: double 4px yellow;
        }

        /*右边控制台*/
        .console {
            position: fixed;
            top: 13%;
            right: 1%;
            width: 30%;
            height: 50%;
            border: double 3px green;
            overflow-y: scroll;
        }

        /*添加任务*/
        .add-task {
            position: fixed;
            top: 64%;
            width: 7%;
            height: 36px;
            right: 24%;
            background-color: green;
            color: #FFF;
            border: double 4px yellow;
        }

        /*执行任务*/
        .exec-task {
            position: fixed;
            top: 64%;
            width: 7%;
            height: 36px;
            right: 16%;
            background-color: green;
            color: #FFF;
            border: double 4px yellow;
        }

        /*任务列表*/
        .list-task {
            position: fixed;
            top: 68%;
            right: 1%;
            width: 30%;
            height: 25%;
            border: double 3px green;
            overflow-y: scroll;
        }

        /*底部显示信息*/
        .bottom-info {
            position: relative;
            bottom: -96vh;
            width: 100%;
            height: auto;
            min-height: 60px;
            border: double 3px blue;
            overflow-x: scroll;
            background-color: #FFF;
        }

        /*禁用按钮时样式*/
        input:disabled {
            background-color: #000;
        }
    </style>
</head>

<body>
<!--左边窗体-->
<webview class="webview-class" id="webviewId" src=""></webview>
<!--输入URL-->
<input class="url-input" id="urlInputId" type="text" placeholder="输入URL"/>
<!--渲染视图-->
<input class="render-view" id="renderViewId" type="button" value="渲染视图"/>
<!--提示信息-->
<div class="info" id="infoId">最终返回的数据, 要通过Promise的 resolve() 方法来实现</div>
<!--打开开发工具-->
<input class="open-dev-tools" id="openDevToolsId" type="button" value="打开DevTools" disabled/>
<!--右边控制台-->
<div class="console" id="consoleId" contenteditable></div>
<!--添加任务-->
<input class="add-task" id="addTaskId" type="button" value="添加任务" disabled/>
<!--执行任务-->
<input class="exec-task" id="execTaskId" type="button" value="执行任务" disabled/>
<!--任务列表-->
<div class="list-task" id="listTaskId"></div>
<!--底部显示信息-->
<div class="bottom-info" id="bottomInfoId"></div>

<!--引用共通窗体-->
<script src="../common-js/RemoteBaseWindow.js"></script>
<script src="../common-js/StorageTools.js"></script>

<script>
    const mWebview = document.getElementById('webviewId');
    // 输入URL
    const mUrlInput = document.getElementById('urlInputId');
    // 渲染视图
    const mRenderView = document.getElementById('renderViewId');
    // 提示信息
    const mInfo = document.getElementById('infoId');
    // 打开开发工具
    const mOpenDevTools = document.getElementById('openDevToolsId');
    // 控制台
    const mConsole = document.getElementById('consoleId');
    // 添加到任务列表
    const mAddTask = document.getElementById('addTaskId');
    // 执行任务
    const mExecTask = document.getElementById('execTaskId');
    // 任务列表
    const mListTask = document.getElementById('listTaskId');
    // 底部显示信息
    const bottomInfo = document.getElementById('bottomInfoId');
    // 缓存 任务流程代码
    var stepCache = [];

    // ===================================================================

    /**
     * 当前文档的导航和副框架的文档 加载完成时触发
     */
    mWebview.addEventListener("load-commit", function () {
        mOpenDevTools.disabled = false;
        mAddTask.disabled = false;
        mExecTask.disabled = false;
        // 使用网站的hostname做为key
        stepCache = StorageTools.getItem(window.location.hostname) || stepCache;
        // 在页面显示任务流程
        showListTask();
    });

    /**
     * 加载失败时触发
     */
    mWebview.addEventListener("did-fail-load", function () {
        mOpenDevTools.disabled = true;
        mAddTask.disabled = true;
        mExecTask.disabled = true;
    });

    /**
     * 渲染视图
     */
    mRenderView.onclick = function () {
        if (!mUrlInput.value.trim().length)
            return;
        mWebview.setAttribute('src', mUrlInput.value);
    }

    /**
     * 打开开发工具
     */
    mOpenDevTools.onclick = function () {
        mWebview.openDevTools();
    }

    /**
     * HTML5 的标准事件, 监听输入框的值变化
     */
    mUrlInput.oninput = function () {
        if (!this.value.trim().length)
            return;
        mWebview.setAttribute('src', this.value);
    }

    /**
     * 监听控制台, 命令变化
     */
    mConsole.oninput = function () {
        let testScript = `
            var testScript = function () {
                return new Promise((resolve, reject) => {
                    ${this.innerText.replace(/[\n]|\s{2,}/g, '')}
                });
            };
            // 执行脚本
            testScript().then((resultData) => {
                return resultData;
            }).catch((err) => {
                console.error('TestScript ==:|====>  ' + err);
            });
        `;
        mWebview.executeJavaScript(testScript, false, (result) => {
            bottomInfo.innerText = '';
            bottomInfoMessage(result);
        });
    }

    /**
     * 添加到任务列表
     */
    mAddTask.onclick = function () {
        // 第几个任务 就放在第几个step中
        // 使用正则.replace(/[\n]|\s{2,}/g, '')移除所有回车符 和 两个以上的空格
        let taskScript = `
            var task${stepCache.length} = function () {
                return new Promise((resolve, reject) => {
                    ${mConsole.innerText}
                });
            };

            task${stepCache.length}().then((resultData) => {
                return resultData;
            }).catch((err) => {
                console.error('task${stepCache.length} ==:|====>  ' + err);
            });
        `;
        // 将脚本添加到 流程当中
        stepCache.push(taskScript.replace(/[\n]|\s{2,}/g, ' '));

        // 在页面显示任务流程
        showListTask();

        // 清空控制台
        mConsole.innerHTML = '';
        // 清空底部显示信息
        bottomInfo.innerHTML = '';
        // 视图重新渲染
        mWebview.reload();
    }

    /**
     * 执行任务
     */
    mExecTask.onclick = function () {
        // 使用网站的hostname做为key, 将脚本保存到 localStorage 数据库
        StorageTools.setItem(window.location.hostname, stepCache);
        // 首次执行脚本
        mWebview.executeJavaScript(stepCache[0], false, (datas) => {

            var datas = datas;
            // 执行任务
            var exec = function () {
                var stepOptions = {
                    nodeIntegration: false,
                    winHide: true,
                    url: datas.shift(),
                    // 注入脚本
                    codeScript: stepCache[1]
                };
                // 在新窗体执行脚本
                BaseWindow.open(stepOptions, (result, manageWindow) => {

                    bottomInfoMessage(result);
                    // 强制关闭窗口
                    manageWindow.destroy();

                    if (datas.length) {
                        // 延迟执行
                        setTimeout(() => {
                            exec();
                        }, 2000);
                    } else {
                        bottomInfoMessage('SUCCESS ==:|====> 数据采集完成!');
                        // 执行下一步
                        mWebview.executeJavaScript(stepCache[2]);
                    }
                });
            }
            // 立即执行
            exec();

        });

    }

    /**
     * 在页面显示任务流程
     */
    var showListTask = function () {
        mListTask.innerHTML = '';
        for (var i = 0, len = stepCache.length; i < len; i++) {
            listTaskOutput(stepCache[i]);
        }
    }

    /**
     * 在任务列表出信息
     * @param info
     * @returns {Element}
     */
    var listTaskOutput = function (info) {
        var msg = document.createElement('div');
        msg.innerHTML = info + '<br/><br/>';
        mListTask.appendChild(msg);
    }

    /**
     * 在控制台输出信息
     * @param info
     * @returns {Element}
     */
    var bottomInfoMessage = function (info) {
        var msg = document.createElement('div');
        msg.innerHTML = info;
        bottomInfo.appendChild(msg);
    }
</script>
</body>
</html>
```
