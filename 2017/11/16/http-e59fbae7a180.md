---
title: 'HTTP 基础'
date: '2017-11-16T14:51:04+00:00'
status: publish
permalink: /2017/11/16/http-%e5%9f%ba%e7%a1%80
author: 毛巳煜
excerpt: ''
type: post
id: 414
category:
    - 网络基础
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
[节选自 Egg.js http-基础](https://eggjs.org/zh-cn/basics/controller.htmlhttp-%E5%9F%BA%E7%A1%80)

由于 Controller 基本上是业务开发中唯一和 HTTP 协议打交道的地方，在继续往下了解之前，我们首先简单的看一下 HTTP 协议是怎样的。

如果我们发起一个 HTTP 请求来访问前面例子中提到的 Controller：

```
<pre class=" line-numbers language-ruby">
  ```ruby

   curl -X POST http://localhost:3000/api/posts --data '{"title":"controller", "content": "what is controller"}' --header 'Content-Type:application/json; charset=UTF-8'
  
```
```

通过 curl 发出的 HTTP 请求的内容就会是下面这样的：

```
<pre class=" line-numbers language-ruby">
  ```ruby

   POST /api/posts HTTP/1.1
   Host: localhost:3000
   Content-Type: application/json; charset=UTF-8
   {"title": "controller", "content": "what is controller"}
  
```
```

请求的第一行包含了三个信息，我们比较常用的是前面两个：

- method：这个请求中 method 的值是 `POST`。
- path：值为 `/api/posts`，如果用户的请求中包含 query，也会在这里出现

从第二行开始直到遇到的第一个空行位置，都是请求的 Headers 部分，这一部分中有许多常用的属性，包括这里看到的 Host，Content-Type，还有 `Cookie`，`User-Agent` 等等。在这个请求中有两个头：

- `Host`：我们在浏览器发起请求的时候，域名会用来通过 DNS 解析找到服务的 IP 地址，但是浏览器也会将域名和端口号放在 Host 头中一并发送给服务端。
- `Content-Type`：当我们的请求有 body 的时候，都会有 Content-Type 来标明我们的请求体是什么格式的。  
  之后的内容全部都是请求的 body，当请求是 POST, PUT, DELETE 等方法的时候，可以带上请求体，服务端会根据 Content-Type 来解析请求体。

在服务端处理完这个请求后，会发送一个 HTTP 响应给客户端

```
<pre class=" line-numbers language-ruby">
  ```ruby

   HTTP/1.1 201 Created
   Content-Type: application/json; charset=utf-8
   Content-Length: 8
   Date: Mon, 09 Jan 2017 08:40:28 GMT
   Connection: keep-alive
   {"id": 1}
  
```
```

第一行中也包含了三段，其中我们常用的主要是`响应状态码`，这个例子中它的值是 201，它的含义是在服务端成功创建了一条资源。

和请求一样，从第二行开始到下一个空行之间都是响应头，这里的 Content-Type, Content-Length 表示这个响应的格式是 JSON，长度为 8 个字节。

最后剩下的部分就是这次响应真正的内容。