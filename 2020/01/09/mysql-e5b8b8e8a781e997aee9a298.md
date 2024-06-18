---
title: 'MySQL 常见问题'
date: '2020-01-09T06:11:50+00:00'
status: publish
permalink: /2020/01/09/mysql-%e5%b8%b8%e8%a7%81%e9%97%ae%e9%a2%98
author: 毛巳煜
excerpt: ''
type: post
id: 5220
category:
    - MySQL
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
wb_sst_seo:
    - 'a:3:{i:0;s:0:"";i:1;s:0:"";i:2;s:0:"";}'
---
###### 3. MySQL 修改root用户密码相关问题

```sql
## 选择 mysql数据库
MariaDB [mysql]> use mysql;
Database changed

## 查看所有用户信息
MariaDB [mysql]> select Host,User,Password from user;
+-----------+-------------+-------------------------------------------+
| Host      | User        | Password                                  |
+-----------+-------------+-------------------------------------------+
| localhost | mariadb.sys |                                           |
| localhost | root        | *94E121291B52E7C11BC0DD99ED636536238E078E |
| %         | root        | *94E121291B52E7C11BC0DD99ED636536238E078E |
+-----------+-------------+-------------------------------------------+
3 rows in set (0.002 sec)

MariaDB [mysql]>


```

> - 从上面结果中可以看到，**root用户** 默认有两个配置 
>   1. 使用 **localhost** 链接数据库时使用的密码
>   2. 使用 **`非`localhost** 链接数据库时使用的密码

- - - - - -

> - 所以修改普通用户，只改一个就好

```sql
SET PASSWORD FOR 'maosiyu' = PASSWORD('******');

```

- - - - - -

> - 修改root用户，改两个

```sql
SET PASSWORD FOR 'root'@'%' = PASSWORD('******');
SET PASSWORD FOR 'root'@'localhost'=PASSWORD('******');

```

- - - - - -

###### 查看最终修改后的用户信息

```sql
MariaDB [mysql]> select Host,User,Password from user;
+-----------+-------------+-------------------------------------------+
| Host      | User        | Password                                  |
+-----------+-------------+-------------------------------------------+
| localhost | mariadb.sys |                                           |
| localhost | root        | *AF8CC607D7356D518FE99B430EF3EE5D807CB42D |
| %         | root        | *AF8CC607D7356D518FE99B430EF3EE5D807CB42D |
+-----------+-------------+-------------------------------------------+


```

- - - - - -

- - - - - -

- - - - - -

###### 2. count 和 limit 混用出现的问题

```sql
SELECT
    name
FROM
    table1
WHERE
    flag = '0'
ORDER BY id LIMIT 530000, 10000;

# 结果有数据
---

SELECT
    COUNT(1)
FROM
    table1
WHERE
    flag = '0'
ORDER BY id LIMIT 530000, 10000;

# 结果无数据
Empty set (0.30 sec)

---

SELECT
    COUNT( 1 )
FROM
    ( SELECT name FROM table1 WHERE flag = '0' ORDER BY paas_id LIMIT 530000, 10000 ) temp;

+------------+
| COUNT( 1 ) |
+------------+
|      10000 |
+------------+
1 row in set (2.43 sec)


```

- - - - - -

- - - - - -

- - - - - -

###### 1. LENGTH 与 CHAR\_LENGTH 函数区别

**`LENGTH`**：按照字节数计算  
**`CHAR_LENGTH`**：按照字符数计算  
**VARCHAR(`2`)**：2表示的是两个字符

```sql
SELECT LENGTH('中华人民共和国');          -- 21 字节
SELECT CHAR_LENGTH('中华人民共和国');     -- 7  字符

SELECT LENGTH(123);                      -- 3 字节
SELECT LENGTH('中国');                   -- 6 字节
SELECT LENGTH('123');                    -- 3 字节
SELECT LENGTH('ABC');                    -- 3 字节
SELECT LENGTH('A,B,C');                  -- 5 字节

```

- - - - - -

- - - - - -

- - - - - -

###### [MariaDB对比MySQL 的兼容性和差异](https://mariadb.com/kb/en/compatibility-differences/ "MariaDB对比MySQL 的兼容性和差异")

- - - - - -

- - - - - -

- - - - - -

###### **MySQL 性能优化 `之` `thread_created` 数值过大**

1. 查看数据库状态如下

```sql
mysql> show status like 'thread%';

+-------------------+-------+
| Variable_name     | Value |
+-------------------+-------+
| Threads_cached    | 5     |
| Threads_connected | 7     |
| Threads_created   | 54018 |      -- 发现创建了好多线程，这肯定不正常
| Threads_running   | 3     |
+-------------------+-------+
4 rows in set (0.00 sec)


```

2. 查询服务器 `thread_cache_size` 配置

```sql
mysql> show variables like 'thread_cache_size';

+-------------------+-------+
| Variable_name     | Value |
+-------------------+-------+
| thread_cache_size | 9     |
+-------------------+-------+
1 row in set (0.05 sec)


```

> - **threads\_created**
>   - **threads\_created** 表示创建过的线程数，很明显， **threads\_created** 过大，表明mysql服务器 **一直在创建线程** ，这也是比较耗资源，说明数据库服务器 **不健康** 。
> - **thread\_cache\_size**
>   - 当客户端断开之后，服务器处理此客户的线程将会缓存起来以响应下一个客户而不是销毁，前提是缓存数未达上限，如果缓存数已经达到上限，那么就会创建新的线程。

- - - - - -

> - **解决方法**
>   - 适当增加配置文件中 **thread\_cache\_size** 值，在 **my.cnf** 文件中直接加上 **thread\_cache\_size = 64** (如果添加到64还会有问题，可适当在增加数值`128=64*2`)，需要重启**Mysql**服务。

- - - - - -

- - - - - -

- - - - - -

###### **MySQL 性能优化 `之` `修改配置文件`**

**my.cnf**

```ini
# 即设置mysql连接睡眠时间为100秒，任何sleep连接睡眠时间若超过100秒，将会被mysql服务自然终止。
wait_timeout             = 100
interactive_timeout      = 100

# 修改mysql占用内存的参数如下
# table_open_cache       = 2000 改为
table_open_cache         = 256

# table_definition_cache=1400 改为
table_definition_cache   = 400

# 只缓存很小的结果集，因此我们可以在查询缓存中容纳更多的结果集。
query_cache_limit        = 128K
query_cache_size         = 64M


```

- - - - - -

- - - - - -

- - - - - -

##### MySQL 拒绝服务漏洞

###### 修复方案

> 官方已发布新版本，建议升级到最新版本。  
>  目前8.0最新版本为8.0.33。https://dev.mysql.com/downloads/mysql/  
>  目前5.7最新版本为5.7.42。 https://dev.mysql.com/downloads/mysql/5.7.html

###### 缓解方案

> MySQL Server若是开启了远程连接，不要设置可连接的ip为`'%'`。

```sql
-- 查看所有用户的权限
-- 留意是否存在可连接的ip为'%'
SELECT user, host, Grant_priv, Super_priv FROM mysql.user;

```

> 设置MySQL Server远程连接的白名单ip:

```sql
-- 赋予某个ip下某个用户 所有权限
-- *.* 代表全部库名.全部表名
grant all privileges on *.* to 'USERNAME'@'IP' identified by 'PASSWORD' with grant option;

-- 赋予某个ip下某个用户 部分权限
grant select,create,drop,update,alter on *.* to 'USERNAME'@'IP' identified by 'PASSWORD' with grant option;

-- 刷新权限
flush privileges;

```

> 如果赋值白名单后，不是白名单的ip连接会提示

```sql
Host 'xx.xx.xx.xx' is not allowed to connect to this MySQL server

```

> 删除mysql.user表中的记录（操作请谨慎）

```sql
DELETE FROM mysql.user WHERE User='root' AND Host='%';
flush privileges;

```