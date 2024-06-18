---
title: 'K8S PV PVC CEPH 共享卷'
date: '2019-12-27T02:19:34+00:00'
status: publish
permalink: /2019/12/27/k8s-pv-pvc-ceph-%e5%85%b1%e4%ba%ab%e5%8d%b7
author: 毛巳煜
excerpt: ''
type: post
id: 5205
category:
    - Kubernetes
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
##### 案例实现思路

1. 使用k8s部署一 httpd网络文件服务器
2. 将`httpd的配置文件`放到ceph服务器上
3. k8s启动时`获取远程ceph共享卷`上的httpd配置文件

##### 前置条件

###### [官方文档](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#mount-options "官方文档")

**注意**:并非所有持久卷类型都支持挂载选项，ceph 相关的 目前只支持两种：

- RBD (Ceph Block Device) **[官方配置 RBD](https://kubernetes.io/docs/concepts/storage/storage-classes/#ceph-rbd "官方配置 RBD")**
- CephFS **[官方配置 CephFS](https://kubernetes.io/docs/concepts/storage/volumes/#cephfs "官方配置 CephFS")**

**[K8s官方github，添加ceph验证文件](https://github.com/kubernetes/examples/tree/master/volumes/cephfs "K8s官方github，添加ceph验证文件")**

**获取cephfs-secret key, 就是`将ceph获取到的密钥转一下base64`**

```ruby
[root@test1 ~]# docker exec ceph-mon ceph-authtool --print-key /etc/ceph/ceph.client.admin.keyring | base64
QVFBemRBUmV3L2Q3SlJBQWJ3YmdSaDlwMHo4c1hDRFZzZzYxZVE9PQo=
[root@test1 ~]#

```

**或者将密钥写到文件中备用，但是这种方法不好用还未验证什么原因**

```ruby
echo $(docker exec ceph-mon ceph-authtool --print-key /etc/ceph/ceph.client.admin.keyring) | base64 > /etc/ceph/admin.secret

```

##### 工作流程

##### `Pod挂载PVC --> PVC绑定PV --> PV挂载共享卷 --> 共享卷里存放文件`

- - - - - -

###### 1 **[搭建 CEPH 集群](http://www.dev-share.top/2019/12/24/docker-compose-%E9%83%A8%E7%BD%B2ceph%E9%9B%86%E7%BE%A4/ "搭建 CEPH 集群")**

- - - - - -

###### 2 配置 PV PVC yaml文件

```ruby
[root@test1 pvc]# pwd
/root/deploy/pvc
[root@test1 pvc]#

```

```ruby
cat > pv-and-pvc.yaml 
```

- - - - - -

###### 3 创建PV与PVC

```ruby
[root@test1 pvc]# kubectl apply -f pv-and-pvc.yaml
persistentvolume/eric-volume-pv created
persistentvolumeclaim/eric-volume-pvc created
[root@test1 pvc]#
[root@test1 pvc]#
[root@test1 pvc]# kubectl get pv
NAME             CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM                          STORAGECLASS   REASON   AGE
eric-volume-pv   5Gi        RWX            Retain           Bound    k8s-tools-os/eric-volume-pvc   pv-classname            25m
[root@test1 pvc]#
[root@test1 pvc]#
[root@test1 pvc]# kubectl get pvc -n k8s-tools-os
NAME              STATUS   VOLUME           CAPACITY   ACCESS MODES   STORAGECLASS   AGE
eric-volume-pvc   Bound    eric-volume-pv   5Gi        RWX            pv-classname   25m
[root@test1 pvc]#

```

- - - - - -

###### 4 查看PV与PVC 详细信息

```ruby
[root@test1 pvc]# kubectl describe pv
Name:            eric-volume-pv
Labels:          <none>
Annotations:     kubectl.kubernetes.io/last-applied-configuration:
                   {"apiVersion":"v1","kind":"PersistentVolume","metadata":{"annotations":{},"name":"eric-volume-pv"},"spec":{"accessModes":["ReadWriteMany"]...
                 pv.kubernetes.io/bound-by-controller: yes
Finalizers:      [kubernetes.io/pv-protection]
StorageClass:    pv-classname
Status:          Bound
Claim:           k8s-tools-os/eric-volume-pvc
Reclaim Policy:  Retain
Access Modes:    RWX
VolumeMode:      Filesystem
Capacity:        5Gi
Node Affinity:   <none>
Message:
Source:
    Type:        CephFS (a CephFS mount on the host that shares a pod's lifetime)
    Monitors:    [172.168.180.46:6789 172.168.180.47:6789 172.168.180.48:6789]
    Path:
    User:        admin
    SecretFile:
    SecretRef:   &SecretReference{Name:ceph-secret,Namespace:,}
    ReadOnly:    true
Events:          <none>
</none></none></none>
```

```ruby
[root@test1 pvc]# kubectl describe pvc -n k8s-tools-os
Name:          eric-volume-pvc
Namespace:     k8s-tools-os
StorageClass:  pv-classname
Status:        Bound
Volume:        eric-volume-pv
Labels:        <none>
Annotations:   kubectl.kubernetes.io/last-applied-configuration:
                 {"apiVersion":"v1","kind":"PersistentVolumeClaim","metadata":{"annotations":{},"name":"eric-volume-pvc","namespace":"k8s-tools-os"},"spec"...
               pv.kubernetes.io/bind-completed: yes
               pv.kubernetes.io/bound-by-controller: yes
Finalizers:    [kubernetes.io/pvc-protection]
Capacity:      5Gi
Access Modes:  RWX
VolumeMode:    Filesystem
Events:        <none>
Mounted By:    tools-deploy-name-69578d4546-zfxrf
[root@test1 pvc]#

</none></none>
```

###### 查看是否挂载成功

可以去web管理界面中`http://172.168.180.46:7000/clients/1/`查看挂载到哪个节点上了，然后去那台节点机查看挂载盘信息

```ruby
[root@test4 ~]# df -h | grep eric-volume-pv
172.168.180.46:6789,172.168.180.47:6789,172.168.180.48:6789:/   91G     0   91G    0% /var/lib/kubelet/pods/95cc821f-286f-11ea-b07c-00505697d756/volumes/kubernetes.io~cephfs/eric-volume-pv
[root@test4 ~]#

```

- - - - - -

###### 5 创建httpd配置文件，放到 ceph 挂载卷中

```ruby
[root@test1 share-volume]# pwd
/mnt/share-volume
[root@test1 share-volume]# cat > welcome.conf 
    Options -Indexes
    ErrorDocument 403 /.noindex.html


<directory>
    AllowOverride None
    Require all granted
</directory>

Alias /.noindex.html /usr/share/httpd/noindex/index.html
Alias /noindex/css/bootstrap.min.css /usr/share/httpd/noindex/css/bootstrap.min.css
Alias /noindex/css/open-sans.css /usr/share/httpd/noindex/css/open-sans.css
Alias /images/apache_pb.gif /usr/share/httpd/noindex/images/apache_pb.gif
Alias /images/poweredby.png /usr/share/httpd/noindex/images/poweredby.png

eric


```

- - - - - -

- - - - - -

- - - - - -

##### 测试

**[构建 httpd 服务器镜像](http://www.dev-share.top/2019/12/12/k8s-%e4%bd%bf%e7%94%a8centos-7-%e9%95%9c%e5%83%8f%ef%bc%8c%e6%9e%84%e5%bb%bak8s%e7%bd%91%e7%bb%9c%e6%b5%8b%e8%af%95%e5%ae%b9%e5%99%a8/ "构建 httpd 服务器镜像")**

###### 1 使用k8s部署httpd服务器，这里只修改 deploy 配置文件, 从PVC映射服务器配置文件

```ruby
cat > k8s-tools-deploy.yaml 
```

- - - - - -

###### 测试连接

```ruby
[root@test1 ~]# kubectl get svc,pod -n k8s-tools-os
NAME                         TYPE       CLUSTER-IP      EXTERNAL-IP   PORT(S)         AGE
service/tools-service-name   NodePort   10.108.164.23   <none>        880:30880/TCP   20h

NAME                                     READY   STATUS    RESTARTS   AGE
pod/tools-deploy-name-5dd8f8db5b-fmzwr   1/1     Running   0          18m
[root@test1 ~]#
[root@test1 ~]# curl 172.168.180.46:30880
</none>
```

###### 注意

1 修改共享卷中的配置时，需要重新启动 pod  
`kubectl delete -f k8s-tools-deploy.yaml && kubectl apply -f k8s-tools-deploy.yaml`