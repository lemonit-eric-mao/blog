---
title: 'CKA 学习笔记(三)'
date: '2022-09-01T10:24:15+00:00'
status: publish
permalink: /2022/09/01/cka-%e5%ad%a6%e4%b9%a0%e7%ac%94%e8%ae%b0%e4%b8%89
author: 毛巳煜
excerpt: ''
type: post
id: 9207
category:
    - Kubernetes
tag: []
post_format: []
wb_sst_seo:
    - 'a:3:{i:0;s:0:"";i:1;s:0:"";i:2;s:0:"";}'
hestia_layout_select:
    - sidebar-right
---
##### **前置资料**

###### **[Service](https://kubernetes.io/zh-cn/docs/concepts/services-networking/service/ "Service")**

> - **Service** 是为一组 Pod 提供**相同的 `DNS` 名**， 并且可以在它们之间进行负载均衡。

- - - - - -

###### **[虚拟 IP 和 Service 代理](https://kubernetes.io/zh-cn/docs/concepts/services-networking/service/#virtual-ips-and-service-proxies "虚拟 IP 和 Service 代理")**

> - 在 **Kubernetes** 集群中，每个 **Node** 运行一个 **kube-proxy** 进程。 **kube-proxy** 负责为 **Service** 实现了一种 **VIP（虚拟 IP）** 的形式，而不是 **ExternalName** 的形式。

- - - - - -

###### **[为什么不使用 DNS 轮询？](https://kubernetes.io/zh-cn/docs/concepts/services-networking/service/#%E4%B8%BA%E4%BB%80%E4%B9%88%E4%B8%8D%E4%BD%BF%E7%94%A8-dns-%E8%BD%AE%E8%AF%A2 "为什么不使用 DNS 轮询？")**

> - **不使用 DNS 轮询，有以下几个原因**： 
>   - **DNS** 实现的历史由来已久，**它不遵守记录 TTL**，并且在名称查找到结果后对其进行缓存。
>   - 有些应用程序仅执行一次 **DNS** 查找，并**无限期地缓存结果**。
>   - 即使应用和库进行了适当的重新解析，**DNS** 记录上的 **TTL** 值`低`或为`零`也**可能会给 DNS 带来高负载**，从而使**管理变得困难**。

- - - - - -

###### **[Service 类型](https://kubernetes.io/zh-cn/docs/concepts/services-networking/service/#publishing-services-service-types "Service 类型")**

> - **`ClusterIP`**：通过集群的内部 **IP** 暴露服务，选择该值时服务只能够在集群内部访问。 这也是默认的 **ServiceType**。

- - - - - -

> - **`NodePort`**：通过每个节点上的 **IP** 和静态端口（**NodePort**）暴露服务。 **NodePort** 服务会路由到自动创建的 **ClusterIP** 服务。 通过请求 **`:`**，你可以从集群的外部访问一个 **NodePort** 服务。

- - - - - -

> - **`LoadBalancer`**：使用云提供商的负载均衡器向外部暴露服务。 外部负载均衡器可以将流量路由到自动创建的 **NodePort** 服务和 **ClusterIP** 服务上。

- - - - - -

> - **`ExternalName`**：通过返回 **CNAME** 和对应值，可以将服务映射到 **externalName** 字段的内容（**例如，`foo.bar.example.com`）**。 无需创建任何类型代理。

- - - - - -

- - - - - -

- - - - - -

##### **[无头服务（Headless Service）](https://kubernetes.io/zh-cn/docs/concepts/services-networking/service/#headless-services "无头服务（Headless Service）")**

**[Pod 与 Service 的 DNS](https://kubernetes.io/zh-cn/docs/concepts/services-networking/dns-pod-service/#services "Pod 与 Service 的 DNS")**

> - 有的时候**你不需要或者不想要负载均衡**，或者不想要单独的 **Service IP**。 
>   - 这种情况，可以通过指定 **Cluster IP（spec.clusterIP）** 的值为 **`"None"`** 来创建 **Headless Service**。
>   - 你可以使用 **无头Service** 与其他服务发现机制进行接口，而不必与 **Kubernetes** 的实现捆绑在一起。
>   - 对于**无头Service** K8S **不会分配`Cluster IP`**，**kube-proxy** 也不会处理它们，而且平台也**不会为它们进行`负载均衡`和`路由`**。

- - - - - -

> - 那么想要在 K8S 中使用它，我们可以通过 k8s 的 DNS来找到它，那么DNS又是根据什么配置的呢？ 
>   - DNS 如何实现自动配置，依赖于 **Service** 是否定义了选择器(**spec.selector**)。

- - - - - -

##### 实战，创建3种不同的Service

<div style="overflow:hidden; clear:both; width: 100%; height: 40px; position: relative;">- - - - - -

 <span style="position: absolute;top: 50%;left: 50%; transform: translate(-50%, -50%); background-color: white;">以下为隐藏内容</span> </div> > **一、创建`无头Service`测试程序**

```ruby
cat > test-headless-server.yaml 
```

- - - - - -

> **二、创建`普通Service`测试程序**

```ruby
cat > web-server.yaml 
```

- - - - - -

> **三、创建`有状态的无头Service`测试程序**

```ruby
cat > headless-web-server.yaml 
```

- - - - - -

> 查看3个服务的 DNS 解析方式

```ruby
## 一、查看【无头Service】的 svc,po
[root@k8s-master ~]# kubectl get svc,po -o wide -l app=headless-server
NAME                   TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE   SELECTOR
service/headless-svc   ClusterIP   None         <none>        80/TCP    13m   app=headless-server


NAME                              READY   STATUS    RESTARTS   AGE   IP             NODE            NOMINATED NODE   READINESS GATES
pod/pod-server-698fc7fb58-8mbsf   1/1     Running   0          13m   10.100.7.159   k8s-worker-03   <none>           <none>
pod/pod-server-698fc7fb58-cnqrn   1/1     Running   0          13m   10.100.7.160   k8s-worker-03   <none>           <none>
pod/pod-server-698fc7fb58-nqd4w   1/1     Running   0          13m   10.100.7.158   k8s-worker-03   <none>           <none>
[root@k8s-master ~]#




## 二、查看【普通Service】的 svc,po
[root@k8s-master ~]# kubectl get svc,po -o wide -l app=web-server
NAME                     TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)   AGE    SELECTOR
service/web-server-svc   ClusterIP   10.96.254.166   <none>        80/TCP    8m1s   app=web-server


NAME                                  READY   STATUS    RESTARTS   AGE    IP              NODE            NOMINATED NODE   READINESS GATES
pod/web-server-pod-7b69fcf97c-bzrrt   1/1     Running   0          8m1s   10.100.118.91   k8s-worker-02   <none>           <none>
pod/web-server-pod-7b69fcf97c-p5mbg   1/1     Running   0          8m1s   10.100.7.164    k8s-worker-03   <none>           <none>
pod/web-server-pod-7b69fcf97c-qdx7j   1/1     Running   0          8m1s   10.100.7.163    k8s-worker-03   <none>           <none>
[root@k8s-master ~]#




## 三、查看【有状态无头Service】的 svc,po
[root@k8s-master ~]# kubectl get svc,po -o wide -l app=headless-web-server
NAME                              TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE   SELECTOR
service/headless-web-server-svc   ClusterIP   None         <none>        80/TCP    35s   app=headless-web-server

NAME               READY   STATUS    RESTARTS   AGE   IP              NODE            NOMINATED NODE   READINESS GATES
pod/web-server-0   1/1     Running   0          32s   10.100.36.233   k8s-worker-01   <none>           <none>
pod/web-server-1   1/1     Running   0          28s   10.100.7.170    k8s-worker-03   <none>           <none>
pod/web-server-2   1/1     Running   0          26s   10.100.118.97   k8s-worker-02   <none>           <none>
[root@k8s-master ~]#


</none></none></none></none></none></none></none></none></none></none></none></none></none></none></none></none></none></none></none></none></none>
```

> 对比查看三个服务的 DNS 解析方式

```ruby
## 一、查看【无头Service】的 DNS 解析方式
[root@k8s-master ~]# kubectl exec busybox -- nslookup headless-svc
Server:    10.96.0.10
Address 1: 10.96.0.10 kube-dns.kube-system.svc.cluster.local

#### 【无头Service】的名，直接解析到pod的域名；
#### 注意：这里Pod的名字是根据IP生成的，因此名字不是固定的
Name:      headless-svc
Address 1: 10.100.7.159 10-100-7-159.headless-svc.default.svc.cluster.local
Address 2: 10.100.7.158 10-100-7-158.headless-svc.default.svc.cluster.local
Address 3: 10.100.7.160 10-100-7-160.headless-svc.default.svc.cluster.local
[root@k8s-master ~]#




#### 二、查看【普通Service】的名，会解析到Service对应的集群IP
## 查看普通服务的 DNS 解析方式
[root@k8s-master ~]# kubectl exec busybox -- nslookup web-server-svc
Server:    10.96.0.10
Address 1: 10.96.0.10 kube-dns.kube-system.svc.cluster.local

Name:      web-server-svc
Address 1: 10.96.254.166 web-server-svc.default.svc.cluster.local
[root@k8s-master ~]#




#### 三、查看【有状态无头Service】的 DNS 解析方式
[root@k8s-master ~]# kubectl exec busybox -- nslookup headless-web-server-svc
Server:    10.96.0.10
Address 1: 10.96.0.10 kube-dns.kube-system.svc.cluster.local

#### 注意：这里Pod的名字是固定的，有顺序的
Name:      headless-web-server-svc
Address 1: 10.100.36.233 web-server-0.headless-web-server-svc.default.svc.cluster.local
Address 2: 10.100.118.97 web-server-2.headless-web-server-svc.default.svc.cluster.local
Address 3: 10.100.7.170  web-server-1.headless-web-server-svc.default.svc.cluster.local
[root@k8s-master ~]#


#### 查看固定的Pod DNS 解析
[root@k8s-master ~]# kubectl exec busybox -- nslookup  web-server-0.headless-web-server-svc
Server:    10.96.0.10
Address 1: 10.96.0.10 kube-dns.kube-system.svc.cluster.local

Name:      web-server-0.headless-web-server-svc
Address 1: 10.100.36.233 web-server-0.headless-web-server-svc.default.svc.cluster.local
[root@k8s-master ~]#

```

> - **`总结：`个人理解：无头Service，就是放弃了k8s默认使用的【`虚拟 IP` 和 `Service 代理`】的模式，改为不推荐使用的【`DNS 轮询`】**

- - - - - -

> - **`普通服务`**可以通过负载均衡路由到不同的容器应用

- - - - - -

> 1. **无头Service**，将**Service**的负载策略改为【`DNS 轮询`】 
>   - **Service**将会以 `10-100-7-159.headless-svc.default.svc.cluster.local` 这样的域名对Pod进行访问
> 2. **无头Service** 与 **StatefulSet** 没有任何关系
> 3. **无头Service**，更适用于 **StatefulSet(有状态)** 应用【例如数据库】 
>   - 因为，`无头Service`只是改变了对Pod的请求方式，改为使用域名去访问，但这样的【域名是`不固定`的】，如果我们期望能够指定域名来访问Pod，那么这样做是不够的，所以要配合**StatefulSet** 来使用
>   - 因为，**StatefulSet**，的域名 `web-server-0.headless-web-server-svc.default.svc.cluster.local` 是这样的，它的名称是【有序而且`固定`】的

- - - - - -

- - - - - -

- - - - - -

##### **[ExternalName 类型](https://kubernetes.io/zh-cn/docs/concepts/services-networking/service/#externalname "ExternalName 类型")**

> **类型为 ExternalName 的Service** 将 **Service名称** 映射到 **DNS**，而不是使用典型的选择算符。 你可以使用 **`spec.externalName`** 参数指定**外部服务地址**。  
>  例如，以下 **Service** 定义将 `prod` 命名空间中的 `my-service` 服务映射到 `my.database.example.com`

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
  namespace: prod
spec:
  type: ExternalName
  externalName: my.database.example.com

```

##### **`警告`**：

对于一些常见的协议，包括 **HTTP** 和 **HTTPS**，你使用 **ExternalName** 可能会遇到问题。如果你使用 **ExternalName**，那么**集群内**客户端**使用的主机名**与 **ExternalName** 引用的**名称不同**。

> 对于使用主机名的协议，此差异可能会导致错误或意外响应。 **HTTP** 请求将具有源服务器**无法识别的 `Host: 标头`**； **TLS** 服务器将无法提供与客户端连接的主机名匹配的证书。

- - - - - -

- - - - - -

- - - - - -