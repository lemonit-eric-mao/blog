---
title: "TiDB 内存快照分析"
date: "2019-09-18"
categories: 
  - "tidb"
---

##### 前置条件

```ruby
[tidb@dev10 ~]$ yum install -y golang
```

* * *

##### 语法

###### 堆内存快照获取方式

```ruby
go tool pprof http://172.160.180.53:10080/debug/pprof/heap
curl 'http://172.160.180.53:10080/debug/pprof/heap?debug=1' > heap.txt
```

###### goroutine ([浅谈goroutine](https://www.jianshu.com/p/7ebf732b6e1f "浅谈goroutine"))

```ruby
go tool pprof http://172.160.180.53:10080/debug/pprof/goroutine
curl 'http://172.160.180.53:10080/debug/pprof/goroutine?debug=2' > goroutine.txt
```

* * *

##### TiDB 内存快照分析

```ruby
[tidb@dev10 ~]$ go tool pprof 172.160.180.33:10080/debug/pprof/heap
```

##### 或者

`curl -G pd的IP:10080/debug/pprof/heap > heap.profile`

```ruby
[tidb@dev10 ~]$ curl -G 172.160.180.33:10080/debug/pprof/heap > heap.profile

[tidb@dev10 ~]$
[tidb@dev10 ~]$ go tool pprof heap.profile
File: tidb-server
Build ID: 40bee8740e5b8cb4930a3d0efa0fa7231d2e8116
Type: inuse_space
Time: Sep 18, 2019 at 3:55pm (CST)
Entering interactive mode (type "help" for commands, "o" for options)
(pprof)
(pprof) top 10
Showing nodes accounting for 154.68MB, 79.82% of 193.79MB total
Dropped 77 nodes (cum <= 0.97MB)
Showing top 10 nodes out of 174
      flat  flat%   sum%        cum   cum%
      96MB 49.54% 49.54%       96MB 49.54%  github.com/pingcap/tidb/store/tikv/latch.NewLatches
   15.99MB  8.25% 57.79%    15.99MB  8.25%  github.com/pingcap/tidb/util/arena.NewAllocator
    9.66MB  4.98% 62.77%     9.66MB  4.98%  bufio.NewReaderSize
    8.06MB  4.16% 66.93%     8.06MB  4.16%  github.com/pingcap/tidb/statistics.NewCMSketch
    6.60MB  3.41% 70.34%     6.60MB  3.41%  github.com/pingcap/parser.New
    4.06MB  2.10% 72.43%     4.06MB  2.10%  bufio.NewWriterSize
    3.72MB  1.92% 74.36%     3.72MB  1.92%  google.golang.org/grpc/internal/transport.newBufWriter
    3.59MB  1.85% 76.21%     7.60MB  3.92%  github.com/pingcap/tidb/util/chunk.(*column).appendBytes
    3.50MB  1.81% 78.01%    14.55MB  7.51%  github.com/pingcap/tidb/statistics/handle.(*Handle).initStatsHistograms4Chunk
    3.50MB  1.81% 79.82%     3.50MB  1.81%  reflect.New
(pprof)

```

##### 实际使用内存 available

```ruby
[root@dev11 ~]# free -h
              total        used        free      shared  buff/cache   available
Mem:            15G        6.3G        7.8G         81M        1.6G         13G
Swap:            0B          0B          0B
[root@dev11 ~]#
```

##### 因为工作节点机器在大数据量处理时，因内存被消耗尽，导致宕机，因此通过设置单条SQL语句执行时所占用的内存阀值，不要分配所有的内存给TiDB使用

```ruby
[tidb@dev10 tidb-ansible]$ vim conf/tidb.yml

 global:
   # TiDB Configuration.

   ......

   # Only print a log when out of memory quota.
   # Valid options: ["log", "cancel"]
   #oom-action: "log"
   # 超过阀值，将取消执行
   oom-action: "cancel"

   # Set the memory quota for a query in bytes. Default: 32GB
   # mem-quota-query: 34359738368
   # 设置阀值 为 8GB
   mem-quota-query: 8589934592

   ......

 performance:
   # Max CPUs to use, 0 use number of CPUs in the machine.
   # max-procs: 0

   # Prepare cache LRU 使用的最大内存限制，超过 performance.max-memory * (1 - prepared-plan-cache.memory-guard-ratio)会 剔除 LRU 中的元素。
   # 默认值：0
   # 这个配置只有在 prepared-plan-cache.enabled 为 true 的情况才会生效。在 LRU 的 size 大于 prepared-plan-cache.capacity 的情况下，也会剔除 LRU 中的元素。
   # Max memory size to use, 0 use the total usable memory in the machine.
   # max-memory: 0
   max-memory: 6

   # StmtCountLimit limits the max count of statement inside a transaction.
   # TiDB 一个事务允许的最大语句条数限制。
   # 默认值：5000
   # 在一个事务中，超过 stmt-count-limit 条语句后还没有 rollback 或者 commit，TiDB 将会返回 statement count 5001 exceeds the transaction limitation, autocommit = false 错误。
   # stmt-count-limit: 5000

   ......

 prepared_plan_cache:
   # enabled: false
   enabled: true
   # capacity: 100
   # memory-guard-ratio: 0.1

   ......

[tidb@dev10 tidb-ansible]$
```
