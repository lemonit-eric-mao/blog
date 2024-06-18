---
title: "使用 Flink-CDC 实现 MariaDB --> MariaDB"
date: "2022-07-01"
categories: 
  - "flink"
---

##### 前置条件

###### **[Flink-CDC 安装部署](http://www.dev-share.top/2022/06/29/flink-cdc-%e5%ae%89%e8%a3%85%e9%83%a8%e7%bd%b2/ "Flink-CDC 安装部署")**

> - 通俗的讲 **CDC** 是处理数据库**数据同步**的，那么我们就需要先有数据库

* * *

###### **[安装 mariadb](http://www.dev-share.top/2019/08/05/docker-%e5%ae%89%e8%a3%85-mariadb/ "安装 mariadb")** 注意: `源数据库需要开启binlog`

##### 创建两个MariaDB数据库，并在每个数据库中创建两个表

###### **DB\_1**

192.168.101.21:3306

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

INSERT INTO user_1 VALUES (110,"user_110","Shanghai","123567891234","user_110@foo.com"),(120,"user_120","Shanghai","abcdefg","user_120@foo.com");

```

* * *

###### **DB\_2**

192.168.101.21:3307

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

##### 使用 Flink SQL CLI 进行测试

```ruby
docker-compose exec sql-client sql-client.sh -d /opt/flink/conf/sql-client-conf.yaml


                                   ▒▓██▓██▒
                               ▓████▒▒█▓▒▓███▓▒
                            ▓███▓░░        ▒▒▒▓██▒  ▒
                          ░██▒   ▒▒▓▓█▓▓▒░      ▒████
                          ██▒         ░▒▓███▒    ▒█▒█▒
                            ░▓█            ███   ▓░▒██
                              ▓█       ▒▒▒▒▒▓██▓░▒░▓▓█
                            █░ █   ▒▒░       ███▓▓█ ▒█▒▒▒
                            ████░   ▒▓█▓      ██▒▒▒ ▓███▒
                         ░▒█▓▓██       ▓█▒    ▓█▒▓██▓ ░█░
                   ▓░▒▓████▒ ██         ▒█    █▓░▒█▒░▒█▒
                  ███▓░██▓  ▓█           █   █▓ ▒▓█▓▓█▒
                ░██▓  ░█░            █  █▒ ▒█████▓▒ ██▓░▒
               ███░ ░ █░          ▓ ░█ █████▒░░    ░█░▓  ▓░
              ██▓█ ▒▒▓▒          ▓███████▓░       ▒█▒ ▒▓ ▓██▓
           ▒██▓ ▓█ █▓█       ░▒█████▓▓▒░         ██▒▒  █ ▒  ▓█▒
           ▓█▓  ▓█ ██▓ ░▓▓▓▓▓▓▓▒              ▒██▓           ░█▒
           ▓█    █ ▓███▓▒░              ░▓▓▓███▓          ░▒░ ▓█
           ██▓    ██▒    ░▒▓▓███▓▓▓▓▓██████▓▒            ▓███  █
          ▓███▒ ███   ░▓▓▒░░   ░▓████▓░                  ░▒▓▒  █▓
          █▓▒▒▓▓██  ░▒▒░░░▒▒▒▒▓██▓░                            █▓
          ██ ▓░▒█   ▓▓▓▓▒░░  ▒█▓       ▒▓▓██▓    ▓▒          ▒▒▓
          ▓█▓ ▓▒█  █▓░  ░▒▓▓██▒            ░▓█▒   ▒▒▒░▒▒▓█████▒
           ██░ ▓█▒█▒  ▒▓▓▒  ▓█                █░      ░░░░   ░█▒
           ▓█   ▒█▓   ░     █░                ▒█              █▓
            █▓   ██         █░                 ▓▓        ▒█▓▓▓▒█░
             █▓ ░▓██░       ▓▒                  ▓█▓▒░░░▒▓█░    ▒█
              ██   ▓█▓░      ▒                    ░▒█▒██▒      ▓▓
               ▓█▒   ▒█▓▒░                         ▒▒ █▒█▓▒▒░░▒██
                ░██▒    ▒▓▓▒                     ▓██▓▒█▒ ░▓▓▓▓▒█▓
                  ░▓██▒                          ▓░  ▒█▓█  ░░▒▒▒
                      ▒▓▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░▓▓  ▓░▒█░

    ______ _ _       _       _____  ____  _         _____ _ _            _  BETA
   |  ____| (_)     | |     / ____|/ __ \| |       / ____| (_)          | |
   | |__  | |_ _ __ | | __ | (___ | |  | | |      | |    | |_  ___ _ __ | |_
   |  __| | | | '_ \| |/ /  \___ \| |  | | |      | |    | | |/ _ \ '_ \| __|
   | |    | | | | | |   <   ____) | |__| | |____  | |____| | |  __/ | | | |_
   |_|    |_|_|_| |_|_|\_\ |_____/ \___\_\______|  \_____|_|_|\___|_| |_|\__|

        Welcome! Enter 'HELP;' to list all available commands. 'QUIT;' to exit.


Flink SQL>

```

* * *

###### 开启 checkpoint，每隔3秒做一次 checkpoint

```sql
Flink SQL>

SET execution.checkpointing.interval = 3s;
```

###### 关联源数据库中的表

> - 创建 source 表 source\_db\_table 来捕获MySQL中所有 user 表的数据，在表的配置项 database-name , table-name 使用正则表达式来匹配这些表。
> - 并且，source\_db\_table 表也定义了 metadata 列来区分数据是来自哪个数据库和表。

```sql
Flink SQL>

-- 如果 source_db_table 表已经存在，就删除
-- DROP TABLE source_db_table;

CREATE TABLE source_db_table (                       -- 使用 Flink SQL 创建一个虚拟的表，用来收集源数据库中的信息
    `id`             DECIMAL(20, 0) NOT NULL,
    name             STRING,
    address          STRING,
    phone_number     STRING,
    email            STRING,
    PRIMARY KEY (`id`) NOT ENFORCED
) WITH (
    'connector'      = 'mysql-cdc',                  -- 表示数据库的链接类型
    'hostname'       = '192.168.101.21',             -- 数据库主机地址
    'port'           = '3306',
    'username'       = 'root',
    'password'       = 'youpasswd',
    'database-name'  = 'db_1',                       -- 库名过滤，指定加载数据库中的哪些库
    'table-name'     = 'user_1'                      -- 表名过滤，指定加载数据库中的哪些表
);
```

```sql
-- 查看(注意表名要区分大小写)
SELECT * FROM source_db_table;
-- 结果如下
                             SQL Query Result (Table)
 Refresh: 1 s                    Page: Last of 1                     Updated: 01:58:40.734

       id             name          address         phone_number                     email
--------- ---------------- ---------------- -------------------- -------------------------
      110         user_110         Shanghai         123567891234          user_110@foo.com
      111         user_111         Shanghai         123567891234          user_111@foo.com

```

* * *

###### 连接目标数据库表

```sql
Flink SQL>

-- 如果 target_db_table_sink 表已经存在，就删除
-- DROP TABLE target_db_table_sink;

CREATE TABLE target_db_table_sink (
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

INSERT INTO target_db_table_sink select * from source_db_table;
```

* * *

* * *

* * *

###### **[常见问题](http://www.dev-share.top/2022/07/05/flink-cdc-%e5%b8%b8%e8%a7%81%e9%97%ae%e9%a2%98/ "常见问题")**
