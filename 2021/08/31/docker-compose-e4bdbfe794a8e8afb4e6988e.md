---
title: 'docker-compose 使用说明'
date: '2021-08-31T09:02:47+00:00'
status: publish
permalink: /2021/08/31/docker-compose-%e4%bd%bf%e7%94%a8%e8%af%b4%e6%98%8e
author: 毛巳煜
excerpt: ''
type: post
id: 7821
category:
    - Docker
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
wb_sst_seo:
    - 'a:3:{i:0;s:0:"";i:1;s:0:"";i:2;s:0:"";}'
---
- - - - - -

- - - - - -

- - - - - -

##### docker-compose.yaml 的常见用法，和 entrypoint 与 command的区别

###### 测试

```yaml
version: '3.6'
services:
  nginx:
    image: nginx:alpine
    restart: always
    # 容器内权限全开，让docker容器内应用获取宿主机root权限。
    privileged: true
#    # 细粒度设置容器内权限，需要什么开什么
#    cap_add:
#     - SYS_PTRACE
    # 指定root用户
    user: root
    # 指定容器中的主机名
    hostname: eric_os
    # 添加hosts解析域名
    extra_hosts:
      - 'eric.rabbitmq.com:12.3.4.5'
    container_name: nginx
    # 定义日志配置
    logging:
    # 指定日志驱动程序为 json-file
      driver: json-file
      # 配置日志驱动程序的选项
      options:
        # 设置单个日志文件的最大大小为 10MB
        max-size: 10m
        # 设置保留的日志文件数量为 3，注意：需要使用引号包裹数字
        max-file: '3'

#    # 资源使用配置 只有在swarm下才可用
#    deploy:
#      resources:
#         # 容器能够使用的资源上限
#         limits:
#            cpus: "2.00"
#            memory: 5G
#         # 容器初始化时预申请资源
#         reservations:
#            memory: 200M
    # 端口映射
    ports:
      - 80:80
    volumes:
      - /etc/localtime:/etc/localtime
    command: |
      echo 'Hello Command'
    entrypoint: |
      echo 'Hello Entrypoint'
#    # 判断文件不存在时，在执行
#    entrypoint: /bin/bash -c "test -f /file/50-server.cnf || cp /etc/mysql/mariadb.conf.d/50-server.cnf /file/50-server.cnf"


#    # 容器执行运行
#    entrypoint: tail -f /dev/null

#    # 串行运行
#    entrypoint:
#      - /bin/bash
#      - -c
#      - |
#          test -f /file/my.cnf || cp /etc/mysql/my.cnf /file/
#          tail -f /dev/null

#    # 并行运行
#    entrypoint:
#      - /bin/bash
#      - -c
#      - |
#          test -f /file/my.cnf || cp /etc/mysql/my.cnf /file/ &
#          tail -f /dev/null

#    # 特殊的环境变量写法
#    environment:
#      - |
#        TZ= Asia/Shanghai
#      - |
#        FLINK_PROPERTIES=
#        jobmanager.rpc.address: jobmanager


```

- - - - - -

###### 查看

```ruby
## 运行
docker-compose up -d

docker ps --no-trunc -a --format "table {{.Names}}\t{{.Image}}\t{{.Command}}"
NAMES     IMAGE          COMMAND
nginx     nginx:alpine   "echo Hello Entrypoint echo Hello Command"


```

- - - - - -

###### 总结

从结果中可以看出， Docker会先执行 entrypoint的指令，然后在接着执行 command的指令； **`command`是做为`entrypoint`的参数**

- - - - - -

- - - - - -

- - - - - -

##### docker-compose 配置**全局字符串**与**全局数组**

> - **注意**：Compose文件的`有效顶级属性`包括： 
>   - version, services, networks, volumes, secrets, configs
>   - 和扩展属性的特殊标识 `x-`
>       - **`x-`{name}** 模版命名规则 以`x-`开头 用于复用

```yaml
version: '3.6'

# 定义全局字符串
x-str:
  &timezone
  "Asia/Shanghai"

# 定义全局数组
x-array:
  &hosts
  - "hostname:127.0.0.1"
  - "hostname:127.0.0.2"
  - "hostname:127.0.0.3"


services:
  web:
    image: nginx
    # 测试使用数组
    extra_hosts: *hosts
    # 测试使用字符串
    environment:
      TZ: *timezone


```

**验证docker-compose文件**

```ruby
[root@centos ~]# docker-compose config
services:
  web:
    environment:
      TZ: Asia/Shanghai
    extra_hosts:
    - hostname:127.0.0.1
    - hostname:127.0.0.2
    - hostname:127.0.0.3
    image: nginx
version: '3.4'


```

- - - - - -

##### 基于 docker-compose 容器网络中是如何实现通信的

> - 我们都见过这样的 **docker-compose.yaml**

```yaml
version: '3.1'
services:
  sql-client:
    restart: always
    user: flink:flink
    image: apache/flink-sql-client:1.14.5-java11
    depends_on:
      - jobmanager
    environment:
      TZ: Asia/Shanghai
      FLINK_JOBMANAGER_HOST: jobmanager
    volumes:
      - /etc/localtime:/etc/localtime
      - ./config/lib/:/opt/flink/lib/

  jobmanager:
    restart: always
    user: flink:flink
    image: apache/flink:1.14.5-java11
    ports:
      - 8081:8081
    command: jobmanager
    environment:
      - |
        TZ= Asia/Shanghai
      - |
        FLINK_PROPERTIES=
        jobmanager.rpc.address: jobmanager

    volumes:
      - /etc/localtime:/etc/localtime
      - ./config/lib/:/opt/flink/lib/

  taskmanager:
    restart: always
    user: flink:flink
    image: apache/flink:1.14.5-java11
    depends_on:
      - jobmanager
    command: taskmanager
    environment:
      - |
        TZ= Asia/Shanghai
      - |
        FLINK_PROPERTIES=
        jobmanager.rpc.address: jobmanager
        taskmanager.numberOfTaskSlots: 2

    volumes:
      - /etc/localtime:/etc/localtime
      - ./config/lib/:/opt/flink/lib/


```

> - 在这里我们只关注应用的网络访问顺序 **sql-client** --RPC访问--&gt; **jobmanager** --RPC访问--&gt; **taskmanager**  
>    那么它是如何实现通过服务名进行的网络访问的呢？  
>    **docker-compose** 在初始化时会自动创建一个属于自己的**网桥**，结果如下：

```ruby
## 查看 docker-compose 文件
[root@centos01 flink-cdc]# ll
total 4
drwxrwxrwx 3 root root   17 Jul  5 15:12 config
-rw-r--r-- 1 root root 1179 Jul  5 15:51 docker-compose.yaml


## 查看 docker-compose 所在的目录
[root@centos01 flink-cdc]# pwd
/data/deploy/flink-cdc


## 查看 docker 容器网络
[root@centos01 flink-cdc]# docker network ls
NETWORK ID     NAME                  DRIVER    SCOPE
9ff7bc2ef8f6   flink-cdc_default     bridge    local


```

> - **flink-cdc\_default** 的命名规则为，**docker-compose.yaml** 所在的 **`目录名_default`**， `_default` 可以通过 `networks:` 修改  
>    **docker-compose** 在初始化时还会将它管辖的服务都加入到这个**网桥**中，结果如下：

```ruby
[root@centos01 flink-cdc]# docker network inspect flink-cdc_default
[
    {
        "Name": "flink-cdc_default",
        "Id": "9ff7bc2ef8f633f369c48adbbd3aa40dd6f324890ad8b2b853c6d4627ddc2508",
        "Created": "2022-07-05T16:47:22.886040651+08:00",
        "Scope": "local",
        "Driver": "bridge",
        "EnableIPv6": false,
        "IPAM": {
            "Driver": "default",
            "Options": null,
            "Config": [
                {
                    "Subnet": "192.168.160.0/20",
                    "Gateway": "192.168.160.1"
                }
            ]
        },
        "Internal": false,
        "Attachable": true,
        "Ingress": false,
        "ConfigFrom": {
            "Network": ""
        },
        "ConfigOnly": false,
        "Containers": {
            "1f033a1c827dd03f9e24168df74b7f051e1155f70ef778d075f0af6999e5e17e": {
                "Name": "flink-cdc_jobmanager_1",
                "EndpointID": "becf3a1d01bb7270f748dda81445a716a922c6b0cc423d24f2dce69b06c1d0a3",
                "MacAddress": "02:42:c0:a8:a0:02",
                "IPv4Address": "192.168.160.2/20",
                "IPv6Address": ""
            },
            "962a29dd3f03860fbb359bcdd9dd27b2975e23232d7649db97a240e2b679ac5e": {
                "Name": "flink-cdc_taskmanager_1",
                "EndpointID": "110bfcba876dc418f2266ae014cf9aafdec03c084f51af3713b611c3c8f8170e",
                "MacAddress": "02:42:c0:a8:a0:03",
                "IPv4Address": "192.168.160.3/20",
                "IPv6Address": ""
            },
            "c65e6a0ade7f43409663656347edb9f3e775f50160b442545958ad2fceee6d5e": {
                "Name": "flink-cdc_sql-client_1",
                "EndpointID": "8e2a40c5754a4bd1ca5d78c760a65b2a073119537722e0c87ed9e45c6b4a2323",
                "MacAddress": "02:42:c0:a8:a0:04",
                "IPv4Address": "192.168.160.4/20",
                "IPv6Address": ""
            }
        },
        "Options": {},
        "Labels": {
            "com.docker.compose.network": "default",
            "com.docker.compose.project": "flink-cdc",
            "com.docker.compose.version": "1.26.2"
        }
    }
]


```

> - 到这里我才明白，容器之间的内部网络通信，都是通过这个网桥进行路由的；因此，如果我们想让其它的应用程序也能够使用容器内部网络，那么我们把它加入到相同的网桥中就可以了。  
>    不过这，只是在**同一个主机中的容器之间网络通信**，跨主机这样是无法通信的。  
>    所以我想到了**k8s的容器网络插件calico**，它就是解决了**跨主机容器之间的网络通信**。

- - - - - -

- - - - - -

- - - - - -