---
title: 'Hadoop Spark 理论学习'
date: '2018-03-20T14:46:23+00:00'
status: publish
permalink: /2018/03/20/hadoop-spark-%e7%90%86%e8%ae%ba%e5%ad%a6%e4%b9%a0
author: 毛巳煜
excerpt: ''
type: post
id: 2037
category:
    - 大数据
tag: []
post_format: []
hestia_layout_select:
    - default
---
### spark 是什么？

`Spark是一个 快速 且 通用 的集群计算平台`

- Spark扩充了流行的Hadoop的 MapReduce计算模型，所以它比Hadoop更快
- Spark是基于内存的计算，当处理大批量的数据的时候，难免会产生中间的数据结果，那么中间的数据结果存放有两种：  
  第一种 就是存放在硬盘中，但会受到写入写出的消耗  
  第二种 就是存放在内存当中，所以速度非常快
- Spark 是通用的  
  Spark的设计容纳了其它分布式系统拥有的功能 如：  
  批处理（例如：Hadoop）,  
  迭代式计算（例如：机器学习）,  
  交互查询（例如：Hive）,  
  流处理（例如：Storm） 等

### Hadoop 与 Spark的区别

- Hadoop 的应用场景  
  离线处理  
  对时效性要求 不高 的场景
- Spark 的应用场景  
  对时效性要求 高 的场景  
  机器学习等领域

- - - - - -

- - - - - -

- - - - - -

### Spark 安装

[官方仓库](http://archive.apache.org/dist "官方仓库")  
[spark下载地址](http://archive.apache.org/dist/spark/spark-2.3.0/spark-2.3.0-bin-hadoop2.7.tgz "spark下载地址")  
`安装Spark不需要安装Hadoop`

```
<pre class="line-numbers prism-highlight" data-start="1">```ruby
[root@sp-64 home]# mkdir myspark
[root@sp-64 home]# cd myspark/
[root@sp-64 myspark]#
[root@sp-64 myspark]# wget http://archive.apache.org/dist/spark/spark-2.3.0/spark-2.3.0-bin-hadoop2.7.tgz
[root@sp-64 myspark]#
[root@sp-64 myspark]# tar -xzvf spark-2.3.0-bin-hadoop2.7.tgz
[root@sp-64 myspark]# ll
总用量 220840
drwxr-xr-x 13 1311767953 1876110778      4096 2月  23 03:42 spark-2.3.0-bin-hadoop2.7
-rw-r--r--  1 root       root       226128401 2月  23 03:54 spark-2.3.0-bin-hadoop2.7.tgz
[root@sp-64 myspark]#

```
```

### 配置环境变量

```
<pre class="line-numbers prism-highlight" data-start="1">```ruby
[root@sp-64 bin]# pwd
/home/myspark/spark-2.3.0-bin-hadoop2.7/bin
[root@sp-64 bin]# vim /etc/profile

export SPARK_HOME=/home/myspark/spark-2.3.0-bin-hadoop2.7
export PATH=<span class="katex math inline">SPARK_HOME/bin:</span>PATH

[root@sp-64 bin]#
[root@sp-64 bin]# source /etc/profile

```
```

### 启动 Spark

```
<pre class="line-numbers prism-highlight" data-start="1">```ruby
[root@sp-64 bin]# spark-shell
2018-03-20 16:55:19 WARN  NativeCodeLoader:62 - Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
Setting default log level to "WARN".
To adjust logging level use sc.setLogLevel(newLevel). For SparkR, use setLogLevel(newLevel).
Spark context Web UI available at http://sp-64:4040
Spark context available as 'sc' (master = local[*], app id = local-1521536125136).
Spark session available as 'spark'.
Welcome to
      ____              __
     / __/__  ___ _____/ /__
    _\ \/ _ \/ _ `/ __/  '_/
   /___/ .__/\_,_/_/ /_/\_\   version 2.3.0
      /_/

Using Scala version 2.11.8 (OpenJDK 64-Bit Server VM, Java 1.8.0_161)
Type in expressions to have them evaluated.
Type :help for more information.

scala>

```
```

**到这里我需要暂停了，做为一名编辑爱好者是不应该拒绝任何的编辑语言的， 所以需要学习一下`Scala`**