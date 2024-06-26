---
title: "docker-compose 部署 Helm 私服仓库"
date: "2020-07-21"
categories: 
  - "helm"
  - "k8s"
---

###### 前置条件

- **私有仓库IP: 192.168.2.10**

* * *

###### docker-compose.yml

```ruby
mkdir -p /home/deploy/chartmuseum/charts && cd /home/deploy/chartmuseum/

cat > /home/deploy/chartmuseum/docker-compose.yml << ERIC

version: '3.1'

services:

  chartmuseum:
    image: chartmuseum/chartmuseum:v0.12.0
    container_name: chartmuseum
    restart: always
    ports:
      - 8008:8080
    volumes:
      # 容器与宿主机时间同步
      - /etc/localtime:/etc/localtime
      - ./charts:/charts
    environment:
      STORAGE: local
      STORAGE_LOCAL_ROOTDIR: ./charts

ERIC

```

* * *

###### Web管理界面

```ruby
docker-compose up -d

curl http://192.168.2.10:8008
```

* * *

###### 将自己的应用 上传到私有仓库

```ruby
# 创建chart模板
[root@harbor chartmuseum]# helm create eric
Creating eric
[root@harbor chartmuseum]# ls
eric
[root@harbor chartmuseum]#


# 配置模版文件，例如 修改镜像
[root@harbor chartmuseum]# vim eric/values.yaml


# 将改好后的 文件夹打包
[root@harbor chartmuseum]# helm package eric
Successfully packaged chart and saved it to: /home/deploy/chartmuseum/eric-0.1.0.tgz
[root@harbor chartmuseum]#
[root@harbor chartmuseum]# ll
drwxr-xr-x 4 root root 4096 7月  21 14:27 eric
-rw-r--r-- 1 root root 3320 7月  21 14:28 eric-0.1.0.tgz
[root@harbor chartmuseum]#


# 将包直接放到 charts/ 就已经成功发布了
[root@harbor chartmuseum]# mv eric-0.1.0.tgz charts/

```

* * *

###### 使用私有仓库

```ruby
# 加入仓库链接
[root@harbor chartmuseum]# helm repo add dhc http://192.168.2.10:8008


# 查看仓库列表
[root@harbor chartmuseum]# helm repo list
NAME    URL
dhc     http://192.168.2.10:8008
[root@harbor chartmuseum]#


# 更新仓库
[root@master home]# helm repo update
Hang tight while we grab the latest from your chart repositories...
...Successfully got an update from the "dhc" chart repository
Update Complete. ⎈ Happy Helming!⎈
[root@master home]#


# 查看刚刚发布的包
[root@master home]# helm search repo eric
NAME                                    CHART VERSION   APP VERSION     DESCRIPTION
dhc/eric                                0.1.0           1.16.0          A Helm chart for Kubernetes
[root@master home]#


# 删除仓库链接
[root@harbor chartmuseum]# helm repo remove dhc

```
