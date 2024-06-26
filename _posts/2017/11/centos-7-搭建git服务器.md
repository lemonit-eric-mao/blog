---
title: "CentOS 7 搭建git服务器"
date: "2017-11-16"
categories: 
  - "centos"
---

## CentOS7搭建git服务器

#### 保存原始的 yum源

```ruby
[root@localhost ~]# mv /etc/yum.repos.d/CentOS-Base.repo /etc/yum.repos.d/CentOS-Base.repo.backup
```

#### 应用阿里云的 yum源

```ruby
[root@localhost ~]# wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo
```

#### 私服地址 10.32.156.58

```ruby
# 安装git
[root@localhost ~]# yum –y install git
# 创建一个仓库位置
[root@localhost ~]# cd /home/
[root@localhost home]# mkdir library
[root@localhost home]# cd library/
# 初始化一个裸仓库 注: --bare 一定要加否则后果自己想办法
[root@localhost library]# git init --bare test.git
[root@localhost library]# cd ..
# 开放这个目录的所有权限,否则其它用户没有权限 push
[root@localhost home]# chmod -R 777 library/

# 创建一个git账户
[root@localhost home]# useradd gitUser
[root@localhost home]# passwd gitUser
更改用户 gitUser 的密码 。
新的 密码：
重新输入新的 密码：
passwd：所有的身份验证令牌已经成功更新。

# 创建git用户组
[root@localhost home]# groupadd gitgroup
# 将用户加入到组中
[root@localhost home]# usermod -G gitgroup gitUser
# 查看组中的用户
[root@localhost home]# grep gitgroup /etc/group
gitgroup:x:1002:gitUser
# 将gitlib文件夹 授权给 gitgroup 组
[root@localhost home]# chgrp gitgroup -R library

[root@localhost home]# cd library/test.git
[root@localhost test.git]# pwd
/home/library/test.git
# 拼接仓库地址
# git clone gitUser@10.32.156.58:/home/library/test.git 发给客户端
```

#### 客户端

```ruby
mao-siyu@mao-siyu-PC:~/视频$ git clone gitUser@10.32.156.58:/home/library/test.git
正克隆到 'test'...
gitUser@10.32.156.58's password:
warning: 您似乎克隆了一个空仓库。
检查连接... 完成。
mao-siyu@mao-siyu-PC:~/视频$ cd test/
mao-siyu@mao-siyu-PC:~/视频/test$ vim test.txt
mao-siyu@mao-siyu-PC:~/视频/test$ git add test.txt
mao-siyu@mao-siyu-PC:~/视频/test$ git commit -m '添加一个新文件'
[master （根提交） be63438] 添加一个新文件
 1 file changed, 0 insertions(+), 0 deletions(-)
 create mode 100644 test.txt
mao-siyu@mao-siyu-PC:~/视频/test$ git push
gitUser@10.32.156.58's password:
对象计数中: 3, 完成.
写入对象中: 100% (3/3), 225 bytes | 0 bytes/s, 完成.
Total 3 (delta 0), reused 0 (delta 0)
To gitUser@10.32.156.58:/home/library/test.git
 * [new branch]      master -> master
mao-siyu@mao-siyu-PC:~/视频/test$
```

#### 常见问题

```ruby
# Permission denied, please try again.
# 权限拒绝, 请在次尝试  原因: 1 服务器文件夹权限没有开放；2 密码输入错误

# remote: error:
# 一大串的错误信息 原因 :创建的仓库 不是使用 --bare 创建的
```
