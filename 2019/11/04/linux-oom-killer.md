---
title: 'Linux OOM-killer'
date: '2019-11-04T03:27:19+00:00'
status: publish
permalink: /2019/11/04/linux-oom-killer
author: 毛巳煜
excerpt: ''
type: post
id: 5102
category:
    - Linux服务器
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
- - - - - -

##### 什么是 OOM\_killer

> ###### OOM\_killer 是Linux自我保护的方式，当内存不足时不至于出现太严重问题，在 `kernel 2.6`，内存不足将唤醒 oom\_killer，挑出 `/proc/<pid>/oom_score</pid>` 最大者并将之kill掉

- - - - - -

##### 保护某个进程不被 OOM\_killer

> ###### 为了保护重要进程不被oom-killer掉，我们可以：`echo -17 > /proc/<pid>/oom_adj</pid>` -17表示禁用OOM

- - - - - -

##### 启用/禁用整个系统的 OOM\_killer 策略

> `sysctl -w vm.panic_on_oom=0` （默认为0:表示启用; 1:表示禁用）  
>  使修改生效  
>  `sysctl -p`

- - - - - -

##### 解释

###### **`什么是Overcommit和OOM`**

> ###### Linux对大部分申请内存的请求都回复`"yes"`，以便能跑更多更大的程序。因为申请内存后，并不会马上使用内存。`这种技术叫做 Overcommit`。
> 
> ###### `当linux发现内存不足时`，会发生OOM killer(OOM=out-of-memory)。它会选择杀死一些进程(用户态进程，不是内核线程)，以便释放内存。
> 
> ###### `当oom-killer发生时，linux会选择杀死哪些进程？` 选择进程的函数是oom\_badness函数(在mm/oom\_kill.c中)，该函数会计算每个进程的点数(0~1000)。点数越高，这个进程越有可能被杀死。每个进程的点数跟oom\_score\_adj有关，而且 oom\_score\_adj可以被设置(-1000最低，1000最高)。

- - - - - -

##### 控制进程对内存过量使用的应对策略

1 修改配置

```ruby
[root@dev25 ~]# echo 2 > /proc/sys/vm/overcommit_memory
[root@dev25 ~]#
[root@dev25 ~]# cat /proc/sys/vm/overcommit_memory
2
[root@dev25 ~]#

```

- overcommit\_memory 是一个内核对内存分配的一种策略。 具体可见`/proc/sys/vm/overcommit_memory`下的值
- 当`overcommit_memory=0` 表示即启发式的 overcommitting handle, 会尽量减少swap的使用, root可以分配比一般用户略多的内存 (默认）
- 当`overcommit_memory=1` 表示允许超过 CommitLimit
- 当`overcommit_memory=2` 表示不允许超过 CommitLimit

- - - - - -

2 查看系统 CommitLimit  
**`overcommit_memory`** 参数就是控制分配内存是否可以超过 CommitLimit

```ruby
[root@dev25 ~]# grep -i commit /proc/meminfo
CommitLimit:    16468436 kB
Committed_AS:    3532884 kB
[root@dev25 ~]#

```

- CommitLimit: 是一个内存分配上限;  
  CommitLimit = 物理内存 \* overcommit\_ratio(默认50，`即50%`) + swap大小
- Committed\_AS: 是已经分配的内存大小

- - - - - -

3 配置系统 CommitLimit  
**通过修改`overcommit_ratio`来配置系统 CommitLimit**  
只有当 `vm.overcommit_memory = 2`的时候才会生效

```ruby
[root@dev25 ~]# sysctl -a | grep vm.overcommit_ratio
vm.overcommit_ratio = 50
[root@dev25 ~]#
[root@dev25 ~]# sysctl -w vm.overcommit_ratio=80
vm.overcommit_ratio = 80
[root@dev25 ~]#
[root@dev25 ~]# sysctl -p

```

- - - - - -