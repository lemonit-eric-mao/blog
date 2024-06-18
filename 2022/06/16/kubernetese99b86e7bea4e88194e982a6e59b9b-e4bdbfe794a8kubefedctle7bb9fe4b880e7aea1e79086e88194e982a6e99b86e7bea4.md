---
title: Kubernetes集群联邦(四)-使用kubefedctl统一管理联邦集群
date: '2022-06-16T08:47:10+00:00'
status: private
permalink: /2022/06/16/kubernetes%e9%9b%86%e7%be%a4%e8%81%94%e9%82%a6%e5%9b%9b-%e4%bd%bf%e7%94%a8kubefedctl%e7%bb%9f%e4%b8%80%e7%ae%a1%e7%90%86%e8%81%94%e9%82%a6%e9%9b%86%e7%be%a4
author: 毛巳煜
excerpt: ''
type: post
id: 8794
category:
    - CloudNative
    - Kubernetes
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
wb_sst_seo:
    - 'a:3:{i:0;s:0:"";i:1;s:0:"";i:2;s:0:"";}'
---
##### 前置资料

1. **[Kubernetes集群联邦(一)-Federation V2 工作原理](http://www.dev-share.top/2021/02/04/kubernetes%e9%9b%86%e7%be%a4%e8%81%94%e9%82%a6%e4%b8%80-federation-v2-%e5%b7%a5%e4%bd%9c%e5%8e%9f%e7%90%86/)**
2. **[Kubernetes集群联邦(二)-使用Helm部署Kubefed](http://www.dev-share.top/2022/06/16/kubernetes%e9%9b%86%e7%be%a4%e8%81%94%e9%82%a6%e4%ba%8c-%e4%bd%bf%e7%94%a8helm%e9%83%a8%e7%bd%b2kubefed/)**
3. **[Kubernetes集群联邦(三)-使用kubefedctl注册集群联邦](http://www.dev-share.top/2022/06/16/kubernetes%e9%9b%86%e7%be%a4%e8%81%94%e9%82%a6%e4%b8%89-%e4%bd%bf%e7%94%a8kubefedctl%e6%b3%a8%e5%86%8c%e9%9b%86%e7%be%a4%e8%81%94%e9%82%a6/)**

- - - - - -

##### 学习使用 kubefedctl 部署

> - 现在我们来测试一下同时部署一个**deployment**到两个集群中去

###### 1. 这里要注意的是，需要**提前在每个集群中**创建好**命名空间**

```ruby
cat > test-namespace.yaml 
```

```ruby
kubectl --context cluster1 apply -f test-namespace.yaml

kubectl --context cluster2 apply -f test-namespace.yaml


```

- - - - - -

###### 2. 创建一个**FederatedNamespace**

```ruby
cat > test-federated-namespace.yaml 
```

###### 3. 创建**FederatedDeployment**就能在两个集群中同时部署服务了

```ruby
cat > test-federated-deployment.yaml 
```

###### 4. 执行部署

```ruby
kubectl apply -f test-federated-namespace.yaml

kubectl apply -f test-federated-deployment.yaml


```

```ruby
## 查看
[root@centos01 siyu.mao]# kubectl --context cluster1 get pod -o wide -n test-namespace

NAME                              READY   STATUS    RESTARTS   AGE     IP             NODE       NOMINATED NODE   READINESS GATES
test-deployment-b67bb7dbd-48bf6   1/1     Running   0          7m35s   10.100.30.86   worker03   <none>           <none>
test-deployment-b67bb7dbd-5v8gg   1/1     Running   0          2m6s    10.100.30.91   worker02   <none>           <none>
test-deployment-b67bb7dbd-7zkcd   1/1     Running   0          2m6s    10.100.5.27    worker01   <none>           <none>


[root@centos01 siyu.mao]# kubectl --context cluster2 get pod -o wide -n test-namespace

NAME                              READY   STATUS    RESTARTS   AGE     IP               NODE       NOMINATED NODE   READINESS GATES
test-deployment-b67bb7dbd-djk25   1/1     Running   0          2m6s    10.100.196.158   worker01   <none>           <none>
test-deployment-b67bb7dbd-dsv9m   1/1     Running   0          2m6s    10.100.196.157   worker02   <none>           <none>
test-deployment-b67bb7dbd-jc822   1/1     Running   0          2m6s    10.100.140.88    worker03   <none>           <none>

</none></none></none></none></none></none></none></none></none></none></none></none>
```

- - - - - -

###### 5. 移除测试程序

```ruby
kubectl delete -f test-federated-deployment.yaml

kubectl delete -f test-federated-namespace.yaml


```

- - - - - -

- - - - - -

- - - - - -

###### 最后

> - 使用联邦创建的应用，只能使用联邦控制端来管控 
>   - 无论你在集群中如何去操作，它最终都会以集群联邦的控制端的配置为准。

- - - - - -

- - - - - -

- - - - - -

系列导航
----

1. **[Kubernetes集群联邦(一)-Federation V2 工作原理](http://www.dev-share.top/2021/02/04/kubernetes%e9%9b%86%e7%be%a4%e8%81%94%e9%82%a6%e4%b8%80-federation-v2-%e5%b7%a5%e4%bd%9c%e5%8e%9f%e7%90%86/)**
2. **[Kubernetes集群联邦(二)-使用Helm部署Kubefed](http://www.dev-share.top/2022/06/16/kubernetes%e9%9b%86%e7%be%a4%e8%81%94%e9%82%a6%e4%ba%8c-%e4%bd%bf%e7%94%a8helm%e9%83%a8%e7%bd%b2kubefed/)**
3. **[Kubernetes集群联邦(三)-使用kubefedctl注册集群联邦](http://www.dev-share.top/2022/06/16/kubernetes%e9%9b%86%e7%be%a4%e8%81%94%e9%82%a6%e4%b8%89-%e4%bd%bf%e7%94%a8kubefedctl%e6%b3%a8%e5%86%8c%e9%9b%86%e7%be%a4%e8%81%94%e9%82%a6/)**
4. **[Kubernetes集群联邦(四)-使用kubefedctl统一管理联邦集群](http://www.dev-share.top/2022/06/16/kubernetes%e9%9b%86%e7%be%a4%e8%81%94%e9%82%a6%e5%9b%9b-%e4%bd%bf%e7%94%a8kubefedctl%e7%bb%9f%e4%b8%80%e7%ae%a1%e7%90%86%e8%81%94%e9%82%a6%e9%9b%86%e7%be%a4/)**

- - - - - -

- - - - - -

- - - - - -