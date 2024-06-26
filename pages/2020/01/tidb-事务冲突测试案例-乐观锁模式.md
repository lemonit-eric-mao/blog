---
title: "TiDB 事务冲突测试案例-乐观锁模式"
date: "2020-01-13"
categories: 
  - "tidb"
---

###### 前置条件

**执行SQL的客户端地址**: 172.168.180.46 **执行SQL的客户端地址**: 172.168.180.47 **TiDB-Server**: 172.168.180.47

* * *

###### 创建数据库

```sql
CREATE DATABASE eric;

USE eric;

DROP TABLE table1;

# 创建表
CREATE TABLE `table1` (
  `id` bigint(20) NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

# 插入数据
INSERT INTO table1(id, name) VALUES (1000, '张三'), (2000, 'PingCAP');

# 查看
mysql> SELECT * FROM table1;
+------+---------+
| id   | name    |
+------+---------+
| 1000 | 张三    |
| 2000 | PingCAP |
+------+---------+
2 rows in set (0.00 sec)

mysql>
```

##### 测试更新数据冲突

**`关闭`了乐观锁`事务重试`** `SET GLOBAL tidb_disable_txn_auto_retry = 1;`

| 事务一 | 步骤 | 事务二 |
| --- | :-: | --- |
| 172.168.180.46 |  | 172.168.180.47 |
| 准备数据查询结果 `name='张三'` | **0** | 准备数据查询结果 `name='张三'` |
| BEGIN; | **1** | BEGIN; |
| `UPDATE table1 SET name='TiDB' WHERE id = 1000;` | **2** |  |
| 查询结果 `name='TiDB'` | **3** | 查询结果 `name='张三'` |
|  | **4** | `UPDATE table1 SET name='TUG' WHERE id = 1000;` |
| 查询结果 `name='TiDB'` | **5** | 查询结果 `name='TUG'` |
| COMMIT; | **6** |  |
| 查询结果 `name='TiDB'` | **7** | 查询结果 `name='TUG'` |
|  | **8** | COMMIT; |
|  | **9** | 发生异常写写冲突：  
`ERROR 9007 (HY000): Write conflict,`  
  `txnStartTS=413963720372256769,`  
  `conflictStartTS=413963719952826370,`  
  `conflictCommitTS=413963759746285570,`  
  `key={tableID=54, handle=1000}`  
  `primary={tableID=54, handle=1000}`  
`[try again later]` |

* * *

* * *

* * *

##### 测试更新数据冲突

**`开启`了乐观锁`事务重试`** `SET GLOBAL tidb_disable_txn_auto_retry = 0;`

| 事务一 | 步骤 | 事务二 |
| --- | :-: | --- |
| 172.168.180.46 |  | 172.168.180.47 |
| 准备数据查询结果 `name='张三'` | **0** | 准备数据查询结果 `name='张三'` |
| BEGIN; | **1** | BEGIN; |
| `UPDATE table1 SET name='TiDB' WHERE id = 1000;` | **2** |  |
| 查询结果 `name='TiDB'` | **3** | 查询结果 `name='张三'` |
|  | **4** | `UPDATE table1 SET name='TUG' WHERE id = 1000;` |
| 查询结果 `name='TiDB'` | **5** | 查询结果 `name='TUG'` |
| COMMIT; | **6** |  |
| 查询结果 `name='TiDB'` | **7** | 查询结果 `name='TUG'` |
|  | **8** | COMMIT; |
| 查询结果 `name='TUG'` | **9** | 查询结果 `name='TUG'`;  
注意：这里的写冲突异常不会抛给客户端，而是由TiDB自动重试机制捕获，  
然后`重新执行事务中所有DML`在更新一次 |

* * *

* * *

* * *
