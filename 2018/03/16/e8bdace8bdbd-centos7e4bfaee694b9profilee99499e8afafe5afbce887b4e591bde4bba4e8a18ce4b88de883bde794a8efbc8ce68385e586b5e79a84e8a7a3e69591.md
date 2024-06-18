---
title: '[转载] Centos7修改profile错误导致命令行不能用，情况的解救方案'
date: '2018-03-16T11:10:04+00:00'
status: publish
permalink: /2018/03/16/%e8%bd%ac%e8%bd%bd-centos7%e4%bf%ae%e6%94%b9profile%e9%94%99%e8%af%af%e5%af%bc%e8%87%b4%e5%91%bd%e4%bb%a4%e8%a1%8c%e4%b8%8d%e8%83%bd%e7%94%a8%ef%bc%8c%e6%83%85%e5%86%b5%e7%9a%84%e8%a7%a3%e6%95%91
author: 毛巳煜
excerpt: ''
type: post
id: 2013
category:
    - CentOS
tag: []
post_format: []
hestia_layout_select:
    - default
---
在改profile的时候，改出问题了，除了cd以外的命令基本都不能用了，  
连vi都不能用了，上网查了下，  
用export PATH=/usr/bin:/usr/sbin:/bin:/sbin:/usr/X11R6/bin，  
然后就可以用命令了，速度用vi把profile改回来，恢复正常。  
shell命令基本都在/usr/bin，/usr/sbin，/bin，/sbin，/usr/X11R6/bin中有定义。  
所以，只要把这些命令重新取出来就能使用了，也算是个补救的办法。

[转载](http://blog.csdn.net/x734400146/article/details/50543886 "转载")