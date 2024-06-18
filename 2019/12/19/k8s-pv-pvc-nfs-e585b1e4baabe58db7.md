---
title: 'K8S PV PVC NFS 共享卷'
date: '2019-12-19T03:21:39+00:00'
status: publish
permalink: /2019/12/19/k8s-pv-pvc-nfs-%e5%85%b1%e4%ba%ab%e5%8d%b7
author: 毛巳煜
excerpt: ''
type: post
id: 5198
category:
    - Kubernetes
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
##### K8S PV PVC 是什么？有什么作用？

[参考资料](https://www.jianshu.com/p/b6671c4c8915 "参考资料")

 Kubernetes的pod本身是无状态的（stateless）,生命周期通常比较短，只要出现了异常，Kubernetes就会自动创建一个新的Pod来代替它，而容器产生的`数据会随着Pod消亡而自动消失`。

 为了实现Pod内数据的存储管理，Kubernetes引入了两个API资源：  
**Persistent Volume（持久卷，以下简称`PV`）**  
**Persistent Volume Claim（持久卷申请，以下简称`PVC`）**。

 PV是Kubernetes集群中的一种网络存储实现，跟Node一样，也是属于集群的资源。  
 PV跟Docker里的Volume(卷)类似，不过会有独立于Pod的生命周期。

 而PVC是用户的一个请求，跟Pod类似。Pod消费Node的资源，PVC消费PV的资源。  
 Pod 能够申请特定的资源（CPU和内存）；PVC能够申请特定的尺寸和访问模式，例如可以加载一个读写实例或者多个只读实例，而无须感知这些实例背后具体的存储实现。

 PV, PVC, Pod 需要在同一个命名空间下才能够挂载。**[详见官方文档](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#a-note-on-namespaces "详见官方文档")**

- - - - - -

##### [Persistent Volume 持久卷的作用](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#persistent-volumes "Persistent Volume 持久卷的作用")

##### [Persistent Volume Claim 作用](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims "Persistent Volume Claim 作用")

- - - - - -

- - - - - -

- - - - - -

##### 案例实现思路

1. 使用k8s部署一 httpd网络文件服务器
2. 将`httpd的配置文件`放到nfs服务器上
3. k8s启动时`获取远程nfs共享卷`上的httpd配置文件

##### 工作流程

##### `Pod挂载PVC --> PVC绑定PV --> PV挂载共享卷 --> 共享卷里存放文件`

- - - - - -

###### 1 **[搭建 NFS 服务器](http://www.dev-share.top/2019/12/18/nfs%e5%ae%9e%e7%8e%b0%e7%bd%91%e7%bb%9c%e5%85%b1%e4%ba%ab%e5%8d%b7/ "搭建 NFS 服务器")**

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
eric-volume-pv   5Gi        RWO            Recycle          Bound    k8s-tools-os/eric-volume-pvc   pv-classname            140m
[root@test1 pvc]#
[root@test1 pvc]# kubectl get pvc -n k8s-tools-os
NAME              STATUS   VOLUME           CAPACITY   ACCESS MODES   STORAGECLASS   AGE
eric-volume-pvc   Bound    eric-volume-pv   5Gi        RWO            pv-classname   141m
[root@test1 pvc]#

```

- - - - - -

###### 4 查看PV与PVC 详细信息

```ruby
[root@test1 pvc]# kubectl describe pv
Name:            eric-volume-pv
Labels:          <none>
Annotations:     kubectl.kubernetes.io/last-applied-configuration:
                   {"apiVersion":"v1","kind":"PersistentVolume","metadata":{"annotations":{},"name":"eric-volume-pv"},"spec":{"accessModes":["ReadWriteOnce"]...
                 pv.kubernetes.io/bound-by-controller: yes
Finalizers:      [kubernetes.io/pv-protection]
StorageClass:    pv-classname
Status:          Bound
Claim:           k8s-tools-os/eric-volume-pvc
Reclaim Policy:  Recycle
Access Modes:    RWO
VolumeMode:      Filesystem
Capacity:        5Gi
Node Affinity:   <none>
Message:
Source:
    Type:      NFS (an NFS mount that lasts the lifetime of a pod)
    Server:    172.160.180.46
    Path:      /home/share-volume/
    ReadOnly:  false
Events:        <none>
[root@test1 pvc]#
[root@test1 pvc]#
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
Access Modes:  RWO
VolumeMode:    Filesystem
Events:        <none>
Mounted By:    tools-deploy-name-5dd8f8db5b-fmzwr
[root@test1 pvc]#

</none></none></none></none></none>
```

- - - - - -

###### 5 创建httpd配置文件，放到 NFS 挂载卷中

```ruby
[root@test1 share-volume]# pwd
/home/share-volume
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
[root@test1 ~]# curl 172.160.180.46:30880
</none>
```

###### 注意

1 修改共享卷中的配置时，需要重新启动 pod  
`kubectl delete -f k8s-tools-deploy.yaml && kubectl apply -f k8s-tools-deploy.yaml`