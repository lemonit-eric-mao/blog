---
title: "使用 docker-compose 做 TiDB-Server 负载均衡-HAProxy"
date: "2019-09-25"
categories: 
  - "tidb"
---

#### 使用HAProxy 为TiDB-Server 做负载均衡

[安装 docker-compose](http://www.dev-share.top/2019/06/12/%E5%AE%89%E8%A3%85-docker-compose/ "安装 docker-compose")

##### 环境

- IP: 172.160.180.46
- 系统： CentOS 7
- Core: 8核
- HAProxy版本 2.0.6

| 服务器 | IP | hostname |
| --- | --- | --- |
| HAProxy | 172.160.180.46 | test1 |
| TiDB-Server | 172.160.180.47 | test2 |
| TiDB-Server | 172.160.180.48 | test3 |
| TiDB-Server | 172.160.181.18 | test4 |

##### 创建文件夹

```ruby
mkdir -p /home/tidb/haproxy/config
```

##### 配置haproxy.cfg

```ruby
cat > /home/tidb/haproxy/config/haproxy.cfg << eric
global
  maxconn 10000                 # 最大同时10000连接
  daemon                        # 以daemon方式在后台运行

defaults
  log     127.0.0.1 local0 debug       # [emerg, alert, crit, err, warning, notice, info, debug]
  # mode http                   # 默认的模式mode { tcp|http|health }，tcp是4层，http是7层，health只会返回OK
  retries         3             # 连接后端服务器失败重试次数，超过3次后会将失败的后端服务器标记为不可用。
  timeout client  1h            # 客户端响应超时             1小时
  timeout server  1h            # server端响应超时           1小时
  timeout connect 1h            # 连接server端超时           1小时
  timeout check   10s           # 对后端服务器的检测超时时间 10秒

listen stats                    # 定义监控页面
  mode  http
  bind  *:1080                  # 绑定容器内的1080端口
  stats refresh 1s              # 每1秒更新监控数据
  stats uri /stats              # 访问监控页面的uri
  stats realm HAProxy\ Stats    # 监控页面的认证提示
  stats auth admin:654321       # 监控页面的用户名和密码

frontend tidb_front
  mode  tcp
  bind  *:4000                  # 监听容器内的4000端口
  default_backend tidb_back

backend tidb_back

  mode    tcp
  option  tcp-check
  balance roundrobin

  server TiDB-Server-test2 172.160.180.47:4000 check inter 10s rise 3 fall 3 weight 1
  server TiDB-Server-test3 172.160.180.48:4000 check inter 10s rise 3 fall 3 weight 2
  server TiDB-Server-test4 172.160.181.18:4000 check inter 10s rise 3 fall 3 weight 3
eric

```

##### 创建 docker-compose.yaml 文件

```ruby
cat > /home/tidb/haproxy/docker-compose.yaml << eric
version: '3.1'

services:

  HAProxy:
    image: haproxy:2.0.6
    restart: always
    container_name: HAProxy
    ports:
      - 4600:4000 # 宿主机端口:容器内端口
      - 1080:1080
    volumes:
      # 容器与宿主机时间同步
      - /etc/localtime:/etc/localtime
      - ./config/haproxy.cfg:/usr/local/etc/haproxy/haproxy.cfg
    environment:
      TIME_ZONE: Asia/Shanghai
eric

```

**`查看管理界面：`** **http://172.160.180.46:1080/stats** **`数据库连接地址：`** **172.160.180.46:4600**

* * *

##### [参照官方文档](https://pingcap.com/docs-cn/v3.0/reference/best-practices/haproxy/ "参照官方文档")

* * *

##### haproxy.cfg 配置详解

```ruby
global
  log     127.0.0.1 local0
  maxconn 32                    # 最大同时32连接
  daemon                        # 以daemon方式在后台运行

  nbproc 8                      # 开启的haproxy进程数，通常与CPU核数保持一致，开启多进程提高并发处理能力。(可选 调优)
  cpu-map 1 0                   # CPU绑定： 这个配置指令有2个参数，第一参数是进程序号，从1开始。第二个参数是CPU序号，从0开始。(可选 调优)
  cpu-map 2 1
  cpu-map 3 2
  cpu-map 4 3
  cpu-map 5 4
  cpu-map 6 5
  cpu-map 7 6
  cpu-map 8 7
  nbthread 1                    # 指定每个haproxy进程开启的线程数，默认为每个进程一个线程。(可选 调优)

defaults
  # mode http                   # 默认的模式mode { tcp|http|health }，tcp是4层，http是7层，health只会返回OK
  retries         3             # 连接后端服务器失败重试次数，超过3次后会将失败的后端服务器标记为不可用。

  # 超时时间如果设置的太短，会导致应用程序断开连接，建议根据实际情况调整
  timeout client  30s           # 客户端响应超时             30秒
  timeout server  30s           # server端响应超时           30秒
  timeout connect 5s            # 连接server端超时           5秒
  timeout check   10s           # 对后端服务器的检测超时时间  10秒

listen stats                    # 定义监控页面
  mode  http
  bind  *:1080                  # 绑定容器内的1080端口
  stats refresh 1s              # 每1秒更新监控数据
  stats uri /stats              # 访问监控页面的uri
  stats realm HAProxy\ Stats    # 监控页面的认证提示
  stats auth admin:654321       # 监控页面的用户名和密码

frontend tidb_front
  mode tcp
  bind *:4000                   # 监听容器内的4000端口
  default_backend tidb_back

backend tidb_back

  mode     tcp
  option   tcp-check            # 这个必须要加，否则健康检查会失败，因为当前使用的是TCP协议，它表示使用TCP协议做检查，而不是使用HTTP或health协议

  # 8种负载均衡方式
  1.balance roundrobin          # 轮询，软负载均衡基本都具备这种算法
  2.balance static-rr           # 根据权重，建议使用
  3.balance leastconn           # 最少连接者先处理，建议使用
  4.balance source              # 根据请求源IP，建议使用
  5.balance uri                 # 根据请求的URI
  6.balance url_param，         # 根据请求的URl参数'balance url_param' requires an URL parameter name
  7.balance hdr(name)           # 根据HTTP请求头来锁定每一次HTTP请求
  8.balance rdp-cookie(name)    # 根据据cookie(name)来锁定并哈希每一次TCP请求

  balance  roundrobin           # roundrobin 轮询方式

  # 健康检查:
  1.inter:   时间间隔10秒
  2.rise:    重试三次
  3.fall:    失败三次连接状态将变为DOWN
  4.weight:  权重1
  server TiDB-Server-test2 172.160.180.47:4000 check inter 10s rise 3 fall 3 weight 1
  server TiDB-Server-test3 172.160.180.48:4000 check inter 10s rise 3 fall 3 weight 2
  server TiDB-Server-test4 172.160.181.18:4000 check inter 10s rise 3 fall 3 weight 3

```

* * *

* * *

* * *
