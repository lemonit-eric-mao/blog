---
title: "K8S PV PVC NFS 共享卷"
date: "2019-12-19"
categories: 
  - "k8s"
---

##### K8S PV PVC 是什么？有什么作用？

[参考资料](https://www.jianshu.com/p/b6671c4c8915 "参考资料")

   Kubernetes的pod本身是无状态的（stateless）,生命周期通常比较短，只要出现了异常，Kubernetes就会自动创建一个新的Pod来代替它，而容器产生的`数据会随着Pod消亡而自动消失`。

   为了实现Pod内数据的存储管理，Kubernetes引入了两个API资源： **Persistent Volume（持久卷，以下简称`PV`）** **Persistent Volume Claim（持久卷申请，以下简称`PVC`）**。

   PV是Kubernetes集群中的一种网络存储实现，跟Node一样，也是属于集群的资源。    PV跟Docker里的Volume(卷)类似，不过会有独立于Pod的生命周期。

   而PVC是用户的一个请求，跟Pod类似。Pod消费Node的资源，PVC消费PV的资源。    Pod 能够申请特定的资源（CPU和内存）；PVC能够申请特定的尺寸和访问模式，例如可以加载一个读写实例或者多个只读实例，而无须感知这些实例背后具体的存储实现。

   PV, PVC, Pod 需要在同一个命名空间下才能够挂载。**[详见官方文档](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#a-note-on-namespaces "详见官方文档")**

* * *

##### [Persistent Volume 持久卷的作用](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#persistent-volumes "Persistent Volume 持久卷的作用")

##### [Persistent Volume Claim 作用](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims "Persistent Volume Claim 作用")

* * *

* * *

* * *

##### 案例实现思路

1. 使用k8s部署一 httpd网络文件服务器
2. 将`httpd的配置文件`放到nfs服务器上
3. k8s启动时`获取远程nfs共享卷`上的httpd配置文件

##### 工作流程

##### `Pod挂载PVC --> PVC绑定PV --> PV挂载共享卷 --> 共享卷里存放文件`

* * *

###### 1 **[搭建 NFS 服务器](nfs%e5%ae%9e%e7%8e%b0%e7%bd%91%e7%bb%9c%e5%85%b1%e4%ba%ab%e5%8d%b7 "搭建 NFS 服务器")**

* * *

###### 2 配置 PV PVC yaml文件

```ruby
[root@test1 pvc]# pwd
/root/deploy/pvc
[root@test1 pvc]#
```

```ruby
cat > pv-and-pvc.yaml << ERIC

---

# 创建命名空间
kind: Namespace
apiVersion: v1
metadata:
  # 不可以使用 下划线
  name: k8s-tools-os
  labels:
    name: k8s-tools-os

---

##### 创建 persistent-volumes 持久卷
##### https://kubernetes.io/docs/concepts/storage/persistent-volumes/#persistent-volumes
apiVersion: v1
kind: PersistentVolume
metadata:
  name: eric-volume-pv

spec:
  # 存储卷的存储容量
  capacity:
    storage: 5Gi

  # 默认值 Filesystem
  volumeMode: Filesystem

  # 存取模式：每个PV都有自己的一组访问模式，用于描述该特定PV的功能
  # 访问方式为：
  #   ReadWriteOnce –读写模式 的持久卷，只能被单个节点映射
  #   ReadOnlyMany  –只读模式 的持久卷，可以被多个节点映射
  #   ReadWriteMany –读写模式 的持久卷，可以被多个节点映射
  # 注意：如果PV与PVC的权限模式不一样，会报找不到storageClass的错误。
  accessModes:
    - ReadWriteOnce

  # 声明storageClassName的PV，是告诉PVC要想找到PV必须通过 storageClassName才能够找到
  storageClassName: pv-classname

  # 持久卷(PV)回收策略：
  # 数据是否删除取决于PV的ReclaimPolicy配置。
  # Reclaim Policy支持以下三种：
  # Retain(保留)  –保留数据，不会再分配给pvc,需要管理员手工清理数据;
  # Recycle(回收) –清除PV中的数据，保留PV资源,可以留供其他PVC使用; 等同于 rm -rf /thevolume/*
  # Delete(删除)  –删除整个pv资源及内部的数据。
  persistentVolumeReclaimPolicy: Recycle
  mountOptions:
    - hard
    - nfsvers=4.1

  # 配置NFS服务器上卷的路径与IP地址
  nfs:
    path: /home/share-volume/
    server: 172.160.180.46

---

##### 创建 persistentvolumeclaims 申请持久卷
##### https://kubernetes.io/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  # 所属的命名空间
  namespace: k8s-tools-os
  name: eric-volume-pvc

spec:
  accessModes:
    - ReadWriteOnce

  # 告诉PVC 要绑定到哪个PV，如果不指定会自动绑定到没有声明storageClassName的PV
  storageClassName: pv-classname

  volumeMode: Filesystem

  resources:
    requests:
      # 注意：申请的空间不能超过 PV存储卷的存储容量
      storage: 2Gi

---

ERIC

```

* * *

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

* * *

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

```

* * *

###### 5 创建httpd配置文件，放到 NFS 挂载卷中

```ruby
[root@test1 share-volume]# pwd
/home/share-volume
[root@test1 share-volume]# cat > welcome.conf << eric
#
# This configuration file enables the default "Welcome" page if there
# is no default index page present for the root URL.  To disable the
# Welcome page, comment out all the lines below.
#
# NOTE: if this file is removed, it will be restored on upgrades.
#
<LocationMatch "^/+\$">
    Options -Indexes
    ErrorDocument 403 /.noindex.html
</LocationMatch>

<Directory /usr/share/httpd/noindex>
    AllowOverride None
    Require all granted
</Directory>

Alias /.noindex.html /usr/share/httpd/noindex/index.html
Alias /noindex/css/bootstrap.min.css /usr/share/httpd/noindex/css/bootstrap.min.css
Alias /noindex/css/open-sans.css /usr/share/httpd/noindex/css/open-sans.css
Alias /images/apache_pb.gif /usr/share/httpd/noindex/images/apache_pb.gif
Alias /images/poweredby.png /usr/share/httpd/noindex/images/poweredby.png

eric

```

* * *

* * *

* * *

##### 测试

**[构建 httpd 服务器镜像](k8s-%e4%bd%bf%e7%94%a8centos-7-%e9%95%9c%e5%83%8f%ef%bc%8c%e6%9e%84%e5%bb%bak8s%e7%bd%91%e7%bb%9c%e6%b5%8b%e8%af%95%e5%ae%b9%e5%99%a8 "构建 httpd 服务器镜像")**

###### 1 使用k8s部署httpd服务器，这里只修改 deploy 配置文件, 从PVC映射服务器配置文件

```ruby
cat > k8s-tools-deploy.yaml << eric

---

# 创建要部署的容器
# 种类：告诉 k8s 下面这些配置模板的含义(常用的包括：Namespace, Deployment, Service, Pod, ......)
kind: Deployment
# 版本号 规定格式 apps/* 必须这么写
apiVersion: apps/v1
# deploy
metadata:
  # deploy 的所属的命名空间
  namespace: k8s-tools-os
  # deploy 名称
  name: tools-deploy-name

# 容器的详细定义
spec:
  # 告诉 K8s 启动几个节点
  replicas: 1
  # 滚动升级时，容器准备就绪时间最少为30s
  minReadySeconds: 30
  # 选择模板
  selector:
    # 根据模板的labels来选择
    matchLabels:
      # 匹配下面模板中, Pod 的label名, Deploy与Pod绑定
      app: tools-pod-label



  # 定义 Pod模板
  template:
    metadata:
      # Pod模板的labels
      labels:
        # Pod的label名
        app: tools-pod-label
    spec:
      # k8s将会给应用发送SIGTERM信号，可以用来正确、优雅地关闭应用,默认为30秒
      terminationGracePeriodSeconds: 30

      # 告诉 k8s 根据设置的节点名称，将这个pod部署到哪个节点机器上（默认不指定，k8s会自动分配）;
      # 因为 nodeName(节点的名称不可以重复，因此使用nodeName只能指定一台节点服务)
      # nodeName: k8s-node1
      # 告诉 k8s 根据设置的节点标签，将这个pod部署到哪个节点机器上（默认不指定，k8s会自动分配）;
      # 因为 nodeLabels(节点的标签可以重复，因此使用nodeSelector是可以指定同一个标签的多个节点服务)
      nodeSelector:
        type: "test"

      # 配置 Docker容器
      containers:
        # Docker 镜像名
        - name: k8s-tools-os
          # 告诉 K8s 要部署的 Docker 镜像名:Tag
          image: tools-os:v1.0.0
          # 告诉 K8s 如果本地没有这个镜像
          # 总是拉取 pull
          # imagePullPolicy: Always
          # 只使用本地镜像，从不拉取
          # imagePullPolicy: Never
          # 默认值,本地有则使用本地镜像,不拉取
          imagePullPolicy: IfNotPresent
          ## 告诉 K8s Docker容器对外开放几个端口
          ports:
            - containerPort: 80
              #protocol: TCP
          volumeMounts:
            # 容器内部文件 /etc/httpd/conf.d/welcome.conf 但这里只映射到目录
            - mountPath: "/etc/httpd/conf.d/"
              # PVC 别名
              name: volume-pvc

      # 映射 PVC
      volumes:
        # 别名
        - name: volume-pvc
          persistentVolumeClaim:
            # PVC 名称
            claimName: eric-volume-pvc

---
eric

```

* * *

###### 测试连接

```ruby
[root@test1 ~]# kubectl get svc,pod -n k8s-tools-os
NAME                         TYPE       CLUSTER-IP      EXTERNAL-IP   PORT(S)         AGE
service/tools-service-name   NodePort   10.108.164.23   <none>        880:30880/TCP   20h

NAME                                     READY   STATUS    RESTARTS   AGE
pod/tools-deploy-name-5dd8f8db5b-fmzwr   1/1     Running   0          18m
[root@test1 ~]#
[root@test1 ~]# curl 172.160.180.46:30880
```

###### 注意

1 修改共享卷中的配置时，需要重新启动 pod `kubectl delete -f k8s-tools-deploy.yaml && kubectl apply -f k8s-tools-deploy.yaml`
