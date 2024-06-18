---
title: 'Oracle 数据库使用手册'
date: '2022-07-06T07:25:38+00:00'
status: private
permalink: /2022/07/06/oracle-%e6%95%b0%e6%8d%ae%e5%ba%93%e4%bd%bf%e7%94%a8%e6%89%8b%e5%86%8c
author: 毛巳煜
excerpt: ''
type: post
id: 8891
category:
    - Oracle
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
wb_sst_seo:
    - 'a:3:{i:0;s:0:"";i:1;s:0:"";i:2;s:0:"";}'
---
##### **[常见问题](http://www.dev-share.top/2022/07/07/oracle-%e6%95%b0%e6%8d%ae%e5%ba%93%e4%bd%bf%e7%94%a8-%e5%b8%b8%e8%a7%81%e9%97%ae%e9%a2%98/ "常见问题")**

- - - - - -

- - - - - -

- - - - - -

##### 3种登录Oralce的方法

> - 方式一 `sqlplus / as sysdba`

```ruby
[oracle@oracle12c ~]$ sqlplus / as sysdba

SQL*Plus: Release 12.2.0.1.0 Production on 星期三 7月 6 15:16:30 2022

Copyright (c) 1982, 2016, Oracle.  All rights reserved.


连接到:
Oracle Database 12c Enterprise Edition Release 12.2.0.1.0 - 64bit Production

SQL>
SQL>
SQL> show user
USER 为 "SYS"
SQL>


```

- - - - - -

> - 方式二  
>    `sqlplus username/password@ip:port/sid`  
>    简写: `sqlplus username/password@orcl`（前提：配置了 TNS）

```ruby
[oracle@oracle12c ~]$ sqlplus SYSTEM/Aa123456@orcl

SQL*Plus: Release 12.2.0.1.0 Production on 星期三 7月 6 15:18:24 2022

Copyright (c) 1982, 2016, Oracle.  All rights reserved.

上次成功登录时间: 星期三 7月  06 2022 15:04:22 +08:00

连接到:
Oracle Database 12c Enterprise Edition Release 12.2.0.1.0 - 64bit Production

SQL>
SQL>
SQL> show user
USER 为 "SYSTEM"
SQL>


```

- - - - - -

> - 方式三
> - `sqlplus /nolog`
> - `conn username/password@ip:port/sid`

```ruby
[oracle@oracle12c ~]$ sqlplus /nolog

SQL*Plus: Release 12.2.0.1.0 Production on 星期三 7月 6 15:19:11 2022

Copyright (c) 1982, 2016, Oracle.  All rights reserved.

SQL>
SQL> conn SYSTEM/Aa123456@orcl
已连接。
SQL>
SQL> show user
USER 为 "SYSTEM"
SQL>


```

- - - - - -

- - - - - -

- - - - - -

#### **开启日志归档(相当于MySQL的binlog)**

###### 执行以下命令，检查日志归档是否已开启

```ruby
## 以数据库管理身份登录
[oracle@oracle12c ~]$ sqlplus / as sysdba

```

```sql
SQL> archive log list
数据库日志模式             非存档模式
自动存档                   禁用
存档终点                   USE_DB_RECOVERY_FILE_DEST
最早的联机日志序列         50
当前日志序列               52
SQL>


```

> - 配置归档日志参数

```sql
ALTER system SET db_recovery_file_dest_size = 100G;
ALTER system SET db_recovery_file_dest = '/opt/oracle/oradata/recovery_area' scope=spfile;

```

> - **100G**为日志文件存储空间的大小，请根据实际情况设置。
> - `/opt/oracle/oradata/recovery_area` 为日志存储路径  
>    请根据实际规划设置，但须确保路径提前创建，并赋予读写权限 `chmod 777 /opt/oracle/oradata/recovery_area`
> - 开启日志归档功能**需要重启数据库**，重启期间将导致业务中断，请谨慎操作。
> - 归档日志会占用较多的磁盘空间，若**磁盘空间满了会影响业务**，请定期清理过期归档日志。

- - - - - -

###### 创建表空间

```sql
CREATE TABLESPACE logminer_tbs DATAFILE '/opt/oracle/oradata/SID/logminer_tbs.dbf' SIZE 25M REUSE AUTOEXTEND ON MAXSIZE UNLIMITED;

```

> - 注意：**/opt/oracle/oradata/`SID`** 路径需使用**root用户**提前创建，并赋予读写权限：**chmod 777 /opt/oracle/oradata/`SID`**。

- - - - - -

###### 执行以下命令开启日志归档

```sql
shutdown immediate;
startup mount;
alter database archivelog;
-- 此处为开启归档模式 需要要开非归档模式的话 语句修改为 alter database noarchivelog;
alter database open;

```

**实际操作**

```sql
SQL> shutdown immediate;
Database closed.
Database dismounted.
ORACLE instance shut down.

------

SQL> startup mount;
ORACLE instance started.

Total System Global Area 2466250752 bytes
Fixed Size                  8795760 bytes
Variable Size             671091088 bytes
Database Buffers         1778384896 bytes
Redo Buffers                7979008 bytes
Database mounted.

------

SQL> alter database archivelog;

Database altered.

------

SQL> alter database open;

Database altered.


```

**查看是否已经成功开启**

```sql
SQL> archive log list
数据库日志模式            存档模式
自动存档                 启用
存档终点                 USE_DB_RECOVERY_FILE_DEST
最早的联机日志序列        50
下一个存档日志序列        52
当前日志序列              52
SQL>


```

**必须为捕获的表或数据库启用补充日志记录，以便数据更改捕获已更改数据库行的之前状态。[官方链接](https://ververica.github.io/flink-cdc-connectors/master/content/connectors/oracle-cdc.html "官方链接")**

```sql
SQL>

-- 为捕获的数据库启用补充日志记录
ALTER DATABASE ADD SUPPLEMENTAL LOG DATA;

-- 为捕获的表启用补充日志记录
-- ALTER TABLE schema名.表名 ADD SUPPLEMENTAL LOG DATA (ALL) COLUMNS;
ALTER TABLE FLINKUSER.USER_1 ADD SUPPLEMENTAL LOG DATA (ALL) COLUMNS;

```

- - - - - -

- - - - - -

- - - - - -

### 创建 pdb数据库

> - 创建PDB：`CREATE PLUGGABLE DATABASE PDB名 ADMIN USER PDB管理员用户名 IDENTIFIED BY ORACLE FILE_NAME_CONVERT=('这个路径是你的Oracle数据库中的真实目录', '这个路径是你想把pdb数据库放在哪个目录下');`
> - 删除PDB：`DROP PLUGGABLE DATABASE PDB名 including datafiles;`
> - 打开所有PDB：`ALTER PLUGGABLE DATABASE ALL OPEN;`
> - 关闭所有PDB：`ALTER PLUGGABLE DATABASE ALL CLOSE;`
> - 打开指定PDB：`ALTER PLUGGABLE DATABASE PDB名 OPEN;`
> - 关闭指定PDB：`ALTER PLUGGABLE DATABASE PDB名 CLOSE;`

```shell
[oracle@oracle12c ~]$ sqlplus / as sysdba

```

```sql
SQL> CREATE PLUGGABLE DATABASE pdb_flink ADMIN USER pdb_flink_user IDENTIFIED BY ORACLE FILE_NAME_CONVERT=('/u01/app/oracle/oradata/orcl/pdbseed', '/u01/app/oracle/oradata/orcl/pdb_flink');


-- 查看 pdb
SQL> SHOW PDBS

    CON_ID CON_NAME                       OPEN MODE  RESTRICTED
---------- ------------------------------ ---------- ----------
         1 PDB$SEED                       READ ONLY  NO
         2 PDB_FLINK                      MOUNTED
SQL>


```

**真实目录**

- 因为真实的安装目录是在 /data/下

```shell
[oracle@oracle12c ~]$ ll /data/u01/app/oracle/oradata/orcl/
......
pdb_flink
pdbseed
......

```

- - - - - -

- - - - - -

- - - - - -