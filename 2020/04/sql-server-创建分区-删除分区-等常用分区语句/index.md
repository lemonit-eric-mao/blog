---
title: "SQL Server 创建分区/删除分区/等常用分区语句"
date: "2020-04-13"
categories: 
  - "sqlserver"
---

在 SQL Server 2019 (15.x) 中，一张表或一个索引最多可以有 15,000 个分区

## 创建已分区表

1、在 “对象资源管理器” 中，连接到 数据库引擎的实例。 2、在标准菜单栏上，单击 “新建查询” 。 3、将以下示例复制并粘贴到查询窗口中，然后单击“执行” 。 该示例将创建新的文件组、分区函数和分区方案。 将创建一个新表，该表具有指定为存储位置的分区方案。

```sql
ALTER DATABASE <数据库名> ADD FILEGROUP <文件组名>

ALTER DATABASE <数据库名称> ADD FILE <数据标识> TO FILEGROUP <文件组名称>
--<数据标识> （name:文件名，fliename:物理路径文件名，size:文件初始大小kb/mb/gb/tb，filegrowth:文件自动增量kb/mb/gb/tb/%,maxsize:文件可以增加到的最大大小kb/mb/gb/tb/unlimited）

--创建分区表语法
create table <表名> (
  <列定义>
)on<分区方案名>(分区列名)
```

```sql
use [leo] 
GO  
-- 向AdventureWorks2012数据库添加四个新文件组（全局唯一）
-- ALTER DATABASE <数据库名> ADD FILEGROUP <文件组名>
ALTER DATABASE leo  
ADD FILEGROUP leo2016;  
GO  
ALTER DATABASE leo  
ADD FILEGROUP leo2017;  
GO  
ALTER DATABASE leo  
ADD FILEGROUP leo2018;  
GO  
ALTER DATABASE leo  
ADD FILEGROUP leo2019;   

-- 为每个文件组添加一个文件。 
-- ALTER DATABASE <数据库名称> ADD FILE <数据标识> TO FILEGROUP <文件组名称>
-- <数据标识> （name:文件名，fliename:物理路径文件名，size:文件初始大小kb/mb/gb/tb，filegrowth:文件自动增量kb/mb/gb/tb/%,maxsize:文件可以增加到的最大大小kb/mb/gb/tb/unlimited）
ALTER DATABASE leo   
ADD FILE   
(  
    NAME = leo1dat1,  
    FILENAME = 'E:\MSSQL\t1dat1.ndf',
    SIZE = 5MB,  
    -- MAXSIZE = 100MB,  
    FILEGROWTH = 5MB  
)  
TO FILEGROUP leo2016;
GO
ALTER DATABASE leo   
ADD FILE   
(  
    NAME = leo2dat2,  
    FILENAME = 'E:\MSSQL\t2dat2.ndf',  
    SIZE = 5MB,  
    -- MAXSIZE = 100MB,  
    FILEGROWTH = 5MB  
)  
TO FILEGROUP leo2017;  
GO  
ALTER DATABASE leo   
ADD FILE   
(  
    NAME = leo3dat3,  
    FILENAME = 'E:\MSSQL\t3dat3.ndf',  
    SIZE = 5MB,  
    -- MAXSIZE = 100MB,  
    FILEGROWTH = 5MB  
)  
TO FILEGROUP leo2018;  
GO  
ALTER DATABASE leo   
ADD FILE   
(  
    NAME = leo4dat4,  
    FILENAME = 'E:\MSSQL\t4dat4.ndf',  
    SIZE = 5MB,  
    -- MAXSIZE = 100MB,  
    FILEGROWTH = 5MB  
)  
TO FILEGROUP leo2019;  
GO  
-- 对 datetime 列创建 RANGE RIGHT 分区函数
-- 创建一个名为myRangePF1的分区函数，该函数将把一个表划分为四个分区
-- 分区函数名称在数据库内必须唯一
CREATE PARTITION FUNCTION [leoRangePF1] (datetime)  
    AS RANGE LEFT FOR VALUES ('2017-01-01', '2018-01-01', '2019-01-01') ;  
GO  
-- 创建一个名为myRangePS1的分区方案，该方案将myRangePF1应用于上面创建的四个文件组
CREATE PARTITION SCHEME leoRangePS1  
    AS PARTITION leoRangePF1  
    TO (leo2016, leo2017, leo2018, leo2019) ;  
GO  

-- 创建一个名为PartitionTable的分区表，它使用myRangePS1对col1进行分区 
-- Creates a partitioned table called PartitionTable that uses myRangePS1 to partition col1  
-- CREATE TABLE PartitionTable (col1 int PRIMARY KEY, col2 char(10))  
-- ON myRangePS1 (col1) ;  
GO  
```

建分区表语句案例：

```sql
use [leo]
GO

-- 以下查询所需时间为00:47:52分钟4905.3000
go
CREATE TABLE [dbo].[DFG_dc_flowdata_deliver_inventory_partition] (
  ……
  [paas_is_del] varchar(32) COLLATE Chinese_PRC_CI_AS  NULL,
  [paas_create_user] varchar(32) COLLATE Chinese_PRC_CI_AS  NULL,
  [paas_create_time] datetime  NULL,
  [paas_update_user] varchar(32) COLLATE Chinese_PRC_CI_AS  NULL,
  [paas_update_time] datetime  not NULL,
  [paas_version_no] varchar(32) COLLATE Chinese_PRC_CI_AS  NULL,
  [business_type] varchar(32) COLLATE Chinese_PRC_CI_AS  NULL,
  [distributor_used_name] varchar(500) COLLATE Chinese_PRC_CI_AS  NULL,
  [mdm_id] uniqueidentifier DEFAULT (newsequentialid()) NOT NULL,
  CONSTRAINT [pk_DFG_dc_flowdata_deliver_inventory_partition_mdm_id_paas_update_time] PRIMARY KEY CLUSTERED (mdm_id,paas_update_time)
WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) 
)  
ON leoRangePS1 (paas_update_time);
GO

CREATE NONCLUSTERED INDEX [index_DFG_dc_flowdata_deliver_inventory_partition_paas_update_time]
ON [dbo].[DFG_dc_flowdata_deliver_inventory_partition] (
  [paas_update_time] ASC
)
GO

EXEC sp_addextendedproperty
'MS_Description', N'客户编码',
'SCHEMA', N'dbo',
'TABLE', N'DFG_dc_flowdata_deliver_inventory_partition',
'COLUMN', N'distributor_code'
GO

………
```

## 参考命令：

**注：建立唯一索引（聚集或者非聚集）时，分区列必须出现在索引列中。** `解释：right，left用法`

```sql
--对 datetime 列创建 RANGE RIGHT 分区函数
CREATE PARTITION FUNCTION [myRangePF1] (datetime)  
    AS RANGE RIGHT FOR VALUES ('2016-01-01', '2017-01-01', '2018-01-01') ; 

Right 表示该分区包含右边界值，上面分区函数会把数据分为

小于2016.1.1
大于等于2016.1.1 且小于2017.1.1
大于等于2017.1.1 且小于2018.1.1
大于等于2018.1.1

四个分区，若把right换为left，则分区变为

小于等于2016.1.1
大于2016.1.1 且小于等于2017.1.1
大于2017.1.1 且小于等于2018.1.1
大于2018.1.1
```

`解释：创建分区表：`

```sql
--创建分区表
create table BigOrder (
   OrderId              int                  identity,
   orderNum             varchar(30)          not null,
   OrderStatus          int                  not null default 0,
   OrderPayStatus       int                  not null default 0,
   UserId               varchar(40)          not null,
   CreateDate           datetime             null default getdate(),
   Mark                 nvarchar(300)        null
)on bgPartitionSchema(OrderId)
```

**1、确定表是否分区**

```sql
-- 如果表 PartitionTable 已分区，以下查询将返回一个或多个行。 如果表未分区，则不返回任何行。
SELECT *   
FROM sys.tables AS t   
JOIN sys.indexes AS i   
    ON t.[object_id] = i.[object_id]   
    AND i.[type] IN (0,1)   
JOIN sys.partition_schemes ps   
    ON i.data_space_id = ps.data_space_id   
WHERE t.name = 'PartitionTable';   
GO
```

例：查询结果：表示已经分区了

```sql
DFG_dc_flowdata_deliver_sale_partition  725577623   NULL    1   0   U   USER_TABLE  2020-04-07 17:17:04.640 2020-04-07 17:17:04.640 0   0   0   0   NULL    1   0   1   0   0   0   0   0   0   0   0   0   TABLE   0   0   0   SCHEMA_AND_DATA 0   NON_TEMPORAL_TABLE  NULL    0   0   725577623   NULL    0   0   HEAP    0   65601   0   0   0   0   0   0   0   1   1   0   NULL    NULL    myRangePS1  65601   PS  PARTITION_SCHEME    0   0   65539
```

**2、确定已分区表的边界值**

```sql
-- 以下查询对于 DFG_dc_flowdata_deliver_sale_partition 表中的每个分区返回边界值。
SELECT t.name AS TableName, i.name AS IndexName, p.partition_number, p.partition_id, i.data_space_id, f.function_id, f.type_desc, r.boundary_id, r.value AS BoundaryValue   
FROM sys.tables AS t  
JOIN sys.indexes AS i  
    ON t.object_id = i.object_id  
JOIN sys.partitions AS p  
    ON i.object_id = p.object_id AND i.index_id = p.index_id   
JOIN  sys.partition_schemes AS s   
    ON i.data_space_id = s.data_space_id  
JOIN sys.partition_functions AS f   
    ON s.function_id = f.function_id  
LEFT JOIN sys.partition_range_values AS r   
    ON f.function_id = r.function_id and r.boundary_id = p.partition_number  
WHERE t.name = 'DFG_dc_flowdata_deliver_sale_partition' AND i.type <= 1  
ORDER BY p.partition_number;
```

**3、确定已分区表的分区列**

```sql
-- 以下查询返回表的分区列的名称。 DFG_dc_flowdata_deliver_sale_partition 列中的一个值匹配。
SELECT   
    t.[object_id] AS ObjectID   
    , t.name AS TableName   
    , ic.column_id AS PartitioningColumnID   
    , c.name AS PartitioningColumnName   
FROM sys.tables AS t   
JOIN sys.indexes AS i   
    ON t.[object_id] = i.[object_id]   
    AND i.[type] <= 1 -- clustered index or a heap   
JOIN sys.partition_schemes AS ps   
    ON ps.data_space_id = i.data_space_id   
JOIN sys.index_columns AS ic   
    ON ic.[object_id] = i.[object_id]   
    AND ic.index_id = i.index_id   
    AND ic.partition_ordinal >= 1 -- because 0 = non-partitioning column   
JOIN sys.columns AS c   
    ON t.[object_id] = c.[object_id]   
    AND ic.column_id = c.column_id   
WHERE t.name = 'DFG_dc_flowdata_deliver_sale_partition' ;   
GO
```

4、查看指定分区中的数据记录

```sql
----查询分区依据列为10000014的数据在哪个分区上
select $partition.myRangePF1('2015-04-04 ')

---查看指定分区中的数据记录
select * from dbo.DFG_dc_flowdata_deliver_inventory where $partition.myRangePF1(paas_update_time)=4

```

## 删除分区相关配置：

按照顺序执行

```sql
USE [master]
--删除分区方案语法
drop partition scheme <分区方案名称>
--删除分区语法
drop partition function <分区函数名>

-- 文件的删除：首先要先清空文件里的数据，删除之前数据一定要记得先备份，可将数据复制到其他表，然后执行：
DBCC SHRINKFILE (File.Name, EMPTYFILE);
例：DBCC SHRINKFILE (test4dat4, EMPTYFILE);

--文件中的内容删除后，再执行删除文件命令，DataBaseName表示数据名，File.Name 表示文件名：
ALTER DATABASE [DataBaseName] REMOVE FILE File.Name;
例：ALTER DATABASE [DataBaseName] REMOVE FILE test4dat4

-- 删除相应的表
DROP TABLE <表名>

-- 文件组的删除：需要删除所有有关使用到文件组的文件，例如分区方案、分区语法、文件、表
ALTER DATABASE [DataBaseName] REMOVE FILEGROUP [FGName]

```

[参考教材](https://docs.microsoft.com/zh-cn/sql/relational-databases/partitions/create-partitioned-tables-and-indexes?view=sql-server-ver15#SSMSProcedure)
