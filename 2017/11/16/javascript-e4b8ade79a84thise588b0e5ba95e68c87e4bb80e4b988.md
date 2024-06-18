---
title: 'JavaScript 中的this到底指什么'
date: '2017-11-16T09:59:33+00:00'
status: publish
permalink: /2017/11/16/javascript-%e4%b8%ad%e7%9a%84this%e5%88%b0%e5%ba%95%e6%8c%87%e4%bb%80%e4%b9%88
author: 毛巳煜
excerpt: ''
type: post
id: 31
category:
    - JavaScript
tag: []
post_format: []
---
### JavaScript 中的this到底指什么

`this是指它所在的作用域被谁执行; 例如: 函数中的this就是谁执行这个函数它就指向谁`  
`一句话 this所在的作用域被谁调用它就指向谁`

### 一道面试题 来说明 this

```
<pre class="line-numbers prism-highlight" data-start="1">```javascript
const TestObj = {
  attr: 'bar',
  method() {
    let self = this;
    (function () {
      console.log('this.attr = ' + this.attr);
      console.log('self.attr = ' + self.attr);
    }());
    console.log('this.attr = ' + this.attr);
    console.log('self.attr = ' + self.attr);
  }
};
TestObj.method();

```
```

### this 在匿名函数中的 与 () ＝&gt; {} 中的不同之处

```
<pre class="line-numbers prism-highlight" data-start="1">```javascript
const obj = {
    getThis: function () {
        return function () {
            console.log(this);
        }
    }
}
obj.getThis()(); // Window

const obj = {
    getThis: function () {
        return () => {
            console.log(this);
        }
    }
}
obj.getThis()(); // obj

```
```

`由此可见， 匿名函数 在浏览器中默认指定的对象是 window， 在node.js中指的是根对象； 箭头函数中是没有this的 所以指的是 有this的 父对象`