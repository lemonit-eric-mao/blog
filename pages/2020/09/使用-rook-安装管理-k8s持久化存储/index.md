---
title: "使用 rook 安装管理 k8s持久化存储"
date: "2020-09-24"
categories: 
  - "rook"
---

###### **什么是 Rook**

> - Rook将分布式存储系统转变为自我管理，自我扩展，自我修复的存储服务。它可以自动执行存储管理员的任务：部署，引导，配置，供应，扩展，升级，迁移，灾难恢复，监视和资源管理。
>     
> - 经过实际测试**kubernetes 1.24.x**使用`rook-ceph-1.12.6`运行时无异常情况
>     

* * *

###### **Rook 可管理以下分布式文件存储系统，在K8S中运行**

- Ceph
- EdgeFS
- CockroachDB
- Cassandra
- NFS
- Yugabyte DB

* * *

* * *

* * *

###### 所需镜像 放到每个worker主机上

```bash
## 从其它机器上，导出离线镜像
ctr -n k8s.io image export rook-ceph-1.12.6.tar \
  rook/ceph:v1.12.6
  quay.io/cephcsi/cephcsi:v3.9.0
  quay.io/ceph/ceph:v17.2.6
  registry.k8s.io/sig-storage/csi-node-driver-registrar:v2.8.0
  registry.k8s.io/sig-storage/csi-attacher:v4.3.0
  registry.k8s.io/sig-storage/csi-provisioner:v3.5.0
  registry.k8s.io/sig-storage/csi-resizer:v1.8.0
  registry.k8s.io/sig-storage/csi-snapshotter:v6.2.2


## 导入镜像
ctr -n k8s.io image import rook-ceph-1.12.6.tar

```

* * *

###### 查看 **[官方文档](https://rook.github.io/docs/rook/v1.12/Getting-Started/quickstart/#tldr "官方文档")** 如何安装

###### **[官方github下载](https://github.com/rook/rook/tags "官方github下载")**

```bash
git clone --single-branch --branch v1.12.6 https://github.com/rook/rook.git ./rook_1.12.6

cd rook_1.12.6/deploy/examples

```

* * *

###### 在k8s中安装 ceph

```bash
kubectl create -f crds.yaml -f common.yaml -f operator.yaml && kubectl create -f cluster.yaml

```

* * *

* * *

* * *

###### 查看集群

```bash
[root@master01 examples]# kubectl -n rook-ceph get pod
NAME                                               READY   STATUS      RESTARTS        AGE
csi-cephfsplugin-provisioner-845b666675-842cf      5/5     Running     5 (6m26s ago)   18m
csi-cephfsplugin-provisioner-845b666675-bnp5c      5/5     Running     5 (6m26s ago)   18m
csi-cephfsplugin-sgksm                             2/2     Running     2 (6m26s ago)   18m
csi-cephfsplugin-v5pst                             2/2     Running     2 (6m26s ago)   18m
csi-cephfsplugin-x22v4                             2/2     Running     2 (6m25s ago)   18m
csi-rbdplugin-9ph86                                2/2     Running     2 (6m26s ago)   18m
csi-rbdplugin-dsvc4                                2/2     Running     2 (6m25s ago)   18m
csi-rbdplugin-lvrkc                                2/2     Running     2 (6m26s ago)   18m
csi-rbdplugin-provisioner-859fcdc5b9-9crf8         5/5     Running     5 (6m26s ago)   18m
csi-rbdplugin-provisioner-859fcdc5b9-kkbx5         5/5     Running     5 (6m25s ago)   18m
rook-ceph-crashcollector-work01-bc7f6b9fb-846jp    1/1     Running     1 (6m26s ago)   17m
rook-ceph-crashcollector-work02-797f68b85f-bj5v2   1/1     Running     1 (6m25s ago)   17m
rook-ceph-crashcollector-work03-557dd655d6-bpn5d   1/1     Running     1 (6m26s ago)   17m
rook-ceph-mgr-a-64764dc6-sgs5z                     3/3     Running     3 (6m25s ago)   17m
rook-ceph-mgr-b-79dcc88967-j2fm2                   3/3     Running     4 (3m49s ago)   17m
rook-ceph-mon-a-5d986bdcfb-dhbft                   2/2     Running     2 (6m25s ago)   18m
rook-ceph-mon-b-69cf8dc66b-v8h7r                   2/2     Running     2 (6m26s ago)   18m
rook-ceph-mon-c-9dfcfb77c-hw6bt                    2/2     Running     2 (6m26s ago)   18m
rook-ceph-operator-88997c68b-4ldfx                 1/1     Running     2 (3m50s ago)   19m
rook-ceph-osd-0-7b8d495cc8-ptszl                   2/2     Running     2 (6m26s ago)   17m
rook-ceph-osd-1-7b79778596-pr84k                   2/2     Running     2 (6m25s ago)   17m
rook-ceph-osd-2-7f4dfd8dc6-jcfxr                   2/2     Running     2 (6m26s ago)   17m
rook-ceph-osd-prepare-work01-qdxwr                 0/1     Completed   0               2m30s
rook-ceph-osd-prepare-work02-n24rg                 0/1     Completed   0               2m27s
rook-ceph-osd-prepare-work03-d9lbb                 0/1     Completed   0               2m24s
[root@master01 examples]#
```

* * *

* * *

* * *

###### 加入dashbord web页面

```bash
[root@master01 examples]# kubectl apply -f dashboard-external-https.yaml
service/rook-ceph-mgr-dashboard-external-https created
[root@master01 examples]#

# 查看
[root@master01 examples]# kubectl -n rook-ceph get svc
NAME                                     TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)             AGE
csi-cephfsplugin-metrics                 ClusterIP   10.96.21.181    <none>        8080/TCP,8081/TCP   17h
csi-rbdplugin-metrics                    ClusterIP   10.96.243.191   <none>        8080/TCP,8081/TCP   17h
rook-ceph-mgr                            ClusterIP   10.96.83.88     <none>        9283/TCP            17h
rook-ceph-mgr-dashboard                  ClusterIP   10.96.20.202    <none>        8443/TCP            17h
rook-ceph-mgr-dashboard-external-https   NodePort    10.96.208.41    <none>        8443:31904/TCP      65s
rook-ceph-mon-a                          ClusterIP   10.96.220.178   <none>        6789/TCP,3300/TCP   17h
rook-ceph-mon-b                          ClusterIP   10.96.108.170   <none>        6789/TCP,3300/TCP   17h
rook-ceph-mon-c                          ClusterIP   10.96.33.120    <none>        6789/TCP,3300/TCP   17h
[root@master01 examples]#
```

**这里使用的是 `dashboard-external-https.yaml`文件， 因为 http 协议的 dashboard 的端口是7000， 而https的端口是 8443， Service `rook-ceph-mgr-dashboard-external-https` 只是对 `rook-ceph-mgr-dashboard`的展示页面**

* * *

###### 获取 ceph dashboard 密码

默认用户名为 admin `kubectl -n rook-ceph get secret rook-ceph-dashboard-password -o jsonpath='{.data.password}' | base64 --decode`

```bash
[root@master01 examples]# kubectl -n rook-ceph get secret rook-ceph-dashboard-password -o jsonpath='{.data.password}'  |  base64 --decode
p<JL|_edJQDqlFa-~5*S
[root@master01 examples]#
```

* * *

* * *

* * *

###### 创建 StorageClass

```bash
[root@master01 examples]# cd csi/rbd/

[root@master01 rbd]# kubectl apply -f storageclass.yaml

[root@master01 rbd]# kubectl get cephblockpool -A
NAMESPACE   NAME          AGE
rook-ceph   replicapool   5m30s
[root@master01 rbd]#

[root@master01 rbd]# kubectl -n rook-ceph get sc
NAME              PROVISIONER                  RECLAIMPOLICY   VOLUMEBINDINGMODE   ALLOWVOLUMEEXPANSION   AGE
rook-ceph-block   rook-ceph.rbd.csi.ceph.com   Delete          Immediate           true                   10s

[root@master01 rbd]#
```

**`注意：` 要想删除StorageClass 需要先删除所有绑定StorageClass的`PVC`，之后才能删除StorageClass**

* * *

###### 解释 `PVC` 如何使用 StorageClass

**`PVC`** 的作用是告诉K8S，它要在 **`分布式文件系统`** 中划取多大空间，然后这块儿空间留给应用程序使用; 当 **`PVC`** 绑定 **`StorageClass`** 以后，**StorageClass** 会自动创建相应的 **`PV`**

```bash
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: webapp-pvc
spec:
  accessModes:
  - ReadWriteOnce
  resources:
    requests:
      storage: 60Gi

  # 告诉PVC 要绑定到哪个StorageClass
  storageClassName: rook-ceph-block
```

* * *

* * *

* * *

###### **[删除 ceph](https://rook.github.io/docs/rook/v1.12/Getting-Started/ceph-teardown/ "删除 ceph")**

```bash
cd rook_1.12.6/deploy/examples/


kubectl -n rook-ceph delete cephcluster rook-ceph
kubectl delete -f operator.yaml
kubectl delete -f common.yaml
kubectl delete -f crds.yaml

```

* * *

###### 清空磁盘的脚本 clear-rook-ceph.sh 连接到每台worker机器并执行清除

```shell
#!/usr/bin/env bash
DISK="/dev/sdX"

# Zap the disk to a fresh, usable state (zap-all is important, b/c MBR has to be clean)
sgdisk --zap-all $DISK

# Wipe a large portion of the beginning of the disk to remove more LVM metadata that may be present
dd if=/dev/zero of="$DISK" bs=1M count=100 oflag=direct,dsync

# SSDs may be better cleaned with blkdiscard instead of dd
blkdiscard $DISK

# Inform the OS of partition table changes
partprobe $DISK

# This command hangs on some systems: with caution, 'dmsetup remove_all --force' can be used
ls /dev/mapper/ceph-* | xargs -I% -- dmsetup remove %

# ceph-volume setup can leave ceph-<UUID> directories in /dev and /dev/mapper (unnecessary clutter)
rm -rf /dev/ceph-*
rm -rf /dev/mapper/ceph--*
```

* * *

* * *

* * *

* * *

* * *

* * *

###### 常见问题

```bash
[root@master01 ~]# kubectl -n rook-ceph get pods -o wide
NAME                                                 READY   STATUS      RESTARTS   AGE   IP            NODE       NOMINATED NODE   READINESS GATES
rook-ceph-crashcollector-worker01-b477db6dc-t2dp9    1/1     Running     0          51m   10.244.1.67   worker01   <none>           <none>
rook-ceph-crashcollector-worker02-6fc4b6c54-hccpf    1/1     Running     0          57m   10.244.2.66   worker02   <none>           <none>
rook-ceph-crashcollector-worker03-7fdd56f567-drn4x   1/1     Running     0          54m   10.244.3.82   worker03   <none>           <none>
rook-ceph-csi-detect-version-gcwxg                   0/1     Completed   0          81m   10.244.3.76   worker03   <none>           <none>
rook-ceph-mgr-a-66d587c477-xr7xm                     1/1     Running     1          51m   10.244.1.65   worker01   <none>           <none>
rook-ceph-mon-a-b98bcd678-ncdrx                      1/1     Running     0          58m   10.244.1.63   worker01   <none>           <none>
rook-ceph-mon-b-68d688995-njm95                      1/1     Running     0          57m   10.244.2.64   worker02   <none>           <none>
rook-ceph-mon-d-5444854b86-hqpm5                     1/1     Running     0          54m   10.244.3.80   worker03   <none>           <none>
rook-ceph-operator-798d94c48-p4w5k                   1/1     Running     0          88m   10.244.1.59   worker01   <none>           <none>
rook-ceph-osd-prepare-worker01-sv6qt                 0/1     Completed   0          51m   10.244.1.66   worker01   <none>           <none>
rook-ceph-osd-prepare-worker02-rmwr4                 0/1     Completed   0          51m   10.244.2.65   worker02   <none>           <none>
rook-ceph-osd-prepare-worker03-h8wbc                 0/1     Completed   0          51m   10.244.3.81   worker03   <none>           <none>
rook-discover-jhpfr                                  1/1     Running     0          81m   10.244.3.74   worker03   <none>           <none>
rook-discover-sn72p                                  1/1     Running     0          81m   10.244.1.60   worker01   <none>           <none>
rook-discover-v5pxs                                  1/1     Running     0          81m   10.244.2.62   worker02   <none>           <none>
[root@master01 ~]#

```

**`问题`** **`rook-ceph-csi` `rook-ceph-osd` 状态为 `Completed` 容器不能成功启动**

**`排查方法`**

```bash
kubectl -n rook-ceph logs -f rook-ceph-operator-798d94c48-p4w5k

......
# 其中的失败原因， 定位为 worker主机上因为只有一块硬盘， 而ceph不允许 osd安装在系统盘中， 因此解决方案为在每个worker节点上在加一块新盘
op-mgr: failed modules: "balancer". failed to configure module "balancer": failed to set balancer module mode to "upmap": failed to set mgr module mode "upmap" even after 5 retries: failed to set balancer mode "upmap": exit status 22
......
```

**`最快解决方案`** 在每个worker节点上在 **`加一块新盘`** 需要删除rook-ceph集群，然后重新创建

* * *

###### 在次查看处理后

```bash
[root@master01 kubernetes]# kubectl -n rook-ceph get pods -o wide
NAME                                                 READY   STATUS      RESTARTS   AGE     IP               NODE       NOMINATED NODE   READINESS GATES
csi-cephfsplugin-fhcjt                               3/3     Running     0          9m33s   192.168.20.95    worker01   <none>           <none>
csi-cephfsplugin-fqpcc                               3/3     Running     0          9m33s   192.168.20.96    worker02   <none>           <none>
csi-cephfsplugin-h6z67                               3/3     Running     0          9m33s   192.168.20.100   worker03   <none>           <none>
csi-cephfsplugin-provisioner-5c5df9d8b5-d8xzt        6/6     Running     0          9m32s   10.244.1.89      worker01   <none>           <none>
csi-cephfsplugin-provisioner-5c5df9d8b5-mg9qw        6/6     Running     0          9m32s   10.244.3.98      worker03   <none>           <none>
csi-rbdplugin-mgk6c                                  3/3     Running     0          9m33s   192.168.20.96    worker02   <none>           <none>
csi-rbdplugin-provisioner-7db86459f7-dkqhj           6/6     Running     0          9m33s   10.244.2.88      worker02   <none>           <none>
csi-rbdplugin-provisioner-7db86459f7-dmwg2           6/6     Running     0          9m33s   10.244.1.88      worker01   <none>           <none>
csi-rbdplugin-rnz4c                                  3/3     Running     0          9m33s   192.168.20.100   worker03   <none>           <none>
csi-rbdplugin-wt5ql                                  3/3     Running     0          9m33s   192.168.20.95    worker01   <none>           <none>
rook-ceph-crashcollector-worker01-7cfdd48649-d54k5   1/1     Running     0          8m      10.244.1.93      worker01   <none>           <none>
rook-ceph-crashcollector-worker02-6fc4b6c54-d2lm8    1/1     Running     0          6m39s   10.244.2.96      worker02   <none>           <none>
rook-ceph-crashcollector-worker03-7fdd56f567-jm8n5   1/1     Running     0          8m20s   10.244.3.102     worker03   <none>           <none>
rook-ceph-mgr-a-75f8b7f95c-ld7v6                     1/1     Running     1          7m34s   10.244.2.92      worker02   <none>           <none>
rook-ceph-mon-a-76956bbccc-rgzph                     1/1     Running     0          8m39s   10.244.2.90      worker02   <none>           <none>
rook-ceph-mon-b-9b6fb966-9xbfd                       1/1     Running     0          8m20s   10.244.3.100     worker03   <none>           <none>
rook-ceph-mon-c-684f76fc8-g7zws                      1/1     Running     0          8m      10.244.1.91      worker01   <none>           <none>
rook-ceph-operator-798d94c48-c6v7p                   1/1     Running     0          9m59s   10.244.2.86      worker02   <none>           <none>
rook-ceph-osd-0-865768bb99-rzhfj                     1/1     Running     0          7m3s    10.244.3.103     worker03   <none>           <none>
rook-ceph-osd-1-7c78966ff7-vmkmm                     1/1     Running     0          6m56s   10.244.1.94      worker01   <none>           <none>
rook-ceph-osd-2-6d6bb959d7-s9v9s                     1/1     Running     0          6m39s   10.244.2.95      worker02   <none>           <none>
rook-ceph-osd-prepare-worker01-6sjtf                 0/1     Completed   0          7m33s   10.244.1.92      worker01   <none>           <none>
rook-ceph-osd-prepare-worker02-99ttj                 0/1     Completed   0          7m32s   10.244.2.94      worker02   <none>           <none>
rook-ceph-osd-prepare-worker03-vgmcg                 0/1     Completed   0          7m32s   10.244.3.101     worker03   <none>           <none>
rook-discover-57dgk                                  1/1     Running     0          9m56s   10.244.1.86      worker01   <none>           <none>
rook-discover-cvxnk                                  1/1     Running     0          9m56s   10.244.2.87      worker02   <none>           <none>
rook-discover-mqnzg                                  1/1     Running     0          9m56s   10.244.3.96      worker03   <none>           <none>
[root@master01 kubernetes]#
```

**`rook-ceph-osd-prepare` 是为了创建所在节点的`rook-ceph-osd`，它的任务完成以后就会变成 Completed 状态**

* * *

* * *

* * *

* * *

* * *

* * *

###### **测试 [bitnami/mariadb](http://www.dev-share.top/2020/07/23/k8s-%e5%ae%89%e8%a3%85%e9%83%a8%e7%bd%b2-mariadb-%e9%ab%98%e5%8f%af%e7%94%a8%e3%80%81%e4%b8%bb%e4%bb%8e%e9%9b%86%e7%be%a4/ "bitnami/mariadb") 使用`rook-ceph`**

###### 生成yaml文件

```bash
# 生成 相关yaml
helm template mariadb ./mariadb-7.6.1.tgz --output-dir . \
    --namespace mariadb-ns \
    --set rootUser.password=1qaz2wsx \
    --set replication.enabled=true \
    --set slave.replicas=1 \
    --set master.persistence.enabled=true \
    --set master.persistence.storageClass=rook-ceph-block \
    --set slave.persistence.enabled=false \
    --set image.debug=true
```

* * *

###### 说明

```bash
helm template mariadb ./mariadb-7.6.1.tgz --output-dir . \
    --namespace mariadb-ns \
    --set rootUser.password=1qaz2wsx \                        # root 密码
    --set replication.enabled=true \                          # 启用MariaDB复制
    --set master.persistence.enabled=true \                   # 主节点是否使用 PVC 持久化数据，我这里给主节点启用
    --set master.persistence.storageClass=StorageClass名称 \  # 主节点是否使用 PVC 持久化数据，我这里做测试，所以选择关闭
    --set slave.persistence.enabled=false \                   # 从节点是否使用 PVC 持久化数据，我这里做测试，所以选择关闭
    --set slave.replicas=1 \                                  # 从节点 副本数
    --set image.debug=true                                    # 开启 调试日志功能，生产环境，要关闭
```

* * *

##### 执行后会 **自动生成 `PVC`**

```bash
kubectl apply -R -f mariadb/


## 查看
[root@master01 ~]# kubectl get sc,pv,pvc -A

###### storageclass 是使用 kubectl apply -f ceph/csi/rbd/storageclass.yaml 生成的
NAME                                          PROVISIONER                  AGE
storageclass.storage.k8s.io/rook-ceph-block   rook-ceph.rbd.csi.ceph.com   163m


###### 这个PV是创建 bitnami/mariadb 时它自己创建的
NAME                                                        CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM                              STORAGECLASS      REASON   AGE
persistentvolume/pvc-0ab32d9a-a2e9-4837-961f-f5c595eef20d   8Gi        RWO            Delete           Bound    mariadb-ns/data-mariadb-master-0   rook-ceph-block            129m

###### 这个PVC也是创建 bitnami/mariadb 时它自己创建的
NAMESPACE    NAME                                          STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS      AGE
mariadb-ns   persistentvolumeclaim/data-mariadb-master-0   Bound    pvc-0ab32d9a-a2e9-4837-961f-f5c595eef20d   8Gi        RWO            rook-ceph-block   129m
[root@master01 ~]#

```

* * *

###### 测试链接数据库

```bash
###### 查看MariaDB的IP地址
[root@master01 ~]# kubectl get svc -n mariadb-ns
NAME            TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
mariadb         ClusterIP   10.222.73.103   <none>        3306/TCP   140m
mariadb-slave   ClusterIP   10.222.49.67    <none>        3306/TCP   140m
[root@master01 ~]#


###### 链接数据库
[root@master01 ~]# mysql -h 10.222.73.103 -u root -p
Enter password:
Welcome to the MariaDB monitor.  Commands end with ; or \g.
Your MariaDB connection id is 1652
Server version: 10.3.23-MariaDB-log Source distribution

Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

MariaDB [(none)]>
MariaDB [(none)]> select version();
+---------------------+
| version()           |
+---------------------+
| 10.3.23-MariaDB-log |
+---------------------+
1 row in set (0.00 sec)

MariaDB [(none)]>

```

* * *

* * *

* * *

### 常见问题

##### [设置默认StorageClass](https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/change-default-storage-class/#%E6%94%B9%E5%8F%98%E9%BB%98%E8%AE%A4-storageclass)

`kubectl patch storageclass <your-class-name> -p '{"metadata": {"annotations":{"storageclass.kubernetes.io/is-default-class":"true"}}}'`

```shell
## 查看现状
[root@master01 ~]# kubectl get sc
NAME              PROVISIONER                  RECLAIMPOLICY   VOLUMEBINDINGMODE   ALLOWVOLUMEEXPANSION   AGE
rook-ceph-block   rook-ceph.rbd.csi.ceph.com   Delete          Immediate           true                   5d17h


## 改变状态
[root@master01 ~]# kubectl patch storageclass rook-ceph-block -p '{"metadata": {"annotations":{"storageclass.kubernetes.io/is-default-class":"true"}}}'
storageclass.storage.k8s.io/rook-ceph-block patched


## 查看现状
[root@master01 ~]# kubectl get sc
NAME                        PROVISIONER                  RECLAIMPOLICY   VOLUMEBINDINGMODE   ALLOWVOLUMEEXPANSION   AGE
rook-ceph-block (default)   rook-ceph.rbd.csi.ceph.com   Delete          Immediate           true                   5d17h

```

* * *

* * *

* * *
