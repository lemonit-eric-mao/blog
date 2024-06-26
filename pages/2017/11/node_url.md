---
title: "node_url"
date: "2017-11-16"
categories: 
  - "node-js"
---

```javascript
//////////////////////////===================url处理==================////////////////////////////////
// url模块的基本用法
// node.js为互联网而生，和url打交道是无法避免的了，url模块提供一些基础的url处理。
console.log('\n=====================================================================\n');


// parse函数的基础用法
// parse函数的作用是解析url，返回一个json格式的数组
var url = require('url');
var resultData = url.parse('http://www.hubwiz.com');
console.log(resultData);


console.log('\n=====================================================================\n');


// parse函数 —— 条件解析
// parse函数的第二个参数是布尔类型，当参数为true时，会将查询条件也解析成json格式的对象。
// 当参数为true时 query: { page: '1' },
// 当参数为false时 query: 'page=1',
var resultData = url.parse('http://www.baidu.com?page=1', false);
console.log(resultData);


console.log('\n=====================================================================\n');


// parse函数 —— 解析主机
// parse函数的第三个参数也是布尔类型的，当参数为true，解析时会将url的"//"和第一个"/"之间的部分解析为主机名
var resultData = url.parse('http://www.baidu.com?page=1', false, true);
console.log(resultData);


console.log('\n=====================================================================\n');


// format函数的基础用法
// format函数的作用与parse相反，它的参数是一个JSON对象，返回一个组装好的url地址，请看如下示例：
var resultData = url.format({
    protocol: 'http:',
    hostname: 'www.baidu.com',
    port: '80',
    pathname: '/news',
    query: { page: 1 }
});
console.log(resultData);
// 运行结果：
// http://www.baidu.com/news?page=1
// 参数JSON对象的字段跟parse函数解析后返回的JSON字段一一对应。


console.log('\n=====================================================================\n');


// resolve函数的基础用法
// resolve函数的参数是两个路径，第一个路径是开始的路径或者说当前路径，第二个则是想要去往的路径，返回值是一个组装好的url，示例如下：
var one = url.resolve('http://example.com/', '/one') // 'http://example.com/one'
var two = url.resolve('http://example.com/one', '/two') // 'http://example.com/two'
console.log(one);
console.log(two);


console.log('\n=====================================================================\n');
```
