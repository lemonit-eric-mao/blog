---
title: 'Helm 安装 bitnami/redis 集群模式'
date: '2020-07-13T11:51:36+00:00'
status: publish
permalink: /2020/07/13/helm-%e5%ae%89%e8%a3%85-bitnami-redis-%e9%9b%86%e7%be%a4%e6%a8%a1%e5%bc%8f
author: 毛巳煜
excerpt: ''
type: post
id: 5365
category:
    - Kubernetes
    - Redis
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
views:
    - '1'
wb_sst_seo:
    - 'a:3:{i:0;s:0:"";i:1;s:0:"";i:2;s:0:"";}'
---
#### 前置资料

###### **[安装 Helm](http://www.dev-share.top/2020/07/16/helm-%e5%ae%89%e8%a3%85-%e4%bd%bf%e7%94%a8/ "安装 Helm")**

###### **[官方github](https://github.com/bitnami/charts/tree/master/bitnami/redis-cluster "官方github")**

- - - - - -

#### Helm 安装 bitnami/redis 集群

```ruby
helm repo add bitnami https://charts.bitnami.com/bitnami

## 查看安装版本
helm search repo list
NAME                            CHART VERSION   APP VERSION     DESCRIPTION
bitnami/kube-state-metrics      3.2.1           2.5.0           kube-state-metrics is a simple service that lis...
bitnami/redis                   17.1.3          7.0.4           部署主从集群，可选择是否启用 Redis Sentinel
bitnami/redis-cluster           8.2.1           7.0.4           部署具有分片的 Redis 集群拓扑


```

```ruby
helm repo update

## 将chart包下载到本地
export REDIS_VERSION=8.2.1
helm pull bitnami/redis-cluster --version $REDIS_VERSION

```

<table><thead><tr><th align="center">**[Redis](http://www.dev-share.top/2022/09/06/helm-%e5%ae%89%e8%a3%85-bitnami-redis/ "Redis")**</th><th align="center">**[Redis 集群](http://www.dev-share.top/2020/07/13/helm-%e5%ae%89%e8%a3%85-bitnami-redis-%e9%9b%86%e7%be%a4/ "Redis 集群")**</th></tr></thead><tbody><tr><td align="center">支持多个数据库</td><td align="center">仅支持一个数据库。如果你有一个大数据集更好</td></tr><tr><td align="center">单写点（单主）</td><td align="center">多个写入点（多个主控）</td></tr><tr><td align="center">![](http://qiniu.dev-share.top/image/png/redis-topology.png)</td><td align="center">![](http://qiniu.dev-share.top/image/png/redis-cluster-topology.png)</td></tr></tbody></table>

#### 先决条件

- Kubernetes 1.19+
- Helm 3.2.0+
- 底层基础设施中的 PV 供应商支持

#### 安装部署 Redis 集群

```ruby
## 创建命令空间
export REDIS_NAMESPACE=redis-cluster
kubectl create ns $REDIS_NAMESPACE


```

**创建`values.yaml`**

```ruby
cat > values.yaml = 6，否则集群创建将失败
  nodes: 6
  ## 集群中每个 master 的副本数
  replicas: 1

  update:
    ## 当前部署的 Redis 节点数
    currentNumberOfNodes: 6
    ## 当前部署的 Redis 副本数
    currentNumberOfReplicas: 1

#  ##
#  externalAccess:
#    ## 是否启动从k8s集群外部访问Redis，默认 (false)
#    ## 这个操作会让每一个Pod都对应一个Service，并且每个Service都需要一个 LoadBalancer IP，所以不建议使用这个功能
#    enabled: false
#    service:
#      type: LoadBalancer
#      port: 6379

ERIC


```

```ruby
## 安装部署
helm install redis ./redis-cluster-<span class="katex math inline">REDIS_VERSION.tgz -f values.yaml -n</span>REDIS_NAMESPACE

```

```ruby
#### 如果安装成功，会输出如下信息
NAME: redis
LAST DEPLOYED: Mon Sep  5 19:37:03 2022
NAMESPACE: redis-cluster
STATUS: deployed
REVISION: 1
TEST SUITE: None
NOTES:
CHART NAME: redis-cluster
CHART VERSION: 8.2.1
APP VERSION: 7.0.4** Please be patient while the chart is being deployed **

...... 省略

```

```ruby
## 查看集群信息
kubectl -n redis-cluster get all -o wide
NAME                        READY   STATUS    RESTARTS   AGE   IP               NODE            NOMINATED NODE   READINESS GATES
pod/redis-redis-cluster-0   1/1     Running   3          11h   10.100.78.244    k8s-worker-04   <none>           <none>
pod/redis-redis-cluster-1   1/1     Running   1          29m   10.100.55.211    k8s-worker-05   <none>           <none>
pod/redis-redis-cluster-2   1/1     Running   0          11h   10.100.165.157   k8s-worker-06   <none>           <none>
pod/redis-redis-cluster-3   1/1     Running   0          11h   10.100.78.211    k8s-worker-04   <none>           <none>
pod/redis-redis-cluster-4   1/1     Running   0          11h   10.100.55.233    k8s-worker-05   <none>           <none>
pod/redis-redis-cluster-5   1/1     Running   0          11h   10.100.165.180   k8s-worker-06   <none>           <none>

NAME                                   TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)              AGE   SELECTOR
service/redis-redis-cluster            ClusterIP   10.96.7.97   <none>        6379/TCP             11h   app.kubernetes.io/instance=redis,app.kubernetes.io/name=redis-cluster
service/redis-redis-cluster-headless   ClusterIP   None         <none>        6379/TCP,16379/TCP   11h   app.kubernetes.io/instance=redis,app.kubernetes.io/name=redis-cluster

NAME                                   READY   AGE   CONTAINERS            IMAGES
statefulset.apps/redis-redis-cluster   6/6     11h   redis-redis-cluster   docker.io/bitnami/redis-cluster:7.0.4-debian-11-r4

</none></none></none></none></none></none></none></none></none></none></none></none></none></none>
```

##### 卸载

```ruby
helm delete redis -n $REDIS_NAMESPACE

```

> - **`注意`，如果首次安装失败，需要进行完全卸载才行，因为PV中会留有缓存**```ruby
>   ## 进行完全卸载，删除命名空间
>   kubectl delete ns $REDIS_NAMESPACE
>   
>   ```

##### 测试，安装客户端容器

```ruby
## 启动后会自动进入容器
kubectl run -ti --rm client-tools --image=rdocker pull cnagent/client-tools:1.0.0

## 在容器内测试，通过负载链接Redis集群
[root@client-tools app]# redis-cli -h redis-redis-cluster.redis-cluster -p 6379

## 测试Redis集群联通性
redis-redis-cluster.redis-cluster:6379> PING
PONG



```

##### 问题

```ruby
## 尝试连接 redis-redis-cluster-0
redis-cli -h redis-redis-cluster-0.redis-redis-cluster-headless.redis-cluster -p 6379
## 并且通过 redis-redis-cluster-0 进行数据库操作
redis-redis-cluster-0.redis-redis-cluster-headless.redis-cluster:6379> SET name Eric
#### 引发一个异常，告诉你要使用 10.100.165.180 也就是 redis-redis-cluster-5 进行操作
(error) MOVED 5798 10.100.165.180:6379


## 尝试连接 redis-redis-cluster-5
redis-cli -h redis-redis-cluster-5.redis-redis-cluster-headless.redis-cluster -p 6379
##
redis-redis-cluster-5.redis-redis-cluster-headless.redis-cluster:6379> SET name Eric
OK
redis-redis-cluster-5.redis-redis-cluster-headless.redis-cluster:6379> GET name
"Eric"


```

###### **疑问**，不是多主吗？为什么会这样？ **[原因在这](http://www.dev-share.top/2022/09/15/%e4%ba%86%e8%a7%a3-redis-%e9%9b%86%e7%be%a4%e5%b7%a5%e4%bd%9c%e5%8e%9f%e7%90%86/ "原因在这")**