---
title: '使用 docker-compose 安装 filebeat+redis'
date: '2019-06-27T11:53:33+00:00'
status: publish
permalink: /2019/06/27/%e4%bd%bf%e7%94%a8-docker-compose-%e5%ae%89%e8%a3%85-filebeatredis
author: 毛巳煜
excerpt: ''
type: post
id: 4940
category:
    - ELK
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
post_views_count:
    - '0'
---
[安装 docker-compose](https://www.lemonit.cn/2019/06/12/%E5%AE%89%E8%A3%85-docker-compose/ "安装 docker-compose")

##### 准备 创建文件夹

```ruby
[root@k8s-master ~]# mkdir -p /home/deploy/filebeat/config/data
[root@k8s-master ~]# mkdir -p /home/deploy/filebeat/config/redis

```

##### 配置 docker-compose.yml

```ruby
[root@k8s-master filebeat]# pwd
/home/deploy/filebeat
[root@k8s-master filebeat]# cat > docker-compose.yml 
```

##### 添加 redis 配置 redis.conf

```ruby
[root@k8s-master redis]# pwd
/home/deploy/filebeat/config/redis
[root@k8s-master redis]# cat > redis.conf 
```

##### 添加 filebeat.yml

```ruby
[root@k8s-master config]# pwd
/home/deploy/filebeat/config
[root@k8s-master config]# cat > filebeat.yml 
```

##### 启动

```ruby
[root@k8s-master filebeat]# pwd
/home/deploy/filebeat
[root@k8s-master filebeat]# ll
total 8
drwxr-xr-x 4 root root 4096 Jun 27 17:08 config
-rwxr-xr-x 1 root root  987 Jun 27 16:05 docker-compose.yml
[root@k8s-master filebeat]#
[root@k8s-master filebeat]# docker-compose up -d

```