---
title: "Hadoop Hive学习 数据迁移框架 Sqoop-1.99.7"
date: "2018-03-17"
categories: 
  - "大数据"
---

### 简述

**在使用Sqoop之前， 我的mysql中有20多万条测试数据，要把这些数据导入到Hive中** **根据之前学到的知识点，先在Hive中创建了与mysql表结构相同的表，然后在使用navicat导出sql文，简单的修改一下sql语句， 然后在Hive中使用 source /root/my.sql文件的方式进行上传，结果20MB的数据用了3个多小时才导入成功！** **这简直是最愚蠢的做法！！！** `所以接下来，非常有必要的好好学习一下 Sqoop这个专业操作数据导入/导出的开源框架！`

# 首先声明 sqoop 1.4.x 都不兼容 hadoop 2.8.x 我之前有一篇踩坑的文章 用了三天的时间才弃坑

### 下载Sqoop

[官方下载地址](http://archive.apache.org/dist/sqoop/1.99.7/sqoop-1.99.7-bin-hadoop200.tar.gz "官方下载地址")

### 下载/解压

```ruby
[root@sp-64 home]# mkdir mysqoop
[root@sp-64 home]# cd mysqoop/
[root@sp-64 mysqoop]# wget http://archive.apache.org/dist/sqoop/1.99.7/sqoop-1.99.7-bin-hadoop200.tar.gz
[root@sp-64 mysqoop]# tar -xzvf sqoop-1.99.7-bin-hadoop200.tar.gz
[root@sp-64 mysqoop]#
```

### 配置环境变量

```ruby
[root@sp-64 ~]# vim /etc/profile
export HADOOP_HOME=/home/myhadoop/hadoop-2.8.1
export PATH=$HADOOP_HOME/bin:$PATH

export HIVE_HOME=/home/myhive/apache-hive-2.3.2-bin
export PATH=$HIVE_HOME/bin:$PATH

export SQOOP_HOME=/home/mysqoop/sqoop-1.99.7-bin-hadoop200
export PATH=$SQOOP_HOME/bin:$PATH
[root@sp-64 ~]#  source /etc/profile
```

### 修改 Hadoop core-site.xml

**要给当前用户添加权限，要不然sqoop会没有权限操作hadoop， 当执行 start job 时会出现 `Caused by: Exception: java.lang.Throwable Message: User: root is not allowed`这个异常**

```markup
<configuration>
    <property>
      <name>hadoop.tmp.dir</name>
      <value>/home/myhadoop/hadoop-2.8.1/tmp</value>
    </property>

    <property>
      <name>fs.defaultFS</name>
      <value>hdfs://sp-64:9000</value>
    </property>

    <!-- 赋予root用户权限 -->
    <property>
      <!-- 如果用户是 msy 那这里就是hadoop.proxyuser.msy.hosts -->
      <name>hadoop.proxyuser.root.hosts</name>
      <value>*</value>
    </property>
    <property>
      <!-- 如果用户是 msy 那这里就是hadoop.proxyuser.msy.groups -->
      <name>hadoop.proxyuser.root.groups</name>
      <value>*</value>
    </property>
</configuration>
```

### 配置 sqoop 服务器端

```ruby
[root@sp-64 conf]# pwd
/home/mysqoop/sqoop-1.99.7-bin-hadoop200/conf
[root@sp-64 conf]# vim sqoop.properties
# 找到下面这行代码修改成自己的 $HADOOP_HOME/etc/hadoop/
# Hadoop configuration directory
#org.apache.sqoop.submission.engine.mapreduce.configuration.directory=/etc/hadoop/conf/
org.apache.sqoop.submission.engine.mapreduce.configuration.directory=/home/myhadoop/hadoop-2.8.1/etc/hadoop/
[root@sp-64 conf]#
# 启动服务器
[root@sp-64 conf]# sqoop2-server start
Starting the Sqoop2 server...
# ......省略中间信息
Sqoop2 server started.
[root@sp-64 conf]#
```

### 进入 sqoop 客户端

```ruby
[root@sp-64 conf]# sqoop2-shell
Setting conf dir: /home/mysqoop/sqoop-1.99.7-bin-hadoop200/bin/../conf
Sqoop home directory: /home/mysqoop/sqoop-1.99.7-bin-hadoop200
三月 17, 2018 4:08:11 下午 java.util.prefs.FileSystemPreferences$1 run
信息: Created user preferences directory.
Sqoop Shell: Type 'help' or '\h' for help.

sqoop:000>
```

#### 对于 verbose 这一项建议设置成为 true，它默认是 false，表示不会在输出过多信息。设置成 true 可以显示更多信息。

```ruby
sqoop:000> set option --name verbose --value true
Verbose option was changed to true
sqoop:000>
```

#### 这个必须要设置 此时只是启动了客户端，还没有连接服务端，如果测试创建link或者job，那么默认会连接localhost。所以，要先设置连接服务器：

```ruby
sqoop:000> set server --host 10.32.156.64 --port 12000 --webapp sqoop
Server is set successfully
```

#### 搜索 connector 测试 是否与服务端成功连接

**connector是用于创建link的模板，例如要创建hdfs的link，则使用hdfs-connector，要创建Oracle的link，则使用oracle-jdbc-connector或者generic-jdbc-connector 如果所设置的服务端连接是正常可用的，那么执行show connector 命令后，会显示如下：**

```ruby
sqoop:000> show connector
0    [main] WARN  org.apache.hadoop.util.NativeCodeLoader  - Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
+------------------------+---------+------------------------------------------------------------+----------------------+
|          Name          | Version |                           Class                            | Supported Directions |
+------------------------+---------+------------------------------------------------------------+----------------------+
| generic-jdbc-connector | 1.99.7  | org.apache.sqoop.connector.jdbc.GenericJdbcConnector       | FROM/TO              |
| kite-connector         | 1.99.7  | org.apache.sqoop.connector.kite.KiteConnector              | FROM/TO              |
| oracle-jdbc-connector  | 1.99.7  | org.apache.sqoop.connector.jdbc.oracle.OracleJdbcConnector | FROM/TO              |
| ftp-connector          | 1.99.7  | org.apache.sqoop.connector.ftp.FtpConnector                | TO                   |
| hdfs-connector         | 1.99.7  | org.apache.sqoop.connector.hdfs.HdfsConnector              | FROM/TO              |
| kafka-connector        | 1.99.7  | org.apache.sqoop.connector.kafka.KafkaConnector            | TO                   |
| sftp-connector         | 1.99.7  | org.apache.sqoop.connector.sftp.SftpConnector              | TO                   |
+------------------------+---------+------------------------------------------------------------+----------------------+
sqoop:000>
```

#### 如果配置不对会出现如果异常信息

```ruby
sqoop:000> show connector
0    [main] WARN  org.apache.hadoop.util.NativeCodeLoader  - Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
Exception has occurred during processing command 
Exception: java.net.ConnectException Message: 拒绝连接 (Connection refused)
sqoop:000>
```

#### 配置 HDFS 链接

```ruby
sqoop:000> create link --connector hdfs-connector
Creating link for connector with name hdfs-connector
Please fill following values to create new link object
Name: HDFS                                                      # （必填）

HDFS cluster

URI: hdfs://sp-64:9000                                          # HADOOP的fs.defaultFS的值 （必填）
Conf directory: /home/myhadoop/hadoop-2.8.1/etc/hadoop          # $HADOOP_HOME 环境变量下的文件夹 （必填）
Additional configs::                                            # （非必填）
There are currently 0 values in the map:
entry#                                                          # （非必填）
New link was successfully created with validation status OK and name HDFS
sqoop:000>

```

### 配置 MYSQL 连接

```ruby
sqoop:000> create link --connector generic-jdbc-connector
Creating link for connector with name generic-jdbc-connector
Please fill following values to create new link object
Name: MYSQL                                                     # （必填）

Database connection

Driver class: com.mysql.jdbc.Driver                             # MySQL数据库驱动名 com.mysql.jdbc.Driver （必填）
Connection String: jdbc:mysql://10.32.156.51:3306/bigdata_dlmap # 这里不能有 中杠线 （-） （必填）
Username: root                                                  # （必填）
Password: **********
Fetch Size:                                                     # （非必填）
Connection Properties:                                          # （非必填）
There are currently 0 values in the map:
entry#                                                          # （非必填）

SQL Dialect

Identifier enclose:                                             # 这里不能直接回车 需要打个空格 （必填）
Sat Mar 17 16:18:41 CST 2018 WARN: Establishing SSL connection without server's identity verification is not recommended. According to MySQL 5.5.45+, 5.6.26+ and 5.7.6+ requirements SSL connection must be established by default if explicit option isn't set. For compliance with existing applications not using SSL the verifyServerCertificate property is set to 'false'. You need either to explicitly disable SSL by setting useSSL=false, or set useSSL=true and provide truststore for server certificate verification.
New link was successfully created with validation status OK and name MYSQL
sqoop:000>

# 查看连接是否创建成功
sqoop:000> show link
+-------+------------------------+---------+
| Name  |     Connector Name     | Enabled |
+-------+------------------------+---------+
| MYSQL | generic-jdbc-connector | true    |
| HDFS  | hdfs-connector         | true    |
+-------+------------------------+---------+
sqoop:000>
```

### Mysql 导入到 Hdfs

#### 创建 Job

```ruby
sqoop:000> create job --from MYSQL --to HDFS
Creating job for links with from name MYSQL and to name HDFS
Please fill following values to create new job object
Name: MysqlToHDFSJob                                             # （必填）

Database source

Schema name: bigdata_dlmap                                       # （必填）
Table name: working_grid_data                                    # （必填）
SQL statement:                                                   # （非必填）
Column names:                                                    # （非必填）
There are currently 0 values in the list:
element#                                                         # （非必填）
Partition column:                                                # 主键（非必填）
Partition column nullable:                                       # （非必填）
Boundary query:                                                  # （非必填）

Incremental read

Check column:                                                    # （非必填）
Last value:                                                      # （非必填）

Target configuration

Override null value:                                             # （非必填）
Null value:                                                      # （非必填）
File format:                                                     # （非必填）
  0 : TEXT_FILE
  1 : SEQUENCE_FILE
  2 : PARQUET_FILE
Choose: 0                                                        # （必填）
Compression codec:                                               # （非必填）
  0 : NONE
  1 : DEFAULT
  2 : DEFLATE
  3 : GZIP
  4 : BZIP2
  5 : LZO
  6 : LZ4
  7 : SNAPPY
  8 : CUSTOM
Choose: 0                                                        # （必填）
Custom codec:                                                    # （非必填）
Output directory: /user/sqoop                                    # HDFS 输出路径（必填）
Append mode: true                                                # （非必填）

Throttling resources

Extractors:                                                      # （非必填）
Loaders:                                                         # （非必填）

Classpath configuration

Extra mapper jars:                                               # （非必填）
There are currently 0 values in the list:
element#                                                         # （非必填）
New job was successfully created with validation status OK  and name MysqlToHDFSJob
sqoop:000>
sqoop:000> show job
+----+----------------+--------------------------------+-----------------------+---------+
| Id |      Name      |         From Connector         |     To Connector      | Enabled |
+----+----------------+--------------------------------+-----------------------+---------+
| 1  | MysqlToHDFSJob | MYSQL (generic-jdbc-connector) | HDFS (hdfs-connector) | true    |
+----+----------------+--------------------------------+-----------------------+---------+
sqoop:000>
```

#### 启动Job 将mysql中数据导入到 HDFS中

```ruby
sqoop:000> start job --name MysqlToHDFSJob
sqoop:000> start job -n MysqlToHDFSJob
Submission details
Job Name: MysqlToHDFSJob
Server URL: http://localhost:12000/sqoop/
Created by: root
Creation date: 2018-03-19 13:13:48 CST
Lastly updated by: root
External ID: job_local1864885847_0003
    http://localhost:8080/
2018-03-19 13:13:48 CST: BOOTING  - Progress is not available
sqoop:000>
# 如果执行失败会有异常信息
```

### 查看 HDFS中的文件

```ruby
[root@sp-64 ~]# hadoop fs -ls /user/sqoop/
Found 10 items
-rw-r--r-- 1 root supergroup     248456 2018-03-19 13:13 /user/sqoop/3ea13d24-1f88-4803-85a2-279b729c7b87.txt
-rw-r--r-- 1 root supergroup     177679 2018-03-19 13:13 /user/sqoop/5137276d-012a-4220-b208-67056d415a05.txt
-rw-r--r-- 1 root supergroup     248218 2018-03-19 13:13 /user/sqoop/55c52d46-4984-4032-9fe9-da6844a0adbe.txt
-rw-r--r-- 1 root supergroup     248407 2018-03-19 13:13 /user/sqoop/5a7c37f3-e829-4214-ac34-7e0e51b5d4c4.txt
-rw-r--r-- 1 root supergroup     238496 2018-03-19 13:13 /user/sqoop/5e2d209d-d55e-414c-8ad1-84204867947f.txt
-rw-r--r-- 1 root supergroup     248432 2018-03-19 13:13 /user/sqoop/b12899cb-a1d2-4ee6-92a6-69fc055b9394.txt
-rw-r--r-- 1 root supergroup     188068 2018-03-19 13:13 /user/sqoop/d61f12c2-aaad-4af2-ae98-d95e81a0869c.txt
-rw-r--r-- 1 root supergroup     169216 2018-03-19 13:13 /user/sqoop/d6649c49-d573-4809-b9f5-3cd37c350e3f.txt
-rw-r--r-- 1 root supergroup     223962 2018-03-19 13:13 /user/sqoop/e04295de-ee93-4863-b105-e99dd9b569f9.txt
-rw-r--r-- 1 root supergroup     248495 2018-03-19 13:13 /user/sqoop/f6927724-600e-4769-bc83-bbe778a07014.txt
[root@sp-64 ~]#
```

### 将文件导入到 hive 中

`默认情况下 无论文件是否成功导入到hive， HDFS中的文件都会被清除！`

```ruby
# 在hive中创建能够存放数据的表
hive> CREATE TABLE test(smid int, wgcode string, wgname string, bdx string, bdy string) ROW FORMAT DELIMITED FIELDS TERMINATED BY ',' STORED AS TEXTFILE; # 指明 列与列之间的分隔符

# 导入数据 到Hive
hive> LOAD DATA INPATH '/user/sqoop/' INTO TABLE test;
Loading data to table default.test
OK
Time taken: 0.822 seconds
hive>
# 查看表中数据
hive> select * from  test;
```
