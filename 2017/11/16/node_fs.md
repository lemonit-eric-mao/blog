---
title: node_fs
date: '2017-11-16T12:19:44+00:00'
status: publish
permalink: /2017/11/16/node_fs
author: 毛巳煜
excerpt: ''
type: post
id: 149
category:
    - node.js
tag: []
post_format: []
hestia_layout_select:
    - default
---
```
<pre data-language="">```javascript
//////////////////////////===================文件IO==================////////////////////////////////
// 文件I/O fs模块的基本用法
// 开发中我们经常会有文件I/O的需求，node.js中提供一个名为fs的模块来支持I/O操作，fs模块的文件I/O是对标准POSIX函数的简单封装。

```
```

```
<pre data-language="">```javascript
// writeFile函数的基本用法
// 文件I/O，写入是必修课之一。fs模块提供writeFile函数，可以异步的将数据写入一个文件, 如果文件已经存在则会被替换。用法如下：
// 例：fs.writeFile(filename, data, callback)
var fs = require('fs');
fs.writeFile('maosiyu.txt', '使用node.js输入文件内容！', function(err) {
    if (err) throw err;
    console.log('保存成功！');
});
// 数据参数可以是string或者是Buffer,编码格式参数可选，默认为"utf8"，回调函数只有一个参数err。

```
```

```
<pre data-language="">```javascript
// appendFile函数的基本用法
// writeFile函数虽然可以写入文件，但是如果文件已经存在，我们只是想添加一部分内容，它就不能满足我们的需求了
// ，很幸运，fs模块中还有appendFile函数，它可以将新的内容追加到已有的文件中，如果文件不存在，则会创建一个新的文件。使用方法如下：
// 例：fs.appendFile(文件名,数据,编码,回调函数(err));
fs.appendFile('maosiyu.txt', '我又追加进来啦！', function(err) {
    if (err) throw err;
    console.log('数据被添加到文件的尾部!');
});
// 编码格式默认为"utf8"，

```
```

```
<pre data-language="">```javascript
// exists函数的基本用法
// 如何检查一个文件是否存在呢？我想exists函数可以帮助你，用法如下：
// 例：fs.exists(文件，回调函数(exists));
// exists的回调函数只有一个参数，类型为布尔型，通过它来表示文件是否存在。
fs.exists('maosiyu.txt', function(exists) {
    console.log(exists ? '存在!' : '不存在!');
});

```
```

```
<pre data-language="">```javascript
// rename函数的基本用法
// 修改文件名称是我们经常会遇见的事情，rename函数提供修改名称服务：
// fs.rename(旧文件，新文件，回调函数(err){
//    if (err) throw err;
//    console.log('Successful modification,');
// });
fs.rename('maosiyu.txt', 'maomao.txt', function(err) {
    if (err) throw err;
    console.log('文件名修改成功!');
});

```
```

```
<pre data-language="">```javascript
// mkdir函数的基本用法
// 除了针对文件的操作，目录的创建、删除也经常遇到的，下面我们来看看node.js中如何创建目录：
// fs.mkdir(路径，权限，回调函数(err));
// 参数
// 路径：新创建的目录。
// 权限：可选参数，只在linux下有效，表示目录的权限，默认为0777，表示文件所有者、文件所有者所在的组的用户、所有用户，都有权限进行读、写、执行的操作。
// 回调函数：当发生错误时，错误信息会传递给回调函数的err参数。
fs.mkdir('./newPath', function(err) {
    if (err) throw err;
    console.log('创建成功!');
});

```
```

```
<pre data-language="">```javascript
// rename函数的基本用法
// 移动文件也是我们经常会遇见的，可是fs没有专门移动文件的函数，但是我们可以通过rename函数来达到移动文件的目的，示例如下。
// fs.rename(oldPath,newPath,function (err) {
//    if (err) throw err;
//    console.log('renamed complete');
// });
fs.rename('maomao.txt', 'newPath/maomao.txt', function(err) {
    if (err) throw err;
    console.log('移动成功!');
});

```
```

```
<pre data-language="">```javascript
// readFile函数的基本用法
// 读取文件是最常用到的功能之一，使用fs模块读取文件语法如下：
// 例：fs.readFile(文件,编码,回调函数);
// fs.readFile(文件名, function (err, data) {
//   if (err) throw err;
//   console.log(data);
// });
// 回调函数里面的data,就是读取的文件内容。
fs.readFile('newPath/maomao.txt', function(err, data) {
    if (err) throw err;
    console.log(data);
});

```
```

```
<pre data-language="">```javascript
// unlink函数的基本用法
// 面对一堆垃圾的文件总是有想删除的冲动，我有强迫症？你才有呢。
// 好在有unlink函数，终于得救了，示例如下：
// 例：fs.unlink(文件,回调函数(err));

fs.unlink('newPath/maomao.txt', function(err) {
    if (err) throw err;
    console.log('删除成功!');
});

```
```

```
<pre data-language="">```javascript
// rmdir函数的基本用法
// 删除目录也是必不可少的功能，rmdir函数可以删除指定的目录：
// 例：fs.rmdir(路径，回调函数(err));
fs.rmdir('newPath', function(err) {
    if (err) throw err;
    console.log('创建成功!');
});

```
```

```
<pre data-language="">```javascript
// readdir函数的基本用法
// 如果要读取目录下所有的文件应该怎么办呢？readdir函数可以读取到指定目录下所有的文件，示例如下：
// fs.readdir(目录,回调函数(err,files));
// 回调函数 (callback) 接受两个参数 (err, files) 其中 files 是一个存储目录中所包含的文件名称的数组，数组中不包括 '.' 和 '..'。
fs.readdir('newPath', function(err, files) {
    if (err) throw err;
    console.log(files);
});

```
```

```
<pre data-language="">```javascript
// 课程小结
// 文件I/O是最基本的操作，应该熟悉掌握。
// fs模块不但提供异步的文件操作，还提供相应的同步操作方法，需要指出的是
////// ，nodejs采用异步I/O正是为了避免I/O时的等待时间，提高CPU的利用率，所以在选择使用异步或同步方法的时候需要权衡取舍。

// 本节课程讲解了fs模块常用的一些功能，当然它还有更多强大的功能，如果你想了解更多，可以参考以下资料：
// http://nodejs.cn/api/fs http://nodeapi.ucdok.com/#/api/fs.html

```
```