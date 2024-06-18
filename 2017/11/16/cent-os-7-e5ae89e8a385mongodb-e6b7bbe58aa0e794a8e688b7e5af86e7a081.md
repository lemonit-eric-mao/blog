---
title: 'Cent OS 7 安装mongoDB 添加用户密码'
date: '2017-11-16T16:27:19+00:00'
status: publish
permalink: /2017/11/16/cent-os-7-%e5%ae%89%e8%a3%85mongodb-%e6%b7%bb%e5%8a%a0%e7%94%a8%e6%88%b7%e5%af%86%e7%a0%81
author: 毛巳煜
excerpt: ''
type: post
id: 534
category:
    - Mongodb
tag: []
post_format: []
---
写个博客数据库都能被删, 无奈添加用户名密码, 某人素质太差
------------------------------

### mongodb 版本 3.4.5

```
<pre class="line-numbers prism-highlight" data-start="1">```ruby
[root@zhujiwu NodeBB-1.5.x]# netstat -antp
Active Internet connections (servers and established)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name
tcp        0      0 127.0.0.1:25            0.0.0.0:*               LISTEN      2523/master
tcp        0      0 127.0.0.1:49473         0.0.0.0:*               LISTEN      3177/java
tcp        0      0 111.67.192.10:27017     0.0.0.0:*               LISTEN      28870/mongod
[root@zhujiwu NodeBB-1.5.x]#

```
```

### 用户权限设置

1. MongoDB是没有默认管理员账号，所以要先添加管理员账号，再开启权限认证。
2. 切换到admin数据库，添加的账号才是管理员账号。
3. 用户只能在用户所在数据库登录，包括管理员账号。
4. 管理员可以管理所有数据库，但是不能直接管理其他数据库，要先在admin数据库认证后才可以。

### 连接进入mongodb

```
<pre class="line-numbers prism-highlight" data-start="1">```ruby
root@zhujiwu NodeBB-1.5.x]# mongo 111.67.192.10:27017
MongoDB shell version v3.4.5
connecting to: 111.67.192.10:27017
MongoDB server version: 3.4.5
Server has startup warnings:
2017-08-09T11:44:38.515+0800 I CONTROL  [initandlisten]
2017-08-09T11:44:38.515+0800 I CONTROL  [initandlisten] ** WARNING: Access control is not enabled for the database.
2017-08-09T11:44:38.515+0800 I CONTROL  [initandlisten] **          Read and write access to data and configuration is unrestricted.
2017-08-09T11:44:38.515+0800 I CONTROL  [initandlisten]
2017-08-09T11:44:38.515+0800 I CONTROL  [initandlisten]
2017-08-09T11:44:38.515+0800 I CONTROL  [initandlisten] ** WARNING: /sys/kernel/mm/transparent_hugepage/enabled is 'always'.
2017-08-09T11:44:38.515+0800 I CONTROL  [initandlisten] **        We suggest setting it to 'never'
2017-08-09T11:44:38.515+0800 I CONTROL  [initandlisten]
2017-08-09T11:44:38.515+0800 I CONTROL  [initandlisten] ** WARNING: /sys/kernel/mm/transparent_hugepage/defrag is 'always'.
2017-08-09T11:44:38.515+0800 I CONTROL  [initandlisten] **        We suggest setting it to 'never'
2017-08-09T11:44:38.515+0800 I CONTROL  [initandlisten]
>
> show dbs
Warning  0.000GB
admin    0.000GB
local    0.000GB
nodebb   0.001GB
>

```
```

### 创建管理员用户

```
<pre class="line-numbers prism-highlight" data-start="1">```ruby
> use admin
switched to db admin
>
> db.createUser({
... user: "root",
... pwd: "mongoPasswd",
... roles: [{role: "userAdminAnyDatabase", db: "admin"}]
... })
Successfully added user: {
    "user" : "root",
    "roles" : [
        {
            "role" : "userAdminAnyDatabase",
            "db" : "admin"
        }
    ]
}
>
> show users
{
    "_id" : "test.root",
    "user" : "root",
    "db" : "test",
    "roles" : [
        {
            "role" : "userAdminAnyDatabase",
            "db" : "admin"
        }
    ]
}

```
```

### 开启权限验证

```
<pre class="line-numbers prism-highlight" data-start="1">```ruby
[root@zhujiwu ~]# echo "security:
>   authorization: enabled
> " >> /etc/mongod.conf
[root@zhujiwu ~]# cat /etc/mongod.conf
# mongod.conf

# for documentation of all options, see:
#   http://docs.mongodb.org/manual/reference/configuration-options/

# where to write logging data.
systemLog:
  destination: file
  logAppend: true
  path: /var/log/mongodb/mongod.log

# Where and how to store data.
storage:
  dbPath: /var/lib/mongo
  journal:
    enabled: true
#  engine:
#  mmapv1:
#  wiredTiger:

# how the process runs
processManagement:
  fork: true  # fork and run in background
  pidFilePath: /var/run/mongodb/mongod.pid  # location of pidfile

# network interfaces
net:
  port: 27017
  bindIp: 111.67.192.10  # Listen to local interface only, comment to listen on all interfaces.
  #auth: true

#security:

##operationProfiling:

#replication:

#sharding:

## Enterprise-Only Options

#auditLog:

#snmp:

# echo命令就是为了添加一条这个信息
security:
  authorization: enabled

[root@zhujiwu ~]# systemctl restart mongod.service

```
```

### 验证权限是否生效

```
<pre class="line-numbers prism-highlight" data-start="1">```ruby
# 如果
security:
  authorization: enabled
# 为启用状态, 连接成功后的信息都是有区别的.

```
```

```
<pre class="line-numbers prism-highlight" data-start="1">```ruby
[root@zhujiwu ~]# mongo 111.67.192.10:27017
MongoDB shell version v3.4.5
connecting to: 111.67.192.10:27017
MongoDB server version: 3.4.5
>
> show dbs
2017-08-09T12:31:21.355+0800 E QUERY    [thread1] Error: listDatabases failed:{
    "ok" : 0,
    "errmsg" : "not authorized on admin to execute command { listDatabases: 1.0 }",
    "code" : 13,
    "codeName" : "Unauthorized"
} :
_getErrorWithCode@src/mongo/shell/utils.js:25:13
Mongo.prototype.getDBs@src/mongo/shell/mongo.js:62:1
shellHelper.show@src/mongo/shell/utils.js:769:19
shellHelper@src/mongo/shell/utils.js:659:15
@(shellhelp2):1:1
>
> db.auth("root", "mongoPasswd");  # 连接后登录
1
>
> show dbs
Warning  0.000GB
admin    0.000GB
local    0.000GB
nodebb   0.001GB
>

```
```

### 或者这样 在连接时输入用户名密码

```
<pre class="line-numbers prism-highlight" data-start="1">```ruby
[root@zhujiwu ~]# mongo 111.67.192.10:27017 -u root -p # 连接时直接登录
MongoDB shell version v3.4.5
Enter password:
connecting to: 111.67.192.10:27017
MongoDB server version: 3.4.5
>
> show dbs
Warning  0.000GB
admin    0.000GB
local    0.000GB
nodebb   0.001GB
>

```
```

### 开启用户权限后 查询用户信息的命令 需使用 db.system.users.find() 这个时候使用show users 确什么也查不到

```
<pre class="line-numbers prism-highlight" data-start="1">```ruby
> use admin
switched to db admin
>
> db.system.users.find()
{ "_id" : "test.root", "user" : "root", "db" : "test", "credentials" : { "SCRAM-SHA-1" : { "iterationCount" : 10000, "salt" : "mchKjlVudUVEx4UyyEIX2A==", "storedKey" : "jzEowxF+Rpnih6k1BfdXlgDW2fE=", "serverKey" : "JJTzbOwF2UaT0lmbEuq0PaxIXeA=" } }, "roles" : [ { "role" : "userAdminAnyDatabase", "db" : "admin" } ] }
>
> show users
>

```
```

```
<pre class="line-numbers prism-highlight" data-start="1">```null
角色说明：
Read：允许用户读取指定数据库
readWrite：允许用户读写指定数据库
dbAdmin：允许用户在指定数据库中执行管理函数，如索引创建、删除，查看统计或访问system.profile
userAdmin：允许用户向system.users集合写入，可以找指定数据库里创建、删除和管理用户
clusterAdmin：只在admin数据库中可用，赋予用户所有分片和复制集相关函数的管理权限。
readAnyDatabase：只在admin数据库中可用，赋予用户所有数据库的读权限
readWriteAnyDatabase：只在admin数据库中可用，赋予用户所有数据库的读写权限
userAdminAnyDatabase：只在admin数据库中可用，赋予用户所有数据库的userAdmin权限
dbAdminAnyDatabase：只在admin数据库中可用，赋予用户所有数据库的dbAdmin权限。
root：只在admin数据库中可用。超级账号，超级权限

```
```