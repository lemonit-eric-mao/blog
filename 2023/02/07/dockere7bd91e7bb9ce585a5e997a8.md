---
title: Docker网络入门
date: '2023-02-07T20:40:02+00:00'
status: private
permalink: /2023/02/07/docker%e7%bd%91%e7%bb%9c%e5%85%a5%e9%97%a8
author: 毛巳煜
excerpt: ''
type: post
id: 5066
category:
    - Docker
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
wb_sst_seo:
    - 'a:3:{i:0;s:0:"";i:1;s:0:"";i:2;s:0:"";}'
---
实验一 默认情况
--------

> 默认情况下，使用不同docker-compose创建的容器，默认都会创建一个只属于自己的独有网络

### 部署测试应用 App\_01

- ```shell
  ┌──(root@centos01 16:39:20) - [/data/deploy/siyu.mao/docker-network/app_01]
  └─#
  cat > docker-compose.yaml 
  ```

### 部署测试应用 App\_02

- ```shell
  ┌──(root@centos01 16:39:20) - [/data/deploy/siyu.mao/docker-network/app_02]
  └─#
  cat > docker-compose.yaml 
  ```

### 部署测试应用 App\_03

- ```shell
  ┌──(root@centos01 16:40:08) - [/data/deploy/siyu.mao/docker-network/app_03]
  └─#
  cat > docker-compose.yaml 
  ```

### 查看程序运行状态

- ```shell
  ┌──(root@centos01 16:47:39) - [/data/deploy/siyu.mao/docker-network/app_01]
  └─# docker ps
  
  CONTAINER ID   IMAGE              COMMAND              CREATED          STATUS          PORTS                                   NAMES
  118ed36480d8   httpd:alpine3.15   "httpd-foreground"   10 seconds ago   Up 9 seconds    0.0.0.0:8003->80/tcp, :::8003->80/tcp   httpd_03
  551de6083d95   httpd:alpine3.15   "httpd-foreground"   13 seconds ago   Up 12 seconds   0.0.0.0:8002->80/tcp, :::8002->80/tcp   httpd_02
  874b18671ff2   httpd:alpine3.15   "httpd-foreground"   10 minutes ago   Up 10 minutes   0.0.0.0:8001->80/tcp, :::8001->80/tcp   httpd_01
  
  
  ```

### 查看网络

- ```shell
  ┌──(root@centos01 16:49:54) - [/data/deploy/siyu.mao/docker-network/app_01]
  └─# docker network ls
  
  NETWORK ID     NAME             DRIVER    SCOPE
  2eea53b1323d   app_01_default   bridge    local
  16797046ac3b   app_02_default   bridge    local
  898a9bbc9398   app_03_default   bridge    local
  c6a379fc69c5   bridge           bridge    local
  be13cec6c76e   host             host      local
  8b9f32c0e4af   none             null      local
  
  
  ```
  
  
  - #### 解释
  - > - 以下3个是创建应用程序时自动生成的，每个应用程序的网络都是独有的，相互隔离 
      >       1. 2eea53b1323d app\_01\_default bridge local
      >       2. 16797046ac3b app\_02\_default bridge local
      >       3. 898a9bbc9398 app\_03\_default bridge local
      > - 以下3个是docker默认创建的3个网络 
      >       1. c6a379fc69c5 bridge bridge local # 指向虚拟网卡 docker0
      >       2. be13cec6c76e host host local # 没任何指向
      >       3. 8b9f32c0e4af none null local # 没任何指向

### 测试结果

- ```shell
  ┌──(root@centos01 18:41:43) - [/data/deploy/siyu.mao/docker-network/app_01]
  └─# docker exec httpd_01 ping httpd_02
  
  ping: bad address 'httpd_02'
  
  
  
  ```
- > 使用容器内的域名【无法通信】

实验二 单主机容器内通信
------------

> 如果让多个容器共享网络，需要自定义网络，然后让所有的容器都加入到同一个网络中

### 创建自定义网络

- ```shell
  ┌──(root@centos01 18:25:29) - [/data/deploy/siyu.mao/docker-network/eric_mao]
  └─# docker network create app_network
  
  ## 查看网络
  ┌──(root@centos01 18:25:44) - [/data/deploy/siyu.mao/docker-network/eric_mao]
  └─# docker network ls
  
  NETWORK ID     NAME          DRIVER    SCOPE
  f3d985204fd8   app_network   bridge    local
  c6a379fc69c5   bridge        bridge    local
  be13cec6c76e   host          host      local
  8b9f32c0e4af   none          null      local
  
  
  ```

### 修改测试应用 App\_01

- ```shell
  ┌──(root@centos01 16:39:20) - [/data/deploy/siyu.mao/docker-network/app_01]
  └─#
  cat > docker-compose.yaml 
  ```

### 修改测试应用 App\_02

- ```shell
  ┌──(root@centos01 16:39:20) - [/data/deploy/siyu.mao/docker-network/app_02]
  └─#
  cat > docker-compose.yaml 
  ```

### 修改测试应用 App\_03

- ```shell
  ┌──(root@centos01 16:40:08) - [/data/deploy/siyu.mao/docker-network/app_03]
  └─#
  cat > docker-compose.yaml 
  ```

### 查看程序运行状态

- ```shell
  ┌──(root@centos01 18:56:51) - [/data/deploy/siyu.mao/docker-network/app_01]
  └─# docker ps
  CONTAINER ID   IMAGE              COMMAND              CREATED          STATUS          PORTS                                   NAMES
  4076a7f95efa   httpd:alpine3.15   "httpd-foreground"   28 minutes ago   Up 28 minutes   0.0.0.0:8003->80/tcp, :::8003->80/tcp   httpd_03
  fdd2e1b78272   httpd:alpine3.15   "httpd-foreground"   28 minutes ago   Up 28 minutes   0.0.0.0:8002->80/tcp, :::8002->80/tcp   httpd_02
  3498778ffb3a   httpd:alpine3.15   "httpd-foreground"   28 minutes ago   Up 28 minutes   0.0.0.0:8001->80/tcp, :::8001->80/tcp   httpd_01
  
  
  ```

### 测试结果

- ```shell
  ┌──(root@centos01 18:41:43) - [/data/deploy/siyu.mao/docker-network/app_01]
  └─# docker exec httpd_01 ping httpd_02
  
  PING httpd_02 (172.25.0.3): 56 data bytes
  64 bytes from 172.25.0.3: seq=0 ttl=64 time=0.207 ms
  64 bytes from 172.25.0.3: seq=1 ttl=64 time=0.183 ms
  
  
  ┌──(root@centos01 18:56:46) - [/data/deploy/siyu.mao/docker-network/app_01]
  └─# docker exec httpd_01 ping httpd_03
  
  PING httpd_03 (172.25.0.4): 56 data bytes
  64 bytes from 172.25.0.4: seq=0 ttl=64 time=0.597 ms
  64 bytes from 172.25.0.4: seq=1 ttl=64 time=0.134 ms
  
  
  
  ```
- > 使用容器内的域名已经【可以通信了】

### 解释

- ```shell
  ┌──(root@centos01 19:02:08) - [~]
  └─# docker network inspect app_network | jq
  [
  {
    "Name": "app_network",
    "Id": "f3d985204fd8e62361dae29bd94a11318b3cf7f3b3dfea72600226321c2f524e",
    "Created": "2023-02-07T18:25:44.542619303+08:00",
    "Scope": "local",
    "Driver": "bridge",
    "EnableIPv6": false,
    "IPAM": {
      "Driver": "default",
      "Options": {},
      "Config": [
        {
          "Subnet": "172.25.0.0/16",    # 子网地址
          "Gateway": "172.25.0.1"       # 网关地址
        }
      ]
    },
    "Internal": false,
    "Attachable": false,
    "Ingress": false,
    "ConfigFrom": {
      "Network": ""
    },
    "ConfigOnly": false,
    "Containers": {                      # 在同一个网络中的【容器】
      "3498778ffb3aae1a9bc3a681e031362772f8babb17ed2e1deaf7bca624ce485a": {
        "Name": "httpd_01",              # 容器名称
        "EndpointID": "930f16333b99c198b173b9a2b57c45585e0a778d4c378f69ecaa2964fbafbd16",
        "MacAddress": "02:42:ac:19:00:02",
        "IPv4Address": "172.25.0.2/16",  # 容器地址
        "IPv6Address": ""
      },
      "4076a7f95efa0b447d5d337b612ade8010b2d6ba9b79b128ccbf3d84a7dc767f": {
        "Name": "httpd_03",              # 容器名称
        "EndpointID": "5c378a3ea1aab334d671a9126afd0fb0bcfdcaa71eebeefd3d13350796e0ceef",
        "MacAddress": "02:42:ac:19:00:04",
        "IPv4Address": "172.25.0.4/16",  # 容器地址
        "IPv6Address": ""
      },
      "fdd2e1b782724d4f6577a18ce604b8aeacc298fc4318dc50f14959c20010164b": {
        "Name": "httpd_02",              # 容器名称
        "EndpointID": "d760c2158360cb63e45360d30e77a66196bdb7afc644cfe837dd290713d15d8d",
        "MacAddress": "02:42:ac:19:00:03",
        "IPv4Address": "172.25.0.3/16",  # 容器地址
        "IPv6Address": ""
      }
    },
    "Options": {},
    "Labels": {}
  }
  ]
  
  
  ```
- > 1. `实验一`中的容器不能够直接使用`容器内网络`进行通信，是因为每个容器都在自己独有的网络中，相互网络是隔离的
  > 2. `实验二`中使用了共享网络，所有容器都是在同一个网络中，所以才能够进行通信

实验三 跨主机通信
---------

> 如果有两台主机`host1`和`host2`，两主机上的`docker`容器是两`个独立的二层网络`，通过在主机中添加`静态路由`来实现`跨主机通信`。