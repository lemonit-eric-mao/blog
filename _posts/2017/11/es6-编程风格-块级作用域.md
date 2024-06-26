---
title: "ES6 编程风格-块级作用域"
date: "2017-11-16"
categories: 
  - "javascript"
---

转载: [ECMAScript 6 入门](http://es6.ruanyifeng.com/)

### 块级作用域

（1）let 取代 var

ES6提出了两个新的声明变量的命令：let和const。其中，let完全可以取代var，因为两者语义相同，而且let没有副作用。

```javascript
'use strict';

if (true) {
    let x = 'hello';
}

for (let i = 0; i < 10; i++) {
    console.log(i);
}
```

上面代码如果用**var替代let**，实际上就声明了两个全局变量，这显然不是本意。变量应该只在其声明的代码块内有效，var命令做不到这一点。

**var** 命令存在变量提升效用，**let** 命令没有这个问题。

```javascript
'use strict';

if (true) {
    console.log(x); // ReferenceError
    let x = 'hello';
}
```

上面代码如果使用var替代let，console.log那一行就不会报错，而是会输出undefined，因为变量声明提升到代码块的头部。这违反了变量先声明后使用的原则。

所以，建议不再使用var命令，而是使用let命令取代。
