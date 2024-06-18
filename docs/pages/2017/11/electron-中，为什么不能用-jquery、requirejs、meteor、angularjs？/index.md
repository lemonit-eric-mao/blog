---
title: "Electron 中，为什么不能用 jQuery、RequireJS、Meteor、AngularJS？"
date: "2017-11-16"
categories: 
  - "electron"
---

###### 因为 Electron 在运行环境中引入了 Node.js，所以在 DOM 中有一些额外的变量，比如 module、exports和 require。这导致 了许多库不能正常运行，因为它们也需要将同名的变量加入运行环境中。

###### **我们可以通过禁用 Node.js 来解决这个问题，用如下的方式：**

```javascript
// 在主进程中
var mainWindow = new BrowserWindow({
  webPreferences: {
    nodeIntegration: false
  }
});
```

[w3cschool中有详细说明](http://www.w3cschool.cn/electronmanual/electronmanual-electron-faq.html "w3cschool中有详细说明")
