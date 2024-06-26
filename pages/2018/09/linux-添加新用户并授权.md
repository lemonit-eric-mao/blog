---
title: "Linux 添加新用户并授权"
date: "2018-09-26"
categories: 
  - "linux服务器"
---

# Ubuntu 22.04添加用户

```bash
sudo adduser <username>

## 删除用户
sudo userdel -r <username>

## 如果需要将新用户添加到 sudo 组（以便执行管理员任务），可以运行以下命令：
sudo usermod -aG sudo <username>

## 从其他组中删除用户
sudo deluser <username> <groupname>
```

* * *

* * *

* * *

# CentOS7.9 添加用户

### 创建一般用户

```shell
[root@eric-mao (22:25:22) ~]# useradd maosiyu
```

### 查看用户密码状态

```shell
[root@eric-mao (22:25:26) ~]# passwd -S maosiyu
maosiyu LK 2023-01-07 0 99999 7 -1 (密码已被锁定。)
```

### 为用户创建密码

```shell
[root@eric-mao (22:25:34) ~]# passwd maosiyu
更改用户 maosiyu 的密码 。
新的 密码：
无效的密码： 密码未通过字典检查 - 过于简单化/系统化
重新输入新的 密码：
passwd：所有的身份验证令牌已经成功更新。
```

### 再次查看用户密码状态

```shell
[root@eric-mao (22:25:42) ~]# passwd -S maosiyu
maosiyu PS 2023-01-07 0 99999 7 -1 (密码已设置，使用 SHA512 算法。)
```

### 正确的删除用户，用户相关文件全部删除

```ruby
[root@eric-mao (22:25:42) ~]# userdel -r maosiyu
```

* * *

## 创建用户

### 创建一个系统用户

```shell
[root@eric-mao (22:25:22) ~]# useradd -r maosiyu-root
```

### 创建普通用户

```shell
[root@eric-mao (22:25:22) ~]# useradd maosiyu
```

### 创建不能登陆的用户

```shell
[root@eric-mao (22:25:22) ~]# useradd maosiyu-ftp -s /sbin/nologin
```

* * *

## 用户修改密码

1. 交互式修改密码
    
    - root 用户权限
2. 非交互式修改密码
    
    - passwd `--stdin`
        
        - `Stdin`
        - `Stdout`
        - `Stderr`
    - ```shell
        ## 添加用户
        [root@centos03 (09:07:47) ~]# useradd siyu.mao
        ## 命令行非交互式 修改密码
        [root@centos03 (09:29:46) ~]# echo 123456 | passwd --stdin siyu.mao
        Changing password for user siyu.mao.
        passwd: all authentication tokens updated successfully.
        
        ```
        
    - ```shell
        [root@centos03 (09:36:17) ~]# cat > passfile << ERIC
        654321
        ERIC
        ## 从文件中读取密码
        [root@centos03 (09:36:17) ~]# passwd --stdin siyu.mao<passfile
        Changing password for user siyu.mao.
        passwd: all authentication tokens updated successfully.
        ```
