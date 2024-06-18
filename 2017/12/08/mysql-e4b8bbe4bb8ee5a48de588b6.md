---
title: 'MySql 主从复制'
date: '2017-12-08T16:45:45+00:00'
status: publish
permalink: /2017/12/08/mysql-%e4%b8%bb%e4%bb%8e%e5%a4%8d%e5%88%b6
author: 毛巳煜
excerpt: ''
type: post
id: 1730
category:
    - MySQL
tag: []
post_format: []
---
##### **系统环境**

```ruby
[root@localhost mysql]# cat /etc/redhat-release
CentOS Linux release 7.3.1611 (Core)

```

`Mysql 版本    5.7`  
`Master(主)    ip：10.32.156.56  server_id:56`  
`Slave(从)     ip：10.32.156.57  server_id:57`

- - - - - -

- - - - - -

#### **配置 主库**

##### **编辑Mysql配置文件**

```ruby
[root@localhost mysql]# vim /etc/my.cnf

```

```ruby
# For advice on how to change settings please see
# http://dev.mysql.com/doc/refman/5.7/en/server-configuration-defaults.html

[mysqld]
#
# Remove leading # and set to the amount of RAM for the most important data
# cache in MySQL. Start at 70% of total RAM for dedicated server, else 10%.
# innodb_buffer_pool_size = 128M
#
# Remove leading # to turn on a very important data integrity option: logging
# changes to the binary log between backups.
# log_bin
#
# Remove leading # to set options mainly useful for reporting servers.
# The server defaults are faster for transactions and fast SELECTs.
# Adjust sizes as needed, experiment to find the optimal values.
# join_buffer_size = 128M
# sort_buffer_size = 2M
# read_rnd_buffer_size = 2M
datadir=/var/lib/mysql
socket=/var/lib/mysql/mysql.sock

# Disabling symbolic-links is recommended to prevent assorted security risks
symbolic-links=0

log-error=/var/log/mysqld.log
pid-file=/var/run/mysqld/mysqld.pid

# 加入 server-id 一般取服务器IP地址的最后一组
server-id=56
# log-bin 会在上面 datadir指定的文件夹下输出, 这里就写 mysql-bin
log-bin=mysql-bin

```

##### **重启mysql**

```ruby
[root@localhost mysql]# systemctl restart mysqld
[root@localhost mysql]#

```

##### **进入 mysql**

```ruby
[root@localhost ~]# mysql -u root -p
Enter password:
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 7
Server version: 5.7.20 MySQL Community Server (GPL)

Copyright (c) 2000, 2017, Oracle and/or its affiliates. All rights reserved.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql>

```

##### **在 mysql 中 执行 `show master status;` 如下信息表示 Master 配置成功**

```ruby
mysql> show master status;
+------------------+----------+--------------+------------------+-------------------+
| File             | Position | Binlog_Do_DB | Binlog_Ignore_DB | Executed_Gtid_Set |
+------------------+----------+--------------+------------------+-------------------+
| mysql-bin.000001 |      154 |              |                  |                   |
+------------------+----------+--------------+------------------+-------------------+
1 row in set (0.00 sec)

mysql>

```

- - - - - -

- - - - - -

#### **配置 从库**

##### **编辑Mysql配置文件**

```ruby
[root@localhost mysql]# vim /etc/my.cnf

```

```ruby
# For advice on how to change settings please see
# http://dev.mysql.com/doc/refman/5.7/en/server-configuration-defaults.html

[mysqld]
#
# Remove leading # and set to the amount of RAM for the most important data
# cache in MySQL. Start at 70% of total RAM for dedicated server, else 10%.
# innodb_buffer_pool_size = 128M
#
# Remove leading # to turn on a very important data integrity option: logging
# changes to the binary log between backups.
# log_bin
#
# Remove leading # to set options mainly useful for reporting servers.
# The server defaults are faster for transactions and fast SELECTs.
# Adjust sizes as needed, experiment to find the optimal values.
# join_buffer_size = 128M
# sort_buffer_size = 2M
# read_rnd_buffer_size = 2M
datadir=/var/lib/mysql
socket=/var/lib/mysql/mysql.sock

# Disabling symbolic-links is recommended to prevent assorted security risks
symbolic-links=0

log-error=/var/log/mysqld.log
pid-file=/var/run/mysqld/mysqld.pid

# 配置从库需要加入如下的配置项
log-bin=mysql-bin
# server-id 是必须并且唯一的, 不能与主库一样
server-id=57
# 配置中继日志
relay-log=mysql-relay-bin
# 表示slave将复制事件写进自己的二进制日志
log-slave-updates=1
read-only=1

```

##### **重启 mysql**

```ruby
[root@localhost mysql]# systemctl restart mysqld
[root@localhost mysql]#

```

##### **进入Mysql**

```ruby
[root@localhost ~]# mysql -uroot -p
Enter password:
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 3
Server version: 5.7.24-log MySQL Community Server (GPL)

Copyright (c) 2000, 2018, Oracle and/or its affiliates. All rights reserved.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql>

```

##### **使用 `change master to` 语句为从库 指定主库**

```ruby
mysql> change master to master_host='10.32.156.56',
       master_user='root',
       master_password='Root#123',
       master_log_file='mysql-bin.000001', # 上面主库show master status的File值
       master_log_pos=154; # 上面主库show master status 的 Position值
Query OK, 0 rows affected, 2 warnings (0.01 sec)
mysql>

```

##### **启动复制**

```ruby
mysql> start slave;
Query OK, 0 rows affected (0.00 sec)

```

##### **查看运行状态**

```ruby
mysql> show slave status\G;
*************************** 1. row ***************************
               Slave_IO_State: Waiting for master to send event
                  Master_Host: 10.32.156.56
                  Master_User: root
                  Master_Port: 3306
                Connect_Retry: 60
              Master_Log_File: mysql-bin.000001
          Read_Master_Log_Pos: 154
               Relay_Log_File: mysql-relay-bin.000002
                Relay_Log_Pos: 320
        Relay_Master_Log_File: mysql-bin.000001
             Slave_IO_Running: Yes
            Slave_SQL_Running: Yes
              Replicate_Do_DB:
          Replicate_Ignore_DB:
           Replicate_Do_Table:
       Replicate_Ignore_Table:
      Replicate_Wild_Do_Table:
  Replicate_Wild_Ignore_Table:
                   Last_Errno: 0
                   Last_Error:
                 Skip_Counter: 0
          Exec_Master_Log_Pos: 154
              Relay_Log_Space: 527
              Until_Condition: None
               Until_Log_File:
                Until_Log_Pos: 0
           Master_SSL_Allowed: No
           Master_SSL_CA_File:
           Master_SSL_CA_Path:
              Master_SSL_Cert:
            Master_SSL_Cipher:
               Master_SSL_Key:
        Seconds_Behind_Master: 0
Master_SSL_Verify_Server_Cert: No
                Last_IO_Errno: 0
                Last_IO_Error:
               Last_SQL_Errno: 0
               Last_SQL_Error:
  Replicate_Ignore_Server_Ids:
             Master_Server_Id: 56
                  Master_UUID: 67a17bbe-dbe5-11e7-8ad5-0050569872f1
             Master_Info_File: /var/lib/mysql/master.info
                    SQL_Delay: 0
          SQL_Remaining_Delay: NULL
      Slave_SQL_Running_State: Slave has read all relay log; waiting for more updates
           Master_Retry_Count: 86400
                  Master_Bind:
      Last_IO_Error_Timestamp:
     Last_SQL_Error_Timestamp:
               Master_SSL_Crl:
           Master_SSL_Crlpath:
           Retrieved_Gtid_Set:
            Executed_Gtid_Set:
                Auto_Position: 0
         Replicate_Rewrite_DB:
                 Channel_Name:
           Master_TLS_Version:
1 row in set (0.00 sec)

ERROR:
No query specified

mysql>

```

`主要是看这两条: Slave_IO_Running: Yes    Slave_SQL_Running: Yes`

###### 测试 在主mysql服务器上新建一个数据库, 然后在从mysql服务器上查看, 也会有一个一模一样的数据库就对了.