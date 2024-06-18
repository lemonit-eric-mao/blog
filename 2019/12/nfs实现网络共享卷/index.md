---
title: "NFS实现网络共享卷"
date: "2019-12-18"
categories: 
  - "docker"
---

##### 当前案例

**期望结果**：让不同的节点机，共用同一个配置文件

##### 环境

| HostName | IP | DES |
| --- | --- | --- |
| test1 | 172.160.180.46 | 共享卷 |
| test2 | 172.160.180.47 | node-1 |
| test3 | 172.160.180.48 | node-2 |

* * *

* * *

* * *

###### 什么是 NFS

**网络文件系统**，英文 **Network File System**(`NFS`)，是由SUN公司研制的UNIX表示层协议(pressentation layer protocol)，能使使用者访问网络上别处的文件就像在使用自己的计算机一样。

* * *

###### 1 安装 nfs

使用 nfs 配置共享卷 test1（172.160.180.46）

```ruby
[root@test1 ~]# yum -y install rpcbind nfs-utils
```

* * *

###### 2 创建卷要映射的目录

```ruby
[root@test1 ~]# mkdir -p /home/share-volume && chmod -R 777 /home/share-volume
```

* * *

###### 3 将目录添加到 nfs服务器配置文件中

```ruby
[root@test1 ~]# cat > /etc/exports << ERIC
/home/share-volume *(rw,sync,all_squash,anonuid=0,anongid=0)
ERIC

[root@test1 ~]#
```

* * *

###### 4 重启 nfs rpcbind 服务

```ruby
systemctl restart nfs rpcbind && systemctl status nfs rpcbind
```

* * *

###### 5 查看共享卷目录

```ruby
# 重新挂载/etc/exports 的设置
[root@test1 ~]# exportfs -arv
exporting *:/home/share-volume


# 显示主机的/etc/exports 所共享的目录数据
[root@test1 ~]# showmount -e
Export list for test1:
/home/share-volume *

```

* * *

* * *

* * *

##### `测试`

* * *

* * *

###### 进入172.160.180.47在虚拟机上测试

```ruby
## 需要安装 nfs-utils
yum -y install nfs-utils


## 创建本地文件夹
mkdir -p /root/test-nfs


## 挂载远程NFS
mount 172.160.180.46:/data/nfs_data /root/test-nfs


## 查看
df -h | grep nfs

Filesystem                     Size    Used  Avail  Use%  Mounted on
172.160.180.46:/data/nfs_data  1008G   72G   885G   8%    /root/test-nfs


## 卸载
umount /root/test-nfs

```

* * *

* * *

###### 进入172.160.180.48使用Docker测试，创建docker卷，并映射到 nfs 服务器

```ruby
[root@test1 ~]# docker volume create --driver local \
     --opt type=nfs \
     --opt o=addr=172.160.180.46,rw \
     --opt device=:/home/share-volume \
     eric-share-volume

# 查看docker卷
[root@test1 ~]# docker volume ls | grep eric-share-volume
local               eric-share-volume
[root@test1 ~]#
```

**解释：**

```
docker volume create --driver local \
     --opt type=nfs \                      # 卷类型, 指定使用nfs服务器做为挂载卷
     --opt o=addr=172.160.180.46,rw \      # 指定 nfs服务器地址
     --opt device=:/home/share-volume \    # 指定 nfs服务器卷目录
     eric-share-volume                     # docker 卷名称
```

* * *

* * *

* * *
