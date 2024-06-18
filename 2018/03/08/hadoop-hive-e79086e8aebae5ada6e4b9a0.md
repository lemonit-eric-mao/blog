---
title: 'Hadoop  Hive 理论学习'
date: '2018-03-08T15:23:32+00:00'
status: publish
permalink: /2018/03/08/hadoop-hive-%e7%90%86%e8%ae%ba%e5%ad%a6%e4%b9%a0
author: 毛巳煜
excerpt: ''
type: post
id: 1959
category:
    - 大数据
tag: []
post_format: []
hestia_layout_select:
    - default
---
什么是 Hive
========

`Hive是建立在Hadoop HDFS之上的数据仓库，也就是说Hive这个数据仓库中的数据是保存在HDFS上的。`

#### 数据仓库 （只做查询）

`数据仓库是一个面向主题的、集成的、可以更新的、随时间不变化的 数据集合;`

#### Hive 的应用场景

`它用于支持企业或组织的决策分析处理`

#### 面向主题

`个人理解， 直白的讲就是你要实现的目标， 实现这个目标可能会需要从不同种类的数据源中得到信息，所以需要 Hive`

### Hive 的三种安装模式

- 嵌入模式 （用于演示）  
  `嵌入模式是Hive将元数据信息存储到Hive自带的Derby数据库当中;`  
  **局限： 它只允许创建一个连接，这就意味着同一时间只能有一个人操作Hive数据仓库中的数据，所以这种方式只用于演示使用！**
- 本地模式 （用于开发和测试）  
  `本地模式是Hive将元数据信息存储到另外的一个数据库上，通常来讲被存储在MySql数据库，很明显MySql不属于Hive整体的框架所以这种模式和嵌入模式是不一样的`  
  **本地模式是指 MySql数据库与Hive运行在同一台物理机上，这就叫本地模式， 多用于开发和测试， 不会用在生产环境**
- 远程模式 （用于生产环境）  
  `远程模式是Hive将元数据信息存储到MySql数据库当中，而MySql数据库与Hive运行在不同的操作系统上，这种方式多用于生产环境，它允许创建多个连接。`

**下载安装**
--------

[Apache软件基础分发目录](http://archive.apache.org/dist/ "Apache软件基础分发目录")  
[apache-hive-2.3.2-bin.tar.gz](http://archive.apache.org/dist/hive/hive-2.3.2/ "apache-hive-2.3.2-bin.tar.gz")

### 从Apache官网下载Hive

```
<pre class="line-numbers prism-highlight" data-start="1">```ruby
[root@sp-64 home]# mkdir myhive
[root@sp-64 home]# cd myhive/
[root@sp-64 myhive]# wget http://archive.apache.org/dist/hive/hive-2.3.2/apache-hive-2.3.2-bin.tar.gz
[root@sp-64 myhive]#
[root@sp-64 myhive]# tar -xzvf apache-hive-2.3.2-bin.tar.gz
[root@sp-64 myhive]# cd apache-hive-2.3.2-bin
[root@sp-64 apache-hive-2.3.2-bin]# ll
总用量 84
drwxr-xr-x 3 root root  4096 3月  13 11:13 bin
drwxr-xr-x 2 root root  4096 3月  13 11:13 binary-package-licenses
drwxr-xr-x 2 root root  4096 3月  13 11:13 conf
drwxr-xr-x 4 root root  4096 3月  13 11:13 examples
drwxr-xr-x 7 root root  4096 3月  13 11:13 hcatalog
drwxr-xr-x 2 root root  4096 3月  13 11:13 jdbc
drwxr-xr-x 4 root root 20480 3月  13 11:13 lib
-rw-r--r-- 1 root root 20798 11月 10 00:26 LICENSE
-rw-r--r-- 1 root root   230 11月 10 00:26 NOTICE
-rw-r--r-- 1 root root  1979 11月 10 00:58 RELEASE_NOTES.txt
drwxr-xr-x 4 root root  4096 3月  13 11:13 scripts
[root@sp-64 apache-hive-2.3.2-bin]#

```
```

### 配置 Hive环境变量

```
<pre class="line-numbers prism-highlight" data-start="1">```ruby
[root@sp-64 apache-hive-2.3.2-bin]# vim /etc/profile
# 插入以下代码
export HIVE_HOME=/home/myhive/apache-hive-2.3.2-bin
export PATH=<span class="katex math inline">HIVE_HOME/bin:</span>PATH

# 刷新环境变量
[root@sp-64 apache-hive-2.3.2-bin]# source /etc/profile
# 直接输入 hive 测试是否配置成功
[root@sp-64 apache-hive-2.3.2-bin]# hive
# ......省略信息 能够进入 Hive表示已经配置成功
hive>

```
```

### 远程模式 配置

`我的MySql安装在了 10.32.156.51：3306 这台服务器上，使用Navicat 创建一个名为hive的数据库`

### 为Hive 添加MySql数据库驱动

- [官方下载MySql驱动](https://dev.mysql.com/downloads/connector/j/ "官方下载MySql驱动")

```
<pre class="line-numbers prism-highlight" data-start="1">```ruby
[root@sp-64 test-file]# wget https://cdn.mysql.com//Downloads/Connector-J/mysql-connector-java-5.1.46.tar.gz
[root@sp-64 test-file]#

```
```

- 添加MySql驱动到 /home/myhive/apache-hive-2.3.2-bin/lib 目录下

```
<pre class="line-numbers prism-highlight" data-start="1">```ruby
# 解压文件， 我一开始忘记解压了，直接传到目录，hive怎么初始化都是错的; 做这一步时要注意
[root@sp-64 test-file]# tar -xzvf mysql-connector-java-5.1.46.tar.gz
[root@sp-64 test-file]#
[root@sp-64 test-file]# cd mysql-connector-java-5.1.46
[root@sp-64 test-file]#
[root@sp-64 mysql-connector-java-5.1.46]# ll
总用量 2452
-rw-r--r-- 1 root root   91845 2月  26 21:28 build.xml
-rw-r--r-- 1 root root  247456 2月  26 21:28 CHANGES
-rw-r--r-- 1 root root   18122 2月  26 21:28 COPYING
-rw-r--r-- 1 root root 1004840 2月  26 21:28 mysql-connector-java-5.1.46-bin.jar
-rw-r--r-- 1 root root 1004838 2月  26 21:28 mysql-connector-java-5.1.46.jar
-rw-r--r-- 1 root root   61407 2月  26 21:28 README
-rw-r--r-- 1 root root   63658 2月  26 21:28 README.txt
drwxr-xr-x 8 root root    4096 2月  26 21:28 src
[root@sp-64 mysql-connector-java-5.1.46]#
[root@sp-64 mysql-connector-java-5.1.46]# cp mysql-connector-java-5.1.46-bin.jar /home/myhive/apache-hive-2.3.2-bin/lib/

```
```

### 创建 hive-site.xml 文件

```
<pre class="line-numbers prism-highlight" data-start="1">```ruby
[root@sp-64 ~]# cd /home/myhive/apache-hive-2.3.2-bin/conf
[root@sp-64 conf]# vim hive-site.xml

```
```

```
<pre class="line-numbers prism-highlight" data-start="1">```xml
<?xml version="1.0"??>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"??>

<configuration>

    <property>
        <name>javax.jdo.option.ConnectionURL</name>
        
        <value>jdbc:mysql://10.32.156.51:3306/hive?createDatabaseIfNotExist=true</value>
    </property>

    <property>
        <name>javax.jdo.option.ConnectionDriverName</name>
        <value>com.mysql.jdbc.Driver</value>
    </property>

    <property>
        <name>javax.jdo.option.ConnectionUserName</name>
        
        <value>root</value>
    </property>

    <property>
        <name>javax.jdo.option.ConnectionPassword</name>
        
        <value>yan8636396</value>
    </property>

</configuration>

```
```

### 初始化 Hive 初始化MySql数据库

`schematool 在 /home/myhive/apache-hive-2.3.2-bin/bin 这里`

```
<pre class="line-numbers prism-highlight" data-start="1">```ruby
[root@sp-64 ～]# schematool -initSchema -dbType mysql
# ......省略中间的细节 出现如下字样表示成功
schemaTool completed

```
```

`这个命令执行成功以后， 远程的hive数据库中就会生成好多的表。`

### 测试

```
<pre class="line-numbers prism-highlight" data-start="1">```ruby
[root@sp-64 bin]# hive
# ......省略中间的细节 出现如下字样表示成功
hive>

```
```