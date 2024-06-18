---
title: 'ES6 编程风格-模块'
date: '2017-11-16T10:07:46+00:00'
status: publish
permalink: /2017/11/16/es6-%e7%bc%96%e7%a8%8b%e9%a3%8e%e6%a0%bc-%e6%a8%a1%e5%9d%97
author: 毛巳煜
excerpt: ''
type: post
id: 62
category:
    - JavaScript
tag: []
post_format: []
hestia_layout_select:
    - default
---
转载: [ECMAScript 6 入门](http://es6.ruanyifeng.com/)

### 模块

首先，Module语法是JavaScript模块的标准写法，坚持使用这种写法。使用import取代require。

```javascript
// bad
const moduleA = require('moduleA');
const func1 = moduleA.func1;
const func2 = moduleA.func2;

// good
import { func1, func2 } from 'moduleA';

```

使用export取代module.exports。

```javascript
// commonJS的写法
var React = require('react');

var Breadcrumbs = React.createClass({
  render() {
    return <nav></nav>;
  }
});

module.exports = Breadcrumbs;

```

```javascript
// ES6的写法
import React from 'react';

class Breadcrumbs extends React.Component {
  render() {
    return <nav></nav>;
  }
};

export default Breadcrumbs;

```

如果模块只有一个输出值，就使用export default，如果模块有多个输出值，就不使用export default，export default与普通的export不要同时使用。

不要在模块输入中使用通配符。因为这样可以确保你的模块之中，有一个默认输出（export default）。

```javascript
// bad
import * as myObject './importModule';

// good
import myObject from './importModule';

```

如果模块默认输出一个函数，函数名的首字母应该小写。

```javascript
function makeStyleGuide() {
}

export default makeStyleGuide;

```

如果模块默认输出一个对象，对象名的首字母应该大写。

```javascript
const StyleGuide = {
  es6: {
  }
};

export default StyleGuide;

```