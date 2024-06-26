---
title: "TiDB 小版本滚动升级"
date: "2019-09-23"
categories: 
  - "tidb"
---

## **`注意：`一定要使用 python2.7.5 安装TiDB 不能使用 python3**

##### **TiDB 3.0.2** 升级到 **`TiDB 3.0.3`**

* * *

* * *

##### `注意：升级前要做好数据库备份`

[备份数据库](https://www.lemonit.cn/2019/07/18/tidb-%E5%A4%87%E4%BB%BD-%E6%81%A2%E5%A4%8D%E6%95%B0%E6%8D%AE/ "备份数据库")

##### 1.备份 tidb-ansible

```ruby
[root@dev10 tidb]# su - tidb
上一次登录：三 7月 31 14:19:28 CST 2019pts/1 上
[tidb@dev10 tidb]$
[tidb@dev10 tidb]$ mv tidb-ansible tidb-ansible-bak-3.0.2
```

下载 TiDB 3.0.x 版本对应 tag 的 tidb-ansible 下载 TiDB-Ansible，默认的文件夹名称为 tidb-ansible `git clone -b $tag https://github.com/pingcap/tidb-ansible.git`

```
注意：
v3.0.1有严重bug, 创建表以后, 不能修改列, 异常信息如下：
mysql> ALTER TABLE 表名 MODIFY COLUMN 列名
1105 - unsupported modify column %!s(ast.CloumnOptionType=12)
v3.0.2修复了这个严重bug
```

```ruby
[tidb@dev10 ~]$ git clone -b v3.0.3 https://github.com/pingcap/tidb-ansible.git
正克隆到 'tidb-ansible'...
......
[tidb@dev10 ~]$
```

升级 tidb-ansible

```ruby
[tidb@dev10 ~]$
[tidb@dev10 ~]$ cd /home/tidb/tidb-ansible
[tidb@dev10 tidb-ansible]$
[tidb@dev10 tidb-ansible]$ sudo pip install -r ./requirements.txt
[tidb@dev10 tidb-ansible]$
```

安装完成后，可通过以下命令查看版本

```ruby
[tidb@dev10 tidb-ansible]$ ansible --version
[tidb@dev10 tidb-ansible]$
[tidb@dev10 tidb-ansible]$ pip show jinja2
[tidb@dev10 tidb-ansible]$
[tidb@dev10 tidb-ansible]$ pip show jmespath
[tidb@dev10 tidb-ansible]$
```

```
注意：
在升级的过程中不要执行 DDL 请求，否则可能会出现行为未定义的问题。
请务必按以上文档安装 Ansible 及其依赖。
确认 Jinja2 版本是否正确，否则启动 Grafana 时会报错。
确认 jmespath 版本是否正确，否则滚动升级 TiKV 时会报错。
```

##### 2.编辑 inventory.ini 文件和配置文件

```
以 tidb 用户登录中控机并进入 /home/tidb/tidb-ansible 目录。
```

###### 2.1 请确认 ansible\_user 配置的是普通用户。

```
## Connection
# ssh via normal user
ansible_user = tidb
```

###### 2.2 process\_supervision 变量请与之前版本保持一致，默认推荐使用 systemd

```
# process supervision, [systemd, supervise]
process_supervision = systemd
```

##### 3.下载 TiDB 3.0.x binary 到中控机

```
确认 `tidb-ansible/inventory.ini` 文件中 `tidb_version = v3.0.3`，然后执行以下命令下载 TiDB 3.0.3 binary 到中控机。
```

```ruby
[tidb@dev10 tidb-ansible]$ ansible-playbook local_prepare.yml
......
Congrats! All goes well. :-)
[tidb@dev10 tidb-ansible]$
```

##### 4.滚动升级 TiDB 集群组件

```
注意：
为优化 TiDB 集群组件的运维管理，TiDB 3.0.x 版本对 systemd 模式下的 PD service 名称进行了调整。如当前版本小于 TiDB 3.0.x 版本，滚动升级到 TiDB 3.0.x 版本集群组件的操作略有不同，注意升级前后 process_supervision 参数配置须保持一致。
```

```ruby
[tidb@dev10 tidb-ansible]$ ansible-playbook rolling_update.yml
```

##### 5.滚动升级 TiDB 监控组件

```ruby
[tidb@dev10 tidb-ansible]$ ansible-playbook rolling_update_monitor.yml
......
Congrats! All goes well. :-)
[tidb@dev10 tidb-ansible]$
```

`经过实际检验，升级过程中，会有很短暂的断开连接，间隔时间在10秒左右`

**因为集群数量较少，共3台测试节点机，全部升级过程大概15分钟左右**
