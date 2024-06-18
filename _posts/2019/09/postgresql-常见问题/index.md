---
title: "PostgreSQL 常见问题"
date: "2019-09-11"
categories: 
  - "postgresql"
---

##### 1.删除 postgres 用户失败

```ruby
[root@test3 ~]# userdel -r postgres
userdel: user postgres is currently used by process PID
# 原因是postgres还有很多运行的进程没有关闭，所以不能够直接删除用户
```

###### 1.1 解决思路

```ruby
# 查看所有占用的进程
[root@test3 ~]# ps -u postgres| awk '{print $1}'

# 统统kill掉
[root@test3 ~]# ps -u postgres| awk '{print $1}' | xargs kill -9
```
