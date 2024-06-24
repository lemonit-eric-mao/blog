---
title: "Docker 学习笔记(五) 下载/安装/运行 MySQL 5.7"
date: "2017-11-16"
categories: 
  - "docker"
---

#### 查看Docker Hub官网MySQL镜像 https://hub.docker.com/r/library/mysql/tags/

#### 服务器地址: 10.32.156.51

#### 下载mysql 镜像

**docker pull registry.docker-cn.com/library/mysql:5.7**

```ruby
[root@localhost ~]# docker pull registry.docker-cn.com/library/mysql:5.7
5.7: Pulling from library/mysql
85b1f47fba49: Pull complete
5671503d4f93: Pull complete
3b43b3b913cb: Pull complete
4fbb803665d0: Pull complete
05808866e6f9: Pull complete
1d8c65d48cfa: Pull complete
e189e187b2b5: Pull complete
02d3e6011ee8: Pull complete
d43b32d5ce04: Pull complete
2a809168ab45: Pull complete
Digest: sha256:1a2f9361228e9b10b4c77a651b460828514845dc7ac51735b919c2c4aec864b7
Status: Downloaded newer image for registry.docker-cn.com/library/mysql:5.7
[root@localhost ~]#
[root@localhost ~]# docker images
REPOSITORY                             TAG                 IMAGE ID            CREATED             SIZE
registry.docker-cn.com/library/mysql   5.7                 5709795eeffa        10 days ago         408MB
[root@localhost ~]#
```

#### 运行启动

**映射mysql外网访问端口: `3307`** **docker run -p 3307:3306 --restart `策略名称` -e MYSQL\_ROOT\_PASSWORD=`mysql密码` -d `镜像ID`**

```ruby
[root@localhost ~]# docker images
REPOSITORY                             TAG                 IMAGE ID            CREATED             SIZE
registry.docker-cn.com/library/mysql   5.7                 5709795eeffa        10 days ago         408MB
[root@localhost ~]#
[root@localhost ~]# docker run -p 3307:3306 --restart always -e MYSQL_ROOT_PASSWORD=rootroot -d 5709795eeffa
493408f765c6d104e2401cfbdac6231a4bcb31b4d432e6e7deaf18cd48152a09
[root@localhost ~]# docker ps -a
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                    NAMES
493408f765c6        5709795eeffa        "docker-entrypoint..."   5 seconds ago       Up 5 seconds        0.0.0.0:3307->3306/tcp   distracted_kare
[root@localhost ~]#
```

#### Navicat 测试连接 用户名:root 密码:rootroot 端口:3307

#### Docker 容器自启动策略

`no` 不自动重启容器. (默认value) `always` 在容器已经stop掉或Docker stoped/restarted的时候才重启容器 `on-failure` 容器发生error而退出(容器退出状态不为0)重启容器 `unless-stopped` 在容器已经stop掉或Docker stoped/restarted的时候才重启容器

#### 将MySQL的数据存到宿主机上

**docker run -p 3307:3306 --restart `策略名称` -v `宿主机目录:mysql容器目录` -e MYSQL\_ROOT\_PASSWORD=`mysql密码` -d --name=`"容器名称"` `镜像ID`**

```ruby
[root@localhost home]# mkdir /mnt/mysql/data
[root@localhost home]#
[root@localhost home]# cd /mnt/mysql/data/
[root@localhost home]#
[root@localhost data]# pwd
/mnt/mysql/data
[root@localhost mysql-db-backup]# docker run -p 3307:3306 --restart always -v /mnt/mysql/data:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=rootroot -d --name="my-mysql-db" 5709795eeffa
ae6ad83608d864a7c4526b511d09a606e95a30d0b9e317473fbdb2b8c4be815d
[root@localhost mysql-db-backup]#
```

#### 使用本地的MySQL配置文件

`docker run -p 宿主机端口:容器端口 --restart 策略名称 -v 宿主机数据目录:/var/lib/mysql -v 宿主机数据库配置文件目录:/etc/mysql/conf.d -e MYSQL_ROOT_PASSWORD=mysql密码 -d --name="容器名称" 镜像ID`

```ruby
docker run -p 3306:3306 --restart always -v /mnt/mysql/data:/var/lib/mysql -v /mnt/mysql/conf.d:/etc/mysql/connf.d -e MYSQL_ROOT_PASSWORD=shared-server-pwd -d --name="my-mysql-db" 563a026a1511
```
