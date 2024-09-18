---
title: "docker-compose 安装 goharbor"
date: "2019-06-06"
categories: 
  - "docker"
---

##### 作用

1. 远程镜像只拉取一次即可，减少下载镜像的网络延迟
2. 存储项目中由开发人员构建的程序镜像
3. 为集群提供镜像共享

* * *

##### Hardware 硬件要求

| 硬件 | 最低配置 | 推荐配置 |
| --- | --- | --- |
| 处理器 | 2 CPU | 4 CPU |
| 内存 | 4GB | 8GB |
| 硬盘 | 40GB | 160GB |

* * *

##### Software 软件要求

| 软件 | 版本 | 说明 |
| --- | --- | --- |
| Docker | 17.03.0-ce 或更高 |  |
| Docker Compose | 1.18.0 或更高 |  |
| Openssl | 首选最新版本 | 为Harbor生成证书和密钥 |

* * *

[goharbor 官方下载地址](https://github.com/goharbor/harbor/releases "goharbor 官方下载地址")

##### 前置条件

[安装 Docker](%e5%ae%89%e8%a3%85-docker "安装 Docker")

[安装 Docker-Compose](%e5%ae%89%e8%a3%85-docker-compose "安装 Docker-Compose")

* * *

##### 安装步骤

1. 下载安装程序;
2. 配置harbor.yml;
3. 运行install.sh安装并启动Harbor;

* * *

##### 下载安装程序

为了简单，我选择了离线安装，在线安装太慢了

```bash
[root@localhost (12:15:13) /data/deploy/harbor]
└─# wget http://qiniu.dev-share.top/harbor-offline-installer-v2.9.1.tgz


[root@localhost (12:15:28) /data/deploy]
└─# tar -zxvf harbor-offline-installer-v2.9.1.tgz
harbor/harbor.v2.9.1.tar.gz
harbor/prepare
harbor/LICENSE
harbor/install.sh
harbor/common.sh
harbor/harbor.yml.tmpl


[root@localhost (12:15:40) /data/deploy]
└─# cd harbor/

```

* * *

##### 配置 harbor.yml

为了简单安装部署，这里只修改必填项 **`注意`： 每次修改这个文件都要重新执行 ./install.sh**

```bash
[root@localhost (12:17:31) /data/deploy/harbor]
└─# cp harbor.yml.tmpl harbor.yml


# 注意：修改配置文件时，如果不使用 https 协议，需要把它注释掉
[root@localhost (12:17:41) /data/deploy/harbor]
└─# vim harbor.yml

# 修改域名 或 IP地址
hostname: k8s.dev-share.top

# 访问接口
http:
  port: 80

# 用户名 admin
# 用户密码
harbor_admin_password: Harbor12345

# 数据库密码
database:
  password: root123

# 数据存储目录
data_volume: /data/deploy/harbor/data

```

* * *

##### 安装

```bash
# 安装带 Helm chart库 (--with-chartmuseum)，带镜像扫描(--with-trivy) 创建的 Harbor
[root@localhost (12:16:59) /data/deploy/harbor]
└─# sh install.sh --with-chartmuseum --with-trivy


[root@localhost (12:21:02) /data/deploy/harbor]
└─# sh install.sh --help
如果需要在Harbor中启用Trivy，请设置--with-trivy。
请勿设置--with-chartmuseum，因为chartmuseum已被弃用并移除。
请勿设置--with-notary，因为notary已被弃用并移除。




# 或者 安装默认的 Harbor
[root@localhost (12:21:38) /data/deploy/harbor]
└─# sh install.sh --with-trivy

[Step 0]: checking if docker is installed ...

Note: docker version: 20.10.0

[Step 1]: checking docker-compose is installed ...

Note: docker-compose version: 1.26.2

```

* * *

##### 测试连接

http://k8s.dev-share.top 用户名：admin 用户密码：Harbor12345

* * *

##### 在远程终端测试连接

`执行 docker push 的时候必需要登录到私有仓库`

```bash
# 不登录不能 push
[root@k8s-master ~]# docker login k8s.dev-share.top -u admin -p Harbor12345
Login Succeeded
[root@k8s-master ~]#
```

* * *

##### 启动/停止

```bash
# 启动
[root@localhost (12:21:38) /data/deploy/harbor]
└─# docker-compose start

# 停止
[root@localhost (12:21:38) /data/deploy/harbor]
└─# docker-compose stop

# 重新创建并启动Harbor的实例
[root@localhost (12:21:38) /data/deploy/harbor]
└─# docker-compose up -d

# 删除Harbor的容器，同时将图像数据和Harbor的数据库文件保存在文件系统上
[root@localhost (12:21:38) /data/deploy/harbor]
└─# docker-compose down -v

```

* * *

##### 配置私有仓库代理地址

`执行 docker pull 的时候需要指定 仓库地址`

```bash
[root@localhost (12:21:38) /data/deploy/harbor]
└─# cat > /etc/docker/daemon.json << EOF
{
    # http连接，非加密连接，数据传输不安全，使用相对简单
    # 私服地址
    "insecure-registries": ["http://k8s.dev-share.top"],
    # 远程镜像代理地址，与Harbor无关
    "registry-mirrors": [
        "https://registry.cn-hangzhou.aliyuncs.com"
    ]
}
EOF



systemctl daemon-reload && systemctl restart docker

```

* * *

##### 远程镜像推送到私有仓库

**分为两步** 1. 在项目中标记镜像： `docker tag SOURCE_IMAGE[:TAG] k8s.dev-share.top/library/IMAGE[:TAG]` docker tag 本地镜像名:Tag 私服仓库地址/远程镜像名:Tag 2. 推送镜像到Harbor私有仓库: `docker push k8s.dev-share.top/library/IMAGE[:TAG]` docker push 私服仓库地址/远程镜像名:Tag

**接下来在如下示例当中实现，将本地的 node.js镜像 推送到远程的 私服仓库**

```bash
[root@k8s-master ~]# docker images | grep node
node
[root@k8s-master ~]#
[root@k8s-master ~]# docker push k8s.dev-share.top/library/node:slim
The push refers to repository [k8s.dev-share.top/library/node]
daade46d532d: Pushed
46b67135288b: Pushed
715cf255d73f: Pushed
aa5a12ea4279: Pushed
6270adb5794c: Pushed
slim: digest: sha256:1b5871385c87ed5cc64e6a6f2a4b789a03266d29b4a0c72c4a740ed67f29286e size: 1367
[root@k8s-master ~]#
```

* * *

* * *

* * *

###### **[常见问题](docker-%e5%b8%b8%e8%a7%81%e9%97%ae%e9%a2%98 "常见问题")**

* * *

* * *

* * *

##### 扩展 配置harbor 非 80 端口访问

###### harbor 机器配置

```bash
[root@master harbor]# vim harbor.yml
# 伪域名
hostname: harbor.software.com
# http related config
http:
  # port for http, default is 80. If https enabled, this port will redirect to https port
  port: 8081

[root@master harbor]#


# 注意这里 要使用 ./install.sh 重新安装， 千万不要直接修改 docker-compose.yaml， 这样是不行的，会导致 docker login 失败
[root@master harbor]# ./install.sh

# 查看 hosts 配置
[root@master harbor]#
[root@master harbor]# cat /etc/hosts
127.0.0.1   cloudserver
::1         localhost localhost.localdomain localhost6 localhost6.localdomain6

192.168.2.10 harbor.software.com

[root@master harbor]#
[root@master harbor]#
[root@master harbor]#
[root@master harbor]# cat /etc/docker/daemon.json
{
    "registry-mirrors": [
        "https://registry.cn-hangzhou.aliyuncs.com"
    ]
}
[root@master harbor]#
```

###### 所有使用 harbor的机器 相关配置

```bash
[root@node2 ~]# cat /etc/hosts
127.0.0.1   cloudserver
::1         localhost localhost.localdomain localhost6 localhost6.localdomain6

# harbor 内网 虚拟机 IP
192.168.2.10 harbor.software.com
[root@node2 ~]#
[root@node2 ~]#
[root@node2 ~]# cat /etc/docker/daemon.json
{
    "insecure-registries": ["http://harbor.software.com:8081"],
    "registry-mirrors": [
        "https://registry.cn-hangzhou.aliyuncs.com"
    ]
}

[root@node2 ~]#
[root@node2 ~]# docker login http://harbor.software.com:8081 -u admin -p Harbor12345
WARNING! Using --password via the CLI is insecure. Use --password-stdin.
WARNING! Your password will be stored unencrypted in /root/.docker/config.json.
Configure a credential helper to remove this warning. See
https://docs.docker.com/engine/reference/commandline/login/#credentials-store

Login Succeeded
[root@node2 ~]#

```
