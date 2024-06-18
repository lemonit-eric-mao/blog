---
title: 'CentOS 7 安装运行 Zookeeper 服务端'
date: '2017-11-16T15:44:11+00:00'
status: publish
permalink: /2017/11/16/centos-7-%e5%ae%89%e8%a3%85%e8%bf%90%e8%a1%8c-zookeeper-%e6%9c%8d%e5%8a%a1%e7%ab%af
author: 毛巳煜
excerpt: ''
type: post
id: 510
category:
    - 大数据
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
**Zookeeper的应用**
----------------

**Zookeeper 服务器: 10.32.156.68  
[Zookeeper 官方下载](http://apache.fayea.com/zookeeper/)  
系统版本:**

```
<pre class="line-numbers prism-highlight" data-start="1">```ruby
[root@localhost ~]# cat /etc/redhat-release
CentOS Linux release 7.2.1511 (Core)
[root@localhost ~]#

```
```

### 重命名hosts

```
<pre class="line-numbers prism-highlight" data-start="1">```ruby
[root@localhost ~]# echo "10.32.156.68 zk-68" >> /etc/hosts
[root@localhost ~]# cat /etc/hosts
10.32.156.68 zk-68
[root@localhost ~]#
[root@localhost ~]# hostname zk-68
[root@localhost ~]# exit
# 退出重新连接
[root@zk-68 ~]#

```
```

### 下载安装 Zookeeper

```
<pre class="line-numbers prism-highlight" data-start="1">```ruby
[root@zk-68 home]# mkdir mao_siyu
[root@zk-68 home]# mkdir mao_siyu/zk
[root@zk-68 home]# cd mao_siyu/zk/
[root@zk-68 zk]#
[root@zk-68 zk]# wget http://apache.fayea.com/zookeeper/zookeeper-3.4.10/zookeeper-3.4.10.tar.gz
[root@zk-68 zk]# ll -a
总用量 34232
drwxr-xr-x 2 root root     4096 8月  16 11:09 .
drwxr-xr-x 3 root root     4096 8月  16 11:07 ..
-rw-r--r-- 1 root root 35042811 6月  20 19:33 zookeeper-3.4.10.tar.gz
[root@zk-68 zk]#
[root@zk-68 zk]# tar -xzvf zookeeper-3.4.10.tar.gz
[root@zk-68 zk]# ll -a
总用量 34236
drwxr-xr-x  3 root root     4096 8月  16 11:10 .
drwxr-xr-x  3 root root     4096 8月  16 11:07 ..
drwxr-xr-x 10 1001 1001     4096 3月  23 19:28 zookeeper-3.4.10
-rw-r--r--  1 root root 35042811 6月  20 19:33 zookeeper-3.4.10.tar.gz

```
```

### 查看配置文件

```
<pre class="line-numbers prism-highlight" data-start="1">```ruby
[root@zk-68 zk]# cd zookeeper-3.4.10
[root@zk-68 zookeeper-3.4.10]# cat conf/zoo_sample.cfg
# The number of milliseconds of each tick
tickTime=2000
# The number of ticks that the initial
# synchronization phase can take
initLimit=10
# The number of ticks that can pass between
# sending a request and getting an acknowledgement
syncLimit=5
# the directory where the snapshot is stored.
# do not use /tmp for storage, /tmp here is just
# example sakes.
dataDir=/tmp/zookeeper
# the port at which the clients will connect
clientPort=2181
# the maximum number of client connections.
# increase this if you need to handle more clients
#maxClientCnxns=60
#
# Be sure to read the maintenance section of the
# administrator guide before turning on autopurge.
#
# http://zookeeper.apache.org/doc/current/zookeeperAdmin.html#sc_maintenance
#
# The number of snapshots to retain in dataDir
#autopurge.snapRetainCount=3
# Purge task interval in hours
# Set to "0" to disable auto purge feature
#autopurge.purgeInterval=1
[root@zk-68 zookeeper-3.4.10]#

```
```

### 根据zoo\_sample.cfg 模板创建新的配置文件zoo.cfg

zookeeper 它识别的是`zoo.cfg`文件 而不是 zoo\_sample.cfg

```
<pre class="line-numbers prism-highlight" data-start="1">```ruby
[root@zk-68 zookeeper-3.4.10]# cd conf/
[root@zk-68 conf]# ll
总用量 12
-rw-rw-r-- 1 1001 1001  535 3月  23 18:14 configuration.xsl
-rw-rw-r-- 1 1001 1001 2161 3月  23 18:14 log4j.properties
-rw-rw-r-- 1 1001 1001  922 3月  23 18:14 zoo_sample.cfg
[root@zk-68 conf]#
[root@zk-68 conf]# cp zoo_sample.cfg zoo.cfg
[root@zk-68 conf]#
[root@zk-68 conf]# vim zoo.cfg
[root@zk-68 conf]#
[root@zk-68 conf]# cat zoo.cfg
# The number of milliseconds of each tick
#
# zookeeper 定义的基准时间间隔，单位：毫秒
tickTime=2000
# The number of ticks that the initial
# synchronization phase can take
initLimit=10
# The number of ticks that can pass between
# sending a request and getting an acknowledgement
syncLimit=5
# the directory where the snapshot is stored.
# do not use /tmp for storage, /tmp here is just
# example sakes.
#dataDir=/tmp/zookeeper
#
# 数据文件
dataDir=/home/mao_siyu/zk/zookeeper-3.4.10/data
#
# 日志文件
dataLogDir=/home/mao_siyu/zk/zookeeper-3.4.10/logs
# the port at which the clients will connect
#
# 客户端访问 Zookeeper 端口号
clientPort=2181
# the maximum number of client connections.
# increase this if you need to handle more clients
#maxClientCnxns=60
#
# Be sure to read the maintenance section of the
# administrator guide before turning on autopurge.
#
# http://zookeeper.apache.org/doc/current/zookeeperAdmin.html#sc_maintenance
#
# The number of snapshots to retain in dataDir
#autopurge.snapRetainCount=3
# Purge task interval in hours
# Set to "0" to disable auto purge feature
#autopurge.purgeInterval=1
[root@zk-68 conf]#

```
```

### 配置环境变量 添加如下代码

```
<pre class="line-numbers prism-highlight" data-start="1">```ruby
[root@zk-68 zk]# vim /etc/profile
...... 省略其它
export ZOOKEEPER_HOME=/home/mao_siyu/zk/zookeeper-3.4.10/
export PATH=<span class="katex math inline">ZOOKEEPER_HOME/bin:</span>PATH
export PATH
[root@zk-68 zk]# source /etc/profile
[root@zk-68 zk]#

```
```

### 启动 Zookeeper

```
<pre class="line-numbers prism-highlight" data-start="1">```ruby
[root@zk-68 zookeeper-3.4.10]# cd bin/
README.txt    zkCleanup.sh  zkCli.cmd     zkCli.sh      zkEnv.cmd     zkEnv.sh      zkServer.cmd  zkServer.sh
[root@zk-68 zookeeper-3.4.10]# cd bin/
[root@zk-68 bin]# ll -a
总用量 44
drwxr-xr-x  2 1001 1001 4096 3月  23 19:27 .
drwxr-xr-x 10 1001 1001 4096 3月  23 19:28 ..
-rwxr-xr-x  1 1001 1001  232 3月  23 18:14 README.txt
-rwxr-xr-x  1 1001 1001 1937 3月  23 18:14 zkCleanup.sh
-rwxr-xr-x  1 1001 1001 1056 3月  23 18:14 zkCli.cmd
-rwxr-xr-x  1 1001 1001 1534 3月  23 18:14 zkCli.sh
-rwxr-xr-x  1 1001 1001 1628 3月  23 18:14 zkEnv.cmd
-rwxr-xr-x  1 1001 1001 2696 3月  23 18:14 zkEnv.sh
-rwxr-xr-x  1 1001 1001 1089 3月  23 18:14 zkServer.cmd
-rwxr-xr-x  1 1001 1001 6773 3月  23 18:14 zkServer.sh
[root@zk-68 bin]#
[root@zk-68 bin]# zkServer.sh start
ZooKeeper JMX enabled by default
Using config: /home/mao_siyu/zk/zookeeper-3.4.10/bin/../conf/zoo.cfg
Starting zookeeper ... STARTED
[root@zk-68 bin]#
# 出现如上信息表示启动成功

```
```