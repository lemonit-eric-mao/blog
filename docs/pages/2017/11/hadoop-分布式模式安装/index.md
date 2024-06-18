---
title: "Hadoop 分布式模式安装"
date: "2017-11-16"
categories: 
  - "大数据"
---

# **书接上文**

### **配置其余剩下的服务器**

服务器列表: \* 10.32.156.65 sp-65 \* 10.32.156.66 sp 66 \* 10.32.156.67 sp-67

### **所有节点服务器 新建用户 用户名 myhadoop 密码 123456**

```ruby
[root@localhost ~]# adduser myhadoop
[root@localhost ~]# passwd myhadoop
更改用户 myhadoop 的密码 。
新的 密码：
无效的密码： 密码少于 8 个字符
重新输入新的 密码：
passwd：所有的身份验证令牌已经成功更新。
[root@localhost ~]#
```

### **所有节点服务器 修改hosts**

```ruby
[root@localhost ~]# echo "
10.32.156.64 sp-64
10.32.156.65 sp-65
10.32.156.66 sp-66
10.32.156.67 sp-67
" >> /etc/hosts
[root@localhost ~]#
[root@localhost ~]# hostname sp-65
[root@localhost ~]# exit
```

### **所有节点服务器 配置ssh 免密**

```ruby
[root@sp-64 ~]# ssh-keygen -t rsa -P ""
[root@sp-64 ~]# cd .ssh/
[root@sp-64 .ssh]# ll
总用量 20
-rw-r--r-- 1 root root  392 9月   4 15:50 authorized_keys
-rw------- 1 root root 1675 9月   4 15:50 id_rsa
-rw-r--r-- 1 root root  392 9月   4 15:50 id_rsa.pub
-rw-r--r-- 1 root root  700 9月   4 17:02 known_hosts
-rw-r--r-- 1 root root  392 9月   4 17:02 root@sp-65
[root@sp-64 .ssh]#
[root@sp-64 .ssh]# scp authorized_keys root@sp-65:~/.ssh/
# 切换到子节点服务器
[root@sp-65 .ssh]# cat id_rsa.pub >> authorized_keys
[root@sp-65 .ssh]# scp authorized_keys root@sp-64:~/.ssh/
```

### **配置java环境变量 与 hadoop环境变量, 在上一篇文章中有配置方法.**

### **所有节点服务器 停止并关闭防火墙**

```ruby
[root@sp-64 ~]# systemctl disable firewalld
[root@sp-64 ~]# systemctl stop firewalld
```

### **替换所有节点服务器 配置文件**

```ruby
[root@sp-64 hadoop]# scp core-site.xml hdfs-site.xml sp-65:/home/myhadoop/hadoop-2.8.1/etc/hadoop/
core-site.xml                                                                                                         100%  966     0.9KB/s   00:00
hdfs-site.xml                                                                                                         100% 1098     1.1KB/s   00:00
[root@sp-64 hadoop]# scp core-site.xml hdfs-site.xml sp-66:/home/myhadoop/hadoop-2.8.1/etc/hadoop/
core-site.xml                                                                                                         100%  966     0.9KB/s   00:00
hdfs-site.xml                                                                                                         100% 1098     1.1KB/s   00:00
[root@sp-64 hadoop]# scp core-site.xml hdfs-site.xml sp-67:/home/myhadoop/hadoop-2.8.1/etc/hadoop/
core-site.xml                                                                                                         100%  966     0.9KB/s   00:00
hdfs-site.xml                                                                                                         100% 1098     1.1KB/s   00:00
[root@sp-64 hadoop]#
```

### **启动所有节点服务器**

```ruby
[root@sp-65 ~]# hadoop namenode -format
[root@sp-65 /]# ./home/myhadoop/hadoop-2.8.1/sbin/start-dfs.sh

[root@sp-66 ~]# hadoop namenode -format
[root@sp-66 /]# ./home/myhadoop/hadoop-2.8.1/sbin/start-dfs.sh

[root@sp-67 ~]# hadoop namenode -format
[root@sp-67 /]# ./home/myhadoop/hadoop-2.8.1/sbin/start-dfs.sh
```

### **各个节点的 jps 状态**

```ruby
[root@sp-64 ~]# jps
7592 SecondaryNameNode
7406 DataNode
8079 Jps
7919 NameNode
[root@sp-64 ~]#

[root@sp-65 ~]# jps
26653 SecondaryNameNode
26850 Jps
26467 DataNode
[root@sp-65 ~]#

[root@sp-66 ~]# jps
21868 SecondaryNameNode
22151 Jps
21691 DataNode
[root@sp-66 ~]#

[root@sp-67 ~]# jps
20594 DataNode
21094 Jps
20771 SecondaryNameNode
[root@sp-67 ~]#
```

## **测试 HDFS 是否安装成功**

```ruby
[root@sp-64 ~]#
[root@sp-64 ~]# hadoop fs -mkdir /user
[root@sp-64 ~]# hadoop fs -mkdir /user/hadoop
[root@sp-64 ~]# hadoop fs -mkdir /user/hadoop/input
# 创建测试文件
[root@sp-64 ~]#
[root@sp-64 ~]# touch test.txt
# 添加测试内容
[root@sp-64 ~]#
[root@sp-64 ~]# echo "
Hello world
Hello world
Hello world
Hello world
" >> test.txt
```

### **将文件上传到 HDFS系统**

```ruby
[root@sp-64 ~]#
# 将文件上传到 HDFS系统的input文件夹下
[root@sp-64 ~]# hadoop fs -put test.txt /user/hadoop/input/
# 查看是否上传成功
[root@sp-64 ~]# hadoop fs -ls /user/hadoop/input/
Found 1 items
-rw-r--r-- 1 root supergroup         50 2017-09-05 11:41 /user/hadoop/input/test.txt
[root@sp-64 ~]#
```

### **下载hadoop-examples-1.2.1.jar 到 /home/myhadoop/hadoop-2.8.1目录**

```ruby
[root@sp-64 hadoop-2.8.1]# cd /home/myhadoop/hadoop-2.8.1
[root@sp-64 hadoop-2.8.1]# wget http://central.maven.org/maven2/org/apache/hadoop/hadoop-examples/1.2.1/hadoop-examples-1.2.1.jar
[root@sp-64 hadoop-2.8.1]#
```

### **测试**

```ruby
[root@sp-64 hadoop-2.8.1]# hadoop jar hadoop-examples-1.2.1.jar wordcount /user/hadoop/input/test.txt /user/hadoop/output
```

### **查看 结果**

```ruby
[root@sp-64 hadoop-2.8.1]# hadoop fs -ls /user/hadoop/output
Found 2 items
-rw-r--r-- 1 root supergroup          0 2017-09-05 12:16 /user/hadoop/output/_SUCCESS
-rw-r--r-- 1 root supergroup         16 2017-09-05 12:16 /user/hadoop/output/part-r-00000
[root@sp-64 hadoop-2.8.1]#
[root@sp-64 hadoop-2.8.1]# hadoop fs -text /user/hadoop/output/part-r-00000
Hello   4
world   4
[root@sp-64 hadoop-2.8.1]#
[root@sp-64 hadoop-2.8.1]# ssh sp-65
Last login: Tue Sep  5 10:08:08 2017 from sp-64
```

#### **所有节点服务器**

```ruby
[root@sp-65 ~]# hadoop fs -text /user/hadoop/output/part-r-00000
Hello   4
world   4
[root@sp-65 ~]#
[root@sp-65 ~]# ssh sp-66
Last login: Tue Sep  5 10:18:27 2017 from sp-65

[root@sp-66 ~]# hadoop fs -text /user/hadoop/output/part-r-00000
Hello   4
world   4
[root@sp-66 ~]#
[root@sp-66 ~]# ssh sp-67
Last login: Tue Sep  5 10:18:39 2017 from sp-66

[root@sp-67 ~]# hadoop fs -text /user/hadoop/output/part-r-00000
Hello   4
world   4
[root@sp-67 ~]#
```

#### **OK! 到这里所有节点的服务器安装结束并且测试成功!**
