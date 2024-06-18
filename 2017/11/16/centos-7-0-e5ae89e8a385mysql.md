---
title: 'Centos 7.0 安装mysql'
date: '2017-11-16T16:28:57+00:00'
status: publish
permalink: /2017/11/16/centos-7-0-%e5%ae%89%e8%a3%85mysql
author: 毛巳煜
excerpt: ''
type: post
id: 536
category:
    - MySQL
tag: []
post_format: []
wb_sst_seo:
    - 'a:3:{i:0;s:0:"";i:1;s:0:"";i:2;s:0:"";}'
hestia_layout_select:
    - sidebar-right
---
[转载/摘选自](http://www.cnblogs.com/baierfa/p/6688737.html)

##### **mysql 安装环境**

系统: centos 7  
地址: 10.32.156.52

##### **第一步 先去官网下载 rpm 源**

官网路径: http://repo.mysql.com/  
下载地址: http://repo.mysql.com/mysql57-community-release-el7-11.noarch.rpm

##### **下载rpm包**

```ruby
[root@localhost mysql]# wget http://repo.mysql.com/mysql57-community-release-el7-11.noarch.rpm
[root@localhost mysql]#
[root@localhost mysql]#  yum localinstall mysql57-community-release-el7-11.noarch.rpm
[root@localhost mysql]#

```

##### **安装mysql 社区版**

```ruby
[root@localhost mysql]# yum install mysql-community-server
.......
// 重启电脑

```

##### **启动MySQL服务**

```ruby
[root@sp-66 CDHInstallFile]# systemctl start mysqld
[root@sp-66 CDHInstallFile]#

```

##### **查看MySQL的启动状态**

```ruby
[root@sp-66 CDHInstallFile]# systemctl status mysqld
● mysqld.service - MySQL Server
   Loaded: loaded (/usr/lib/systemd/system/mysqld.service; enabled; vendor preset: disabled)
   Active: active (running) since 三 2017-07-26 09:19:39 CST; 49s ago
     Docs: man:mysqld(8)
           http://dev.mysql.com/doc/refman/en/using-systemd.html
  Process: 14138 ExecStart=/usr/sbin/mysqld --daemonize --pid-file=/var/run/mysqld/mysqld.pid $MYSQLD_OPTS (code=exited, status=0/SUCCESS)
  Process: 14064 ExecStartPre=/usr/bin/mysqld_pre_systemd (code=exited, status=0/SUCCESS)
 Main PID: 14142 (mysqld)
   CGroup: /system.slice/mysqld.service
           └─14142 /usr/sbin/mysqld --daemonize --pid-file=/var/run/mysqld/mysqld.pid

7月 26 09:19:36 sp-66 systemd[1]: Starting MySQL Server...
7月 26 09:19:39 sp-66 systemd[1]: Started MySQL Server.
[root@sp-66 CDHInstallFile]#

```

##### **开机启动**

```ruby
[root@sp-66 CDHInstallFile]# systemctl enable mysqld
[root@sp-66 CDHInstallFile]# systemctl daemon-reload
[root@sp-66 CDHInstallFile]#

```

##### **修改root默认密码**

**mysql安装完成之后，在/var/log/mysqld.log文件中给root生成了一个默认密码。通过下面的方式找到root默认密码，然后登录mysql进行修改，`必须要修改` !**

```ruby
[root@sp-66 CDHInstallFile]# grep 'temporary password' /var/log/mysqld.log
2017-07-26T01:19:37.091367Z 1 [Note] A temporary password is generated for root@localhost: d1+U?F;zp#er
[root@sp-66 CDHInstallFile]#

```

**登录mysql 修改root密码, 使用密码 `d1+U?F;zp#er` 进行登录**  
`注意：mysql5.7默认安装了密码安全检查插件（validate_password），默认密码检查策略要求密码必须包含：大小写字母、数字和特殊符号，并且长度不能少于8位。否则会提示: ERROR 1819 (HY000): Your password does not satisfy the current policy requirements`

```ruby
[root@sp-66 CDHInstallFile]# mysql -uroot -p
Enter password:
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 3
Server version: 5.7.42

Copyright (c) 2000, 2017, Oracle and/or its affiliates. All rights reserved.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql>
mysql> ALTER USER 'root'@'localhost' IDENTIFIED BY 'MysqlPasswd';
ERROR 1819 (HY000): Your password does not satisfy the current policy requirements
mysql> ALTER USER 'root'@'localhost' IDENTIFIED BY 'MysqlPasswd1234!';
Query OK, 0 rows affected (0.00 sec)

mysql>

```

##### 通过msyql环境变量可以查看密码策略的相关信息：

```ruby
mysql> show variables like '%password%';
+---------------------------------------+--------+
| Variable_name                         | Value  |
+---------------------------------------+--------+
| default_password_lifetime             | 0      |
| disconnect_on_expired_password        | ON     |
| log_builtin_as_identified_by_password | OFF    |
| mysql_native_password_proxy_users     | OFF    |
| old_passwords                         | 0      |
| report_password                       |        |
| sha256_password_proxy_users           | OFF    |
| validate_password_check_user_name     | OFF    |
| validate_password_dictionary_file     |        |
| validate_password_length              | 8      |
| validate_password_mixed_case_count    | 1      |
| validate_password_number_count        | 1      |
| validate_password_policy              | MEDIUM |
| validate_password_special_char_count  | 1      |
+---------------------------------------+--------+
14 rows in set (0.00 sec)

mysql>

```

1. validate\_password\_policy：密码策略，默认为MEDIUM策略
2. validate\_password\_dictionary\_file：密码策略文件，策略为STRONG才需要
3. validate\_password\_length：密码最少长度
4. validate\_password\_mixed\_case\_count：大小写字符长度，至少1个
5. validate\_password\_number\_count ：数字至少1个
6. validate\_password\_special\_char\_count：特殊字符至少1个 上述参数是默认策略MEDIUM的密码检查规则。  
  **MySQL官网密码策略详细说明：** http://dev.mysql.com/doc/refman/5.7/en/validate-password-options-variables.html#sysvar\_validate\_password\_policy

##### **修改密码策略**

在/etc/my.cnf文件添加validate\_password\_policy配置，指定密码策略  
选择0（LOW），1（MEDIUM），2（STRONG）其中一种，选择2需要提供密码字典文件  
validate\_password\_policy=0  
如果不需要密码策略，添加my.cnf文件中添加如下配置禁用即可：  
validate\_password = off  
重新启动mysql服务使配置生效：  
systemctl restart mysqld

##### **添加远程登录用户**

**默认只允许root帐户在本地登录，如果要在其它机器上连接mysql，必须修改root允许远程连接，或者添加一个允许远程连接的帐户，为了安全起见，添加一个新的帐户：**

```ruby
mysql> GRANT ALL PRIVILEGES ON *.* TO 'maosiyu'@'%' IDENTIFIED BY 'Maosiyu1987!' WITH GRANT OPTION;

```

##### 注意: 如果没有关闭防火墙, 远程访问有可能会报 access denied for user root @% 异常!!!