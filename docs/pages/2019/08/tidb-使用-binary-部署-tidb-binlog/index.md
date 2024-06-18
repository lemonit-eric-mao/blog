---
title: "TiDB 使用 Binary 部署 TiDB Binlog"
date: "2019-08-09"
categories: 
  - "tidb"
---

##### TiDB 3.0 同步到 MariaDB 10.4.7 (使用 Binary 部署)

[官方地址](https://pingcap.com/docs-cn/v3.0/how-to/deploy/tidb-binlog/ "官方地址") [官方隐藏地址](https://pingcap.com/docs-cn/v3.0/reference/tools/tidb-binlog/tidb-binlog-local/#%E4%BD%BF%E7%94%A8-tidb-ansible-%E9%83%A8%E7%BD%B2-pump-%E6%8E%A8%E8%8D%90 "官方隐藏地址")

**注意：** **`一个 drainer 对应一个下游。不能多个 drainer 对应一个下游。`** 优点：配置操作简单，适合单点部署速度快 缺点：扩展集群麻烦，需要在每台机器上下载二进制工具包，手动进行启动

##### TiDB 3.0 同步到 MariaDB 10.4.7

TiDB(主) --> Pump/Drainer --> MariaDB(从)

- 开发服务器 TiDB 3.0：
    
    - IP: 172.160.180.46(入口机), 172.160.180.47, 172.160.180.48
    - 用户名: root
    - 密码：数据库密码
    - 端口: 4000
- MariaDB 10.4.7：
    
    - IP: 172.160.180.6
    - 用户名: root
    - 密码：数据库密码
    - 端口: 3305

**Pump 和 Drainer 已经包含在 TiDB 3.0 的下载包中 `/home/tidb/tidb-ansible/resources/bin`**

##### 1\. 使用 binary 部署 Pump

构建配置文件 pump.toml

```ruby
[tidb@test1 resources]$ pwd
/home/tidb/tidb-ansible/resources
[tidb@test1 resources]$
[tidb@test1 resources]$ mkdir config
[tidb@test1 resources]$
[tidb@test1 resources]$ cat > config/pump.toml << eric

# Pump Configuration

# 这里的IP地址是，pump工具所在的服务器IP地址
# Pump 绑定的地址
addr = "172.160.180.46:8250"

# Pump 对外提供服务的地址
advertise-addr = "172.160.180.46:8250"

# Pump 只保留多少天以内的数据 (默认 7)
gc = 1

# Pump 数据存储位置路径
data-dir = "data/pump"

# Pump 向 PD 发送心跳的间隔 (单位 秒)
heartbeat-interval = 2

# PD 集群节点的地址
pd-urls = "http://172.160.180.46:2379,http://172.160.180.47:2379,http://172.160.180.48:2379"

# log 文件路径
log-file = "logs/pump.log"

# [storage]
# 设置为 true（默认值）来保证可靠性，确保 binlog 数据刷新到磁盘
# sync-log = true
eric

[tidb@test1 resources]$
[tidb@test1 resources]$
[tidb@test1 resources]$ nohup ./bin/pump -config config/pump.toml &

```

登录TiDB 使用命令行查看 pump

```sql
mysql>
mysql> show pump status;
+------------+---------------------+--------+--------------------+---------------------+
| NodeID     | Address             | State  | Max_Commit_Ts      | Update_Time         |
+------------+---------------------+--------+--------------------+---------------------+
| test1:8250 | 172.160.180.46:8250 | online | 410338410374627329 | 2019-08-09 10:13:31 |
+------------+---------------------+--------+--------------------+---------------------+
1 row in set (0.00 sec)

mysql>
```

##### 2\. 对已有的 TiDB Cluster 部署 binlog

- 修改 tidb-ansible/inventory.ini 文件
    
    - enable\_binlog = True
- 执行 \[tidb@test1 tidb-ansible\]$ ansible-playbook rolling\_update.yml --tags=tidb
    
    - drainer 目前需要手动部署 `注意： Pump服务启动以后才可以开启binlog，否则执行 ansible-playbook rolling_update.yml --tags=tidb 更新会失败`

##### 3\. 使用 binary 部署 Drainer

构建配置文件 drainer.toml

```ruby
[tidb@test1 resources]$ cat > config/drainer.toml << eric

# Drainer Configuration.
# 这里的IP地址是，drainer工具所在的服务器IP地址
# Drainer 提供服务的地址("172.160.180.46:8249")
addr = "172.160.180.46:8249"

# 向 PD 查询在线 Pump 的时间间隔 (默认 10，单位 秒)
detect-interval = 10

# Drainer 数据存储位置路径 (默认 "data.drainer")
data-dir = "data/drainer"

# PD 集群节点的地址
pd-urls = "http://172.160.180.46:2379,http://172.160.180.47:2379,http://172.160.180.48:2379"

# log 文件路径
log-file = "logs/drainer.log"

# Drainer 从 Pump 获取 binlog 时对数据进行压缩，值可以为 "gzip"，如果不配置则不进行压缩
# compressor = "gzip"

# Syncer Configuration
[syncer]
# 如果设置了该项，会使用该 sql-mode 解析 DDL 语句
# sql-mode = "STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION"

# 输出到下游数据库一个事务的 SQL 语句数量 (默认 20)
txn-batch = 20

# 同步下游的并发数，该值设置越高同步的吞吐性能越好 (默认 16)
worker-count = 16

# 是否禁用拆分单个 binlog 的 SQL 的功能，如果设置为 true，则按照每个 binlog
# 顺序依次还原成单个事务进行同步（下游服务类型为 MySQL, 该项设置为 False）
disable-dispatch = false

# Drainer 下游服务类型（默认为 mysql）
# 参数有效值为 "mysql"，"file"，"kafka"，"flash"
db-type = "mysql"

# db 过滤列表 (默认 "INFORMATION_SCHEMA,PERFORMANCE_SCHEMA,mysql,test")，
# 不支持对 ignore schemas 的 table 进行 rename DDL 操作
ignore-schemas = "INFORMATION_SCHEMA,PERFORMANCE_SCHEMA,mysql"

# replicate-do-db 配置的优先级高于 replicate-do-table。如果配置了相同的库名，支持使用正则表达式进行配置。
# 以 '~' 开始声明使用正则表达式

# replicate-do-db = ["~^b.*","s1"]

# [[syncer.replicate-do-table]]
# db-name ="test"
# tbl-name = "log"

# [[syncer.replicate-do-table]]
# db-name ="test"
# tbl-name = "~^a.*"

# 忽略同步某些表
# [[syncer.ignore-table]]
# db-name = "test"
# tbl-name = "log"

# db-type 设置为 mysql 时，下游数据库服务器参数
[syncer.to]
host = "172.160.180.6"
user = "root"
password = "q1w2E#R"
port = 3305

# db-type 设置为 file 时，存放 binlog 文件的目录
# [syncer.to]
# dir = "data/drainer"

# db-type 设置为 kafka 时，Kafka 相关配置
# [syncer.to]
# zookeeper-addrs = "127.0.0.1:2181"
# kafka-addrs = "127.0.0.1:9092"
# kafka-version = "0.8.2.0"

# 保存 binlog 数据的 Kafka 集群的 topic 名称，默认值为 <cluster-id>_obinlog
# 如果运行多个 Drainer 同步数据到同一个 Kafka 集群，每个 Drainer 的 topic-name 需要设置不同的名称
# topic-name = ""
eric

[tidb@test1 resources]$
```

使用 binlogctl 工具生成 Drainer 初次启动所需的 tso 信息

```ruby
[tidb@test1 resources]$ ./bin/binlogctl -pd-urls=http://172.160.180.46:2379 -cmd generate_meta
INFO[0000] [pd] create pd client with endpoints [http://172.160.180.46:2379]
INFO[0000] [pd] leader switches to: http://172.160.180.47:2379, previous:
INFO[0000] [pd] init cluster id 6722975452193162868
[2019/08/09 10:11:26.523 +08:00] [INFO] [meta.go:124] ["save meta"] [meta="commitTS: 410338921974857729"]
[tidb@test1 resources]$
[tidb@test1 resources]$
[tidb@test1 resources]$ nohup ./bin/drainer -config config/drainer.toml -initial-commit-ts 410338921974857729 &
```

登录TiDB 使用命令行查看 drainer

```sql
mysql>
mysql> show drainer status;
+------------+---------------------+--------+--------------------+---------------------+
| NodeID     | Address             | State  | Max_Commit_Ts      | Update_Time         |
+------------+---------------------+--------+--------------------+---------------------+
| test1:8249 | 172.160.180.48:8249 | online | 410338377462448129 | 2019-08-09 10:12:54 |
+------------+---------------------+--------+--------------------+---------------------+
1 row in set (0.01 sec)

mysql>
```

* * *

* * *

* * *

##### binlogctl 工具用法

##### 工具目录

```ruby
[tidb@test1 resources]$ pwd
/home/tidb/tidb-ansible/resources
[tidb@test1 resources]$
```

##### 查询所有的 Pump 的状态：

```ruby
[tidb@test1 resources]$ ./bin/binlogctl -pd-urls=http://172.160.180.46:2379 -cmd pumps
[2019/08/09 15:28:31.177 +08:00] [INFO] [nodes.go:47] ["query node"] [type=pump] [node="{NodeID: test1:8250, Addr: 172.160.180.46:8250, State: paused, MaxCommitTS: 410342402329673729, UpdateTime: 2019-08-09 14:27:20 +0800 CST}"]
[tidb@test1 resources]$
```

##### 修改 Pump 的状态

```ruby
bin/binlogctl -pd-urls=http://172.160.180.46:2379 -cmd update-pump -node-id test1:8250 -state paused
```

##### 暂停 Pump

```ruby
bin/binlogctl -pd-urls=http://172.160.180.46:2379 -cmd pause-pump -node-id test1:8250
```

##### 下线 Pump

```ruby
bin/binlogctl -pd-urls=http://172.160.180.46:2379 -cmd offline-pump -node-id test1:8250
```

* * *

##### 查询所有的 Drainer 的状态：

```ruby
[tidb@test1 resources]$ ./bin/binlogctl -pd-urls=http://172.160.180.46:2379 -cmd drainers
[2019/08/09 15:29:33.606 +08:00] [INFO] [nodes.go:47] ["query node"] [type=drainer] [node="{NodeID: test1:8249, Addr: 172.160.180.46:8249, State: paused, MaxCommitTS: 410342402329673729, UpdateTime: 2019-08-09 14:34:53 +0800 CST}"]
[tidb@test1 resources]$
```

##### 修改 Drainer 的状态

```ruby
bin/binlogctl -pd-urls=http://172.160.180.46:2379 -cmd update-drainer -node-id test1:8249 -state paused
```

##### 暂停 Drainer

```ruby
bin/binlogctl -pd-urls=http://172.160.180.46:2379 -cmd pause-drainer -node-id test1:8249
```

##### 下线 Drainer

```ruby
bin/binlogctl -pd-urls=http://172.160.180.46:2379 -cmd offline-drainer -node-id test1:8249
```

* * *

* * *

##### 下线pump集群与 drainer

**注意：下线pump集群 `必须要优先下线drainer`否则pump集群里始终有一个是停不下来的** 1.先下线drainer

```ruby
# 先修改状态
bin/binlogctl -pd-urls=http://172.160.180.46:2379 -cmd update-drainer -node-id test1:8249 -state offline
# 在下线drainer
bin/binlogctl -pd-urls=http://172.160.180.46:2379 -cmd offline-drainer -node-id test1:8249
```

2.下线pump集群

```ruby
# 将pump集群所有状态修改为 offline
bin/binlogctl -pd-urls=http://172.160.180.46:2379 -cmd update-pump -node-id test1:8250 -state offline
# 下线pump
bin/binlogctl -pd-urls=http://172.160.180.46:2379 -cmd offline-pump -node-id test1:8250
```

* * *

* * *
