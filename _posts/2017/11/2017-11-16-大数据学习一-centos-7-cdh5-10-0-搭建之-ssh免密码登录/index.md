---
title: "大数据学习(一)  Centos 7 + cdh5.10.0 搭建之-ssh免密码登录"
date: "2017-11-16"
categories: 
  - "大数据"
---

[转载/摘选自](http://www.cnblogs.com/baierfa/p/6688737.html)

### 安装 jdk-7u80-linux-x64.rpm

#### 从官网下载 http://download.oracle.com/otn/java/jdk/7u80-b15/jdk-7u80-linux-x64.rpm

```ruby
[root@sp-66 mao_siyu]# rpm -ivh jdk-7u80-linux-x64.rpm
```

### 登录到10.32.156.66服务器 `root`用户

```ruby
[root@localhost ~]# adduser hadoop
[root@localhost ~]# passwd hadoop
[root@localhost ~]# vim /etc/hosts
10.32.156.66 sp-66
10.32.156.67 sp-67
wq!
[root@localhost ~]# hostname sp-66
[root@sp-66 .ssh]# exit
```

### 切换到10.32.156.66服务器 `hadoop`用户

#### 生成 公钥与私钥

```ruby
[hadoop@localhost ~]$ ssh-keygen -t rsa -P ""
[hadoop@localhost .ssh]$ cd /home/hadoop/.ssh/
[hadoop@localhost .ssh]$ ls
id_rsa  id_rsa.pub
[hadoop@localhost .ssh]$ cat id_rsa.pub >> authorized_keys
[hadoop@localhost .ssh]$ ls
authorized_keys  id_rsa  id_rsa.pub
[hadoop@localhost .ssh]$
```

### 登录到10.32.156.67服务器 `root`用户,需以同样的方式,执行命令生成密钥

```ruby
[root@localhost ~]# adduser hadoop
[root@localhost ~]# passwd hadoop
[root@localhost ~]# vim /etc/hosts
10.32.156.66 sp-66
10.32.156.67 sp-67
wq!

[root@localhost ~]# hostname sp-67
[root@sp-67 .ssh]# exit
```

### 切换到10.32.156.67服务器 `hadoop`用户

#### 生成 公钥与私钥, 并将公钥发送到10.32.156.66服务器

```ruby
[hadoop@localhost ~]$ ssh-keygen -t rsa -P ""
[hadoop@localhost .ssh]$ cd /home/hadoop/.ssh/
[hadoop@localhost .ssh]$ ls
id_rsa  id_rsa.pub
[hadoop@localhost .ssh]$ scp id_rsa.pub hadoop@10.32.156.66:/home/hadoop/.ssh/id_rsa.pub.s1
```

### 切换到10.32.156.66服务器 `hadoop`用户

#### 执行如下命令, 将公钥全都写到 `authorized_keys`文件中, 并将`authorized_keys`文件交给`10.32.156.67`服务器一份

```ruby
[hadoop@localhost .ssh]$ cd /home/hadoop/.ssh/
[hadoop@localhost .ssh]$ ls
authorized_keys  id_rsa  id_rsa.pub  id_rsa.pub.s1
[hadoop@localhost .ssh]$ cat id_rsa.pub.s1 >> authorized_keys
[hadoop@localhost .ssh]$ scp authorized_keys hadoop@10.32.156.67:/home/hadoop/.ssh/
```

### 切换到10.32.156.67服务器 `hadoop`用户

#### 文件受权

```ruby
[hadoop@sp-67 ~]$ chmod 600 /home/hadoop/.ssh/authorized_keys
[hadoop@sp-67 ~]$ chmod 700 /home/hadoop/.ssh/
```

### 切换到10.32.156.67服务器 `root`用户

```ruby
[root@sp-67 hadoop]# systemctl restart  sshd.service
[root@sp-67 hadoop]#
```

### 切换到10.32.156.66服务器 `hadoop`用户

#### 测试免密登录是否配置成功：ssh 主机名 例：ssh sp-67

```ruby
[hadoop@sp-66 .ssh]$ ssh sp-67
Last login: Mon Jul 24 15:19:09 2017 from 10.32.156.66
[hadoop@sp-67 ~]$
```

### 时间同步

使用ntpdate搭建时间同步

```ruby
[root@sp-66 hadoop]# yum -y install ntpdate
```

ntp.sjtu.edu.cn 202.120.2.101 (上海交通大学网络中心NTP服务器地址）

```ruby
[root@sp-66 hadoop]# ntpdate 202.120.2.101
24 Jul 16:32:29 ntpdate[3320]: adjust time server 202.120.2.101 offset 0.057572 sec
[root@sp-66 hadoop]# date
2017年 07月 24日 星期一 16:32:56 CST
[root@sp-66 hadoop]#
```
