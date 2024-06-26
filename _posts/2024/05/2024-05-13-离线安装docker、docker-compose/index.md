---
title: "离线安装docker、docker-compose"
date: "2024-05-13"
categories: 
  - "centos"
  - "docker"
---

## 准备工作

```bash
[root@localhost ~]# cat /etc/redhat-release
Red Hat Enterprise Linux Server release 7.9 (Maipo)

```

#### 文件列表

```
deploy/
└── docker-lib
    ├── docker-24.0.6.tgz
    ├── docker-compose-linux-x86_64
    ├── docker-compose.yaml
    └── kkdd_milvus-images.docker
```

## 安装部署

### 1\. 离线-安装Docker

[离线包下载地址](https://download.docker.com/linux/static/stable/x86_64/)

> https://download.docker.com/linux/static/stable/x86\_64/docker-24.0.6.tgz

#### 解压安装

```bash
# 将压缩文件中的内容解压到 /usr/local/bin 目录，并忽略压缩文件中的顶层目录结构。
tar -xvf deploy/docker-lib/docker-24.0.6.tgz -C /usr/local/bin --strip-components=1

# 查看
[root@localhost ~]# ll /usr/local/bin
total 182244
-rwxr-xr-x. 1 cloud cloud 39129088 Sep  4  2023 containerd
-rwxr-xr-x. 1 cloud cloud 12374016 Sep  4  2023 containerd-shim-runc-v2
-rwxr-xr-x. 1 cloud cloud 19140608 Sep  4  2023 ctr
-rwxr-xr-x. 1 cloud cloud 34752096 Sep  4  2023 docker
-rwxr-xr-x. 1 cloud cloud 63346888 Sep  4  2023 dockerd
-rwxr-xr-x. 1 cloud cloud   761712 Sep  4  2023 docker-init
-rwxr-xr-x. 1 cloud cloud  1965694 Sep  4  2023 docker-proxy
-rwxr-xr-x. 1 cloud cloud 15142440 Sep  4  2023 runc

```

#### 配置docker服务

> vi /etc/systemd/system/docker.service

```bash
[Unit]
Description=Docker Application Container Engine
Documentation=https://docs.docker.com
After=network-online.target firewalld.service
Wants=network-online.target

[Service]
Type=notify
ExecStart=/usr/local/bin/dockerd
ExecReload=/bin/kill -s HUP $MAINPID
LimitNOFILE=infinity
LimitNPROC=infinity
TimeoutStartSec=0
Delegate=yes
KillMode=process
Restart=on-failure
StartLimitBurst=3
StartLimitInterval=60s

[Install]
WantedBy=multi-user.target

```

**授权**

```bash
chmod +x /etc/systemd/system/docker.service
systemctl daemon-reload

```

**启动**

```bash
# 开机自启动
systemctl enable docker.service
# 启动docker
systemctl start docker
# docker状态
systemctl status docker

```

### 2\. 离线-安装Docker-Compose

[离线包下载地址](https://github.com/docker/compose/releases)

> https://github.com/docker/compose/releases/download/v2.27.0/docker-compose-linux-x86\_64

```bash
cp deploy/docker-lib/docker-compose-linux-x86_64 /usr/local/bin/docker-compose && chmod 777 /usr/local/bin/docker-compose

```

### 3\. 加载Milvus镜像

```bash
# 导入镜像
docker load < deploy/docker-lib/kkdd_milvus-images.docker


# 查看导入后的镜像
[root@localhost (11:11:09) ~/images]
└─# docker images
REPOSITORY                                           TAG                            IMAGE ID       CREATED         SIZE
milvusdb/milvus                                      v2.4.0                         a9fb7550de57   3 weeks ago     1.71GB
zilliz/attu                                          v2.3.1                         9097b24f157c   8 months ago    1.18GB
minio/minio                                          RELEASE.2023-03-20T20-16-18Z   400c20c8aac0   13 months ago   252MB
quay.io/coreos/etcd                                  v3.5.5                         673f29d03de9   20 months ago   182MB

```

### 4.启动milvus

```bash
# 切换目录
cd deploy/docker-lib

# 启动数据库
docker-compose up -d

# 查看程序运行状态
[root@localhost (11:15:45) /data/xuejia.li/milvus]
└─# docker-compose ps
      Name                     Command                       State                                                   Ports
-------------------------------------------------------------------------------------------------------------------------------------------------------------------
attu                docker-entrypoint.sh /bin/ ...   Up                      0.0.0.0:8002->3000/tcp,:::8002->3000/tcp
milvus-etcd         etcd -advertise-client-url ...   Up (health: starting)   2379/tcp, 2380/tcp
milvus-minio        /usr/bin/docker-entrypoint ...   Up (health: starting)   0.0.0.0:9000->9000/tcp,:::9000->9000/tcp, 0.0.0.0:9001->9001/tcp,:::9001->9001/tcp
milvus-standalone   /tini -- milvus run standalone   Up (health: starting)   0.0.0.0:19530->19530/tcp,:::19530->19530/tcp, 0.0.0.0:9091->9091/tcp,:::9091->9091/tcp
[root@localhost (11:16:51) /data/xuejia.li/milvus]

```

#### 查看Web页面(`attu`)

http://当前主机地址:8002
