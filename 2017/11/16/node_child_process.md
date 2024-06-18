---
title: node_child_process
date: '2017-11-16T12:21:57+00:00'
status: publish
permalink: /2017/11/16/node_child_process
author: 毛巳煜
excerpt: ''
type: post
id: 157
category:
    - node.js
tag: []
post_format: []
hestia_layout_select:
    - default
---
```javascript
# ===================child_process子进程==================
# 众所周知node.js是基于单线程模型架构，这样的设计可以带来高效的CPU利用率，但是无法却利用多个核心的CPU，为了解决这个问题
# ，node.js提供了child_process模块，通过多进程来实现对多核CPU的利用. child_process模块提供了四个创建子进程的函数
# ，分别是spawn，exec，execFile和fork。

```

```javascript
const child_process = require('child_process');
 准备转码
var iconv = require('iconv-lite');


// spawn函数的简单用法
// spawn函数用给定的命令发布一个子进程，只能运行指定的程序，参数需要在列表中给出。如下示例：
 child_process.spawn(command[, args][, options])
// TODO 没用明白
 const spawn = child_process.spawn;
 const ipconfig = spawn('cmd.exe', ['java', '-version']);
 ipconfig.stdout.on('data', (data) => {
     console.log(data);
 });
// 所以想使用内置命令可以直接使用exec或者把spawn改成spawn(“cmd.exe”,["\s", “\c”, “dir”]);
// 总结起来就是spawn是调用一个文件! 不要被docs上的child_process.spawn(command, [args], [options])中的command给骗了

```

```javascript
// exec函数的简单用法
// exec也是一个创建子进程的函数，与spawn函数不同它可以直接接受一个回调函数作为参数
// ，回调函数有三个参数，分别是err, stdout , stderr，基本使用方法如下：
// child_process.exec(command[, options][, callback])
const exec = child_process.exec;
// 使用lambda 表达式输出
exec('ipconfig', (err, stdout, stderr) => {
    if (err) throw err;
    if (stderr) throw stderr;
    console.log(iconv.decode(stdout, 'UTF-8'));
});
// 未使用 Lambda表达式
 child_process.exec('ipconfig', function(err, stdout, stderr) {
     if (err) throw err;
     if (stderr) throw stderr;
     console.log(stdout);
 });
// exec函数可以直接接受一个回调函数作为参数， 回调函数有三个参数， 分别是err, stdout, stderr， 非常方便直接使用

```

```javascript
# execFile函数的简单用法
# execFile函数与exec函数类似，但execFile函数更显得精简，因为它可以直接执行所指定的文件，基本使用方法如下：
 // TODO 没研究明白
 const execFile = child_process.execFile;
 execFile('C:/Windows/System32/cmd.exe', (err, stdout, stderr) => {
     console.log(stdout);
 });
// execFile与spawn的参数相似，也需要分别指定执行的命令和参数，但可以接受一个回调函数，与exec的回调函数相同。

```

```javascript
// fork函数的简单用法
// fork函数可直接运行Node.js模块，所以我们可以直接通过指定模块路径而直接进行操作。使用方法如下：
 // TODO 没研究明白
 child_process.fork( modulePath );
 该方法是spawn()的特殊情景，用于派生Node进程。除了普通ChildProcess实例所具有的所有方法，所返回的对象还具有内建的通讯通道。

```