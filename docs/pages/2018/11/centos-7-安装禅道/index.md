---
title: "CentOS 7 安装禅道"
date: "2018-11-26"
categories: 
  - "开发工具"
---

[禅道官网下载地址](https://www.zentao.net/download/80099.html "禅道官网下载地址") 下载地址在最下面

[官方推荐的安装方法](https://www.zentao.net/book/zentaopmshelp/40.html "官方推荐的安装方法")

##### 根据官网要求选择安装包

Linux 64位一键安装包（适用于Linux 64位） http://dl.cnezsoft.com/zentao/12.5.3/ZenTaoPMS.12.5.3.zbox\_64.tar.gz

```ruby
[root@zentao www]# wget http://dl.cnezsoft.com/zentao/12.5.3/ZenTaoPMS.12.5.3.zbox_64.tar.gz
```

###### 前置条件

| IP | host |
| --- | --- |
| 172.160.180.6 | dev1 |

* * *

* * *

* * *

###### 1、将安装包直接解压到/opt目录下

**特别说明：** 不要 解压到别的目录再拷贝到/opt/，因为这样会导致文件的所有者和读写权限改变， 也不要解压后把整个目录777权限 。 可以使用命令：

```ruby
[root@zentao www]# sudo tar -zxvf ZenTaoPMS.12.5.3.zbox_64.tar.gz -C /opt
```

* * *

###### 2、启动/停止/重启 禅道web 与 MySQL

```ruby
[root@dev1 auth]# /opt/zbox/zbox start
[root@dev1 auth]# /opt/zbox/zbox stop
[root@dev1 auth]# /opt/zbox/zbox restart
```

* * *

###### 3、访问和登录禅道

```
启动 Apache和Mysql服务后，
浏览器直接访问 http://172.160.180.6 即可访问和登录禅道。
注：如果网页无法访问，请先关闭禅道所在电脑的防火墙和selinux再刷新网页访问试一下。
禅道默认管理员帐号是 admin，密码 123456。
禅道数据库默认管理员帐号是 root，密码 空。
```

* * *

###### 4、修改禅道web端口 与 禅道数据库端口

可以使用`/opt/zbox/zbox -h`命令来获取关于zbox命令的帮助。 其中 `-ap`参数 可以修改Apache的端口，`-mp`参数 可以修改Mysql的端口。 例如（apache端口改为8080，mysql端口改为3308）：

```ruby
/opt/zbox/zbox stop
/opt/zbox/zbox -ap 8080 -mp 3308
/opt/zbox/zbox start
```

* * *

###### 5、修改禅道数据库密码

`/opt/zbox/auth/adduser.sh`

```ruby
[root@dev1 auth]# /opt/zbox/auth/adduser.sh
This tool is used to add user to access adminer
Account: root
Password: # 输入密码 123456
Adding password for user root
[root@dev1 auth]#
[root@dev1 auth]#
[root@dev1 auth]#
[root@dev1 auth]# mysql -h 127.0.0.1 -u root -P 3308 -p123456
Enter password:
Welcome to the MariaDB monitor.  Commands end with ; or \g.
Your MariaDB connection id is 55
Server version: 10.1.22-MariaDB Source distribution

Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

MariaDB [(none)]> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
| zentao             |
| zentaobiz          |
| zentaopro          |
+--------------------+
6 rows in set (0.016 sec)

MariaDB [(none)]>
```

* * *

###### 6、添加开机自启动

```ruby
[root@zentao etc]# echo '/opt/zbox/zbox restart' >> /etc/rc.local
[root@zentao etc]#
[root@zentao etc]# chmod +x /etc/rc.d/rc.local
[root@zentao etc]#
[root@zentao etc]# reboot
```

* * *

* * *

* * *

##### 重置管理员密码

登录页面，点击忘记密码，按照提示创建文件后，在网页点击刷新应该出现重置密码的页面

```ruby
[root@dev1 ~]# mkdir -p /opt/zbox/app/zentao/tmp/
[root@dev1 ~]#
[root@dev1 ~]# echo '' > /opt/zbox/app/zentao/tmp/reset_5ebb85558b1c9.txt
[root@dev1 ~]#
```

* * *

* * *

* * *
