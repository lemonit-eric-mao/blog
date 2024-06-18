---
title: 'JavaScript 原生 XHR 与 Ajax 的实现原理'
date: '2017-12-20T22:25:01+00:00'
status: publish
permalink: /2017/12/20/javascript-%e5%8e%9f%e7%94%9f-xhr-%e4%b8%8e-ajax-%e7%9a%84%e5%ae%9e%e7%8e%b0%e5%8e%9f%e7%90%86
author: 毛巳煜
excerpt: ''
type: post
id: 1777
category:
    - JavaScript
tag: []
post_format: []
hestia_layout_select:
    - default
---
#### **XMLHttpRequest是一个浏览器接口，使得Javascript可以进行HTTP(S)通信。**

#### **最早，微软在IE 5引进了这个接口。因为它太有用，其他浏览器也模仿部署了，ajax操作因此得以诞生。**

#### **但是，这个接口一直没有标准化，每家浏览器的实现或多或少有点不同。**

#### **HTML 5的概念形成后，W3C开始考虑标准化这个接口。2008年2月，就提出了XMLHttpRequest Level 2 草案。**

```javascript
/**
 * js原生 XHR 与 Ajax 的实现原理
 * Created by mao_siyu on 2017/12/20.
 */
const xhr = new XMLHttpRequest();
xhr.onreadystatechange = function () {
    console.log(`
        xhr.readyState: <span class="katex math inline">{xhr.readyState}
        xhr.statusText:</span>{xhr.statusText}
        xhr.response: ${xhr.response}
    `);
}
// xhr.open(method, url, async, user, password);
// xhr.open(访问类型, url, 请求是否异步处理, user, password);
// async = true 表示脚本会在 send() 方法之后继续执行，而不等待来自服务器的响应。
// username 和 password 参数是可选的，为 url 所需的授权提供认证资格。如果指定了，它们会覆盖 url 自己指定的任何资格。
xhr.open('GET', 'http://localhost:8060/', true);
xhr.send({body: 'json-data'});

```

- - - - - -

- - - - - -

- - - - - -

### 属性

##### readyState

`HTTP 请求的状态.当一个 XMLHttpRequest 初次创建时，这个属性的值从 0 开始，直到接收到完整的 HTTP 响应，这个值增加到 4。<br></br>5 个状态中每一个都有一个相关联的非正式的名称<br></br>0    Uninitialized    初始化状态。XMLHttpRequest 对象已创建或已被 abort() 方法重置。<br></br>1    Open             open() 方法已调用，但是 send() 方法未调用。请求还没有被发送。<br></br>2    Sent             Send() 方法已调用，HTTP 请求已发送到 Web 服务器。未接收到响应。<br></br>3    Receiving        所有响应头部都已经接收到。响应体开始接收但未完成。<br></br>4    Loaded           HTTP 响应已经完全接收。<br></br>readyState 的值不会递减，除非当一个请求在处理过程中的时候调用了 abort() 或 open() 方法。<br></br>每次这个属性的值增加的时候，都会触发 onreadystatechange 事件句柄。`

##### status

`由服务器返回的 HTTP 状态代码，如 200 表示成功，而 404 表示 "Not Found" 错误。<br></br>当 readyState 小于 3 的时候读取这一属性会导致一个异常。`

##### statusText

`这个属性用名称而不是数字指定了请求的 HTTP 的状态代码。也就是说，当状态为 200 的时候它是 "OK"，当状态为 404 的时候它是 "Not Found"。<br></br>和 status 属性一样，当 readyState 小于 3 的时候读取这一属性会导致一个异常。`

- - - - - -

- - - - - -

- - - - - -

### 方法

##### abort()

取消当前响应，关闭连接并且结束任何未决的网络活动。

##### getAllResponseHeaders()

把 HTTP 响应头部作为未解析的字符串返回。

##### getResponseHeader()

返回指定的 HTTP 响应头部的值。其参数是要返回的 HTTP 响应头部的名称。

##### setRequestHeader()

向一个打开但未发送的请求设置或添加一个 HTTP 请求头。

### 事件句柄

##### onreadystatechange

每次 readyState 属性改变的时候调用的事件句柄函数。当 readyState 为 3 时，它也可能调用多次。

### `以上使用的技术方案是 旧的 XMLHttpRequest`

- - - - - -

- - - - - -

- - - - - -

### XMLHttpRequest Level 2

###### 新版本的XMLHttpRequest对象 举例其中之一

###### 测试 HTTP请求的时限

```javascript
const xhr = new XMLHttpRequest();
xhr.timeout = 1;
xhr.ontimeout = function(event) {
    alert('请求超时！');
}
xhr.open('GET', 'https://www.baidu.com/', true);
xhr.send({body: 'json-data'});

```

[参考阮一峰博客](http://www.ruanyifeng.com/blog/2012/09/xmlhttprequest_level_2.html "新版本的XMLHttpRequest对象")