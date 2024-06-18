---
title: "docker-compose 安装 mariadb"
date: "2019-08-05"
categories: 
  - "mysql"
---

[目前最新版](https://hub.docker.com/_/mariadb?tab=tags "目前最新版")

[安装 docker-compose](http://www.dev-share.top/2019/06/12/%e5%ae%89%e8%a3%85-docker-compose/ "安装 docker-compose")

* * *

##### 创建文件夹

```ruby
mkdir -p mariadb/config/mariadb-config/

```

* * *

##### 创建 docker-compose 文件

```ruby
cat > mariadb/docker-compose.yaml << ERIC

version: '3.6'

services:

  # 复制文件
  copy-file:
    privileged: true
    user: root
    container_name: copy-file
    image: mariadb:10.6.0
    volumes:
      - ./config/mariadb-config/:/file
    # 判断文件不存在时，在执行
    entrypoint: /bin/bash -c "test -f /file/50-server.cnf || cp /etc/mysql/mariadb.conf.d/50-server.cnf /file/50-server.cnf"


  mariadb:
    depends_on:
      - copy-file
    image: mariadb:10.6.0
    restart: always
    container_name: mariadb
    ports:
      # 端口映射
      - 3306:3306
    volumes:
      # 容器与宿主机时间同步
      - /etc/localtime:/etc/localtime
      # 数据库目录映射
      - ./config/mariadb:/var/lib/mysql
      # 数据库配置文件映射
      - ./config/mariadb-config/:/etc/mysql/conf.d/
    environment:
      TIME_ZONE: Asia/Shanghai
      MYSQL_ROOT_PASSWORD: '******'

ERIC

```

* * *

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

* * *

##### 访问：默认不能使用 localhost 要使用数据库服务器的IP进行访问

```ruby
[root@master mariadb]# mysql -h 192.168.2.10 -u root -P 3306 -p
```

* * *

* * *

##### 只开启binlog (可选功能)

> 修改配置文件, 加如下内容

```ruby
cat > config/mariadb-config/50-server.cnf << ERIC

# Start Binlog
[mysqld]
server-id               = 1
log_bin                 = /var/log/mysql/mariadb-bin
log_bin_index           = /var/log/mysql/mariadb-bin.index
expire_logs_days        = 10
binlog_format           = ROW
# End Binlog

ERIC


## 重启数据库
docker-compose restart

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

* * *

* * *

### 添加大小写不敏感 (可选功能)

##### 修改`my.cnf`配置文件， 添加大小写不敏感， 需要`down`掉数据库， 再重启

```yaml
cat > config/mariadb-config/50-server.cnf << ERIC

[mysqld]
# 添加大小写不敏感， 默认的SQL语句是大小写敏感的
lower_case_table_names = 1
pid-file        = /var/run/mysqld/mysqld.pid
socket          = /var/run/mysqld/mysqld.sock
port            = 3306
basedir         = /usr
datadir         = /var/lib/mysql
tmpdir          = /tmp
lc_messages_dir = /usr/share/mysql
lc_messages     = en_US
skip-external-locking

ERIC


## 重启数据库
docker-compose down && docker-compose up -d

```

* * *

* * *

* * *
