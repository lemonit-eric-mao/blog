---
title: 'Linux 系统配置阿里云源'
date: '2019-11-06T02:38:42+00:00'
status: publish
permalink: /2019/11/06/linux-%e7%b3%bb%e7%bb%9f%e9%85%8d%e7%bd%ae%e9%98%bf%e9%87%8c%e4%ba%91%e6%ba%90
author: 毛巳煜
excerpt: ''
type: post
id: 5104
category:
    - Linux服务器
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
wb_sst_seo:
    - 'a:3:{i:0;s:0:"";i:1;s:0:"";i:2;s:0:"";}'
---
###### [阿里云各系统镜像](https://developer.aliyun.com/mirror "阿里云各系统镜像")

Ubuntu 22.04.1 apt源
===================

### 备份默认源

```bash
sudo cp /etc/apt/sources.list /etc/apt/sources.list.bak

```

### 替换阿里源

```bash
sudo tee /etc/apt/sources.list 
```

### 更新软件包

```bash
sudo apt update


```

- - - - - -

- - - - - -

- - - - - -

CentOS 7 yum源
=============

##### 将本机yum源修改为阿里云源

```ruby
# 备份 CentOS-Base.repo
[root@test1 ~]# mv /etc/yum.repos.d/CentOS-Base.repo /etc/yum.repos.d/CentOS-Base.repo.backup

# 下载阿里云源
[root@test1 ~]# wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo
[root@test1 ~]# wget -O /etc/yum.repos.d/epel.repo http://mirrors.aliyun.com/repo/epel-7.repo

# 删除无用内容
[root@test1 ~]# sed -i -e '/mirrors.cloud.aliyuncs.com/d' -e '/mirrors.aliyuncs.com/d' /etc/yum.repos.d/CentOS-Base.repo
[root@test1 ~]# sed -i '/aliyuncs/d' /etc/yum.repos.d/epel.repo

# 阿里云建议普通用户使用/7/, 而不使用/7.6.1810/这种小版本, 所以替换阿里云源的版本
[root@test1 ~]# sed -i 's/$releasever/7/g' /etc/yum.repos.d/CentOS-Base.repo

# 更新源
[root@test1 ~]# yum clean all && yum makecache all

# 更新系统(可选)
[root@test1 ~]# yum update -y


```

- - - - - -

###### 直接用

```ruby
mv /etc/yum.repos.d/CentOS-Base.repo /etc/yum.repos.d/CentOS-Base.repo.backup
wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo
wget -O /etc/yum.repos.d/epel.repo http://mirrors.aliyun.com/repo/epel-7.repo
sed -i -e '/mirrors.cloud.aliyuncs.com/d' -e '/mirrors.aliyuncs.com/d' /etc/yum.repos.d/CentOS-Base.repo
sed -i '/aliyuncs/d' /etc/yum.repos.d/epel.repo
sed -i 's/$releasever/7/g' /etc/yum.repos.d/CentOS-Base.repo
yum clean all && yum makecache all && yum update -y

```

- - - - - -

- - - - - -

- - - - - -

- - - - - -

- - - - - -

- - - - - -

###### **`yum源 修复`**

```ruby
# 删除所有源
[root@test1 ~]# rm -rf /etc/yum.repos.d/*
[root@test1 ~]#
# 查看当前系统
[root@test1 yum.repos.d]# cat /etc/redhat-release
CentOS Linux release 7.7.1908 (Core)
[root@test1 yum.repos.d]#

```

根据自己的操作系统 `http://mirror.centos.org/centos-7/` 从这个路径一点一点往下找，直到找到自己的yum源配置位置，例如：  
`http://mirror.centos.org/centos-7/7.9.2009/os/x86_64/Packages/centos-release-7-9.2009.0.el7.centos.x86_64.rpm`

```ruby
[root@test1 yum.repos.d]# rpm -Uvh --force http://mirror.centos.org/centos-7/7.7.1908/os/x86_64/Packages/centos-release-7-7.1908.0.el7.centos.x86_64.rpm
[root@test1 yum.repos.d]#

##### 注意：重新换源，必需要下面这两步，否则什么都安装不了
# 重新安装 epel-release
[root@test1 yum.repos.d]# yum remove -y epel-release && yum install -y epel-release
# 重新缓存
[root@test1 yum.repos.d]# yum clean all && yum makecache all && yum update -y


```

- - - - - -

- - - - - -

- - - - - -