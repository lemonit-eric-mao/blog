---
title: 'k8s 部署 rabbitmq'
date: '2019-03-15T09:47:36+00:00'
status: publish
permalink: /2019/03/15/k8s-%e9%83%a8%e7%bd%b2-rabbitmq
author: 毛巳煜
excerpt: ''
type: post
id: 3503
category:
    - Kubernetes
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
##### k8s 部署 rabbitmq

###### 查看 k8s集群版本

```ruby
[root@dev15 ~]# kubectl get node
NAME      STATUS    ROLES     AGE       VERSION
dev13     Ready     <none>    2d        v1.11.0
dev14     Ready     <none>    2d        v1.11.0
dev15     Ready     master    2d        v1.11.0
[root@dev15 ~]#
</none></none>
```

###### 查看已经运行的容器

```ruby
[root@dev15 ~]# kubectl get namespace
NAME          STATUS    AGE
default       Active    2d
kube-public   Active    2d
kube-system   Active    2d
[root@dev15 ~]#

```

##### 简单说一下 yaml

1. YAML 还有一个小的怪癖. 所有的 YAML 文件(无论和 Ansible 有没有关系)开始行都应该是 `---`. 这是 YAML 格式的一部分, 表明一个文件的开始.
2. 列表中的所有成员都开始于相同的缩进级别, 并且使用一个 `"- "` 作为开头(一个横杠和一个空格)

#### 从追踪和维护的角度出发，建议使用json或yaml的方式定义资源。

```
kubectl apply -f yaml文件名

```

###### 创建命名空间 01-k8s-Namespace.yaml

```ruby
---
# Namespace 创建命名空间
kind: Namespace
apiVersion: v1
metadata:
   # 不可以使用 下划线，
   name: paas-basic
   labels:
     name: paas-basic

```

###### 创建要部署的容器 02-k8s-Deployment.yaml

```ruby
---
# 创建要部署的容器
# 种类：告诉 k8s 下面这些配置的含义
kind: Deployment
# 版本号 规定格式 apps/* 必须这么写
apiVersion: apps/v1
metadata:
  # 所属的命名空间
  namespace: paas-basic
  # 名称
  name: rabbitmq
  # 自定义标签 TODO
  labels:
    app: rabbitmq-master
# 容器的详细定义
spec:
  # 告诉 K8s 启动几个节点
  replicas: 1
  selector:
    matchLabels:
      app: rabbitmq-master
  template:
    metadata:
      labels:
        app: rabbitmq-master
    spec:
      # 配置 Docker容器
      containers:
          # Docker容器启动后的名称
        - name: rabbitmq
          # 告诉 K8s Docker的镜像名称（此版本镜像不需要在手动启动rabbitmq webUI）
          image: rabbitmq:3-management
          # 告诉 K8s 如果本地没有这个镜像
          # 总是拉取 pull
          # imagePullPolicy: Always
          # 只使用本地镜像，从不拉取
          # imagePullPolicy: Never
          # 默认值,本地有则使用本地镜像,不拉取
          imagePullPolicy: IfNotPresent
          # 告诉 K8s Docker容器对外开放几个端口
          ports:
          - containerPort: 4369
            protocol: TCP
          - containerPort: 15672
            protocol: TCP
          - containerPort: 25672
            protocol: TCP
          - containerPort: 5671
            protocol: TCP
          - containerPort: 5672
            protocol: TCP
          env:
          - name: RABBITMQ_ERLANG_COOKIE
            value: sinoeyes
          - name: RABBITMQ_DEFAULT_USER
            value: paas
          - name: RABBITMQ_DEFAULT_PASS
            # 不能是纯数字，会报错
            value: "123456"


```

###### 为部署的容器开放端口 03-k8s-Service.yaml

```ruby
---
# 为部署的容器开放端口
# Service
kind: Service
apiVersion: v1
metadata:
  # 所属的命名空间
  namespace: paas-basic
  # 名称
  name: rabbitmq
  # 自定义标签 TODO
  labels:
    app: rabbitmq-master
# 容器的详细定义
spec:
  # 如果指定为 NodePort 则这个service的端口可以被外界访问
  type: NodePort
  # 告诉 K8s Docker容器对外开放几个端口
  ports:
    - port: 4369
      targetPort: 4369
      name: mq1
    - port: 15672
      targetPort: 15672
      name: mq2
    - port: 25672
      targetPort: 25672
      name: mq3
    - port: 5671
      targetPort: 5671
      name: mq4
    - port: 5672
      targetPort: 5672
      name: mq5
  selector:
    app: rabbitmq-master

```

###### 根据需要，配置负载均衡器（可选） 04-k8s-Ingress.yaml

```ruby
---
# Ingress 负载均衡器 (可以简单的理解成 k8s 内部的 nginx)
# 为什么不使用 Nginx？ 因为在k8s集群中，如果每加入一个服务，我们都要在Nginx中添加一个配置，不灵活！
# ingress 就可以解决这个问题
kind: Ingress
apiVersion: extensions/v1beta1
metadata:
  # 所属的命名空间
  namespace: paas-basic
  # 名称
  name: rabbitmq
spec:
  rules:
  - host: 要访问的域名，和nginx配置反向代理，道理相同
    http:
      paths:
      - path: /
        backend:
          serviceName: rabbitmq
          servicePort: 15672

```

###### 查看目录

```ruby
[root@dev15 test]# ll
总用量 32
-rw-r--r--. 1 root root   95 3月  15 17:58 01-k8s-Namespace.yaml
-rw-r--r--. 1 root root  962 3月  15 17:59 02-k8s-Deployment.yaml
-rw-r--r--. 1 root root  473 3月  15 18:00 03-k8s-Service.yaml
-rw-r--r--. 1 root root  271 3月  15 18:01 04-k8s-Ingress.yaml
[root@dev15 test]#

```

##### 执行配置文件部署

```ruby
[root@dev15 test]# kubectl apply -f 01-k8s-Namespace.yaml -f 02-k8s-Deployment.yaml -f 03-k8s-Service.yaml
namespace/paas-basic created
deployment.apps/rabbitmq created
service/rabbitmq created
[root@dev15 test]#

```

##### 查看容器运行状态

```ruby
[root@dev15 test]# kubectl get namespace -n paas-basic
NAME            STATUS    AGE
cattle-system   Active    23h
default         Active    3d
kube-public     Active    3d
kube-system     Active    3d
paas-basic      Active    1m
[root@dev15 test]#
[root@dev15 test]#
[root@dev15 test]# kubectl get deployment -n paas-basic
NAME       DESIRED   CURRENT   UP-TO-DATE   AVAILABLE   AGE
rabbitmq   1         1         1            1           1m
[root@dev15 test]#
[root@dev15 test]#
[root@dev15 test]# kubectl get service -n paas-basic
NAME       TYPE       CLUSTER-IP   EXTERNAL-IP   PORT(S)                                                                        AGE
rabbitmq   NodePort   10.97.9.6    <none>        4369:31065/TCP,15672:30880/TCP,25672:32238/TCP,5671:30421/TCP,5672:31080/TCP   1m
[root@dev15 test]#
[root@dev15 test]#
</none>
```

###### 测试

```
dev13 需要修改本地电脑 hosts 文件，  Slave节点IP dev13
在浏览器上输入  http://dev13:30880 成功后会进入 rabbitmq

```

###### 删除容器 `kubectl delete -f 你的配置文件`， 执行此命令会将由指定配置文件创建的容器相关的pod全部删除

```ruby
[root@dev15 test]#
[root@dev15 test]# kubectl delete -f 01-k8s-Namespace.yaml -f 02-k8s-Deployment.yaml -f 03-k8s-Service.yaml
namespace "paas-basic" deleted
deployment.apps "rabbitmq" deleted
service "rabbitmq" deleted
[root@dev15 test]#

```