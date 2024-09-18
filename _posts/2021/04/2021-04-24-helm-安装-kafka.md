---
title: "Helm 安装 kafka"
date: "2021-04-24"
categories: 
  - "kafka"
---

###### 前置条件

CentOS 7.7+ 系统内核 5.11.6-1.el7.elrepo.x86\_64 硬盘 2块 K8S 1.20.x containerd 1.4.4 **[RookCeph 1.5.10](%e4%bd%bf%e7%94%a8-rook-%e5%ae%89%e8%a3%85%e7%ae%a1%e7%90%86-k8s%e6%8c%81%e4%b9%85%e5%8c%96%e5%ad%98%e5%82%a8 "RookCeph 1.5.10")**

```ruby
[root@master01 rbd]#  kubectl -n rook-ceph get sc
NAME              PROVISIONER                  RECLAIMPOLICY   VOLUMEBINDINGMODE   ALLOWVOLUMEEXPANSION   AGE
rook-ceph-block   rook-ceph.rbd.csi.ceph.com   Delete          Immediate           true                   29m
[root@master01 rbd]#
```

* * *

* * *

* * *

###### **[bitnami/kafka](https://github.com/bitnami/charts/tree/master/bitnami/kafka "bitnami/kafka")**

###### **[安装Helm](helm-%e5%ae%89%e8%a3%85-%e4%bd%bf%e7%94%a8 "安装Helm")**

* * *

###### 安装

```ruby
helm repo add bitnami https://charts.bitnami.com/bitnami

helm search repo bitnami/kafka
NAME            CHART VERSION   APP VERSION     DESCRIPTION
bitnami/kafka   18.4.4          3.2.3           Apache Kafka is a distributed streaming platfor...


## 配置版本号
export KAFKA_CHART_VERSION=18.4.4
helm pull bitnami/kafka --version $KAFKA_CHART_VERSION


## 创建命名空间
export KAFKA_ING_NAMESPACE=kafka-ns
kubectl create ns $KAFKA_ING_NAMESPACE


## 安装部署
helm install kafka-3-2-3 ./kafka-$KAFKA_CHART_VERSION.tgz \
  --namespace $KAFKA_ING_NAMESPACE \
  --set replicaCount=3 \
  --set global.storageClass='rook-ceph-block' \
  --set persistence.storageClass='rook-ceph-block'

## 输出日志
NAME: kafka-3-2-3
LAST DEPLOYED: Fri Sep 23 17:44:08 2022
NAMESPACE: kafka-ns
STATUS: deployed
REVISION: 1
TEST SUITE: None
NOTES:
CHART NAME: kafka
CHART VERSION: 18.4.4
APP VERSION: 3.2.3

** Please be patient while the chart is being deployed **

Kafka can be accessed by consumers via port 9092 on the following DNS name from within your cluster:

    kafka-3-2-3.kafka-ns.svc.cluster.local

Each Kafka broker can be accessed by producers via port 9092 on the following DNS name(s) from within your cluster:

    kafka-3-2-3-0.kafka-3-2-3-headless.kafka-ns.svc.cluster.local:9092
    kafka-3-2-3-1.kafka-3-2-3-headless.kafka-ns.svc.cluster.local:9092
    kafka-3-2-3-2.kafka-3-2-3-headless.kafka-ns.svc.cluster.local:9092

To create a pod that you can use as a Kafka client run the following commands:

    kubectl run kafka-3-2-3-client --restart='Never' --image docker.io/bitnami/kafka:3.2.3-debian-11-r1 --namespace kafka-ns --command -- sleep infinity
    kubectl exec --tty -i kafka-3-2-3-client --namespace kafka-ns -- bash

    PRODUCER:
        kafka-console-producer.sh \

            --broker-list kafka-3-2-3-0.kafka-3-2-3-headless.kafka-ns.svc.cluster.local:9092,kafka-3-2-3-1.kafka-3-2-3-headless.kafka-ns.svc.cluster.local:9092,kafka-3-2-3-2.kafka-3-2-3-headless.kafka-ns.svc.cluster.local:9092 \
            --topic test

    CONSUMER:
        kafka-console-consumer.sh \

            --bootstrap-server kafka-3-2-3.kafka-ns.svc.cluster.local:9092 \
            --topic test \
            --from-beginning

[root@master01 ~]#

```

```ruby
## 卸载
helm uninstall kafka-3-2-3 -n $KAFKA_ING_NAMESPACE

```

* * *

###### 查看 kafka的pvc

创建pvc过程有点慢，需要等待

```ruby
[root@master01 ~]# kubectl get pvc -n $KAFKA_ING_NAMESPACE
NAME                           STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS      AGE
data-kafka-3-2-3-0             Bound    pvc-9d270ed2-2547-487f-9260-378afff57cde   8Gi        RWO            rook-ceph-block   3m10s
data-kafka-3-2-3-1             Bound    pvc-d0777012-7ee7-43c4-94d4-4f9f67428f88   8Gi        RWO            rook-ceph-block   3m10s
data-kafka-3-2-3-2             Bound    pvc-f6efd45a-32ae-4f4e-a71b-5d5e400db8cf   8Gi        RWO            rook-ceph-block   3m10s
data-kafka-3-2-3-zookeeper-0   Bound    pvc-4b3a399f-dccd-40c6-ac8b-b33fd22cc196   8Gi        RWO            rook-ceph-block   3m10s
[root@master01 ~]#

```

* * *

###### 查看kafka

```ruby
[root@master01 ~]# kubectl get svc,po -n $KAFKA_ING_NAMESPACE
NAME                                     TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)                      AGE
service/kafka-3-2-3                      ClusterIP   10.96.91.218    <none>        9092/TCP                     4m14s
service/kafka-3-2-3-headless             ClusterIP   None            <none>        9092/TCP,9093/TCP            4m14s
service/kafka-3-2-3-zookeeper            ClusterIP   10.96.225.245   <none>        2181/TCP,2888/TCP,3888/TCP   4m14s
service/kafka-3-2-3-zookeeper-headless   ClusterIP   None            <none>        2181/TCP,2888/TCP,3888/TCP   4m14s

NAME                          READY   STATUS              RESTARTS   AGE
pod/kafka-3-2-3-0             0/1     ContainerCreating   0          4m14s
pod/kafka-3-2-3-1             0/1     ContainerCreating   0          4m14s
pod/kafka-3-2-3-2             0/1     ContainerCreating   0          4m14s
pod/kafka-3-2-3-zookeeper-0   0/1     ContainerCreating   0          4m14s
[root@master01 ~]#

```

* * *

###### **[安装Web管理页面](helm-%e5%ae%89%e8%a3%85-kafka-web%e7%ae%a1%e7%90%86%e9%a1%b5%e9%9d%a2 "安装Web管理页面")**

* * *

* * *

* * *

* * *

* * *

* * *

###### 常用命令

```ruby
kubectl exec -it -n dhc dhc-kafka-0 -- bash /opt/bitnami/kafka/bin/kafka-topics.sh --zookeeper 10.96.79.101:2181 --list

```

* * *

* * *

* * *
