---
title: 'docker-compose 安装 mariadb'
date: '2019-08-05T08:01:53+00:00'
status: publish
permalink: /2019/08/05/docker-%e5%ae%89%e8%a3%85-mariadb
author: 毛巳煜
excerpt: ''
type: post
id: 4984
category:
    - MySQL
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
wb_sst_seo:
    - 'a:3:{i:0;s:0:"";i:1;s:0:"";i:2;s:0:"";}'
---
[目前最新版](https://hub.docker.com/_/mariadb?tab=tags "目前最新版")

[安装 docker-compose](http://www.dev-share.top/2019/06/12/%e5%ae%89%e8%a3%85-docker-compose/ "安装 docker-compose")

- - - - - -

##### 创建文件夹

```ruby
mkdir -p mariadb/config/mariadb-config/


```

- - - - - -

##### 创建 docker-compose 文件

```ruby
cat > mariadb/docker-compose.yaml 
```

- - - - - -

##### 启动

```ruby
[root@master mariadb]# docker-compose up -d


[root@master mariadb]# docker-compose ps
 Name               Command             State           Ports
----------------------------------------------------------------------
mariadb   docker-entrypoint.sh mysqld   Up      0.0.0.0:3306->3306/tcp
[root@master mariadb]#

# 查看 Log 等待 出现 start up 表示启动成功， 如果机器配置不好，这个过程有点儿久
[root@master mariadb]# docker-compose logs -f mariadb | grep 'start up'
mariadb    | MySQL init process done. Ready for start up.


```

- - - - - -

##### 访问：默认不能使用 localhost 要使用数据库服务器的IP进行访问

```ruby
[root@master mariadb]# mysql -h 192.168.2.10 -u root -P 3306 -p

```

- - - - - -

- - - - - -

##### 只开启binlog (可选功能)

> 修改配置文件, 加如下内容

```ruby
cat > config/mariadb-config/50-server.cnf 
```

**查看是否开启binlog**

> `docker-compose exec mariadb mysql -u 数据库用户名 -p数据库密码 -e "SQL语句;"`

```ruby
docker-compose exec mariadb mysql -u root -p'******' -e "SHOW VARIABLES LIKE 'log_bin';"

+---------------+-------+
| Variable_name | Value |
+---------------+-------+
| log_bin       | ON    |
+---------------+-------+


```

- - - - - -

- - - - - -

### 添加大小写不敏感 (可选功能)

##### 修改`my.cnf`配置文件， 添加大小写不敏感， 需要`down`掉数据库， 再重启

```yaml
cat > config/mariadb-config/50-server.cnf 
```

- - - - - -

- - - - - -

- - - - - -