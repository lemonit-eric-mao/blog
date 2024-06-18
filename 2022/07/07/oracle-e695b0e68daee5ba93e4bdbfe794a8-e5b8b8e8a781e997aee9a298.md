---
title: 'Oracle 数据库使用-常见问题'
date: '2022-07-07T01:45:26+00:00'
status: private
permalink: /2022/07/07/oracle-%e6%95%b0%e6%8d%ae%e5%ba%93%e4%bd%bf%e7%94%a8-%e5%b8%b8%e8%a7%81%e9%97%ae%e9%a2%98
author: 毛巳煜
excerpt: ''
type: post
id: 8902
category:
    - Oracle
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
wb_sst_seo:
    - 'a:3:{i:0;s:0:"";i:1;s:0:"";i:2;s:0:"";}'
---
##### 常见问题

> - Oracle数据库中 用户和表空间的关系是什么？ 
>   - 用户和表空间没有隶属关系
>   - 一个用户可以使用一个或多个表空间
>   - 一个表空间也可以供多个用户使用
> - 表空间概念 
>   - 表空间只是和数据库文件发生关系，数据文件是物理的
>   - 一个表空间可以包含多个数据文件
>   - 而一个数据文件只能隶属一个表空间

- - - - - -

> - 如果使用 sqlplus 登录 Oracle 出现问号乱码  
>    只需要在Oracle用户下，添加如下环境变量即可

```ruby
cat > ~/.base_profile 
```

- - - - - -

> - 美化 sqlplus 输出结果

```sql
SQL> SET linesize 1024 pagesize 30 newpage 2;


```

- - - - - -

- - - - - -

- - - - - -

##### 常用语句

```sql
--1、查看表空间的名称及大小
SELECT
    t.tablespace_name,
    round( SUM( bytes / ( 1024 * 1024 ) ), 0 ) ts_size
FROM
    dba_tablespaces t,
    dba_data_files d
WHERE
    t.tablespace_name = d.tablespace_name
GROUP BY
    t.tablespace_name;


--2、查看表空间物理文件的名称及大小
SELECT
    tablespace_name,
    file_id,
    file_name,
    round( bytes / ( 1024 * 1024 ), 0 ) total_space
FROM
    dba_data_files
ORDER BY
    tablespace_name;


--3、查看回滚段名称及大小
SELECT
    segment_name,
    tablespace_name,
    r.status,
    ( initial_extent / 1024 ) initialextent,
    ( next_extent / 1024 ) nextextent,
    max_extents,
    v.curext curextent
FROM
    dba_rollback_segs r,
    v<span class="katex math inline">rollstat v
WHERE
    r.segment_id = v.usn ( + )
ORDER BY
    segment_name;


--4、查看控制文件
SELECT
    NAME
FROM
    v</span>controlfile;


--5、查看日志文件
SELECT
    MEMBER
FROM
    v<span class="katex math inline">logfile;


--6、查看表空间的使用情况
SELECT
    SUM( bytes ) / ( 1024 * 1024 ) AS free_space,
    tablespace_name
FROM
    dba_free_space
GROUP BY
    tablespace_name;
SELECT
    a.tablespace_name,
    a.bytes total,
    b.bytes used,
    c.bytes free,
    ( b.bytes * 100 ) / a.bytes "% USED ",
    ( c.bytes * 100 ) / a.bytes "% FREE "
FROM
    sys.sm</span>ts_avail a,
    sys.sm<span class="katex math inline">ts_used b,
    sys.sm</span>ts_free c
WHERE
    a.tablespace_name = b.tablespace_name
    AND a.tablespace_name = c.tablespace_name;


--7、查看数据库库对象
SELECT
    owner,
    object_type,
    status,
    COUNT( * ) count #
FROM
    all_objects
GROUP BY
    owner,
    object_type,
    status;


--8、查看数据库的版本
SELECT
    version
FROM
    product_component_version
WHERE
    substr( product, 1, 6 ) = 'Oracle';


--9、查看数据库的创建日期和归档方式
SELECT
    created,
    log_mode,
    log_mode
FROM
    v$database;
--1G=1024MB
--1M=1024KB
--1K=1024Bytes
--1M=11048576Bytes
--1G=1024*11048576Bytes=11313741824Bytes
SELECT
    a.tablespace_name "表空间名",
    total "表空间大小",
    free "表空间剩余大小",
    ( total - free ) "表空间使用大小",
    total / ( 1024 * 1024 * 1024 ) "表空间大小(G)",
    free / ( 1024 * 1024 * 1024 ) "表空间剩余大小(G)",
    ( total - free ) / ( 1024 * 1024 * 1024 ) "表空间使用大小(G)",
    round( ( total - free ) / total, 4 ) * 100 "使用率 %"
FROM
    ( SELECT tablespace_name, SUM( bytes ) free FROM dba_free_space GROUP BY tablespace_name ) a,
    ( SELECT tablespace_name, SUM( bytes ) total FROM dba_data_files GROUP BY tablespace_name ) b


```

- - - - - -

```sql
-- 1、查询数据库名
show parameter db_name;

-- 2、查询实例名
show parameter instance_name;

-- 3、查询数据库域名
show parameter domain;

-- 4、查询数据库服务器
show parameter service;
show parameter names;


```

- - - - - -

- - - - - -

- - - - - -

**ORA-04036: 实例使用的 PGA 内存超过 PGA\_AGGREGATE\_LIMIT**

> - `Caused by: java.sql.SQLException: ORA-04036: PGA memory used by the instance exceeds PGA_AGGREGATE_LIMIT`
> - 问题原因
>   
>   
>   - Oracle 12.1.0.1版本中引入了新特性：
>   - 使用**PGA\_AGGREGATE\_LIMIT**参数来限制**Oracle**实例**PGA**使用内存的上限。
>   - 后台进程**ckpt**每三秒检查一次**PGA**使用的内存总量，如果**超过限制就采取终止会话**的方式来降低**PGA**内存的使用量 
>       - 对于SYS用户进程和后台进程不包括job队列不会被终止掉。
>   - 有了这个限制，不会造成**PGA**内存疯涨，导致内存耗尽。
>   - 默认的**PGA\_AGGREGATE\_LIMIT**参数为**2G**或**200%**的**PGA\_AGGREGATE\_TARGET**值或PROCESSES参数值\*3M
> - 解决方法 ```sql
>   ## 查看 pga 现状内存大小
>   SQL> SHOW PARAMETER PGA;
>   NAME                                 TYPE        VALUE
>   ------------------------------------ ----------- ------------------------------
>   pga_aggregate_limit                  big integer 2G
>   pga_aggregate_target                 big integer 782M
>   SQL>
>   
>   ```
>   
>   
>   - **修改 pga 内存大小为 10G**
>   
>   ```sql
>   SQL> ALTER system SET PGA_AGGREGATE_LIMIT = 10G;
>   System altered.
>   
>   ```
>   
>   
>   - **再次查看 pga 内存大小**
>   
>   ```sql
>   SQL> SHOW PARAMETER PGA;
>   NAME                                 TYPE        VALUE
>   ------------------------------------ ----------- ------------------------------
>   pga_aggregate_limit                  big integer 10G
>   pga_aggregate_target                 big integer 782M
>   SQL>
>   
>   
>   ```

**java.sql.SQLException: ORA-00257**

> - Caused by: java.sql.SQLException: ORA-00257: 归档程序错误。只有在解析完成后才以 AS SYSDBA 方式连接。
> - 排查原因：
>   
>   ```sql
>   SQL> SELECT FILE_TYPE, PERCENT_SPACE_USED, NUMBER_OF_FILES FROM V$FLASH_RECOVERY_AREA_USAGE;
>   
>   FILE_TYPE               PERCENT_SPACE_USED NUMBER_OF_FILES
>   ----------------------- ------------------ ---------------
>   CONTROL FILE                             0               0
>   REDO LOG                                 0               0
>   ARCHIVED LOG                         99.75             760
>   BACKUP PIECE                           .09               5
>   IMAGE COPY                               0               0
>   FLASHBACK LOG                            0               0
>   FOREIGN ARCHIVED LOG                     0               0
>   AUXILIARY DATAFILE COPY                  0               0
>   
>   
>   ```
>   
>   
>   - **ARCHIVED LOG** 这一项的空间占用率已接近100%
>   
>   ```sql
>   -- 查看设置的空间大小
>   SQL> SHOW PARAMETER DB_RECOVER;
>   
>   NAME                                 TYPE        VALUE
>   ------------------------------------ ----------- ----------------------------------
>   db_recovery_file_dest                string      /data/oracle/oradata/recovery_area
>   db_recovery_file_dest_size           big integer 100G
>   
>   -- 如果磁盘空间够用，就将磁盘空间添加到200G
>   SQL> ALTER SYSTEM SET DB_RECOVERY_FILE_DEST_SIZE=200G SCOPE=BOTH;
>   
>   
>   ```
>   
>   
>   - 再次查看
>   
>   ```sql
>   SQL> SHOW PARAMETER DB_RECOVER;
>   
>   NAME                                 TYPE        VALUE
>   ------------------------------------ ----------- ------------------------------
>   db_recovery_file_dest                string      /data/oracle/oradata/recovery_
>                                                    area
>   db_recovery_file_dest_size           big integer 200G
>   
>   ```
>   
>   ```sql
>   SQL> SELECT FILE_TYPE, PERCENT_SPACE_USED, NUMBER_OF_FILES FROM V$FLASH_RECOVERY_AREA_USAGE;
>   
>   FILE_TYPE               PERCENT_SPACE_USED NUMBER_OF_FILES
>   ----------------------- ------------------ ---------------
>   CONTROL FILE                             0               0
>   REDO LOG                                 0               0
>   ARCHIVED LOG                         50.13             763
>   BACKUP PIECE                           .05               5
>   IMAGE COPY                               0               0
>   FLASHBACK LOG                            0               0
>   FOREIGN ARCHIVED LOG                     0               0
>   AUXILIARY DATAFILE COPY                  0               0
>   
>   
>   ```
>   
>   
>   - [相关资料](https://blog.csdn.net/weixin_45843683/article/details/114253607)

- - - - - -

- - - - - -

- - - - - -