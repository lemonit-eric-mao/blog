---
title: '什么是 CDN?'
date: '2021-02-02T13:52:40+00:00'
status: private
permalink: /2021/02/02/%e4%bb%80%e4%b9%88%e6%98%af-cdn
author: 毛巳煜
excerpt: ''
type: post
id: 6864
category:
    - 自学整理
tag: []
post_format: []
---
###### 内容分发网络（Content Delivery Network，简称CDN）

1. 用户请求全局DNS域名
2. 全局DNS会通过用户请求过来的IP地址，计算出地理位置
3. 根据地理位置选择最近的服务器
4. **个人理解，就是在内部做了一次对各个节点的网速测试操作，然后选出网速最快、最稳定的一个链路去请求**
5. 然后记录这个请求(**记录请求的ip与目标的ip进行缓存**)，下次在有相同的ip地址访问，就不需要在进行网速测试了
6. **`CDN解决了链路长短的问题，起到了请求响应上的优化`**

[![](http://qiniu.dev-share.top/image/%E4%BB%80%E4%B9%88%E6%98%AFCDN.png)](http://qiniu.dev-share.top/image/%E4%BB%80%E4%B9%88%E6%98%AFCDN.png)