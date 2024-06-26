---
title: "TiDB 4.0 安装部署"
date: "2020-04-09"
categories: 
  - "tidb"
---

**[TiUP部署](https://pingcap.com/docs-cn/stable/how-to/deploy/orchestrated/tiup/#%E7%AC%AC-1-%E6%AD%A5%E8%BD%AF%E7%A1%AC%E4%BB%B6%E7%8E%AF%E5%A2%83%E9%85%8D%E7%BD%AE "TiUP部署")**

##### 环境

- host: 172.18.180.46   test1
- host: 172.18.180.47   test2
- host: 172.18.180.48   test3
- host: 172.18.181.18   test4
- host: 172.18.181.6   test5

* * *

* * *

* * *

###### 在中控机上创建 tidb 用户

```ruby
[root@test1 ~]# useradd -m -d /home/tidb tidb
[root@test1 ~]# passwd tidb
# 输入tidb用户密码
[root@test1 ~]# visudo
tidb ALL=(ALL) NOPASSWD: ALL
[root@test1 ~]#
# 进入tidb用户
[root@test1 ~]# su - tidb
```

* * *

* * *

* * *

###### 下载TiUP安装文件

```ruby
[tidb@test1 ~]$ curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 6030k  100 6030k    0     0  4780k      0  0:00:01  0:00:01 --:--:-- 4782k
Detected shell: /bin/bash
Shell profile:  /home/tidb/.bash_profile
/home/tidb/.bash_profile has been modified to to add tiup to PATH
open a new terminal or source /home/tidb/.bash_profile to use it
Installed path: /home/tidb/.tiup/bin/tiup
===============================================
Have a try:     tiup playground
===============================================
[tidb@test1 ~]$
```

1. 重新声明全局环境变量

```ruby
[tidb@test1 ~]$ source .bash_profile
```

2. 确认 TiUP 工具是否安装

```ruby
[tidb@test1 ~]$ which tiup
~/.tiup/bin/tiup
[tidb@test1 ~]$
```

3. 安装 TiUP cluster 组件

```ruby
[tidb@test1 ~]$ tiup cluster
```

4. 如果已经安装，则更新 TiUP cluster 组件至最新版本

```ruby
[tidb@test1 ~]$ tiup update --self && tiup update cluster
```

预期输出 **`Update successfully!`** 字样。

5. 验证当前 TiUP cluster 版本信息

```ruby
[tidb@test1 ~]$ tiup --binary cluster
[tidb@test1 ~]$
```

* * *

* * *

* * *

###### 配置文件模版 topology.yaml

```yaml
# Global variables are applied to all deployments and as the default value of
# them if the specific deployment value missing.
global:
  user: "tidb"
  ssh_port: 22
  deploy_dir: "/home/tidb/tidb-deploy"
  data_dir: "/home/tidb/tidb-data"


monitored:
  deploy_dir: "/home/tidb/tidb-deploy/monitored-9100"
  data_dir: "/home/tidb/tidb-data/monitored-9100"
  log_dir: "/home/tidb/tidb-deploy/monitored-9100/log"


server_configs:

  tidb:
    log.slow-threshold: 300
    log.level: warn
    binlog.enable: false
    binlog.ignore-error: false
    # 用于处理v3.0.7和以前版本升级中的兼容性问题(为了兼容联合索引长度超长的问题，原(3072) 这里改为4倍)
    max-index-length: 12288
    # 开启支持大小写不敏感, 只有在集群初始化时配置才生效, 默认 false
    new_collations_enabled_on_first_bootstrap: true


  tikv:
    readpool.storage.use-unified-pool: true
    readpool.coprocessor.use-unified-pool: true


  pd:
    schedule.leader-schedule-limit: 4
    schedule.region-schedule-limit: 2048
    schedule.replica-schedule-limit: 64
    # 如果要使用TiFlash，需要加入下面这行配置
    replication.enable-placement-rules: true


pd_servers:
  #- host: 172.18.180.47
    # ssh_port: 22
    # name: "pd-1"
    # client_port: 2379
    # peer_port: 2380
    # deploy_dir: "deploy/pd-2379"
    # data_dir: "data/pd-2379"
    # log_dir: "deploy/pd-2379/log"
    # numa_node: "0,1"
    # # Config is used to overwrite the `server_configs.pd` values
    # config:
    #   schedule.max-merge-region-size: 20
    #   schedule.max-merge-region-keys: 200000
  - host: 172.18.180.48
  - host: 172.18.181.18
  - host: 172.18.180.47

tidb_servers:
  #- host: 172.18.180.47
    # ssh_port: 22
    # port: 4000
    # status_port: 10080
    # deploy_dir: "deploy/tidb-4000"
    # log_dir: "deploy/tidb-4000/log"
    # numa_node: "0,1"
    # # Config is used to overwrite the `server_configs.tidb` values
    # config:
    #   log.level: warn
    #   log.slow-query-file: tidb-slow-overwritten.log
  - host: 172.18.180.47
  - host: 172.18.180.48
  - host: 172.18.181.18

tikv_servers:
  #- host: 172.18.180.47
    # ssh_port: 22
    # port: 20160
    # status_port: 20180
    # deploy_dir: "deploy/tikv-20160"
    # data_dir: "data/tikv-20160"
    # log_dir: "deploy/tikv-20160/log"
    # numa_node: "0,1"
    # # Config is used to overwrite the `server_configs.tikv` values
    #  config:
    #    server.labels:
    #      zone: sh
    #      dc: sha
    #      rack: rack1
    #      host: host1
  - host: 172.18.180.47
  - host: 172.18.180.48
  - host: 172.18.181.18

# 添加 TiFlash
tiflash_servers:
  #- host: 172.18.181.6
    # ssh_port: 22
    # tcp_port: 9000
    # http_port: 8123
    # flash_service_port: 3930
    # flash_proxy_port: 20170
    # flash_proxy_status_port: 20292
    # metrics_port: 8234
    # deploy_dir: deploy/tiflash-9000
    # data_dir: deploy/tiflash-9000/data
    # log_dir: deploy/tiflash-9000/log
    # numa_node: "0,1"
    # # Config is used to overwrite the `server_configs.tiflash` values
    #  config:
    #    logger:
    #      level: "info"
    #  learner_config:
    #    log-level: "info"
  - host: 172.18.181.6

monitoring_servers:
  - host: 172.18.180.46

grafana_servers:
  - host: 172.18.180.46

alertmanager_servers:
  - host: 172.18.180.46

```

* * *

* * *

* * *

##### 部署集群

**通过 TiUP 进行集群部署可以使用密钥或者交互密码方式来进行安全认证：**

- 如果是密钥方式，可以通过 `-i` 或者 `--identity_file` 来指定密钥的路径；
- 如果是密码方式，无需添加其他参数，Enter 即可进入密码交互窗口。
- `tiup cluster deploy tidb-dev v4.0.0 ./topology.yaml --user root [-p] [-i /home/root/.ssh/gcp_rsa]`

```ruby
[tidb@test1 ~]$ tiup cluster deploy tidb-dev v4.0.0 ./topology.yaml --user root -p

......

Attention:
    1. If the topology is not what you expected, check your yaml file.
    1. Please confirm there is no port/directory conflicts in same host.
Do you want to continue? [y/N]:  y
Input SSH password: 输入 SSH密码

......

# 部署成功，请使用 tiup cluster start tidb-dev 命令启动集群
Deployed cluster `tidb-dev` successfully, you can start the cluster via `tiup cluster start tidb-dev`

```

* * *

###### 1\. 检查 TiUP 管理集群情况

```ruby
[tidb@test1 ~]$ tiup cluster list
Starting component `cluster`: /home/tidb/.tiup/components/cluster/v1.0.7/tiup-cluster list
Name       User  Version  Path                                                 PrivateKey
---- ---- ------- ---- ----------
tidb-dev  tidb  v4.0.0   /home/tidb/.tiup/storage/cluster/clusters/tidb-dev  /home/tidb/.tiup/storage/cluster/clusters/tidb-dev/ssh/id_rsa
[tidb@test1 ~]$
```

* * *

###### 2\. 检查 tidb-dev 集群情况

```ruby
[tidb@test1 ~]$ tiup cluster display tidb-dev
Starting component `cluster`: /home/tidb/.tiup/components/cluster/v1.0.7/tiup-cluster display tidb-dev
TiDB Cluster: tidb-dev
TiDB Version: v4.0.0
ID                    Role          Host            Ports        Status        Data Dir                                  Deploy Dir
-- ---- ---- ----- ------ -------- ----------
172.18.180.46:9093    alertmanager  172.18.180.46   9093/9094    inactive      /home/tidb/tidb-data/alertmanager-9093    /home/tidb/tidb-deploy/alertmanager-9093
172.18.180.46:3000    grafana       172.18.180.46   3000         inactive      - /home/tidb/tidb-deploy/grafana-3000
172.18.180.47:2379    pd            172.18.180.47   2379/2380    Down          /home/tidb/tidb-data/pd-2379              /home/tidb/tidb-deploy/pd-2379
172.18.180.48:2379    pd            172.18.180.48   2379/2380    Down          /home/tidb/tidb-data/pd-2379              /home/tidb/tidb-deploy/pd-2379
172.18.181.18:2379    pd            172.18.181.18   2379/2380    Down          /home/tidb/tidb-data/pd-2379              /home/tidb/tidb-deploy/pd-2379
172.18.180.46:9090    prometheus    172.18.180.46   9090         inactive      /home/tidb/tidb-data/prometheus-9090      /home/tidb/tidb-deploy/prometheus-9090
172.18.180.47:4000    tidb          172.18.180.47   4000/10080   Down          - /home/tidb/tidb-deploy/tidb-4000
172.18.180.48:4000    tidb          172.18.180.48   4000/10080   Down          - /home/tidb/tidb-deploy/tidb-4000
172.18.181.18:4000    tidb          172.18.181.18   4000/10080   Down          - /home/tidb/tidb-deploy/tidb-4000
172.18.180.47:20160   tikv          172.18.180.47   20160/20180  Down          /home/tidb/tidb-data/tikv-20160           /home/tidb/tidb-deploy/tikv-20160
172.18.180.48:20160   tikv          172.18.180.48   20160/20180  Down          /home/tidb/tidb-data/tikv-20160           /home/tidb/tidb-deploy/tikv-20160
172.18.181.18:20160   tikv          172.18.181.18   20160/20180  Down          /home/tidb/tidb-data/tikv-20160           /home/tidb/tidb-deploy/tikv-20160
[tidb@test1 ~]$
```

预期输出包括 tidb-dev 集群中实例 ID、角色、主机、监听端口和状态（由于还未启动，所以状态为 `Down/inactive`）、目录信息。

* * *

###### 3\. 启动集群

```ruby
[tidb@test1 ~]$ tiup cluster start tidb-dev
......
Started cluster `tidb-dev` successfully
[tidb@test1 ~]$
```

* * *

###### 4\. 再次 查看集群情况

```ruby
[tidb@test1 ~]$ tiup cluster display tidb-dev
Starting component `cluster`: /home/tidb/.tiup/components/cluster/v1.0.7/tiup-cluster display tidb-dev
TiDB Cluster: tidb-dev
TiDB Version: v4.0.0
ID                    Role          Host            Ports        Status        Data Dir                                  Deploy Dir
-- ---- ---- ----- ------ -------- ----------
172.18.180.46:9093    alertmanager  172.18.180.46   9093/9094    Up            /home/tidb/tidb-data/alertmanager-9093    /home/tidb/tidb-deploy/alertmanager-9093
172.18.180.46:3000    grafana       172.18.180.46   3000         Up            - /home/tidb/tidb-deploy/grafana-3000
172.18.180.47:2379    pd            172.18.180.47   2379/2380    Up            /home/tidb/tidb-data/pd-2379              /home/tidb/tidb-deploy/pd-2379
172.18.180.48:2379    pd            172.18.180.48   2379/2380    Up|L          /home/tidb/tidb-data/pd-2379              /home/tidb/tidb-deploy/pd-2379
172.18.181.18:2379    pd            172.18.181.18   2379/2380    Up            /home/tidb/tidb-data/pd-2379              /home/tidb/tidb-deploy/pd-2379
172.18.180.46:9090    prometheus    172.18.180.46   9090         Up            /home/tidb/tidb-data/prometheus-9090      /home/tidb/tidb-deploy/prometheus-9090
172.18.180.47:4000    tidb          172.18.180.47   4000/10080   Up            - /home/tidb/tidb-deploy/tidb-4000
172.18.180.48:4000    tidb          172.18.180.48   4000/10080   Up            - /home/tidb/tidb-deploy/tidb-4000
172.18.181.18:4000    tidb          172.18.181.18   4000/10080   Up            - /home/tidb/tidb-deploy/tidb-4000
172.18.180.47:20160   tikv          172.18.180.47   20160/20180  Up            /home/tidb/tidb-data/tikv-20160           /home/tidb/tidb-deploy/tikv-20160
172.18.180.48:20160   tikv          172.18.180.48   20160/20180  Up            /home/tidb/tidb-data/tikv-20160           /home/tidb/tidb-deploy/tikv-20160
172.18.181.18:20160   tikv          172.18.181.18   20160/20180  Up            /home/tidb/tidb-data/tikv-20160           /home/tidb/tidb-deploy/tikv-20160
[tidb@test1 ~]$
```

* * *

* * *

* * *

###### 常用命令

```ruby
# 手动启动指定节点
[tidb@test1 ~]$ tiup cluster start tidb-dev -R grafana

# 手动停止集群
[tidb@test1 ~]$ tiup cluster stop tidb-dev

# 销毁集群
[tidb@test1 ~]$ tiup cluster destroy tidb-dev

# 重新加载配置文件
[tidb@test1 ~]$ tiup cluster reload tidb-dev

# 重新加载配置文件 以 IP：端口的方式 指定节点
[tidb@test1 ~]$ tiup cluster reload tidb-dev -N ip:port
# 或 以 节点名称的方式
[tidb@test1 ~]$ tiup cluster reload tidb-dev -R tidb,tikv
```

* * *

* * *

* * *

###### 访问 dashboard

`http://PD_IP:2379/dashboard` http://172.18.181.18:2379/dashboard 用户名：root 密码：数据库root密码 (默认无)

* * *

###### 访问 grafana

`http://TiDB_Server_IP:3000` http://172.18.180.46:3000 用户名：admin 密码：admin

* * *

* * *

* * *

###### 修改数据库密码

```sql
mysql root@172.18.180.48:(none)> ALTER USER 'root'@'%' IDENTIFIED BY 'eric&123';
You're about to run a destructive command.
Do you want to proceed? (y/n): y
Your call!
Query OK, 0 rows affected
Time: 0.061s
mysql root@172.18.180.48:(none)>
```

* * *

* * *

* * *

##### 扩容 TiDB/TiKV/PD 节点

###### 创建扩容文件

```ruby
[tidb@test1 ~]$ cat > scale-out.yaml << ERIC
tidb_servers:
  - host: 172.18.181.57
ERIC
```

###### 执行扩容

**tiup cluster scale-out `<cluster-name>` scale-out.yaml**

```ruby
[tidb@test1 ~]$ tiup cluster scale-out tidb-dev scale-out.yaml
```

###### 更新监控

```ruby
[tidb@test1 ~]$ tiup cluster reload tidb-dev -R prometheus
```

* * *

##### 缩容 TiDB/TiKV/PD 节点

###### 查看集群信息

**tiup cluster display `<cluster-name>`**

```ruby
[tidb@test1 ~]$ tiup cluster display tidb-dev
Starting component `cluster`: /home/tidb/.tiup/components/cluster/v1.0.7/tiup-cluster display tidb-dev
TiDB Cluster: tidb-dev
TiDB Version: v4.0.0
ID                    Role          Host            Ports                            Status     Data Dir                                Deploy Dir
-- ---- ---- ----- ------ -------- ----------
172.18.180.58:9093    alertmanager  172.18.180.58   9093/9094                        Up         /home/tidb/tidb-data/alertmanager-9093  /home/tidb/tidb-deploy/alertmanager-9093
172.18.180.58:3000    grafana       172.18.180.58   3000                             Up         - /home/tidb/tidb-deploy/grafana-3000
172.18.180.58:2379    pd            172.18.180.58   2379/2380                        Up|L       /home/tidb/tidb-data/pd-2379            /home/tidb/tidb-deploy/pd-2379
172.18.180.59:2379    pd            172.18.180.59   2379/2380                        Up         /home/tidb/tidb-data/pd-2379            /home/tidb/tidb-deploy/pd-2379
172.18.181.57:2379    pd            172.18.181.57   2379/2380                        Up         /home/tidb/tidb-data/pd-2379            /home/tidb/tidb-deploy/pd-2379
172.18.180.58:9090    prometheus    172.18.180.58   9090                             Up         /home/tidb/tidb-data/prometheus-9090    /home/tidb/tidb-deploy/prometheus-9090
172.18.180.59:4000    tidb          172.18.180.59   4000/10080                       Up         - /home/tidb/tidb-deploy/tidb-4000
172.18.181.57:4000    tidb          172.18.181.57   4000/10080                       Up         - deploy/tidb-4000
172.18.181.6:9000     tiflash       172.18.181.6    9000/8123/3930/20170/20292/8234  Up         /home/tidb/tidb-data/tiflash-9000       /home/tidb/tidb-deploy/tiflash-9000
172.18.192.34:20160   tikv          172.18.192.34   20160/20180                      Up         /home/tidb/tidb-data/tikv-20160         /home/tidb/tidb-deploy/tikv-20160
172.18.192.35:20160   tikv          172.18.192.35   20160/20180                      Up         /home/tidb/tidb-data/tikv-20160         /home/tidb/tidb-deploy/tikv-20160
172.18.192.36:20160   tikv          172.18.192.36   20160/20180                      Up         /home/tidb/tidb-data/tikv-20160         /home/tidb/tidb-deploy/tikv-20160
[tidb@test1 ~]$

```

###### 执行缩容

**tiup cluster scale-in `<cluster-name>` -N 172.18.180.59:4000**

```ruby
[tidb@test1 ~]$ tiup cluster scale-in tidb-dev -N 172.18.180.59:4000
```

###### 更新监控

```ruby
[tidb@test1 ~]$ tiup cluster reload tidb-dev -R prometheus
```

* * *

###### [可能要修改的 配置文件](http://www.dev-share.top/2020/05/22/tidb-4-0-%E5%8F%AF%E8%83%BD%E8%A6%81%E4%BF%AE%E6%94%B9%E7%9A%84-%E9%85%8D%E7%BD%AE%E6%96%87%E4%BB%B6/ "可能要修改的 配置文件")

* * *

* * *

* * *
