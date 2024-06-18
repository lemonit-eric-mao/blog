---
title: "electron 开发窗体应用 (三)  修改子网页内容  executeJavaScript"
date: "2017-11-16"
categories: 
  - "electron"
---

##### 在webContents 中执行脚本

**executeJavaScript 这个方法是可以 将事先编写好的js代码, 在子窗体中运行, 执行方法时, 需要使用 Promise , 也有其它方法, 但我觉得这种用法更好!**

```javascript
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Electron 修改子网页内容</title>
    <style>
        .codeScript {
            width: 100%;
            height: 100%;
        }
    </style>
</head>
<body>
    <input id="urlId" type="text" value="https://www.baidu.com/" placeholder="输入URL"/>
    <textarea class="codeScript" id="codeScript" cols="30" rows="10">resolve(document.getElementById('su').value='百度两下');</textarea>
    <input type="button" value="打开新窗体" onclick="openNewWin()"/>
    <input id="execScriptId" type="button" value="执行脚本" disabled="true" onclick="execCodeScript()"/>

<script>
    const electron = require('electron');
    const BrowserWindow = electron.remote.BrowserWindow;
    const mUrl = document.getElementById('urlId');
    const mCodeScript = document.getElementById('codeScript');
    const mExecScriptId = document.getElementById('execScriptId');

    // 获取 webContents
    var webContents;

    /**
     * 打开一个新窗体
     */
    var openNewWin = function () {
        var manageWindow = new BrowserWindow({
            webPreferences: {
                nodeIntegration: false
            }, show: false
        });
        manageWindow.on('closed', () => {
            mExecScriptId.disabled = true;
            manageWindow = null;
        });
        manageWindow.loadURL(mUrl.value);
        manageWindow.openDevTools();
        manageWindow.maximize();

        webContents = manageWindow.webContents;
        /**
         * 渲染完成时触发
         */
        webContents.on('dom-ready', () => {
            mExecScriptId.disabled = false;
        });
    }

    /**
     * 在新窗体中执行脚本
     */
    var execCodeScript = function () {
        // 这里 是使用 ES6的 模板块来写的 不是普通的 '' 单引号字符串 而是 ESC下的  `~  这个键
        let codeScript = `
            var execCodeScript = function () {
                return new Promise((resolve, reject) => {
                    ${mCodeScript.value.replace(/\r\n/gi, '')}
                });
            };
            execCodeScript().then((obj) => {
                return obj;
            }).catch((err) => {
                console.error(err);
            });
        `;
        // 在 webContents 中执行脚本
        webContents.executeJavaScript(codeScript, false, (result) => {
            console.log(result);
        });
    }
</script>
</body>
</html>
```
