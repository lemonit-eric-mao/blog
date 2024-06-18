---
title: 'Hadoop Hive CLI常用语句学习'
date: '2018-03-14T09:25:47+00:00'
status: publish
permalink: /2018/03/14/hadoop-hive-cli%e5%b8%b8%e7%94%a8%e8%af%ad%e5%8f%a5%e5%ad%a6%e4%b9%a0
author: 毛巳煜
excerpt: ''
type: post
id: 1983
category:
    - 大数据
tag: []
post_format: []
hestia_layout_select:
    - default
---
### CLI 常用语句 （进入命令行交互模式）

```
<pre class="line-numbers prism-highlight" data-start="1">```ruby
# 进入Hive
[root@sp-64 ~]# hive
# 或者 进入Hive 静默模式 加上 -S 执行语句时不会打印调试信息
[root@sp-64 ~]# hive -S


# 在Hive数据库中创建一张表
hive> create table Test1(tid int, tname string);
OK
Time taken: 0.552 seconds
hive>

# 查询Hive数据库中所有表
hive> show tables;
OK
test1
Time taken: 0.029 seconds, Fetched: 1 row(s)
hive>

# 查看表的结构
hive> desc test1;
OK
tid                     int
tname                   string
Time taken: 0.062 seconds, Fetched: 2 row(s)
hive>

# 插入一条数据
hive> INSERT INTO test1 (tid, tname) VALUES (1, 'maosiyu');
hive>

# 查看表中数据 （注：SELECT * 不会执行MapReduce， 而查询列时是会执行MapReduce的）
hive> SELECT * FROM test1;
OK
1   maosiyu
Time taken: 0.108 seconds, Fetched: 1 row(s)
hive>

# 递归查看 HDFS文件目录
hive> dfs -ls -R /user;
hive>

# 删除表
hive> drop table test1;
OK
Time taken: 1.244 seconds
hive>


```
```

### source 命令 执行 \*.sql 文件

**在服务器本地 /root/目录下创建一个my.sql文件**  
`这个source 命令与 mysql的 source 是一样的`

```
<pre class="line-numbers prism-highlight" data-start="1">```ruby
# 里面是sql语句
[root@sp-64 ~]# cat my.sql
SELECT * FROM test1;
[root@sp-64 ~]# hive
hive> source /root/my.sql;
OK
1   maosiyu
Time taken: 0.112 seconds, Fetched: 1 row(s)
hive>

```
```

### 不进入 交互模式 也可执行 hive语句

`hive -e '语句'`

```
<pre class="line-numbers prism-highlight" data-start="1">```ruby
[root@sp-64 ~]# hive -S -e 'SELECT * FROM test1';
1   maosiyu
[root@sp-64 ~]#
[root@sp-64 ~]# hive -S -e 'source /root/my.sql';
1   maosiyu
[root@sp-64 ~]#

```
```