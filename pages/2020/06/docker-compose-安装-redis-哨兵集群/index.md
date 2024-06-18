---
title: "docker-compose 安装 redis 哨兵集群"
date: "2020-06-09"
categories: 
  - "redis"
---

###### **基础知识**

什么是哨兵？ 哨兵作用是干什么的？ 如何实现的高可用？

> [![](http://qiniu.dev-share.top/image/gif/Redis.gif)](http://qiniu.dev-share.top/image/gif/Redis.gif)

* * *

###### 前置条件

| IP | 节点 |
| --- | --- |
| 192.168.2.10 | master |
| 192.168.2.11 | slave |
| 192.168.2.12 | slave |

```ruby
mkdir -p /home/deploy/redis-cluster/config/
mkdir -p /home/deploy/redis-cluster/data/
```

* * *

###### **[官方-配置文件](http://download.redis.io/redis-stable/ "官方-哨兵配置文件")**

```ruby
# 下载 redis 配置文件
wget -P /home/deploy/redis-cluster/config/ http://download.redis.io/redis-stable/redis.conf

# 下载 哨兵 配置文件
wget -P /home/deploy/redis-cluster/config/ http://download.redis.io/redis-stable/sentinel.conf
```

* * *

###### **192.168.2.10 `master`**; 创建主节点 redis-compose 文件

```ruby
cat > /home/deploy/redis-cluster/redis-compose.yml << ERIC
version: '3'

services:

  # 创建 redis
  redis:
    container_name: redis
    image: redis:latest
    network_mode: host
    restart: always
    ports:
      - 6379:6379
    volumes:
      # 容器与宿主机时间同步
      - /etc/localtime:/etc/localtime
      - ./config/redis.conf:/usr/local/etc/redis/redis.conf
      - ./data:/data
    # 在容器中执行的命令
    command: redis-server /usr/local/etc/redis/redis.conf

ERIC

```

###### **192.168.2.10 `master`**; 创建主节点 sentinel-compose 文件

```ruby
cat > /home/deploy/redis-cluster/sentinel-compose.yml << ERIC
version: '3'

services:

  # 创建哨兵
  sentinel:
    container_name: sentinel
    image: redis:latest
    ports:
    - 26379:26379
    volumes:
      # 容器与宿主机时间同步
      - /etc/localtime:/etc/localtime
      - ./config/sentinel.conf:/usr/local/etc/redis/sentinel.conf
    command: redis-sentinel /usr/local/etc/redis/sentinel.conf

ERIC

```

* * *

###### 修改配置文件 redis.conf 添加密码

```ruby
......

# bind 127.0.0.1 这个是指docker容器内部的地址
# 修改绑定IP为 0.0.0.0 让外网可以访问
bind 0.0.0.0

# 给redis添加密码(加不加随意)
requirepass 123456
......
```

* * *

###### 修改配置文件 sentinel.conf

```ruby
cat > /home/deploy/redis-cluster/config/sentinel.conf << ERIC

port 26379

# 关闭了保护模式，便于测试
protected-mode no

# 告诉哨兵，要监控哪个 Redis
# sentinel monitor   代表监控
# mymaster           给要监控的Redis, 起个名
# 192.168.2.10       要监控的Redis, 服务器IP
# 6379               要监控的Redis, 端口
# 2                  代表只有两个或两个以上的哨兵认为主服务器不可用的时候，才会进行failover操作。
sentinel monitor mymaster 192.168.2.10 6379 2

# 告诉哨兵，要监控的 Redis 登录密码
# sentinel author-pass定义服务的密码，mymaster是服务名称，123456是Redis服务器密码
sentinel auth-pass mymaster 123456

sentinel down-after-milliseconds mymaster 5000
sentinel failover-timeout mymaster 5000
sentinel parallel-syncs mymaster 1

ERIC

```

* * *

* * *

* * *

##### 添加 从节点

**192.168.2.11 `slave`**; 使用主节点 compose 文件 **192.168.2.12 `slave`**; 使用主节点 compose 文件

###### 修改配置文件 redis.conf 与`主节点`配置文件`不同` 其它都一样

```ruby
......
# bind 127.0.0.1 这个是指docker容器内部的地址
# 修改绑定IP为 0.0.0.0 使得Redis服务器可以跨网络访问
bind 0.0.0.0
# 给当前Redis添加密码(加不加随意)
requirepass 123456

# 指定Redis主节点服务器，注意：有关slaveof的配置只是配置从服务器，主服务器不需要配置
slaveof 192.168.2.10 6379
# 指定Redis主节点服务器密码，注意：有关slaveof的配置只是配置从服务器，主服务器不需要配置
masterauth 123456
......
```

* * *

##### 修改配置文件 sentinel.conf **`主、从哨兵配置文件都一样`**

* * *

* * *

* * *

###### **[安装 Redis 客户端](http://www.dev-share.top/2020/03/12/centos7-redis-%e5%ae%a2%e6%88%b7%e7%ab%af/ "安装 Redis 客户端")**

* * *

###### **`注意`启动顺序**。首先是启动主机（192.168.2.10）的**`Redis`服务进程**，然后启动从机的服务进程，最后启动3个**`哨兵`的服务进程**。

```ruby
# 1 启动 主服务器
[root@master redis-cluster]# docker-compose -f redis-compose.yml up -d
# 2 启动 从服务器
[root@node1 redis-cluster]# docker-compose -f redis-compose.yml up -d
# 3 启动 从服务器
[root@node2 redis-cluster]# docker-compose -f redis-compose.yml up -d


# 4 启动 主哨兵
[root@master redis-cluster]# docker-compose -f sentinel-compose.yml up -d
# 5 启动 从哨兵
[root@node1 redis-cluster]# docker-compose -f sentinel-compose.yml up -d
# 6 启动 从哨兵
[root@node2 redis-cluster]# docker-compose -f sentinel-compose.yml up -d

```

* * *

* * *

* * *

###### 测试

```ruby
[root@master redis-cluster]# redis-cli -h 192.168.2.10 -p 26379 -a 123456
# 查看 主节点信息
192.168.2.10:26379> sentinel master mymaster
 1) "name"
 2) "mymaster"
 3) "ip"
 4) "192.168.2.10"
 5) "port"
 6) "6379"
 7) "runid"
 8) "9dcbe577bcf199d104317a342a5fa5101c2cacb7"
 9) "flags"
10) "master"
11) "link-pending-commands"
12) "0"
13) "link-refcount"
14) "1"
15) "last-ping-sent"
16) "0"
17) "last-ok-ping-reply"
18) "43"
19) "last-ping-reply"
20) "43"
21) "down-after-milliseconds"
22) "5000"
23) "info-refresh"
24) "7268"
25) "role-reported"
26) "master"
27) "role-reported-time"
28) "1392458"
29) "config-epoch"
30) "0"
31) "num-slaves"
32) "2"                       # 从节点有两台
33) "num-other-sentinels"
34) "3"                       # 有三个哨兵
35) "quorum"
36) "2"
37) "failover-timeout"
38) "5000"
39) "parallel-syncs"
40) "1"
192.168.2.10:26379>
```

```ruby
[root@master redis-cluster]# redis-cli -h 192.168.2.10 -p 26379 -a 123456
# 查看子节点信息
192.168.2.10:26379> sentinel slaves mymaster
1)  1) "name"
    2) "192.168.2.12:6379"
    3) "ip"
    4) "192.168.2.12"
    5) "port"
    6) "6379"
    7) "runid"
    8) "da3f5c946847694f4964c38e1e19984b609303dd"
    9) "flags"
   10) "slave"
   11) "link-pending-commands"
   12) "0"
   13) "link-refcount"
   14) "1"
   15) "last-ping-sent"
   16) "0"
   17) "last-ok-ping-reply"
   18) "171"
   19) "last-ping-reply"
   20) "171"
   21) "down-after-milliseconds"
   22) "5000"
   23) "info-refresh"
   24) "3539"
   25) "role-reported"
   26) "slave"
   27) "role-reported-time"
   28) "1399101"
   29) "master-link-down-time"
   30) "0"
   31) "master-link-status"
   32) "ok"                       # 在线状态
   33) "master-host"
   34) "192.168.2.10"
   35) "master-port"
   36) "6379"
   37) "slave-priority"
   38) "100"
   39) "slave-repl-offset"
   40) "251827"
2)  1) "name"
    2) "192.168.2.11:6379"
    3) "ip"
    4) "192.168.2.11"
    5) "port"
    6) "6379"
    7) "runid"
    8) "06430ff6c01133b2c208f56882b6d046b88c68ae"
    9) "flags"
   10) "slave"
   11) "link-pending-commands"
   12) "0"
   13) "link-refcount"
   14) "1"
   15) "last-ping-sent"
   16) "0"
   17) "last-ok-ping-reply"
   18) "171"
   19) "last-ping-reply"
   20) "171"
   21) "down-after-milliseconds"
   22) "5000"
   23) "info-refresh"
   24) "3539"
   25) "role-reported"
   26) "slave"
   27) "role-reported-time"
   28) "1449266"
   29) "master-link-down-time"
   30) "0"
   31) "master-link-status"
   32) "ok"                       # 在线状态
   33) "master-host"
   34) "192.168.2.10"
   35) "master-port"
   36) "6379"
   37) "slave-priority"
   38) "100"
   39) "slave-repl-offset"
   40) "251827"
192.168.2.10:26379>
```

* * *

###### 测试主从数据是否同步

```ruby
# 主节点 192.168.2.10
[root@master redis-cluster]# redis-cli -h 192.168.2.10 -p 6379 -a 123456
Warning: Using a password with '-a' or '-u' option on the command line interface may not be safe.
192.168.2.10:6379>
192.168.2.10:6379> set key eric:mao
OK
192.168.2.10:6379>
192.168.2.10:6379> get key
"eric:mao"
192.168.2.10:6379>
[root@master redis-cluster]#

# 从节点 192.168.2.11
[root@master redis-cluster]# redis-cli -h 192.168.2.11 -p 6379 -a 123456
Warning: Using a password with '-a' or '-u' option on the command line interface may not be safe.
192.168.2.11:6379>
192.168.2.11:6379> get key
"eric:mao"
192.168.2.11:6379>
[root@master redis-cluster]#

# 从节点 192.168.2.12
[root@master redis-cluster]# redis-cli -h 192.168.2.12 -p 6379 -a 123456
Warning: Using a password with '-a' or '-u' option on the command line interface may not be safe.
192.168.2.12:6379>
192.168.2.12:6379> get key
"eric:mao"
192.168.2.12:6379>
[root@master redis-cluster]#
```

* * *

###### 测试主宕机后，是否自动选举

```ruby
# 停止 Master Redis
[root@master redis-cluster]# docker-compose -f redis-compose.yml stop
Stopping redis ... done

# 在次查看 Master 节点，已经变为 192.168.2.11
[root@master redis-cluster]# redis-cli -h 192.168.2.10 -p 26379 -a 123456
192.168.2.10:26379> sentinel master mymaster
 1) "name"
 2) "mymaster"
 3) "ip"
 4) "192.168.2.11"
 5) "port"
 6) "6379"
 7) "runid"
 8) "06430ff6c01133b2c208f56882b6d046b88c68ae"
 9) "flags"
10) "master"
11) "link-pending-commands"
12) "0"
13) "link-refcount"
14) "1"
15) "last-ping-sent"
16) "0"
17) "last-ok-ping-reply"
18) "31"
19) "last-ping-reply"
20) "31"
21) "down-after-milliseconds"
22) "5000"
23) "info-refresh"
24) "2105"
25) "role-reported"
26) "master"
27) "role-reported-time"
28) "2955"
29) "config-epoch"
30) "1"
31) "num-slaves"
32) "2"                       # 有两个Redis从节点
33) "num-other-sentinels"
34) "3"                       # 有三个哨兵节点
35) "quorum"
36) "2"
37) "failover-timeout"
38) "5000"
39) "parallel-syncs"
40) "1"

# 查看 从节点
192.168.2.12:26379> sentinel slaves mymaster
1)  1) "name"
    2) "192.168.2.12:6379"
    3) "ip"
    4) "192.168.2.12"
    5) "port"
    6) "6379"
    7) "runid"
    8) "da3f5c946847694f4964c38e1e19984b609303dd"
    9) "flags"
   10) "slave"
   11) "link-pending-commands"
   12) "0"
   13) "link-refcount"
   14) "1"
   15) "last-ping-sent"
   16) "0"
   17) "last-ok-ping-reply"
   18) "561"
   19) "last-ping-reply"
   20) "561"
   21) "down-after-milliseconds"
   22) "5000"
   23) "info-refresh"
   24) "7875"
   25) "role-reported"
   26) "slave"
   27) "role-reported-time"
   28) "7970"
   29) "master-link-down-time"
   30) "0"
   31) "master-link-status"
   32) "ok"                       # 在线状态
   33) "master-host"
   34) "192.168.2.11"
   35) "master-port"
   36) "6379"
   37) "slave-priority"
   38) "100"
   39) "slave-repl-offset"
   40) "315441"
2)  1) "name"
    2) "192.168.2.10:6379"
    3) "ip"
    4) "192.168.2.10"
    5) "port"
    6) "6379"
    7) "runid"
    8) ""
    9) "flags"
   10) "s_down,slave,disconnected"
   11) "link-pending-commands"
   12) "3"
   13) "link-refcount"
   14) "1"
   15) "last-ping-sent"
   16) "7970"
   17) "last-ok-ping-reply"
   18) "7970"
   19) "last-ping-reply"
   20) "7970"
   21) "s-down-time"
   22) "2936"
   23) "down-after-milliseconds"
   24) "5000"
   25) "info-refresh"
   26) "1594276335299"
   27) "role-reported"
   28) "slave"
   29) "role-reported-time"
   30) "7970"
   31) "master-link-down-time"
   32) "0"
   33) "master-link-status"
   34) "err"                       # 在这里发现原来的 主节点Redis已经不在线
   35) "master-host"
   36) "?"
   37) "master-port"
   38) "0"
   39) "slave-priority"
   40) "100"
   41) "slave-repl-offset"
   42) "0"
192.168.2.12:26379>

```

##### 测试总结

1. 当 主节点切换到 node1 以后， 原来的master 启动时，**要手动指定 `新的master节点IP`地址** ，才可以重新加入到集群中
2. 从节点不能够添加数据，只有`主节点才可以添加数据`，那么 **`问题`来了** ， master 节点IP地址发生了变化， 在应用程序使用上会出现 `连接失败`或者`不能写入数据`的问题, 所以要考虑是否使用 HAProxy 代替哨兵 做Redis高可用+负载均衡
