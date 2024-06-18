---
title: 'electron 数据抓取 控制管理软件 (一)'
date: '2017-11-16T12:46:09+00:00'
status: publish
permalink: /2017/11/16/electron-%e6%95%b0%e6%8d%ae%e6%8a%93%e5%8f%96-%e6%8e%a7%e5%88%b6%e7%ae%a1%e7%90%86%e8%bd%af%e4%bb%b6-%e4%b8%80
author: 毛巳煜
excerpt: ''
type: post
id: 207
category:
    - Electron
tag: []
post_format: []
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



    <meta charset="UTF-8"></meta>
    <title>Electron 控制管理界面</title>
    <style>
        /*&#24038;&#36793;&#31383;&#20307;*/
        .webview-class {
            position: fixed;
            top: 3%;
            width: 66%;
            line-height: 100%;
            height: 90%;
            border: double 3px #000;
        }

        /*&#36755;&#20837;URL*/
        .url-input {
            position: fixed;
            top: 3%;
            right: 9%;
            width: 22%;
            height: 3%;
            border: double 3px blue;
        }

        /*&#28210;&#26579;&#35270;&#22270;&#25353;&#38062;*/
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

        /*&#25552;&#31034;&#20449;&#24687;*/
        .info {
            position: fixed;
            top: 8%;
            right: 9%;
            width: 22%;
            height: 3%;
            border: dashed 3px fuchsia;
        }

        /*&#25171;&#24320;&#24320;&#21457;&#24037;&#20855;*/
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

        /*&#21491;&#36793;&#25511;&#21046;&#21488;*/
        .console {
            position: fixed;
            top: 13%;
            right: 1%;
            width: 30%;
            height: 50%;
            border: double 3px green;
            overflow-y: scroll;
        }

        /*&#28155;&#21152;&#20219;&#21153;*/
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

        /*&#25191;&#34892;&#20219;&#21153;*/
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

        /*&#20219;&#21153;&#21015;&#34920;*/
        .list-task {
            position: fixed;
            top: 68%;
            right: 1%;
            width: 30%;
            height: 25%;
            border: double 3px green;
            overflow-y: scroll;
        }

        /*&#24213;&#37096;&#26174;&#31034;&#20449;&#24687;*/
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

        /*&#31105;&#29992;&#25353;&#38062;&#26102;&#26679;&#24335;*/
        input:disabled {
            background-color: #000;
        }
    </style>




<webview class="webview-class" id="webviewId" src=""></webview>

<input class="url-input" id="urlInputId" placeholder="输入URL" type="text"></input>

<input class="render-view" id="renderViewId" type="button" value="渲染视图"></input>

<div class="info" id="infoId">最终返回的数据, 要通过Promise的 resolve() 方法来实现</div>

<input class="open-dev-tools" disabled="disabled" id="openDevToolsId" type="button" value="打开DevTools"></input>

<div class="console" contenteditable="" id="consoleId"></div>

<input class="add-task" disabled="disabled" id="addTaskId" type="button" value="添加任务"></input>

<input class="exec-task" disabled="disabled" id="execTaskId" type="button" value="执行任务"></input>

<div class="list-task" id="listTaskId"></div>

<div class="bottom-info" id="bottomInfoId"></div>


<script src="../common-js/RemoteBaseWindow.js"></script>
<script src="../common-js/StorageTools.js"></script>

<script>
    const mWebview = document.getElementById('webviewId');
    // &#36755;&#20837;URL
    const mUrlInput = document.getElementById('urlInputId');
    // &#28210;&#26579;&#35270;&#22270;
    const mRenderView = document.getElementById('renderViewId');
    // &#25552;&#31034;&#20449;&#24687;
    const mInfo = document.getElementById('infoId');
    // &#25171;&#24320;&#24320;&#21457;&#24037;&#20855;
    const mOpenDevTools = document.getElementById('openDevToolsId');
    // &#25511;&#21046;&#21488;
    const mConsole = document.getElementById('consoleId');
    // &#28155;&#21152;&#21040;&#20219;&#21153;&#21015;&#34920;
    const mAddTask = document.getElementById('addTaskId');
    // &#25191;&#34892;&#20219;&#21153;
    const mExecTask = document.getElementById('execTaskId');
    // &#20219;&#21153;&#21015;&#34920;
    const mListTask = document.getElementById('listTaskId');
    // &#24213;&#37096;&#26174;&#31034;&#20449;&#24687;
    const bottomInfo = document.getElementById('bottomInfoId');
    // &#32531;&#23384; &#20219;&#21153;&#27969;&#31243;&#20195;&#30721;
    var stepCache = [];

    // ===================================================================

    /**
     * &#24403;&#21069;&#25991;&#26723;&#30340;&#23548;&#33322;&#21644;&#21103;&#26694;&#26550;&#30340;&#25991;&#26723; &#21152;&#36733;&#23436;&#25104;&#26102;&#35302;&#21457;
     */
    mWebview.addEventListener("load-commit", function () {
        mOpenDevTools.disabled = false;
        mAddTask.disabled = false;
        mExecTask.disabled = false;
        // &#20351;&#29992;&#32593;&#31449;&#30340;hostname&#20570;&#20026;key
        stepCache = StorageTools.getItem(window.location.hostname) || stepCache;
        // &#22312;&#39029;&#38754;&#26174;&#31034;&#20219;&#21153;&#27969;&#31243;
        showListTask();
    });

    /**
     * &#21152;&#36733;&#22833;&#36133;&#26102;&#35302;&#21457;
     */
    mWebview.addEventListener("did-fail-load", function () {
        mOpenDevTools.disabled = true;
        mAddTask.disabled = true;
        mExecTask.disabled = true;
    });

    /**
     * &#28210;&#26579;&#35270;&#22270;
     */
    mRenderView.onclick = function () {
        if (!mUrlInput.value.trim().length)
            return;
        mWebview.setAttribute('src', mUrlInput.value);
    }

    /**
     * &#25171;&#24320;&#24320;&#21457;&#24037;&#20855;
     */
    mOpenDevTools.onclick = function () {
        mWebview.openDevTools();
    }

    /**
     * HTML5 &#30340;&#26631;&#20934;&#20107;&#20214;, &#30417;&#21548;&#36755;&#20837;&#26694;&#30340;&#20540;&#21464;&#21270;
     */
    mUrlInput.oninput = function () {
        if (!this.value.trim().length)
            return;
        mWebview.setAttribute('src', this.value);
    }

    /**
     * &#30417;&#21548;&#25511;&#21046;&#21488;, &#21629;&#20196;&#21464;&#21270;
     */
    mConsole.oninput = function () {
        let testScript = `
            var testScript = function () {
                return new Promise((resolve, reject) => {
                    <span class="katex math inline">{this.innerText.replace(/[\n]|\s{2,}/g, '')}
                });
            };
            // &#25191;&#34892;&#33050;&#26412;
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
     * &#28155;&#21152;&#21040;&#20219;&#21153;&#21015;&#34920;
     */
    mAddTask.onclick = function () {
        // &#31532;&#20960;&#20010;&#20219;&#21153; &#23601;&#25918;&#22312;&#31532;&#20960;&#20010;step&#20013;
        // &#20351;&#29992;&#27491;&#21017;.replace(/[\n]|\s{2,}/g, '')&#31227;&#38500;&#25152;&#26377;&#22238;&#36710;&#31526; &#21644; &#20004;&#20010;&#20197;&#19978;&#30340;&#31354;&#26684;
        let taskScript = `
            var task{stepCache.length} = function () {
                return new Promise((resolve, reject) => {
                    <span class="katex math inline">{mConsole.innerText}
                });
            };

            task{stepCache.length}().then((resultData) => {
                return resultData;
            }).catch((err) => {
                console.error('task${stepCache.length} ==:|====>  ' + err);
            });
        `;
        // &#23558;&#33050;&#26412;&#28155;&#21152;&#21040; &#27969;&#31243;&#24403;&#20013;
        stepCache.push(taskScript.replace(/[\n]|\s{2,}/g, ' '));

        // &#22312;&#39029;&#38754;&#26174;&#31034;&#20219;&#21153;&#27969;&#31243;
        showListTask();

        // &#28165;&#31354;&#25511;&#21046;&#21488;
        mConsole.innerHTML = '';
        // &#28165;&#31354;&#24213;&#37096;&#26174;&#31034;&#20449;&#24687;
        bottomInfo.innerHTML = '';
        // &#35270;&#22270;&#37325;&#26032;&#28210;&#26579;
        mWebview.reload();
    }

    /**
     * &#25191;&#34892;&#20219;&#21153;
     */
    mExecTask.onclick = function () {
        // &#20351;&#29992;&#32593;&#31449;&#30340;hostname&#20570;&#20026;key, &#23558;&#33050;&#26412;&#20445;&#23384;&#21040; localStorage &#25968;&#25454;&#24211;
        StorageTools.setItem(window.location.hostname, stepCache);
        // &#39318;&#27425;&#25191;&#34892;&#33050;&#26412;
        mWebview.executeJavaScript(stepCache[0], false, (datas) => {

            var datas = datas;
            // &#25191;&#34892;&#20219;&#21153;
            var exec = function () {
                var stepOptions = {
                    nodeIntegration: false,
                    winHide: true,
                    url: datas.shift(),
                    // &#27880;&#20837;&#33050;&#26412;
                    codeScript: stepCache[1]
                };
                // &#22312;&#26032;&#31383;&#20307;&#25191;&#34892;&#33050;&#26412;
                BaseWindow.open(stepOptions, (result, manageWindow) => {

                    bottomInfoMessage(result);
                    // &#24378;&#21046;&#20851;&#38381;&#31383;&#21475;
                    manageWindow.destroy();

                    if (datas.length) {
                        // &#24310;&#36831;&#25191;&#34892;
                        setTimeout(() => {
                            exec();
                        }, 2000);
                    } else {
                        bottomInfoMessage('SUCCESS ==:|====> &#25968;&#25454;&#37319;&#38598;&#23436;&#25104;!');
                        // &#25191;&#34892;&#19979;&#19968;&#27493;
                        mWebview.executeJavaScript(stepCache[2]);
                    }
                });
            }
            // &#31435;&#21363;&#25191;&#34892;
            exec();

        });

    }

    /**
     * &#22312;&#39029;&#38754;&#26174;&#31034;&#20219;&#21153;&#27969;&#31243;
     */
    var showListTask = function () {
        mListTask.innerHTML = '';
        for (var i = 0, len = stepCache.length; i < len; i++) {
            listTaskOutput(stepCache[i]);
        }
    }

    /**
     * &#22312;&#20219;&#21153;&#21015;&#34920;&#20986;&#20449;&#24687;
     * @param info
     * @returns {Element}
     */
    var listTaskOutput = function (info) {
        var msg = document.createElement('div');
        msg.innerHTML = info + '<br/><br/>';
        mListTask.appendChild(msg);
    }

    /**
     * &#22312;&#25511;&#21046;&#21488;&#36755;&#20986;&#20449;&#24687;
     * @param info
     * @returns {Element}
     */
    var bottomInfoMessage = function (info) {
        var msg = document.createElement('div');
        msg.innerHTML = info;
        bottomInfo.appendChild(msg);
    }
</script>



```