---
title: "docker-compose 安装 mysql 8.0"
date: "2019-08-05"
categories: 
  - "mysql"
---

[目前最新版](https://hub.docker.com/_/mysql?tab=tags "目前最新版")

[安装 docker-compose](http://www.dev-share.top/2019/06/12/%e5%ae%89%e8%a3%85-docker-compose/ "安装 docker-compose")

##### docker-compose安装

```ruby
[root@dev1 deploy]# mkdir -p /home/deploy/mysqldb/config && cd /home/deploy/mysqldb/
[root@dev1 deploy]#

[root@dev1 mysqldb]# cat > docker-compose.yaml << ERIC
version: '3.1'

services:

  mysql:
    image: mysql:8.0.33
    restart: always
    container_name: mysqldb
    environment:
      TIME_ZONE: Asia/Shanghai
      MYSQL_ROOT_PASSWORD: yourpasswd
    command:
      --default-authentication-plugin=mysql_native_password
      --character-set-server=utf8mb4
      --collation-server=utf8mb4_general_ci
      --explicit_defaults_for_timestamp=true
      --lower_case_table_names=1
    ports:
      - 3305:3306
    volumes:
      # 容器与宿主机时间同步
      - /etc/localtime:/etc/localtime
      - ./config/data/mysql:/var/lib/mysql
ERIC

[root@dev1 mysqldb]#
[root@dev1 mysqldb]# docker-comopose up -d
[root@dev1 mysqldb]#
[root@dev1 mysqldb]# docker-compose ps
 Name                Command               State                 Ports
------------------------------------------------------------------------------------
mysqldb   docker-entrypoint.sh --def ...   Up      0.0.0.0:3305->3306/tcp, 33060/tcp
[root@dev1 mysqldb]#
```

##### 访问：默认不能使用 localhost 要使用数据库服务器的IP进行访问

```ruby
[root@dev1 mysqldb]# mysql -h 172.160.180.6 -u root -P 3305 -p
```
