---
title: 'TiDB 定位慢查询'
date: '2019-08-29T06:01:36+00:00'
status: publish
permalink: /2019/08/29/tidb-%e5%ae%9a%e4%bd%8d%e6%85%a2%e6%9f%a5%e8%af%a2
author: 毛巳煜
excerpt: ''
type: post
id: 5018
category:
    - TiDB
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
###### **[官方文档](https://book.tidb.io/session3/chapter3/slow-query-table.html "官方文档")**

- - - - - -

###### **[定位消耗系统资源多的查询](https://pingcap.com/docs-cn/stable/identify-expensive-queries/#%E5%AE%9A%E4%BD%8D%E6%B6%88%E8%80%97%E7%B3%BB%E7%BB%9F%E8%B5%84%E6%BA%90%E5%A4%9A%E7%9A%84%E6%9F%A5%E8%AF%A2 "定位消耗系统资源多的查询")**

通过修改 tidb配置文件, 来获取超过阈值的log, 例如：如下配置为，将 单条SQL语句超过 **`1G`** 的信息，输出到 tidb.log文件中

```yaml
global:
  # TiDB Configuration.

  # Valid options: ["log", "cancel"]
  oom-action: "log"
  #oom-action: "cancel"

  # Set the memory quota for a query in bytes. Default: 32GB
  #mem-quota-query: 34359738368
  mem-quota-query: 1073741824

```

- - - - - -

- - - - - -

- - - - - -

##### 查找慢查询语句

```sql
mysql> admin show slow top 10;
# 或 将行转列显示
mysql> admin show slow top 10 \G

```

- - - - - -

##### 说明

 **SLOW\_QUERY** 中的语句并不是都是有问题的。造成集群整体压力增大的是那些`process_time 很大的语句`。**如果 wait\_time 很大，但 process\_time 很小**的语句通常不是问题语句，而是因为**被问题语句`阻塞`** ，在执行队列等待造成的响应时间过长

- - - - - -

##### 也可以自己编写SQL

**`查询所有用户执行的SQL，且按执行消耗时间排序`**

```sql
SELECT
    DATE_FORMAT( Time, '%Y年 %m月 %d日 %H:%i' ) AS '发生日期',
    Query_time AS '执行语句花费的时间(秒)',
    DB AS 'DB',
    `Query` AS 'SQL语句',
    Mem_max / 1024 / 1024 AS 'sql 使用的内存（MB）',

    Request_count AS 'Request_count [语句发送的 Coprocessor 请求的数量]',
    Process_keys AS 'Process Keys [Coprocessor 处理的 key 的数量, 数量越多越占用TiKV资源]',
    Process_time AS 'Process_time [SQL在TiKV的 处理时间之和(秒)]',

    Wait_time AS 'Wait_time [SQL在TiKV中, Coprocessor 请求排队等待时间之和(秒)]',
    Backoff_time AS 'Backoff_time [语句遇到错误, 在重试前等待的时间(秒)]',

    CONCAT( `User`, '@', `HOST` ) AS '谁执行的',
    ( CASE succ WHEN '1' THEN '成功' ELSE '失败' END ) AS '是否执行成功',
    Stats AS '统计信息时间戳, 是否显示为 pseudo'
FROM
    information_schema.`slow_query`
WHERE
    `is_internal` = FALSE -- 是否为 tidb 内部的 sql 语句
    AND DB != ''
--  AND WEEK ( time ) = WEEK ( now( ) ) -- 查询一周内的
--  AND TO_DAYS( time ) = TO_DAYS( now( ) ) -- 查询今天的
--  AND time BETWEEN '2020-05-11 11:00' AND '2020-05-11 11:10' -- 查询指定时间范围的
    AND time > DATE_SUB( NOW( ), INTERVAL 1 HOUR ) -- 查询最近一小时的

ORDER BY
    `time` DESC,
    `query_time` DESC,
    Process_keys DESC
    LIMIT 100;


```

##### 查看慢查询日志文件存放位置

```sql
mysql> show variables like 'tidb_slow_query_file';
+----------------------+-------------------------------------------+
| Variable_name        | Value                                     |
+----------------------+-------------------------------------------+
| tidb_slow_query_file | /home/tidb/deploy/log/tidb_slow_query.log |
+----------------------+-------------------------------------------+
1 row in set (0.01 sec)

mysql>

```

- - - - - -

- - - - - -

- - - - - -

##### 慢查询解读

**[TiDB慢日志解析源码解读](https://asktug.com/t/topic/1902 "TiDB慢日志解析源码解读")**

**和 TiKV Coprocessor Task 相关的字段：**  
`Request_count` ：表示这个语句发送的 Coprocessor 请求的数量。  
`Total_keys` ：表示 Coprocessor 扫过的 key 的数量。  
`Process_keys` ：表示 Coprocessor 处理的 key 的数量。相比 total\_keys，processed\_keys 不包含 MVCC 的旧版本。如果 processed\_keys 和 total\_keys 相差很大，说明旧版本比较多。  
`Cop_proc_avg` ：cop-task 的平均执行时间。  
`Cop_proc_p90` ：cop-task 的 P90 分位执行时间。  
`Cop_proc_max` ：cop-task 的最大执行时间。  
`Cop_proc_addr` ：执行时间最长的 cop-task 所在地址。  
`Cop_wait_avg` ：cop-task 的平均等待时间。  
`Cop_wait_p90` ：cop-task 的 P90 分位等待时间。  
`Cop_wait_max` ：cop-task 的最大等待时间。  
`Cop_wait_addr` ：等待时间最长的 cop-task 所在地址。  
`Process_time` ：执行 SQL 在 TiKV 的处理时间之和，因为数据会并行的发到 TiKV 执行，这个值可能会超过 Query\_time 。

**`Wait_time` ：表示这个语句在 TiKV 的等待时间之和，`因为 TiKV 的 Coprocessor 线程数是有限的，当所有的 Coprocessor 线程都在工作的时候，请求会排队`；当队列中有某些请求耗时很长的时候，后面的请求的等待时间都会增加。**  
 [官方解决方案](https://pingcap.com/docs-cn/v3.0/reference/configuration/tikv-server/configuration-file/#readpoolcoprocessor "官方解决方案")  
 [官方书籍](https://book.tidb.io/session4/chapter7/tidb-oom.html "官方书籍")  
修改`conf/tikv.yml`

```yml
readpool:
  coprocessor:
    ## If CPU_NUM > 8, the default thread pool size for coprocessors is set to CPU_NUM * 0.8.
    ## 因为`Cluster-TiKV-Details --> Coprocessor Detail --> Wait duration`查询等待时间较长
    ## ，其原因有可能是慢因为SQL堆满线程池导致，所有查询操作都变慢
    ## ，所以增加 Coprocessor 线程池数据，来降低查询阻塞
    high-concurrency: 8
    normal-concurrency: 8
    low-concurrency: 8

```

- - - - - -

- - - - - -

- - - - - -