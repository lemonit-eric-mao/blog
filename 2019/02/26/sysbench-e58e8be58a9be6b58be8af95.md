---
title: 'sysbench 压力测试'
date: '2019-02-26T10:22:39+00:00'
status: publish
permalink: /2019/02/26/sysbench-%e5%8e%8b%e5%8a%9b%e6%b5%8b%e8%af%95
author: 毛巳煜
excerpt: ''
type: post
id: 3477
category:
    - 测试工具
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
##### 运行环境

###### 查看操作系统

```ruby
[tidb@dev10 ~]<span class="katex math inline">more /etc/redhat-release
CentOS Linux release 7.6.1810 (Core)
[tidb@dev10 ~]</span>

```

- - - - - -

###### 查看 CPU

```ruby
[tidb@dev10 ~]<span class="katex math inline">lscpu
Architecture:          x86_64
CPU op-mode(s):        32-bit, 64-bit
Byte Order:            Little Endian
CPU(s):                8
On-line CPU(s) list:   0-7
Thread(s) per core:    1
Core(s) per socket:    4
座：                 2
NUMA 节点：         1
厂商 ID：           GenuineIntel
CPU 系列：          6
型号：              79
型号名称：        Intel(R) Xeon(R) CPU E5-2650 v4 @ 2.20GHz
步进：              1
CPU MHz：             2194.917
BogoMIPS：            4389.83
超管理器厂商：  VMware
虚拟化类型：     完全
L1d 缓存：          32K
L1i 缓存：          32K
L2 缓存：           256K
L3 缓存：           30720K
NUMA 节点0 CPU：    0-7
......
[tidb@dev10 ~]</span>

```

- - - - - -

##### sysbench 是什么？

```
github： https://github.com/akopytov/sysbench
sysbench 是一款压力测试工具，可以测试系统的硬件性能，也可以用来对数据库进行基准测试

```

**它主要包括以下几种方式的测试：**

<table><thead><tr><th>序号</th><th>支持</th><th>说明</th></tr></thead><tbody><tr><td>1</td><td>cpu</td><td>处理器性能</td></tr><tr><td>2</td><td>threads</td><td>线程调度器性</td></tr><tr><td>3</td><td>mutex</td><td>互斥锁性能</td></tr><tr><td>4</td><td>memory</td><td>内存分配及传输速度</td></tr><tr><td>5</td><td>fileio</td><td>文件IO性能</td></tr><tr><td>6</td><td>oltp</td><td>数据库性能(OLTP基准测试)</td></tr></tbody></table>

- - - - - -

###### 添加 Sysbench支持

```
如果是 mysql数据库 则需要安装 mysql-devel
如果是 maria数据库 则需要安装 mariadb-devel
因为 sysbench 运行时会用到数据库的驱动，所以本地必须要安装同样的数据库

```

```ruby
[root@dev10 ~]<span class="katex math inline">yum install -y make automake libtool pkgconfig libaio-devel
[root@dev10 ~]</span>
[root@dev10 ~]$ yum install -y mariadb-devel

```

###### 下载安装

```ruby
[root@dev10 ~]<span class="katex math inline">[root@dev10 ~]</span> curl -s https://packagecloud.io/install/repositories/akopytov/sysbench/script.rpm.sh | sudo bash
[root@dev10 ~]<span class="katex math inline">[root@dev10 ~]</span> sudo yum install -y sysbench
[root@dev10 ~]<span class="katex math inline"># 查看版本
[root@dev10 ~]</span> sysbench --version
sysbench 1.0.16
[root@dev10 ~]<span class="katex math inline"># 查看安装目录
[root@dev10 ~]</span> find / -name sysbench
/usr/bin/sysbench
/usr/share/sysbench         # 默认会安装到这个目录
[root@dev10 ~]<span class="katex math inline"># 查看常用的测试脚本文件
[root@dev10 ~]</span> ls /usr/share/sysbench/oltp_read_write.lua
/usr/share/sysbench/oltp_read_write.lua
[root@dev10 ~]$

```

- - - - - -

- - - - - -

- - - - - -

##### **`开始压力测试`**

###### 1 测试数据导入

###### 1.1 创建配置文件

```ruby
[root@dev10 ~]$ cat > config 
```

###### 1.2 导入数据

- **`--tables=1`** 创建测试表数量，1等于 1张表
- **`--table_size=10000`** 每张测试表的数据量，1等于 1条数据

```ruby
[root@dev10 ~]<span class="katex math inline">sysbench --config-file=config /usr/share/sysbench/oltp_common.lua --tables=1 --table-size=10000 prepare
sysbench 1.0.17 (using system LuaJIT 2.0.4)

Initializing worker threads...

Creating table 'sbtest1'...
Creating a secondary index on 'sbtest1'...
Inserting 10000 records into 'sbtest1'

[root@dev10 ~]</span>

```

###### 1.3 开始压测

```ruby
[root@dev10 ~]<span class="katex math inline">sysbench --config-file=config /usr/share/sysbench/oltp_common.lua --tables=1 --table-size=10000 run
sysbench 1.0.17 (using system LuaJIT 2.0.4)

Running the test with following options:
Number of threads: 16
Report intermediate results every 10 second(s)
Initializing random number generator from current time


Initializing worker threads...

Threads started!

SQL statistics:
    queries performed:
        read:                            0                         # 读总数
        write:                           5000                      # 写总数
        other:                           0                         # 其他操作总数(增、删、改、查之外的操作，例如COMMIT等)
        total:                           5000                      # 全部总数
    transactions:                        5000   (579.22 per sec.)  # 总事务数(每秒事务数)
    queries:                             5000   (579.22 per sec.)
    ignored errors:                      0      (0.00 per sec.)
    reconnects:                          0      (0.00 per sec.)

General statistics:
    total time:                          8.6300s                   # 总耗时
    total number of events:              5000                      # 共发生多少事务数

Latency (ms):
         min:                                   15.15              # 最小耗时
         avg:                                   27.57              # 平均耗时
         max:                                   63.24              # 最大耗时
         95th percentile:                       33.72              # 超过95%平均耗时
         sum:                               137833.94

Threads fairness:
    events (avg/stddev):           312.5000/0.87
    execution time (avg/stddev):   8.6146/0.01

[root@dev10 ~]</span>

```

###### 1.4 清除压测数据

```ruby
[root@dev10 ~]<span class="katex math inline">sysbench --config-file=config /usr/share/sysbench/oltp_common.lua --tables=1 --table-size=10000 cleanup
sysbench 1.0.17 (using system LuaJIT 2.0.4)

Dropping table 'sbtest1'...
[root@dev10 ~]</span>

```

- - - - - -

###### **[自定义 lua 压测脚本](http://www.dev-share.top/2019/10/31/lua-%e8%87%aa%e5%ae%9a%e4%b9%89-sysbench-%e5%8e%8b%e5%8a%9b%e6%b5%8b%e8%af%95%e8%84%9a%e6%9c%ac/ "自定义 lua 压测脚本")**

- - - - - -

###### 使用sysbench的一些建议。

1、在开始测试之前，应该首先明确：应采用针对整个系统的基准测试，还是针对MySQL的基准测试，还是二者都需要。  
2、如果需要针对MySQL的基准测试，那么还需要明确精度方面的要求：是否需要使用生产环境的真实数据，还是使用工具生成也可以；前者实施起来更加繁琐。如果要使用真实数据，尽量使用全部数据，而不是部分数据。  
3、基准测试要进行多次才有意义。  
4、测试时需要注意主从同步的状态。  
5、测试必须模拟多线程的情况，单线程情况不但无法模拟真实的效率，也无法模拟阻塞甚至死锁情况。

- - - - - -