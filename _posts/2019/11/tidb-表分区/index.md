---
title: "TiDB 表分区"
date: "2019-11-26"
categories: 
  - "tidb"
---

##### 前置条件

###### [对比MySQL的表分区](https://dev.mysql.com/doc/refman/5.7/en/partitioning-limitations-partitioning-keys-unique-keys.html "对比MySQL的表分区")

###### [使用之前，要先读官方文档](https://pingcap.com/docs-cn/stable/reference/sql/partitioning/#%E5%88%86%E5%8C%BA%E8%A1%A8 "使用之前，要先读官方文档")

* * *

* * *

* * *

##### 表分区，注意事项

1. 确认表中是否`存在`**唯一键(`包括主键`)** ，如果存在，那么**唯一键** 中，必须包含分区表达式中用到的所有列
2. 如果表中`不存在`**唯一键** ，那么`第1条`规则也就不需要遵守了
3. 分区列是主键列，那么分区列`不可以是 NULL`
4. 分区表达式中列的数据类型，要与**表中列的数据`类型`相符合**
5. 删除分区`一定会删除分区中所有数据`，不会自动转移数据
6. **`MAXVALUE`** 因为添加分区必须是递增的，添加此分区时要注意，此分区表示已经是最大的分区，无法在添加新的分区。

* * *

* * *

* * *

##### 1 表分区 RANGE

```sql
-- 创建表
CREATE TABLE table_range (
  a bigint(20) DEFAULT NULL,
  b varchar(255) DEFAULT NULL,
  c int(11) DEFAULT NULL,
  d date DEFAULT NULL,
  KEY m_index (a,b,c)
)
-- 创建 RANGE 表分区 按照年分区
PARTITION BY RANGE(YEAR(d)) (
    PARTITION p0 VALUES LESS THAN (1900),
    PARTITION p1 VALUES LESS THAN (2010),
    PARTITION p2 VALUES LESS THAN MAXVALUE
);

-- 添加数据
INSERT INTO table_range VALUES (1,'1',1,'1900-01-01'), (2,'2',2,'2009-02-02'), (3,'3',3,'2019-03-03');

-- 添加表分区
-- ALTER TABLE table_range ADD PARTITION (PARTITION p3 VALUES LESS THAN (2014));

-- 清空表分区
-- ALTER TABLE table_range TRUNCATE PARTITION p1;

-- 删除表分区
-- ALTER TABLE table_range DROP PARTITION p3;

-- 查询数据 1900~2009 之间的数据，这里只会查询 p0 表分区
SELECT * FROM table_range WHERE d > 1900 AND d < 2009;

-- 指定查询 p1 表分区
SELECT * FROM table_range PARTITION (p1);
```

* * *

```sql
-- 创建表
CREATE TABLE table_range (
  a bigint(20) DEFAULT NULL,
  b varchar(255) DEFAULT NULL,
  c int(11) DEFAULT NULL,
  d date DEFAULT NULL,
  KEY m_index (a,b,c)
)
-- 创建 RANGE 表分区 按照 年、月、日 分区
PARTITION BY RANGE(TO_DAYS(d)) (
    PARTITION p0 VALUES LESS THAN (TO_DAYS('2017-02-01')),
    PARTITION p1 VALUES LESS THAN (TO_DAYS('2017-03-01')),
    PARTITION p2 VALUES LESS THAN MAXVALUE
);
```

* * *

```sql
-- 创建表
CREATE TABLE table_range (
  a bigint(20) DEFAULT NULL,
  b varchar(255) DEFAULT NULL,
  c int(11) DEFAULT NULL,
  d TIMESTAMP DEFAULT NULL,
  KEY m_index (a,b,c)
)
-- 创建 RANGE 表分区 按照 时间戳 分区
PARTITION BY RANGE(UNIX_TIMESTAMP(d)) (
    PARTITION p0 VALUES LESS THAN (UNIX_TIMESTAMP('2017-02-01 00:00:00')),
    PARTITION p1 VALUES LESS THAN (UNIX_TIMESTAMP('2017-03-01 00:00:00')),
    PARTITION p2 VALUES LESS THAN MAXVALUE
);
```

* * *

##### **`查询系统表中记录的表分区`**

```sql
SELECT
    PARTITION_NAME AS '分区名称',
    FROM_DAYS(PARTITION_DESCRIPTION) AS '原分区条件',
    PARTITION_EXPRESSION AS '分区表达式',
    PARTITION_DESCRIPTION AS '分区条件',
    TABLE_ROWS AS '分区中数据行数'
FROM
    INFORMATION_SCHEMA.PARTITIONS
WHERE
    TABLE_SCHEMA = 'prd2_pfizer'
    AND TABLE_NAME = 'dc_flowdata_deliver_sale_range';
```

* * *

* * *

* * *

##### 2 表分区 HASH

```sql
-- 创建表
CREATE TABLE table_hash (
  a bigint(20) DEFAULT NULL,
  b varchar(255) DEFAULT NULL,
  c int(11) DEFAULT NULL,
  d date DEFAULT NULL,
  KEY m_index (a,b,c)
)
-- 创建 HASH 表分区
PARTITION BY HASH(YEAR(d))
PARTITIONS 6;

-- 添加数据
INSERT INTO table_hash VALUES (1,'1',1,'1900-01-01'), (2,'2',2,'2009-02-02'), (3,'3',3,'2019-03-03');
```
