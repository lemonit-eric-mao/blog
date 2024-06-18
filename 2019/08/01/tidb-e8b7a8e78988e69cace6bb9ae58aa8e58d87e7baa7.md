---
title: 'TiDB 跨版本滚动升级'
date: '2019-08-01T11:28:14+00:00'
status: publish
permalink: /2019/08/01/tidb-%e8%b7%a8%e7%89%88%e6%9c%ac%e6%bb%9a%e5%8a%a8%e5%8d%87%e7%ba%a7
author: 毛巳煜
excerpt: ''
type: post
id: 4980
category:
    - TiDB
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
[跳转到开源社区](https://www.oschina.net/news/107836/tidb-3-0-ga "跳转到开源社区")

TiDB 3.0 版本显著提升了大规模集群的稳定性，集群支持 150+ 存储节点，300+TB 存储容量长期稳定运行。易用性方面引入大量降低用户运维成本的优化，包括引入 Information\_Schema 中的多个实用系统视图、EXPLAIN ANALYZE、SQL Trace 等。在性能方面，特别是 OLTP 性能方面，3.0 比 2.1 也有大幅提升，其中 TPC-C 性能提升约 4.5 倍，Sysbench 性能提升约 1.5 倍，OLAP 方面，TPC-H 50G Q15 因实现 View 可以执行，至此 TPC-H 22 个 Query 均可正常运行。新功能方面增加了窗口函数、视图（实验特性）、分区表、插件系统、悲观锁（实验特性）。

- - - - - -

- - - - - -

**`注意：`一定要使用 python2.7.5 安装TiDB 不能使用 python3**
----------------------------------------------

- - - - - -

- - - - - -

##### `注意：升级前要做好数据库备份`

[备份数据库](https://www.lemonit.cn/2019/07/18/tidb-%E5%A4%87%E4%BB%BD-%E6%81%A2%E5%A4%8D%E6%95%B0%E6%8D%AE/ "备份数据库")

##### TiDB 2.0.x 升级到 TiDB 3.0

在中控机上安装系统依赖包  
以 root 用户登录中控机

如果中控机是 CentOS 7 系统，执行以下命令：

```ruby
[root@dev10 tidb]# yum -y install epel-release git curl sshpass
[root@dev10 tidb]# yum -y install python2-pip

```

以 tidb 用户登录中控机并进入 /home/tidb 目录，备份 TiDB 2.0 版本或 TiDB 2.1 版本的 tidb-ansible 文件夹：

```ruby
[root@dev10 tidb]# su - tidb
上一次登录：三 7月 31 14:19:28 CST 2019pts/1 上
[tidb@dev10 ~]<span class="katex math inline">[tidb@dev10 ~]</span> mv tidb-ansible tidb-ansible-bak

```

下载 TiDB 3.0 版本对应 tag 的 tidb-ansible 下载 TiDB-Ansible，默认的文件夹名称为 tidb-ansible  
`git clone -b $tag https://github.com/pingcap/tidb-ansible.git`

```
注意：
v3.0.1有严重bug, 创建表以后, 不能修改列, 异常信息如下：
mysql> ALTER TABLE 表名 MODIFY COLUMN 列名
1105 - unsupported modify column %!s(ast.CloumnOptionType=12)
v3.0.2修复了这个严重bug

```

```ruby
[tidb@dev10 ~]<span class="katex math inline">git clone -b v3.0.2 https://github.com/pingcap/tidb-ansible.git
正克隆到 'tidb-ansible'...
......
[tidb@dev10 ~]</span>

```

升级 tidb-ansible

```ruby
[tidb@dev10 ~]<span class="katex math inline">[tidb@dev10 ~]</span> cd /home/tidb/tidb-ansible
[tidb@dev10 tidb-ansible]<span class="katex math inline">[tidb@dev10 tidb-ansible]</span> sudo pip install -r ./requirements.txt
Collecting ansible==2.7.11 (from -r ./requirements.txt (line 1))
  Downloading https://files.pythonhosted.org/packages/2a/0a/52a0daaf3f7f8fecb3ea3fe866100ae1f9a9462403a0aaaebedcfbbbdba4/ansible-2.7.11.tar.gz (11.9MB)
......
Installing collected packages: ansible
  Found existing installation: ansible 2.6.18
    Uninstalling ansible-2.6.18:
      Successfully uninstalled ansible-2.6.18
  Running setup.py install for ansible ... done
Successfully installed ansible-2.7.11
WARNING: You are using pip version 19.1.1, however version 19.2.1 is available.
You should consider upgrading via the 'pip install --upgrade pip' command.

[tidb@dev10 tidb-ansible]$

```

安装完成后，可通过以下命令查看版本

```ruby
[tidb@dev10 tidb-ansible]<span class="katex math inline">ansible --version
ansible 2.7.11
[tidb@dev10 tidb-ansible]</span>
[tidb@dev10 tidb-ansible]<span class="katex math inline">[tidb@dev10 tidb-ansible]</span> pip show jinja2
Name: Jinja2
Version: 2.10.1
[tidb@dev10 tidb-ansible]<span class="katex math inline">[tidb@dev10 tidb-ansible]</span>
[tidb@dev10 tidb-ansible]<span class="katex math inline">pip show jmespath
Name: jmespath
Version: 0.9.0
[tidb@dev10 tidb-ansible]</span>

```

```
注意：
在升级的过程中不要执行 DDL 请求，否则可能会出现行为未定义的问题。

注意：
请务必按以上文档安装 Ansible 及其依赖。
确认 Jinja2 版本是否正确，否则启动 Grafana 时会报错。
确认 jmespath 版本是否正确，否则滚动升级 TiKV 时会报错。

```

- - - - - -

- - - - - -

#### 编辑 inventory.ini 文件和配置文件

```
以 tidb 用户登录中控机并进入 /home/tidb/tidb-ansible 目录。

```

##### 编辑 inventory.ini 文件

```
编辑 inventory.ini 文件，IP 信息参照备份文件 /home/tidb/tidb-ansible-bak/inventory.ini。

```

以下变量配置，需要重点确认，变量含义可参考 [inventory.ini 变量调整](https://pingcap.com/docs-cn/v3.0/how-to/deploy/orchestrated/ansible/#%E5%85%B6%E4%BB%96%E5%8F%98%E9%87%8F%E8%B0%83%E6%95%B4 "inventory.ini 变量调整")

1. 请确认 ansible\_user 配置的是普通用户。为统一权限管理，不再支持使用 root 用户远程安装。默认配置中使用 tidb 用户作为 SSH 远程用户及程序运行用户。

```
## Connection
# ssh via normal user
ansible_user = tidb

```

2. process\_supervision 变量请与之前版本保持一致，默认推荐使用 systemd

```
# process supervision, [systemd, supervise]
process_supervision = systemd

```

如需变更，可参考 [如何调整进程监管方式从 supervise 到 systemd](https://pingcap.com/docs-cn/v3.0/how-to/deploy/orchestrated/ansible/#%E5%A6%82%E4%BD%95%E8%B0%83%E6%95%B4%E8%BF%9B%E7%A8%8B%E7%9B%91%E7%AE%A1%E6%96%B9%E5%BC%8F%E4%BB%8E-supervise-%E5%88%B0-systemd "如何调整进程监管方式从 supervise 到 systemd")，先使用备份 /home/tidb/tidb-ansible-bak/ 分支变更进程监管方式再升级。

##### 编辑 TiDB 集群组件配置文件

`如之前自定义过 TiDB 集群组件配置文件，请参照备份文件修改 /home/tidb/tidb-ansible/conf 下对应配置文件。`

**注意以下参数变更：**

- TiKV 配置中 end-point-concurrency 变更为 high-concurrency、normal-concurrency 和 low-concurrency 三个参数

```
readpool:
  coprocessor:
    # Notice: if CPU_NUM > 8, default thread pool size for coprocessors
    # will be set to CPU_NUM * 0.8.
    # high-concurrency: 8
    # normal-concurrency: 8
    # low-concurrency: 8

```

```
注意：
单机多 TiKV 实例（进程）情况下，需要修改这三个参数。
推荐设置：TiKV 实例数量 * 参数值 = CPU 核心数量 * 0.8

```

- TiKV 配置中不同 CF 中的 block-cache-size 参数变更为 block-cache

```
storage:
  block-cache:
    capacity: "1GB"

```

```
注意：
单机多 TiKV 实例（进程）情况下，需要修改 capacity 参数。
推荐设置：capacity = (MEM_TOTAL * 0.5 / TiKV 实例数量)

```

- - - - - -

- - - - - -

#### 下载 TiDB 3.0 binary 到中控机

```
确认 `tidb-ansible/inventory.ini` 文件中 `tidb_version = v3.0.2`，然后执行以下命令下载 TiDB 3.0 binary 到中控机。

```

```ruby
[tidb@dev10 tidb-ansible]<span class="katex math inline">ansible-playbook local_prepare.yml
......
Congrats! All goes well. :-)
[tidb@dev10 tidb-ansible]</span>

```

- - - - - -

- - - - - -

#### 滚动升级 TiDB 集群组件

```
注意：
为优化 TiDB 集群组件的运维管理，TiDB 3.0 版本对 systemd 模式下的 PD service 名称进行了调整。如当前版本小于 TiDB 3.0 版本，滚动升级到 TiDB 3.0 版本集群组件的操作略有不同，注意升级前后 process_supervision 参数配置须保持一致。

```

**确认1** 如果 `tidb-ansible/inventory.ini` 文件中 `process_supervision`变量使用默认的 **`systemd`** 参数，则通过 `excessive_rolling_update.yml` 滚动升级 TiDB 集群。

```ruby
[tidb@dev10 tidb-ansible]<span class="katex math inline">ansible-playbook excessive_rolling_update.yml
......
excessive_rolling_update.ymlCongrats! All goes well. :-)
[tidb@dev10 tidb-ansible]</span>

```

`经过实际检验，2.0升级到3.0升级过程中，会有两次断开连接，因此跨版本升级不建议在数据库使用频繁的时间段操作。每次间隔时间在10秒左右`

- - - - - -

**确认2** 如果 `tidb-ansible/inventory.ini` 文件中 `process_supervision`变量使用 **`supervise`** 参数，则通过 `rolling_update.yml` 滚动升级 TiDB 集群。

```ruby
[tidb@dev10 tidb-ansible]$ ansible-playbook rolling_update.yml

```

```
注意：
如当前版本大于或等于 TiDB 3.0 版本，则滚动升级及日常滚动重启 TiDB 集群仍然使用 rolling_update.yml 操作。

```

- - - - - -

- - - - - -

#### 滚动升级 TiDB 监控组件

```ruby
[tidb@dev10 tidb-ansible]<span class="katex math inline">ansible-playbook rolling_update_monitor.yml
......
Congrats! All goes well. :-)
[tidb@dev10 tidb-ansible]</span>

```

`经过实际检验，升级过程中，会有很短暂的断开连接，间隔时间在10秒左右`

**因为集群数量较少，共3台测试节点机，全部升级过程大概15分钟左右**