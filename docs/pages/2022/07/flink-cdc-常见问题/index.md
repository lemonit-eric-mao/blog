---
title: "Flink-CDC 常见问题"
date: "2022-07-05"
categories: 
  - "flink"
---

> - **timezone region not found**

```sql
java.sql.SQLException: ORA-00604: error occurred at recursive SQL level 1
ORA-01882: timezone region not found
```

- **原因：** 容器中的时区也Oralce数据库的时区不一致导致的
- **解决方法：**

```yaml
...
    environment:
      - |
        TZ= Asia/Shanghai              # 同步容器时区
      - |
        FLINK_PROPERTIES=
        jobmanager.rpc.address: jobmanager
        taskmanager.numberOfTaskSlots: 20

    volumes:
      - /etc/localtime:/etc/localtime  # 同步容器时区
...
```

* * *

> - **使用Flink SQL 查询Oracle库时引发异常**

```sql
[ERROR] Could not execute SQL statement. Reason:
java.sql.SQLException: ORA-00604: error occurred at recursive SQL level 1
ORA-01882: timezone region not found
```

- **原因：** 当使用 JDBC 版本 11.2.0.1 和更高版本连接到 Oracle 数据库时，驱动程序现在会将配置的时区发送到 Oracle。有时会出现问题，因为 JDBC 客户端不检查它发送的时区是否受 Oracle 数据库支持。如果 Oracle 数据库不知道客户端发送的时区，则会导致上述连接错误。 https://community.boomi.com/s/article/ORA-01882-timezone-region-not-found

* * *

> - **使用Flink SQL 查询目标库时引发异常**

```sql
Flink SQL>

-- 执行
SELECT * FROM target_db_table_sink;
-- 异常信息
[ERROR] Could not execute SQL statement. Reason:
java.lang.ClassNotFoundException: org.apache.flink.connector.jdbc.table.JdbcRowDataInputFormat
```

- **原因：** 目标库只能做为输入，不能进行查询

* * *

> - 如何使用 JDBC进行查询？

```sql
Flink SQL>

-- 注意表的字段类型与目标数据库的字段类型一致即可，但是这种做法，不能做目标数据库进行数据同步
CREATE TABLE target_db_table_sink (
    `id`             INT,
    `name`           VARCHAR,
    `address`        VARCHAR,
    `phone_number`   VARCHAR,
    `email`          VARCHAR,
    PRIMARY KEY (`id`) NOT ENFORCED
  ) WITH (
    'connector'      = 'jdbc',                       -- 表示数据库的链接类型
    'url'            = 'jdbc:mysql://192.168.101.21:3307/db_1',
    'driver'         = 'com.mysql.jdbc.Driver',      -- MySQL 5.x 、MariaDB 通用
    'username'       = 'root',
    'password'       = 'youpasswd',
    'table-name'     = 'user_1'                      -- 指定加载数据库中的哪些表
  );
```

```sql
-- 查看
SELECT * FROM target_db_table_sink;
-- 结果如下
                             SQL Query Result (Table)
 Refresh: 1 s                    Page: Last of 1                     Updated: 01:58:40.734

       id             name          address         phone_number                     email
--------- ---------------- ---------------- -------------------- -------------------------

```

> - **在 Flink SQL 中执行 INSERT INTO 同步数据时引发 TaskManager 异常**
> - **原因：** 缺少依赖的插件包

```java
Caused by: java.lang.ClassNotFoundException: org.apache.flink.connector.jdbc.internal.GenericJdbcSinkFunction
```

* * *
