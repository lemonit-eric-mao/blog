---
title: "docker-compose 安装 redis"
date: "2019-12-10"
categories: 
  - "redis"
---

###### 资料

[Docker官网，compose参数解释](https://docs.docker.com/compose/compose-file/ "Docker官网，compose参数解释")

* * *

##### 准备 创建文件夹

```ruby
[root@k8s-master ~]# mkdir -p /home/deploy/redis-compose/config /home/deploy/redis-compose/data && cd /home/deploy/redis-compose/

```

* * *

##### 从官网源码中下载最新稳定版 配置文件 redis.conf

[Redis 官网地址](https://redis.io/download "Redis 官网地址") [最新稳定版源码地址](http://download.redis.io/redis-stable/ "最新稳定版源码地址")

```ruby
# 直接下载到配置文件目录中备用
[root@k8s-master ~]# wget -P /home/deploy/redis-compose/config/redis/ http://download.redis.io/redis-stable/redis.conf

```

* * *

##### 配置 docker-compose.yml (配置 docker 容器内存限制)

```ruby
[root@k8s-master ~]# cat > docker-compose.yml << ERIC
version: '3'
services:

  redis:
    image: redis:6.2
    hostname: redis
    container_name: redis
    restart: always
    ports:
      # 端口映射
      - 6379:6379
    volumes:
      # 目录映射
      - ./config/redis/redis.conf:/usr/local/etc/redis/redis.conf
      - ./config/data:/data
    # 在容器中执行的命令
    command: redis-server /usr/local/etc/redis/redis.conf
ERIC

[root@k8s-master ~]#
```

* * *

##### 修改配置文件 redis.conf 添加密码

```ruby
......
# bind 127.0.0.1 这个是指docker容器内部的地址
# 修改绑定IP为 0.0.0.0 让外网可以访问
bind 0.0.0.0
# 给redis添加密码(加不加随意)
requirepass maosiyu1987
......
```

* * *

##### 启动

```ruby
[root@k8s-master ~]# docker-compose down && docker-compose up -d
[root@k8s-master ~]#
[root@k8s-master ~]# docker-compose logs -f redis
```

* * *

##### **`注意`**

  这里要强调一下， Redis 是`没有用户名`的，`默认`情况下`也没有密码`，可以通过配置文件修改密码，远程访问时只需要使用，ip地址:端口号和密码，进行连接

* * *
