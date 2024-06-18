---
title: 'electron 开发窗体应用 (三)  修改子网页内容  executeJavaScript'
date: '2017-11-16T12:44:56+00:00'
status: publish
permalink: /2017/11/16/electron-%e5%bc%80%e5%8f%91%e7%aa%97%e4%bd%93%e5%ba%94%e7%94%a8-%e4%b8%89-%e4%bf%ae%e6%94%b9%e5%ad%90%e7%bd%91%e9%a1%b5%e5%86%85%e5%ae%b9-executejavascript
author: 毛巳煜
excerpt: ''
type: post
id: 203
category:
    - Electron
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
##### 在webContents 中执行脚本

**executeJavaScript 这个方法是可以 将事先编写好的js代码, 在子窗体中运行, 执行方法时, 需要使用 Promise , 也有其它方法, 但我觉得这种用法更好!**

```javascript



    <meta charset="UTF-8"></meta>
    <title>Electron 修改子网页内容</title>
    <style>
        .codeScript {
            width: 100%;
            height: 100%;
        }
    </style>


    <input id="urlId" placeholder="输入URL" type="text" value="https://www.baidu.com/"></input>
    <textarea class="codeScript" cols="30" id="codeScript" rows="10">resolve(document.getElementById('su').value='百度两下');</textarea>
    <input onclick="openNewWin()" type="button" value="打开新窗体"></input>
    <input disabled="disabled" id="execScriptId" onclick="execCodeScript()" type="button" value="执行脚本"></input>

<script>
    const electron = require('electron');
    const BrowserWindow = electron.remote.BrowserWindow;
    const mUrl = document.getElementById('urlId');
    const mCodeScript = document.getElementById('codeScript');
    const mExecScriptId = document.getElementById('execScriptId');

    // &#33719;&#21462; webContents
    var webContents;

    /**
     * &#25171;&#24320;&#19968;&#20010;&#26032;&#31383;&#20307;
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
         * &#28210;&#26579;&#23436;&#25104;&#26102;&#35302;&#21457;
         */
        webContents.on('dom-ready', () => {
            mExecScriptId.disabled = false;
        });
    }

    /**
     * &#22312;&#26032;&#31383;&#20307;&#20013;&#25191;&#34892;&#33050;&#26412;
     */
    var execCodeScript = function () {
        // &#36825;&#37324; &#26159;&#20351;&#29992; ES6&#30340; &#27169;&#26495;&#22359;&#26469;&#20889;&#30340; &#19981;&#26159;&#26222;&#36890;&#30340; '' &#21333;&#24341;&#21495;&#23383;&#31526;&#20018; &#32780;&#26159; ESC&#19979;&#30340;  `~  &#36825;&#20010;&#38190;
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
        // &#22312; webContents &#20013;&#25191;&#34892;&#33050;&#26412;
        webContents.executeJavaScript(codeScript, false, (result) => {
            console.log(result);
        });
    }
</script>



```