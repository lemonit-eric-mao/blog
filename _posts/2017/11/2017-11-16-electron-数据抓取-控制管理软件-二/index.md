---
title: "electron 数据抓取 控制管理软件 (二)"
date: "2017-11-16"
categories: 
  - "electron"
---

##### [github项目地址](https://github.com/maosiyu/data-acquisition-manage)

##### **新版 新思路**

之前写的代码将业务逻辑都写死在程序中,如果这样做,根本无法在继续扩展了, 因此 最近又做了优化应该的方式比之前简单 灵活 第二版改成了 mvc的模式去写, 方便代码后期的维护开发, 使用了部分ES6语法, 以后会慢慢的全部改成ES6语法 项目.

**开发思路:** 因为第一版的 局限性问题, 所以在第二版, 把复杂的逻辑编写任务, 交给了使用者, 也就是执行的脚本部分, 开发者想要什么样的数据, 就直接在页面窗体上 根据项目中 提供的API 自己去编写, 这样既灵活, 就节省编程时间, 相当于自己写了一个简单的浏览器窗体.

以下是源码:

###### **main.js**

```javascript
// 全局异常捕获
require('./src/main/js/common/tools/GlobalException');
const path = require('path');
const ipcMain = require('electron').ipcMain;
const MainWindow = require('./src/main/js/common/core/MainWindow');
const mMainWindow = new MainWindow();

const url = path.join('file://', __dirname, './src/main/js/controller/controller.html');
mMainWindow.open(url);
```

###### **MainWindow.js**

```javascript
'use strict';
const electron = require('electron');
// 控制应用生命周期的模块。
const app = electron.app;
// 创建原生浏览器窗口的模块
const BrowserWindow = electron.BrowserWindow;

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

const MainWindow = function () {
}

// 保持一个对于 window 对象的全局引用，不然，当 JavaScript 被 GC，
// window 会被自动地关闭
var win = null;

/**
 * 创建窗体
 * @param callback
 */
MainWindow.prototype.createWindow = function (callback) {
    // 当 Electron 完成了初始化并且准备创建浏览器窗口的时候
    // 这个方法就被调用
    app.on('ready', () => {
        win = new BrowserWindow();
        /**
         * 当前 window 被关闭，这个事件会被发出
         */
        win.on('closed', () => {
            // 取消引用 window 对象，如果你的应用支持多窗口的话，
            // 通常会把多个 window 对象存放在一个数组里面，
            // 但这次不是。
            win = null;
            console.info('窗口关闭');
        });
        callback();
    });
};

/**
 * 打开窗体
 * @param url
 */
MainWindow.prototype.open = function (url) {
    MainWindow.prototype.createWindow(() => {
        // 可以是本地的html 也可以是 http://www.baidu.com
        win.loadURL(url);
        // 全屏显示
        win.maximize();
        // 打开开发工具
        win.openDevTools();
    });
};

module.exports = MainWindow;
```

###### **RemoteBaseWindow.js**

```javascript
/**
 * Created by mao_siyu on 2017/4/21.
 */
const electron = require('electron');
const BrowserWindow = electron.remote.BrowserWindow;
// 窗体池
const windowPool = {};

const RemoteBaseWindow = function () {
}

/**
 * 创建一个窗体对象
 * @param winName
 * @param options
 */
RemoteBaseWindow.prototype.createWindow = function (winName, options) {

    // 判断窗体池中是否已经有这个窗体
    if (windowPool[winName])
        throw '=:|======> createWindow 创建失败, 窗体已经存在！';

    let defaults = {
        nodeIntegration: false
    };
    // 合并替换
    options = Object.assign(defaults, options);

    // 新建一个窗体
    let manageWindow = new BrowserWindow({
        show: false,
        webPreferences: {
            nodeIntegration: options.nodeIntegration // nodeIntegration: false 禁用子窗体使用 node.js功能
        }
    });
    // 当窗口已经关闭的时候触发
    manageWindow.on('closed', () => {
        manageWindow = null; // 删除对已经关闭的窗口的引用对象和避免再次使用它
        windowPool[winName] = null; // 删除窗体池里对应的对象
    });
    // 将窗体保存到窗体池
    windowPool[winName] = manageWindow;
    return windowPool[winName];
}

/**
 * 获取一个已经存在的窗体
 * @param winName
 */
RemoteBaseWindow.prototype.getWindow = function (winName) {
    let win = windowPool[winName];
    if (win)
        return win;
    else
        throw '=:|======> getWindow 获取的窗体不存在！';
}

/**
 * 打开新窗体
 */
RemoteBaseWindow.prototype.open = function (win, url) {
    win.loadURL(url);
    // win.minimize();
    win.openDevTools();
    win.maximize();
}

/**
 * 执行脚本
 * @param manageWindow
 * @param injectScript
 * @param callback
 */
RemoteBaseWindow.prototype.execJavaScript = function (win, injectScript, callback) {
    // 脚本不为空时才能执行
    if (!injectScript)
        throw '=:|======> 执行脚本不能为空';
    // 在 webContents 中执行脚本
    win.webContents.executeJavaScript(RemoteBaseWindow.scriptBuilder(injectScript), false, (result) => {
        try {
            callback(result);
        } catch (err) {
            console.error('=:|======> executeJavaScript 执行失败!' + err);
        }
    });
}

/**
 * 脚本生成
 * @param script
 * @param index
 */
RemoteBaseWindow.scriptBuilder = function (script) {
    let scriptShell = `
        var scriptBuilder = function () {
            return new Promise((resolve, reject) => {
                ${script}
            });
        };

        scriptBuilder().then((resultData) => {
            return resultData;
        }).catch((err) => {
            console.error('scriptBuilder ==:|======>  ' + err);
        });
    `;

    // 使用正则.replace(/[\n]|\s{2,}/g, '')移除所有回车符 和 两个以上的空格
    return scriptShell.replace(/[\n]|\s{2,}/g, ' ');
}

module.exports = RemoteBaseWindow;
```

###### **DataSourceProxy.js**

```javascript
/**
 * Created by mao-siyu on 17-6-23.
 */
const Mysql = require('./Mysql');
const FileIO = require('../tools/FileIO');
const path = require('path');

const DBProxy = function () {
}

// 应用 mysql 数据库
DBProxy.prototype.mySqlExec = function (sql, callback) {
    Mysql.query(sql, callback);
}

// 向本地写数据
DBProxy.prototype.files = function (options) {
    let option = {
        fileName: '',
        resultData: ''
    }
    options = Object.assign(option, options);

    let newFilePath = path.join(__dirname, '../../../../../../' + option.fileName);
    // 保存到本地硬盘
    FileIO.mkdirsPromise(newFilePath).then(() => {
        return FileIO.localWriteFilePromise(newFilePath, option.resultData).catch((err) => {
            console.error(err);
        });
    }).then(() => {
        console.info('本地数据保存成功!    ' + newFilePath);
    }).catch((err) => {
        console.error('本地数据保存失败!' + err);
    });
}

module.exports = DBProxy;
```

###### **controller.html**

```markup
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Electron 控制管理界面</title>
    <style>

        .submit {
            position: fixed;
            top: 5%;
            right: 6%;
            width: 9%;
            height: 9%;
            border: double 3px green;
        }

        .console {
            top: 6%;
            width: 60%;
            height: 50%;
            position: relative;
            width: 100%;
            height: auto;
            min-height: 666px;
            border: double 3px green;
            overflow-y: scroll;
        }
    </style>
</head>

<body>
<!--右边控制台-->
<div class="console" id="consoleId" contenteditable></div>
<input class="submit" type="button" id="submitId" value="提交"/>
<!--DOM Script-->
<script>
    let mConsole = document.getElementById('consoleId');
    let mSubmit = document.getElementById('submitId');
    mSubmit.onclick = function () {
        eval(mConsole.innerText);
    }
</script>
<script src="controller.js"></script>
</body>
</html>
```

###### **controller.js**

```javascript
/**
 * Created by mao_siyu on 2017/7/2.
 */
// 工具
const fs = require('fs');
const URL = require('url');
const AXIOS = require('axios');
const MOMENT = require('moment');
const SCHEDULE = require('node-schedule');
const UUID = require('../common/tools/UUID');
// 实例
const BaseService = require('../service/BaseService');
const mBaseService = new BaseService();
/**
 * 打开新窗体
 *
 * @param arg 格式要求 {"winName": "","url": "https://www.private-blog.com/", "injectScript": "resolve(document.querySelector(''));"}
 * @param callback 返回(result, win)
 */
const openNewWindow = function (arg, callback) {
    try {
        mBaseService.openNewWindow(arg, callback);
    } catch (e) {
        console.error(`openNewWindow =:|====> ${e}`);
        saveDataToLocal('controllerErrorLog.txt', `openNewWindow =:|====> ${e} \n\n`);
    }
}

/**
 * 操作一个已存在的窗体
 *
 * @param arg 格式要求 {"winName": "","url": "https://www.private-blog.com/", "injectScript": "resolve(document.querySelector(''));"}
 * @param callback 返回(result, win)
 */
const operationExistsWindow = function (arg, callback) {
    try {
        mBaseService.operationExistsWindow(arg, callback);
    } catch (e) {
        console.error(`operationExistsWindow =:|====> ${e}`);
        saveDataToLocal('controllerErrorLog.txt', `operationExistsWindow =:|====> ${e} \n\n`);
    }
}

/**
 * 插入数据
 * @param sql
 * @param callback
 */
const insertData = function (sql, callback) {
    try {
        mBaseService.insertData(sql, callback);
    } catch (e) {
        console.error(`insertData =:|====> ${e}`);
        saveDataToLocal('controllerErrorLog.txt', `insertData =:|====> ${e} \n\n`);
    }
}

/**
 * 查询数据
 * @param sql
 * @param callback
 */
const selectData = function (sql, callback) {
    try {
        mBaseService.selectData(sql, callback);
    } catch (e) {
        console.error(`selectData =:|====> ${e}`);
        saveDataToLocal('controllerErrorLog.txt', `selectData =:|====> ${e} \n\n`);
    }
}

/**
 * 数据保存到本地
 * @param fileName
 * @param data
 */
const saveDataToLocal = function (fileName, data) {
    try {
        mBaseService.saveDataToLocal(fileName, data);
    } catch (e) {
        console.error(`saveDataToLocal =:|====> ${e}`);
    }
}

// 定时器池
const mSchedulePool = {};
/**
 * 开启一个新的定时器
 * @param scheduleName
 * @param rule    var rule = new SCHEDULE.RecurrenceRule();
 * @param callback
 */
const timerOpen = function (scheduleName, rule, callback) {
    if (!rule)
        throw `=:|======> timerOpen rule 参数不能为 ${rule} ！`;

    let schedule = mSchedulePool[scheduleName];
    // 如果池中存在, 就返回这个定时器
    if (schedule)
        return schedule;
    // 如果池中没有, 就新建一个定时器
    schedule = SCHEDULE.scheduleJob(rule, function () {
        callback();
    });
    // 将定时器保存到池中
    mSchedulePool[scheduleName] = schedule;
}

/**
 * 关闭定时器
 * @param scheduleName
 */
const timerClose = function (scheduleName) {
    let schedule = mSchedulePool[scheduleName];
    // 如果池中有就关闭这个定时器
    if (schedule) {
        schedule.cancel();
        mSchedulePool[scheduleName] = null;
    }
    // 如果没有就什么都不做
}
```

###### **BaseService.js**

```javascript
/**
 * Created by mao-siyu on 17-6-29.
 */
const RemoteBaseWindow = require('../common/core/RemoteBaseWindow');
const mRemoteBaseWindow = new RemoteBaseWindow();

const BaseDao = require('../dao/BaseDao');
const mBaseDao = new BaseDao();

/**
 * 基础服务类
 * @param webview
 * @param stepCache
 * @param repeatNum
 * @constructor
 */
const BaseService = function () {
}

/**
 * 打开窗体
 * @param arg
 * @param callback
 */
BaseService.prototype.openNewWindow = function (arg, callback) {
    // 打开窗体
    let win;
    try {
        win = mRemoteBaseWindow.getWindow(arg.winName);
    } catch (e) {
        win = mRemoteBaseWindow.createWindow(arg.winName);
    }
    // 打开新窗体
    mRemoteBaseWindow.open(win, arg.url);
    // 执行脚本
    mRemoteBaseWindow.execJavaScript(win, arg.injectScript, (result) => {
        if (!callback)
            return;
        callback(result, win);
    });
}

/**
 * 应用已存在的窗体
 * @param arg
 * @param callback
 */
BaseService.prototype.operationExistsWindow = function (arg, callback) {
    let win = mRemoteBaseWindow.getWindow(arg.winName);
    // 如果 url 存在就替换之前的 URL, 否则只复用窗体
    if (arg.url)
        mRemoteBaseWindow.open(win, arg.url);
    // 执行脚本
    mRemoteBaseWindow.execJavaScript(win, arg.injectScript, (result) => {
        if (!callback)
            return;
        callback(result, win);
    });
}

/**
 * 插入数据
 * @param sql
 * @param callback
 */
BaseService.prototype.insertData = function (sql, callback) {
    mBaseDao.insertData(sql, callback);
}

/**
 * 查询数据
 * @param sql
 * @param callback
 */
BaseService.prototype.selectData = function (sql, callback) {
    mBaseDao.selectData(sql, callback);
}

/**
 * 数据保存到本地
 * @param param
 * @param url
 */
BaseService.prototype.saveDataToLocal = function (fileName, data) {
    mBaseDao.saveDataToLocal(fileName, data);
}

module.exports = BaseService;
```

###### **BaseDao.js**

```javascript
/**
 * Created by mao-siyu on 17-6-29.
 */
// 数据源代理
const DataSourceProxy = require('../common/database/DataSourceProxy');
const mDataSourceProxy = new DataSourceProxy();

const BaseDao = function () {
}

/**
 * 插入数据
 * @param sql
 * @param callback
 */
BaseDao.prototype.insertData = function (sql, callback) {
    mDataSourceProxy.mySqlExec(sql, callback);
}

/**
 * 查询数据
 * @param sql
 * @param callback
 */
BaseDao.prototype.selectData = function (sql, callback) {
    mDataSourceProxy.mySqlExec(sql, callback);
}

/** ===================================== 以下是操作本地数据方法区域 ======================================== */

/**
 * 数据保存到本地
 * @param param
 * @param hostname
 */
BaseDao.prototype.saveDataToLocal = function (fileName, data) {
    mDataSourceProxy.files({
        fileName: fileName,
        resultData: data,
    });
}

module.exports = BaseDao;
```
