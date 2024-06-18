---
title: 'Influxdb 常用功能'
date: '2020-09-23T08:53:09+00:00'
status: publish
permalink: /2020/09/23/influxdb-%e5%b8%b8%e7%94%a8%e5%8a%9f%e8%83%bd
author: 毛巳煜
excerpt: ''
type: post
id: 6268
category:
    - Influxdb
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
###### 备份指定库

**首先进入到influxdb这台主机**  
**influxd backup -portable -db `数据库名` `保存到哪个路径下`**

```ruby
[root@CentOS-7 ~]# influxd backup -portable -db graf_vcenter ./grafana-backup
2020/09/23 16:55:18 backing up metastore to grafana-backup/meta.00
2020/09/23 16:55:18 backing up db=graf_vcenter
2020/09/23 16:55:18 backing up db=graf_vcenter rp=autogen shard=274 to grafana-backup/graf_vcenter.autogen.00274.00 since 0001-01-01T00:00:00Z
2020/09/23 16:55:31 backing up db=graf_vcenter rp=autogen shard=282 to grafana-backup/graf_vcenter.autogen.00282.00 since 0001-01-01T00:00:00Z
2020/09/23 16:55:36 backup complete:
2020/09/23 16:55:36     grafana-backup/20200923T085518Z.meta
2020/09/23 16:55:36     grafana-backup/20200923T085518Z.s274.tar.gz
2020/09/23 16:55:36     grafana-backup/20200923T085518Z.s282.tar.gz
2020/09/23 16:55:36     grafana-backup/20200923T085518Z.manifest
[root@CentOS-7 ~]#

```

- - - - - -

###### 恢复到另一个新数据库

```ruby
[root@mao-controllor ~]# influxd restore -portable ./grafana-backup/
2020/09/23 21:16:55 Restoring shard 274 live from backup 20200923T085518Z.s274.tar.gz
2020/09/23 21:17:28 Restoring shard 282 live from backup 20200923T085518Z.s282.tar.gz

# 查看新导入的数据库
[root@mao-controllor ~]# influx
Connected to http://localhost:8086 version 1.8.2
InfluxDB shell version: 1.8.2
>
> show databases
name: databases
name
----
_internal
graf_vcenter
>


```

- - - - - -

- - - - - -

- - - - - -

- - - - - -

- - - - - -

- - - - - -

##### InfluxDB 设置数据保留策略

**`注意`**

- InfluxDB QL 语法中`不能使用单引号`做为字符串标识， **`必须使用双引号`** 才可以
- 添加或修改完数据保留策略以后，执行 **`exit` 退出** influxdb 才会生效

- - - - - -

- - - - - -

- - - - - -

##### 常用命令

###### 新建一个保留策略

```sql
# 新建一个策略
CREATE RETENTION POLICY "策略名称" ON 数据库名 DURATION 时长 REPLICATION 副本个数;

# 新建一个策略并且直接设置为默认策略
CREATE RETENTION POLICY "策略名称" ON 数据库名 DURATION 时长 REPLICATION 副本个数 DEFAULT;

```

- - - - - -

###### 修改数据保留策略

```sql
ALTER RETENTION POLICY "策略名称" ON "数据库名" DURATION 时长

ALTER RETENTION POLICY "策略名称" ON "数据库名" DURATION 时长 DEFAULT

```

- - - - - -

###### 删除数据保留策略

```sql
DROP RETENTION POLICY "策略名" ON "数据库名"

```

- - - - - -

- - - - - -

- - - - - -

###### 查询数据保留策略

```sql
> show retention policies on graf_vcenter
name    duration shardGroupDuration replicaN default
----    -------- ------------------ -------- -------
autogen 0s       168h0m0s           1        true
>

```

- **name** 策略名称：默认autogen
- **duration** 持续时间： 0s 代表无限制
- **shardGroupDuration** 数据存储时间：shardGroup是InfluxDB的一个基本存储结构, 应该大于这个时间的数据在查询效率上应该有所降低。
- **replicaN** 副本个数：1 代表只有一个副本
- **default** 是否默认策略：true 代表设置为该数据库的默认策略

- - - - - -

```sql
# 修改数据默认保留策略
> ALTER RETENTION POLICY "autogen" ON "graf_vcenter" DURATION 168h DEFAULT

# 查看策略的变化
> show retention policies on graf_vcenter
name       duration shardGroupDuration replicaN default
----       -------- ------------------ -------- -------
autogen    168h0m0s 168h0m0s           1        true
>

```

- - - - - -

- - - - - -

- - - - - -

###### 查看修改策略后的数据量

```ruby
# 默认策略的数据量
[root@CentOS-7 ~]# du -sh /var/lib/influxdb/data/
30G     /var/lib/influxdb/data/

# 策略修改后的数据量
[root@CentOS-7 ~]# du -sh /var/lib/influxdb/data/
18G     /var/lib/influxdb/data/


```

- - - - - -

- - - - - -

- - - - - -