---
title: 'SQLServer 常见问题'
date: '2020-02-20T11:32:08+00:00'
status: private
permalink: /2020/02/20/sqlserver-%e5%b8%b8%e8%a7%81%e9%97%ae%e9%a2%98
author: 毛巳煜
excerpt: ''
type: post
id: 5260
category:
    - SQLServer
tag: []
post_format: []
---
###### 1 com.microsoft.sqlserver.jdbc.SQLServerException: 传入的请求具有过多的参数。该服务器支持最多 2100 个参数

- `SqlServer` 对语句的`条数`和`参数`的数量都有限制，分别是 `1000` 和 `2100`。
- `Mysql` 对语句的长度有限制，默认是 `4M`。
- `Mybatis` 对动态语句没有数量上的限制