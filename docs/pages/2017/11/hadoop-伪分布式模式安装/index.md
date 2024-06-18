---
title: "Hadoop 伪分布式模式安装"
date: "2017-11-16"
categories: 
  - "大数据"
---

- 操作系统: Cent OS 7
- Hadoop : 2.8.1
- jdk版本: 1.7

## 服务器列表:

- 10.32.156.64 sp-64 \`masterer\`
- 10.32.156.65 sp-65
- 10.32.156.66 sp 66
- 10.32.156.67 sp-67

### 创建新用户 配置hosts 文件 并改名

```ruby
[root@localhost ~]# echo "
10.32.156.64 sp-64
10.32.156.65 sp-65
10.32.156.66 sp-66
10.32.156.67 sp-67
" >> /etc/hosts
[root@localhost ~]#
[root@localhost ~]# adduser myhadoop
[root@localhost ~]# passwd myhadoop
更改用户 myhadoop 的密码 。
新的 密码：
无效的密码： 密码少于 8 个字符
重新输入新的 密码：
passwd：所有的身份验证令牌已经成功更新。
# 密码是123456
[root@localhost ~]#
[root@localhost ~]# hostname sp-64
[root@localhost ~]# exit
```

### **下载 Apache Hadoop Release**

下载发行版 http://101.96.8.165/www.apache.org/dyn/closer.cgi/hadoop/common/hadoop-2.8.1/hadoop-2.8.1.tar.gz

### 安装jdk 配置环境变量, 虽然rpm默认安装不需要配置, 但为了可控还是手动配置一下

```ruby
[root@sp-64 myhadoop]# ll
-rwxrwxrwx  1 root root 424555111 8月  29 09:43 hadoop-2.8.1.tar.gz
-rwxrwxrwx  1 root root 138090286 8月  29 11:22 jdk-7u80-linux-x64.rpm
[root@sp-64 myhadoop]#
[root@sp-64 myhadoop]# rpm -ivh jdk-7u80-linux-x64.rpm
[root@sp-64 myhadoop]#
[root@sp-64 myhadoop]# vim /etc/profile

JAVA_HOME=/usr/java/jdk1.7.0_80
JRE_HOME=$JAVA_HOME/jre
PATH=$PATH:$JAVA_HOME/bin:$JRE_HOME/bin
CLASSPATH=.:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar:$JRE_HOME/lib
export JAVA_HOME JRE_HOME PATH CLASSPATH

:wq!
[root@sp-64 myhadoop]#
[root@sp-64 myhadoop]# java -version
java version "1.7.0_80"
Java(TM) SE Runtime Environment (build 1.7.0_80-b15)
Java HotSpot(TM) 64-Bit Server VM (build 24.80-b11, mixed mode)
[root@sp-64 myhadoop]#
```

### **安装 Hadoop**

```ruby
[root@sp-64 myhadoop]# tar -xzvf hadoop-2.8.1.tar.gz
[root@sp-64 myhadoop]# ll
drwxrwxr-x 9  500  500      4096 6月   2 14:24 hadoop-2.8.1
-rwxr-xr-x 1 root root 424555111 9月   4 10:35 hadoop-2.8.1.tar.gz
-rwxr-xr-x 1 root root 138090286 9月   4 10:35 jdk-7u80-linux-x64.rpm
[root@sp-64 myhadoop]#
```

### **配置 Hadoop 环境变量**

```ruby
[root@sp-64 myhadoop]# vim /etc/profile

export HADOOP_HOME=/home/myhadoop/hadoop-2.8.1
export PATH=$HADOOP_HOME/bin:$PATH
:wq!
[root@sp-64 myhadoop]#
[root@sp-64 myhadoop]# source /etc/profile
[root@sp-64 myhadoop]#
```

### **启动 Hadoop**

```ruby
[root@sp-64 myhadoop]# cd hadoop-2.8.1
[root@sp-64 hadoop-2.8.1]# ./sbin/start-all.sh
localhost: Error: JAVA_HOME is not set and could not be found.
```

#### **Error: JAVA\_HOME is not set**

**原因是在%HADOOP\_HOME%/etc/hadoop/hadoop-env.sh 内缺少JAVA\_HOME的定义，只需要把 hadoop-env.sh中 export JAVA\_HOME=${JAVA\_HOME} 改为 export JAVA\_HOME=/usr/java/jdk1.7.0\_80** `注意etc`是 hadoop-2.8.1/etc 而`非系统`的 /etc

```ruby
[root@sp-64 hadoop-2.8.1]# vim etc/hadoop/hadoop-env.sh
```

#### **namenode running as process 7607. Stop it first.**

**原因是hadoop已经启动了, 需要先停止hadoop; 后续也会有相应的问题, 只要关闭重启对应的程序即可解决**

```null
[root@sp-64 hadoop-2.8.1]# ./sbin/stop-all.sh
```

### **使用jps命令查看进程是否启动成功**

```ruby
[root@sp-64 ~]# jps
21984 Jps
21838 NodeManager
21540 ResourceManager
[root@sp-64 ~]#
```

### **查看安装是否成功**

```ruby
[root@sp-64 ~]#
[root@sp-64 ~]# hadoop fs -ls /
Found 22 items
-rw-r--r-- 1 root root          0 2017-07-28 07:17 /.autorelabel
dr-xr-xr-x   - root root      20480 2017-09-04 10:37 /bin
dr-xr-xr-x   - root root       4096 2017-07-28 15:25 /boot
drwxr-xr-x   - root root       4096 2017-07-28 15:15 /data
drwxr-xr-x   - root root       3120 2017-08-25 02:20 /dev
drwxr-xr-x   - root root       4096 2017-09-04 10:43 /etc
drwxr-xr-x   - root root       4096 2017-09-04 10:27 /home
dr-xr-xr-x   - root root       4096 2017-07-28 07:20 /lib
dr-xr-xr-x   - root root      24576 2017-07-28 07:20 /lib64
drwx------ - root root      16384 2017-07-28 15:15 /lost+found
drwxr-xr-x   - root root       4096 2015-08-12 22:22 /media
drwxr-xr-x   - root root       4096 2015-08-12 22:22 /mnt
drwxr-xr-x   - root root       4096 2015-08-12 22:22 /opt
dr-xr-xr-x   - root root          0 2017-08-25 10:20 /proc
dr-xr-x--- - root root       4096 2017-09-04 10:51 /root
drwxr-xr-x   - root root        620 2017-08-25 10:20 /run
dr-xr-xr-x   - root root      20480 2017-07-28 07:20 /sbin
drwxr-xr-x   - root root       4096 2015-08-12 22:22 /srv
dr-xr-xr-x   - root root          0 2017-08-25 10:20 /sys
drwxrwxrwt   - root root       4096 2017-09-04 10:53 /tmp
drwxr-xr-x   - root root       4096 2017-09-04 10:37 /usr
drwxr-xr-x   - root root       4096 2017-08-25 10:20 /var
[root@sp-64 ~]#
# 安装成功
```

### **发送到其它分支服务器上, 并重复上面的步骤**

```ruby
[root@sp-64 myhadoop]# scp hadoop-2.8.1.tar.gz jdk-7u80-linux-x64.rpm root@sp-65:/home/myhadoop/
root@sp-65's password:
```

### **配置SSH免密, 不然每次启动hadoop都要输入好多次密码**

```ruby
[root@sp-64 ~]# ssh-keygen -t rsa -P ""
[root@sp-64 ~]# cd /root/.ssh/
[root@sp-64 .ssh]# ll
总用量 8
-rw------- 1 root root 1675 9月   4 15:26 id_rsa
-rw-r--r-- 1 root root  392 9月   4 15:26 id_rsa.pub
[root@sp-64 .ssh]#
[root@sp-64 .ssh]# cat id_rsa.pub >> authorized_keys
[root@sp-64 .ssh]# ll
总用量 12
-rw-r--r-- 1 root root  392 9月   4 15:26 authorized_keys
-rw------- 1 root root 1675 9月   4 15:26 id_rsa
-rw-r--r-- 1 root root  392 9月   4 15:26 id_rsa.pub
[root@sp-64 .ssh]#
```

### **配置 core-site.xml**

```ruby
[root@sp-64 hadoop-2.8.1]#
[root@sp-64 hadoop-2.8.1]# vim etc/hadoop/core-site.xml
<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>

<!-- Put site-specific property overrides in this file. -->

<configuration>

<property>
  <name>hadoop.tmp.dir</name>
  <value>/home/myhadoop/hadoop-2.8.1/tmp</value>
</property>

<property>
  <name>fs.defaultFS</name>
  <value>hdfs://sp-64:9000</value>
</property>

</configuration>
```

### **配置 hdfs-site.xml**

```ruby
[root@sp-64 hadoop-2.8.1]#
[root@sp-64 hadoop-2.8.1]# vim etc/hadoop/hdfs-site.xml
<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>

<!-- Put site-specific property overrides in this file. -->

<configuration>

  <property>
    <name>dfs.replication</name>
    <value>1</value>
  </property>

  <property>
    <name>dfs.namenode.name.dir</name>
    <value>file://${hadoop.tmp.dir}/dfs/name</value>
  </property>

  <property>
    <name>dfs.datanode.data.dir</name>
    <value>file://${hadoop.tmp.dir}/dfs/data</value>
  </property>

</configuration>
```

### **firewalld 开放50070端口**

```ruby
[root@sp-64 hadoop-2.8.1]# firewall-cmd --zone=public --add-port=50070/tcp --permanent
success
[root@sp-64 hadoop-2.8.1]# firewall-cmd --reload
success
[root@sp-64 hadoop-2.8.1]#
```

### **格式化Hadoop**

```ruby
[root@sp-64 hadoop-2.8.1]# hadoop namenode -format
DEPRECATED: Use of this script to execute hdfs command is deprecated.
Instead use the hdfs command for it.

17/09/04 11:44:23 INFO namenode.NameNode: STARTUP_MSG:
/************************************************************
# 中间内容太多, 在这里省略.
STARTUP_MSG:   java = 1.7.0_80
************************************************************/
# 中间内容太多, 在这里省略.
17/09/04 15:32:12 INFO util.ExitUtil: Exiting with status 0 # 这里等于0代表成功, 等于1 代表有错误.
17/09/04 15:32:12 INFO namenode.NameNode: SHUTDOWN_MSG:
/************************************************************
SHUTDOWN_MSG: Shutting down NameNode at sp-64/10.32.156.64
************************************************************/
[root@sp-64 hadoop-2.8.1]#
[root@sp-64 hadoop-2.8.1]# ./sbin/start-all.sh
[root@sp-64 hadoop-2.8.1]#
[root@sp-64 hadoop-2.8.1]# jps
8787 NameNode
8941 DataNode
9680 Jps
9127 SecondaryNameNode
[root@sp-64 hadoop-2.8.1]#
```

### **测试是hadoop 是否启动成功**

浏览器打开: http://10.32.156.64:50070
