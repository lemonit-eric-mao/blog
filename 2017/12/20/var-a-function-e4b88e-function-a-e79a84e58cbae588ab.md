---
title: 'var A = function() {} 与 function A() {}   的区别'
date: '2017-12-20T15:28:06+00:00'
status: publish
permalink: /2017/12/20/var-a-function-%e4%b8%8e-function-a-%e7%9a%84%e5%8c%ba%e5%88%ab
author: 毛巳煜
excerpt: ''
type: post
id: 1760
category:
    - JavaScript
tag: []
post_format: []
---
##### 创建一个变量 并赋给这个变量一个匿名函数对象

```
<pre class="line-numbers prism-highlight" data-start="1">```javascript
var A = function() {}

```
```

##### 创建一个常量 并赋给这个变量一个匿名函数对象

```
<pre class="line-numbers prism-highlight" data-start="1">```javascript
// 使用 var 创建的对象 还可以被替换成任意的对象 为了避免创建的这个对象被修改 使用 const 来创建
const A = function() {}

```
```

##### 创建一个名为A的函数对象

```
<pre class="line-numbers prism-highlight" data-start="1">```javascript
function A() {}

```
```

- - - - - -

- - - - - -

- - - - - -

##### 匿名函数 与 直接声明函数 的区别

`var 与 function的声明是不同的, var的声明会让变量声明提升到作用域顶部, 但是变量的赋值还是在原位, 而function的声明, 会全部提升到顶部执行。<br></br>js预编译时，会扫描作用域， 将作用域内的函数声明提升到作用域顶部。而执行代码还在原位。`

```
<pre class="line-numbers prism-highlight" data-start="1">```javascript
A();
var A = function() {console.log('init')}
Uncaught TypeError: A is not a function
    at <anonymous>:1:1

////////////////////////////////////////

A();
function A() {console.log('init')}
init // 输出了 init
</anonymous>
```
```

- - - - - -

- - - - - -

- - - - - -

##### 以下是在chrome 浏览器控制台 做的输出测试

```
<pre class="line-numbers prism-highlight" data-start="1">```javascript
console.log(A());
function A() {
    return 'init';
}
init // 输出了 init

```
```

##### var 声明的变量会提升到作用域顶部, 但是变量的赋值还是在原位

```
<pre class="line-numbers prism-highlight" data-start="1">```javascript
console.log(A);
console.log(A());
var A = function() {
    return 'init';
}
undefined // 输出了 undefined
Uncaught TypeError: A is not a function
    at <anonymous>:1:13

// 上面的这种写法相当于

var A;
console.log(A);
console.log(A());
A = function() {
    return 'init'
}
undefined // console.log 输出了 undefined， 所以在A为 undefined时 A()相当于undefined()
Uncaught TypeError: A is not a function
    at <anonymous>:3:13
</anonymous></anonymous>
```
```

##### const 必须初始化， 被修饰的对象 内存地址是不可变的 （即： 对象不可更改， 内容可以更改）

```
<pre class="line-numbers prism-highlight" data-start="1">```javascript
console.log(A());
const A = function() {
    return 'init';
}
Uncaught ReferenceError: A is not defined
    at <anonymous>:1:13
</anonymous>
```
```