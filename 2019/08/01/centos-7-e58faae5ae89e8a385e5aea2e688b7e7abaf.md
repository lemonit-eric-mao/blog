---
title: 'CentOS 7 只安装客户端'
date: '2019-08-01T09:21:56+00:00'
status: publish
permalink: /2019/08/01/centos-7-%e5%8f%aa%e5%ae%89%e8%a3%85%e5%ae%a2%e6%88%b7%e7%ab%af
author: 毛巳煜
excerpt: ''
type: post
id: 4977
category:
    - MySQL
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
wb_sst_seo:
    - 'a:3:{i:0;s:0:"";i:1;s:0:"";i:2;s:0:"";}'
---
##### 仅安装MariaDB客户端

```ruby
[root@k8s-master ~]# yum install -y mariadb

```

##### 下载离线包

```ruby
mkdir mysql-client && cd mysql-client/

yumdownloader --resolve --downloadonly --downloaddir=$PWD mariadb

rpm -ivh --force --nodeps *.rpm


```

- - - - - -

- - - - - -

- - - - - -

##### 仅安装MySQL客户端

```ruby
# 添加rpm源
[root@k8s-master ~]# rpm -ivh https://repo.mysql.com/mysql57-community-release-el7-11.noarch.rpm
[root@k8s-master ~]#
# 通过yum搜索
[root@k8s-master ~]# yum search mysql-community
[root@k8s-master ~]#
# 安装x64位的 mysql客户端
[root@k8s-master ~]# yum install -y mysql-community-client.x86_64

```

- - - - - -

- - - - - -

- - - - - -

### 原Dockerfile

```shell
cat > Dockerfile 
```

- - - - - -

- - - - - -

- - - - - -

### 制作客户端镜像

```shell
cat > Dockerfile 
```

- - - - - -

- - - - - -

- - - - - -