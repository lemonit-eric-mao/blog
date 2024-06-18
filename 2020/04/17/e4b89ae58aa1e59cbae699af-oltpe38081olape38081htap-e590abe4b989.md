---
title: '业务场景 OLTP、OLAP、HTAP 含义'
date: '2020-04-17T07:08:21+00:00'
status: private
permalink: /2020/04/17/%e4%b8%9a%e5%8a%a1%e5%9c%ba%e6%99%af-oltp%e3%80%81olap%e3%80%81htap-%e5%90%ab%e4%b9%89
author: 毛巳煜
excerpt: ''
type: post
id: 5318
category:
    - 默认
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
wb_sst_seo:
    - 'a:3:{i:0;s:0:"";i:1;s:0:"";i:2;s:0:"";}'
---
- - - - - -

##### **OLTP**【On-Line `Transaction` Processing】 `事务`处理

**(系统主要用于大量`写`操作)**

- 业务场景：涉及到多用户大量并发的操作
- 数据库： 主要用于**事务处理** `增、删、改`
- 数据库选型：`操作型` 数据库

- - - - - -

##### **OLAP**【On-Line `Analytical` Processing】 `分析`处理

**(系统主要用于大量`读`操作)**

- 业务场景：主要是做大量的数据统计操作，例如企业报表
- 数据库： 主要用于**分析处理** `查`
- 数据库选型：`决策型` 数据库

- - - - - -

##### HTAP

- 业务场景：即有大量的数据统计，也有多用户大量并发的操作
- 混合 **OLTP + OLAP**
- 数据库选型：`混合型` 数据库

- - - - - -

[![](http://qiniu.dev-share.top/image/jpg/OLTP-OLAP.jpg)](http://qiniu.dev-share.top/image/jpg/OLTP-OLAP.jpg)

- - - - - -

**[什么是 吞吐量](http://www.dev-share.top/2019/11/07/%e4%bb%80%e4%b9%88%e6%98%af-%e5%90%9e%e5%90%90%e9%87%8f/ "什么是 吞吐量")**