---
title: 'HTTP 报文  回车符 与 换行符'
date: '2017-11-16T14:52:29+00:00'
status: publish
permalink: /2017/11/16/http-%e6%8a%a5%e6%96%87-%e5%9b%9e%e8%bd%a6%e7%ac%a6-%e4%b8%8e-%e6%8d%a2%e8%a1%8c%e7%ac%a6
author: 毛巳煜
excerpt: ''
type: post
id: 420
category:
    - 网络基础
tag: []
post_format: []
---
### 回车和换行难道不是一回事儿吗?

先来了解一下 回车的 和 换行的概念

- \*\*回车\*\* \\r 本义是光标重新回到本行开头，r的英文return，控制字符可以写成CR，即Carriage Return
- \*\*换行\*\* \\n 本义是光标往下一行（不一定到下一行行首），n的英文newline，控制字符可以写成LF，即Line Feed

### HTTP 报文

用于 HTTP 协议交互的信息被称为 HTTP 报文。  
客户端请求的叫做 `请求报文`  
服务端响应的叫做 `响应报文`  
HTTP 报文大致可分为报文首部和报文主体两块。两者由最初出现的`空行(CR+LF)`来划分。通常,并不一定要有报文主体。