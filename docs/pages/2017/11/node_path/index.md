---
title: "node_path"
date: "2017-11-16"
categories: 
  - "node-js"
---

```javascript
//////////////////////////===================path优化==================////////////////////////////////
// path模块的基本用法
// 本模块包含一套用于处理和转换文件路径的工具集,用于处理目录的对象，提高用户开发效率，让我们一起来快速的认识path对象的一些常用方法吧！
```

```javascript
// normalize 函数的基本用法
// normalize 函数将不符合规范的路径经过格式化转换为标准路径,解析路径中的.与..外，还能去掉多余的斜杠。
var path = require('path');
var resultData = path.normalize('/path///normalize/hi/..');
console.log(resultData);
```

```javascript
// join 函数的基本用法
// join 函数将传入的多个路径拼接为标准路径并将其格式化，返回规范后的路径，避免手工拼接路径字符串的繁琐
// 如果路径中有 .. 拼接时路径会指定到 ..的 上一级
var resultData = path.join('/mao', '///si', '/yu', 'haha/..');
console.log(resultData);
```

```javascript
// dirname 函数的基本用法
// dirname 函数用来返回路径中的目录名(注意：最后一个永远当成是文件名，所以每次都会取得除最后一个的所有路径, 一次类推结果成递减)
// 实例：递归调用时
// com/grg/ddd/aaa
// com/grg/ddd
// com/grg
// com
var resultData = path.dirname('com/grg/ddd/aaa/bbb');
console.log(resultData);
```

```javascript
// basename 函数的基本用法
// basename 函数可返回路径中的最后一部分，并且可以对其进行条件排除.
// 例1：path.basename('路径字符串');
// 例2：path.basename('路径字符串', '[ext]')<排除[ext]后缀字符串>;
var path = require('path');
var data1 = path.basename('/foo/strong/basename/index.html');
var data2 = path.basename('/foo/strong/basename/index.html', '.html');
console.log(data1 + ' "and" ' + data2);
```

```javascript
// extname 函数的基本用法
// extname 函数返回路径中文件的扩展名(以最后一个'.'开始,返回'.'以及'.'以后的所有字符串,如没有'.',则返回空字符串).
var data = path.extname('index.html');
console.log(data);
```
