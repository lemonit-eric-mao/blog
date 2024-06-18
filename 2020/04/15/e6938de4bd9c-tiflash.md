---
title: '操作 TiFlash'
date: '2020-04-15T02:51:05+00:00'
status: publish
permalink: /2020/04/15/%e6%93%8d%e4%bd%9c-tiflash
author: 毛巳煜
excerpt: ''
type: post
id: 5316
category:
    - TiDB
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
##### 查询已存在 TiFlash 中的表

```sql
mysql :(none)> SELECT * FROM INFORMATION_SCHEMA.TIFLASH_REPLICA;
+--------------+-------------------------------+----------+---------------+-----------------+-----------+----------+
| TABLE_SCHEMA | TABLE_NAME                    | TABLE_ID | REPLICA_COUNT | LOCATION_LABELS | AVAILABLE | PROGRESS |
+--------------+-------------------------------+----------+---------------+-----------------+-----------+----------+
| dev2_pfizer  | dc_flowdata_deliver_inventory | 10761    | 1             |                 | 1         | 1.0      |
| dev2_pfizer  | dc_flowdata_deliver_purchase  | 11241    | 1             |                 | 1         | 1.0      |
| dev2_pfizer  | dc_flowdata_deliver_sale      | 11539    | 1             |                 | 1         | 1.0      |
| leojiang     | test1                         | 13095    | 1             |                 | 1         | 1.0      |
+--------------+-------------------------------+----------+---------------+-----------------+-----------+----------+

4 rows in set
Time: 0.016s
mysql :(none)>

```

- - - - - -

##### TiFlash 创建/删除

**ALTER TABLE `表名` SET TIFLASH REPLICA `副本数`;**  
**ALTER TABLE `表名` SET TIFLASH REPLICA `0`;**

```sql
-- 将TiKV中的表加入到 TiFlash
ALTER TABLE table_1 SET TIFLASH REPLICA 1;

-- 删除TiFlash副本
ALTER TABLE table_1 SET TIFLASH REPLICA 0;

```

- - - - - -

##### 使用注解，手动指定SQL句，从哪个存储引擎读取数据**\[TiKV`|`TiFlash\]**

**SELECT `/*+` read\_from\_storage(`tikv`\[`表名`\] )`*/` COUNT(\*) FROM `表名`;**  
**SELECT `/*+` read\_from\_storage(`tiflash`\[`表名`\] )`*/` COUNT(\*) FROM `表名`;**

```sql
-- 手动指定 SQL句 从 TiKV 中读取数据
SELECT /*+ read_from_storage(tikv[table_1] )*/ COUNT(*) FROM table_1;

-- 手动指定 SQL句 从 tiflash 中读取数据
SELECT /*+ read_from_storage(tiflash[table_1] )*/ COUNT(*) FROM table_1;

```

- - - - - -