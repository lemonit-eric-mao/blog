---
title: "[转载] Centos7修改profile错误导致命令行不能用，情况的解救方案"
date: "2018-03-16"
categories: 
  - "centos"
---

在改profile的时候，改出问题了，除了cd以外的命令基本都不能用了， 连vi都不能用了，上网查了下， 用export PATH=/usr/bin:/usr/sbin:/bin:/sbin:/usr/X11R6/bin， 然后就可以用命令了，速度用vi把profile改回来，恢复正常。 shell命令基本都在/usr/bin，/usr/sbin，/bin，/sbin，/usr/X11R6/bin中有定义。 所以，只要把这些命令重新取出来就能使用了，也算是个补救的办法。

[转载](http://blog.csdn.net/x734400146/article/details/50543886 "转载")
