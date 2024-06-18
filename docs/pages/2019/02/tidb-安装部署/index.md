---
title: "TiDB 安装部署"
date: "2019-02-22"
categories: 
  - "tidb"
---

##### [TiDB官方学习视频](https://university.pingcap.com/cc8cbf92456a427db87119e15203127d.shtml "TiDB官方学习视频")

* * *

### 安装部署

##### 据说 TiDB-Ansible坑较多，以下安装步骤严格遵循 《TiDB 软件部署建议》

https://www.pingcap.com/docs-cn/dev/how-to/deploy/hardware-recommendations/

```
TiDB 在 CentOS 7.3 的环境下进行过大量的测试，同时社区也有很多该操作系统部署的最佳实践，因此，建议使用 CentOS 7.3 以上的 Linux 操作系统来部署 TiDB。
```

* * *

* * *

## `注意事项`

**1.** **一定要使用 python2.7.X 安装TiDB 不能使用 python3**

* * *

**2.** 生产环境中的 TiDB 和 PD 可以部署和运行在同服务器上，如对性能和可靠性有更高的要求，应尽可能分开部署。生产环境强烈推荐使用更高的配置。

* * *

**3.** TiKV 硬盘大小配置建议 PCI-E SSD 不超过 2TB，普通 SSD 不超过 1.5TB。

* * *

**4.** TiKV 集群存在木桶原理，建议TiKV资源配置一致，以下举例几种情况:

- 现有TiKV集群`3台`，配置为`16核32G`，`单机单实例`部署； 现在加入一台8核16G机器，TiKV的整体处理性能会受到新加入的这台机器的影响
- 现有TiKV集群`3台`，配置为`16核32G`，`单机单实例`部署； 现在加入一台`32核64G`机器，这时TiKV集群所提升的性能，只是相当于又添加了一台`16核32G`的机器

* * *

**5.** TiKV 不建议使用混合部署，部署时最好全部是`单机单实例`或`单机多实例`； 单机多实例会打**label**, PD调度**leader**和 **region**会按照**host**来调度，最终`单机多实例`的物理机还是不能有效的使用资源；即使部署`单机单实例`时加上host也是不能有效的使用资源的。

* * *

**6.** TiDB对表的列数限制为**`512列`**

* * *

**7.** 内核需要4.5以上版本 **[内核升级](http://www.dev-share.top/2019/07/10/linux-%e7%b3%bb%e7%bb%9f%e5%86%85%e6%a0%b8%e5%8d%87%e7%ba%a7/ "内核升级")**

* * *

**8.** 关闭内网防火墙 `systemctl stop firewalld && systemctl disable firewalld && systemctl status firewalld`

* * *

* * *

* * *

* * *

* * *

* * *

## `可能需要调整的配置`

##### 调整单条SQL语句可使用的最大内存

###### conf/tidb.yml

```yml
global:

  # Only print a log when out of memory quota.
  # Valid options: ["log", "cancel"]
  # oom-action: "log"
  # 如果单条SQL语句使用内存超出 mem-quota-query 限制, 将返回异常
  # 超限会引发异常信息: **`Out Of Memory Quota!`**
  oom-action: "cancel"

  # 单条SQL语句使用内存限制
  # Set the memory quota for a query in bytes. Default: 32GB
  # mem-quota-query: 34359738368
  # 改为 1G
  mem-quota-query: 1073741824

  # 用于处理v3.0.7和以前版本升级中的兼容性问题(为了兼容联合索引长度超长的问题，这里改为4倍)
  # max-index-length is used to deal with compatibility issues from v3.0.7 and previous version upgrades. It can only be in [3072, 3072*4].
  # max-index-length: 3072
  max-index-length: 12288

log:

  # 最长的 SQL 输出长度
  # Maximum query length recorded in log.
  # query-log-max-len: 2048
  query-log-max-len: 4096
```

* * *

###### 还可以使用SQL语句动态调整阈值

**[官方文档，使用注解方式](https://pingcap.com/docs-cn/stable/reference/performance/optimizer-hints/#memory_quotan "官方文档，使用注解方式")**

```sql
-- 配置整条 SQL 的内存使用阈值为 8GB
set @@tidb_mem_quota_query = 8 << 30;
```

```sql
-- 配置整条 SQL 的内存使用阈值为 8MB
set @@tidb_mem_quota_query = 8 << 20;
```

###### 修改所有算子的内存控制

```sql
-- 34359738368 默认 32G
-- 1073741824  改为  1G

SET @@tidb_mem_quota_query=1073741824;
SET @@tidb_mem_quota_nestedloopapply=1073741824;
SET @@tidb_mem_quota_hashjoin=1073741824;
SET @@tidb_mem_quota_mergejoin=1073741824;
SET @@tidb_mem_quota_sort=1073741824;
SET @@tidb_mem_quota_topn=1073741824;
SET @@tidb_mem_quota_indexlookupreader=1073741824;
SET @@tidb_mem_quota_indexlookupjoin=1073741824;
SET @@tidb_mem_quota_nestedloopapply=1073741824;

SELECT @@tidb_mem_quota_query;
SELECT @@tidb_mem_quota_nestedloopapply;
SELECT @@tidb_mem_quota_hashjoin;
SELECT @@tidb_mem_quota_mergejoin;
SELECT @@tidb_mem_quota_sort;
SELECT @@tidb_mem_quota_topn;
SELECT @@tidb_mem_quota_indexlookupreader;
SELECT @@tidb_mem_quota_indexlookupjoin;
SELECT @@tidb_mem_quota_nestedloopapply;

```

* * *

* * *

##### 限制SQL执行时间

**[官方文档，使用注解方式](https://pingcap.com/docs-cn/stable/reference/performance/optimizer-hints/ "官方文档，使用注解方式")** `max_execution_time 目前对所有类型的 statement 生效，并非只对 SELECT 语句生效。` `其单位为 ms，但实际精度在 100ms 级别，而非更准确的毫秒级别。` 超时会引发异常信息: **`Query execution was interrupted`**

```sql
-- 设置最大执行时间为10秒
set @@global.MAX_EXECUTION_TIME=100000
```

* * *

* * *

##### 乐观锁配置调整

```sql
-- Session 级别设置 开启乐观锁重试 1关闭 0开启
set @@tidb_disable_txn_auto_retry = 0;
set @@tidb_retry_limit = 20;
```

```sql
-- Global 级别设置 开启乐观锁重试 1关闭 0开启
set @@global.tidb_disable_txn_auto_retry = off;
set @@global.tidb_retry_limit = 20;
```

* * *

* * *

* * *

* * *

* * *

* * *

#### 以下安装环境安装正式生产环境部署

###### 注：对于生产环境，须使用 TiDB-Ansible 部署 TiDB 集群。

1. Linux 操作系统版本要求 CentOS 7.3

##### 生产环境 （至少 9 台机器）

| 组件 | CPU | 内存 | 硬盘类型 | 网络 | 实例数量(最低要求) |
| --- | --- | --- | --- | --- | --- |
| TiDB | 16核+ | 32 GB+ | SAS | 万兆网卡（2块最佳） | 2 |
| PD | 4核+ | 8 GB+ | SSD | 万兆网卡（2块最佳） | 3 |
| TiKV | 16核+ | 32 GB+ | SSD | 万兆网卡（2块最佳） | 3 |
| 监控 | 8核+ | 16 GB+ | SAS | 千兆网卡 | 1 |

| HostName | IP | DES |
| --- | --- | --- |
| dev10 | 172.160.180.32 | 主控机 master |
| dev11 | 172.160.180.33 | 监控机 |
| dev12 | 172.160.180.34 | 工作节点 |
| dev13 | 172.160.180.35 | 工作节点 |
| dev14 | 172.160.180.36 | 工作节点 |
| dev15 | 172.160.180.37 | 工作节点 |

* * *

* * *

* * *

##### 准备机器

一、 部署目标机器若干

- 建议 4 台及以上，TiKV 至少 3 实例，且与 TiDB、PD 模块不位于同一主机
- 推荐安装 CentOS 7.3 及以上版本 Linux 操作系统，x86\_64 架构 (amd64)。
- 机器之间内网互通。
- 使用 Ansible 方式部署时，TiKV 及 PD 节点数据目录所在磁盘请使用 SSD 磁盘，否则无法通过检测。
- 目标机器如果没有安装 NTP 服务也需要外网

二、 部署中控机一台

- 中控机可以是部署目标机器中的某一台。
- 该机器需开放外网访问，用于下载 TiDB 及相关软件安装包。

* * *

* * *

* * *

#### 安装TiDB 调整目标机配置

###### 选择要安装的硬盘， 使用 fdisk -l命令查看哪个硬盘的配置最好

```ruby
[root@dev12 ~]# fdisk -l

磁盘 /dev/sdb：128.8 GB, 128849018880 字节，251658240 个扇区
Units = 扇区 of 1 * 512 = 512 bytes
扇区大小(逻辑/物理)：512 字节 / 512 字节
I/O 大小(最小/最佳)：512 字节 / 512 字节
磁盘标签类型：dos
磁盘标识符：0x056246d0

   设备 Boot      Start         End      Blocks   Id  System
/dev/sdb1            2048   251658239   125828096   8e  Linux LVM

磁盘 /dev/sda：85.9 GB, 85899345920 字节，167772160 个扇区
Units = 扇区 of 1 * 512 = 512 bytes
扇区大小(逻辑/物理)：512 字节 / 512 字节
I/O 大小(最小/最佳)：512 字节 / 512 字节
磁盘标签类型：dos
磁盘标识符：0x000c8857

   设备 Boot      Start         End      Blocks   Id  System
/dev/sda1   *        2048    20973567    10485760   83  Linux
/dev/sda2        20973568   167772159    73399296   8e  Linux LVM

磁盘 /dev/mapper/centos-root：61.2 GB, 61199089664 字节，119529472 个扇区
Units = 扇区 of 1 * 512 = 512 bytes
扇区大小(逻辑/物理)：512 字节 / 512 字节
I/O 大小(最小/最佳)：512 字节 / 512 字节


磁盘 /dev/mapper/centos-swap：8589 MB, 8589934592 字节，16777216 个扇区
Units = 扇区 of 1 * 512 = 512 bytes
扇区大小(逻辑/物理)：512 字节 / 512 字节
I/O 大小(最小/最佳)：512 字节 / 512 字节


# 这块硬盘的配置相对最高，我们选择它
磁盘 /dev/mapper/centos-home：128.8 GB, 128844824576 字节，251650048 个扇区
Units = 扇区 of 1 * 512 = 512 bytes
扇区大小(逻辑/物理)：512 字节 / 512 字节
I/O 大小(最小/最佳)：512 字节 / 512 字节

[root@dev12 ~]#
```

###### 查看硬盘的文件系统是否 属于 ext4, TiDB要求是 ext4, 如果不是我们需要进行调整

```ruby
[root@dev12 ~]# lsblk -f
NAME            FSTYPE      LABEL UUID                                   MOUNTPOINT
fd0
sda
├─sda1          xfs               ddd0be93-ca35-4ce1-b320-e2c5ac06e62d   /boot
└─sda2          LVM2_member       miDtM6-xhfw-cAKd-tcZL-3mPa-ShfJ-NeuHoS
  ├─centos-root xfs               bf264188-ae9c-40f5-bb5b-722a8e2e05db   /
  └─centos-swap swap              5df5770f-ebe4-4d0f-88b5-3032f8c05cb1
sdb
└─sdb1          LVM2_member       74fYOA-BPos-Wm6z-VvyB-Hcf7-4AQV-UlW13b
   # centos-home 这块硬盘挂载到了 当前系统的 /home目录下， 也就是说 /home目录用的是这块硬盘, 但是这块硬盘的格式是不符合要求的需要调整
  └─centos-home     xfs               3e05369b-c17c-4f2b-94ef-8691a5797368   /home
sr0
[root@dev12 ~]#
```

##### 调整硬盘为 ext4格式 **[用命令编写](#jump)**

###### 1\. 卸载硬盘

```ruby
[root@dev12 ~]# umount /dev/mapper/centos-home
umount: /home：目标忙。
        (有些情况下通过 lsof(8) 或 fuser(1) 可以
         找到有关使用该设备的进程的有用信息)

[root@dev12 ~]# fuser -m /home
-bash: fuser: 未找到命令
[root@dev12 ~]#
# 安装工具
[root@dev12 ~]# yum install psmisc -y
# 查看正在使用 /home 的程序
[root@dev12 ~]# fuser -m /home
/home:                5190c
[root@dev12 ~]#
# 杀死进程
[root@dev12 ~]# kill -9 5190
[root@dev12 ~]#
[root@dev12 ~]# umount /dev/mapper/centos-home
[root@dev12 ~]#
```

* * *

###### 2\. 格式化硬盘为 ext4格式

```ruby
[root@dev12 ~]# mkfs.ext4 /dev/mapper/centos-home
mke2fs 1.42.9 (28-Dec-2013)
文件系统标签=
OS type: Linux
块大小=4096 (log=2)
分块大小=4096 (log=2)
Stride=0 blocks, Stripe width=0 blocks
7864320 inodes, 31456256 blocks
1572812 blocks (5.00%) reserved for the super user
第一个数据块=0
Maximum filesystem blocks=2178940928
960 block groups
32768 blocks per group, 32768 fragments per group
8192 inodes per group
Superblock backups stored on blocks:
        32768, 98304, 163840, 229376, 294912, 819200, 884736, 1605632, 2654208,
        4096000, 7962624, 11239424, 20480000, 23887872

Allocating group tables: 完成
正在写入inode表: 完成
Creating journal (32768 blocks): 完成
Writing superblocks and filesystem accounting information: 完成

[root@dev12 ~]#
```

* * *

###### 3\. 修改 操作系统启动时，自动挂载硬盘的引导文件，告诉操作系统启动时这块硬盘已经是ext4格式的了，要以ext4的方式进行挂载

```ruby
# 编辑 /etc/fstab 文件，添加 nodelalloc 挂载参数
[root@dev12 ~]# vim /etc/fstab
# 将原来的写法
#  /dev/mapper/centos-home /home                   xfs     defaults        0 0
# 改为这种 TiDB要求的写法
/dev/mapper/centos-home    /home                   ext4    defaults,nodelalloc,noatime 0 2
[root@dev12 ~]#
# 挂载硬盘
[root@dev12 ~]# mount /dev/mapper/centos-home /home
# 查看是否更改成功
[root@dev12 ~]# mount -t ext4
/dev/mapper/centos-home on /home type ext4 (rw,noatime,seclabel,nodelalloc,data=ordered)
[root@dev12 ~]#
# 重启系统
[root@dev12 ~]# reboot
```

* * *

##### 将以上步骤，改为用命令编写

```ruby
# 定义变量
disk_path=/dev/mapper/centos-home

umount $disk_path && mkfs.ext4 $disk_path && mount $disk_path /home && lsblk -mf

cat >> /etc/fstab << ERIC
$disk_path /home                   ext4    defaults,nodelalloc,noatime 0 2
ERIC

vim /etc/fstab

reboot
```

* * *

* * *

* * *

##### 基本配置

```ruby
[root@dev10 ~]# more /etc/redhat-release
CentOS Linux release 7.6.1810 (Core)

[root@dev10 ~]# cat /etc/motd
********************
*   TiDB 中控机    *
********************
```

##### 在中控机上安装系统依赖包

###### 1 以 root 用户登录中控机，执行以下命令：

```ruby
[root@dev10 ~]# yum -y install epel-release git curl sshpass
[root@dev10 ~]# yum -y install python2-pip
```

* * *

###### 2 在中控机上创建 tidb 用户

```ruby
[root@dev10 ~]# useradd -m -d /home/tidb tidb
[root@dev10 ~]# passwd tidb
输入tidb用户密码
[root@dev10 ~]# visudo
tidb ALL=(ALL) NOPASSWD: ALL
```

* * *

###### 3 生成 ssh key

`注： su 命令从 root 用户切换到 tidb 用户下`

```ruby
[root@dev10 ~]# su - tidb
Attempting to create directory /home/tidb/perl5
[tidb@dev10 ~]$
[tidb@dev10 ~]$ ssh-keygen -t rsa
Generating public/private rsa key pair.
Enter file in which to save the key (/home/tidb/.ssh/id_rsa):
Created directory '/home/tidb/.ssh'.
Enter passphrase (empty for no passphrase):
Enter same passphrase again:
Your identification has been saved in /home/tidb/.ssh/id_rsa.
Your public key has been saved in /home/tidb/.ssh/id_rsa.pub.
The key fingerprint is:
SHA256:TMyVHftcI7hl6ranQdbDKfNOeVRe3ZGzXB0TN1yhxJA tidb@dev10
The key's randomart image is:
+---[RSA 2048]----+
|          .+=o.BX|
|       o ..E+o.+X|
|        +  ..=..X|
|       o    Boo=+|
|        S  B =o..|
|          + + +  |
|           + + . |
|          . =..  |
|           oo.   |
+----[SHA256]-----+
[tidb@dev10 ~]$

```

* * *

###### 4 在中控机器上下载 TiDB-Ansible

`以 tidb 用户登录中控机并进入 /home/tidb 目录。` _注： 务必按文档操作，将 tidb-ansible 下载到 /home/tidb 目录下，权限为 tidb 用户，不要下载到 /root 下，否则会遇到权限问题。_

| tidb-ansible 分支 | TiDB 版本 | 备注 |
| --- | --- | --- |
| release-2.0 | 2.0 版本 | 最新 2.0 稳定版本，可用于生产环境。 |
| release-2.1 | 2.1 版本 | 最新 2.1 稳定版本，可用于生产环境（建议）。 |
| maste | master 版本 | 包含最新特性，每日更新。 |

`根据官方建议选择 release-2.1`

```ruby
[tidb@dev10 ~]$ pwd
/home/tidb
[tidb@dev10 ~]$ git clone -b release-2.1 https://github.com/pingcap/tidb-ansible.git
# 如果安装 3.0.9
# git clone -b v3.0.9 https://github.com/pingcap/tidb-ansible.git
```

* * *

###### 5 在中控机器上安装 Ansible 及其依赖

```
以 tidb 用户登录中控机，请务必按以下方式通过 pip 安装 Ansible 及其相关依赖的指定版本，否则会有兼容问题。安装完成后，可通过 ansible --version 查看 Ansible 版本。目前 release-2.0、release-2.1 及 master 版本兼容 Ansible 2.4 及 Ansible 2.5 版本，Ansible 及相关依赖版本记录在 tidb-ansible/requirements.txt 文件中。
```

```ruby
[tidb@dev10 ~]$ cd tidb-ansible/
[tidb@dev10 ~]$
# 安装 pip 如果已经安装了，这一步可以跳过
[tidb@dev10 ~]$ sudo wget https://bootstrap.pypa.io/get-pip.py && sudo python get-pip.py
[tidb@dev10 ~]$
[tidb@dev10 tidb-ansible]$ sudo pip install -r ./requirements.txt -i https://pypi.douban.com/simple
......
You are using pip version 8.1.2, however version 19.0.3 is available.
You should consider upgrading via the 'pip install --upgrade pip' command.
[tidb@dev10 tidb-ansible]$
[tidb@dev10 tidb-ansible]$ ansible --version
ansible 2.6.13
......
[tidb@dev10 tidb-ansible]$
```

* * *

###### 6 在中控机上配置部署机器 ssh 互信及 sudo 规则

`以 tidb 用户登录中控机，将你的部署目标机器 IP 添加到 hosts.ini 文件 [servers] 区块下。` `注：不要加入主控机IP`

```ruby
[tidb@dev10 tidb-ansible]$ vim hosts.ini
[tidb@dev10 tidb-ansible]$ cat hosts.ini
[servers]
172.160.180.33
172.160.180.34
172.160.180.35
172.160.180.36
172.160.180.37

[all:vars]
username = tidb
ntp_server = pool.ntp.org
[tidb@dev10 tidb-ansible]$
```

* * *

###### 7 配置中控机与部署目标机器之间的 ssh 互信

`执行以下命令，按提示输入部署目标机器 root 用户密码。` `该步骤将在部署目标机器上创建 tidb 用户，并配置 sudo 规则，配置中控机与部署目标机器之间的 ssh 互信。`

```ruby
[tidb@dev10 tidb-ansible]$ ansible-playbook -i hosts.ini create_users.yml -u root -k
SSH password:

PLAY [all] *************************************************************************************************
......

Congrats! All goes well. :-)
[tidb@dev10 tidb-ansible]$
```

* * *

###### 8 执行以下命令如果所有 server 返回 tidb 表示 ssh 互信配置成功。

```ruby
[tidb@dev10 tidb-ansible]$ ansible -i hosts.ini all -m shell -a 'whoami'
172.160.180.33 | SUCCESS | rc=0 >>
tidb
......
[tidb@dev10 tidb-ansible]$
```

* * *

###### 9 执行以下命令如果所有 server 返回 root 表示 tidb 用户 sudo 免密码配置成功。

```ruby
[tidb@dev10 tidb-ansible]$ ansible -i hosts.ini all -m shell -a 'whoami' -b
172.160.180.33 | SUCCESS | rc=0 >>
root
......
[tidb@dev10 tidb-ansible]$
```

* * *

###### 10 时区同步

`在部署目标机器上安装 NTP 服务` `以 tidb 用户登录中控机，执行以下命令：`

```ruby
[tidb@dev10 tidb-ansible]$ ansible-playbook -i hosts.ini deploy_ntp.yml -u tidb -b
```

* * *

###### 11 检测 NTP 服务是否正常

```ruby
[tidb@dev10 tidb-ansible]$ ansible -i hosts.ini all -m shell -a 'systemctl status ntpd.service'

172.160.180.52 | CHANGED | rc=0 >>
● ntpd.service - Network Time Service
   Loaded: loaded (/usr/lib/systemd/system/ntpd.service; disabled; vendor preset: disabled)
   Active: active (running) since 三 2019-10-16 08:58:05 CST; 9min ago
  Process: 1767 ExecStart=/usr/sbin/ntpd -u ntp:ntp $OPTIONS (code=exited, status=0/SUCCESS)
 Main PID: 1768 (ntpd)
    Tasks: 1
   Memory: 1.3M
   CGroup: /system.slice/ntpd.service
           └─1768 /usr/sbin/ntpd -u ntp:ntp -g
   ......
```

`执行如下命令所有节点都提示 synchronised to NTP server 服务表示同步成功`

```ruby
[tidb@dev10 tidb-ansible]$ ansible -i hosts.ini all -m shell -a 'ntpstat'
172.160.180.52 | CHANGED | rc=0 >>
synchronised to NTP server (193.182.111.141) at stratum 3
   time correct to within 179 ms
   polling server every 1024 s

   ......
```

* * *

###### 12 NTP开机自启动

```ruby
[tidb@dev10 tidb-ansible]$ ansible -i hosts.ini all -m shell -a 'systemctl enable ntpd.service && systemctl start ntpd.service' -b
```

* * *

###### 13 在部署目标机器上配置 CPUfreq 调节器模式

**为了让 CPU 发挥最大性能，请将 CPUfreq 调节器模式设置为 performance 模式。** **官网中系统支持设置 performance 和 powersave 模式。`如果返回 "Not Available"`，表示当前系统不支持配置 CPUfreq，`跳过该步骤即可`。**

```ruby
[root@dev10 ~]# ansible -i hosts.ini all -m shell -a 'cpupower frequency-info --governors'
analyzing CPU 0:
  available cpufreq governors: Not Available
......
[root@dev10 ~]#
```

**如果系统支持的调节器模式时需要做如下配置** **通过 cpupower 命令查看系统当前的 CPUfreq 调节器模式：**

```ruby
[root@dev16 ~]# cpupower frequency-info --governors
analyzing CPU 0:
  available cpufreq governors: performance powersave

[root@dev16 ~]#
```

**查看系统当前的 CPUfreq 调节器模式：**

```ruby
[root@dev16 ~]# cpupower frequency-info --policy
analyzing CPU 0:
  current policy: frequency should be within 800 MHz and 4.90 GHz.
                  The governor "powersave" may decide which speed to use
                  within this range.
[root@dev16 ~]#
```

**当前配置是 powersave 模式，可以通过以下命令设置为 performance 模式。**

```ruby
[root@dev16 ~]# cpupower frequency-set --governor performance
Setting cpu: 0
Setting cpu: 1
Setting cpu: 2
Setting cpu: 3
Setting cpu: 4
Setting cpu: 5
Setting cpu: 6
Setting cpu: 7
[root@dev16 ~]#

[root@dev16 ~]# cpupower frequency-info --policy
analyzing CPU 0:
  current policy: frequency should be within 800 MHz and 4.90 GHz.
                  The governor "performance" may decide which speed to use
                  within this range.
[root@dev16 ~]#
```

**也可以通过以下命令在部署目标机器上批量设置：** `但是本集群中 部分机器是虚拟机，部分机器是 PC机， 所以在做批量处理时需要格外注意命令的使用`

```ruby
[root@dev16 ~]# ansible -i hosts.ini all -m shell -a "cpupower frequency-set --governor performance" -u tidb -b
```

* * *

* * *

* * *

##### 分配机器资源，编辑 inventory.ini 文件

资源分配分为两个种： 一、单机单 TiKV 实例集群

- 一台目标机器一个 TiKV 实例

二、单机多 TiKV 实例集群（[官网地址](https://pingcap.com/docs-cn/v3.0/how-to/deploy/orchestrated/ansible/#%E5%8D%95%E6%9C%BA%E5%A4%9A-tikv-%E5%AE%9E%E4%BE%8B%E9%9B%86%E7%BE%A4%E6%8B%93%E6%89%91 "官网地址")）

- 一台目标机器多个 TiKV 实例

###### 单机单 TiKV 实例集群拓扑

`注：不要加入主控机IP`

```ruby
[tidb@dev10 tidb-ansible]$ cat inventory.ini
## TiDB Cluster Part
## TiDB Cluster Part
[tidb_servers]
172.160.180.33
172.160.180.34

[tikv_servers]
172.160.180.35
172.160.180.36
172.160.180.37

[pd_servers]
172.160.180.33
172.160.180.34
172.160.180.35

[spark_master]

[spark_slaves]

[lightning_server]

[importer_server]

## Monitoring Part
# prometheus and pushgateway servers
[monitoring_servers]
172.160.180.33

[grafana_servers]
172.160.180.33

# node_exporter and blackbox_exporter servers
[monitored_servers]
172.160.180.33
172.160.180.34
172.160.180.35
172.160.180.36
172.160.180.37

[alertmanager_servers]
172.160.180.33

[kafka_exporter_servers]

## Binlog Part
[pump_servers]

[drainer_servers]

## Group variables
[pd_servers:vars]
# location_labels = ["zone","rack","host"]

## Global variables
## 将每个TiDB集群安装部署到哪个目录下
[all:vars]
deploy_dir = /home/tidb/deploy

## Connection
# ssh via normal user
ansible_user = tidb

cluster_name = test-cluster

tidb_version = v2.1.4

# process supervision, [systemd, supervise]
process_supervision = systemd

timezone = Asia/Shanghai

enable_firewalld = False
# check NTP service
enable_ntpd = True
set_hostname = False

## binlog trigger
enable_binlog = False

# kafka cluster address for monitoring, example:
# kafka_addrs = "172.160.0.11:9092,172.160.0.12:9092,172.160.0.13:9092"
kafka_addrs = ""

# zookeeper address of kafka cluster for monitoring, example:
# zookeeper_addrs = "172.160.0.11:2181,172.160.0.12:2181,172.160.0.13:2181"
zookeeper_addrs = ""

# store slow query log into seperate file
enable_slow_query_log = False

# enable TLS authentication in the TiDB cluster
enable_tls = False

# KV mode
deploy_without_tidb = False

# Optional: Set if you already have a alertmanager server.
# Format: alertmanager_host:alertmanager_port
alertmanager_target = ""

grafana_admin_user = "admin"
grafana_admin_password = "admin"


### Collect diagnosis
collect_log_recent_hours = 2

enable_bandwidth_limit = True
# default: 10Mb/s, unit: Kbit/s
collect_bandwidth_limit = 10000

# 常驻内存上限，根据实际内存修改
MemoryLimit = 25G

[tidb@dev10 tidb-ansible]$
```

* * *

* * *

##### 部署任务

1.确认 tidb-ansible/inventory.ini 文件中 ansible\_user = tidb，本例使用 tidb 用户作为服务运行用户，配置如下： ansible\_user 不要设置成 root 用户，tidb-ansible 限制了服务以普通用户运行。

```ruby
## Connection
# ssh via normal user
ansible_user = tidb
```

* * *

2.执行 local\_prepare.yml playbook，联网下载 TiDB binary 到中控机： `如果网络不好，这个过程会非常非常非常的漫长`

```ruby
[tidb@dev10 tidb-ansible]$ ansible-playbook local_prepare.yml
......
Congrats! All goes well. :-)
[tidb@dev10 tidb-ansible]$
```

* * *

3.初始化系统环境，修改内核参数

```ruby
[tidb@dev10 tidb-ansible]$ ansible-playbook bootstrap.yml --extra-vars "dev_mode=True"
......
Congrats! All goes well. :-)
[tidb@dev10 tidb-ansible]$
```

* * *

4.批量执行关闭Swap

```ruby
[tidb@dev10 tidb-ansible]$ ansible -i hosts.ini all -m shell -a 'swapoff -a' -u tidb -b

172.160.180.52 | CHANGED | rc=0 >>

172.160.180.51 | CHANGED | rc=0 >>

172.160.180.34 | CHANGED | rc=0 >>

172.160.180.33 | CHANGED | rc=0 >>

172.160.180.35 | CHANGED | rc=0 >>

172.160.180.53 | CHANGED | rc=0 >>

[tidb@dev10 tidb-ansible]$
```

* * *

5.部署 TiDB 集群软件

```ruby
# 重新执行
[tidb@dev10 tidb-ansible]$ ansible-playbook deploy.yml
......
Congrats! All goes well. :-)
[tidb@dev10 tidb-ansible]$
```

* * *

6.启动 TiDB 集群

```ruby
[tidb@dev10 tidb-ansible]$ ansible-playbook start.yml
......
Congrats! All goes well. :-)
[tidb@dev10 tidb-ansible]$
```

* * *

7.web测试 http://172.160.180.33:3000/login User: admin Password: admin

* * *

8.MySQL 客户端连接测试，TCP 4000 端口是 TiDB 服务默认端口。 默认没有密码

```ruby
mysql -u root -h 172.160.180.33 -P 4000
```

* * *

* * *

* * *

##### 查看运行状态

```ruby
[tidb@dev10 tidb-ansible]$ mysql -u root -h 172.160.180.33 -P 4000
Welcome to the MariaDB monitor.  Commands end with ; or \g.
Your MySQL connection id is 11
Server version: 5.7.10-TiDB-v2.1.4 MySQL Community Server (Apache License 2.0)
Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.
Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.
MySQL [(none)]> show databases;
+--------------------+
| Database           |
+--------------------+
| INFORMATION_SCHEMA |
| PERFORMANCE_SCHEMA |
| mysql              |
| test               |
+--------------------+
4 rows in set (0.00 sec)
MySQL [(none)]> use mysql;
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A
Database changed
MySQL [mysql]> show tables;
+----------------------+
| Tables_in_mysql      |
+----------------------+
| GLOBAL_VARIABLES     |
| columns_priv         |
| db                   |
| gc_delete_range      |
| gc_delete_range_done |
| help_topic           |
| stats_buckets        |
| stats_feedback       |
| stats_histograms     |
| stats_meta           |
| tables_priv          |
| tidb                 |
| user                 |
+----------------------+
13 rows in set (0.00 sec)
MySQL [mysql]>
```

##### 修改密码

```sql
MySQL [mysql]>
MySQL [mysql]> ALTER USER 'root'@'%' IDENTIFIED BY '数据库密码';
Query OK, 0 rows affected (0.03 sec)
MySQL [mysql]>
```

* * *

* * *

* * *

##### 运维常用命令

```ruby
启动集群
此操作会按顺序启动整个 TiDB 集群所有组件（包括 PD、TiDB、TiKV 等组件和监控组件）。
[tidb@dev10 tidb-ansible]$ ansible-playbook start.yml
```

```ruby
关闭集群
此操作会按顺序关闭整个 TiDB 集群所有组件（包括 PD、TiDB、TiKV 等组件和监控组件）。
[tidb@dev10 tidb-ansible]$ ansible-playbook stop.yml
```

```ruby
清除集群数据
此操作会关闭 TiDB、Pump、TiKV、PD 服务，并清空 Pump、TiKV、PD 数据目录。
[tidb@dev10 tidb-ansible]$ ansible-playbook unsafe_cleanup_data.yml
```

```ruby
销毁集群
此操作会关闭集群，并清空部署目录，若部署目录为挂载点，会报错，可忽略。
[tidb@dev10 tidb-ansible]$ ansible-playbook unsafe_cleanup.yml
```

* * *

* * *

* * *
