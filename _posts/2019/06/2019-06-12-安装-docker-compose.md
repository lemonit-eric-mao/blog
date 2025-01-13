---
title: "安装 Docker-Compose"
date: "2019-06-12"
categories: 
  - "docker"
---

##### 安装 docker-compose

###### [安装 Docker](%e5%ae%89%e8%a3%85-docker "安装 Docker")

###### [官网地址](https://docs.docker.com/compose/install/ "官网地址")

###### 官网下载地址(较慢)

``` bash
# 1.x
curl -L "https://github.com/docker/compose/releases/download/1.26.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

# 2.x
curl -L "https://github.com/docker/compose/releases/download/v2.32.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

```

###### 使用自己的七牛云

``` bash
# 下载 V1
curl http://qiniu.dev-share.top/docker-compose-1.26.2-Linux-x86_64 -o /usr/local/bin/docker-compose && chmod -R 777 /usr/local/bin/docker-compose

# 下载 V2
curl http://qiniu.dev-share.top/docker-compose-2.23.3-linux-x86_64 -o /usr/local/bin/docker-compose && chmod -R 777 /usr/local/bin/docker-compose
```

##### 常用命令

``` bash
#  V2 版本支持指定服务名 down

docker-compose --profile frontend down

```

``` bash
# 启动容器
[root@k8s-master ~]# docker-compose up
# 后台启动容器
[root@k8s-master ~]# docker-compose up -d
# 停止并删除启动容器
[root@k8s-master ~]# docker-compose down

# 根据指定的配置文件 启动容器
[root@k8s-master ~]# docker-compose -f docker-compose.yml up
# 根据指定的配置文件 后台启动容器
[root@k8s-master ~]# docker-compose -f docker-compose.yml up -d
# 根据指定的配置文件 停止并删除启动容器
[root@k8s-master ~]# docker-compose -f docker-compose.yml down
# 根据指定的配置文件 查看容器的运行状态
[root@k8s-master ~]# docker-compose -f docker-compose.yml ps
```
