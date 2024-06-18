---
title: node_process
date: '2017-11-16T12:16:54+00:00'
status: publish
permalink: /2017/11/16/node_process
author: 毛巳煜
excerpt: ''
type: post
id: 143
category:
    - node.js
tag: []
post_format: []
hestia_layout_select:
    - default
---
```javascript
//////////////////////////===================process进程==================////////////////////////////////
// process是一个全局内置对象，可以在代码中的任何位置访问此对象，这个对象代表我们的node.js代码宿主的操作系统进程对象。
// 使用process对象可以截获进程的异常、退出等事件，也可以获取进程的当前目录、环境变量、内存占用等信息，还可以执行进程退出、工作目录切换等操作。
// 下面我们一起来学习一下process对象的一些常用方法。

```

```javascript
var os = require("os");
var result = os.platform(); // 查看操作系统平台
var result1 = os.release(); // 查看操作系统版本
var result2 = os.type(); // 查看操作系统名称
var result3 = os.arch(); // 查看操作系统CPU架构
console.log('操作系统平台:===>' + result);
console.log('操作系统版本:===>' + result1);
console.log('操作系统名称:===>' + result2);
console.log('操作系统CPU架构:===>' + result3);

```

```javascript
// cwd函数的基本用法
// 当我们想要查看应用程序当前目录时，可以使用cwd函数，使用语法如下：
var cwd = process.cwd();
console.log('应用程序当前目录:===>' + cwd);
// 获取程序目录的方法就是这样简单

```

```javascript
// chdir函数的基本用法
// 如果需要改变应用程序目录，就要使用chdir函数了，它的用法如下：
process.chdir("d:\Node"); // TODO 未实现
// 改变应用程序目录的方法就是这样简单

```

```javascript
// stdout的基本用法
// stdout是标准输出流，它是干什么的呢？请下看下面的示例：
// console.log = function(d){
//     process.stdout.write(d+'\n');
// }
// 没错，它的作用就是将内容打印到输出设备上，console.log就是封装了它。
// 练习 试一试，用stdout输出"hello world"。
process.stdout.write('hello world!');

```

```javascript
// stderr的基本用法
// stderr是标准错误流，和stdout的作用差不多，不同的是它是用来打印错误信息的，我们可以通过它来捕获错误信息，基本使用方法如下：
// process.stderr.write(输入内容);
// 试一试，用stderr输出字符串"test"。
process.stderr.write('test');

```

```javascript
// 设置编码
// 在我们的输入输出的内容中有中文的时候，可能会乱码的问题，这是因为编码不同造成的，所以在这种情况下需要为流设置编码，如下示例：
// process.stdin.setEncoding(编码);
// process.stdout.setEncoding(编码);
// process.stderr.setEncoding(编码);
// 试一试，设置stdout编码格式为"utf8"
process.stdin.setEncoding('UTF-8');
process.stdout.setEncoding('UTF-8');
process.stderr.setEncoding('UTF-8');

```

```javascript
// stdin的基本用法
// stdin是进程的输入流,我们可以通过注册事件的方式来获取输入的内容，如下：
process.stdin.on('readable', function() {
    var chunk = process.stdin.read();

    // TODO 不知道为什么 chunk 只能与控制台输入的数字想匹配，输入字符串匹配全是false，而且还不能是 严格类型判断
    if (9 == chunk) {
        process.exit();
    }
    if (chunk !== null) {
        process.stdout.write('退出程序请输入9\n');
        process.stdout.write('data:===> ' + chunk);
    }
});
// process.stdin.on('write', function (input) {
//     process.stdout.write('input: ' + chunk);
//     if ('exit' == input) {
//         process.exit();
//     }
// });
// 示例中的chunk就是输入流中的内容。

```

```javascript
// exit函数的基本用法
// 如果你需要在程序内杀死进程，退出程序，可以使用exit函数，示例如下：
process.exit(code);
// 参数code为退出后返回的代码，如果省略则默认返回0；
// 示例：
process.exit(console.log('程序运行结束!'));

```

```javascript
// 监听进程事件
// 使用process.on()方法可以监听进程事件。
// exit事件
// 当进程要退出之前，会触发exit事件。通过监听exit事件，我们可就以在进程退出前进行一些清理工作：
// 参数code表示退出码
// 监听 exit事件
process.on("exit", function(code) {
    //进行一些清理工作
    console.log('退出码:===>' + code);
});
var tick = Date.now();
console.log('tick:===>' + tick);

```

```javascript
// uncaughtException事件
// 如果进程发生了未捕捉的异常，会触发uncaughtException事件。通过监听这个事件，你可以 让进程优雅的退出：
//参数err表示发生的异常
process.on("uncaughtException", function(err) {
    console.log(err);
});
//故意抛出一个异常
throw new Error("我故意的...");

```