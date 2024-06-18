---
title: 'CommonJs 规范理解 exports 与 module.exports'
date: '2017-11-16T12:36:13+00:00'
status: publish
permalink: /2017/11/16/commonjs-%e8%a7%84%e8%8c%83%e7%90%86%e8%a7%a3-exports-%e4%b8%8e-module-exports
author: 毛巳煜
excerpt: ''
type: post
id: 182
category:
    - node.js
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
###### **CommonJS 模块的加载原理**

CommonJs 规范规定，每个模块内部，module变量代表当前模块。这个变量是一个对象，它的 exports属性（即module.exports）是对外的接口，加载某个模块，其实是加载该模块的module.exports属性。

```javascript
const x = 5;
const addX = function (value) {
  return value + x;
};
module.exports.x = x;
module.exports.addX = addX;

```

上面代码通过module.exports输出变量x和函数addX。

**require方法用于加载模块。**

```javascript
const example = require('./example.js');

console.log(example.x); // 5
console.log(example.addX(1)); // 6

```

**CommonJS 模块的特点如下：**

- 所有代码运行在模块作用域，不会污染全局作用域
- 模块可以多次加载，但是只会在第一次加载时运行一次，然后运行结果就被缓存了，以后再加载，就直接读取缓存结果。要想让模块再次运行，必须清除缓存。
- 模块加载的顺序，按照其在代码中出现的顺序

- - - - - -

###### **module对象**

Node内部提供一个Module构建函数。所有模块都是Module的实例。

```javascript
function Module(id, parent) {
  this.id = id;
  this.exports = {};
  this.parent = parent;
  // ...
}

```

**每个模块内部，都有一个module对象，代表当前模块。它有以下属性:**

- module.id 模块的识别符，通常是带有绝对路径的模块文件名。
- module.filename 模块的文件名，带有绝对路径。
- module.loaded 返回一个布尔值，表示模块是否已经完成加载。
- module.parent 返回一个对象，表示调用该模块的模块。
- module.children 返回一个数组，表示该模块要用到的其他模块。
- module.exports 表示模块对外输出的值。
- module.exports属性表示当前模块对外输出的接口，其他文件加载该模块，实际上就是读取module.exports变量。

为了方便，Node为每个模块提供一个exports变量，指向module.exports。这等同在每个模块头部，有一行这样的命令

```javascript
const exports = module.exports;

```

注意，不能直接将exports变量指向一个值，因为这样等于切断了exports与module.exports的联系。

```javascript
exports = function(x) {console.log(x)};

```

上面这样的写法是无效的，因为exports不再指向module.exports了。

- - - - - -

- - - - - -

- - - - - -

**[原文链接](https://segmentfault.com/a/1190000021911869 "原文链接")**

- - - - - -

- - - - - -

- - - - - -