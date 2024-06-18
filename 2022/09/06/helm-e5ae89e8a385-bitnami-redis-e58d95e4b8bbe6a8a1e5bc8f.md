---
title: 'Helm 安装 bitnami/redis 单主模式'
date: '2022-09-06T03:05:13+00:00'
status: publish
permalink: /2022/09/06/helm-%e5%ae%89%e8%a3%85-bitnami-redis-%e5%8d%95%e4%b8%bb%e6%a8%a1%e5%bc%8f
author: 毛巳煜
excerpt: ''
type: post
id: 9239
category:
    - Kubernetes
    - Redis
tag: []
post_format: []
wb_sst_seo:
    - 'a:3:{i:0;s:0:"";i:1;s:0:"";i:2;s:0:"";}'
hestia_layout_select:
    - sidebar-right
---
#### 前置资料

###### **[安装 Helm](http://www.dev-share.top/2020/07/16/helm-%e5%ae%89%e8%a3%85-%e4%bd%bf%e7%94%a8/ "安装 Helm")**

- - - - - -

#### Helm 安装 bitnami/redis

```shell
helm repo add bitnami https://charts.bitnami.com/bitnami

## 查看安装版本
helm search repo list
NAME                            CHART VERSION   APP VERSION     DESCRIPTION
bitnami/kube-state-metrics      3.2.1           2.5.0           kube-state-metrics is a simple service that lis...
bitnami/redis                   17.1.3          7.0.4           部署主从集群，可选择是否启用 Redis Sentinel
bitnami/redis-cluster           8.2.1           7.0.4           部署具有分片的 Redis拓扑


```

```shell
helm repo update

## 将chart包下载到本地
export REDIS_VERSION=17.1.3
helm pull bitnami/redis --version $REDIS_VERSION

```

<table><thead><tr><th align="center">**[Redis](http://www.dev-share.top/2022/09/06/helm-%e5%ae%89%e8%a3%85-bitnami-redis/ "Redis")**</th><th align="center">**[Redis 集群](http://www.dev-share.top/2020/07/13/helm-%e5%ae%89%e8%a3%85-bitnami-redis-%e9%9b%86%e7%be%a4/ "Redis 集群")**</th></tr></thead><tbody><tr><td align="center">支持多个数据库</td><td align="center">仅支持一个数据库。如果你有一个大数据集更好</td></tr><tr><td align="center">单写点（单主）</td><td align="center">多个写入点（多个主控）</td></tr><tr><td align="center">![](http://qiniu.dev-share.top/image/png/redis-topology.png)</td><td align="center">![](http://qiniu.dev-share.top/image/png/redis-cluster-topology.png)</td></tr></tbody></table>

#### 先决条件

- Kubernetes 1.19+
- Helm 3.2.0+
- 底层基础设施中的 PV 供应商支持

#### 安装部署 Redis

```shell
## 创建命令空间
export REDIS_NAMESPACE=redis
kubectl create ns $REDIS_NAMESPACE


```

**创建`values.yaml`**

```shell
cat > values.yaml 
```

```shell
## 安装部署
helm install redis ./redis-<span class="katex math inline">REDIS_VERSION.tgz -f values.yaml -n</span>REDIS_NAMESPACE

```

```shell
#### 如果安装成功，会输出如下信息
NAME: redis
LAST DEPLOYED: Tue Sep  6 10:37:02 2022
NAMESPACE: redis
STATUS: deployed
REVISION: 1
TEST SUITE: None
NOTES:
CHART NAME: redis
CHART VERSION: 17.1.3
APP VERSION: 7.0.4

...... 省略

```

```shell
## 查看集群信息
kubectl -n redis get all -o wide
NAME                   READY   STATUS    RESTARTS   AGE     IP               NODE            NOMINATED NODE   READINESS GATES
pod/redis-master-0     1/1     Running   0          3m9s    10.100.78.223    k8s-worker-04   <none>           <none>
pod/redis-replicas-0   1/1     Running   0          3m9s    10.100.78.213    k8s-worker-04   <none>           <none>
pod/redis-replicas-1   1/1     Running   0          2m17s   10.100.55.216    k8s-worker-05   <none>           <none>
pod/redis-replicas-2   1/1     Running   0          96s     10.100.165.179   k8s-worker-06   <none>           <none>

NAME                     TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)    AGE    SELECTOR
service/redis-headless   ClusterIP   None           <none>        6379/TCP   3m9s   app.kubernetes.io/instance=redis,app.kubernetes.io/name=redis
service/redis-master     ClusterIP   10.96.191.26   <none>        6379/TCP   3m9s   app.kubernetes.io/component=master,app.kubernetes.io/instance=redis,app.kubernetes.io/name=redis
service/redis-replicas   ClusterIP   10.96.36.130   <none>        6379/TCP   3m9s   app.kubernetes.io/component=replica,app.kubernetes.io/instance=redis,app.kubernetes.io/name=redis

NAME                              READY   AGE    CONTAINERS   IMAGES
statefulset.apps/redis-master     1/1     3m9s   redis        docker.io/bitnami/redis-cluster:7.0.4-debian-11-r4
statefulset.apps/redis-replicas   3/3     3m9s   redis        docker.io/bitnami/redis-cluster:7.0.4-debian-11-r4

</none></none></none></none></none></none></none></none></none></none></none>
```

##### 卸载

```ruby
helm delete redis -n $REDIS_NAMESPACE

```

##### 测试，安装客户端容器

```shell
## 启动后会自动进入容器
kubectl run -ti --rm client-tools --image=rdocker pull cnagent/client-tools:1.0.0

## 在容器内测试，通过负载链接Redis集群
[root@client-tools app]# redis-cli -h redis-master.redis -p 6379

## 输入登录密码
redis-master.redis:6379> auth ******
OK

## 测试Redis集群联通性
redis-master.redis:6379> PING
PONG

redis-master.redis:6379> SET name Eric
OK

redis-master.redis:6379> GET name
"Eric"


```

##### 测试，副本节点读写

```shell
## 尝试连接 redis-replicas
redis-cli -h redis-replicas.redis -p 6379
redis-replicas.redis:6379> auth ******
OK

## 测试 读
redis-replicas.redis:6379> GET name
"Eric"

## 测试 写
redis-replicas.redis:6379> SET name Eric
(error) READONLY You can't write against a read only replica.


```