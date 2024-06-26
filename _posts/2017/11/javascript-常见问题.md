---
title: "JavaScript 常见问题"
date: "2017-11-16"
categories: 
  - "javascript"
---

##### **如何处理多维数组**

> `flat()` 方法创建一个新的数组，并根据指定深度递归地将所有子数组元素拼接到新的数组中。

```javascript
let arr = [[[1, 2], [3, 4]], [[5, 6], [7, 8]]];

// 默认
arr.flat()
[[1,2],[3,4],[5,6],[7,8]]

// 默认是去掉1层
arr.flat(1)
[[1,2],[3,4],[5,6],[7,8]]

// 去掉2层
arr.flat(2)
[1,2,3,4,5,6,7,8]


// JSON.stringify(arr.flat(2))
// '[1,2,3,4,5,6,7,8]'

```

* * *

* * *

* * *

##### **什么是`词法作用域`**

在这个例子中有三个逐级嵌套的作用域

```javascript
// ------------------------------------- 第 1 级 START
function foo(a) {
    // ========================================= 第 2 级 START
    var b = a * 2;

    function bar(c) {
        // ############################################# 第 3 级 START
        console.log(a, b, c);
        // ############################################# 第 3 级 END
    }

    bar(b * 3);
    // ========================================= 第 2 级 END
}

foo(2); // 2, 4, 12
// ------------------------------------- 第 1 级 END
```

1. **第 1 级** 包含着整个`全局作用域`，其中只有一个标识符： **`foo`**
2. **第 2 级** 包含着 `foo` 所创建的作用域，其中有三个标识符： **`a、bar 和 b`**
3. **第 3 级** 包含着 `bar` 所创建的作用域， 其中只有一个标识符： **`c`**

* * *

##### **什么是`闭包`?**

  只要使用了 **`回调函数`** ， 实际上就是在使用 **`闭包`** ；   如果函数是在 **它本身的词法作用域`以外执行`** 的， 就是在使用 **`闭包`** ；

```javascript
function foo(a) {
    // b 相当于 Java 的 私有变量
    var b = a * 2;
    // bar 相当于 Java 的 私有方法
    function bar(c) {
        console.log(a, b, c);
    }
    // 将私有方法做为返回值
    return bar;
}

var bazz = foo(2); // 得到foo作用域内部的 bar() (私有函数)
// 在bar()函数的， 词法作用域以外执行
bazz(6);           // 2, 4, 6  ----> 这就是闭包的效果
```

* * *

* * *

* * *

##### 模块

```javascript
function CoolModule() {
    var something = 'cool';
    var another = [1, 2, 3];

    function doSomething() {
        console.log('something');
    }

    function doAnother() {
        console.log(another.join(' ! '));
    }

    return {
        doSomething: doSomething,
        doAnother: doAnother
    }
}

var foo = CoolModule();
foo.doSomething();       // something
foo.doAnother();         // 1 ! 2 ! 3
```

这个模式在 JavaScript 中被称为 **`模块`** , 不过这是 ES6 之前的写法

* * *

##### ES6 以后的写法

- **`import`** 会将一个模块中的**一个**或**多个** **`API`** 导入并绑定到一个变量上。
- **`module`** 会将整个模块的 **`API`** 导入并绑定到一个变量上
- **`export`** 会将当前模块的一个标识符导出为 **公共`API`**

###### bar.js

```javascript
function hello(who) {
    return `hello ${who}`;
}

export hello;
```

###### foo.js

```javascript
// 仅从 'bar' 模块导入 hello()
import hello from 'bar'

var foo = 'my foo world!';

function show() {
    console.log(hello(foo).toUpperCase());
}
export show;
```

###### bazz.js

```javascript
// 导入完整的 'bar' 模块
module bar from 'bar'
// 导入完整的 'foo' 模块
module foo from 'foo'

console.log(bar.hello('world!'));  // hello world!
console.log(foo.show());           // HELLO MY FOO WORLD!
```

* * *

* * *

* * *

###### 一条语句排序 在不考虑性能的情况下,使用一条语句排序

```javascript
let numbers = [1, 22, 44, 2, 11, 54, 21, 300];
numbers.forEach(num => {
    setTimeout(() => {
        console.log(num)
    }, num);
});
```

* * *

* * *

* * *

###### Javascript中什么类型是引用传递, 什么类型是值传递? 如何将值类型的变量以引用的方式传递?

**Javascript 中`没有引用传递`只是传递引用(值传递)**

```javascript
// [1] == [1] 是 true 还是 false
// 这是两个数组的比较, 并不是两个数组的值比较
[1] == [1]; // false

// == 的 === 的区别的了解
// == 值比较
// === 同类型同值
1 == '1'; // true
1 === '1'; // false
1 - '1'; // 0
1 * '1'; // 1
1 / '1'; // 1
```

* * *

* * *

* * *

###### const 定义的 Array 中间元素能否被修改? 如果可以, 那 const 修饰对象有什么意义?

  其中的值可以被修改. 意义上, 主要保护引用不被修改 (如用 Map 等接口对引用的变化很敏感, 使用 const 保护引用始终如一是有意义的), 也适合用在 immutable 的场景

* * *

* * *

* * *

##### Switch 的执行原理

自上向下匹配`case:`的内容，如果**匹配到了**就从这个`case`开始一直向下执行到`break;` 如果没有找到`break;`就执行到退出函数。 自上向下匹配`case:`的内容，如果**匹配不到**就从`default:`开始一直向下执行到`break;` 如果没有找到`break;`就执行到退出函数。

* * *

* * *

* * *
