---
title: 'MariaDB 10.4.7&#8211;>主从复制到&#8211;>TiDB 3.0'
date: '2019-08-07T08:39:30+00:00'
status: publish
permalink: /2019/08/07/mariadb-10-4-7-%e4%b8%bb%e4%bb%8e%e5%a4%8d%e5%88%b6%e5%88%b0-tidb-3-0
author: 毛巳煜
excerpt: ''
type: post
id: 4987
category:
    - TiDB
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
#### MariaDB 10.4.7 同步到 TiDB 3.0

MariaDB(主) --&gt; Syncer --&gt; TiDB(从)

- 开发服务器 TiDB 3.0： 
  - IP: 172.160.180.46
  - 用户名: root
  - 密码：数据库密码
  - 端口: 4000
  - 数据库：eric\_tidb\_test
  - 备份路径：./backup\_0
- MariaDB 10.4.7： 
  - IP: 172.160.180.6
  - 用户名: root
  - 密码：数据库密码
  - 端口: 3305
  - 数据库：eric\_tidb\_test

##### 创建MySQL测试表 t1

```sql
MariaDB [eric_tidb_test]> CREATE TABLE t1 ( NAME VARCHAR ( 65530 ) DEFAULT NULL, VALUE VARCHAR ( 1 ) DEFAULT NULL ) charset = latin1;
Query OK, 0 rows affected (0.204 sec)

MariaDB [eric_tidb_test]> show tables;
+--------------------------+
| Tables_in_eric_tidb_test |
+--------------------------+
| t1                       |
+--------------------------+
1 row in set (0.000 sec)

MariaDB [eric_tidb_test]>

```

##### 1 检查源库 server-id

```sql
MariaDB [eric_tidb_test]> show global variables like 'server_id';
+---------------+-------+
| Variable_name | Value |
+---------------+-------+
| server_id     | 6     |
+---------------+-------+
1 row in set (0.001 sec)

MariaDB [eric_tidb_test]>

```

- 结果为空或者为 0，Syncer 无法同步数据。
- Syncer server-id 与 MySQL server-id 不能相同，且必须在 MySQL cluster 中唯一。

##### 2 检查 MySQL 是否开启了 binlog。

```sql
MariaDB [eric_tidb_test]> show global variables like 'log_bin';
+---------------+-------+
| Variable_name | Value |
+---------------+-------+
| log_bin       | OFF   |
+---------------+-------+
1 row in set (0.001 sec)

MariaDB [eric_tidb_test]>

```

- 结果是 log\_bin = OFF，则需要开启 binlog

修改 MariaDB 的配置文件 my.cnf， 改变如下属性之后重启数据库，即可开启binlog

```ruby
......
# 开启binlog的配置在这里
server-id               = 6
log_bin                 = /var/log/mysql/mariadb-bin
log_bin_index           = /var/log/mysql/mariadb-bin.index
expire_logs_days        = 10
binlog_format           = ROW
# binlog的基本配置结束
......

```

##### 3 binlog 格式必须为 ROW

`binlog 格式必须为 ROW，且参数 binlog_row_image 必须设置为 FULL，可使用如下命令查看参数设置：`

```sql
MariaDB [eric_tidb_test]> select variable_name, variable_value from information_schema.global_variables where variable_name in ('binlog_format','binlog_row_image');
+------------------+----------------+
| variable_name    | variable_value |
+------------------+----------------+
| BINLOG_ROW_IMAGE | FULL           |
| BINLOG_FORMAT    | MIXED          |
+------------------+----------------+
2 rows in set (0.001 sec)

MariaDB [eric_tidb_test]>

```

- binlog 格式不为 ROW时的查询结果

```sql
MariaDB [(none)]>  select variable_name, variable_value from information_schema.global_variables where variable_name in ('binlog_format','binlog_row_image');
+------------------+----------------+
| variable_name    | variable_value |
+------------------+----------------+
| BINLOG_ROW_IMAGE | FULL           |
| BINLOG_FORMAT    | ROW            |
+------------------+----------------+
2 rows in set (0.002 sec)

MariaDB [(none)]>

```

- binlog 格式为 ROW时的查询结果

**Binlog 有三种模式：**

- `STATEMENT`：顾名思义，STATEMENT 格式的 Binlog 记录的是数据库上执行的原生SQL语句
- `ROW`：这种格式的 Binlog 记录的是数据表的行是怎样被修改的。
- `MIXED`：混合模式，如果设置了这种格式，MariaDB / MySQL 会在一些特定的情况下自动从 STATEMENT 格式切换到 ROW 格式。例如，包含 UUID 等不确定性函数的语句，引用了系统变量的语句等等。

##### 4 检查用户权限

为所同步的数据库或者表，执行下面的 GRANT 语句：  
给 MariaDB(主库)的 root 账号至少赋予 SELECT, replication SLAVE, replication client 权限

```sql
MariaDB [(none)]> GRANT SELECT, replication SLAVE, replication client ON *.* TO 'root' @'172.160.180.6';
Query OK, 0 rows affected (0.049 sec)

MariaDB [(none)]>

```

给 TiDB(从库)的 root 账号赋予 SELECT,INSERT,UPDATE,DELETE,CREATE,DROP,ALTER,INDEX

```sql
mysql> GRANT SELECT,INSERT,UPDATE,DELETE,CREATE,DROP,ALTER,INDEX  ON eric_tidb_test TO 'root'@'172.160.180.46';
Query OK, 1 row affected (0.24 sec)

mysql>

```

- GRANT命令 参考资料：https://blog.csdn.net/bbwangj/article/details/80778113

##### 5 检查 SQL mode

必须确认上下游的 SQL mode 一致；如果不一致，则会出现数据同步的错误。

###### MariaDB 的 SQL mode

```sql
MariaDB [(none)]> show variables like '%sql_mode%';
+---------------+-------------------------------------------------------------------------------------------+
| Variable_name | Value                                                                                     |
+---------------+-------------------------------------------------------------------------------------------+
| sql_mode      | STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION |
+---------------+-------------------------------------------------------------------------------------------+
1 row in set (0.002 sec)

MariaDB [(none)]>

```

###### TiDB 的 SQL mode

```sql
mysql> show variables like '%sql_mode%';
+---------------+--------------------------------------------+
| Variable_name | Value                                      |
+---------------+--------------------------------------------+
| sql_mode      | STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION |
+---------------+--------------------------------------------+
1 row in set (0.00 sec)

mysql>

```

- 修改 MariaDB 的配置 my.cnf， 改变sql\_mode属性与 TiDB相同
- sql\_mode = STRICT\_TRANS\_TABLES,NO\_ENGINE\_SUBSTITUTION

#### Syncer 的部署位置

Syncer 可以部署在任一台可以连通对应的 MySQL 和 TiDB 集群的机器上，推荐部署在 TiDB 集群。

###### 1 备份MySQL数据库

```ruby
[tidb@test1 bin]$ ./mydumper -h 172.160.180.6 -u root -p 数据库密码 -P 3305 -t 16 -F 64 -B eric_tidb_test --skip-tz-utc -o ./backup_mysql_0

```

###### 2 将数据同步到从库

```ruby
[tidb@test1 bin]$ ./loader -h 172.160.180.46 -u root -p 数据库密码 -P 4000 -t 32 -d ./backup_mysql_0/

```

###### 3 查看 metadata

```ruby
[tidb@test1 bin]<span class="katex math inline">cd backup_mysql_0/
[tidb@test1 backup_mysql_0]</span> ll
总用量 12
-rw-rw-r-- 1 tidb tidb  96 8月   7 14:15 eric_tidb_test-schema-create.sql
-rw-rw-r-- 1 tidb tidb 199 8月   7 14:15 eric_tidb_test.t1-schema.sql
-rw-rw-r-- 1 tidb tidb 143 8月   7 14:15 metadata
[tidb@test1 bin]<span class="katex math inline">cat backup_mysql_0/metadata
Started dump at: 2019-08-07 14:58:04
SHOW MASTER STATUS:
        Log: mariadb-bin.000001
        Pos: 623
        GTID: 0-6-1

Finished dump at: 2019-08-07 14:58:04
[tidb@test1 bin]</span>

```

###### 根据metadata文件 配置 syncer.meta文件

```ruby
[tidb@test1 bin]<span class="katex math inline">pwd
/home/tidb/tidb-enterprise-tools-latest-linux-amd64/bin
[tidb@test1 bin]</span>
[tidb@test1 bin]$ cat > syncer.meta 
```

###### 创建 config.toml文件

```ruby
[tidb@test1 bin]$ cat > config.toml  replicate-do-table --> replicate-ignore-db --> replicate-ignore-table
## 指定要同步数据库名；支持正则匹配，表达式语句必须以 \`~\` 开始
#replicate-do-db = ["~^b.*","s1"]

## 指定 **忽略** 同步数据库；支持正则匹配，表达式语句必须以 \`~\` 开始
#replicate-ignore-db = ["~^b.*","s1"]

# skip-dmls 支持跳过 DML binlog events，type 字段的值可为：'insert'，'update' 和 'delete'
# 跳过 foo.bar 表的所有 delete 语句
# [[skip-dmls]]
# db-name = "foo"
# tbl-name = "bar"
# type = "delete"
#
# 跳过所有表的 delete 语句
# [[skip-dmls]]
# type = "delete"
#
# 跳过 foo.* 表的 delete 语句
# [[skip-dmls]]
# db-name = "foo"
# type = "delete"

## 指定要同步的 db.table 表
## db-name 与 tbl-name 不支持 \`db-name ="dbname，dbname2"\` 格式
#[[replicate-do-table]]
#db-name ="eric_tidb_test"
#tbl-name = "t1"

#[[replicate-do-table]]
#db-name ="dbname1"
#tbl-name = "table-name1"

## 指定要同步的 db.table 表；支持正则匹配，表达式语句必须以 \`~\` 开始
#[[replicate-do-table]]
#db-name ="test"
#tbl-name = "~^a.*"

## 指定 **忽略** 同步数据库
## db-name & tbl-name 不支持 \`db-name ="dbname，dbname2"\` 语句格式
#[[replicate-ignore-table]]
#db-name = "your_db"
#tbl-name = "your_table"

## 指定要 **忽略** 同步数据库名；支持正则匹配，表达式语句必须以 \`~\` 开始
#[[replicate-ignore-table]]
#db-name ="test"
#tbl-name = "~^a.*"

# sharding 同步规则，采用 wildcharacter
# 1. 星号字符 (*) 可以匹配零个或者多个字符,
#    例子, doc* 匹配 doc 和 document, 但是和 dodo 不匹配;
#    星号只能放在 pattern 结尾，并且一个 pattern 中只能有一个
# 2. 问号字符 (?) 匹配任一一个字符

#[[route-rules]]
#pattern-schema = "route_*"
#pattern-table = "abc_*"
#target-schema = "route"
#target-table = "abc"

#[[route-rules]]
#pattern-schema = "route_*"
#pattern-table = "xyz_*"
#target-schema = "route"
#target-table = "xyz"

# MariaDB 10.4.7
[from]
host = "172.160.180.6"
user = "root"
password = "q1w2E#R"
port = 3305

# 开发服务器 TiDB 3.0
[to]
host = "172.160.180.46"
user = "root"
password = "q1w2E#R\$"
port = 4000
eric

```

##### 执行同步数据

```ruby
[tidb@test1 bin]<span class="katex math inline">./syncer -config config.toml
# 正式运行时，使用后台运行
[tidb@test1 bin]</span> nohup ./syncer -config config.toml &

```