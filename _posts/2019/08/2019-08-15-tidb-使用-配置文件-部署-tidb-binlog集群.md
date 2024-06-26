---
title: "TiDB 使用 配置文件 部署 TiDB Binlog(集群)"
date: "2019-08-15"
categories: 
  - "tidb"
---

#### TiDB 3.0 同步到 MariaDB 10.4.7 (修改 配置文件 部署到集群)

TiDB(主) --> Pump/Drainer --> MariaDB(从)

[官网教程](https://pingcap.com/docs-cn/v3.0/how-to/deploy/tidb-binlog/ "官网教程")

**注意**： **`一个 drainer 对应一个下游。不能多个 drainer 对应一个下游。`** 优点：修改配置文件，相对来说比较麻烦 缺点：扩展集群简单，加入对应的IP地址，使用ansible-playbook部署运行

- 开发服务器 TiDB 3.0：
    
    - IP: 172.160.180.46
    - 用户名: root
    - 密码：数据库密码
    - 端口: 4000
    - 数据库：eric\_tidb\_test
    - 备份路径：./backup\_0
- MariaDB 10.4.7：
    
    - IP: 172.160.180.6
    - 用户名: root
    - 密码：数据库密码
    - 端口: 3305
    - 数据库：eric\_tidb\_test

##### Pump/Drainer

**TiDB Binlog 集群主要分为 Pump 和 Drainer 两个组件，以及 binlogctl 工具：**

**Pump** Pump 用于实时记录 TiDB 产生的 Binlog，并将 Binlog 按照事务的提交时间进行排序，再提供给 Drainer 进行消费。

**Drainer** Drainer 从各个 Pump 中收集 Binlog 进行归并，再将 Binlog 转化成 SQL 或者指定格式的数据，最终同步到下游。

##### binlogctl 工具

**binlogctl 是一个 TiDB Binlog 配套的运维工具，具有如下功能：**

- 获取 TiDB 集群当前的 TSO
- 查看 Pump/Drainer 状态
- 修改 Pump/Drainer 状态
- 暂停/下线 Pump/Drainer

##### 主要特性

- 多个 Pump 形成一个集群，可以水平扩容。
- TiDB 通过内置的 Pump Client 将 Binlog 分发到各个 Pump。
- Pump 负责存储 Binlog，并将 Binlog 按顺序提供给 Drainer。
- Drainer 负责读取各个 Pump 的 Binlog，归并排序后发送到下游。

官方文档：https://pingcap.com/docs-cn/v3.0/reference/tidb-binlog-overview/

##### 注意事项

- 需要使用 TiDB v2.0.8-binlog、v2.1.0-rc.5 及以上版本，否则不兼容该版本的 TiDB Binlog。
    
- Drainer 支持将 Binlog 同步到 MySQL、TiDB、Kafka 或者本地文件。如果需要将 Binlog 同步到其他 Drainer 不支持的类型的系统中，可以设置 Drainer 将 Binlog 同步到 Kafka，然后根据 binlog slave protocol 进行定制处理，参考 binlog slave client 用户文档。
    
- 如果 TiDB Binlog 用于增量恢复，可以设置配置项 db-type="file"，Drainer 会将 binlog 转化为指定的 proto buffer 格式的数据，再写入到本地文件中。这样就可以使用 Reparo 恢复增量数据。 关于 db-type 的取值，应注意：
    
    如果 TiDB 版本 < 2.1.9，则 db-type="pb"。 如果 TiDB 版本 > = 2.1.9，则 db-type="file" 或 db-type="pb"。
    
- 如果下游为 MySQL/TiDB，数据同步后可以使用 sync-diff-inspector 进行数据校验。

* * *

* * *

* * *

#### 在已有的集群上部署 pump/drainer

##### 配置/部署 pump

官网地址: https://pingcap.com/docs-cn/v3.0/how-to/deploy/tidb-binlog/

###### 1 编辑 inventory.ini 配置文件，添加 pump服务器的配置，默认可以和 tidb-server 一起部署

```
......
## 为 pump_servers 主机组添加部署机器 IP。
[pump_servers]
172.160.180.46
172.160.180.47
172.160.180.48

......

### 设置 enable_binlog = True，表示 TiDB 集群开启 binlog。
## binlog trigger
#enable_binlog = False
enable_binlog = True
......
```

###### 2 部署 pump\_servers

```ruby
[tidb@test1 tidb-ansible]$ pwd
/home/tidb/tidb-ansible
[tidb@test1 tidb-ansible]$ ansible-playbook deploy.yml --tags=pump
......
Congrats! All goes well. :-)
[tidb@test1 tidb-ansible]$
```

###### 3 启动 pump\_servers

```ruby
[tidb@test1 tidb-ansible]$ ansible-playbook start.yml --tags=pump
......
Congrats! All goes well. :-)
[tidb@test1 tidb-ansible]$
```

###### 4 滚动更新 tidb\_servers

```ruby
[tidb@test1 tidb-ansible]$ ansible-playbook rolling_update.yml --tags=tidb
......
Congrats! All goes well. :-)
[tidb@test1 tidb-ansible]$
```

###### 5 滚动更新监控信息

```ruby
[tidb@test1 tidb-ansible]$ ansible-playbook rolling_update_monitor.yml --tags=prometheus
......
Congrats! All goes well. :-)
[tidb@test1 tidb-ansible]$
```

##### 查看 Pump 服务状态

###### 方式一 登录TiDB

```sql
# 查看 pump 运行状态
mysql>  show pump status;
+------------+---------------------+--------+--------------------+---------------------+
| NodeID     | Address             | State  | Max_Commit_Ts      | Update_Time         |
+------------+---------------------+--------+--------------------+---------------------+
| test3:8250 | 172.160.180.48:8250 | online | 410320483015983108 | 2019-08-08 15:13:45 |
| test1:8250 | 172.160.180.46:8250 | online | 410320483002875905 | 2019-08-08 15:13:44 |
| test2:8250 | 172.160.180.47:8250 | online | 410320483015983105 | 2019-08-08 15:13:45 |
+------------+---------------------+--------+--------------------+---------------------+
3 rows in set (0.00 sec)

# 查看 drainer 运行状态
mysql> show drainer status;
Empty set (0.00 sec)

# 查看 binlog 是否开启   1:开启   0:关闭
mysql> show variables like "log_bin";
+---------------+-------+
| Variable_name | Value |
+---------------+-------+
| log_bin       | 1     |
+---------------+-------+
1 row in set (0.01 sec)

mysql>
```

###### 方式二 使用工具查看 pump 运行状态

```ruby
[tidb@test1 resources]$ pwd
/home/tidb/tidb-ansible/resources
[tidb@test1 resources]$
[tidb@test1 resources]$ bin/binlogctl -pd-urls=http://172.160.180.46:2379 -cmd pumps
[2019/08/08 15:18:00.761 +08:00] [INFO] [nodes.go:47] ["query node"] [type=pump] [node="{NodeID: test2:8250, Addr: 172.160.180.47:8250, State: online, MaxCommitTS: 410320549967560705, UpdateTime: 2019-08-08 15:18:00 +0800 CST}"]
[2019/08/08 15:18:00.762 +08:00] [INFO] [nodes.go:47] ["query node"] [type=pump] [node="{NodeID: test3:8250, Addr: 172.160.180.48:8250, State: online, MaxCommitTS: 410320549980667905, UpdateTime: 2019-08-08 15:18:00 +0800 CST}"]
[2019/08/08 15:18:00.762 +08:00] [INFO] [nodes.go:47] ["query node"] [type=pump] [node="{NodeID: test1:8250, Addr: 172.160.180.46:8250, State: online, MaxCommitTS: 410320549967560706, UpdateTime: 2019-08-08 15:17:59 +0800 CST}"]
[tidb@test1 resources]$
```

* * *

* * *

##### 配置/部署 drainer

###### 1 使用 binlogctl 工具生成 Drainer 初次启动所需的 tso 信息，命令：(仅限首次部署)

```ruby
[tidb@test1 resources]$ pwd
/home/tidb/tidb-ansible/resources
[tidb@test1 resources]$
[tidb@test1 resources]$ bin/binlogctl -pd-urls=http://172.160.180.46:2379 -cmd generate_meta
INFO[0000] [pd] create pd client with endpoints [http://172.160.180.46:2379]
INFO[0000] [pd] leader switches to: http://172.160.180.46:2379, previous:
INFO[0000] [pd] init cluster id 6720123059944601191
[2019/08/08 15:22:40.926 +08:00] [INFO] [meta.go:124] ["save meta"] [meta="commitTS: 410320623603810307"]
[tidb@test1 resources]$
```

`如果不是首次部署 drainer 需要从mydumper 备份的文件中找到 metadata，使用它里面的 Pos:的值`

```ruby
[tidb@test1 bin]$ pwd
/home/tidb/tidb-tools/tidb-enterprise-tools-latest-linux-amd64/bin
[tidb@test1 bin]$
[tidb@test1 bin]$./mydumper -h 172.160.180.46 -u root -p 数据库密码 -P 4000 -t 16 -F 64 -x dev2* --skip-tz-utc -o ./tidb_dev2_backup_20190822_180003
[tidb@test1 bin]$ grep Pos tidb_dev2_backup_20190822_180003/metadata | awk -F ':' '{print $2}'
 410640237391249412
[tidb@test1 bin]$
```

###### 2 编辑 inventory.ini 配置文件，以下游为 MySQL 为例，别名为 drainer\_mysql

```
......
# 以下游为 MySQL 为例，别名为 `drainer_mysql_1`
[drainer_servers]
drainer_mysql_1 ansible_host=172.160.180.46 initial_commit_ts="410320623603810307"

......
```

###### 3 复制 drainer 模板文件

**注意：** 配置文件名命名规则为 `别名_drainer-cluster.toml`，否则部署时无法找到自定义配置文件。

```ruby
[tidb@test1 conf]$ pwd
/home/tidb/tidb-ansible/conf
[tidb@test1 conf]$
[tidb@test1 conf]$ cp drainer-cluster.toml drainer_mysql_1_drainer-cluster.toml
```

###### 4 db-type 设置为 "mysql"， 配置下游 MySQL 信息。

```ruby
[tidb@test1 conf]$ cat drainer_mysql_1_drainer-cluster.toml
......
[syncer]
# downstream storage, equal to --dest-db-type
# valid values are "mysql", "file", "tidb", "flash", "kafka"
# 设置下游的存储类型为 MySQL
db-type = "mysql"
......
# the downstream mysql protocol database
# 设置下游存储的连接地址
[syncer.to]
host = "172.160.180.6"
user = "root"
password = "数据库密码"
port = 3305
......
```

###### 5 部署 Drainer

```ruby
[tidb@test1 tidb-ansible]$ pwd
/home/tidb/tidb-ansible
[tidb@test1 tidb-ansible]$
[tidb@test1 tidb-ansible]$ ansible-playbook deploy_drainer.yml
......
Congrats! All goes well. :-)
[tidb@test1 tidb-ansible]$
```

###### 6 启动 Drainer

```ruby
[tidb@test1 tidb-ansible]$ pwd
/home/tidb/tidb-ansible
[tidb@test1 tidb-ansible]$
[tidb@test1 tidb-ansible]$ ansible-playbook start_drainer.yml
......
Congrats! All goes well. :-)
[tidb@test1 tidb-ansible]$
```

##### 查看 Drainer 服务状态

###### 方式一 登录TiDB

```sql
# 查看 drainer 运行状态
mysql> show drainer status;
+------------+---------------------+--------+--------------------+---------------------+
| NodeID     | Address             | State  | Max_Commit_Ts      | Update_Time         |
+------------+---------------------+--------+--------------------+---------------------+
| test1:8249 | 172.160.180.46:8249 | online | 410565673411411969 | 2019-08-19 11:02:34 |
+------------+---------------------+--------+--------------------+---------------------+
3 rows in set (0.01 sec)

mysql>
```

###### 方式二 使用工具查看 Drainer 运行状态

```ruby
[tidb@test1 resources]$ pwd
/home/tidb/tidb-ansible/resources
[tidb@test1 resources]$ bin/binlogctl -pd-urls=http://172.160.180.46:2379 -cmd drainers
[2019/08/19 11:04:55.158 +08:00] [INFO] [nodes.go:47] ["query node"] [type=drainer] [node="{NodeID: test2:8249, Addr: 172.160.180.47:8249, State: online, MaxCommitTS: 410565709639712769, UpdateTime: 2019-08-19 11:04:53 +0800 CST}"]
[tidb@test1 resources]$

```

* * *

* * *

* * *

#### 常用命令

##### pump

```ruby
# 部署 pump_servers
[tidb@test1 tidb-ansible]$ ansible-playbook deploy.yml --tags=pump
# 启动 pump_servers
[tidb@test1 tidb-ansible]$ ansible-playbook start.yml --tags=pump
# 停止 pump_servers
[tidb@test1 tidb-ansible]$ ansible-playbook stop.yml --tags=pump
```

##### drainer

```ruby
# 部署 Drainer
[tidb@test1 tidb-ansible]$ ansible-playbook deploy_drainer.yml
# 启动 Drainer
[tidb@test1 tidb-ansible]$ ansible-playbook start_drainer.yml
# 停止 Drainer
[tidb@test1 tidb-ansible]$ ansible-playbook stop_drainer.yml
```

* * *

\===========================================================

* * *

##### 注意事项

1. 先启动pump > 在启动drainer
2. 先停止drainer > 在停止pump
3. 开启 pump/drainer 必须开启 binlog
