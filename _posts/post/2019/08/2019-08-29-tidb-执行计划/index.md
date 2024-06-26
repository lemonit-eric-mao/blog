---
title: "TiDB 执行计划"
date: "2019-08-29"
categories: 
  - "tidb"
---

#### 使用执行计划分析慢查询语句

[官方文档](https://pingcap.com/docs-cn/v3.0/reference/performance/understanding-the-query-execution-plan/ "官方文档")

##### 慢查询日志中所有时间相关字段的单位都是 秒：

优化一个查询, 比如一个语句查询比较慢，我们要优化这个查询； 首先要知道这个查询语句的 查询计划是什么; **`EXPLAIN`** `SELECT * FROM table1`

- `id` 算子的 ID，在整个执行计划中唯一的标识一个算子。在 TiDB 2.1 中，id 会格式化显示算子的树状结构。 数据从 child 流向 parent，每个 算子的 parent 有且仅有一个。
    
- `count` 预计当前算子将会输出的数据条数，基于统计信息以及算子的执行逻辑估算而来。
    
- `task` 当前这个算子属于什么 task。 目前的执行计划分成为两种 task，`一种叫 root task，在 tidb-server 上执行`，`一种叫 cop task，并行的在 TiKV 上执行`。 当前的执行计划在 task 级别的拓扑关系是一个 root task 后面可以跟许多 cop task，root task 使用 cop task 的输出结果作为输入。 cop task 中执行的也即是 TiDB 下推到 TiKV 上的任务，每个 cop task 分散在 TiKV 集群中，由多个进程共同执行。
    
- `operator info` 每个算子的详细信息。各个算子的 operator info 各有不同。
    

**`EXPLAIN ANALYZE`** `SELECT * FROM table1` **EXPLAIN 语句的扩展**

- `time` 显示从进入算子到离开算子的全部 wall time，包括所有子算子操作的全部执行时间。 如果该算子被父算子多次调用 (`loops`)，这个时间就是累积的时间。
    
- `loops` 是当前算子被父算子的调用次数。
    
- `rows` 是当前算子返回的行的总数。 例如，可以将 `count` 列的精度和 `execution_info` 列中的 rows/loops 值进行对比，据此评定查询优化器估算的精确度。
    

* * *

##### 1\. 添加索引之前(慢SQL)

```sql
MySQL [dev2_dc_test]>
MySQL [dev2_dc_test]> EXPLAIN SELECT * FROM dc_organ_mapping_todo WHERE organ_code = 'C0001';
+---------------------+--------+------+--------------------------------------------------------------------------------+
| id                  | count  | task | operator info                                                                  |
+---------------------+--------+------+--------------------------------------------------------------------------------+
| TableReader_7       | 0.69   | root | data:Selection_6                                                               |
| └─Selection_6       | 0.69   | cop  | eq(dev2_dc_test.dc_organ_mapping_todo.organ_code, "C0001")                     |
|   └─TableScan_5     | 689.00 | cop  | table:dc_organ_mapping_todo, range:[-inf,+inf], keep order:false, stats:pseudo |
+---------------------+--------+------+--------------------------------------------------------------------------------+
3 rows in set (0.00 sec)
```

* * *

##### 2\. 添加索引

```
MySQL [dev2_dc_test]>
MySQL [dev2_dc_test]> ALTER TABLE dc_organ_mapping_todo add index idx_name(organ_code);
Query OK, 0 rows affected (0.46 sec)
```

* * *

##### 3\. 添加索引之后(优化后SQL)

```sql
MySQL [dev2_dc_test]>
MySQL [dev2_dc_test]> EXPLAIN SELECT * FROM dc_organ_mapping_todo WHERE organ_code = 'C0001';
+-------------------+-------+------+--------------------------------------------------------------------------------------------------------+
| id                | count | task | operator info                                                                                          |
+-------------------+-------+------+--------------------------------------------------------------------------------------------------------+
| IndexLookUp_10    | 0.86  | root |                                                                                                        |
| ├─IndexScan_8     | 0.86  | cop  | table:dc_organ_mapping_todo, index:organ_code, range:["C0001","C0001"], keep order:false, stats:pseudo |
| └─TableScan_9     | 0.86  | cop  | table:dc_organ_mapping_todo, keep order:false, stats:pseudo                                            |
+-------------------+-------+------+--------------------------------------------------------------------------------------------------------+
3 rows in set (0.00 sec)

MySQL [dev2_dc_test]>
```

* * *

##### 4\. 解释：

这个结果 是要从下往上读，因为TiDB 算子的数据流动是自底向上的 1. 它先执行的是 TableScan\_5语句， 2. 然后是基于TableScan\_5的结果执行 Selection\_6语句， 3. 最后是基于Selection\_6的结果执行 TableReader\_7语句，它是把Selection\_6的结果返回给了客户端

```sql
+---------------------+--------+-------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| id                  | count  | task                          | operator info                                                                                                                                                             |
+---------------------+--------+-------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| TableReader_7       | 0.69   | root(表示TiDB中进行的计算)    | data:Selection_6                                                                                                                                                          |
| └─Selection_6       | 0.69   | cop (表示TiKV中进行的计算)    | eq(dev2_dc_test.dc_organ_mapping_todo.organ_code, "C0001")                                                                                                                |
|   └─TableScan_5     | 689.00 | cop (表示TiKV中进行的计算)    | table:dc_organ_mapping_todo(表示对哪个表进行扫描), range:[-inf,+inf](表示扫描的范围是 全表扫), keep order:false(表示不需要向上层保持一定的顺序), stats:pseudo             |
+---------------------+--------+-------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
3 rows in set (0.00 sec)

MySQL [dev2_dc_test]>
```

* * *

##### 5\. **名词作用解释**

###### **TableReader** 和 **TableScan**

1. `TableScan` 表示在 KV 端对表数据进行扫描。
2. `TableReader` 表示在 TiDB 端从 TiKV 端读取，属于同一功能的两个算子。
3. `table` 表示 SQL 语句中的表名，如果表名被重命名，则显示重命名。
4. `range` 表示扫描的数据范围，如果在查询中不指定 WHERE/HAVING/ON 条件，则会选择全表扫描，如果在 int 类型的主键上有范围查询条件，会选择范围查询。
5. `keep order` 表示 table scan 是否按顺序返回

* * *

###### **IndexReader** 和 **IndexLookUp**

Index 在 TiDB 端的读取方式有两种： 1. `IndexReader` 表示直接从索引中读取索引列，适用于 SQL 语句中仅引用了该索引相关的列或主键。 2. `IndexLookUp` 表示从索引中过滤部分数据，仅返回这些数据的 Handle ID，通过 Handle ID 再次查找表数据，这种方式需要两次从 TiKV 获取数据。Index 的读取方式是由优化器自动选择的。

* * *

###### **IndexScan**

1. `IndexScan` 是 KV 端读取索引数据的算子，和 TableScan 功能类似。
2. `table` 表示 SQL 语句中的表名，如果表名被重命名，则显示重命名。
3. `index` 表示索引名。
4. `range` 表示扫描的数据范围。
5. `out of order` 表示 index scan 是否按照顺序返回。 注意在 TiDB 中，多列或者非 int 列构成的主键是当作唯一索引处理的。

* * *

###### **Selection**

1. `Selection` 表示 SQL 语句中的选择条件，通常出现在 WHERE/HAVING/ON 子句中。

* * *

###### **Projection**

1. `Projection` 对应 SQL 语句中的 SELECT 列表，功能是将每一条输入数据映射成新的输出数据。(可以理解为，编译后的SQL语句)

* * *

###### **Aggregation**

1. `Aggregation` 对应 SQL 语句中的 Group By 语句或者没有 Group By 语句但是存在聚合函数，例如 count 或 sum 函数等。

* * *

###### **Join**

1. `Join` TiDB 支持 Inner Join 以及 Left/Right Outer Join，并会自动将可以化简的外连接转换为 Inner Join。

* * *

###### **Apply**

1. `Apply` 是 TiDB 用来描述子查询的一种算子，行为类似于 Nested Loop，即每次从外表中取一条数据，带入到内表的关联列中，并执行，最后根据 Apply 内联的 Join 算法进行连接计算。

* * *
