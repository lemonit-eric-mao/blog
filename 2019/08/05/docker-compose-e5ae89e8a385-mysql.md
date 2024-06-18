---
title: 'docker-compose 安装 mysql 8.0'
date: '2019-08-05T10:25:03+00:00'
status: publish
permalink: /2019/08/05/docker-compose-%e5%ae%89%e8%a3%85-mysql
author: 毛巳煜
excerpt: ''
type: post
id: 4985
category:
    - MySQL
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
wb_sst_seo:
    - 'a:3:{i:0;s:0:"";i:1;s:0:"";i:2;s:0:"";}'
---
[目前最新版](https://hub.docker.com/_/mysql?tab=tags "目前最新版")

[安装 docker-compose](http://www.dev-share.top/2019/06/12/%e5%ae%89%e8%a3%85-docker-compose/ "安装 docker-compose")

##### docker-compose安装

```ruby
[root@dev1 deploy]# mkdir -p /home/deploy/mysqldb/config && cd /home/deploy/mysqldb/
[root@dev1 deploy]#

[root@dev1 mysqldb]# cat > docker-compose.yaml 3306/tcp, 33060/tcp
[root@dev1 mysqldb]#

```

##### 访问：默认不能使用 localhost 要使用数据库服务器的IP进行访问

```ruby
[root@dev1 mysqldb]# mysql -h 172.160.180.6 -u root -P 3305 -p

```