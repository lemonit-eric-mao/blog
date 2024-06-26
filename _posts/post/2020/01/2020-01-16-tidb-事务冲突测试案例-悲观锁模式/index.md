---
title: "TiDB 事务冲突测试案例-悲观锁模式"
date: "2020-01-16"
categories: 
  - "tidb"
---

###### **`注意：`以后在程序设计中不要使用autocommit(`隐式事务`), 因为使用悲观锁时，必须要是`显示事务`**

* * *

###### 前置条件

**执行SQL的客户端地址**: 172.168.180.46 **执行SQL的客户端地址**: 172.168.180.47 **TiDB-Server**: 172.168.180.33

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

* * *

* * *

* * *

##### 测试`更新`数据冲突

| 事务一 | 步骤 | 事务二 |
| --- | :-: | --- |
| 172.168.180.46 |  | 172.168.180.47 |
| 准备数据查询结果 `name='张三'` | **0** | 准备数据查询结果 `name='张三'` |
| BEGIN; | **1** | BEGIN; |
| `UPDATE table1 SET name='TiDB' WHERE id = 1000;` | **2** |  |
| 查询结果 `name='TiDB'` | **3** | 查询结果 `name='张三'` |
|  | **4** | `UPDATE table1 SET name='TUG' WHERE id = 1000;` |
|  | **5** | 此时`事务二`与`事务一`**产生冲突**，一直处于等待状态(获取锁中)，直到**事务一**执行`COMMIT;`或`ROLLBACK;` |
| COMMIT; | **6** |  |
| 查询结果 `name='TiDB'` | **7** | 查询结果 `name='TUG'` |
|  | **8** | COMMIT; |
| 查询结果 `name='TUG'` | **9** | 查询结果 `name='TUG'` |

* * *

* * *

* * *

##### 测试`插入`数据主键冲突

| 事务一 | 步骤 | 事务二 |
| --- | :-: | --- |
| 172.168.180.46 |  | 172.168.180.47 |
| BEGIN; | **1** | BEGIN; |
| `INSERT INTO table1(id, name) VALUES (1000, '张三');` | **2** |  |
| 查询结果 `id='1000' name='张三'` | **3** |  |
|  | **4** | `INSERT INTO table1(id, name) VALUES (1000, '张三'), (2000, 'PingCAP');` |
|  | **5** | 此时`事务二`与`事务一`**产生主键冲突**，一直处于等待状态(获取锁中)，直到**事务一**执行`COMMIT;`或`ROLLBACK;` |
| COMMIT; | **6** |  |
| 查询结果 `id='1000' name='张三'` | **7** | 发生异常：  
`ERROR 1062 (23000):`  
  `Duplicate entry '1000' for key 'PRIMARY'` |
|  | **8** | COMMIT; |
| 查询结果 `id='1000' name='张三'` | **9** | 查询结果 `id='1000' name='张三'` |

* * *

* * *

* * *
