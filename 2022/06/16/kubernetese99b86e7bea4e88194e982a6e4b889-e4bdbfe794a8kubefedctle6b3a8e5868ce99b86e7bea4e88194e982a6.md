---
title: Kubernetes集群联邦(三)-使用kubefedctl注册集群联邦
date: '2022-06-16T05:15:43+00:00'
status: private
permalink: /2022/06/16/kubernetes%e9%9b%86%e7%be%a4%e8%81%94%e9%82%a6%e4%b8%89-%e4%bd%bf%e7%94%a8kubefedctl%e6%b3%a8%e5%86%8c%e9%9b%86%e7%be%a4%e8%81%94%e9%82%a6
author: 毛巳煜
excerpt: ''
type: post
id: 8780
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

- - - - - -

- - - - - -

- - - - - -

- - - - - -

##### 前置条件

###### 控制机，独立于k8s集群的主机

> <table><thead><tr><th align="center">管理服务器</th><th align="center">IP地址</th><th align="center">资源配置</th><th align="center">功能</th><th align="center">备注</th></tr></thead><tbody><tr><td align="center">控制机-kubefed</td><td align="center">12.3.4.5</td><td align="center">4vCPU;8GB;100G+400G</td><td align="center">虚拟机</td><td align="center">CentOS7.9 内核：3.10以上</td></tr><tr><td align="center">集群01-Master</td><td align="center">12.3.4.11</td><td align="center">4vCPU;8GB;100G+400G</td><td align="center">k8s-v1.20.4 基于containerd部署</td><td align="center">CentOS7.9 内核：3.10以上</td></tr><tr><td align="center">集群02-Master</td><td align="center">12.3.4.15</td><td align="center">4vCPU;8GB;100G+400G</td><td align="center">k8s-v1.20.4 基于containerd部署</td><td align="center">CentOS7.9 内核：3.10以上</td></tr></tbody></table>

##### 统一管理k8s集群

###### 安装 kubectl

```ruby
## 配置K8S的yum源
cat > /etc/yum.repos.d/kubernetes.repo 
```

###### 配置在当前的机器中能够切换多个k8s集群

**[拉取k8s集群.kube/config](http://www.dev-share.top/2020/09/29/k8s-%e5%a4%9a%e9%9b%86%e7%be%a4%e5%88%87%e6%8d%a2/ "拉取k8s集群.kube/config") 跳转链接**

```ruby
./generate-kube-config.sh \
    cluster1=12.3.4.11 \
    cluster2=12.3.4.15 \
    && source /etc/profile


```

```ruby
## 查看
kubectl config get-contexts

```

```ruby
CURRENT   NAME       CLUSTER    AUTHINFO   NAMESPACE
*         cluster1   cluster1   cluster1
          cluster2   cluster2   cluster2


```

###### 检查不同集群的链接状态

```ruby
kubectl --context cluster1 get node -o wide

kubectl --context cluster2 get node -o wide


```

- - - - - -

- - - - - -

- - - - - -

##### 使用**kubefedctl**工具管理集群联邦

**[官方github地址](https://github.com/kubernetes-sigs/kubefed/tags "官方github下载地址")**

- - - - - -

###### 下载kubefedctl工具

```ruby
## 下载
wget https://github.com/kubernetes-sigs/kubefed/releases/download/v0.9.2/kubefedctl-0.9.2-linux-amd64.tgz

## 解压
tar -zxvf kubefedctl-0.9.2-linux-amd64.tgz

## 将工具放到全局
mv kubefedctl /usr/local/bin/


```

```ruby
## 查看版本
kubefedctl version

kubefedctl version: version.Info{Version:"v0.9.1-27-g44c3be44d", GitCommit:"44c3be44db2385f6a09d815d0942679e0e0f04d2", GitTreeState:"clean", BuildDate:"2022-05-18T08:31:38Z", GoVersion:"go1.16.6", Compiler:"gc", Platform:"linux/amd64"}


```

- - - - - -

###### 加入集群

```ruby
## 加入集群cluster1，并且将cluster1做为主集群
kubefedctl join cluster1 --cluster-context cluster1 \
    --host-cluster-context cluster1 --v=2

## 加入集群cluster2，并且将cluster1做为主集群
kubefedctl join cluster2 --cluster-context cluster2 \
    --host-cluster-context cluster1 --v=2


```

- - - - - -

###### 检查加入集群的状态

```ruby
kubectl -n kube-federation-system get kubefedclusters


```

```ruby
NAME       AGE   READY   KUBERNETES-VERSION
cluster1   11m   True    v1.20.6
cluster2   11m   True    v1.20.6


```

> ###### 到这里 我们已经成功的使用 **`kubefedctl`** 工具将集群**加入联邦**

- - - - - -

###### 分离集群

```ruby
kubefedctl unjoin cluster1 --cluster-context cluster1 \
    --host-cluster-context cluster1 --v=2

kubefedctl unjoin cluster2 --cluster-context cluster2 \
    --host-cluster-context cluster1 --v=2


```

> - **分离集群**时，这里会有一个问题，当被分离的集群为 **`非`cluster1** 时，集群上所部署的 **kubefed** 程序会被删除，并且需要手动强制删除其它命名空间。 
>   1. 如果想要分离哪个集群，就先手动删除那个集群上的**kubefed**，然后在执行**分离集群**的命令
>   2. 如果直接执行了**分离集群**的命令，就需要手动删除那个集群上，执行强制删除命令

```ruby
## 强制删除
NS_NAME=kube-federation-system

kubectl get namespace <span class="katex math inline">NS_NAME -o json | tr -d "\n" | sed "s/\"finalizers\": \[[^]]\+\]/\"finalizers\": []/" | kubectl replace --raw /api/v1/namespaces/</span>NS_NAME/finalize -f -

```

- - - - - -

- - - - - -

- - - - - -

##### 最后

> - 到此，使用kubefedctl注册集群联邦已经完成，接下来，需要了解，我们如何去使用它部署应用程序

**[Kubernetes集群联邦(四)-使用kubefedctl统一管理联邦集群](http://www.dev-share.top/2022/06/16/kubernetes%e9%9b%86%e7%be%a4%e8%81%94%e9%82%a6%e5%9b%9b-%e4%bd%bf%e7%94%a8kubefedctl%e7%bb%9f%e4%b8%80%e7%ae%a1%e7%90%86%e8%81%94%e9%82%a6%e9%9b%86%e7%be%a4/)**

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