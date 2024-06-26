---
title: "node.js require分析"
date: "2017-11-16"
categories: 
  - "node-js"
---

## require('');

require 用来加载一个文件的代码，关于 require 的机制这里不展开讲解，请仔细阅读 官方文档。

#### 简单概括以下几点:

require 可加载 .js、.json 和 .node 后缀的文件

```javascript
require 的过程是同步的，所以这样是错误的:
setTimeout(() => {
  module.exports = { a: 'hello' };
}, 0);
```

```javascript
require 这个文件得到的是空对象 {}

require 目录的机制是:
如果目录下有 package.json 并指定了 main 字段，则用之
如果不存在 package.json，则依次尝试加载目录下的 index.js 和 index.node
require 过的文件会加载到缓存，所以多次 require 同一个文件（模块）不会重复加载
判断是否是程序的入口文件有两种方式:
require.main === module（推荐）
module.parent === null
```

#### 循环引用

```javascript
循环引用（或循环依赖）简单点来说就是
a 文件 require 了 b 文件，
然后 b 文件又反过来 require 了 a 文件。
我们用 a->b 代表 b require 了 a。

简单的情况:
a->b
b->a

复杂点的情况:
a->b
b->c
c->a
循环引用并不会报错，导致的结果是 require 的结果是空对象 {}，
原因是
b require 了 a，
a 又去 require 了 b，
此时 b 还没初始化好，
所以只能拿到初始值 {}。

当产生循环引用时一般有两种方法解决：
通过分离共用的代码到另一个文件解决，如上面简单的情况，可拆出共用的代码到 c 中，如下:
c->a
c->b
不在最外层 require，在用到的地方 require，通常在函数的内部
总的来说，循环依赖的陷阱并不大容易出现，但一旦出现了，对于新手来说还真不好定位。
它的存在给我们提了个醒，要时刻注意你项目的依赖关系不要过于复杂，
哪天你发现一个你明明已经 exports 了的方法报 undefined is not a function，
我们就该提醒一下自己：哦，也许是它来了。
```

#### require 用来加载代码，而 exports 和 module.exports 则用来导出代码。

很多新手可能会迷惑于 exports 和 module.exports 的区别，为了更好的理解 exports 和 module.exports 的关系，我们先来巩固下 js 的基础。示例：

test.js

```javascript
var a = {name: 1};
var b = a;

console.log(a);
console.log(b);

b.name = 2;
console.log(a);
console.log(b);

var b = {name: 3};
console.log(a);
console.log(b);
运行 test.js 结果为：

{ name: 1 }
{ name: 1 }
{ name: 2 }
{ name: 2 }
{ name: 2 }
{ name: 3 }

解释：a 是一个对象，b 是对 a 的引用，即 a 和 b 指向同一块内存，所以前两个输出一样。
当对 b 作修改时，即 a 和 b 指向同一块内存地址的内容发生了改变，所以 a 也会体现出来，
所以第三四个输出一样。当 b 被覆盖时，b 指向了一块新的内存，a 还是指向原来的内存，
所以最后两个输出不一样。
```

#### 明白了上述例子后，我们只需知道三点就知道 exports 和 module.exports 的区别了：

```javascript
module.exports 初始值为一个空对象 {}
exports 是指向的 module.exports 的引用
require() 返回的是 module.exports 而不是 exports
Node.js 官方文档的截图证实了我们的观点:
```

![](images/2.2.1.png)

```javascript
exports = module.exports = {...}

我们经常看到这样的写法：

exports = module.exports = {...}
上面的代码等价于:

module.exports = {...}
exports = module.exports
原理很简单：module.exports 指向新的对象时，exports 断开了与 module.exports 的引用，
那么通过 exports = module.exports 让 exports 重新指向 module.exports。
```
