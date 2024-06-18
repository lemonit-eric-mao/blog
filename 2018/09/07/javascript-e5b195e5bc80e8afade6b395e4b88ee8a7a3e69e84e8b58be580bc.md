---
title: 'Javascript 展开语法与解构赋值'
date: '2018-09-07T09:33:27+00:00'
status: publish
permalink: /2018/09/07/javascript-%e5%b1%95%e5%bc%80%e8%af%ad%e6%b3%95%e4%b8%8e%e8%a7%a3%e6%9e%84%e8%b5%8b%e5%80%bc
author: 毛巳煜
excerpt: ''
type: post
id: 2345
category:
    - JavaScript
tag: []
post_format: []
wb_sst_seo:
    - 'a:3:{i:0;s:0:"";i:1;s:0:"";i:2;s:0:"";}'
hestia_layout_select:
    - sidebar-right
---
展开语法
----

> 展开语法(Spread syntax), 可以在`函数调用`/`数组构造`时, 将数组表达式或者string在语法层面展开；还可以在构造字面量对象时, 将对象表达式按key-value的方式展开。(译者注: 字面量一般指 `[1, 2, 3]` 或者 `{name: "mdn"}` 这种简洁的构造方式)

```javascript
function sum(x, y, z) {
  return x + y + z;
}

const numbers = [1, 2, 3];

console.log(sum(...numbers));
// expected output: 6

```

[展开语法(Spread syntax)](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Operators/Spread_syntax "展开语法(Spread syntax)")

- - - - - -

### 模拟案例

```javascript
// 将字符打散，相当于把网址加密
var input = 'http://www.baidu.com';
var arrays = [...'abcdefghijklmnopqrstuvwxyz./:'];
var result = [];

for (let i = 0; i  {
        return str == input[i];
    });
    result.push(`\<span class="katex math inline">{str.at(</span>{temp})}`);
}
console.log(result.join(''));

// 输出
// <span class="katex math inline">{str.at(7)}</span>{str.at(19)}<span class="katex math inline">{str.at(19)}</span>{str.at(15)}<span class="katex math inline">{str.at(28)}</span>{str.at(27)}<span class="katex math inline">{str.at(27)}</span>{str.at(22)}<span class="katex math inline">{str.at(22)}</span>{str.at(22)}<span class="katex math inline">{str.at(26)}</span>{str.at(1)}<span class="katex math inline">{str.at(0)}</span>{str.at(8)}<span class="katex math inline">{str.at(3)}</span>{str.at(20)}<span class="katex math inline">{str.at(26)}</span>{str.at(2)}<span class="katex math inline">{str.at(14)}</span>{str.at(12)}

```

**还原**

```javascript
var str = 'abcdefghijklmnopqrstuvwxyz./:';
var temp = `<span class="katex math inline">{str.at(7)}</span>{str.at(19)}<span class="katex math inline">{str.at(19)}</span>{str.at(15)}<span class="katex math inline">{str.at(28)}</span>{str.at(27)}<span class="katex math inline">{str.at(27)}</span>{str.at(22)}<span class="katex math inline">{str.at(22)}</span>{str.at(22)}<span class="katex math inline">{str.at(26)}</span>{str.at(1)}<span class="katex math inline">{str.at(0)}</span>{str.at(8)}<span class="katex math inline">{str.at(3)}</span>{str.at(20)}<span class="katex math inline">{str.at(26)}</span>{str.at(2)}<span class="katex math inline">{str.at(14)}</span>{str.at(12)}`;

console.log(temp);

// 输出
// http://www.baidu.com


```

- - - - - -

- - - - - -

- - - - - -

解构赋值
----

转载: [ECMAScript 6 入门](http://es6.ruanyifeng.com/)

### 解构赋值

使用数组成员对变量赋值时，优先使用解构赋值。

```javascript
const arr = [1, 2, 3, 4];

// bad
const first = arr[0];
const second = arr[1];

// good
const [first, second] = arr;
函数的参数如果是对象的成员，优先使用解构赋值。

// bad
function getFullName(user) {
  const firstName = user.firstName;
  const lastName = user.lastName;
}

// good
function getFullName(obj) {
  const { firstName, lastName } = obj;
}

// best
function getFullName({ firstName, lastName }) {
}

```

如果函数返回多个值，优先使用对象的解构赋值，而不是数组的解构赋值。这样便于以后添加返回值，以及更改返回值的顺序。

```javascript
// bad
function processInput(input) {
  return [left, right, top, bottom];
}

// good
function processInput(input) {
  return { left, right, top, bottom };
}

const { left, right } = processInput(input);

```

- - - - - -

- - - - - -

- - - - - -

- - - - - -

- - - - - -

- - - - - -

**展开语法**（Spread Syntax）和**解构赋值**（Destructuring Assignment）在 JavaScript 中是不同的概念，尽管它们可以在某些情况下进行类似的操作。

> 展开语法是一种操作符（...），用于将一个可迭代对象（例如数组、字符串或类似数组的对象）展开为多个元素，以便在函数调用、数组字面量或对象字面量中使用。它可以用于将数组中的元素展开为函数的参数，或者将一个数组合并到另一个数组中。下面是一些展开语法的示例：

```javascript
const array1 = [1, 2, 3];
const array2 = [4, 5, 6];
const mergedArray = [...array1, ...array2]; // 合并两个数组
console.log(mergedArray); // 输出: [1, 2, 3, 4, 5, 6]

function sum(a, b, c) {
  return a + b + c;
}

const numbers = [1, 2, 3];
console.log(sum(...numbers)); // 将数组展开为函数参数，输出: 6

```

> 解构赋值是一种从数组或对象中提取值并将其赋给变量的语法。它可以使你从数组或对象中轻松地提取数据，并将其赋值给对应的变量。解构赋值使用模式匹配的方式来提取数据。下面是一些解构赋值的示例：

```javascript
const [x, y, z] = [1, 2, 3];
console.log(x); // 输出: 1
console.log(y); // 输出: 2
console.log(z); // 输出: 3

const { name, age } = { name: 'John', age: 30 };
console.log(name); // 输出: 'John'
console.log(age); // 输出: 30

```

> 可以看到，展开语法用于展开一个可迭代对象，而解构赋值用于从数组或对象中提取数据并赋值给变量。它们在语法和使用方式上略有不同，但在某些情况下可以一起使用以实现特定的操作。