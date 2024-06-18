---
title: "MySQL 常用命令"
date: "2019-08-20"
categories: 
  - "mysql"
---

##### **[MySQL 常见问题](http://www.dev-share.top/2020/01/09/mysql-%e5%b8%b8%e8%a7%81%e9%97%ae%e9%a2%98/ "MySQL 常见问题")**

* * *

* * *

* * *

##### **事件调度器**（**Event Scheduler**）

**说白了，就是 '定时任务'**

```sql
-- 开启调度器
set global event_scheduler = 1;
set global event_scheduler = ON;

-- 关闭调度器
set global event_scheduler = 0;
set global event_scheduler = OFF;

-- 查看 event_scheduler 是否已开启
select @@event_scheduler;
show variables like 'event_scheduler';

```

* * *

* * *

* * *

##### 用户管理

```sql
-- 查看数据库用户
SELECT * FROM mysql.`user`;
```

* * *

###### 创建用户

**CREATE USER `'用户名'`@`'允许登录的主机'` IDENTIFIED BY `'密码'`;**

```sql
-- 创建用户: eric  密码: passwd_eric
CREATE USER 'eric'@'%' IDENTIFIED BY 'passwd_eric';
```

* * *

###### 修改密码

```sql
ALTER USER 'eric'@'%' IDENTIFIED BY '数据库密码';
```

* * *

###### 用户授权

**`注`：** 要想单用户授予多数据库权限，只需修改数据库名称，执行多次下面的语句即可 **GRANT `权限` ON `数据库`.\* TO `'用户名'`@`'允许登录的主机'` IDENTIFIED BY `'密码'`;**

```sql
-- 为用户eric, 授权所有数据库的, 所有权限(此用户拥有可以为其它用户授权的权限，相当于root权限)
GRANT ALL PRIVILEGES ON *.* TO 'eric'@'%' IDENTIFIED BY 'passwd_eric' WITH GRANT OPTION;

-- 为用户eric, 授权所有数据库的, 所有权限(无授权权限)
GRANT ALL PRIVILEGES ON *.* TO 'eric'@'%' IDENTIFIED BY 'passwd_eric';

-- 为用户eric, 授权某个数据库的, 所有权限(无授权权限)
GRANT ALL PRIVILEGES ON test_db.* TO 'eric'@'%' IDENTIFIED BY 'passwd_eric';

-- 为用户eric, 授权某个数据库的, 部分权限(无授权权限)
GRANT SELECT,UPDATE ON test_db.* TO 'eric'@'%' IDENTIFIED BY 'passwd_eric';
```

###### 刷新授权

```sql
FLUSH PRIVILEGES;
```

###### 撤销授权

```sql
-- 撤销 ALL 权限
REVOKE ALL ON *.* FROM 'eric'@'%';

-- 撤销 SELECT, UPDATE 权限
REVOKE SELECT, UPDATE ON test_db.* FROM 'eric'@'%';
```

###### 查看用户权限

```sql
SHOW GRANTS FOR eric;
```

* * *

###### 删除用户

```sql
DROP USER eric;
```

* * *

* * *

* * *

##### 查看表结构，获取建表语句

**SHOW CREATE TABLE `表名`;**

```sql
SHOW CREATE TABLE test1;
```

* * *

* * *

* * *

##### 查询数据库中有多少表

```sql
SELECT
    COUNT( tb.TABLE_NAME )
FROM
    INFORMATION_SCHEMA.TABLES tb
```

* * *

* * *

* * *

##### 查询数据库中, 表行数

```sql
SELECT
    TABLE_NAME,
    TABLE_ROWS
FROM
    INFORMATION_SCHEMA.TABLES
WHERE
    TABLE_SCHEMA = "库名"
ORDER BY
    TABLE_ROWS DESC;
```

* * *

* * *

* * *

##### 定位慢查询

```sql
# 临时开启慢查询日志
MariaDB [(none)]> SET slow_query_log = 1;
Query OK, 0 rows affected (0.06 sec)

MariaDB [(none)]>
MariaDB [(none)]>
# 查看是否开启了 慢查询日志
MariaDB [(none)]> SHOW VARIABLES LIKE '%slow_query_log%';
+---------------------+---------------------------------+
| Variable_name       | Value                           |
+---------------------+---------------------------------+
| slow_query_log      | ON                              |
| slow_query_log_file | /var/log/mysql/mariadb-slow.log |
+---------------------+---------------------------------+
2 rows in set (0.05 sec)

MariaDB [(none)]>
# 查看慢查询语句执行时间的阈值 默认 10.000000 秒 改为 3.000000 秒
MariaDB [(none)]> SET long_query_time = 3.000000;
Query OK, 0 rows affected (0.05 sec)

MariaDB [(none)]> SHOW VARIABLES LIKE 'long_query_time%';
+-----------------+----------+
| Variable_name   | Value    |
+-----------------+----------+
| long_query_time | 3.000000 |
+-----------------+----------+
1 row in set (0.05 sec)

MariaDB [(none)]>
MariaDB [(none)]>
# 查看慢SQL
MariaDB [(none)]> SELECT * FROM mysql.slow_log;
Empty set (0.06 sec)

MariaDB [(none)]>

```

* * *

* * *

* * *

##### 处理死锁

[解读MySQL死锁信息](https://www.jianshu.com/p/6049b046e7b4 "解读MySQL死锁信息")

```sql
-- 获取INNODB引擎当前信息
-- LATEST DETECTED DEADLOCK 记录了最近一次的死锁情况
-- 上面还可以看出两个事务之间发生锁竞争时，给我们留下的部分数据
MySQL [(none)]> SHOW ENGINE INNODB STATUS \G
*************************** 1. row ***************************
  Type: InnoDB
  Name:
Status:
=====================================
2019-12-10 15:54:21 0x7f80c47a5700 INNODB MONITOR OUTPUT
=====================================
Per second averages calculated from the last 21 seconds
-----------------
BACKGROUND THREAD
-----------------
...... 内容无用省略

----------
SEMAPHORES
----------
...... 内容无用省略

------------------------
LATEST DETECTED DEADLOCK
------------------------
2019-12-10 13:15:00 0x7f809c6f9700
*** (1) TRANSACTION: # 事务 1

TRANSACTION 2188445, ACTIVE 0 sec starting index read
mysql tables in use 1, locked 1
LOCK WAIT 3 lock struct(s), heap size 1136, 2 row lock(s)
MySQL thread id 20878, OS thread handle 140190373996288, query id 2310223 172.21.60.209 root Updating
UPDATE dc_temp_mapping_sale 
SET normal_organ_code='H2210009' , normal_organ_name='常德市第二人民医院' , organ_mapping_id='organMapping494681' , is_mapped_organ='1' 
WHERE distributor_code='H2210040' AND organ_name='常德市第二人民医院' 
AND biz_date >= '2019-10-26'
*** (1) WAITING FOR THIS LOCK TO BE GRANTED:
RECORD LOCKS space id 973 page no 535 n bits 96 index PRIMARY of table `prd2_hengrui`.`dc_temp_mapping_sale` trx id 2188445 lock_mode X locks rec but not gap waiting
Record lock, heap no 25 PHYSICAL RECORD: n_fields 54; compact format; info bits 32
 0: len 30; hex 303735316630656562386231343062386166666335363337663365336163; asc 0751f0eeb8b140b8affc5637f3e3ac; (total 32 bytes);
 ...... 内容太多省略
 53: len 1; hex 30; asc 0;;

*** (2) TRANSACTION: # 事务 2
TRANSACTION 2188444, ACTIVE 0 sec updating or deleting
mysql tables in use 1, locked 1
4 lock struct(s), heap size 1136, 3 row lock(s), undo log entries 1
MySQL thread id 31552, OS thread handle 140190357100288, query id 2310224 172.21.60.209 root Updating
DELETE FROM dc_temp_mapping_sale
WHERE distributor_code = 'H2210040' AND biz_date >= '2019-10-26'
    AND is_daily = '1'
*** (2) HOLDS THE LOCK(S):
RECORD LOCKS space id 973 page no 535 n bits 96 index PRIMARY of table `prd2_hengrui`.`dc_temp_mapping_sale` trx id 2188444 lock_mode X locks rec but not gap
Record lock, heap no 25 PHYSICAL RECORD: n_fields 54; compact format; info bits 32
 0: len 30; hex 303735316630656562386231343062386166666335363337663365336163; asc 0751f0eeb8b140b8affc5637f3e3ac; (total 32 bytes);
 ...... 内容太多省略
 53: len 1; hex 30; asc 0;;

*** (2) WAITING FOR THIS LOCK TO BE GRANTED:
RECORD LOCKS space id 973 page no 1669 n bits 176 index organMatchCode of table `prd2_hengrui`.`dc_temp_mapping_sale` trx id 2188444 lock_mode X locks rec but not gap waiting
Record lock, heap no 19 PHYSICAL RECORD: n_fields 3; compact format; info bits 0
 0: len 8; hex 4832323130303430; asc H2210040;;
 1: len 27; hex e5b8b8e5beb7e5b882e7acace4ba8ce4babae6b091e58cbbe999a2; asc                            ;;
 2: len 30; hex 303735316630656562386231343062386166666335363337663365336163; asc 0751f0eeb8b140b8affc5637f3e3ac; (total 32 bytes);

*** WE ROLL BACK TRANSACTION (1) # MYSQL提示回滚了 事务 1
------------
TRANSACTIONS
------------
...... 内容无用省略

--------
FILE I/O
--------
...... 内容无用省略

-------------------------------------
INSERT BUFFER AND ADAPTIVE HASH INDEX
-------------------------------------
...... 内容无用省略

---
LOG
---
...... 内容无用省略

----------------------
BUFFER POOL AND MEMORY
----------------------
...... 内容无用省略

--------------
ROW OPERATIONS
--------------
...... 内容无用省略

----------------------------
END OF INNODB MONITOR OUTPUT
============================

```

```sql
-- 查询进程
SHOW FULL PROCESSLIST;

-- 查看状态为Sleep的进程，然后批量杀死
SELECT CONCAT( 'KILL ', id, ';' ) FROM information_schema.PROCESSLIST WHERE command = 'Sleep';

-- 查询是否锁表
SHOW OPEN TABLES WHERE In_use > 0;

-- 查看正在锁的事务
SELECT * FROM INFORMATION_SCHEMA.INNODB_LOCKS;

-- 查看等待锁的事务
SELECT * FROM INFORMATION_SCHEMA.INNODB_LOCK_WAITS;
```

* * *

* * *

* * *

##### 批量执行删除外键语句

```sql
Welcome to the MariaDB monitor.  Commands end with ; or \g.
Your MariaDB connection id is 974
Server version: 10.3.12-MariaDB MariaDB Server

Copyright (c) 2000, 2017, Oracle, MariaDB Corporation Ab and others.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

MariaDB [(none)]>
MariaDB [(none)]>
MariaDB [(none)]>
MariaDB [information_schema]> use information_schema;
Database changed
MariaDB [information_schema]>
MariaDB [information_schema]>
MariaDB [information_schema]>
    SELECT
       CONCAT( 'ALTER TABLE ', TABLE_SCHEMA, '.', TABLE_NAME, ' DROP FOREIGN KEY ', CONSTRAINT_NAME, ' ;' )  AS 删除外键
    FROM
       information_schema.TABLE_CONSTRAINTS c
    WHERE
       c.CONSTRAINT_TYPE = 'FOREIGN KEY';
+--------------------------------------------------------------------------------------------------+
| 删除外键                                                                                         |
+--------------------------------------------------------------------------------------------------+
| ALTER TABLE dev2_pfizer_activiti_mandy.act_ru_task DROP FOREIGN KEY ACT_FK_TASK_PROCDEF ;        |
| ALTER TABLE dev2_pfizer_activiti_mandy.act_ru_task DROP FOREIGN KEY ACT_FK_TASK_PROCINST ;       |
| ALTER TABLE dev2_pfizer_activiti_mandy.act_ru_event_subscr DROP FOREIGN KEY ACT_FK_EVENT_EXEC ;  |
| ALTER TABLE dev2_pfizer_activiti_mandy.act_procdef_info DROP FOREIGN KEY ACT_FK_INFO_JSON_BA ;   |
| ALTER TABLE dev2_pfizer_activiti_mandy.act_procdef_info DROP FOREIGN KEY ACT_FK_INFO_PROCDEF ;   |
| ALTER TABLE dev2_pfizer_activiti_mandy.act_re_model DROP FOREIGN KEY ACT_FK_MODEL_DEPLOYMENT ;   |
| ALTER TABLE dev2_pfizer_activiti_mandy.act_re_model DROP FOREIGN KEY ACT_FK_MODEL_SOURCE ;       |
| ALTER TABLE dev2_pfizer_activiti_mandy.act_re_model DROP FOREIGN KEY ACT_FK_MODEL_SOURCE_EXTRA ; |
| ALTER TABLE dev2_pfizer_activiti_mandy.act_ru_variable DROP FOREIGN KEY ACT_FK_VAR_BYTEARRAY ;   |
| ALTER TABLE dev2_pfizer_activiti_mandy.act_ru_variable DROP FOREIGN KEY ACT_FK_VAR_EXE ;         |
| ALTER TABLE dev2_pfizer_activiti_mandy.act_ru_variable DROP FOREIGN KEY ACT_FK_VAR_PROCINST ;    |
| ALTER TABLE dev2_pfizer_activiti_mandy.act_ru_job DROP FOREIGN KEY ACT_FK_JOB_EXCEPTION ;        |
+--------------------------------------------------------------------------------------------------+
12 rows in set (0.06 sec)

MariaDB [information_schema]>
```

* * *

* * *

* * *

##### 更新同一张表中字段

将列**biz\_date**数据`2020-04-02`转为`202004`格式给**biz\_year\_month**列

```sql
UPDATE
    dc_flowdata_deliver_purchase
SET
    biz_year_month = DATE_FORMAT(biz_date, '%Y%m')
WHERE
    biz_year_month = ''
LIMIT 50000
```

* * *

* * *

* * *

###### 查看设置的最大连接数

```sql
mariadb root@127.0.0.1:(none)> show variables like '%max_connections%';
+-----------------------+---------+
| Variable_name         |   Value |
|-----------------------+---------|
| extra_max_connections |       1 |
| max_connections       |     100 |
+-----------------------+---------+
2 rows in set
Time: 0.014s
mariadb root@127.0.0.1:(none)>
```

* * *

###### 查看当前连接数

```sql
mariadb root@127.0.0.1:(none)> show status like 'Threads%';
+-------------------+---------+--------------------------------------------------------------------------------------+
| Variable_name     |   Value |                                                                                      |
|-------------------+---------+--------------------------------------------------------------------------------------|
| Threads_cached    |      10 |                                                                                      |
| Threads_connected |       3 | 表示打开的连接数                                                                      |
| Threads_created   |      86 | 表示创建过的线程数，如果发现threads_created值过大的话，表明mysql服务器一直在创建线程       |
| Threads_running   |       1 | 表示激活的连接数，这个数值一般远低于connected数值                                        |
+-------------------+---------+--------------------------------------------------------------------------------------+
4 rows in set
Time: 0.010s
mariadb root@127.0.0.1:(none)>
```

* * *

* * *

* * *

###### HAVING 的作用是什么?

> HAVING是用于在SQL的GROUP BY语句中，对GROUP BY后的结果进行过滤的关键字。 它的作用类似于WHERE语句，但是它是对GROUP BY后的结果进行过滤，而不是对原始数据进行过滤。 HAVING可以对GROUP BY后的结果进行条件过滤，过滤出符合条件的记录，并将结果返回。 HAVING语句通常用于配合GROUP BY语句使用，它可以用来限制结果集合，并只返回符合条件的结果。 HAVING语句必须在GROUP BY语句之后使用，并且在WHERE语句之前使用。 HAVING语句中的条件可以是聚合函数（如SUM、AVG、COUNT、MAX、MIN）的结果或者列名，也可以是与聚合函数相关的条件表达式，例如SUM(column\_name) > 100。

* * *

* * *

* * *
