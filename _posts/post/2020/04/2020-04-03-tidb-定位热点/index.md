---
title: "TiDB 定位热点"
date: "2020-04-03"
categories: 
  - "tidb"
---

##### 定位热点表

**[官方资料-热点问题处理思路](https://book.tidb.io/session4/chapter7/hotspot-resolved.html?q= "官方资料-热点问题处理思路")**

```sql
SELECT
    `DB_NAME` AS '热点数据库',
    `TABLE_NAME` AS '热点表_名称',
    `TABLE_ID` AS '热点表_ID',
    `INDEX_NAME` AS '热点表索引_名称',
    `INDEX_ID` AS '热点表索引_ID',
    `REGION_ID`,
    `TYPE` AS '读热点/写热点',
    `MAX_HOT_DEGREE`,
    `REGION_COUNT`,
    `FLOW_BYTES`
FROM
    INFORMATION_SCHEMA.TIDB_HOT_REGIONS
-- WHERE
-- TABLE_NAME != ''
-- AND TABLE_NAME = 'dc_organization_master';
```

* * *

* * *

* * *

##### 查看热点表的`REGION`分部， 定位具体是哪个`REGION`产生的热点

`SHOW TABLE 数据库名.表名 REGIONS;`

```sql
SHOW TABLE prd2_pfizer.dc_organization_master REGIONS;

+-----------+------------------------+------------------------+-----------+-----------------+---------------------+------------+---------------+------------+----------------------+------------------+
| REGION_ID | START_KEY              | END_KEY                | LEADER_ID | LEADER_STORE_ID | PEERS               | SCATTERING | WRITTEN_BYTES | READ_BYTES | APPROXIMATE_SIZE(MB) | APPROXIMATE_KEYS |
+-----------+------------------------+------------------------+-----------+-----------------+---------------------+------------+---------------+------------+----------------------+------------------+
| 26001     | t_4258_i_6_013......   | t_4258_r_48145         | 26002     | 1               | 26002, 26003, 26004 | 0          | 0             | 3304344003 | 96                   | 819944           |
| 25113     | t_4258_r_48145         | t_4258_r_161205        | 25116     | 5               | 25114, 25115, 25116 | 0          | 0             | 1736211    | 49                   | 98943            |
| 25133     | t_4258_r_161205        | t_4258_r_377643        | 25134     | 1               | 25134, 25135, 25136 | 0          | 0             | 1680717    | 91                   | 226228           |
| 25121     | t_4258_r_377643        | t_4258_r_2153423       | 25123     | 4               | 25122, 25123, 25124 | 0          | 0             | 1301039    | 87                   | 204800           |
| 25141     | t_4258_r_2153423       | t_4258_r_2371340       | 25143     | 4               | 25142, 25143, 25144 | 0          | 0             | 1267105    | 96                   | 230966           |
| 26017     | t_4258_r_2371340       | t_4263_5f7......       | 26018     | 1               | 26018, 26019, 26020 | 0          | 0             | 124000105  | 136                  | 669477           |
| 25137     | t_4258_                | t_4258_i_2_013......   | 25140     | 5               | 25138, 25139, 25140 | 0          | 0             | 0          | 105                  | 1007100          |
| 25125     | t_4258_i_2_013......   | t_4258_i_2_014......   | 25126     | 1               | 25126, 25127, 25128 | 0          | 0             | 0          | 73                   | 688866           |
| 25117     | t_4258_i_2_014......   | t_4258_i_3_014......   | 25118     | 1               | 25118, 25119, 25120 | 0          | 0             | 0          | 104                  | 785285           |
| 25129     | t_4258_i_3_014......   | t_4258_i_4_01e......   | 25131     | 4               | 25130, 25131, 25132 | 0          | 0             | 0          | 139                  | 1111149          |
| 25145     | t_4258_i_4_01e......   | t_4258_i_5_013......   | 25147     | 4               | 25146, 25147, 25148 | 0          | 37            | 0          | 92                   | 848465           |
| 25109     | t_4258_i_5_013......   | t_4258_i_6_013......   | 25111     | 4               | 25110, 25111, 25112 | 0          | 0             | 808085616  | 57                   | 555004           |
+-----------+------------------------+------------------------+-----------+-----------------+---------------------+------------+---------------+------------+----------------------+------------------+

```

**`READ_BYTES`**: 估算的 Region 在 1 个心跳周期内的读数据量大小，单位是 byte。由此可见，**`数值特别大的就是发生热点的 REGION`**

* * *

* * *

* * *

##### 通过 URL查看 REGION 的信息

`curl http://{TiDBIP}:10080/regions/{REGION_ID}`

```ruby
[root@test1 ~]# curl http://192.168.192.31:10080/regions/26001
{
 "region_id": 26001,
 "start_key": "dIAAAAAAABCiX2mAAAAAAAAABgEwAAAAAAAAAPgBRFMwMjA4MTj/MQAAAAAAAAD4ATMAAAAAAAAA+AOAAAAAAAA3hw==",
 "end_key": "dIAAAAAAABCiX3KAAAAAAAC8EQ==",
 "frames": [
  {
   "db_name": "prd2_pfizer",
   "table_name": "dc_organization_master",
   "table_id": 4258,
   "is_record": false,
   "index_name": "index_1",
   "index_id": 6,
   "index_values": [
    "0",
    "DS0208181",
    "3",
    "14215"
   ]
  },
  {
   "db_name": "prd2_pfizer",
   "table_name": "dc_organization_master",
   "table_id": 4258,
   "is_record": true,
   "record_id": 48145
  }
 ]
}

[root@test1 ~]#
```

* * *

* * *

* * *

##### 打散**`写`**热点

**[官方资料-打散日志](https://pingcap.com/docs-cn/stable/reference/sql/statements/split-region/#split-region-%E4%BD%BF%E7%94%A8%E6%96%87%E6%A1%A3 "官方资料-打散日志")**

**[AskTug 帖子](https://asktug.com/t/topic/33380 "AskTug 帖子")**

* * *

* * *

##### 拆分**`读`**热点

**[官网地址](https://pingcap.com/docs-cn/stable/reference/tools/pd-control/#operator-show--add--remove "官网地址")**

- `operator add split-region 26001 --policy=approximate` 将 Region\_ID为26001的 Region 对半拆分成两个 Region，基于**`粗略`估计值**, 消耗更少的 I/O，可以更快地完成。
    
- `operator add split-region 26001 --policy=scan` 将 Region\_ID为26001的 Region 对半拆分成两个 Region，基于**`精确`扫描值**
    

```ruby
[tidb@back-paas bin]$ pwd
/home/tidb/tidb-ansible/resources/bin
[tidb@back-paas bin]$
[tidb@back-paas bin]$ ./pd-ctl -u http://192.168.192.31:2379 operator add split-region 26001 --policy=approximate
Success!
[tidb@back-paas bin]$
```

##### 在次查看 REGION，会发现数量变小了

```sql
SHOW TABLE prd2_pfizer.dc_organization_master REGIONS WHERE REGION_ID = 26001;

+-----------+------------------------+------------------------+-----------+-----------------+---------------------+------------+---------------+------------+----------------------+------------------+
| REGION_ID | START_KEY              | END_KEY                | LEADER_ID | LEADER_STORE_ID | PEERS               | SCATTERING | WRITTEN_BYTES | READ_BYTES | APPROXIMATE_SIZE(MB) | APPROXIMATE_KEYS |
+-----------+------------------------+------------------------+-----------+-----------------+---------------------+------------+---------------+------------+----------------------+------------------+
| 26001     | t_4258_i_6_013......   | t_4258_r_48145         | 26002     | 1               | 26002, 26003, 26004 | 0          | 0             | 1304344003 | 96                   | 436077           |
+-----------+------------------------+------------------------+-----------+-----------------+---------------------+------------+---------------+------------+----------------------+------------------+

```

* * *

* * *

* * *
