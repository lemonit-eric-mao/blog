---
title: "TiDB 优化"
date: "2019-08-29"
categories: 
  - "tidb"
---

#### **[看懂工作原理与配置，才能调优，这个必需看懂才行](http://g1eny0ung.coding.me/tidb-performance-map/#/ "看懂工作原理与配置，才能调优，这个必需看懂才行")**

**[TiDB Performance Map 副本](http://qiniu.dev-share.top/TiDB%20Performance%20Map.html "TiDB Performance Map 副本")**

* * *

* * *

* * *

##### **问题排查思路**

###### **场景**：

  数据查询卡，所有程序访问操作都很慢

###### **排查顺序**：

1. **`机器硬件性能`**
    
    1.1 内存是否打满   大量获取数据到内存中, `需要排查慢SQL`
    
    1.2 CPU是否满负荷工作   计算压力大, `需要排查慢SQL`
    
    1.3 硬盘IO   磁盘使用率，`最高为 100%`，一般到 `80% - 90%` 就需要考虑加节点
    
2. **`网速、流量`**
    
    2.1 网络吞吐量是否达到瓶颈   比如说，**TiKV从RocksDB中每秒获取`1G`的数据**，但传给客户端时，**每秒只能传输`500M`的数据**，这种情况下可以增加TiKV与TiDB之间的线程数来提高传输效率，也可以提高带宽来解决问题。
    
    2.2 网络流量是否过大   如果网络流量实在太大，两种选择： 1 降低业务并发量，2 提升到万兆网卡
    
3. **[慢SQL](http://www.dev-share.top/2019/08/29/tidb-%e5%ae%9a%e4%bd%8d%e6%85%a2%e6%9f%a5%e8%af%a2/ "慢SQL")** 3.1 大表分页查询慢
    
    3.2 大表关联慢
    
    3.3 大表排序慢
    

* * *

* * *

* * *

##### 一、SQL 优化方法

**[参考资料](http://www.dev-share.top/2020/01/19/sql-%E8%AF%AD%E5%8F%A5%E4%BC%98%E5%8C%96/ "参考资料")**

###### 1\. SQL 优化的目标之一是`将计算尽可能地下推到 TiKV 中执行`。

TiKV 中的 coprocessor 能支持大部分 SQL 内建函数（包括聚合函数和标量函数）、SQL LIMIT 操作、索引扫描和表扫描。 但是，所有的 Join 操作都只能作为 root task 在 TiDB 上执行。

* * *

###### 2\. 注意是否有数据的类型转换

因为数据类型转换是在TiDB中进行的这样会降低效率，如下结果 **`cast`(sbtest.this\_.paas\_is\_del)** 因此 尽可能地下推到 TiKV 中执行，查询时不要类型转换

```sql
EXPLAIN ANALYZE SELECT
    *
FROM
    dc_organization_master this_
WHERE
    this_.STATUS = 3
    AND this_.paas_is_del = 0
    AND ( this_.organ_name LIKE '%港花园%' OR this_.organ_used_names LIKE '%凤%' )
ORDER BY
    this_.organ_name ASC
    LIMIT 10

# 执行计划如下
+----------------------------+-------+------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| id                         | count | task | operator info                                                                                        | execution info                                                            | memory                |
+----------------------------+-------+------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Limit_13                   | 10.00 | root | offset:0, count:10                                                                                   | time:956.196287ms, loops:2, rows:10                                       | N/A                   |
| └─Selection_18             | 10.00 | root | eq(cast(sbtest.this_.paas_is_del), 0), eq(cast(sbtest.this_.status), 3)                              | time:956.194026ms, loops:1, rows:10                                       | N/A                   |
|   └─Projection_23          | 10.00 | root | 这里内容太多省略不写                                                                                   | time:956.032871ms, loops:1, rows:1024                                     | N/A                   |
|     └─IndexLookUp_22       | 10.00 | root |                                                                                                      | time:956.0138ms, loops:1, rows:1024                                       | 102.52162551879883 MB |
|       ├─IndexScan_19       | 12.50 | cop  | table:this_, index:organ_name, range:[NULL,+inf], keep order:true                                    | time:443ms, loops:896, rows:912968                                        | N/A                   |
|       └─Selection_21       | 10.00 | cop  | or(like(sbtest.this_.organ_name, "%港花园%", 92), like(sbtest.this_.organ_used_names, "%凤%", 92))    | proc max:33ms, min:2ms, p80:27ms, p95:33ms, rows:51744, iters:80, tasks:6 | N/A                   |
|         └─TableScan_20     | 12.50 | cop  | table:dc_organization_master, keep order:false                                                       | proc max:30ms, min:2ms, p80:23ms, p95:30ms, rows:51744, iters:80, tasks:6 | N/A                   |
+----------------------------+-------+------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
```

处理方式，只需要将SQL中发生类型转换的数据改过来

```sql
EXPLAIN ANALYZE SELECT
    *
FROM
    dc_organization_master this_
WHERE
    this_.STATUS = '3'
    AND this_.paas_is_del = '0'
    AND ( this_.organ_name LIKE '%港花园%' OR this_.organ_used_names LIKE '%凤%' )
ORDER BY
    this_.organ_name ASC
    LIMIT 10

# 执行计划如下
+--------------------------+-------+------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| id                       | count | task | operator info                                                                                                                                                         | execution info                                                     | memory               |
+--------------------------+-------+------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Limit_12                 | 10.00 | root | offset:0, count:10                                                                                                                                                    | time:1.05856674s, loops:2, rows:10                                 | N/A                  |
| └─Projection_25          | 10.00 | root |  这里内容太多省略不写                                                                                                                                                   | time:1.058564699s, loops:1, rows:10                                | N/A                  |
|   └─IndexLookUp_24       | 10.00 | root |                                                                                                                                                                       | time:1.058537896s, loops:1, rows:10                                | 70.27115440368652 MB |
|     ├─IndexScan_21       | 12.50 | cop  | table:this_, index:organ_name, range:[NULL,+inf], keep order:true                                                                                                     | time:481ms, loops:896, rows:912968                                 | N/A                  |
|     └─Selection_23       | 10.00 | cop  | eq(sbtest.this_.paas_is_del, "0"), eq(sbtest.this_.status, "3"), or(like(sbtest.this_.organ_name, "%港花园%", 92), like(sbtest.this_.organ_used_names, "%凤%", 92))    | proc max:1ms, min:0s, p80:0s, p95:1ms, rows:630, iters:13, tasks:6 | N/A                  |
|       └─TableScan_22     | 12.50 | cop  | table:dc_organization_master, keep order:false                                                                                                                        | proc max:1ms, min:0s, p80:0s, p95:1ms, rows:630, iters:13, tasks:6 | N/A                  |
+--------------------------+-------+------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
```

* * *

###### 3\. 自增唯一键, 作为游标取代limit offset的分页方式

[大数据分页查询 会越来越慢，如何调优？](https://asktug.com/t/topic/1601 "大数据分页查询 会越来越慢，如何调优？")

```sql
CREATE TABLE `dc_organization_master` (
`cursor_num` INT ( 11 ) UNIQUE KEY AUTO_INCREMENT COMMENT '游标(自增唯一键)'
) ENGINE = INNODB DEFAULT CHARSET = utf8 COLLATE = utf8_bin COMMENT = '机构主数据';
```

* * *

* * *

* * *

##### 二、配置优化

###### 1\. 优化写冲突

**[开启乐观锁事务重试功能](http://www.dev-share.top/2019/12/04/tidb-%e5%b8%b8%e7%94%a8%e5%91%bd%e4%bb%a4/ "开启乐观锁事务重试功能")** **[设置事务模式](https://pingcap.com/docs-cn/stable/reference/configuration/tidb-server/tidb-specific-variables/#tidb_txn_mode "设置事务模式")** **[写冲突问题](https://asktug.com/t/tikv/2016/4 "写冲突问题")** `冲突取决于业务模式和特点，需要从业务的角度自行分析。原则上与 kv 的节点数量关系不大`

* * *

###### 2\. 优化查询语句

**[将子查询转成 join 和 aggregation](https://pingcap.com/docs-cn/stable/reference/configuration/tidb-server/tidb-specific-variables/#tidb_opt_insubq_to_join_and_agg "将子查询转成 join 和 aggregation")**

* * *

###### 3\. 设置 hash join 算法的并发度。

适当调大 `tidb_hash_join_concurrency` 以增加 hash join 的性能。（注意 TiDB 的内存是否足够，过大有可能会引起 OOM ） **[官网介绍](https://pingcap.com/docs-cn/stable/reference/configuration/tidb-server/tidb-specific-variables/#tidb_hash_join_concurrency "官网介绍")**

* * *

* * *

* * *

##### 三、使用窗口函数优化 limit

**[参考资料](https://www.jianshu.com/p/7a2fd8c2af25?from=timeline "参考资料")** **[优化方法](https://asktug.com/t/topic/2465 "优化方法")**

###### 【TiDB 版本】：

v3.0.5

###### 【前置条件】：

150万数据，分页查询，每页1万条

###### 【优化前】：

```sql
MySQL [pressure_table1]> EXPLAIN ANALYZE
    -> SELECT
    ->     code1,
    ->     code2,
    ->     code3,
    ->     normal1,
    ->     date1
    -> FROM
    ->     dc_sale
    -> WHERE
    ->     Is_Del = '0'
    -> ORDER BY id
    -> LIMIT 740000, 10000;
+--------------------------+------------+------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------+----------------------+
| id                       | count      | task | operator info                                                                                                                                                      | execution info                                                                     | memory               |
+--------------------------+------------+------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------+----------------------+
| Projection_8             | 10000.00   | root | pressure_table1.dc_sale.code1, pressure_table1.dc_sale.code2, pressure_table1.dc_sale.code3, pressure_table1.dc_sale.normal1, pressure_table1.dc_sale.date1        | time:5.455002597s, loops:11, rows:10000                                            | N/A                  |
| └─TopN_11                | 10000.00   | root | pressure_table1.dc_sale.id:asc, offset:740000, count:10000                                                                                                         | time:5.454709343s, loops:11, rows:10000                                            | 145.3629379272461 MB |
|   └─TableReader_21       | 956849.86  | root | data:Selection_20                                                                                                                                                  | time:1.069426628s, loops:1019, rows:1041178                                        | 53.48866653442383 MB |
|     └─Selection_20       | 956849.86  | cop  | eq(pressure_table1.dc_sale.Is_Del, "0")                                                                                                                            | proc max:538ms, min:58ms, p80:442ms, p95:538ms, rows:1041178, iters:1519, tasks:11 | N/A                  |
|       └─TableScan_19     | 1477850.00 | cop  | table:dc_sale, range:[-inf,+inf], keep order:false                                                                                                                 | proc max:530ms, min:55ms, p80:431ms, p95:530ms, rows:1503640, iters:1519, tasks:11 | N/A                  |
+--------------------------+------------+------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------+----------------------+
5 rows in set (5.46 sec)

MySQL [pressure_table1]>

```

###### 【优化后】：

```sql
MySQL [pressure_table1]> EXPLAIN ANALYZE
    -> SELECT
    -> *
    -> FROM
    -> (
    ->     SELECT
    ->     Is_Del,
    ->     code1,
    ->     code2,
    ->     code3,
    ->     normal1,
    ->     date1,
    ->     ROW_NUMBER ( ) OVER ( ORDER BY id ) AS row_num
    ->     FROM
    ->     dc_sale
    ->     WHERE
    ->     Is_Del = '0'
    ->    ) t
    -> WHERE
    -> t.row_num > 740000
    -> LIMIT 10000;
+--------------------------------+------------+------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------+----------------------+
| id                             | count      | task | operator info                                                                                                                                                                                                                 | execution info                                                                     | memory               |
+--------------------------------+------------+------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------+----------------------+
| Projection_13                  | 10000.00   | root | pressure_table1.dc_sale.Is_Del, pressure_table1.dc_sale.code1, pressure_table1.dc_sale.code2, pressure_table1.dc_sale.code3, pressure_table1.dc_sale.normal1, pressure_table1.dc_sale.date1, row_num                          | time:2.2110195s, loops:11, rows:10000                                              | N/A                  |
| └─Limit_16                     | 10000.00   | root | offset:0, count:10000                                                                                                                                                                                                         | time:2.210741782s, loops:11, rows:10000                                            | N/A                  |
|   └─Selection_17               | 10000.00   | root | gt(row_num, 740000)                                                                                                                                                                                                           | time:2.210717323s, loops:10, rows:10000                                            | N/A                  |
|     └─Window_18                | 10000.00   | root | row_number() over(order by pressure_table1.dc_sale.id asc)                                                                                                                                                                    | time:2.165769184s, loops:733, rows:750592                                          | N/A                  |
|       └─Projection_23          | 956849.86  | root | pressure_table1.dc_sale.code1, pressure_table1.dc_sale.code2, pressure_table1.dc_sale.code3, pressure_table1.dc_sale.normal1, pressure_table1.dc_sale.date1, pressure_table1.dc_sale.Is_Del, pressure_table1.dc_sale.id       | time:2.050503838s, loops:1018, rows:1041178                                        | N/A                  |
|         └─IndexLookUp_22       | 956849.86  | root |                                                                                                                                                                                                                               | time:2.103801808s, loops:1018, rows:1041178                                        | 32.93011474609375 MB |
|           ├─IndexScan_19       | 1477850.00 | cop  | table:dc_sale, index:id, range:[NULL,+inf], keep order:true                                                                                                                                                                   | proc max:515ms, min:371ms, p80:515ms, p95:515ms, rows:1503640, iters:1478, tasks:2 | N/A                  |
|           └─Selection_21       | 956849.86  | cop  | eq(pressure_table1.dc_sale.Is_Del, "0")                                                                                                                                                                                       | proc max:70ms, min:0s, p80:41ms, p95:59ms, rows:1041178, iters:4654, tasks:710     | N/A                  |
|             └─TableScan_20     | 1477850.00 | cop  | table:dc_sale, keep order:false                                                                                                                                                                                               | proc max:70ms, min:0s, p80:41ms, p95:58ms, rows:1503640, iters:4654, tasks:710     | N/A                  |
+--------------------------------+------------+------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------+----------------------+
9 rows in set (2.22 sec)

MySQL [pressure_table1]>

```

**总结：**   大概明白了，分页之所以慢是因为, 慢在了offset上，从上面的查询计划中可以看出来，优化前的语句，消耗了两次内存，第一次是在扫表，而第二次是执行 offset, 消耗的内存更大   而优化后的语句，是只做了一次的全表扫然后排序，之后的操作只是对结果数据进行截取，并且只消耗了一次内存

* * *

* * *

* * *

##### 四、根据统计信息健康度，提供给数据库优化器

**[官方链接](https://pingcap.com/docs-cn/stable/reference/performance/statistics/#%E7%BB%9F%E8%AE%A1%E4%BF%A1%E6%81%AF%E7%AE%80%E4%BB%8B "官方链接")**

  **`TiDB优化器`会根据`统计信息`来`选择最优`的`执行计划`** 。   统计信息收集了表级别和列级别的信息，表的统计信息包括总行数和修改的行数。列的统计信息包括不同值的数量、NULL 的数量、直方图、列上出现次数最多的值 TOPN 以及该列的 `Count-Min Sketch` 信息。

###### 列的不同值数量以及 NULL 值数量

通过 `SHOW STATS_HISTOGRAMS` 来查看列的不同值数量以及 `NULL` 值数量等信息

###### 查看统计信息中，表的健康度

`SHOW STATS_HEALTHY;`

```sql
SHOW STATS_HEALTHY WHERE healthy < 100;
```

###### 健康度低于60需要做, 收集统计信息

`ANALYZE TABLE t1,t2,t3,.....`

```sql
ANALYZE TABLE channel_data_table, sys_file_import_column
```

###### 如果表数据量较大，可以设定下面参数来提升统计效率

```sql
SET tidb_build_stats_concurrency=20;
SET tidb_distsql_scan_concurrency=100;
SET tidb_index_serial_scan_concurrency=20;
```

###### 另外补充下，统计信息收集得满足条件才会收集：

1）table 需要满足行数**`大于 1000 行`** 2）表重未被 analyze 过，并且至少 1 分钟内没有 DML 操作 3）analyze 过的表，再次 analyze 需要满足数据变化超过 ratio 定义的 0.5

* * *

###### **`例如` 查看 affiliated\_drugstore\_master 表信息**

```sql
-- 查看统计信息，(也就是查看修改了多少行数据)
mysql root@192.168.192.31:(none)> show stats_meta WHERE table_name = 'affiliated_drugstore_master';
+-------------+-----------------------------+----------------+---------------------+--------------+-----------+
| Db_name     | Table_name                  | Partition_name | Update_time         | Modify_count | Row_count |
+-------------+-----------------------------+----------------+---------------------+--------------+-----------+
| prd2_pfizer | affiliated_drugstore_master |                | 2020-04-07 19:20:58 | 187089       | 467089    |
+-------------+-----------------------------+----------------+---------------------+--------------+-----------+

1 row in set
Time: 0.023s
mysql root@192.168.192.31:(none)>
mysql root@192.168.192.31:(none)>
-- 查看健康度，(修改的行数越多，健康度越底)
mysql root@192.168.192.31:(none)> show stats_healthy WHERE table_name = 'affiliated_drugstore_master';
+-------------+-----------------------------+----------------+---------+
| Db_name     | Table_name                  | Partition_name | Healthy |
+-------------+-----------------------------+----------------+---------+
| prd2_pfizer | affiliated_drugstore_master |                | 59      |
+-------------+-----------------------------+----------------+---------+

1 row in set
Time: 0.014s
mysql root@192.168.192.31:(none)>
```

###### 重新收集表信息

```sql
mysql root@192.168.192.31:(none)> analyze table prd2_pfizer.affiliated_drugstore_master;
Query OK, 0 rows affected
Time: 1.717s
mysql root@192.168.192.31:(none)>
```

###### 重新查看信息

```sql
mysql root@192.168.192.31:(none)>  show stats_meta WHERE table_name = 'affiliated_drugstore_master';

+-------------+-----------------------------+----------------+---------------------+--------------+-----------+
| Db_name     | Table_name                  | Partition_name | Update_time         | Modify_count | Row_count |
+-------------+-----------------------------+----------------+---------------------+--------------+-----------+
| prd2_pfizer | affiliated_drugstore_master |                | 2020-04-08 16:39:27 | 0            | 457089    |
+-------------+-----------------------------+----------------+---------------------+--------------+-----------+

1 row in set
Time: 0.014s
mysql root@192.168.192.31:(none)>
mysql root@192.168.192.31:(none)> show stats_healthy WHERE table_name = 'affiliated_drugstore_master';
+-------------+-----------------------------+----------------+---------+
| Db_name     | Table_name                  | Partition_name | Healthy |
+-------------+-----------------------------+----------------+---------+
| prd2_pfizer | affiliated_drugstore_master |                | 100     |
+-------------+-----------------------------+----------------+---------+

1 row in set
Time: 0.014s
mysql root@192.168.192.31:(none)>
```

* * *

* * *

* * *

##### 五、调优TiKV配置

###### 修改 TiKV.yml

```yml
以上省略......

raftstore:

  # 开启静默region, 用于减少 raftstore CPU 的消耗
  hibernate-regions: true

  ## Use how many threads to handle log apply
  # 增加 Apply Thread Pool 线程池数量，最大可调整到单机CPU核数的 90%
  # apply-pool-size: 2
  apply-pool-size: 7

  ## Use how many threads to handle raft messages
  # 增加 Raftstore Pool 线程池数量，最大可调整到单机CPU核数的 80%
  # store-pool-size: 2
  store-pool-size: 6

以下省略......

```

###### 修改 PD.yml

```yml
---
# default configuration file for pd in yaml format

global:
  # lease: 3
  # tso-save-interval: "3s"

  # 默认 table 情况下，region merge 不会进行表表合并，所以在有大量的 drop/truncate table, create table, drop database 的时候，需要开启该参数
  # namespace-classifier: "table"
  namespace-classifier: "default"

以下省略......
```

###### **[如果引发异常，请看这里](http://www.dev-share.top/2019/08/21/tidb-%E5%B8%B8%E8%A7%81%E9%97%AE%E9%A2%98/ "如果引发异常，请看这里")**

* * *

* * *

* * *
