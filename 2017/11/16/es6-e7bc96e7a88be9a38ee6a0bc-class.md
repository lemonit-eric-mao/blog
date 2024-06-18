---
title: 'ES6 编程风格-Class'
date: '2017-11-16T10:07:16+00:00'
status: publish
permalink: /2017/11/16/es6-%e7%bc%96%e7%a8%8b%e9%a3%8e%e6%a0%bc-class
author: 毛巳煜
excerpt: ''
type: post
id: 60
category:
    - JavaScript
tag: []
post_format: []
hestia_layout_select:
    - default
---
转载: [ECMAScript 6 入门](http://es6.ruanyifeng.com/)

### **Class**

总是用Class，取代需要prototype的操作。因为Class的写法更简洁，更易于理解。

```javascript
// bad
function Queue(contents = []) {
  this._queue = [...contents];
}
Queue.prototype.pop = function() {
  const value = this._queue[0];
  this._queue.splice(0, 1);
  return value;
}

// good
class Queue {
  constructor(contents = []) {
    this._queue = [...contents];
  }
  pop() {
    const value = this._queue[0];
    this._queue.splice(0, 1);
    return value;
  }
}

```

使用**extends**实现继承，因为这样更简单，不会有破坏**instanceof**运算的危险。

```javascript
// bad
const inherits = require('inherits');
function PeekableQueue(contents) {
  Queue.apply(this, contents);
}
inherits(PeekableQueue, Queue);
PeekableQueue.prototype.peek = function() {
  return this._queue[0];
}

// good
class PeekableQueue extends Queue {
  peek() {
    return this._queue[0];
  }
}

```