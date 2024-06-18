---
title: "TiDB 4.0 可能要修改的 配置文件"
date: "2020-05-22"
categories: 
  - "tidb"
---

###### **[官方帖子](https://asktug.com/t/topic/34585/3 "官方帖子")**

* * *

* * *

* * *

#### 可能要修改的

###### 使用 TiUP 修改 原tidb 3.x `config/tidb.yml`、 `config/pd.yml`、 `config/tikv.yml` 配置文件

```ruby
[tidb@test1 ~]$ tiup cluster list
Starting /home/tidb/.tiup/components/cluster/v0.4.6/cluster list
Name      User  Version    Path                                                PrivateKey
---- ---- ------- ---- ----------
tidb-dev  tidb  v4.0.0-rc  /home/tidb/.tiup/storage/cluster/clusters/tidb-dev  /home/tidb/.tiup/storage/cluster/clusters/tidb-dev/ssh/id_rsa
[tidb@test1 ~]$

[tidb@test1 ~]$ tiup cluster edit-config tidb-dev
global:
  user: tidb
  ssh_port: 22
  deploy_dir: /home/tidb/tidb-deploy
  data_dir: /home/tidb/tidb-data

monitored:
  node_exporter_port: 9100
  blackbox_exporter_port: 9115
  deploy_dir: /home/tidb/tidb-deploy/monitored-9100
  data_dir: /home/tidb/tidb-data/monitored-9100
  log_dir: /home/tidb/tidb-deploy/monitored-9100/log


server_configs:

  tidb:
    binlog.enable: false
    binlog.ignore-error: false
    log.level: warn
    log.slow-threshold: 300
    # 用于处理v3.0.7和以前版本升级中的兼容性问题(为了兼容联合索引长度超长的问题，原(3072) 这里改为4倍)
    max-index-length: 12288
    # 开启支持大小写不敏感, 只有在集群初始化时配置才生效, 默认 false
    new_collations_enabled_on_first_bootstrap: true

  tikv:
    # 开启静默region, 用于减少 raftstore CPU 的消耗
    raftstore.hibernate-regions: true
    # 关闭将 tikv 的按 table 分裂配置, 默认 true
    coprocessor.split-region-on-table: false
    # coprocessor.split-region-on-table: true
    readpool.coprocessor.use-unified-pool: true
    readpool.storage.use-unified-pool: true

  pd:
    replication.enable-placement-rules: true
    schedule.leader-schedule-limit: 4
    schedule.region-schedule-limit: 2048
    schedule.replica-schedule-limit: 64
    # 默认 table 情况下，region merge 不会进行表表合并，所以在有大量的 drop/truncate table, create table, drop database 的时候，需要开启该参数
    # 原3.0 中 global.namespace-classifier: "table" 改为 schedule.enable-cross-table-merge: false
    # 原3.0 中 global.namespace-classifier: "default" 改为 schedule.enable-cross-table-merge: true
    # 当通过 tiup cluster edit-config 和 reload 的方式来修改的 PD 的参数，相应的参数不生效，还是以 pd-ctl 看到的参数状态为准。
    # tiup cluster 中跟 PD 相关的参数，只有在第一次初始化部署的时候才会生效，后续需要使用 pd-ctl 来修改。
    # /home/tidb/tidb-ansible/resources/bin/pd-ctl -u  http://192.168.180.59:2379 config show all
    # /home/tidb/tidb-ansible/resources/bin/pd-ctl -u http://192.168.180.59:2379 config set enable-cross-table-merge true
    schedule.enable-cross-table-merge: true

  tiflash: {}
  tiflash-learner: {}
  pump: {}
  drainer: {}
tidb_servers:
...................下面省略
[tidb@test1 ~]$
```

###### 重新加载配置文件

**`tiup cluster reload tidb-dev -N ip:port`** 或 **`tiup cluster reload tidb-dev -R tidb,tikv`**

```ruby
[tidb@test1 ~]$ tiup cluster reload tidb-dev -N 172.18.180.47:4000
```
