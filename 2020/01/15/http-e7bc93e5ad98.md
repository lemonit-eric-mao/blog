---
title: 'HTTP 缓存'
date: '2020-01-15T02:53:30+00:00'
status: publish
permalink: /2020/01/15/http-%e7%bc%93%e5%ad%98
author: 毛巳煜
excerpt: ''
type: post
id: 5235
category:
    - 网络基础
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
##### 个人理解

 通俗的讲，`http缓存`就是为了减少`浏览器`向`服务器`端`获取资源的请求次数`而实现的优化方案，此方案通过减少频繁向服务器发起请求而对服务器造成的压力。以下是讲解通过配置`HTTP头部`参数来实现`http缓存规则`的工作原理

- - - - - -

##### 一、http缓存请求相应头

###### **1. Cache-Control**

 请求/响应头，缓存控制字段，可以说是控制http缓存的最高指令，要不要缓存也是它说了算。它有以下常用值：

<table><thead><tr><th>序号</th><th>**Cache-Control** 属性</th><th>解释</th></tr></thead><tbody><tr><td>1.1</td><td>**no-store：**</td><td> 所有内容都不缓存</td></tr><tr><td>1.2</td><td>**no-cache：**</td><td> `缓存，但是浏览器使用缓存前，都会请求服务器判断缓存资源是否是最新，它是个比较高贵的存在，因为它只用不过期的缓存。`</td></tr><tr><td>1.3</td><td>**max-age=x：**</td><td> 请求缓存后的X秒不再发起请求，属于http1.1属性，与下方Expires(http1.0属性)类似，但优先级要比Expires高。(单位秒)</td></tr><tr><td>1.4</td><td>**s-maxage=x：**</td><td> 代理服务器请求源站缓存后的X秒不再发起请求，只对CDN缓存有效(这个在后面会细说)(单位秒)</td></tr><tr><td>1.5</td><td>**public:**</td><td> 客户端和代理服务器(CDN)都可缓存</td></tr><tr><td>1.6</td><td>**private:**</td><td> 只有客户端可以缓存</td></tr></tbody></table>

###### **2. Expires**

 响应头，代表资源过期时间，由服务器返回提供，GMT格式日期，是http1.0的属性，在与`max-age(http1.1)`共存的情况下，优先级要低。

###### **3. Last-Modified**

 响应头，资源最新修改时间，由服务器告诉浏览器。

###### **4. if-Modified-Since**

 请求头，资源最新修改时间，由浏览器告诉服务器(其实就是上次服务器给的Last-Modified，请求又还给服务器对比)，和Last-Modified是一对，它两会进行对比。

###### **5. Etag**

 响应头，资源标识，由服务器告诉浏览器。  
**6. if-None-Match**  
 请求头，缓存资源标识，由浏览器告诉服务器(其实就是上次服务器给的Etag)，和Etag是一对，它两会进行对比。

- - - - - -

##### 二、为什么要使用HTTP缓存

 假设我们请求一次服务器，请求头大小1kb，响应头大小1kb，请求文件10kb。  
1次请求流量：`12kb`  
10次请求流量：**120kb**  
N次请求：**12\*N....**

 这只是假想的一次请求，但事实上的请求不仅是请求文件，请求客户端也会更多，那么问题就很明显：

1.客户端每次都要请求服务器，浪费流量(比如手机端？)。  
2.服务器每次都得提供查找，下载，请求用户基础如果较大，服务器存在较大压力。  
3.客户端每次请求完都要进行页面渲染，用户体验较差。

 那么我们是否可以将请求的文件存放起来使用，比如使用`http缓存`。

- - - - - -

###### **更详细的解释请参考[原文链接](https://www.cnblogs.com/echolun/p/9419517.html "原文链接")**

###### **[fiddler 下载](https://www.telerik.com/download/fiddler "fiddler 下载")**

- - - - - -