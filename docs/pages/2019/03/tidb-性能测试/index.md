---
title: "TiDB 性能测试"
date: "2019-03-05"
categories: 
  - "tidb"
---

##### TiDB 超低配置，联表查询，性能测试

* * *

##### 前置条件

192.168.100.45      4C 16G 192.168.100.46      4C 16G 192.168.100.47      4C 16G 192.168.100.48      4C 16G

TiDB、PD、TiKV 三台机器共用

数据范围 2013年01月01日 至 2020年01月01日

* * *

| 表1 `dc_flowdata_deliver_sale` sale | 数据量 |
| --- | :-: |
| 数据量(总)： | 43397632 |
| 范围内数据量(`'2014-01-01' AND '2014-12-31'`): | 864564 |

| 表2 `dc_flowdata_deliver_sale_index` sale | 数据量 |
| --- | :-: |
| 数据量(总)： | 43397632 |
| 范围内数据量(`'2014-01-01' AND '2014-12-31'`): | 864564 |

| 表3 `dc_flowdata_deliver_sale_jion_index` sale | 数据量 |
| --- | :-: |
| 数据量(总)： | 43397632 |
| 范围内数据量(`'2014-01-01' AND '2014-12-31'`): | 864564 |

| 表4 `dc_flowdata_deliver_sale_range` sale | 数据量 |
| --- | :-: |
| 数据量(总)： | 43397632 |
| 范围内数据量(`'2014-01-01' AND '2014-12-31'`): | 864564 |

* * *

| `关联表` `dc_product_master` prod | 数据量 |
| --- | :-: |
| 数据量(总)： | 117 |

**`数据库总数据量`： 173,590,528**

* * *

* * *

* * *

**1.** 测试未进行表分区情况下，联表查询效率; **`未添加索引`**

```sql
SELECT
    COUNT(*)
FROM
    dc_flowdata_deliver_sale sale
    INNER JOIN dc_product_master prod ON sale.normal_product_code = prod.product_code 
WHERE
    sale.seller_date BETWEEN '2014-01-01' AND '2014-12-31';


+----------+
| COUNT(*) |
+----------+
| 780823   |
+----------+
1 row in set
Time: 34.537s


```

* * *

**2.** 测试未进行表分区情况下，联表查询效率; **`添加单独索引`**

KEY `seller_date` (`seller_date`), KEY `normal_product_code` (`normal_product_code`)

```sql
SELECT
   COUNT(*)
FROM
   dc_flowdata_deliver_sale_index sale
   INNER JOIN dc_product_master prod ON sale.normal_product_code = prod.product_code
WHERE
   sale.seller_date BETWEEN '2014-01-01' AND '2014-12-31';


+----------+
| COUNT(*) |
+----------+
| 780823   |
+----------+
1 row in set
Time: 366.416s

```

* * *

**3.** 测试未进行表分区情况下，联表查询效率; **`添加联合索引`**

KEY `seller_date` (`seller_date`,`normal_product_code`)

```sql
SELECT
   COUNT(*)
FROM
   dc_flowdata_deliver_sale_jion_index sale
   INNER JOIN dc_product_master prod ON sale.normal_product_code = prod.product_code
WHERE
   sale.seller_date BETWEEN '2014-01-01' AND '2014-12-31';


+----------+
| COUNT(*) |
+----------+
| 780823   |
+----------+
1 row in set
Time: 0.759s

```

* * *

**4.** 表分区情况下，联表查询效率;

```sql
SELECT
    COUNT(*)
FROM
    dc_flowdata_deliver_sale_range sale
    INNER JOIN dc_product_master prod ON sale.normal_product_code = prod.product_code 
WHERE
    sale.seller_date BETWEEN '2014-01-01' AND '2014-12-31';


+----------+
| COUNT(*) |
+----------+
| 780823   |
+----------+
1 row in set
Time: 5.178s

```

* * *

* * *

* * *

* * *

* * *

* * *

##### 测试目的

对比 TiDB v2.1.4 版本和 MySql 5.7 版本在 OLTP 场景下的性能。 根据节点的增加与减少 来比较 所带来的性能上的差异， 根据这些差异， 来衡量我们要实现的产品的报价

##### 测试版本、时间、地点

时间：2019 年 2 月 27 日 地点：大连 零壹光年

##### 测试环境

| 类别 | 名称 |
| --- | --- |
| OS | CentOS Linux release 7.6.1810 (Core) |
| CPU | Intel(R) Xeon(R) CPU E5-2650 v4 @ 2.20GHz, cpu 1 \* 8 |
| RAM | 16GB |
| DISK | 130GB \* 1 |

##### 测试方案

使用 Sysbench 向集群导入 100 张表，每张表数据 500 万条。 测试 增、删、改、查。 测试 联表查询 测试 混合 通过 HAProxy 代理，分别以递增并发数向集群发送请求，单次并发测试时间 5 分钟。

##### TiDB 版本信息

TiDB 版本: TiDB v2.1.4

##### TiDB 参数配置

TiDB 使用默认配置

##### TiKV 参数配置

TiKV 使用默认配置

##### 集群拓扑

| TiDB | \[tidb\_servers\] | \[tidb\_servers\] |
| --- | --- | --- |
| 主控机 | dev11 | 172.160.180.33 |
| 监控机 | dev12 | 172.160.180.34 |

| PD | \[pd\_servers\] | \[pd\_servers\] |
| --- | --- | --- |
|  | dev13 | 172.160.180.35 |
|  | dev14 | 172.160.180.36 |
|  | dev15 | 172.160.180.37 |

| TiKV | \[tikv\_servers\] | \[tikv\_servers\] |
| --- | --- | --- |
|  | dev11 | 172.160.180.33 |
|  | dev12 | 172.160.180.34 |
|  | dev13 | 172.160.180.35 |

###### 准备表和数据

开启100的线程工作，向集群导入 30 张表，每张表数据 500 万条数据。

```ruby
[tidb@dev10 lua]$ time sysbench --test=/usr/local/share/sysbench/oltp_read_write.lua \
--mysql-db=eric_tidb_test \
--mysql-host=172.160.180.33 \
--mysql-port=4000 \
--mysql-user=root \
--mysql-password=数据库密码 \
--tables=30 \
--table_size=5000000 \
--threads=100 \
prepare >> /home/tidb/tools/logs/tidb_prepare.log
```

###### 插入数据异常

```ruby
FATAL: mysql_drv_query() returned error 1105 (Information schema is changed.) for query 'CREATE TABLE sbtest44(
  id INTEGER NOT NULL AUTO_INCREMENT,
  k INTEGER DEFAULT '0' NOT NULL,
  c CHAR(120) DEFAULT '' NOT NULL,
  pad CHAR(60) DEFAULT '' NOT NULL,
  PRIMARY KEY (id)
) /*! ENGINE = innodb */ '
FATAL: `sysbench.cmdline.call_command' function failed: /usr/share/sysbench/oltp_common.lua:197: SQL error, errno = 1105, state = 'HY000': Information schema is changed.
```

###### 测试TiDB时需要改为 rocksdb 存储引擎

```ruby
[tidb@dev10 ~]$
[tidb@dev10 ~]$ sudo vim /usr/share/sysbench/oltp_common.lua
# 根据提示，找到 innodb 改为 rocksdb
   mysql_storage_engine =
    -- {"Storage engine, if MySQL is used", "innodb"},
      {"Storage engine, if MySQL is used", "rocksdb"},
```

##### 别忘了先连接TiDB创建数据库 eric\_tidb\_test

`要想看 sysbench 执行时的错误， 请将time 命令与 log输出去掉`

##### 第一步 创建数据库 与 数据库表 并插入数据

`创建 1张表， 500万数据`

```ruby
[tidb@dev10 sysbench]$ time sysbench --test=/usr/local/share/sysbench/oltp_read_write.lua \
--mysql-db=eric_tidb_test \
--mysql-host=172.160.180.33 \
--mysql-port=4000 \
--mysql-user=root \
--mysql-password=数据库密码 \
--tables=1 \
--table_size=5000000 \
--threads=100 \
prepare >> /home/tidb/tools/logs/tidb_prepare.log
```

##### 第二 进行读写压力测试

##### 测试1

`50线程， 1张表， 500万数据， 执行5分钟，每10秒生成一次报告`

```ruby
[tidb@dev10 sysbench]$ time sysbench --test=/usr/local/share/sysbench/oltp_read_write.lua \
--mysql-db=eric_tidb_test \
--mysql-host=172.160.180.33 \
--mysql-port=4000 \
--mysql-user=root \
--mysql-password=数据库密码 \
--threads=50 \
--tables=1 \
--table_size=5000000 \
--time=300 \
--report-interval=10 \
--events=200000 \
run >> /home/tidb/tools/logs/tidb_run_thread50_tables1.log
```

##### 测试1结果

```python
[ 10s ] thds: 50 tps: 747.92 qps: 15014.65 (r/w/o: 10518.21/2995.69/1500.75) lat (ms,95%): 139.85 err/s: 0.00 reconn/s: 0.00
[ 20s ] thds: 50 tps: 749.42 qps: 14989.77 (r/w/o: 10491.73/2999.19/1498.85) lat (ms,95%): 142.39 err/s: 0.00 reconn/s: 0.00
[ 30s ] thds: 50 tps: 729.51 qps: 14591.43 (r/w/o: 10215.36/2916.95/1459.12) lat (ms,95%): 142.39 err/s: 0.00 reconn/s: 0.00
[ 40s ] thds: 50 tps: 603.38 qps: 12081.36 (r/w/o: 8458.89/2415.71/1206.76) lat (ms,95%): 155.80 err/s: 0.00 reconn/s: 0.00
[ 50s ] thds: 50 tps: 561.82 qps: 11245.96 (r/w/o: 7869.85/2252.47/1123.64) lat (ms,95%): 167.44 err/s: 0.00 reconn/s: 0.00
[ 60s ] thds: 50 tps: 568.00 qps: 11358.86 (r/w/o: 7950.67/2272.19/1136.00) lat (ms,95%): 167.44 err/s: 0.00 reconn/s: 0.00
[ 70s ] thds: 50 tps: 578.81 qps: 11570.51 (r/w/o: 8100.18/2312.82/1157.51) lat (ms,95%): 164.45 err/s: 0.00 reconn/s: 0.00
[ 80s ] thds: 50 tps: 506.69 qps: 10142.83 (r/w/o: 7096.88/2032.47/1013.48) lat (ms,95%): 186.54 err/s: 0.00 reconn/s: 0.00
[ 90s ] thds: 50 tps: 448.30 qps: 8937.95 (r/w/o: 6259.04/1782.51/896.41) lat (ms,95%): 223.34 err/s: 0.00 reconn/s: 0.00
[ 100s ] thds: 50 tps: 436.00 qps: 8742.47 (r/w/o: 6119.65/1750.61/872.21) lat (ms,95%): 231.53 err/s: 0.00 reconn/s: 0.00
[ 110s ] thds: 50 tps: 447.80 qps: 8961.89 (r/w/o: 6272.69/1793.60/895.60) lat (ms,95%): 227.40 err/s: 0.00 reconn/s: 0.00
[ 120s ] thds: 50 tps: 441.09 qps: 8806.74 (r/w/o: 6166.29/1758.27/882.18) lat (ms,95%): 235.74 err/s: 0.00 reconn/s: 0.00
[ 130s ] thds: 50 tps: 417.11 qps: 8361.07 (r/w/o: 5850.32/1676.53/834.22) lat (ms,95%): 235.74 err/s: 0.00 reconn/s: 0.00
[ 140s ] thds: 50 tps: 397.69 qps: 7938.55 (r/w/o: 5559.19/1583.97/795.38) lat (ms,95%): 248.83 err/s: 0.00 reconn/s: 0.00
[ 150s ] thds: 50 tps: 441.91 qps: 8848.60 (r/w/o: 6192.57/1772.22/883.81) lat (ms,95%): 215.44 err/s: 0.00 reconn/s: 0.00
[ 160s ] thds: 50 tps: 448.49 qps: 8964.23 (r/w/o: 6276.78/1790.47/896.98) lat (ms,95%): 231.53 err/s: 0.00 reconn/s: 0.00
[ 170s ] thds: 50 tps: 451.90 qps: 9041.85 (r/w/o: 6326.94/1811.11/903.81) lat (ms,95%): 215.44 err/s: 0.00 reconn/s: 0.00
[ 180s ] thds: 50 tps: 444.20 qps: 8880.47 (r/w/o: 6216.78/1775.39/888.30) lat (ms,95%): 231.53 err/s: 0.00 reconn/s: 0.00
[ 190s ] thds: 50 tps: 457.40 qps: 9145.64 (r/w/o: 6403.13/1827.61/914.90) lat (ms,95%): 196.89 err/s: 0.00 reconn/s: 0.00
[ 200s ] thds: 50 tps: 434.50 qps: 8683.92 (r/w/o: 6079.24/1735.68/868.99) lat (ms,95%): 248.83 err/s: 0.00 reconn/s: 0.00
[ 210s ] thds: 50 tps: 433.50 qps: 8668.58 (r/w/o: 6066.49/1735.10/867.00) lat (ms,95%): 235.74 err/s: 0.00 reconn/s: 0.00
[ 220s ] thds: 50 tps: 451.01 qps: 9037.37 (r/w/o: 6325.42/1809.93/902.02) lat (ms,95%): 219.36 err/s: 0.00 reconn/s: 0.00
[ 230s ] thds: 50 tps: 431.20 qps: 8613.80 (r/w/o: 6031.60/1719.80/862.40) lat (ms,95%): 240.02 err/s: 0.00 reconn/s: 0.00
[ 240s ] thds: 50 tps: 418.90 qps: 8374.46 (r/w/o: 5861.64/1675.11/837.71) lat (ms,95%): 235.74 err/s: 0.00 reconn/s: 0.00
[ 250s ] thds: 50 tps: 452.90 qps: 9071.13 (r/w/o: 6348.72/1816.51/905.90) lat (ms,95%): 219.36 err/s: 0.00 reconn/s: 0.00
[ 260s ] thds: 50 tps: 448.40 qps: 8959.02 (r/w/o: 6273.14/1789.08/896.79) lat (ms,95%): 219.36 err/s: 0.00 reconn/s: 0.00
[ 270s ] thds: 50 tps: 444.00 qps: 8872.96 (r/w/o: 6210.44/1774.51/888.01) lat (ms,95%): 223.34 err/s: 0.00 reconn/s: 0.00
[ 280s ] thds: 50 tps: 431.29 qps: 8627.71 (r/w/o: 6041.47/1723.66/862.58) lat (ms,95%): 240.02 err/s: 0.00 reconn/s: 0.00
[ 290s ] thds: 50 tps: 410.20 qps: 8204.47 (r/w/o: 5741.35/1643.01/820.11) lat (ms,95%): 257.95 err/s: 0.00 reconn/s: 0.00
[ 300s ] thds: 50 tps: 455.50 qps: 9105.65 (r/w/o: 6371.14/1823.21/911.31) lat (ms,95%): 223.34 err/s: 0.00 reconn/s: 0.00
SQL statistics:
    queries performed:                           # 性能统计
        read:                            2057174 # 总select数量
        write:                           587764  # 总update、insert、delete语句数量
        other:                           293882  # commit、unlock tables以及其他mutex的数量
        total:                           2938820 # 总的执行语句数
    transactions:                        146941 (489.25 per sec.)    # 总的事物数（每秒处理事物数）|通常需要关注的数字(TPS)
    queries:                             2938820 (9784.94 per sec.)  # 读写请求次数（每秒的读写次数）|通常需要关注的数字(QPS)
    ignored errors:                      0      (0.00 per sec.)      # 忽略的错误数
    reconnects:                          0      (0.00 per sec.)

General statistics:
    total time:                          300.3391s     # 即 time指定的压测总时间
    total number of events:              146941        # 总的事件数,一般与transactions相同

Latency (ms):                                          # 应答时间
         min:                                   34.02
         avg:                                  102.10
         max:                                  870.80
         95th percentile:                      204.11  # 95%的语句的平均响应时间
         sum:                             15003046.59

Threads fairness:
    events (avg/stddev):           2938.8200/30.36
    execution time (avg/stddev):   300.0609/0.07
# Latency (ms):的 avg: 平均响应时间。(后面的95%的大小可以通过–percentile=98的方式去更改)
# transactions: 精确的说是这一项后面的TPS 。但如果使用了-skip-trx=on,这项事务数恒为0,需要用total number of events 去除以总时间,得到tps(其实还可以分为读tps和写tps)
# queries: 用它除以总时间,得到吞吐量QPS
```

##### 测试2

`100线程， 1张表， 500万数据， 执行5分钟，每10秒生成一次报告`

```ruby
[tidb@dev10 sysbench]$ time sysbench --test=/usr/local/share/sysbench/oltp_read_write.lua \
--mysql-db=eric_tidb_test \
--mysql-host=172.160.180.33 \
--mysql-port=4000 \
--mysql-user=root \
--mysql-password=数据库密码 \
--threads=100 \
--tables=1 \
--table_size=5000000 \
--time=300 \
--report-interval=10 \
--events=200000 \
run >> /home/tidb/tools/logs/tidb_run_thread100_tables1.log
```

##### 测试2结果

```python
[ 10s ] thds: 100 tps: 755.56 qps: 15211.91 (r/w/o: 10664.73/3026.06/1521.12) lat (ms,95%): 267.41 err/s: 0.00 reconn/s: 0.00
[ 20s ] thds: 100 tps: 706.22 qps: 14185.85 (r/w/o: 9928.61/2844.79/1412.44) lat (ms,95%): 262.64 err/s: 0.00 reconn/s: 0.00
[ 30s ] thds: 100 tps: 677.10 qps: 13522.92 (r/w/o: 9466.11/2702.80/1354.00) lat (ms,95%): 282.25 err/s: 0.00 reconn/s: 0.00
[ 40s ] thds: 100 tps: 724.70 qps: 14485.34 (r/w/o: 10143.83/2891.91/1449.60) lat (ms,95%): 282.25 err/s: 0.00 reconn/s: 0.00
[ 50s ] thds: 100 tps: 705.40 qps: 14088.34 (r/w/o: 9857.06/2820.79/1410.49) lat (ms,95%): 282.25 err/s: 0.00 reconn/s: 0.00
[ 60s ] thds: 100 tps: 712.69 qps: 14271.48 (r/w/o: 9994.51/2851.28/1425.69) lat (ms,95%): 287.38 err/s: 0.00 reconn/s: 0.00
[ 70s ] thds: 100 tps: 705.11 qps: 14108.19 (r/w/o: 9871.73/2826.44/1410.02) lat (ms,95%): 297.92 err/s: 0.00 reconn/s: 0.00
[ 80s ] thds: 100 tps: 626.50 qps: 12526.94 (r/w/o: 8768.66/2505.29/1252.99) lat (ms,95%): 337.94 err/s: 0.00 reconn/s: 0.00
[ 90s ] thds: 100 tps: 575.30 qps: 11455.65 (r/w/o: 8017.16/2291.29/1147.19) lat (ms,95%): 344.08 err/s: 0.00 reconn/s: 0.00
[ 100s ] thds: 100 tps: 561.70 qps: 11269.55 (r/w/o: 7892.36/2250.19/1126.99) lat (ms,95%): 325.98 err/s: 0.00 reconn/s: 0.00
[ 110s ] thds: 100 tps: 536.31 qps: 10727.27 (r/w/o: 7512.02/2142.63/1072.62) lat (ms,95%): 356.70 err/s: 0.00 reconn/s: 0.00
[ 120s ] thds: 100 tps: 507.99 qps: 10172.17 (r/w/o: 7120.11/2036.07/1015.99) lat (ms,95%): 350.33 err/s: 0.00 reconn/s: 0.00
[ 130s ] thds: 100 tps: 589.41 qps: 11815.28 (r/w/o: 8266.93/2369.54/1178.82) lat (ms,95%): 337.94 err/s: 0.00 reconn/s: 0.00
[ 140s ] thds: 100 tps: 632.78 qps: 12609.26 (r/w/o: 8826.06/2518.03/1265.17) lat (ms,95%): 337.94 err/s: 0.00 reconn/s: 0.00
[ 150s ] thds: 100 tps: 628.81 qps: 12618.49 (r/w/o: 8834.60/2525.86/1258.03) lat (ms,95%): 331.91 err/s: 0.00 reconn/s: 0.00
[ 160s ] thds: 100 tps: 634.77 qps: 12664.34 (r/w/o: 8864.84/2530.27/1269.23) lat (ms,95%): 325.98 err/s: 0.00 reconn/s: 0.00
[ 170s ] thds: 100 tps: 621.21 qps: 12430.04 (r/w/o: 8702.67/2484.85/1242.52) lat (ms,95%): 337.94 err/s: 0.00 reconn/s: 0.00
[ 180s ] thds: 100 tps: 529.40 qps: 10596.73 (r/w/o: 7414.92/2122.81/1059.00) lat (ms,95%): 383.33 err/s: 0.00 reconn/s: 0.00
[ 190s ] thds: 100 tps: 544.68 qps: 10897.00 (r/w/o: 7627.62/2180.62/1088.76) lat (ms,95%): 383.33 err/s: 0.00 reconn/s: 0.00
[ 200s ] thds: 100 tps: 578.32 qps: 11575.56 (r/w/o: 8103.95/2314.37/1157.24) lat (ms,95%): 356.70 err/s: 0.00 reconn/s: 0.00
[ 210s ] thds: 100 tps: 557.21 qps: 11132.84 (r/w/o: 7795.30/2223.13/1114.41) lat (ms,95%): 376.49 err/s: 0.00 reconn/s: 0.00
[ 220s ] thds: 100 tps: 637.29 qps: 12759.07 (r/w/o: 8930.21/2554.27/1274.59) lat (ms,95%): 325.98 err/s: 0.00 reconn/s: 0.00
[ 230s ] thds: 100 tps: 598.40 qps: 11962.32 (r/w/o: 8373.52/2392.00/1196.80) lat (ms,95%): 325.98 err/s: 0.00 reconn/s: 0.00
[ 240s ] thds: 100 tps: 637.71 qps: 12743.89 (r/w/o: 8913.00/2555.46/1275.43) lat (ms,95%): 331.91 err/s: 0.00 reconn/s: 0.00
[ 250s ] thds: 100 tps: 635.08 qps: 12717.81 (r/w/o: 8908.63/2539.02/1270.16) lat (ms,95%): 331.91 err/s: 0.00 reconn/s: 0.00
[ 260s ] thds: 100 tps: 613.50 qps: 12272.95 (r/w/o: 8592.86/2453.09/1226.99) lat (ms,95%): 344.08 err/s: 0.00 reconn/s: 0.00
[ 270s ] thds: 100 tps: 637.52 qps: 12681.49 (r/w/o: 8874.07/2534.88/1272.54) lat (ms,95%): 331.91 err/s: 0.00 reconn/s: 0.00
[ 280s ] thds: 100 tps: 627.79 qps: 12595.23 (r/w/o: 8819.18/2517.97/1258.08) lat (ms,95%): 337.94 err/s: 0.00 reconn/s: 0.00
[ 290s ] thds: 100 tps: 600.71 qps: 12041.63 (r/w/o: 8426.36/2413.85/1201.42) lat (ms,95%): 356.70 err/s: 0.00 reconn/s: 0.00
[ 300s ] thds: 100 tps: 633.70 qps: 12658.40 (r/w/o: 8866.13/2524.98/1267.29) lat (ms,95%): 325.98 err/s: 0.00 reconn/s: 0.00
SQL statistics:
    queries performed:
        read:                            2624076
        write:                           749736
        other:                           374868
        total:                           3748680
    transactions:                        187434 (624.13 per sec.)
    queries:                             3748680 (12482.51 per sec.)
    ignored errors:                      0      (0.00 per sec.)
    reconnects:                          0      (0.00 per sec.)

General statistics:
    total time:                          300.3125s
    total number of events:              187434

Latency (ms):
         min:                                   38.90
         avg:                                  160.11
         max:                                 9569.82
         95th percentile:                      331.91
         sum:                             30009654.85

Threads fairness:
    events (avg/stddev):           1874.3400/49.67
    execution time (avg/stddev):   300.0965/0.06
```

##### 第三步 清空测试数据

```ruby
[tidb@dev10 sysbench]$ sysbench --test=/usr/local/share/sysbench/oltp_read_write.lua \
--mysql-db=eric_tidb_test \
--mysql-host=172.160.180.33 \
--mysql-port=4000 \
--mysql-user=root \
--mysql-password=数据库密码 \
--tables=10 \
--table_size=5000000 \
cleanup
```
