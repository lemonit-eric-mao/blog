---
title: "CentOS 7 只安装客户端"
date: "2019-08-01"
categories: 
  - "mysql"
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

* * *

* * *

* * *

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

* * *

* * *

* * *

### 原Dockerfile

```shell
cat > Dockerfile << ERIC

# centos:centos7.9.2009  204MB
FROM centos:centos7.9.2009
RUN mkdir /app
WORKDIR /app

## 加入Redis客户端
COPY redis-cli /usr/local/bin/

## 加入客户端工具
COPY mariadb-5.5.68-1.el7.x86_64.rpm \
     mariadb-libs-5.5.68-1.el7.x86_64.rpm \
     net-tools-2.0-0.25.20131004git.el7.x86_64.rpm \
     telnet-0.17-66.el7.x86_64.rpm \
     wget-1.14-18.el7_6.1.x86_64.rpm \
     iptraf-ng-1.1.4-7.el7.x86_64.rpm \
     ./

RUN rpm -ivh --force --nodeps *.rpm

ERIC


## 构建镜像
docker build -t cnagent/client-tools:base .

## 测试
docker run -it --rm cnagent/client-tools:base

```

* * *

* * *

* * *

### 制作客户端镜像

```shell
cat > Dockerfile << ERIC

FROM cnagent/client-tools:base
WORKDIR /app

## 加入客户端工具
COPY xxxxxx.rpm
     ./

RUN rpm -ivh --force --nodeps *.rpm

ERIC


## 构建镜像
docker build -t cnagent/client-tools:1.0.0 .

## 测试
docker run -it --rm cnagent/client-tools:1.0.0

```

* * *

* * *

* * *
