---
title: "大数据学习(三)  Cloudera-Manager 下载安装"
date: "2017-11-16"
categories: 
  - "大数据"
---

[转载/摘选自](http://www.cnblogs.com/baierfa/p/6688737.html)

[cloudera-manager 下载列表](http://archive.cloudera.com/cm5/cm/5) [parcel 下载列表](http://archive.cloudera.com/cdh5/parcels/5.10.2/)

#### 版本必须要一致, 当前应用的版本是:

http://archive.cloudera.com/cm5/cm/5/cloudera-manager-centos7-cm5.10.2\_x86\_64.tar.gz http://archive.cloudera.com/cdh5/parcels/5.10.2/CDH-5.10.2-1.cdh5.10.2.p0.5-el7.parcel http://archive.cloudera.com/cdh5/parcels/5.10.2/CDH-5.10.2-1.cdh5.10.2.p0.5-el7.parcel.sha1 http://archive.cloudera.com/cdh5/parcels/5.10.2/manifest.json

#### 下载mysql 驱动

https://dev.mysql.com/get/Downloads/Connector-J/mysql-connector-java-5.1.43.tar.gz

#### 将下载好的包全部放在 CDHInstallFile中

```ruby
[root@sp-66 ~]# mkdir /home/hadoop/CDHInstallFile
```

### 第三方依赖包 所有节点都安装

```ruby
[root@sp-66 CDHInstallFile]# yum install chkconfig python bind-utils psmisc libxslt zlib sqlite fuse fuse-libs redhat-lsb cyrus-sasl-plain cyrus-sasl-gssapi
```

#### 配置mysql驱动, 修改mysql驱动 jar包的名字，并拷贝到/usr/share/java/目录

```ruby
[root@sp-66 CDHInstallFile]# mkdir -p /usr/share/java
[root@sp-66 CDHInstallFile]# tar -xzvf mysql-connector-java-5.1.43.tar.gz
[root@sp-66 CDHInstallFile]# cd mysql-connector-java-5.1.43
[root@sp-66 mysql-connector-java-5.1.43]# ll
总用量 1456
-rw-r--r-- 1 root root  91463 7月   7 03:42 build.xml
-rw-r--r-- 1 root root 245279 7月   7 03:42 CHANGES
-rw-r--r-- 1 root root  18122 7月   7 03:42 COPYING
-rwxrwxrwx 1 root root 999018 7月   7 03:42 mysql-connector-java-5.1.43-bin.jar
-rw-r--r-- 1 root root  61407 7月   7 03:42 README
-rw-r--r-- 1 root root  63658 7月   7 03:42 README.txt
drwxr-xr-x 8 root root   4096 7月   7 03:42 src
[root@sp-66 mysql-connector-java-5.1.43]#
[root@sp-66 mysql-connector-java-5.1.43]# cp mysql-connector-java-5.1.43-bin.jar /usr/share/java/mysql-connector-java.jar
```

#### 解压cm tar包到指定目录，所有服务器都要

```ruby
[root@sp-66 CDHInstallFile]# mkdir /opt/cloudera-manager
[root@sp-66 CDHInstallFile]# tar -xzvf cloudera-manager-centos7-cm5.10.2_x86_64.tar.gz -C /opt/cloudera-manager/
```

#### 复制文件到各个节点

```ruby
[root@sp-66 CDHInstallFile]# scp cloudera-manager-centos7-cm5.10.2_x86_64.tar.gz root@10.32.156.67:/home/hadoop/CDHInstallFile/
```

#### 创建`cloudera-scm`用户（**所有节点**）

```ruby
[root@sp-66 CDHInstallFile]# useradd -r -d /opt/cloudera-manager/cm-5.10.2/run/cloudera-scm-server/ -M -c "Cloudera SCM User" cloudera-scm
[root@sp-66 CDHInstallFile]#
[root@sp-66 CDHInstallFile]# id cloudera-scm
uid=996(cloudera-scm) gid=994(cloudera-scm) 组=994(cloudera-scm)
[root@sp-66 CDHInstallFile]#
```

#### 配置从节点cloudera-manger-agent指向主节点服务器（根据集群的分配这里面应当全部节点都需要）

```ruby
[root@sp-66 CDHInstallFile]# vim /opt/cloudera-manager/cm-5.10.2/etc/cloudera-scm-agent/config.ini
[General]
# Hostname of the CM server.
# server_host=localhost
# 改为主节点名称
server_host=sp-66

# Port that the CM server is listening on.
server_port=7182
# 以下省略 .....
wq!
```

#### 主节点中创建parcel-repo仓库目录（这个只在主节点sp-66上需要）

```ruby
[root@sp-66 CDHInstallFile]# mkdir -p /opt/cloudera/parcel-repo
[root@sp-66 CDHInstallFile]# chown cloudera-scm:cloudera-scm /opt/cloudera/parcel-repo
[root@sp-66 CDHInstallFile]#
```

#### 将 \***.sha1** `文件重命名`为 \*\*\*.sha\*\* 必须要把 后面的1去掉

```ruby
[root@sp-66 CDHInstallFile]# ls
CDH-5.10.2-1.cdh5.10.2.p0.5-el7.parcel.sha1  cloudera-manager-centos7-cm5.10.2_x86_64.tar.gz  manifest.json
[root@sp-66 CDHInstallFile]# mv CDH-5.10.2-1.cdh5.10.2.p0.5-el7.parcel.sha1 CDH-5.10.2-1.cdh5.10.2.p0.5-el7.parcel.sha
[root@sp-66 CDHInstallFile]# ls
CDH-5.10.2-1.cdh5.10.2.p0.5-el7.parcel.sha  cloudera-manager-centos7-cm5.10.2_x86_64.tar.gz  manifest.json
[root@sp-66 CDHInstallFile]#
```

#### 将文件复制到 /opt/cloudera/parcel-repo

```ruby
[root@sp-66 CDHInstallFile]# ll
总用量 2168732
-rw-r--r-- 1 root root 1584033825 7月  25 15:57 CDH-5.10.2-1.cdh5.10.2.p0.5-el7.parcel
-rw-r--r-- 1 root root         41 7月  25 14:16 CDH-5.10.2-1.cdh5.10.2.p0.5-el7.parcel.sha
-rwxrwxrwx 1 root root  636662419 7月  25 14:40 cloudera-manager-centos7-cm5.10.2_x86_64.tar.gz
-rw-r--r-- 1 root root      64807 7月  25 15:33 manifest.json
[root@sp-66 CDHInstallFile]# cp CDH-5.10.2-1.cdh5.10.2.p0.5-el7.parcel CDH-5.10.2-1.cdh5.10.2.p0.5-el7.parcel.sha manifest.json /opt/cloudera/parcel-repo/
[root@sp-66 CDHInstallFile]#
```

#### 所有节点创建parcels目录（**所有节点**）

```ruby
[root@sp-66 CDHInstallFile]# mkdir -p /opt/cloudera/parcels
[root@sp-66 CDHInstallFile]# ll /opt/cloudera/
总用量 8
drwxr-xr-x 2 cloudera-scm cloudera-scm 4096 7月  25 16:18 parcel-repo
drwxr-xr-x 2 root         root         4096 7月  25 16:20 parcels
[root@sp-66 CDHInstallFile]#
```

#### 授权用户组用户

```ruby
[root@sp-66 CDHInstallFile]# chown cloudera-scm:cloudera-scm /opt/cloudera/parcels
[root@sp-66 CDHInstallFile]# ll /opt/cloudera/
总用量 8
drwxr-xr-x 2 cloudera-scm cloudera-scm 4096 7月  25 16:18 parcel-repo
drwxr-xr-x 2 cloudera-scm cloudera-scm 4096 7月  25 16:20 parcels
[root@sp-66 CDHInstallFile]#
```

#### 初始脚本配置数据库scm\_prepare\_database.sh (**在主节点上**)

```ruby
[root@sp-66 CDHInstallFile]# /opt/cloudera-manager/cm-5.10.2/share/cmf/schema/scm_prepare_database.sh mysql -h10.32.156.52 -umaosiyu -pMaosiyu1987! --scm-host sp-66 hadoopDBexample maosiyu Maosiyu1987!
JAVA_HOME=/usr/java/jdk1.7.0_80
Verifying that we can write to /opt/cloudera-manager/cm-5.10.2/etc/cloudera-scm-server
Thu Jul 27 10:04:08 CST 2017 WARN: Establishing SSL connection without server's identity verification is not recommended. According to MySQL 5.5.45+, 5.6.26+ and 5.7.6+ requirements SSL connection must be established by default if explicit option isn't set. For compliance with existing applications not using SSL the verifyServerCertificate property is set to 'false'. You need either to explicitly disable SSL by setting useSSL=false, or set useSSL=true and provide truststore for server certificate verification.
Creating SCM configuration file in /opt/cloudera-manager/cm-5.10.2/etc/cloudera-scm-server
Executing:  /usr/java/jdk1.7.0_80/bin/java -cp /usr/share/java/mysql-connector-java.jar:/usr/share/java/oracle-connector-java.jar:/opt/cloudera-manager/cm-5.10.2/share/cmf/schema/../lib/* com.cloudera.enterprise.dbutil.DbCommandExecutor /opt/cloudera-manager/cm-5.10.2/etc/cloudera-scm-server/db.properties com.cloudera.cmf.db.
Thu Jul 27 10:04:09 CST 2017 WARN: Establishing SSL connection without server's identity verification is not recommended. According to MySQL 5.5.45+, 5.6.26+ and 5.7.6+ requirements SSL connection must be established by default if explicit option isn't set. For compliance with existing applications not using SSL the verifyServerCertificate property is set to 'false'. You need either to explicitly disable SSL by setting useSSL=false, or set useSSL=true and provide truststore for server certificate verification.
[                          main] DbCommandExecutor              INFO  Successfully connected to database.
All done, your SCM database is configured correctly!
[root@sp-66 CDHInstallFile]#
```

说明：这个脚本就是用来创建和配置CMS需要的数据库的脚本。各参数是指：

- mysql：数据库用的是mysql，如果安装过程中用的oracle，那么该参数就应该改为oracle。
    
- \-h10.32.156.52：数据库建立在10.32.156.52上面。
    
- \-umaosiyu：maosiyu身份运行mysql。
    
- \-pMaosiyu1987!：mysql的maosiyu密码。
    
- \--scm-host sp-66：CMS的主机，也就是 10.32.156.66 这台主机。 提示: hosts文件的配置 10.32.156.66 sp-66。
    
- 最后三个参数是：数据库名，数据库用户名，数据库密码。
    

### 启动主节点 cloudera-scm-server

```ruby
[root@sp-66 CDHInstallFile]# cp /opt/cloudera-manager/cm-5.10.2/etc/init.d/cloudera-scm-server /etc/init.d/cloudera-scm-server
[root@sp-66 CDHInstallFile]# ll /etc/init.d/
总用量 112
-rwxr-xr-x  1 root root  8594 7月  26 10:48 cloudera-scm-agent
-rwxr-xr-x  1 root root  8436 7月  26 10:43 cloudera-scm-server
-rw-r--r--. 1 root root 13948 9月  16 2015 functions
-rwxr-xr-x  1 root root  9980 4月  11 2015 jexec
-rwxr-xr-x. 1 root root  2989 9月  16 2015 netconsole
-rwxr-xr-x. 1 root root  6630 9月  16 2015 network
-rw-r--r--. 1 root root  1160 11月 22 2016 README
-rwxr-xr-x  1 root root 42062 1月  11 2017 vmware-tools
[root@sp-66 CDHInstallFile]#
[root@sp-66 CDHInstallFile]# chkconfig cloudera-scm-server on
[root@sp-66 CDHInstallFile]#
```

### 主节点添加开机启动

同时为了保证在每次服务器重启的时候都能启动cloudera-scm-server，应该在开机启动脚本/etc/rc.local中加入命令：service cloudera-scm-server restart

```ruby
[root@sp-66 CDHInstallFile]# vim /etc/rc.local
[root@sp-66 CDHInstallFile]# cat /etc/rc.local
#!/bin/bash
# THIS FILE IS ADDED FOR COMPATIBILITY PURPOSES
#
# It is highly advisable to create own systemd services or udev rules
# to run scripts during boot instead of using this file.
#
# In contrast to previous versions due to parallel execution during boot
# this script will NOT be run after all other services.
#
# Please note that you must run 'chmod +x /etc/rc.d/rc.local' to ensure
# that this script will be executed during boot.

touch /var/lock/subsys/local
service cloudera-scm-server restart
[root@sp-66 CDHInstallFile]#
```

### 启动cloudera-scm-agent所有节点

```ruby
[root@sp-66 CDHInstallFile]# mkdir /opt/cloudera-manager/cm-5.10.2/run/cloudera-scm-agent
[root@sp-66 CDHInstallFile]# cp /opt/cloudera-manager/cm-5.10.2/etc/init.d/cloudera-scm-agent /etc/init.d/cloudera-scm-agent
[root@sp-66 CDHInstallFile]# ll /etc/init.d/cloudera-scm-agent
-rwxr-xr-x 1 root root 8594 7月  26 10:48 /etc/init.d/cloudera-scm-agent
[root@sp-66 CDHInstallFile]# chkconfig cloudera-scm-agent on
```

### 子节点添加开机启动

同时为了保证在每次服务器重启的时候都能启动cloudera-scm-agent，应该在开机启动脚本/etc/rc.local中加入命令：service cloudera-scm-agent restart

```ruby
[root@sp-66 CDHInstallFile]# vim /etc/rc.local
[root@sp-66 CDHInstallFile]# cat /etc/rc.local
#!/bin/bash
# THIS FILE IS ADDED FOR COMPATIBILITY PURPOSES
#
# It is highly advisable to create own systemd services or udev rules
# to run scripts during boot instead of using this file.
#
# In contrast to previous versions due to parallel execution during boot
# this script will NOT be run after all other services.
#
# Please note that you must run 'chmod +x /etc/rc.d/rc.local' to ensure
# that this script will be executed during boot.

touch /var/lock/subsys/local
service cloudera-scm-server restart
service cloudera-scm-agent restart
[root@sp-66 CDHInstallFile]#
```

### 启动主节点 与 agent

```ruby
[root@sp-66 hadoop]# /opt/cloudera-manager/cm-5.10.2/etc/init.d/cloudera-scm-server start
Starting cloudera-scm-server:                              [  确定  ]
[root@sp-66 hadoop]# /opt/cloudera-manager/cm-5.10.2/etc/init.d/cloudera-scm-agent start
Starting cloudera-scm-agent:                               [  确定  ]
[root@sp-66 hadoop]#
```

#### 稍等片刻在浏览器中 输入CMS的主机地址 http://10.32.156.66:7180 启动成功后会有登录界面出来 输入账号: admin 密码: admin 到此 Cloudera-Manager已经安装成功了!

#### 此时已经完成一半的工作量了，出现这个界面说明CM已经安装成功了，下面就在这个web界面中部署CDH吧！

### 注意: 如果连接不上有可能是端口没有开放

```ruby
[root@sp-66 CDHInstallFile]# firewall-cmd --zone=public --add-port=7180/tcp --permanent
[root@sp-66 CDHInstallFile]# firewall-cmd --reload
```
