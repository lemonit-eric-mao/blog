---
title: 'Hadoop 单机模式安装'
date: '2017-11-16T15:47:04+00:00'
status: publish
permalink: /2017/11/16/hadoop-%e5%8d%95%e6%9c%ba%e6%a8%a1%e5%bc%8f%e5%ae%89%e8%a3%85
author: 毛巳煜
excerpt: ''
type: post
id: 514
category:
    - 大数据
tag: []
post_format: []
---
- 操作系统: ubuntu 16.04
- Hadoop : 2.8.1
- jdk版本: 1.8

### **下载 Apache Hadoop Release**

下载发行版 http://101.96.8.165/www.apache.org/dyn/closer.cgi/hadoop/common/hadoop-2.8.1/hadoop-2.8.1.tar.gz

### **安装 Hadoop**

```
<pre class="line-numbers prism-highlight" data-start="1">```ruby
mao-siyu@mao-siyu-PC:~/MyHadoop<span class="katex math inline">tar -xzvf hadoop-2.8.1.tar.gz
mao-siyu@mao-siyu-PC:~/MyHadoop</span> cd hadoop-2.8.1/
mao-siyu@mao-siyu-PC:~/MyHadoop/hadoop-2.8.1$

```
```

### **配置 Hadoop 环境变量**

```
<pre class="line-numbers prism-highlight" data-start="1">```ruby
mao-siyu@mao-siyu-PC:~/MyHadoop/hadoop-2.8.1<span class="katex math inline">pwd
/home/mao-siyu/MyHadoop/hadoop-2.8.1
mao-siyu@mao-siyu-PC:~/MyHadoop/hadoop-2.8.1</span> sudo vim /etc/profile

export HADOOP_HOME=/home/mao-siyu/MyHadoop/hadoop-2.8.1
export PATH=<span class="katex math inline">HADOOP_HOME/bin:</span>PATH
:wq!

mao-siyu@mao-siyu-PC:~/MyHadoop/hadoop-2.8.1<span class="katex math inline">source /etc/profile
mao-siyu@mao-siyu-PC:~/MyHadoop/hadoop-2.8.1</span>
mao-siyu@mao-siyu-PC:~/MyHadoop/hadoop-2.8.1$ exit

```
```

### **启动 Hadoop**

```
<pre class="line-numbers prism-highlight" data-start="1">```ruby
mao-siyu@mao-siyu-PC:~/MyHadoop/hadoop-2.8.1$ ./sbin/start-all.sh
localhost: Error: JAVA_HOME is not set and could not be found.

```
```

#### **Error: JAVA\_HOME is not set**

**原因是在%HADOOP\_HOME%/etc/hadoop/hadoop-env.sh 内缺少JAVA\_HOME的定义，只需要把 hadoop-env.sh中  
export JAVA\_HOME=${JAVA\_HOME}  
改为  
export JAVA\_HOME=/home/java/jdk1.8.0\_111**

```
<pre class="line-numbers prism-highlight" data-start="1">```ruby
mao-siyu@mao-siyu-PC:~/MyHadoop/hadoop-2.8.1<span class="katex math inline">vim etc/hadoop/hadoop-env.sh
mao-siyu@mao-siyu-PC:~/MyHadoop/hadoop-2.8.1</span>
mao-siyu@mao-siyu-PC:~/MyHadoop/hadoop-2.8.1<span class="katex math inline">./sbin/start-all.sh
This script is Deprecated. Instead use start-dfs.sh and start-yarn.sh
Incorrect configuration: namenode address dfs.namenode.servicerpc-address or dfs.namenode.rpc-address is not configured.
Starting namenodes on []
mao-siyu@localhost's password:
localhost: starting namenode, logging to /home/mao-siyu/MyHadoop/hadoop-2.8.1/logs/hadoop-mao-siyu-namenode-mao-siyu-PC.out
mao-siyu@localhost's password:
localhost: starting datanode, logging to /home/mao-siyu/MyHadoop/hadoop-2.8.1/logs/hadoop-mao-siyu-datanode-mao-siyu-PC.out
Starting secondary namenodes [0.0.0.0]
mao-siyu@0.0.0.0's password:
0.0.0.0: starting secondarynamenode, logging to /home/mao-siyu/MyHadoop/hadoop-2.8.1/logs/hadoop-mao-siyu-secondarynamenode-mao-siyu-PC.out
starting yarn daemons
starting resourcemanager, logging to /home/mao-siyu/MyHadoop/hadoop-2.8.1/logs/yarn-mao-siyu-resourcemanager-mao-siyu-PC.out
mao-siyu@localhost's password:
localhost: starting nodemanager, logging to /home/mao-siyu/MyHadoop/hadoop-2.8.1/logs/yarn-mao-siyu-nodemanager-mao-siyu-PC.out
mao-siyu@mao-siyu-PC:~/MyHadoop/hadoop-2.8.1</span>

```
```

### **使用jps命令查看进程是否启动成功**

```
<pre class="line-numbers prism-highlight" data-start="1">```ruby
mao-siyu@mao-siyu-PC:~/MyHadoop/hadoop-2.8.1$ jps
3083 ResourceManager
3611 Jps
3381 NodeManager

```
```

### **查看安装是否成功**

```
<pre class="line-numbers prism-highlight" data-start="1">```ruby
mao-siyu@mao-siyu-PC:~/MyHadoop/hadoop-2.8.1<span class="katex math inline">./bin/hadoop fs -ls /
Found 26 items
drwxr-xr-x   - root root       4096 2017-06-05 15:47 /bin
drwxr-xr-x   - root root       4096 2017-08-16 12:28 /boot
drwxrwxr-x   - root root       4096 2016-10-19 09:24 /cdrom
drwxr-xr-x   - root root       4060 2017-08-23 10:02 /dev
drwxr-xr-x   - root root      12288 2017-08-24 16:16 /etc
drwxr-xr-x   - root root       4096 2016-10-19 14:36 /home
-rw-r--r--   1 root root   38048656 2017-08-16 12:28 /initrd.img
-rw-r--r--   1 root root   38050472 2017-08-15 19:57 /initrd.img.old
drwxr-xr-x   - root root       4096 2017-03-16 09:42 /lib
drwxr-xr-x   - root root       4096 2017-06-20 04:36 /lib64
drwx------   - root root      16384 2016-10-19 09:21 /lost+found
drwxr-xr-x   - root root       4096 2016-10-19 10:51 /media
drwxr-xr-x   - root root       4096 2016-04-21 06:07 /mnt
drwxr-xr-x   - root root       4096 2017-08-24 15:20 /opt
dr-xr-xr-x   - root root          0 2017-08-23 10:01 /proc
drwx------   - root root       4096 2017-08-24 16:16 /root
drwxr-xr-x   - root root       1020 2017-08-24 16:21 /run
drwxr-xr-x   - root root      12288 2017-06-20 04:36 /sbin
drwxr-xr-x   - root root       4096 2016-04-19 22:31 /snap
drwxr-xr-x   - root root       4096 2016-04-21 06:07 /srv
dr-xr-xr-x   - root root          0 2017-08-24 16:08 /sys
drwxrwxrwt   - root root      90112 2017-08-24 16:21 /tmp
drwxr-xr-x   - root root       4096 2016-04-21 06:13 /usr
drwxr-xr-x   - root root       4096 2017-08-21 16:58 /var
-rw-------   1 root root    7098032 2017-08-10 19:02 /vmlinuz
-rw-------   1 root root    7097936 2017-08-08 21:58 /vmlinuz.old
mao-siyu@mao-siyu-PC:~/MyHadoop/hadoop-2.8.1</span>
# 单机模式安装成功

```
```