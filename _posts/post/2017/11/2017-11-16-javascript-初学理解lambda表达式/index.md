---
title: "JavaScript 初学理解lambda表达式"
date: "2017-11-16"
categories: 
  - "javascript"
---

```
 lambda表达式
 lambda表达式用法主要是针对 代码的回调函数做了简化写法儿;
 初学时的理解方式
 为了不让lambda表达式的灵活变化用法给弄晕可以这样记
 左边是方法的参数, 右边是方法的方法体;
// java中:
参数 -> 方法体
() -> {}

// javascript中:
参数 => 方法体
() => {}

一开始保持这种习惯应用lambda表达式就不会晕了, 至于后期的
() 参数小括号的省略
{} 方法体花括号的省略

慢慢的在应用中去体会去习惯;
```

## 使用注意点

##### 箭头函数有几个使用注意点。

```javascript
（1）函数体内的this对象，绑定定义时所在的对象，而不是使用时所在的对象。

（2）不可以当作构造函数，也就是说，不可以使用new命令，否则会抛出一个错误。

（3）不可以使用arguments对象，该对象在函数体内不存在。如果要用，可以用Rest参数代替。

（4）不可以使用yield命令，因此箭头函数不能用作Generator函数。
```

##### this对象的指向是可变的，但是在箭头函数中，它是固定的。

```javascript
function Timer () {
  this.seconds = 0
  setInterval(() => this.seconds++, 1000);
}
var timer = new Timer();
setTimeout(() => console.log(timer.seconds), 3100);
// 3
```

##### 上面代码中，Timer函数内部的setInterval-调用了\_this.seconds-属性，通过箭头函数将\_this绑定在Timer的实例对象。否则，输出结果是0，而不是3。
