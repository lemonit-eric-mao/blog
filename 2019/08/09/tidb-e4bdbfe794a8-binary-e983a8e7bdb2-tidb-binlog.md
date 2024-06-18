---
title: 'TiDB 使用 Binary 部署 TiDB Binlog'
date: '2019-08-09T03:11:51+00:00'
status: publish
permalink: /2019/08/09/tidb-%e4%bd%bf%e7%94%a8-binary-%e9%83%a8%e7%bd%b2-tidb-binlog
author: 毛巳煜
excerpt: ''
type: post
id: 4991
category:
    - TiDB
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
##### TiDB 3.0 同步到 MariaDB 10.4.7 (使用 Binary 部署)

[官方地址](https://pingcap.com/docs-cn/v3.0/how-to/deploy/tidb-binlog/ "官方地址")  
[官方隐藏地址](https://pingcap.com/docs-cn/v3.0/reference/tools/tidb-binlog/tidb-binlog-local/#%E4%BD%BF%E7%94%A8-tidb-ansible-%E9%83%A8%E7%BD%B2-pump-%E6%8E%A8%E8%8D%90 "官方隐藏地址")

**注意：**  
**`一个 drainer 对应一个下游。不能多个 drainer 对应一个下游。`**  
优点：配置操作简单，适合单点部署速度快  
缺点：扩展集群麻烦，需要在每台机器上下载二进制工具包，手动进行启动

##### TiDB 3.0 同步到 MariaDB 10.4.7

TiDB(主) --&gt; Pump/Drainer --&gt; MariaDB(从)

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

##### 1. 使用 binary 部署 Pump

构建配置文件 pump.toml

```ruby
[tidb@test1 resources]<span class="katex math inline">pwd
/home/tidb/tidb-ansible/resources
[tidb@test1 resources]</span>
[tidb@test1 resources]<span class="katex math inline">mkdir config
[tidb@test1 resources]</span>
[tidb@test1 resources]$ cat > config/pump.toml 
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

##### 2. 对已有的 TiDB Cluster 部署 binlog

- 修改 tidb-ansible/inventory.ini 文件 
  - enable\_binlog = True
- 执行 \[tidb@test1 tidb-ansible\]$ ansible-playbook rolling\_update.yml --tags=tidb 
  - drainer 目前需要手动部署  
      `注意： Pump服务启动以后才可以开启binlog，否则执行 ansible-playbook rolling_update.yml --tags=tidb 更新会失败`

##### 3. 使用 binary 部署 Drainer

构建配置文件 drainer.toml

```ruby
[tidb@test1 resources]$ cat > config/drainer.toml _obinlog
# 如果运行多个 Drainer 同步数据到同一个 Kafka 集群，每个 Drainer 的 topic-name 需要设置不同的名称
# topic-name = ""
eric

[tidb@test1 resources]$

```

使用 binlogctl 工具生成 Drainer 初次启动所需的 tso 信息

```ruby
[tidb@test1 resources]<span class="katex math inline">./bin/binlogctl -pd-urls=http://172.160.180.46:2379 -cmd generate_meta
INFO[0000] [pd] create pd client with endpoints [http://172.160.180.46:2379]
INFO[0000] [pd] leader switches to: http://172.160.180.47:2379, previous:
INFO[0000] [pd] init cluster id 6722975452193162868
[2019/08/09 10:11:26.523 +08:00] [INFO] [meta.go:124] ["save meta"] [meta="commitTS: 410338921974857729"]
[tidb@test1 resources]</span>
[tidb@test1 resources]<span class="katex math inline">[tidb@test1 resources]</span> nohup ./bin/drainer -config config/drainer.toml -initial-commit-ts 410338921974857729 &

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

- - - - - -

- - - - - -

- - - - - -

##### binlogctl 工具用法

##### 工具目录

```ruby
[tidb@test1 resources]<span class="katex math inline">pwd
/home/tidb/tidb-ansible/resources
[tidb@test1 resources]</span>

```

##### 查询所有的 Pump 的状态：

```ruby
[tidb@test1 resources]<span class="katex math inline">./bin/binlogctl -pd-urls=http://172.160.180.46:2379 -cmd pumps
[2019/08/09 15:28:31.177 +08:00] [INFO] [nodes.go:47] ["query node"] [type=pump] [node="{NodeID: test1:8250, Addr: 172.160.180.46:8250, State: paused, MaxCommitTS: 410342402329673729, UpdateTime: 2019-08-09 14:27:20 +0800 CST}"]
[tidb@test1 resources]</span>

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

- - - - - -

##### 查询所有的 Drainer 的状态：

```ruby
[tidb@test1 resources]<span class="katex math inline">./bin/binlogctl -pd-urls=http://172.160.180.46:2379 -cmd drainers
[2019/08/09 15:29:33.606 +08:00] [INFO] [nodes.go:47] ["query node"] [type=drainer] [node="{NodeID: test1:8249, Addr: 172.160.180.46:8249, State: paused, MaxCommitTS: 410342402329673729, UpdateTime: 2019-08-09 14:34:53 +0800 CST}"]
[tidb@test1 resources]</span>

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

- - - - - -

- - - - - -

##### 下线pump集群与 drainer

**注意：下线pump集群 `必须要优先下线drainer`否则pump集群里始终有一个是停不下来的**  
1.先下线drainer

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

- - - - - -

- - - - - -