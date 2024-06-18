---
title: 'Helm 安装 Kafka Web管理页面'
date: '2021-05-07T01:28:38+00:00'
status: private
permalink: /2021/05/07/helm-%e5%ae%89%e8%a3%85-kafka-web%e7%ae%a1%e7%90%86%e9%a1%b5%e9%9d%a2
author: 毛巳煜
excerpt: ''
type: post
id: 7220
category:
    - Kafka
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
wb_sst_seo:
    - 'a:3:{i:0;s:0:"";i:1;s:0:"";i:2;s:0:"";}'
---
###### 前置条件

```ruby
[root@master01 deploy]# kubectl -n dhc get svc
NAME                           TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)                      AGE
dhc-kafka                      ClusterIP   10.96.252.66   <none>        9092/TCP                     6d16h
dhc-kafka-headless             ClusterIP   None           <none>        9092/TCP,9093/TCP            6d16h
dhc-kafka-zookeeper            ClusterIP   10.96.79.101   <none>        2181/TCP,2888/TCP,3888/TCP   6d16h
dhc-kafka-zookeeper-headless   ClusterIP   None           <none>        2181/TCP,2888/TCP,3888/TCP   6d16h
[root@master01 deploy]#
</none></none></none></none>
```

- - - - - -

###### k8s中 安装部署 **[官方GitHub](https://github.com/obsidiandynamics/kafdrop#running-in-kubernetes-using-a-helm-chart "官方GitHub")**

```
helm upgrade -i kafdrop chart --set image.tag=3.x.x \
    --set kafka.brokerConnect=<port> \
    --set server.servlet.contextPath="/" \
    --set cmdArgs="--message.format=AVRO --schemaregistry.connect=http://localhost:8080" \ #optional
    --set jvm.opts="-Xms32M -Xmx64M"
</port>
```

```ruby
wget https://github.com/obsidiandynamics/kafdrop/archive/refs/tags/3.27.0.tar.gz && tar -zxvf 3.27.0.tar.gz && cd kafdrop-3.27.0/


helm upgrade -i kafdrop chart --set image.tag=3.27.0 \
    --set kafka.brokerConnect=dhc-kafka.dhc:9092 \
    --set server.servlet.contextPath="/" \
    --set jvm.opts="-Xms32M -Xmx64M"


NAME: kafdrop
LAST DEPLOYED: Fri May  7 09:08:24 2021
NAMESPACE: default
STATUS: deployed
REVISION: 1
TEST SUITE: None
NOTES:
1. Get the application URL by running these commands:
  export NODE_PORT=<span class="katex math inline">(kubectl get --namespace default -o jsonpath="{.spec.ports[0].nodePort}" services kafdrop)
  export NODE_IP=</span>(kubectl get nodes --namespace default -o jsonpath="{.items[0].status.addresses[0].address}")
  echo http://<span class="katex math inline">NODE_IP:</span>NODE_PORT

##　执行后输出结果：
http://192.168.103.230:30900
[root@master01 kafdrop-3.27.0]#


```

- - - - - -

###### 查看

```ruby
[root@master01 ~]# kubectl get svc,po
NAME                 TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)          AGE
service/kafdrop      NodePort    10.96.225.11   <none>        9000:30900/TCP   7m1s
service/kubernetes   ClusterIP   10.96.0.1      <none>        443/TCP          43d

NAME                          READY   STATUS    RESTARTS   AGE
pod/kafdrop-7f8c6866f-r4rf8   1/1     Running   0          7m1s
[root@master01 ~]#

</none></none>
```

- - - - - -

- - - - - -

- - - - - -