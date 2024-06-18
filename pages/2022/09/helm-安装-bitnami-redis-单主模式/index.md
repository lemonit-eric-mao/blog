---
title: "Helm 安装 bitnami/redis 单主模式"
date: "2022-09-06"
categories: 
  - "k8s"
  - "redis"
---

#### 前置资料

###### **[安装 Helm](http://www.dev-share.top/2020/07/16/helm-%e5%ae%89%e8%a3%85-%e4%bd%bf%e7%94%a8/ "安装 Helm")**

* * *

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

| **[Redis](http://www.dev-share.top/2022/09/06/helm-%e5%ae%89%e8%a3%85-bitnami-redis/ "Redis")** | **[Redis 集群](http://www.dev-share.top/2020/07/13/helm-%e5%ae%89%e8%a3%85-bitnami-redis-%e9%9b%86%e7%be%a4/ "Redis 集群")** |
| :-: | :-: |
| 支持多个数据库 | 仅支持一个数据库。如果你有一个大数据集更好 |
| 单写点（单主） | 多个写入点（多个主控） |
| ![](http://qiniu.dev-share.top/image/png/redis-topology.png) | ![](http://qiniu.dev-share.top/image/png/redis-cluster-topology.png) |

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
cat > values.yaml << ERIC

##
global:
  ## 持久卷的全局存储类
  storageClass: "rook-ceph-block"
  ## Redis 密码（覆盖auth.password）
  redis:
    password: "******"

## 安装集群
image:
  ## 镜像下载地址
  registry: docker.io
  ## 镜像
  repository: bitnami/redis-cluster
  ## 镜像 tag
  tag: 7.0.4-debian-11-r4
  ## 是否调试
  debug: false

## 允许值：standalone 或 replication
architecture: replication

## 认证授权配置
auth:
  ## 启用密码验证
  enabled: true
  ## 在哨兵上启用密码身份验证
  sentinel: true
  ## @param auth.password Redis® password
  ## Defaults to a random 10-character alphanumeric string if not set
  ##
  password: "******"

## 主节点配置
master:
  ## 可选类型 StatefulSet（默认）或 Deployment
  kind: StatefulSet
  ## Master实例数量，只能是一个，（因为多个主之间，不能够数据同步）
  count: 1
  ## Master程序对应的k8s Service配置
  service:
    ## 可选类型 ClusterIP (默认) 与 LoadBalancer
    type: ClusterIP
    ports:
      redis: 6379

## 副本配置
replica:
  ## 要部署的 Redis® 副本数
  replicaCount: 3
  ## 副本程序对应的k8s Service配置
  service:
    ## 可选类型 ClusterIP (默认) 与 LoadBalancer
    type: ClusterIP
    ports:
      redis: 6379

## 哨兵配置
sentinel:
  ## 在 Redis® pod 上使用 Redis® Sentinel。
  enabled: false
  image:
    ## 镜像下载地址
    registry: docker.io
    ## 镜像
    repository: bitnami/redis-sentinel
    ## 镜像 tag
    tag: 7.0.4-debian-11-r14
  ## 哨兵程序对应的k8s Service配置
  service:
    ports:
      redis: 6379
      sentinel: 26379
    ## 可选类型 ClusterIP (默认) 与 LoadBalancer
    type: ClusterIP

ERIC

```

```shell
## 安装部署
helm install redis ./redis-$REDIS_VERSION.tgz -f values.yaml -n $REDIS_NAMESPACE
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
