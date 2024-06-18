---
title: 'Hadoop Hive学习 数据迁移框架 Sqoop(不兼容的坑)'
date: '2018-03-15T14:18:43+00:00'
status: publish
permalink: /2018/03/15/hadoop-hive%e5%ad%a6%e4%b9%a0-%e6%95%b0%e6%8d%ae%e8%bf%81%e7%a7%bb%e6%a1%86%e6%9e%b6-sqoop%e4%b8%8d%e5%85%bc%e5%ae%b9%e7%9a%84%e5%9d%91
author: 毛巳煜
excerpt: ''
type: post
id: 1999
category:
    - 大数据
tag: []
post_format: []
hestia_layout_select:
    - default
---
### 简述

**在使用Sqoop之前， 我的mysql中有20多万条测试数据，要把这些数据导入到Hive中**  
**根据之前学到的知识点，先在Hive中创建了与mysql表结构相同的表，然后在使用navicat导出sql文，简单的修改一下sql语句， 然后在Hive中使用 source /root/my.sql文件的方式进行上传，结果20MB的数据用了3个多小时才导入成功！**  
**这简直是最愚蠢的做法！！！**  
`所以接下来，非常有必要的好好学习一下 Sqoop这个专业操作数据导入/导出的开源框架！`

### 下载Sqoop

[官方下载地址](http://archive.apache.org/dist/sqoop/1.4.7/sqoop-1.4.7.bin__hadoop-2.6.0.tar.gz "官方下载地址")

### 下载/解压

```
<pre class="line-numbers prism-highlight" data-start="1">```ruby
[root@sp-64 home]# mkdir mysqoop
[root@sp-64 home]# cd mysqoop/
[root@sp-64 mysqoop]# wget http://archive.apache.org/dist/sqoop/1.4.7/sqoop-1.4.7.bin__hadoop-2.6.0.tar.gz
[root@sp-64 mysqoop]# tar -xzvf sqoop-1.4.7.bin__hadoop-2.6.0.tar.gz
[root@sp-64 mysqoop]#

```
```

### 复制mysql数据库驱动到 Sqoop的lib/文件夹下

```
<pre class="line-numbers prism-highlight" data-start="1">```ruby
[root@sp-64 ~]# cp /home/test-file/mysql-connector-java-5.1.46/mysql-connector-java-5.1.46-bin.jar /home/mysqoop/sqoop-1.4.7.bin__hadoop-2.6.0/lib/
[root@sp-64 ~]#

```
```

### 配置环境变量

```
<pre class="line-numbers prism-highlight" data-start="1">```ruby
[root@sp-64 sqoop-1.4.7.bin__hadoop-2.6.0]# vim /etc/profile
# 加入这一条
export SQOOP_HOME=/home/mysqoop/sqoop-1.4.7.bin__hadoop-2.6.0
export PATH=<span class="katex math inline">SQOOP_HOME/bin:</span>PATH

[root@sp-64 sqoop-1.4.7.bin__hadoop-2.6.0]# source /etc/profile
[root@sp-64 sqoop-1.4.7.bin__hadoop-2.6.0]#

```
```

### 使用sqoop列出 远程mysql下的所有 数据库

```
<pre class="line-numbers prism-highlight" data-start="1">```ruby
[root@sp-64 ~]# sqoop list-databases --connect jdbc:mysql://10.32.156.50:3306 -username root -password yan8636396
information_schema
dlfc_bigdata
mysql
performance_schema
quartztest
sys
[root@sp-64 ~]#

```
```

### 使用sqoop列出 远程mysql下的 dlfc\_bigdata数据库 中的所有表

```
<pre class="line-numbers prism-highlight" data-start="1">```ruby
[root@sp-64 ~]# sqoop list-tables --connect jdbc:mysql://10.32.156.50:3306/dlfc_bigdata -username root -password yan8636396
dlfc_bd_basedata
dlfc_bd_basedata_backups
dlfc_bd_cleandata
dlfc_bd_cleandata_format
dlfc_bd_quartz_config
dlfc_bd_quartz_config_log
[root@sp-64 ~]#

```
```

### 从远程数据库中导入数据到 HDFS中

```
<pre class="line-numbers prism-highlight" data-start="1">```ruby
[root@sp-64 ~]# sqoop import --connect jdbc:mysql://10.32.156.50:3306/dlfc_bigdata -username root -password yan8636396 --table dlfc_bd_basedata_backups -m 1
# 部分异常 （说找不到dlfc_bd_basedata_backups这个类， 这是怎么回事儿 完全搞不懂。）
# .....代码太多部分省略
18/03/15 16:37:11 WARN mapred.LocalJobRunner: job_local109098066_0001
java.lang.Exception: java.lang.RuntimeException: java.lang.ClassNotFoundException: Class dlfc_bd_basedata_backups not found
    at org.apache.hadoop.mapred.LocalJobRunner<span class="katex math inline">Job.runTasks(LocalJobRunner.java:489)
    at org.apache.hadoop.mapred.LocalJobRunner</span>Job.run(LocalJobRunner.java:549)
Caused by: java.lang.RuntimeException: java.lang.ClassNotFoundException: Class dlfc_bd_basedata_backups not found
    at org.apache.hadoop.conf.Configuration.getClass(Configuration.java:2216)
# .....代码太多部分省略

```
```

### 解决方案 （一） 指定java编译后的文件目录

```
<pre class="line-numbers prism-highlight" data-start="1">```ruby
# 先使用 sqoop codegen 命令生成jar文件
[root@sp-64 ~]# sqoop codegen --connect jdbc:mysql://10.32.156.50:3306/dlfc_bigdata -username root -password yan8636396 --table dlfc_bd_basedata_backups

# 在使用 sqoop import -libjars 参数指定 jar包的位置
[root@sp-64 ~]# sqoop import -libjars /tmp/sqoop-root/compile/a6a893e8a24e6753d126a2a329209ff7/dlfc_bd_basedata_backups.jar --connect jdbc:mysql://10.32.156.50:3306/dlfc_bigdata -username root -password yan8636396 --table dlfc_bd_basedata_backups
# .....代码太多部分省略
18/03/16 14:31:58 INFO mapred.LocalJobRunner: map task executor complete.
18/03/16 14:31:59 INFO mapreduce.Job:  map 100% reduce 0%
18/03/16 14:31:59 INFO mapreduce.Job: Job job_local2075378699_0001 completed successfully
18/03/16 14:31:59 INFO mapreduce.Job: Counters: 20
    File System Counters
        FILE: Number of bytes read=24431274
        FILE: Number of bytes written=24976880
        FILE: Number of read operations=0
        FILE: Number of large read operations=0
        FILE: Number of write operations=0
        HDFS: Number of bytes read=0
        HDFS: Number of bytes written=17753125
        HDFS: Number of read operations=4
        HDFS: Number of large read operations=0
        HDFS: Number of write operations=3
    Map-Reduce Framework
        Map input records=28284
        Map output records=28284
        Input split bytes=87
        Spilled Records=0
        Failed Shuffles=0
        Merged Map outputs=0
        GC time elapsed (ms)=71
        Total committed heap usage (bytes)=385875968
    File Input Format Counters 
        Bytes Read=0
    File Output Format Counters 
        Bytes Written=17753125
18/03/16 14:31:59 INFO mapreduce.ImportJobBase: Transferred 16.9307 MB in 2.9985 seconds (5.6463 MB/sec)
18/03/16 14:31:59 INFO mapreduce.ImportJobBase: Retrieved 28284 records.
[root@sp-64 ~]#

```
```

### 解决方案 （二） 将java编译文件目录改为当前目录下

```
<pre class="line-numbers prism-highlight" data-start="1">```ruby
# 或者 直接使用 sqoop import --bindir ./ 这样所有的编译后的文件都生成在了当前目录下
[root@sp-64 ~]# sqoop import --bindir ./ --connect jdbc:mysql://10.32.156.50:3306/dlfc_bigdata -username root -password yan8636396 --table dlfc_bd_basedata_backups -m 1
# .....代码太多部分省略
18/03/16 15:55:33 INFO mapred.LocalJobRunner: map task executor complete.
18/03/16 15:55:34 INFO mapreduce.Job:  map 100% reduce 0%
18/03/16 15:55:34 INFO mapreduce.Job: Job job_local573823525_0001 completed successfully
18/03/16 15:55:34 INFO mapreduce.Job: Counters: 20
    File System Counters
        FILE: Number of bytes read=24421325
        FILE: Number of bytes written=24964358
        FILE: Number of read operations=0
        FILE: Number of large read operations=0
        FILE: Number of write operations=0
        HDFS: Number of bytes read=0
        HDFS: Number of bytes written=17753125
        HDFS: Number of read operations=4
        HDFS: Number of large read operations=0
        HDFS: Number of write operations=3
    Map-Reduce Framework
        Map input records=28284
        Map output records=28284
        Input split bytes=87
        Spilled Records=0
        Failed Shuffles=0
        Merged Map outputs=0
        GC time elapsed (ms)=67
        Total committed heap usage (bytes)=508035072
    File Input Format Counters 
        Bytes Read=0
    File Output Format Counters 
        Bytes Written=17753125
18/03/16 15:55:34 INFO mapreduce.ImportJobBase: Transferred 16.9307 MB in 2.9618 seconds (5.7163 MB/sec)
18/03/16 15:55:34 INFO mapreduce.ImportJobBase: Retrieved 28284 records.
[root@sp-64 ~]#

```
```

### 从远程数据库中导入数据到 Hive中(目前处于失败状态)

```
<pre class="line-numbers prism-highlight" data-start="1">```ruby
[root@sp-64 ~]# sqoop import --bindir ./ --connect jdbc:mysql://10.32.156.50:3306/dlfc_bigdata -username root -password yan8636396 --table dlfc_bd_basedata_backups -m 1 --hive-import
# .....代码太多部分省略
18/03/16 15:55:34 INFO hive.HiveImport: Loading uploaded data into Hive
18/03/16 15:55:34 ERROR hive.HiveConfig: Could not load org.apache.hadoop.hive.conf.HiveConf. Make sure HIVE_CONF_DIR is set correctly.
18/03/16 15:55:34 ERROR tool.ImportTool: Import failed: java.io.IOException: java.lang.ClassNotFoundException: org.apache.hadoop.hive.conf.HiveConf
    at org.apache.sqoop.hive.HiveConfig.getHiveConf(HiveConfig.java:50)
    at org.apache.sqoop.hive.HiveImport.getHiveArgs(HiveImport.java:392)
    at org.apache.sqoop.hive.HiveImport.executeExternalHiveScript(HiveImport.java:379)
    at org.apache.sqoop.hive.HiveImport.executeScript(HiveImport.java:337)
    at org.apache.sqoop.hive.HiveImport.importTable(HiveImport.java:241)
    at org.apache.sqoop.tool.ImportTool.importTable(ImportTool.java:537)
    at org.apache.sqoop.tool.ImportTool.run(ImportTool.java:628)
    at org.apache.sqoop.Sqoop.run(Sqoop.java:147)
    at org.apache.hadoop.util.ToolRunner.run(ToolRunner.java:76)
    at org.apache.sqoop.Sqoop.runSqoop(Sqoop.java:183)
    at org.apache.sqoop.Sqoop.runTool(Sqoop.java:234)
    at org.apache.sqoop.Sqoop.runTool(Sqoop.java:243)
    at org.apache.sqoop.Sqoop.main(Sqoop.java:252)
Caused by: java.lang.ClassNotFoundException: org.apache.hadoop.hive.conf.HiveConf
    at java.net.URLClassLoader.findClass(URLClassLoader.java:381)
    at java.lang.ClassLoader.loadClass(ClassLoader.java:424)
    at sun.misc.Launcher$AppClassLoader.loadClass(Launcher.java:338)
    at java.lang.ClassLoader.loadClass(ClassLoader.java:357)
    at java.lang.Class.forName0(Native Method)
    at java.lang.Class.forName(Class.java:264)
    at org.apache.sqoop.hive.HiveConfig.getHiveConf(HiveConfig.java:44)
    ... 12 more
[root@sp-64 ~]#

```
```

### 解决方案

```
<pre class="line-numbers prism-highlight" data-start="1">```ruby
[root@sp-64 ~]# vim /etc/profile
# 在系统环境变量中加入这一句
export HADOOP_CLASSPATH=$HIVE_HOME/lib/*
[root@sp-64 ~]#

# 结果又出现了这个 bug （我也是晕了， 放这儿放着吧， 想明白在说， 三天后找到原因了，就是1.4.x不兼容 hadoop 2.8.x）
18/03/16 16:43:23 INFO tool.CodeGenTool: Beginning code generation
Exception in thread "main" java.lang.NoClassDefFoundError: Could not initialize class org.apache.derby.jdbc.AutoloadedDriver40
    at java.lang.Class.forName0(Native Method)

```
```