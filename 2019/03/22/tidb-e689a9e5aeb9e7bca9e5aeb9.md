---
title: 'TiDB 扩容缩容'
date: '2019-03-22T01:00:35+00:00'
status: publish
permalink: /2019/03/22/tidb-%e6%89%a9%e5%ae%b9%e7%bc%a9%e5%ae%b9
author: 毛巳煜
excerpt: ''
type: post
id: 3508
category:
    - TiDB
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
#### TiDB 扩容缩容

[官网教程](https://pingcap.com/docs-cn/v3.0/how-to/scale/with-ansible/ "官网教程")  
[官网隐藏教程](https://pingcap.com/docs-cn/v3.0/how-to/scale/horizontally/#%E5%8A%A8%E6%80%81%E5%88%A0%E9%99%A4%E8%8A%82%E7%82%B9-1 "官网隐藏教程")

##### 检测TiDB-servers运行情况

```ruby
[tidb@dev10 tidb-ansible]$ ansible -i inventory.ini tidb_servers -m shell -a "curl http://{{ ansible_host }}:{{ tidb_status_port }}/status"

```

`TiDB 集群可以在不影响线上服务的情况下进行扩容和缩容。以下缩容示例中，被移除的节点没有混合部署其他服务；如果混合部署了其他服务，不能按如下操作。`

- - - - - -

**[tikv缩容问题](https://asktug.com/t/tidb-3-2-tikv/609 "tikv缩容问题")**  
**tikv默认`最少3个节点`，不能从`3`节点缩容，tikv节点由`3`到`2`节点缩容，节点不会变成`tombstone`状态。此时需要将下线节点的状态改成`up`，如测试缩容步骤，建议先扩容至`4`节点，再进行缩容操作。**  
**TiKV`扩容缩容可以同时进行`，缩容操作后需要等待 TiKV 状态变成`tombstone`后，在做停服下线操作**

#### 扩容 TiKV 节点

- - - - - -

- - - - - -

**注意：**  
 单机多KV 与 单机间单KV 扩容缩容的区别就是 `指定IP` 还是指定 `IP的别名`  
**例如：**

```yaml
[tikv_servers]
TiKV1-1 ansible_host=172.160.180.52 deploy_dir=/home/tidb/data1/deploy tikv_port=20171 tikv_status_port=20181 labels="host=tikv1"
TiKV1-2 ansible_host=172.160.180.52 deploy_dir=/home/tidb/data2/deploy tikv_port=20172 tikv_status_port=20182 labels="host=tikv1"
TiKV1-3 ansible_host=172.160.180.52 deploy_dir=/home/tidb/data3/deploy tikv_port=20173 tikv_status_port=20183 labels="host=tikv1"


```

**单机`多`KV**使用命令： `ansible-playbook *.yml -l TiKV1-3`  
 **如果是修改单台 tikv 节点的配置，参考步骤如下：**  
 **1**. 单独修改 `TiKV1-1` 的配置文件到最新配置，不要 tikv 节点的修改模板文件。如果修改了 模板文件，那么所有的 tikv 节点需要滚动升级  
 **2**. `ansible-playbook stop.yml -l TiKV1-1` （因为改服务器指定了别名，所以建议使用别名）  
 **3**. `ansible-playbook start.yml -l TiKV1-1` （因为改服务器指定了别名，所以建议使用别名）

**单机`单`KV**使用命令： `ansible-playbook *.yml -l 172.160.180.52`

- - - - - -

- - - - - -

###### 1.编辑 inventory.ini 文件

```ruby
[tidb@dev10 tidb-ansible]$ vim inventory.ini
## TiDB Cluster Part
[tidb_servers]
172.160.180.33
172.160.180.34

[pd_servers]
172.160.180.33
172.160.180.34
172.160.180.35

### step 1 将节点机IP追加到 [tikv_servers] 后面
[tikv_servers]
172.160.180.35
172.160.180.36
172.160.180.37
172.160.180.51
# 加入目标机
172.160.180.52
172.160.180.53

### step 2 将节点机IP追加到 [monitored_servers] 后面，告诉普罗米修斯要监控它
# node_exporter and blackbox_exporter servers
[monitored_servers]
172.160.180.33
172.160.180.34
172.160.180.35
172.160.180.36
172.160.180.37
172.160.180.51
# 加入目标机
172.160.180.52
172.160.180.53

[spark_master]

[spark_slaves]

[monitoring_servers]
172.160.180.33

[grafana_servers]
172.160.180.33

[alertmanager_servers]
172.160.180.33


```

###### 2.配置添加 集群 hosts

```ruby
[tidb@dev10 tidb-ansible]$ vim hosts.ini
[servers]
172.160.180.33
172.160.180.34
172.160.180.35
172.160.180.36
172.160.180.37
172.160.180.51
# 加入目标机
172.160.180.52
172.160.180.53

[all:vars]
username = tidb
ntp_server = pool.ntp.org

```

###### 3.清空tikv缓存(**如果之前没安装，就跳过此步**)

```ruby
[tidb@dev10 tidb-ansible]<span class="katex math inline">ansible-playbook unsafe_cleanup.yml --tags=tikv -l 172.160.180.52,172.160.180.53
[tidb@dev10 tidb-ansible]</span>
# 物理删除节点机的缓存文件
[tidb@dev17 tidb-ansible]<span class="katex math inline">rm -rf /home/tidb/deploy/data/
[tidb@dev18 tidb-ansible]</span> rm -rf /home/tidb/deploy/data/

```

###### 4.配置中控机与新目标机器之间的 ssh 互信（如果已经配置，跳过此步）

```ruby
[tidb@dev10 tidb-ansible]$ ansible-playbook -i hosts.ini create_users.yml -u root -k

```

###### 5.配置时间同步

```ruby
[tidb@dev10 tidb-ansible]$ ansible-playbook -i hosts.ini deploy_ntp.yml -u tidb -b

```

###### 6.初始化新增节点 并跳过磁盘检查

- 172.160.180.52
- 172.160.180.53
- `ansible-playbook bootstrap.yml -l 目标机IP --extra-vars "dev_mode=True"`

```ruby
[tidb@dev10 tidb-ansible]$ ansible-playbook bootstrap.yml -l 172.160.180.52,172.160.180.53 --extra-vars "dev_mode=True"
......
Congrats! All goes well. :-)

```

###### 7.部署新增节点

```ruby
[tidb@dev10 tidb-ansible]$ ansible-playbook deploy.yml -l 172.160.180.52,172.160.180.53
......
Congrats! All goes well. :-)

```

###### 8.启动新节点服务

```ruby
[tidb@dev10 tidb-ansible]$ ansible-playbook start.yml -l 172.160.180.52,172.160.180.53
......
Congrats! All goes well. :-)

```

###### 9.更新 Prometheus 监控

```ruby
[tidb@dev10 tidb-ansible]$ ansible-playbook rolling_update_monitor.yml

```

##### 监控

监控地址: http://172.160.180.33:3000/login  
User: admin  
Password: admin

节点上报状态: http://172.16.0.1:9091

- - - - - -

- - - - - -

- - - - - -

#### 缩容 TiKV 节点

- 删除 dev15 172.160.180.37 节点
- 通过如下命令来查询 所有节点的详细配置信息
- `/home/tidb/tidb-ansible/resources/bin/pd-ctl -u "http://PD的IP地址:2379" -d store`

```ruby
[tidb@dev10 tidb-ansible]<span class="katex math inline">/home/tidb/tidb-ansible/resources/bin/pd-ctl -u "http://172.160.180.33:2379" -d store
{
  "count": 6,
  "stores": [
    {
      "store": {
        "id": 1,
        "address": "172.160.180.37:20160",
        "version": "2.1.4",
        "state_name": "Up" # 在线
      },
      "status": {
        ......
      }
    },
......
[tidb@dev10 tidb-ansible]</span>

```

###### 1.根据 store id 将服务下线

`下线需要一定时间，下线节点的状态变为 state_name: Tombstone 就说明下线成功了`

```ruby
[tidb@dev10 tidb-ansible]<span class="katex math inline">/home/tidb/tidb-ansible/resources/bin/pd-ctl -u "http://172.160.180.33:2379" -d store delete 1
Success!
[tidb@dev10 tidb-ansible]</span>

```

###### 2.查看状态

```ruby
[tidb@dev10 tidb-ansible]<span class="katex math inline">/home/tidb/tidb-ansible/resources/bin/pd-ctl -u "http://172.160.180.33:2379" -d store 1
{
  "store": {
    "id": 1,
    "address": "172.160.180.37:20160",
    "state": 1,
    "version": "2.1.4",
    "state_name": "Offline" # 这个 store 正在将其中的 Region 转移到其他节点，此时这个 store 仍在服务中
  },
  "status": {
    ......
  }
}

[tidb@dev10 tidb-ansible]</span>
[tidb@dev10 tidb-ansible]<span class="katex math inline">[tidb@dev10 tidb-ansible]</span>
[tidb@dev10 tidb-ansible]<span class="katex math inline">/home/tidb/tidb-ansible/resources/bin/pd-ctl -u "http://172.160.180.33:2379" -d store 1
{
  "store": {
    "id": 1,
    "address": "172.160.180.37:20160",
    "state": 1,
    "version": "2.1.4",
    "state_name": "Tombstone" # 这个 store 已经完成下线，此时 store 上已经没有数据，可以关闭实例
  },
  "status": {
    ......
  }
}

[tidb@dev10 tidb-ansible]</span>

```

##### 2.1store 的状态说明：

- **Up**：这个 store 正常服务
- **Disconnected**：当前没有检测到这个 store 的心跳，可能是故障或网络连接中断
- **Down**：超过一小时（可通过 max-down-time 配置）没有收到 store 心跳，此时 PD 会为这个 store 上的数据添加副本
- **Offline**：这个 store 正在将其中的 Region 转移到其他节点，此时这个 store 仍在服务中
- **Tombstone**：这个 store 已经完成下线，此时 store 上已经没有数据，可以关闭实例

###### 3.下线成功后，停止服务 (`停服要慎重，下线完成后在进行停服`)

```ruby
# 关掉节点机器上所有的服务模块。根据实际情况 二选一
[tidb@dev10 tidb-ansible]<span class="katex math inline">ansible-playbook stop.yml -l 172.160.180.37

# 只关掉节点机器上的TiKV，不包括监控模块。根据实际情况 二选一
[tidb@dev10 tidb-ansible]</span> ansible-playbook stop.yml --tags=tikv -l 172.160.180.37

```

###### 4.编辑 inventory.ini 文件，移除节点信息

```ruby
 ## TiDB Cluster Part
[tidb_servers]
172.160.180.33
172.160.180.34

# 下线成功后在移除这个KV节点
[tikv_servers]
172.160.180.35
172.160.180.36
# 172.160.180.37
172.160.180.51
172.160.180.52
172.160.180.53
......

# 下线成功后在移除这个监控节点，告诉普罗米修斯不用在监控了
[monitored_servers]
172.160.180.35
172.160.180.36
# 172.160.180.37
172.160.180.51
172.160.180.52
172.160.180.53
......

```

###### 5.更新 Prometheus 监控

```ruby
[tidb@dev10 tidb-ansible]<span class="katex math inline">ansible-playbook rolling_update_monitor.yml
......
Congrats! All goes well. :-)
[tidb@dev10 tidb-ansible]</span>

```

###### 6.清空TiKV缓存

```ruby
[tidb@dev10 tidb-ansible]$ ansible-playbook unsafe_cleanup.yml --tags=tikv -l 172.160.180.37

```

打开浏览器访问监控平台：http://172.160.180.33:3000，监控整个集群的状态

- - - - - -

- - - - - -

- - - - - -

#### 扩容 PD 节点

**目标：** 加入新节点 172.160.181.18

1.编辑 inventory.ini 文件，加入节点信息

2.清空pd缓存(**如果之前没安装，就跳过此步**)

```ruby
[tidb@test1 tidb-ansible]$ ansible-playbook unsafe_cleanup.yml --tags=pd -l 172.160.181.18

```

3.重新部署

```ruby
[tidb@test1 tidb-ansible]<span class="katex math inline">ansible-playbook bootstrap.yml -l 172.160.181.18 --extra-vars "dev_mode=True"

Congrats! All goes well. :-)
[tidb@test1 tidb-ansible]</span>
[tidb@test1 tidb-ansible]<span class="katex math inline">[tidb@test1 tidb-ansible]</span>
[tidb@test1 tidb-ansible]<span class="katex math inline">[tidb@test1 tidb-ansible]</span> ansible-playbook deploy.yml --tags=pd -l 172.160.181.18

Congrats! All goes well. :-)
[tidb@test1 tidb-ansible]$

```

4.进入节点机 test4, 修改节点机配置

- 删除 `--initial-cluster="......"` 不可以使用注释，要直接删除
- 加入 `--join="......"` IP地址是现有PD集群中的任意一个即可

```sh
# 例子
......
exec bin/pd-server \
    --name="pd_test4" \
    --client-urls="http://172.160.181.18:2379" \
    --advertise-client-urls="http://172.160.181.18:2379" \
    --peer-urls="http://172.160.181.18:2380" \
    --advertise-peer-urls="http://172.160.181.18:2380" \
    --data-dir="/home/tidb/deploy/data.pd" \
    --initial-cluster="pd_test1=http://172.160.180.46:2380,pd_test2=http://172.160.180.47:2380,pd_test3=http://172.160.180.48:2380,pd_test4=http://172.160.181.18:2380" \ # 删除这一行，不可以使用注释，要直接删除
    --join="http://172.160.180.48:2379" \  # 替换为这一行，IP地址是现有PD集群中的任意一个即可
    --config=conf/pd.toml \
    --log-file="/home/tidb/deploy/log/pd.log" 2>> "/home/tidb/deploy/log/pd_stderr.log"
......

```

```ruby
[tidb@test4 ~]<span class="katex math inline">vim /home/tidb/deploy/scripts/run_pd.sh
#!/bin/bash
set -e
ulimit -n 1000000

# WARNING: This file was auto-generated. Do not edit!
#          All your edit might be overwritten!
DEPLOY_DIR=/home/tidb/deploy

cd "</span>{DEPLOY_DIR}" || exit 1



exec bin/pd-server \
    --name="pd_test4" \
    --client-urls="http://172.160.181.18:2379" \
    --advertise-client-urls="http://172.160.181.18:2379" \
    --peer-urls="http://172.160.181.18:2380" \
    --advertise-peer-urls="http://172.160.181.18:2380" \
    --data-dir="/home/tidb/deploy/data.pd" \
    --join="http://172.160.180.48:2379" \
    --config=conf/pd.toml \
    --log-file="/home/tidb/deploy/log/pd.log" 2>> "/home/tidb/deploy/log/pd_stderr.log"

```

5.删除缓存节点机中的缓存数据(**如果之前没安装，就跳过此步**)

```ruby
# 删除缓存数据
[tidb@test4 ~]<span class="katex math inline">rm -rf /home/tidb/deploy/data.pd/
# 删除历史pd.log
[tidb@test4 ~]</span> rm -rf /home/tidb/deploy/log/pd*

```

6.启动pd

```ruby
[tidb@test4 ~]$ /home/tidb/deploy/scripts/start_pd.sh

```

7.进入主控机，查看PD节点是否成功加入

```ruby
[tidb@test1 tidb-ansible]$ /home/tidb/tidb-ansible/resources/bin/pd-ctl -u "http://172.160.180.46:2379" -d member

```

8.滚动升级整个集群

```ruby
[tidb@test1 tidb-ansible]$ ansible-playbook rolling_update.yml

```

9.启动PD

```ruby
[tidb@test1 tidb-ansible]$ ansible-playbook start.yml --tags=pd -l 172.160.181.18

```

10.更新监控

```ruby
[tidb@test1 tidb-ansible]$ ansible-playbook rolling_update_monitor.yml --tags=prometheus

```

- - - - - -

- - - - - -

- - - - - -

#### 缩容 PD 节点

**目标：** 移除 172.160.180.46机器上的 PD服务

1. 查看所有PD节点信息

```ruby
[tidb@test1 tidb-ansible]$ /home/tidb/tidb-ansible/resources/bin/pd-ctl -u "http://172.160.180.48:2379" -d member

```

2. 删除要移除的节点

```ruby
[tidb@test1 tidb-ansible]<span class="katex math inline">/home/tidb/tidb-ansible/resources/bin/pd-ctl -u "http://172.160.180.48:2379" -d member delete name pd_test1
Success!
[tidb@test1 tidb-ansible]</span>

```

3. 停止PD节点服务

```ruby
[tidb@test1 tidb-ansible]$ ansible-playbook stop.yml --tags=pd -l 172.160.180.46

```

4. 编辑 inventory.ini 文件，移除节点信息
5. 滚动升级整个集群

```ruby
[tidb@test1 tidb-ansible]$ ansible-playbook rolling_update.yml

```

6. 更新监控

```ruby
[tidb@test1 tidb-ansible]$ ansible-playbook rolling_update_monitor.yml --tags=prometheus

```