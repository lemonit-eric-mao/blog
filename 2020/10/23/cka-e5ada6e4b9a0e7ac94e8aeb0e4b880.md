---
title: 'CKA 学习笔记(一)'
date: '2020-10-23T10:59:14+00:00'
status: private
permalink: /2020/10/23/cka-%e5%ad%a6%e4%b9%a0%e7%ac%94%e8%ae%b0%e4%b8%80
author: 毛巳煜
excerpt: ''
type: post
id: 6460
category:
    - Kubernetes
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
wb_sst_seo:
    - 'a:3:{i:0;s:0:"";i:1;s:0:"";i:2;s:0:"";}'
---
##### **整体架构**

[![](https://kuboard.cn/images/topology/kubernetes.png)](https://kuboard.cn/images/topology/kubernetes.png)

#### **[kubernetes设计图](https://kubernetes.io/zh/docs/concepts/architecture/cloud-controller/#design "kubernetes设计图")**

[![](http://qiniu.dev-share.top/image/components-of-kubernetes.png)](http://qiniu.dev-share.top/image/components-of-kubernetes.png)

- - - - - -

- - - - - -

- - - - - -

##### **知识补充**

**什么是路由表？**  
 要理解k8s的网络一定要先理解路由是怎么回事儿，还要知道所有的路由器都是在 **`已知可路由的情况下`** 才会工作， 如果路由表中没有找到可路由信息， 所有路由器都一样，它会直接扔掉这个请求。不可路由的现象就是我们常见的 **`丢包`**

**kubelet的作用是什么？**  
 kubelet在WorkerNode中负责管理自己的节点，并将当前节点中的所有情况及时汇报给 **`kube-apiserver`**

**kube-proxy的作用是什么？**  
 kube-proxy它负责监听 **`kube-apiserver`** 中的信息如：**svc ip、pod ip**， 并将这些信息同步到自己所在WorkerNode的 **`iptables`** 的路由表中

**service是如何为Pod做负载均衡的？**  
 svc只知道自己要负责哪些Pod负载均衡， 但它不知道这些Pod在哪些机器上， 所以svc要想找到Pod在哪儿，必需先找CNI的路由器(`这里使用calico容器网络插件`)， 然后通过CNI路由到节点机， 之后才能够找对应的Pod

- - - - - -

- - - - - -

- - - - - -

##### **Kubernetes 工作原理图**

[![](http://qiniu.dev-share.top/k8s-%E5%B7%A5%E4%BD%9C%E5%8E%9F%E7%90%86.png)](http://qiniu.dev-share.top/k8s-%E5%B7%A5%E4%BD%9C%E5%8E%9F%E7%90%86.png)

1. kubectl 发请求
2. `kube-apiserver`接收到请求 --&gt; 先询问`kube-controller-manager`用户需要多少资源并将结果告诉`kube-apiserver`
3. `kube-apiserver`得到响应 --&gt; 根据响应结果，再去询问`kube-scheduler`在哪些节点上申请资源运行程序最合适并将结果告诉`kube-apiserver`
4. `kube-apiserver`得到响应 --&gt; 根据响应结果，找到对应节点上的`kubelet`
5. 告诉对应的节点上的`kubelet`， 需要在它所在的这台机器上申请资源并且运行程序
6. `kubelet`接收到请求 --&gt; 找到本机的容器引擎`Container Engine`
7. `Container Engine`接收到请求后驱动容器 --&gt; 从image仓库拉取镜像
8. 最后告诉Pod可以创建容器并启动应用程序。

- - - - - -

- - - - - -

- - - - - -

##### **Kubernetes 东西向-网络架构图**

[![](http://qiniu.dev-share.top/k8s-W-E.jpg)](http://qiniu.dev-share.top/k8s-W-E.jpg)

**前提：** 此时iptables中的路由表已经由 kube-proxy完成同步， iptables中存放的是k8s集群内部所有的 **`pod与svc`之间的可路由地址**  
1\. `Pod D`向`Pod A`发起请求 --&gt; 首先找`Pod D`所在的主机WorkerNode 2的iptables  
2\. 通过`WorkerNode 2`的iptables找到对应的容器网络接口 **CNI**  
3\. 由WorkerNode 2的CNI路由进行DNAT转换 --&gt; 找到WorkerNode 1的CNI路由  
4\. 通过WorkerNode 1的路由找到Service 1相关的 **`Pod A`**

- - - - - -

- - - - - -

- - - - - -

##### **Kubernetes 南北向-网络架构图**

[![](http://qiniu.dev-share.top/k8s-N-S.png)](http://qiniu.dev-share.top/k8s-N-S.png)

**前提：** Service Type: **Load Balancer**  
1\. 外部请求 --&gt; External IP --&gt; NodePort:31204 --&gt; ClusterIP --&gt; CNI --&gt; 本地iptables --&gt; Pod  
2\. **`注意`：** 如果Pod与**本地iptables**不在同一个节点上， **本地iptables**会将请求重新指给 **CNI**， 然后路由到其它节点的Pod上

- - - - - -

- - - - - -

- - - - - -

[![](http://qiniu.dev-share.top/k8s-%E7%94%9F%E5%91%BD%E5%91%A8%E6%9C%9F.png)](http://qiniu.dev-share.top/k8s-%E7%94%9F%E5%91%BD%E5%91%A8%E6%9C%9F.png)

- - - - - -

[![](http://qiniu.dev-share.top/k8s-%E6%9C%80%E5%B0%8F%E8%B0%83%E5%BA%A6%E5%8D%95%E5%85%83.png)](http://qiniu.dev-share.top/k8s-%E6%9C%80%E5%B0%8F%E8%B0%83%E5%BA%A6%E5%8D%95%E5%85%83.png)

- - - - - -

##### **[添加kubectl命令自动补全](https://kubernetes.io/zh/docs/reference/kubectl/cheatsheet/ "添加kubectl命令自动补全")**

```ruby
###### 安装依赖
yum install -y bash-completion

###### 在 bash 中设置当前 shell 的自动补全，要先安装 bash-completion 包。
source > ~/.bashrc

```

- - - - - -

##### 使用k8s命令创建pod的 yaml文件

```
kubectl run              run命令只能创建pod
-o yaml                  输出yaml文件内容
--dry-run client         不执行

```

```ruby
kubectl run mybusybox --image=busybox --command sleep 300 -o yaml --dry-run client

```

- - - - - -

- - - - - -

- - - - - -

##### **[配置存活、就绪和启动探测器](https://kubernetes.io/zh/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/ "配置存活、就绪和启动探测器")**

场景： pod是活着的，但pod中的程序可能运行的不正常， 探针起到探测、健康检查的作用

```ruby
cat > liveness-pod.yaml 
```

- - - - - -

- - - - - -

- - - - - -

##### 使用k8s命令创建 deployment 的yaml文件

```
kubectl create           创建
-o yaml                  输出yaml文件内容
--dry-run client         只生成文件，但不执行

```

**kubectl create deployment `deployment名称` --image=`镜像名` -o yaml --dry-run=client &gt; yaml文件名.yaml**

```ruby
kubectl create deployment my-nginx --image=nginx -o yaml --dry-run=client > nginx-deployment.yaml
kubectl apply -f nginx-deployment.yaml

```

- - - - - -

- - - - - -

- - - - - -

##### 打标签

**node、 deploy、 namespace 等都可以打标签**  
`kubectl     label     [node | deploy | namespace | ......]     名称     标签名(key=value)`

```ruby
###### 给pod打标签
kubectl label pod my-nginx app666=001

###### 根据标签查询 pod
kubectl get pod -l app666=001

###### 删除标签
kubectl label pod my-nginx app666-

```

- - - - - -

- - - - - -

- - - - - -

##### 回滚

###### `kubectl set image deploy deploy名称 镜像=镜像:版本 --record` 开启记录命令

```ruby
###### 创建 deployment
root@msy-master01:~# kubectl create deployment nginx-app --image=nginx:1.10.2-alpine --replicas=3
deployment.apps/nginx-app created
root@msy-master01:~#
root@msy-master01:~#
root@msy-master01:~# kubectl rollout history deploy nginx-app
deployment.apps/nginx-app
REVISION  CHANGE-CAUSE
1         <none>


###### 修改镜像版本为 1.13.0-alpine
root@msy-master01:~# kubectl set image deploy nginx-app nginx=nginx:1.13.0-alpine --record
deployment.apps/nginx-app image updated

###### 修改镜像版本为 1.10.2-alpine
root@msy-master01:~# kubectl set image deploy nginx-app nginx=nginx:1.10.2-alpine --record
deployment.apps/nginx-app image updated

###### 查看历史记录
root@msy-master01:~# kubectl rollout history deploy nginx-app
deployment.apps/nginx-app
REVISION  CHANGE-CAUSE
2         kubectl set image deploy nginx-app nginx=nginx:1.13.0-alpine --record=true
3         kubectl set image deploy nginx-app nginx=nginx:1.10.2-alpine --record=true     # 最下面的为当前运行的版本


###### 回滚
root@msy-master01:~# kubectl rollout undo deploy nginx-app
deployment.apps/nginx-app rolled back
###### 查看
root@msy-master01:~# kubectl rollout history deploy nginx-app
deployment.apps/nginx-app
REVISION  CHANGE-CAUSE
4         kubectl set image deploy nginx-app nginx=nginx:1.13.0-alpine --record=true
5         kubectl set image deploy nginx-app nginx=nginx:1.10.2-alpine --record=true     # 最下面的为当前运行的版本


###### 回滚到指定版本号
root@msy-master01:~# kubectl rollout undo deploy nginx-app --to-revision=4
deployment.apps/nginx-app rolled back

###### 查看
root@msy-master01:~# kubectl rollout history deploy nginx-app
deployment.apps/nginx-app
REVISION  CHANGE-CAUSE
5         kubectl set image deploy nginx-app nginx=nginx:1.10.2-alpine --record=true
6         kubectl set image deploy nginx-app nginx=nginx:1.13.0-alpine --record=true     # 最下面的为当前运行的版本

root@msy-master01:~#

</none>
```

- - - - - -

##### 总结

**`deployment` --&gt; `RS`(replicaset) --&gt; `pod`**  
1\. deployment 管理 `RS`  
2\. 每次修改deploy都会创建一个 `RS`  
3\. 回滚 实际上是告诉deploy使用哪个 `RS`  
4\. 真正管理 pod副本数量的是 `RS`

- - - - - -

- - - - - -

- - - - - -

##### 基于deployment 创建service

**容器的命名端口：**  
 **通常容器端口写法 `--target-port=8080`**  
 **命名端口写法 `--target-port=http`**  
**kubectl expose deployment `deployment名称` --port=80`(service代理的端口)` --target-port=http`(pod端口)`**

```ruby
kubectl expose deployment my-nginx --port=80 --target-port=http

```

- - - - - -

**之前在pod中创建的容器，只能在集群内部访问， 这里创建service 是为了在集群外部也通过访问**

- - - - - -

##### 基于deployment**文件** 创建service

```ruby
## 创建deployment
kubectl create deployment my-nginx --image=nginx:1.21.1 --port=80 --dry-run=client -o yaml > my-nginx-deploy.yaml

## 基于deployment 创建service
kubectl expose -f my-nginx-deploy.yaml --port=80 --target-port=80 --dry-run=client -o yaml > my-nginx-service.yaml


```

- - - - - -

- - - - - -

- - - - - -