---
title: "docker-compose 部署ceph集群"
date: "2019-12-24"
categories: 
  - "linux服务器"
---

##### **`关闭防火墙`**

###### [官网资料](https://hub.docker.com/r/ceph/daemon "官网资料")

* * *

###### 前置条件

| hostname | ip |
| --- | --- |
| test1 | 172.168.180.46 |
| test2 | 172.168.180.47 |
| test3 | 172.168.180.48 |

* * *

###### [升级内核](http://www.dev-share.top/2019/07/10/linux-%e7%b3%bb%e7%bb%9f%e5%86%85%e6%a0%b8%e5%8d%87%e7%ba%a7/ "升级内核")

* * *

ceph 有三种存储方式：

1. CephFS
    
    - 挂载分区
    - 挂载目录
2. RBD
3. 对象存储

* * *

###### [安装 Docker-Compose](http://www.dev-share.top/2019/06/12/%e5%ae%89%e8%a3%85-docker-compose/ "安装 Docker-Compose")

* * *

**创建文件夹为`部署ceph`做准备**

```ruby
[root@test1 ~]# mkdir -p /home/compose /etc/ceph/ /var/lib/ceph/
[root@test1 ~]# ssh test2 mkdir -p /home/compose /etc/ceph/ /var/lib/ceph/
[root@test1 ~]# ssh test3 mkdir -p /home/compose /etc/ceph/ /var/lib/ceph/
```

* * *

**如果启用了SELinux，则运行以下命令, 给文件夹授权, 否则这一步可以`跳过`**

```ruby
[root@test1 ~]# chcon -Rt svirt_sandbox_file_t /etc/ceph && chcon -Rt svirt_sandbox_file_t /var/lib/ceph
[root@test1 ~]# ssh test2 chcon -Rt svirt_sandbox_file_t /etc/ceph && ssh test2 chcon -Rt svirt_sandbox_file_t /var/lib/ceph
[root@test1 ~]# ssh test3 chcon -Rt svirt_sandbox_file_t /etc/ceph && ssh test3 chcon -Rt svirt_sandbox_file_t /var/lib/ceph
```

* * *

**创建文件夹为`osd挂载`做准备, 挂载文件夹与分区无关，只要是目录就行, 如果不使用`挂载分区`, 这一步可以`跳过`**

```ruby
[root@test1 ~]# mkdir -p /mnt/cephfs
[root@test1 ~]# ssh test2 mkdir -p /mnt/cephfs
[root@test1 ~]# ssh test3 mkdir -p /mnt/cephfs
```

* * *

**下载docker镜像，并推送到自己的 harbor 私服仓库中, 如果已经实现，这一步可以`跳过`**

```ruby
# 下载镜像
docker pull ceph/daemon:latest-luminous
# 改镜像名
docker tag ceph/daemon:latest-luminous sinoeyes.io/cephlib/ceph/daemon:latest-luminous
# 登录 harbor
docker login sinoeyes.io -u admin -p Harbor12345
# 推送到 harbor
docker push sinoeyes.io/cephlib/ceph/daemon:latest-luminous
```

* * *

**如果是重新安装，需要清空缓存, 否则这一步可以`跳过`**

```ruby
[root@test1 ~]# rm -rf /etc/ceph/* && rm -rf /var/lib/ceph/*
[root@test1 ~]# ssh test2 rm -rf /etc/ceph/ && ssh test2 rm -rf /var/lib/ceph/*
[root@test1 ~]# ssh test3 rm -rf /etc/ceph/ && ssh test3 rm -rf /var/lib/ceph/*
```

* * *

* * *

* * *

###### 1 创建compose文件，并在(test2、test3)节点上同样创建

**注意事项**：

1. `MON_IP`不要写多个ip，只写所在服务器的IP即可；如果写多个重启docker以后 mon会启动失败
2. 这个`/etc/ceph/ceph.conf`文件中的内容所有节点都要要保持一致，不要单独修改内容

```ruby
cat > /home/compose/docker-compose.yml << eric
version: '3'

services:

  # 部署 Monitor 模块
  ceph-mon:
    # 镜像已经下载到harbor私服
    image: sinoeyes.io/cephlib/ceph/daemon:latest-luminous
    network_mode: host
    container_name: ceph-mon
    restart: always
    volumes:
      - /etc/localtime:/etc/localtime
      - /etc/ceph:/etc/ceph
      - /var/lib/ceph/:/var/lib/ceph
    environment:
      # 当前服务器的IP, 在不同的服务器部署不要忘记改IP
      MON_IP: 172.168.180.46
      CEPH_PUBLIC_NETWORK: 172.168.180.1/24
    command: mon


  # 部署 Manager daemon 模块
  ceph-mgr:
    image: sinoeyes.io/cephlib/ceph/daemon:latest-luminous
    network_mode: host
    container_name: ceph-mgr
    restart: always
    depends_on:
        - ceph-mon
    volumes:
      - /etc/localtime:/etc/localtime
      - /etc/ceph:/etc/ceph
      - /var/lib/ceph/:/var/lib/ceph
    command: mgr


  # 部署 OSD 模块
  ceph-osd:
    image: sinoeyes.io/cephlib/ceph/daemon:latest-luminous
    network_mode: host
    container_name: ceph-osd
    restart: always
    privileged: true
    # 跟主机系统共享进程命名空间。打开该选项的容器可以相互通过进程 ID 来访问和操作。
    pid: host
    depends_on:
        - ceph-mgr
    volumes:
      - /etc/localtime:/etc/localtime
      - /etc/ceph:/etc/ceph
      - /var/lib/ceph/:/var/lib/ceph
      - /dev/:/dev/
      # 单独指定osd数据空间, 如果不单独指定，默认在/var/lib/ceph目录下
      #-/mnt/cephfs://var/lib/ceph/osd
    command: osd_directory


  # 部署 MDS 模块 (用来支持 CephFS文件系统存储, 根据实际情况选用，非必须)
  ceph-mds:
    image: sinoeyes.io/cephlib/ceph/daemon:latest-luminous
    network_mode: host
    container_name: ceph-mds
    restart: always
    depends_on:
        - ceph-osd
    volumes:
      - /etc/localtime:/etc/localtime
      - /etc/ceph:/etc/ceph
      - /var/lib/ceph/:/var/lib/ceph
    environment:
      # 0表示不自动创建文件系统（推荐），1表示自动创建
      CEPHFS_CREATE: 1
    command: mds


#  # 部署 Rados Gateway 模块 (用来支持 对象存储, 根据实际情况选用，非必须)
#  ceph-rgw:
#    image: sinoeyes.io/cephlib/ceph/daemon:latest-luminous
#    network_mode: host
#    container_name: ceph-rgw
#    restart: always
#    depends_on:
#        - ceph-osd
#    volumes:
#      - /etc/localtime:/etc/localtime
#      - /etc/ceph:/etc/ceph
#      - /var/lib/ceph/:/var/lib/ceph
#    command: rgw


#  # 部署 RBD mirror 模块 (用来支持 块存储, 根据实际情况选用，非必须)
#  ceph-rbd:
#    image: sinoeyes.io/cephlib/ceph/daemon:latest-luminous
#    network_mode: host
#    container_name: ceph-rbd
#    restart: always
#    volumes:
#      - /etc/localtime:/etc/localtime
#      - /etc/ceph:/etc/ceph
#      - /var/lib/ceph/:/var/lib/ceph
#    depends_on:
#        - ceph-osd
#    command: rbd_mirror


eric

```

   如果IP跨网段，那么`CEPH_PUBLIC_NETWORK`必须写上所有网段，否则就会像网上大部分已有教程一样，只指定一个IP和一个网段是无法启动的！

* * *

###### 2 先启动 test1

```ruby
[root@test1 compose]# docker-compose up -d
```

* * *

###### 3 将多个节点组建成集群

   如果要增加同一个集群的Monitor，需要将`test1`服务器上的`/etc/ceph/`和`/var/lib/ceph/bootstrap-*`下的文件，分别复制到`test2`、`test3`服务器的`/etc/ceph/`和`/var/lib/ceph/`目录下，记得不要保留文件的属主权限。

```ruby
[root@test1 compose]# scp -r /etc/ceph/ test2:/etc/ceph/ && scp -r /var/lib/ceph/bootstrap-* test2:/var/lib/ceph/
......
[root@test1 compose]# scp -r /etc/ceph/ test3:/etc/ceph/ && scp -r /var/lib/ceph/bootstrap-* test3:/var/lib/ceph/
ceph.client.admin.keyring                                100%  161   116.0KB/s   00:00
ceph.conf                                                100%  235   204.5KB/s   00:00
ceph.mon.keyring                                         100%  690   385.9KB/s   00:00
ceph.keyring                                             100%  113    84.3KB/s   00:00
ceph.keyring                                             100%  113    50.4KB/s   00:00
ceph.keyring                                             100%  113    35.3KB/s   00:00
ceph.keyring                                             100%  113    29.0KB/s   00:00
[root@test1 compose]#
```

* * *

###### 4 启动其它节点机

```ruby
[root@test1 compose]# ssh test2 docker-compose -f /home/compose/docker-compose.yml up -d
[root@test1 compose]# ssh test3 docker-compose -f /home/compose/docker-compose.yml up -d
```

###### 5 查看各组件启动是否成功

```ruby
# 查看 osd 是否加入集群
[root@test1 compose]# docker-compose exec ceph-osd ceph osd tree
ID CLASS WEIGHT  TYPE NAME      STATUS REWEIGHT PRI-AFF
-1       0.16676 root default
-3       0.05559     host test1
 0   hdd 0.05559         osd.0      up  1.00000 1.00000
-5       0.05559     host test2
 1   hdd 0.05559         osd.1      up  1.00000 1.00000
-7       0.05559     host test3
 2   hdd 0.05559         osd.2      up  1.00000 1.00000
[root@test1 compose]#
```

其它查看命令

```ruby
[root@test1 compose]# docker-compose exec ceph-mon ceph -s
[root@test1 compose]# docker-compose exec ceph-mgr ceph -s
[root@test1 compose]# docker-compose exec ceph-mds ceph -s
[root@test1 compose]# docker-compose exec ceph-rgw ceph -s
[root@test1 compose]# docker-compose exec ceph-rbd ceph -s
```

* * *

###### 6 启动 dashboard

```ruby
[root@test1 compose]# docker-compose exec ceph-mon ceph mgr dump
[root@test1 compose]# docker-compose exec ceph-mgr ceph mgr module enable dashboard
```

**访问dashboard**: http://172.168.180.46:7000

* * *

* * *

* * *

###### [使用 K8S 挂载](http://www.dev-share.top/2019/12/27/k8s-pv-pvc-ceph-%E5%85%B1%E4%BA%AB%E5%8D%B7/ "使用 K8S 挂载")

###### **`注意`：如果想使用 k8s pv 进行挂载，如下的操作就不需要在做了，k8s pv 配置好以后，pod 启动时会自动挂载**

* * *

* * *

* * *

###### 测试 内核方式挂载cephfs

**明文挂载**

```ruby
# 获取密钥
[root@test1 compose]# docker-compose exec ceph-mon ceph-authtool --print-key /etc/ceph/ceph.client.admin.keyring
AQAzdARew/d7JRAAbwbgRh9p0z8sXCDVsg61eQ==
[root@test1 ~]#

# 挂载之前
[root@test1 ~]# df -h | grep mnt
[root@test1 ~]#

# 挂载目录
[root@test1 ~]# mount -t ceph 172.168.180.46:6789,172.168.180.47:6789,172.168.180.48:6789:/ /mnt/cephfs -o name=admin,secret=AQAzdARew/d7JRAAbwbgRh9p0z8sXCDVsg61eQ==
[root@test1 ~]# 

# 挂载之后
[root@test1 compose]# df -h | grep mnt
172.168.180.46:6789,172.168.180.47:6789,172.168.180.48:6789:/   46G     0   46G    0% /mnt/cephfs
[root@test1 compose]#


# 卸载目录
[root@test1 ~]# umount /mnt/cephfs
```

###### 其它节点挂载情况

这里要**`注意`** 挂载盘的ip地址都是**`172.168.180.46:6789`**，不是每个节点的IP

```ruby
[root@test2 ~]# mount -t ceph 172.168.180.46:6789,172.168.180.47:6789,172.168.180.48:6789:/ /mnt/cephfs -o name=admin,secret=AQAzdARew/d7JRAAbwbgRh9p0z8sXCDVsg61eQ==
[root@test2 ~]# df -h | grep mnt
172.168.180.46:6789,172.168.180.47:6789,172.168.180.48:6789:/   46G     0   46G    0% /mnt/cephfs
[root@test2 ~]#

[root@test3 ~]# mount -t ceph 172.168.180.46:6789,172.168.180.47:6789,172.168.180.48:6789:/ /mnt/cephfs -o name=admin,secret=AQAzdARew/d7JRAAbwbgRh9p0z8sXCDVsg61eQ==
[root@test3 ~]# df -h | grep mnt
172.168.180.46:6789,172.168.180.47:6789,172.168.180.48:6789:/   46G     0   46G    0% /mnt/cephfs
[root@test3 ~]#
```

* * *
