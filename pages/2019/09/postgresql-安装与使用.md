---
title: "PostgreSQL 安装与使用"
date: "2019-09-05"
categories: 
  - "postgresql"
---

#### CentOS7 postgresql安装与使用

##### 1\. 安装配置postgresql

```ruby
# 安装
[root@test1 ~ ]$ yum -y install postgresql-server
# 初始化
[root@test1 ~ ]$ postgresql-setup initdb
Initializing database ... OK
# 设置postgresql可被远程连接登录
[root@test1 ~ ]$ vim /var/lib/pgsql/data/postgresql.conf
# 第59行取消注释，更改为：
listen_addresses = '*'
# 第397行，添加
log_line_prefix = '%t %u %d '
# 启动
[root@est1 ~ ]$ systemctl start postgresql
# 开机自启动
[root@test1 ~ ]$ systemctl enable postgresql
# 查看数据库版本
[root@test1 ~ ]$ postgres -V
postgres (PostgreSQL) 9.2.24
[root@test1 ~ ]$
```

##### 2\. 配置防火墙(`如果开启了防火墙`)

```ruby
[root@vm-06 ~]# firewall-cmd --add-service=postgresql --permanent
success
[root@vm-06 ~]# firewall-cmd --reload
success
```

##### 3\. 设置PostgreSQL管理员用户的密码并添加一个新用户

```ruby
# 设置PostgreSQL管理员用户的密码
[root@test1 ~ ]$ su - postgres
-bash-4.2$ psql -c "alter user postgres with password 'QWE@2345'"
ALTER ROLE
-bash-4.2$
# 添加一个新用户
-bash-4.2$ createuser eric
-bash-4.2$
# 创建一个测试数据库
-bash-4.2$ createdb testdb -O eric
-bash-4.2$
-bash-4.2$ exit
登出
[root@test1 ~ ]$
```

##### 4\. 简单的操作数据库CRUD

```sql
-bash-4.2$  psql testdb
psql (9.2.24)
输入 "help" 来获取帮助信息.

testdb=# alter user eric with password '123456';
ALTER ROLE
testdb=#
testdb=# create table test (no int,name text );
CREATE TABLE
testdb=#
testdb=# insert into test (no,name) values (1,'devops');
INSERT 0 1
testdb=#
testdb=# select * from test;
 no |  name
----+--------
  1 | devops
(1 行记录)

testdb=# drop table test;
DROP TABLE
testdb=#
testdb=#
testdb=# \q
-bash-4.2$
-bash-4.2$ dropdb testdb
-bash-4.2$
-bash-4.2$
```

* * *

* * *

* * *

#### 使用 Docker compose 安装 PostgreSQL

```ruby
[root@test1 setup_postgreSQL ]$ cat > docker-compose.yml << eric
# 镜像仓库地址：https://hub.docker.com/_/postgres?tab=tags
postgres:
  image: postgres:12
  container_name: PostgreSQL
  restart: always
  environment:
    # 初始化时创建个数据库(可有可无)
    # POSTGRES_DB: dev2
    # 管理员用户名
    POSTGRES_USER: postgres
    # 管理员密码
    POSTGRES_PASSWORD: 'QWE@2345'
  ports:
      - 2345:5432
  volumes:
    - ./data/postgresql:/var/lib/postgresql/data
eric

[root@test1 setup_postgreSQL ]$
[root@test1 setup_postgreSQL ]$ docker-compose up -d
Creating local_postgresql ... done
[root@test1 setup_postgreSQL ]$
```

* * *

* * *

* * *

##### 命令行远程登录

```ruby
[root@test1 setup_postgreSQL ]$ psql -h 172.160.180.46 -p 2345 -U postgres
用户 postgres 的口令：
psql (9.2.24, 服务器 11.5 (Debian 11.5-1.pgdg90+1))
警告：psql 版本9.2， 服务器版本11.0.
一些psql功能可能无法工作.
输入 "help" 来获取帮助信息.

postgres=# \q
[root@test1 setup_postgreSQL ]$
```

* * *

* * *

* * *

##### 安装 PosttreSQL 可视化工具

###### **[DBeaver社区](https://dbeaver.io/ "DBeaver社区")**

###### **[DBeaver社区 下载地址](https://dbeaver.io/download/ "DBeaver社区 下载地址")**

* * *

* * *

* * *
