---
title: "使用 Flink-CDC 实现 Oracle --> MariaDB"
date: "2022-07-06"
categories: 
  - "flink"
---

##### 前置资料

###### **[Flink-CDC 安装部署](http://www.dev-share.top/2022/06/29/flink-cdc-%e5%ae%89%e8%a3%85%e9%83%a8%e7%bd%b2/ "Flink-CDC 安装部署")**

**[参考 Oracle 数据库使用手册，开启归档日志](http://www.dev-share.top/2022/07/06/oracle-%e6%95%b0%e6%8d%ae%e5%ba%93%e4%bd%bf%e7%94%a8%e6%89%8b%e5%86%8c/ "参考 Oracle 数据库使用手册，开启归档日志")**

* * *

#### **`Oracle 11g` 配置方法**

##### 创建用户

**在Oracle数据库中为`Flink-CDC`创建特定用户 账号为 `flinkuser` 密码为 `youpasswd`**

###### **Oracle `11g` 语句**

```sql
-- 创建用户flinkuser，并指定默认的表空间 为 LOGMINER_TBS
CREATE USER flinkuser IDENTIFIED BY youpasswd DEFAULT TABLESPACE LOGMINER_TBS QUOTA UNLIMITED ON LOGMINER_TBS;
GRANT CREATE SESSION TO flinkuser;
-- GRANT SET CONTAINER TO flinkuser; 11g 中没有容器的概念，所以这条不需要
GRANT SELECT ON V_$DATABASE to flinkuser;
GRANT FLASHBACK ANY TABLE TO flinkuser;
GRANT SELECT ANY TABLE TO flinkuser;
GRANT SELECT_CATALOG_ROLE TO flinkuser;
GRANT EXECUTE_CATALOG_ROLE TO flinkuser;
GRANT SELECT ANY TRANSACTION TO flinkuser;
GRANT LOGMINING TO flinkuser;

GRANT CREATE TABLE TO flinkuser;
GRANT LOCK ANY TABLE TO flinkuser;
GRANT ALTER ANY TABLE TO flinkuser;
GRANT CREATE SEQUENCE TO flinkuser;

GRANT EXECUTE ON DBMS_LOGMNR TO flinkuser;
GRANT EXECUTE ON DBMS_LOGMNR_D TO flinkuser;

GRANT SELECT ON V_$LOG TO flinkuser;
GRANT SELECT ON V_$LOG_HISTORY TO flinkuser;
GRANT SELECT ON V_$LOGMNR_LOGS TO flinkuser;
GRANT SELECT ON V_$LOGMNR_CONTENTS TO flinkuser;
GRANT SELECT ON V_$LOGMNR_PARAMETERS TO flinkuser;
GRANT SELECT ON V_$LOGFILE TO flinkuser;
GRANT SELECT ON V_$ARCHIVED_LOG TO flinkuser;
GRANT SELECT ON V_$ARCHIVE_DEST_STATUS TO flinkuser;

```

* * *

* * *

* * *

##### 在Oracle的表空间中，创建表

```ruby
[oracle@oracle11g ~]$ sqlplus /nolog
```

```sql
SQL> conn flinkuser/youpasswd
Connected.


SQL> show user
USER is "FLINKUSER"
SQL>

```

```sql
CREATE TABLE user_1 (
  id INTEGER NOT NULL PRIMARY KEY,
  name VARCHAR2(255) DEFAULT 'flink_11g',
  address VARCHAR2(1024),
  phone_number VARCHAR2(512),
  email VARCHAR2(255)
) TABLESPACE LOGMINER_TBS;

-- 同时插入多条数据
INSERT ALL
  INTO FLINKUSER.user_1 VALUES ( 110, 'user_110_11g', 'Shanghai', '123567891234', 'user_110@foo.com' )
  INTO FLINKUSER.user_1 VALUES ( 120, 'user_120_11g', 'Shanghai', 'abcdefg', 'user_120@foo.com' )
-- Dual就是一个空表。它是Oracle提供的最小的工作表。它只有一行和一列。它通常用于通过select语句计算常量表达式。
SELECT * FROM dual;

```

* * *

##### 在MariaDB中创建测试数据库

```sql
CREATE DATABASE db_1;
USE db_1;
CREATE TABLE user_1 (
  id INTEGER NOT NULL PRIMARY KEY,
  name VARCHAR(255) NOT NULL DEFAULT 'flink',
  address VARCHAR(1024),
  phone_number VARCHAR(512),
  email VARCHAR(255)
);

```

* * *

* * *

* * *

##### 依赖组件

> - flink-sql-connector-oracle-cdc-2.2.1.jar flink-connector-jdbc\_2.12-1.14.5.jar mysql-connector-java-8.0.21.jar

* * *

#### 使用 Flink SQL CLI 进行测试

```ruby
docker-compose exec sql-client sql-client.sh -d /opt/flink/conf/sql-client-conf.yaml

```

**开启 checkpoint，每隔3秒做一次 checkpoint**

```sql
Flink SQL>

SET execution.checkpointing.interval = 3s;
```

###### 关联源数据库(**Oracle**)中的表

```sql
-- 如果 source_db_table_11g 表已经存在，就删除
-- DROP TABLE source_db_table_11g;

CREATE TABLE source_db_table_11g (                   -- 注意：关联Oracle数据库时，字段名必须是大写，否则查不出来数据
    ID               INT NOT NULL,
    NAME             STRING,
    ADDRESS          STRING,
    PHONE_NUMBER     STRING,
    EMAIL            STRING,
    PRIMARY KEY (ID) NOT ENFORCED
) WITH (
    'connector'      = 'oracle-cdc',                 -- 表示数据库的链接类型
    'hostname'       = '192.168.101.19',             -- 数据库主机地址
    'port'           = '1521',
    'username'       = 'flinkuser',
    'password'       = 'youpasswd',
    'database-name'  = 'ORCL',                       -- 库名过滤，指定加载数据库中的哪些库
    'schema-name'    = 'FLINKUSER',
    'table-name'     = 'USER_1'                      -- 表名过滤，指定加载数据库中的哪些表
);

```

**查看连接**

```sql
SELECT * FROM source_db_table_11g;
```

* * *

###### 连接目标数据库表

```sql
Flink SQL>

-- 如果 target_db_table_sink_mariadb_3306 表已经存在，就删除
-- DROP TABLE target_db_table_sink_mariadb_3306;

CREATE TABLE target_db_table_sink_mariadb_3306 (
    `id`             DECIMAL(20, 0) NOT NULL,
    name             STRING,
    address          STRING,
    phone_number     STRING,
    email            STRING,
    PRIMARY KEY (`id`) NOT ENFORCED
) WITH (
    'connector'      = 'jdbc',                       -- 表示数据库的链接类型
    'url'            = 'jdbc:mysql://192.168.101.21:3306/db_1',
    'driver'         = 'com.mysql.jdbc.Driver',      -- MySQL 5.x 、MariaDB 通用
    'username'       = 'root',
    'password'       = 'youpasswd',
    'table-name'     = 'user_1'                      -- 指定加载数据库中的哪些表
);

```

* * *

###### 使用 **Flink SQL** 语句将数据从源 **数据库** 写入 **目标库** 中

```sql
Flink SQL>

INSERT INTO target_db_table_sink_mariadb_3306 select * from source_db_table_11g;
```

* * *

* * *

* * *

* * *

* * *

* * *

* * *

* * *

* * *

#### **`Oracle 12c` 配置方法**

##### 创建用户

**在Oracle数据库中为`Flink-CDC`创建特定用户 账号为 `c##flinkuser` 密码为 `youpasswd`**

> 因为创建的库是**CDB**不是**PDB**。连接到 **PDB** 就不用写**C##** 了。 或者不启用 **PDB** 。

###### **Oracle `12c` 语句**

```sql
-- 创建用户c##flinkuser，并指定默认的表空间 为 LOGMINER_TBS
CREATE USER c##flinkuser IDENTIFIED BY youpasswd DEFAULT TABLESPACE LOGMINER_TBS QUOTA UNLIMITED ON LOGMINER_TBS;
GRANT CREATE SESSION TO c##flinkuser;
GRANT SET CONTAINER TO c##flinkuser;
GRANT SELECT ON V_$DATABASE to c##flinkuser;
GRANT FLASHBACK ANY TABLE TO c##flinkuser;
GRANT SELECT ANY TABLE TO c##flinkuser;
GRANT SELECT_CATALOG_ROLE TO c##flinkuser;
GRANT EXECUTE_CATALOG_ROLE TO c##flinkuser;
GRANT SELECT ANY TRANSACTION TO c##flinkuser;
GRANT LOGMINING TO c##flinkuser;

GRANT CREATE TABLE TO c##flinkuser;
GRANT LOCK ANY TABLE TO c##flinkuser;
GRANT ALTER ANY TABLE TO c##flinkuser;
GRANT CREATE SEQUENCE TO c##flinkuser;

GRANT EXECUTE ON DBMS_LOGMNR TO c##flinkuser;
GRANT EXECUTE ON DBMS_LOGMNR_D TO c##flinkuser;

GRANT SELECT ON V_$LOG TO c##flinkuser;
GRANT SELECT ON V_$LOG_HISTORY TO c##flinkuser;
GRANT SELECT ON V_$LOGMNR_LOGS TO c##flinkuser;
GRANT SELECT ON V_$LOGMNR_CONTENTS TO c##flinkuser;
GRANT SELECT ON V_$LOGMNR_PARAMETERS TO c##flinkuser;
GRANT SELECT ON V_$LOGFILE TO c##flinkuser;
GRANT SELECT ON V_$ARCHIVED_LOG TO c##flinkuser;
GRANT SELECT ON V_$ARCHIVE_DEST_STATUS TO c##flinkuser;

```

* * *

* * *

* * *

##### 在Oracle的表空间中，创建表

```sql
SQL> conn c##flinkuser/youpasswd
Connected.


SQL> show user
USER is "C##FLINKUSER"
SQL>

```

```sql
CREATE TABLE user_1 (
  id INTEGER NOT NULL PRIMARY KEY,
  name VARCHAR2(255) DEFAULT 'flink_12c',
  address VARCHAR2(1024),
  phone_number VARCHAR2(512),
  email VARCHAR2(255)
) TABLESPACE LOGMINER_TBS;

-- 同时插入多条数据
INSERT ALL
  INTO c##FLINKUSER.user_1 VALUES ( 110, 'user_110_12c', 'Shanghai', '123567891234', 'user_110@foo.com' )
  INTO c##FLINKUSER.user_1 VALUES ( 120, 'user_120_12c', 'Shanghai', 'abcdefg', 'user_120@foo.com' )
-- Dual就是一个空表。它是Oracle提供的最小的工作表。它只有一行和一列。它通常用于通过select语句计算常量表达式。
SELECT * FROM dual;

```

* * *

##### 在MariaDB中创建测试数据库

```sql
CREATE DATABASE db_2;
USE db_2;
CREATE TABLE user_1 (
  id INTEGER NOT NULL PRIMARY KEY,
  name VARCHAR(255) NOT NULL DEFAULT 'flink',
  address VARCHAR(1024),
  phone_number VARCHAR(512),
  email VARCHAR(255)
);

```

* * *

* * *

* * *

##### 依赖组件

> - flink-sql-connector-oracle-cdc-2.2.1.jar flink-connector-jdbc\_2.12-1.14.5.jar mysql-connector-java-8.0.21.jar

* * *

#### 使用 Flink SQL CLI 进行测试

```ruby
docker-compose exec sql-client sql-client.sh -d /opt/flink/conf/sql-client-conf.yaml

```

**开启 checkpoint，每隔3秒做一次 checkpoint**

```sql
Flink SQL>

SET execution.checkpointing.interval = 3s;
```

###### 关联源数据库(**Oracle**)中的表

```sql
-- 如果 source_db_table_12c 表已经存在，就删除
-- DROP TABLE source_db_table_12c;

CREATE TABLE source_db_table_12c (                   -- 注意：关联Oracle 12c数据库时，字段名必须是大写，否则查不出来数据
    ID               INT NOT NULL,
    NAME             STRING,
    ADDRESS          STRING,
    PHONE_NUMBER     STRING,
    EMAIL            STRING,
    PRIMARY KEY (ID) NOT ENFORCED
) WITH (
    'connector'      = 'oracle-cdc',                 -- 表示数据库的链接类型
    'hostname'       = '192.168.101.20',             -- 数据库主机地址
    'port'           = '1521',
    'username'       = 'c##flinkuser',
    'password'       = 'youpasswd',
    'database-name'  = 'orcl',                       -- 库名过滤，指定加载数据库中的哪些库
    'schema-name'    = 'c##flinkuser',
    'table-name'     = 'user_1'                      -- 表名过滤，指定加载数据库中的哪些表
);

```

**查看连接**

```sql
-- 查看(注意表名要区分大小写)
SELECT * FROM source_db_table_12c;
-- 结果如下
                             SQL Query Result (Table)
 Refresh: 1 s                    Page: Last of 1                     Updated: 01:58:40.734

       id             name          address         phone_number                     email
--------- ---------------- ---------------- -------------------- -------------------------
      110     user_110_12c         Shanghai         123567891234          user_110@foo.com
      111     user_111_12c         Shanghai         123567891234          user_111@foo.com

```

* * *

###### 连接目标数据库表

```sql
Flink SQL>

-- 如果 target_db_table_sink_mariadb_3307 表已经存在，就删除
-- DROP TABLE target_db_table_sink_mariadb_3307;

CREATE TABLE target_db_table_sink_mariadb_3307 (
    `id`             DECIMAL(20, 0) NOT NULL,
    name             STRING,
    address          STRING,
    phone_number     STRING,
    email            STRING,
    PRIMARY KEY (`id`) NOT ENFORCED
) WITH (
    'connector'      = 'jdbc',                       -- 表示数据库的链接类型
    'url'            = 'jdbc:mysql://192.168.101.21:3307/db_2',
    'driver'         = 'com.mysql.jdbc.Driver',      -- MySQL 5.x 、MariaDB 通用
    'username'       = 'root',
    'password'       = 'youpasswd',
    'table-name'     = 'user_1'                      -- 指定加载数据库中的哪些表
);

```

* * *

###### 使用 **Flink SQL** 语句将数据从源 **数据库** 写入 **目标库** 中

```sql
Flink SQL>

INSERT INTO target_db_table_sink_mariadb_3307 select * from source_db_table_12c;
```

* * *

* * *

* * *
