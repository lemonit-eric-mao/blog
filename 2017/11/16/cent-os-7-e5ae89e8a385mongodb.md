---
title: 'Cent OS 7 安装mongoDB'
date: '2017-11-16T16:25:40+00:00'
status: publish
permalink: /2017/11/16/cent-os-7-%e5%ae%89%e8%a3%85mongodb
author: 毛巳煜
excerpt: ''
type: post
id: 532
category:
    - Mongodb
tag: []
post_format: []
---
### 查看系统版本

```
<pre class="line-numbers prism-highlight" data-start="1">```ruby
[root@zhujiwu]# more /etc/redhat-release
CentOS Linux release 7.0.1406 (Core)

```
```

### 按照官网的安装步骤 新建文件

```
<pre class="line-numbers prism-highlight" data-start="1">```ruby
[root@zhujiwu]# vim /etc/yum.repos.d/mongodb-org-3.4.repo

```
```

### 粘贴如下内容

```
<pre class="line-numbers prism-highlight" data-start="1">```ruby
[mongodb-org-3.4]
name=MongoDB Repository
baseurl=https://repo.mongodb.org/yum/redhat/$releasever/mongodb-org/3.4/x86_64/
gpgcheck=1
enabled=1
gpgkey=https://www.mongodb.org/static/pgp/server-3.4.asc

```
```

### 配置完成以后 开始安装

```
<pre class="line-numbers prism-highlight" data-start="1">```ruby
[root@zhujiwu]# yum install -y mongodb-org

```
```

### 如果出现

> ##### 源 "MongoDB Repository" 的 GPG 密钥已安装，但是不适用于此软件包。请检查源的公钥 URL 是否配置正确。
> 
>  ##### 这种类似的问题， 有可能是已经添加了其它不同的版本的源，删除其它没用的源重新在安装一次就好了。
> 
>  ##### \*\*例如：如下场景\*\*

```
<pre class="line-numbers prism-highlight" data-start="1">```ruby
[root@zhujiwu]# cd  /etc/yum.repos.d/
[root@zhujiwu yum.repos.d]# ls
......
mongodb-org-3.2.repo
mongodb-org-3.4.repo
......
[root@zhujiwu yum.repos.d]# rm -rf mongodb-org-3.2.repo

```
```

### 安装完成后

> 查看mongo安装位置 whereis mongod  
>  查看修改配置文件 ： vim /etc/mongod.conf  
>  3.启动MongoDB  
>  启动mongodb ： sudo systemctl start mongod.service  
>  停止mongodb ： sudo systemctl stop mongod.service

查看mongodb的状态： sudo systemctl status mongod.service