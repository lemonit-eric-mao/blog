---
title: 'Javascript 的函数对象'
date: '2018-11-12T15:24:35+00:00'
status: publish
permalink: /2018/11/12/javascript-%e7%9a%84%e5%87%bd%e6%95%b0%e5%af%b9%e8%b1%a1
author: 毛巳煜
excerpt: ''
type: post
id: 3297
category:
    - JavaScript
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
```javascript
/**
 * Created by mao_siyu on 2018/11/12.
 */
// 下面两行代码的作用是一样的，都是创建一个数组对象myArray：
var myArray = [];
// 等价于
var myArray = new Array();

// ==============================================================

// 同样，下面的两段代码也是等价的，都是创建一个函数myFunction：
function myFunction(a, b) {
    return a + b;
}
// 等价于
var myFunction = new Function('a', 'a', 'return a + b');

/**
 * 解释：
 * 函数声明是上述代码的第一种方式，而在解释器内部，当遇到这种带有function的语法时，
 * 就会自动构造一个Function 对象，将函数作为一个内部的对象来存储和运行。
 *
 * 没有人通过new Function()的形式来创建一个函数，是因为一个函数体通常会有多条语句，
 * 如果将它们以一个字符串的形式作为参数传递，那么代码的可读性会非常的差。
 *
 * var funcName = new Function(p1, p2, ..., pn, body);
 * 参数的类型都是字符串，p1 到 pn表示所创建函数的参数名称列表，
 * body表示所创建函数的函数体语句， 而funcName就是所创建函数的名称了。
 */


// 尽管下面两种创建函数的方法是等价的：
function funcName() {
}
// 等价于
var funcName = function () {
}
/**
 * 解释：
 * 但前面一种方式创建的是有名函数，而后面是创建了一个无名函数，只是让一个变量指向了这个无名函数。
 * 在使用上仅有一点区别，就是：
 * 对于有名函数，它可以出现在调用之后再定义；
 * 而对于无名函数，它必须是在调用之前就已经定义。
 */

// 正确执行
func1();
function func1() {
}

// 这段语句将产生 func2 is not a function
func2();
var func2 = function () {
}
// 错误原因等价于
var func2;
func2();
func2 = function () {
}

```