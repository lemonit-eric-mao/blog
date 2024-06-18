---
title: "TiDB 备份/恢复数据"
date: "2019-07-18"
categories: 
  - "tidb"
---

##### TiDB 最新工具

###### **[数据导出工具 Dumpling](https://docs.pingcap.com/zh/tidb/stable/dumpling-overview#dumpling-%E4%BD%BF%E7%94%A8%E6%96%87%E6%A1%A3 "数据导出工具 Dumpling")**

```ruby
./dumpling \
  -u lemonit_apps \
  -p 'lemonit_apps' \
  -P 10042 \
  -h db.lemonit.cn \
  --filter "wordpress.*" \
  -o /tmp/output/sql/
```

* * *

##### 下载

**[官方下载地址](https://docs.pingcap.com/zh/tidb/stable/download-ecosystem-tools#dumpling "官方下载地址")**

```ruby
wget https://download.pingcap.org/tidb-toolkit-v4.0.2-linux-amd64.tar.gz
```

* * *

* * *

* * *

##### [官方教程](https://www.pingcap.com/docs-cn/v3.0/how-to/maintain/backup-and-restore/ "官方教程")

###### [七牛云阉割版](http://qiniu.dev-share.top/tidb-mydumper-and-loader.zip "七牛云阉割版")

```ruby
wget http://qiniu.dev-share.top/tidb-mydumper-and-loader.zip
```

###### [官网下载 新版](https://download.pingcap.org/tidb-enterprise-tools-nightly-linux-amd64.tar.gz "官网下载 新版")

```ruby
wget https://download.pingcap.org/tidb-enterprise-tools-nightly-linux-amd64.tar.gz
```

###### [官网latest版](http://download.pingcap.org/tidb-enterprise-tools-latest-linux-amd64.tar.gz "官网latest版")

##### 一、下载 TiDB 工具集 (Linux)

```ruby
[tidb@dev10 tidb-tools]$ pwd
/home/tidb/tidb-tools
[tidb@dev10 tidb-tools]$
# 官网latest版
[tidb@dev10 tidb-tools]$ wget http://download.pingcap.org/tidb-enterprise-tools-latest-linux-amd64.tar.gz
[tidb@dev10 tidb-tools]$
[tidb@dev10 tidb-tools]$ ll
总用量 88512
-rw-rw-r--. 1 tidb tidb 90634703 7月  18 07:55 tidb-enterprise-tools-latest-linux-amd64.tar.gz
[tidb@dev10 tidb-tools]$ tar -zxvf tidb-enterprise-tools-latest-linux-amd64.tar.gz
......
```

##### 进入工具包 备份数据

```ruby
[tidb@dev10 bin]$ pwd
/home/tidb/tidb-tools/tidb-enterprise-tools-latest-linux-amd64/bin
[tidb@dev10 bin]$ ll
总用量 218544
-rwxr-xr-x. 1 tidb tidb 19552470 7月  18 07:55 binlogctl
-rwxr-xr-x. 1 tidb tidb 58789632 7月  18 07:55 ddl_checker
-rwxr-xr-x. 1 tidb tidb 38003427 7月  18 07:55 importer
-rwxr-xr-x. 1 tidb tidb 14282889 7月  18 07:55 loader
-rwxr-xr-x. 1 tidb tidb 12772200 7月  18 07:55 mydumper
-rwxr-xr-x. 1 tidb tidb 38426024 7月  18 07:55 sync_diff_inspector
-rwxr-xr-x. 1 tidb tidb 41945470 7月  18 07:55 syncer
[tidb@dev10 bin]$
[tidb@dev10 bin]$ ./mydumper -h 172.160.180.33 -u root -p 数据库密码 -P 4000 -t 16 -F 64 -c -e --skip-tz-utc -o ./backup
```

##### mydumper 常用参数解释

```ruby
-B, --database              要备份的数据库，不指定则备份所有库
-T, --tables-list           需要备份的表，名字用逗号隔开
-o, --outputdir             备份文件输出的目录
-s, --statement-size        生成的insert语句的字节数，默认1000000
-r, --rows                  将表按行分块时，指定的块行数，指定这个选项会关闭 --chunk-filesize
-F, --chunk-filesize        将表按大小分块时，指定的块大小，单位是 MB
-c, --compress              压缩输出文件
-e, --build-empty-files     如果表数据是空，还是产生一个空文件（默认无数据则只有表结构文件）
-x, --regex                 是同正则表达式匹配 'db.table'
-i, --ignore-engines        忽略的存储引擎，用逗号分割
-m, --no-schemas            不备份表结构
-d, --no-data               不导出表数据
-G, --triggers              导出触发器
-E, --events                导出事件
-R, --routines              导出存储过程
-k, --no-locks              不使用临时共享只读锁，使用这个选项会造成数据不一致
-l, --long-query-guard      设定阻塞备份的长查询超时时间，单位是秒，默认是60秒（超时后默认mydumper将会退出）
-K, --kill-long-queries     kill掉长时间执行的查询，备份报错：Lock wait timeout exceeded; try restarting transaction

-D, --daemon                启用守护进程模式，守护进程模式以某个间隔不间断对数据库进行备份
-I, --snapshot-interval     dump快照间隔时间，默认60s，需要在daemon模式下
-L, --logfile               使用的日志文件名(mydumper所产生的日志), 默认使用标准输出
-h, --host                  连接的主机名
-u, --user                  备份所使用的用户
-p, --password              密码
-P, --port                  端口
-S, --socket                使用socket通信时的socket文件
-t, --threads               开启的备份线程数，默认是4
-C, --compress-protocol     压缩与mysql通信的数据
-V, --version               显示版本号
-v, --verbose               输出信息模式, 0 = silent, 1 = errors, 2 = warnings, 3 = info, 默认为 2
--lock-all-tables           锁全表，代替FLUSH TABLE WITH READ LOCK
--tz-utc                    备份的时候允许备份Timestamp，这样会导致不同时区的备份还原会出问题,默认禁用
--skip-tz-utc               同上
--use-savepoints            使用savepoints来减少采集metadata所造成的锁时间，需要 SUPER 权限
--success-on-1146           如果表不存在，则不增加错误计数和警告而不是关键错误
--less-locking              减少对InnoDB表的锁施加时间（这种模式的机制下文详解）
```

##### loader 常用参数解释

```ruby
  -L string
      log 级别设置，可以设置为 debug, info, warn, error, fatal (默认为 "info")
  -P int
      TiDB/MySQL 的端口 (默认为 4000)
  -V
      打印 loader 版本
  -c string
      指定配置文件启动 loader
  -checkpoint-schema string
      checkpoint 数据库名，loader 在运行过程中会不断的更新这个数据库，在中断并恢复后，会通过这个库获取上次运行的进度 (默认为 "tidb_loader")
  -d string
       需要导入的数据存放路径 (default "./")
  -h string
       TiDB 服务 host IP  (default "127.0.0.1")
  -p string
      TiDB 账户密码
  -status-addr string
      Prometheus 可以通过该地址拉取 Loader metrics, 也是 Loader 的 pprof 调试地址 (默认为 ":8272")。
  -t int
      线程数 (默认为 16). 每个线程同一时刻只能操作一个数据文件。
  -u string
      TiDB 的用户名 (默认为 "root")
```

* * *

* * *

##### 二、数据库备份与恢复

`备份数据库时如果使用了压缩文件的方式，loader时会失败`

- 测试服：
    
    - ip: 172.160.180.33
    - 用户名: root
    - 密码：数据库密码
    - 端口: 4000
    - 数据库：dev2\_dc\_test
    - 备份路径：./backup\_0
- 开发服：
    
    - ip: 172.160.180.46
    - 用户名: root
    - 密码：数据库密码
    - 端口: 4000

将测试服的数据迁移到开发服

```ruby
[tidb@dev10 bin]$ pwd
/home/tidb/tidb-tools/tidb-enterprise-tools-latest-linux-amd64/bin
# 备份测试服 数据库
[tidb@dev10 bin]$ ./mydumper -h 172.160.180.33 -u root -p 数据库密码 -P 4000 -t 16 -F 64 -B dev2_dc_test --skip-tz-utc -o ./backup_0
[tidb@dev10 bin]$
# 恢复数据到 开发服务器
[tidb@dev10 bin]$ ./loader -h 172.160.180.46 -u root -p 数据库密码 -P 4000 -t 32 -d ./backup_0/
......
2019/08/02 17:03:30 main.go:88: [info] loader stopped and exits
[tidb@dev10 bin]$
[tidb@dev10 bin]$
```

* * *

* * *

##### 三、TiDB 2.0 ~ TiDB 3.0 数据迁移遇到的`坑`

**`CURRENT_TIMESTAMP(3)` 与 `CURRENT_TIMESTAMP` 这两个语法是不能兼容的，其它的都可以兼容**

```sql
-- TiDB 3.0 创建表的脚本
CREATE TABLE `ACT_RU_EVENT_SUBSCR` (
  `ID_` varchar(64) NOT NULL,
  `REV_` int(11) DEFAULT NULL,
  `EVENT_TYPE_` varchar(255) NOT NULL,
  `EVENT_NAME_` varchar(255) DEFAULT NULL,
  `EXECUTION_ID_` varchar(64) DEFAULT NULL,
  `PROC_INST_ID_` varchar(64) DEFAULT NULL,
  `ACTIVITY_ID_` varchar(64) DEFAULT NULL,
  `CONFIGURATION_` varchar(255) DEFAULT NULL,
  `CREATED_` timestamp(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3), -- 这里有个坑
  `PROC_DEF_ID_` varchar(64) DEFAULT NULL,
  `TENANT_ID_` varchar(255) DEFAULT '',
  PRIMARY KEY (`ID_`),
  KEY `ACT_IDX_EVENT_SUBSCR_CONFIG_` (`CONFIGURATION_`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- TiDB 2.0 创建表的脚本
CREATE TABLE `ACT_RU_EVENT_SUBSCR` (
  `ID_` varchar(64) CHARSET utf8 COLLATE utf8_bin NOT NULL,
  `REV_` int(11) DEFAULT NULL,
  `EVENT_TYPE_` varchar(255) CHARSET utf8 COLLATE utf8_bin NOT NULL,
  `EVENT_NAME_` varchar(255) CHARSET utf8 COLLATE utf8_bin DEFAULT NULL,
  `EXECUTION_ID_` varchar(64) CHARSET utf8 COLLATE utf8_bin DEFAULT NULL,
  `PROC_INST_ID_` varchar(64) CHARSET utf8 COLLATE utf8_bin DEFAULT NULL,
  `ACTIVITY_ID_` varchar(64) CHARSET utf8 COLLATE utf8_bin DEFAULT NULL,
  `CONFIGURATION_` varchar(255) CHARSET utf8 COLLATE utf8_bin DEFAULT NULL,
  `CREATED_` timestamp(3) NOT NULL DEFAULT CURRENT_TIMESTAMP, -- 这里有个坑
  `PROC_DEF_ID_` varchar(64) CHARSET utf8 COLLATE utf8_bin DEFAULT NULL,
  `TENANT_ID_` varchar(255) CHARSET utf8 COLLATE utf8_bin DEFAULT '',
  PRIMARY KEY (`ID_`),
  KEY `ACT_IDX_EVENT_SUBSCR_CONFIG_` (`CONFIGURATION_`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
```

* * *

* * *

#### 四、TiDB 3.0 与 MySQL 5.7数据交互 备份/恢复

- 开发服务器 TiDB 3.0：
    
    - ip: 172.160.180.46
    - 用户名: root
    - 密码：数据库密码
    - 端口: 4000
    - 数据库：dev2\_dc\_test
    - 备份路径：./backup\_0
- MySQL 5.7：
    
    - ip: 172.160.180.6
    - 用户名: root
    - 密码：数据库密码
    - 端口: 3306

##### MySQL数据库 全量备份 && 迁移到 TiDB开发服务器

```ruby
[tidb@test1 bin]$ pwd
/home/tidb/tidb-tools/tidb-enterprise-tools-latest-linux-amd64/bin
[tidb@test1 bin]$
# 备份 MySQL数据库
[tidb@test1 bin]$ ./mydumper -h 172.160.180.6 -u root -p 数据库密码 -P 3306 -t 16 -F 64 -B paas --skip-tz-utc -o ./backup_mysql_0
[tidb@test1 bin]$
# 恢复到TiDB
[tidb@test1 bin]$ ./loader -h 172.160.180.46 -u root -p 数据库密码 -P 4000 -t 32 -d ./backup_mysql_0/
......
2019/08/02 17:33:30 main.go:88: [info] loader stopped and exits
[tidb@test1 bin]$
```

##### TiDB开发服务器 全量备份 && 迁移到 MySQL数据库

```ruby
[tidb@test1 bin]$ ./mydumper -h 172.160.180.46 -u root -p 数据库密码 -P 4000 -t 16 -F 64 -B dev2_dc_test --skip-tz-utc -o ./backup_0/
[tidb@test1 bin]$
[tidb@test1 bin]$ ./loader -h 172.160.180.6 -u root -p 数据库密码 -P 3306 -t 32 -d ./backup_0/
[tidb@test1 bin]$
```

* * *

* * *

#### `问`、迁移到 MySQL数据库遇到的`坑`

##### 问题1 索引过长

```ruby
2019/08/05 11:20:59 main.go:84: [fatal] Error 1071: Specified key was too long; max key length is 3072 bytes
# 原因：创建表设置索引时 索引的总和超长
CREATE TABLE `dc_product_mapping_todo` (
  `dealer_code` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '标准经销商编码',
  `source_product_name` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '原始流向产品名称',
  `source_product_spec` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '原始流向产品规格',
  `mapping_relation_id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '映射关系ID',
  `paas_id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  PRIMARY KEY (`paas_id`),
  KEY `mapping_relation_id_fk_index` (`mapping_relation_id`),
UNIQUE KEY `unique_index` (`dealer_code`,`source_product_name`,`source_product_spec`) -- 设置索引时 索引的总和超长
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci COMMENT='产品mapping待办';
```

##### 问题2 数据插入MySQL 5.7时

```ruby
2019/08/05 11:35:28 main.go:84: [fatal] Error 1118: Row size too large. The maximum row size for the used table type, not counting BLOBs, is 65535. This includes storage overhead, check the manual. You have to change some columns to TEXT or BLOBs
# 原因：是因为MySQL中对行数据的最大限制为 一行数据不能超过 65535个字节,  varchar(1000)的字段太多了
CREATE TABLE `business_import_data_temp` (
  `tenant_id` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '租户id',
  `file_id` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '文件id',
  `valid_status` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '校验状态',
  `valid_result` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '校验结果',
  `op_time` datetime DEFAULT NULL COMMENT '入库时间',
  `c1` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '列c1',
  `c2` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '列c2',
  `c3` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '列c3',
  `c4` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '列c4',
   ......
  `c120` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '列c120',
  `paas_is_disable` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT '0' COMMENT '系统是否有效',
  `paas_create_user` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '系统创建人',
  `paas_create_time` datetime DEFAULT NULL COMMENT '系统创建时间',
  `paas_update_user` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '系统修改人',
  `paas_update_time` datetime DEFAULT NULL COMMENT '系统修改时间',
  `paas_version_no` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '系统版本号',
  `paas_is_del` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '系统是否删除',
  `paas_id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  PRIMARY KEY (`paas_id`),
  KEY `index_fileId` (`file_id`,`op_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci COMMENT='导入临时表';
```

##### 问题2相关资料： https://blog.csdn.net/qq\_30336433/article/details/81669957

```sql
1、varchar最多能存储65535个字节的数据。varchar 的最大长度受限于最大行长度（max row size，65535bytes）。65535并不是一个很精确的上限，可以继续缩小这个上限。65535个字节包括所有字段的长度，变长字段的长度标识（每个变长字段额外使用1或者2个字节记录实际数据长度）、NULL标识位的累计。
2、NULL标识位，如果varchar字段定义中带有default null允许列空,则需要需要1bit来标识，每8个bits的标识组成一个字段。一张表中存在N个varchar字段，那么需要（N+7）/8 （取整）bytes存储所有的NULL标识位。
        如果数据表只有一个varchar字段且该字段DEFAULT NULL，那么该varchar字段的最大长度为65532个字节，即65535-2-1=65532 byte。

mysql> CREATE TABLE t1 ( NAME VARCHAR ( 65533 ) ) charset = latin1;
ERROR 1118 (42000): Row size too large. The maximum row size for the used table type, not counting BLOBs, is 65535. This includes storage overhead, check the manual. You have to change some columns to TEXT or BLOBs

mysql> CREATE TABLE t1 ( NAME VARCHAR ( 65532 ) ) charset = latin1;
Query OK, 0 rows affected (0.31 sec)


# 测试认证：charset = latin1
# 根据 default null 占用 1bit； 65530+default null+2+default null 等于 65530 + 1 + 2 + 1
mysql> CREATE TABLE t1 ( NAME VARCHAR ( 65530 ) DEFAULT NULL, VALUE VARCHAR ( 2 ) DEFAULT NULL ) charset = latin1;
# 结果失败
ERROR 1118 (42000): Row size too large. The maximum row size for the used table type, not counting BLOBs, is 65535. This includes storage overhead, check the manual. You have to change some columns to TEXT or BLOBs

mysql>
# 65530+default null+1+default null 等于 65530 + 1 + 1 + 1
mysql> CREATE TABLE t1 ( NAME VARCHAR ( 65530 ) DEFAULT NULL, VALUE VARCHAR ( 1 ) DEFAULT NULL ) charset = latin1;
# 执行结果成功
Query OK, 0 rows affected (0.86 sec)

mysql>

# 测试TiDB3.0 插入数据
mysql>
mysql> CREATE TABLE t0 ( NAME1 VARCHAR ( 65535 ), NAME2 VARCHAR ( 65535 ), NAME3 VARCHAR ( 65535 ), NAME4 VARCHAR ( 65535 ) ) charset = latin1;
Query OK, 0 rows affected (0.14 sec)

mysql>
# 由此得出结论:
MySQL 单个列最大支持 65533 单位字节(不加 DEFAULT NULL)
TiDB  单个列最大支持 65535 单位字节(不加 DEFAULT NULL)

MySQL 单行最大不能超过 65535 单位字节(不加 DEFAULT NULL)
TiDB  单行没限制
```

* * *

* * *

#### `测`、TiDB 3.0 与 MariaDB 10.3.12数据交互 备份/恢复

- 开发服务器 TiDB 3.0：
    
    - ip: 172.160.180.46
    - 用户名: root
    - 密码：数据库密码
    - 端口: 4000
    - 数据库：dev2\_dc\_test
    - 备份路径：./backup\_0
- MariaDB 10.3.12：
    
    - ip: 172.160.180.6
    - 用户名: root
    - 密码：数据库密码
    - 端口: 3307

测试结果与 MySQL 5.7的问题一致

* * *

* * *

#### `测`、TiDB 3.0 与 MySQL 8.0数据交互 备份/恢复

- 开发服务器 TiDB 3.0：
    
    - ip: 172.160.180.46
    - 用户名: root
    - 密码：数据库密码
    - 端口: 4000
    - 数据库：dev2\_dc\_test
    - 备份路径：./backup\_0
- MySQL 8.0：
    
    - ip: 172.160.180.6
    - 用户名: root
    - 密码：数据库密码
    - 端口: 3305

测试结果 loader恢复数据时，不能自动创建 tidb\_loader数据库导致恢复失败，需要手动在目标库中创建；其它的问题与 MySQL 5.7 | MariaDB 10.3.12 的问题一致

* * *

* * *

##### 五、数据库备份常见用法

```sql
# 使用正则: 只备份以 dev2*开头的数据库
./mydumper -h 172.160.180.33 -u root -p 数据库密码 -P 4000 -v 3 -t 16 -F 64 -x 'dev2_*' --skip-tz-utc -o ./tidb_backup_20190814

# 使用正则: 过滤特定库，例如不备份mysql|test|INFORMATION_SCHEMA|PERFORMANCE_SCHEMA|tidb_loader库
./mydumper -h 172.160.180.33 -u root -p 数据库密码 -P 4000 -v 3 -t 16 -F 64 -x '^(?!(mysql|test|INFORMATION_SCHEMA|PERFORMANCE_SCHEMA|tidb_loader))' --skip-tz-utc -o ./tidb_backup_20190814

# 备所有数据库
./mydumper -h 172.160.180.33 -u root -p 数据库密码 -P 4000 -v 3 -t 16 -F 64 --skip-tz-utc -o ./tidb_backup_20190814

# 备所指定的数据库, 中的所有表
./mydumper -h 172.160.180.33 -u root -p 数据库密码 -P 4000 -v 3 -t 16 -F 64 -B dev2_dc_test --skip-tz-utc -o ./tidb_backup_20190814

# 备所指定的数据库, 中的某些表
./mydumper -h 172.160.180.33 -u root -p 数据库密码 -P 4000 -v 3 -t 16 -F 64 -B dev2_dc_test -T product,history,mapping,dc_unit --skip-tz-utc -o ./tidb_backup_20190814

# 备份以某些名称开头的数据库
./mydumper -h 172.160.180.53 -u root -p 数据库密码 -P 4000 -v 3 -t 16 -F 64 -e -x '^(dev2_paas\.|dev2_paas_system\.|dev2_quartz\.|dev2_pfizer\.|dev2_pfizer_activiti\.)' --skip-tz-utc -o ./tidb_backup_20190814

# 按每行 5000条数据，进行压缩备份
./mydumper -h 172.160.180.33 -u root -p 数据库密码 -P 4000 -v 3 -c -t 16 -r 5000 -x '^(?!(mysql|test|INFORMATION_SCHEMA|PERFORMANCE_SCHEMA|tidb_loader))' --skip-tz-utc -o ./tidb_backup_20190814

# 压缩备份数据库(解压时使用 gunzip *.gz)
./mydumper -h 172.160.180.33 -u root -p 数据库密码 -P 4000 -v 3 -c -t 16 -F 64 -B dev2_dc_test --skip-tz-utc -o ./tidb_backup_20190814
```

* * *

* * *

##### 六、单表恢复

`mysql -h 172.160.180.47 -u root -P 4000 -p schema < sql文件`

```ruby
# 恢复表结构
[tidb@dev10 ~]$ mysql -h 172.160.180.47 -u root -P 4000 -p dev2_pfizer < dev2_pfizer.sys_user-schema.sql
Enter password:
[tidb@dev10 ~]$

# 恢复数据
[tidb@dev10 ~]$ mysql -h 172.160.180.47 -u root -P 4000 -p dev2_pfizer < dev2_pfizer.sys_user.sql
Enter password:
[tidb@dev10 ~]$

```

* * *

* * *

##### 七、RECOVER TABLE 恢复GC之前的数据

[官网地址](https://pingcap.com/docs-cn/v3.0/reference/sql/statements/recover-table/ "官网地址")

[GC相关文档](https://pingcap.com/docs-cn/v3.0/reference/garbage-collection/configuration/ "GC相关文档")

**注意事项** 1. RECOVER 目前版本`只可以恢复 Table级别`的误操作，`DB级别`的还没有实现 2. 如果删除表后并过了 GC lifetime，就不能再用 RECOVER TABLE 来恢复被删除的表了，执行 RECOVER TABLE 语句会返回类似错误：`snapshot is older than GC safe point 2019-07-10 13:45:57 +0800 CST`

##### 语法

**根据表名恢复；需要 `use database;`**

```sql
> RECOVER TABLE table_name
```

**根据JOB\_ID恢复**

```sql
> RECOVER TABLE BY JOB ddl_job_id
```

##### **1\. `如果误删表，先将GC时间改大，防止数据被回收`**

```sql
SELECT VARIABLE_VALUE FROM mysql.tidb WHERE VARIABLE_NAME = 'tikv_gc_life_time';
-- 先将 gc时间改为24小时
UPDATE mysql.tidb SET VARIABLE_VALUE = '24h' WHERE VARIABLE_NAME = 'tikv_gc_life_time';
-- 数据恢复后在将 gc时间改为10分钟(默认)
UPDATE mysql.tidb SET VARIABLE_VALUE = '10m' WHERE VARIABLE_NAME = 'tikv_gc_life_time';
```

##### **2\. 恢复表**

```sql
mysql> DROP TABLE sys_user;
mysql>
mysql> ADMIN SHOW DDL JOBS 6;
+--------+-------------+------------+---------------+--------------+-----------+----------+-----------+-----------------------------------+--------+
| JOB_ID | DB_NAME     | TABLE_NAME | JOB_TYPE      | SCHEMA_STATE | SCHEMA_ID | TABLE_ID | ROW_COUNT | START_TIME                        | STATE  |
+--------+-------------+------------+---------------+--------------+-----------+----------+-----------+-----------------------------------+--------+
|   2226 | dev2_pfizer |            | drop table    | none         |      1437 |     2224 |         0 | 2019-08-30 15:44:12.884 +0800 CST | synced |
|   2225 | dev2_pfizer |            | create table  | public       |      1437 |     2224 |         0 | 2019-08-30 15:43:53.434 +0800 CST | synced |
+--------+-------------+------------+---------------+--------------+-----------+----------+-----------+-----------------------------------+--------+
6 rows in set (0.02 sec)

mysql>
mysql>
mysql>
# 要选择 JOB_TYPE 为 drop table 的 JOB_ID 进行恢复
mysql> RECOVER TABLE BY JOB 2226;
Query OK, 0 rows affected (1.38 sec)

mysql>
# 查看恢复后的结果
mysql> ADMIN SHOW DDL JOBS 6;
+--------+-------------+------------+---------------+--------------+-----------+----------+-----------+-----------------------------------+--------+
| JOB_ID | DB_NAME     | TABLE_NAME | JOB_TYPE      | SCHEMA_STATE | SCHEMA_ID | TABLE_ID | ROW_COUNT | START_TIME                        | STATE  |
+--------+-------------+------------+---------------+--------------+-----------+----------+-----------+-----------------------------------+--------+
|   2227 | dev2_pfizer | sys_user   | recover table | public       |      1437 |     2224 |         0 | 2019-08-30 15:44:58.835 +0800 CST | synced |
|   2226 | dev2_pfizer | sys_user   | drop table    | none         |      1437 |     2224 |         0 | 2019-08-30 15:44:12.884 +0800 CST | synced |
|   2225 | dev2_pfizer | sys_user   | create table  | public       |      1437 |     2224 |         0 | 2019-08-30 15:43:53.434 +0800 CST | synced |
+--------+-------------+------------+---------------+--------------+-----------+----------+-----------+-----------------------------------+--------+
6 rows in set (0.02 sec)

mysql>
```

**注意:** 根据删除表时的 DDL JOB\_ID 恢复被删除的表，会直接用 DDL JOB\_ID 找到被删除表进行恢复。 如果指定的 DDL JOB\_ID 的 DDL JOB\_TYPE `不是 DROP TABLE 类型，会报错`。
